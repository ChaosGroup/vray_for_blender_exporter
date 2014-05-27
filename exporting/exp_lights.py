#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

from vb30.lib     import BlenderUtils, SysUtils, ExportUtils, LibUtils
from vb30.nodes   import export as NodesExport
from vb30.plugins import PLUGINS

from vb30 import debug


def ExportLamp(bus):
    scene = bus['scene']
    ob    = bus['node']['object']

    lamp     = ob.data
    VRayLamp = lamp.vray

    lamp_name   = BlenderUtils.GetObjectName(ob, prefix='LA')
    lamp_matrix = ob.matrix_world

    lightPluginName = LibUtils.GetLightPluginName(lamp)

    lightPropGroup = getattr(VRayLamp, lightPluginName)

    # Check if we have a node tree and export it
    #
    socketParams = {
        'transform' : lamp_matrix,
    }

    if VRayLamp.ntree:
        lightNode = NodesExport.GetNodeByType(VRayLamp.ntree, 'VRayNode%s' % lightPluginName)
        if lightNode:
            for nodeSocket in lightNode.inputs:
                vrayAttr = nodeSocket.vray_attr
                value = NodesExport.WriteConnectedNode(bus, VRayLamp.ntree, nodeSocket, linkedOnly=True)
                if value is not None:
                    socketParams[vrayAttr] = value

    if lamp.type == 'AREA':
        if lamp.shape == 'RECTANGLE':
            socketParams['u_size'] = lamp.size   / 2.0
            socketParams['v_size'] = lamp.size_y / 2.0
        else:
            socketParams['u_size'] = lamp.size / 2.0
            socketParams['v_size'] = lamp.size / 2.0
    elif lamp.type == 'SPOT':
        if lamp.vray.spot_type == 'SPOT':
            socketParams['fallsize'] = lamp.spot_size
        elif lamp.vray.spot_type == 'IES':
            pass
    elif lamp.type == 'SUN':
        if lamp.vray.direct_type == 'DIRECT':
            pass
        elif lamp.vray.direct_type == 'SUN':
            pass

    # Check 'Render Elements' and add light to channels
    #
    if scene.vray.ntree:
        passesNode = NodesExport.GetNodeByType(scene.vray.ntree, 'VRayNodeRenderChannels')
        if passesNode:
            listRenderElements = {
                'channels_raw'      : [],
                'channels_diffuse'  : [],
                'channels_specular' : [],
            }

            for socket in passesNode.inputs:
                if not socket.is_linked or not socket.use:
                    continue

                lightSelectNode = NodesExport.GetConnectedNode(scene.vray.ntree, socket)
                if not lightSelectNode or not lightSelectNode.bl_idname == 'VRayNodeRenderChannelLightSelect':
                    continue

                lightsSocket = lightSelectNode.inputs['Lights']
                if not lightsSocket.is_linked:
                    continue

                lightSelectChannelName = NodesExport.GetNodeName(scene.vray.ntree, lightSelectNode)

                lightGroup = NodesExport.WriteConnectedNode(bus, scene.vray.ntree, lightsSocket)
                for l in lightGroup:
                    if not l.type == 'LAMP':
                        continue
                    if not l == ob:
                        continue

                    lightChannelType = lightSelectNode.RenderChannelLightSelect.type

                    if lightChannelType == 'RAW':
                        listRenderElements['channels_raw'].append(lightSelectChannelName)
                    elif lightChannelType == 'DIFFUSE':
                        listRenderElements['channels_diffuse'].append(lightSelectChannelName)
                    elif lightChannelType == 'SPECULAR':
                        listRenderElements['channels_specular'].append(lightSelectChannelName)

            for key in listRenderElements:
                socketParams[key] = "List(%s)" % ",".join(listRenderElements[key])

    # Write light
    ExportUtils.WritePlugin(
        bus,
        PLUGINS['LIGHT'][lightPluginName],
        lamp_name,
        lightPropGroup,
        socketParams
    )

    if VRayLamp.use_include_exclude:
        bus['lightlinker'][lamp_name] = {}

        if VRayLamp.use_include:
            bus['lightlinker'][lamp_name]['include'] = BlenderUtils.GetObjectList(VRayLamp.include_objects, VRayLamp.include_groups)

        if VRayLamp.use_exclude:
            bus['lightlinker'][lamp_name]['exclude'] = BlenderUtils.GetObjectList(VRayLamp.exclude_objects, VRayLamp.exclude_groups)


@debug.TimeIt
def ExportLights(bus):
    scene = bus['scene']

    for ob in BlenderUtils.SceneLampIt(scene):
        if not BlenderUtils.ObjectVisible(bus, ob):
            continue

        bus['node'] = {
            'object' : ob,
        }

        ExportLamp(bus)

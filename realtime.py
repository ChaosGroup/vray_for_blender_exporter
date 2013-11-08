#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

import bpy

from bpy.app.handlers import persistent

from vb25.plugins import PLUGINS_ID

from vb25.nodes import export as NodeExport
from vb25.debug import Debug

from vb25.lib.VRayStream import VRayStream
from vb25.lib import utils as LibUtils
from vb25.lib import ExportUtils

from vb25 import utils
from vb25 import export


@persistent
def scene_update_post(scene, context=None, is_viewport=True):
    if not (bpy.data.node_groups.is_updated or
            bpy.data.lamps.is_updated or
            bpy.data.cameras.is_updated or
            bpy.data.scenes.is_updated or
            bpy.data.objects.is_updated):
        return

    if not scene.render.engine == 'VRAY_RENDER_RT':
        return

    if not VRayStream.process.is_running():
        return

    Debug("scene_update_post()", msgType='ERROR')

    VRayStream.setMode('SOCKET')

    bus = {
        # Data exporter
        # Refactor this if needed
        'output' : VRayStream,

        # We always need to access scene data
        'scene' : scene,

        # Current frame
        'frame' : scene.frame_current,

        # Active camera
        'camera' : scene.camera,

        # We will override some params in case of preview
        'preview' : False,

        # Set of environment effects objects
        'volumes' : set(),

        # Set of fog gizmos, to exclude from 'Node' creation
        'gizmos' : set(),

        # Prevents export data duplication
        'cache' : {
            'plugins' : set(),
            'mesh'    : set(),
            'nodes'   : set(),
        },

        # We need to know render engine type
        'engine' : 'VRAY_RENDER_RT',

        # Some storage
        'context' : {},

        # Fail safe defaults
        'defaults' : {
            'brdf' : "BRDFNOBRDFISSET",
            'material' : "MANOMATERIALISSET",
            'texture' : "TENOTEXTUREIESSET",
            'uvwgen' : "DEFAULTUVWC",
            'blend' : "TEDefaultBlend",
        },

        'node' : {},

        'is_viewport' : is_viewport,
        'bContext' : context,
    }

    VRayScene = scene.vray

    if bpy.data.node_groups.is_updated:
        for ntree in bpy.data.node_groups:
            if not ntree.is_updated or not ntree.is_updated_data:
                continue

            if ntree.bl_idname in {'VRayNodeTreeMaterial'}:
                NodeExport.WriteVRayMaterialNodeTree(bus, ntree)

        VRayStream.commit()

    if bpy.data.objects.is_updated:
        for ob in export.GetObjects(bus, checkUpdated=True):
            bus['node'] = {
                'object' : ob,
                'visible' : ob,
                'base' : ob,
                'dupli' : {},
                'particle' : {},
            }

            if ob.type == 'LAMP':
                export.write_lamp(bus)
            elif ob.type == 'EMPTY':
                pass
            elif ob.type == 'CAMERA':
                VRayCamera = ob.data.vray

                for pluginName in {'RenderView', 'SettingsCamera', 'CameraPhysical'}:
                    pluginModule = PLUGINS_ID[pluginName]
                    propGroup = getattr(VRayCamera, pluginName)

                    overrideParams = {}

                    ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)
            else:
                pluginName = utils.get_name(ob, prefix='OB')

                VRayStream.set('OBJECT', 'Node', pluginName)
                VRayStream.writeAttibute('transform', LibUtils.FormatValue(ob.matrix_world))

        VRayStream.commit()

    for pluginName in {'SettingsRTEngine'}:
        pluginModule = PLUGINS_ID[pluginName]
        propGroup = getattr(VRayScene, pluginName)

        overrideParams = {}

        ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

    PLUGINS_ID['SettingsEnvironment'].write(bus)

    VRayStream.commit()


def register():
    bpy.app.handlers.scene_update_post.append(scene_update_post)


def unregister():
    bpy.app.handlers.scene_update_post.remove(scene_update_post)

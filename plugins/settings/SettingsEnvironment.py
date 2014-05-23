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

import bpy

from vb30.lib import LibUtils
from vb30.nodes import export as NodesExport


TYPE = 'SETTINGS'
ID   = 'SettingsEnvironment'
NAME = 'Environment & Effects'
DESC = "Environment and effects"


######## ######## ######## ########  ######  ########  ######  
##       ##       ##       ##       ##    ##    ##    ##    ## 
##       ##       ##       ##       ##          ##    ##       
######   ######   ######   ######   ##          ##     ######  
##       ##       ##       ##       ##          ##          ## 
##       ##       ##       ##       ##    ##    ##    ##    ## 
######## ##       ##       ########  ######     ##     ######  

def WriteEffects(bus, ntree, node):
    for nodeSocket in node.inputs:
        if nodeSocket.use:
            NodesExport.WriteConnectedNode(bus, ntree, nodeSocket)


######## ##    ## ##     ## #### ########   #######  ##    ## ##     ## ######## ##    ## ######## 
##       ###   ## ##     ##  ##  ##     ## ##     ## ###   ## ###   ### ##       ###   ##    ##    
##       ####  ## ##     ##  ##  ##     ## ##     ## ####  ## #### #### ##       ####  ##    ##    
######   ## ## ## ##     ##  ##  ########  ##     ## ## ## ## ## ### ## ######   ## ## ##    ##    
##       ##  ####  ##   ##   ##  ##   ##   ##     ## ##  #### ##     ## ##       ##  ####    ##    
##       ##   ###   ## ##    ##  ##    ##  ##     ## ##   ### ##     ## ##       ##   ###    ##    
######## ##    ##    ###    #### ##     ##  #######  ##    ## ##     ## ######## ##    ##    ##    

def WriteEnvironment(bus, ntree, node):
    scene = bus['scene']
    o     = bus['output']

    volumes = bus.get('environment_volume', ())

    VRayWorld = scene.world.vray

    lLevel = VRayWorld.global_light_level
    global_light_level = mathutils.Color((lLevel,lLevel,lLevel))

    if node is None:
        o.set('WORLD', ID, 'SettingsEnvironment')
        o.writeHeader()
        o.writeAttibute('global_light_level', global_light_level)
        o.writeAttibute('environment_volume', "List(%s)" % (','.join(volumes)))
        o.writeFooter()
        return

    socketParams = {}
    for nodeSocket in node.inputs:
        vrayAttr = nodeSocket.vray_attr
        socketParams[vrayAttr] = NodesExport.WriteConnectedNode(bus, ntree, nodeSocket)

    o.set('WORLD', ID, 'SettingsEnvironment')
    o.writeHeader()
    o.writeAttibute('global_light_level', global_light_level)
    o.writeAttibute('environment_volume', "List(%s)" % (','.join(volumes)))
    o.writeAttibute('bg_color', "Color(0.0,0.0,0.0)")
    o.writeAttibute('bg_tex_mult', 1.0)
    o.writeAttibute('gi_color', "Color(0.0,0.0,0.0)")
    o.writeAttibute('gi_tex_mult', 1.0)
    o.writeAttibute('reflect_color', "Color(0.0,0.0,0.0)")
    o.writeAttibute('reflect_tex_mult', 1.0)
    o.writeAttibute('refract_color', "Color(0.0,0.0,0.0)")
    o.writeAttibute('refract_tex_mult', 1.0)

    o.writeAttibute('bg_tex', socketParams.get('bg_tex', node.inputs['Background'].value))

    for override in {'gi_tex', 'reflect_tex', 'refract_tex'}:
        value = None

        if override in socketParams and getattr(node, override):
            value = socketParams[override]
        else:
            value = socketParams.get('bg_tex', None)

        if value:
            o.writeAttibute(override, value)

    o.writeFooter()


def write(bus):
    scene = bus['scene']

    ntree = scene.world.vray.ntree
    if not ntree:
        return 

    outputNode = NodesExport.GetNodeByType(ntree, 'VRayNodeWorldOutput')
    if not outputNode:
        return

    # Effects must be always exported before Environment
    # because of 'environment_volume' attribute
    #
    effectsSocket = outputNode.inputs['Effects']
    if effectsSocket.is_linked:
        effectsNode = NodesExport.GetConnectedNode(ntree, effectsSocket)
        if effectsNode:
            WriteEffects(bus, ntree, effectsNode)

    environmentSocket = outputNode.inputs['Environment']
    environmentNode = NodesExport.GetConnectedNode(ntree, environmentSocket)
    WriteEnvironment(bus, ntree, environmentNode)

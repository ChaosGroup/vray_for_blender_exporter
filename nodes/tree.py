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

# TODO:
#   Use "idref" for tree storage:
#     http://www.pasteall.org/46081/python
#     http://www.pasteall.org/46083/python

import bpy

from vb25.ui import classes


class VRayData:
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in classes.VRayEngines


##     ##    ###    ######## ######## ########  ####    ###    ##       
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##       
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##       
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##       
##     ## #########    ##    ##       ##   ##    ##  ######### ##       
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##       
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ######## 

class VRayNodeTree(bpy.types.NodeTree, VRayData):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayShaderTreeType'
    bl_icon   = 'VRAY_LOGO'

    # Return a node tree from the context to be used in the editor
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma != None:
                nt_name = ma.vray.nodetree
                if nt_name != '' and nt_name in bpy.data.node_groups:
                    return bpy.data.node_groups[ma.vray.nodetree], ma, ma
        elif ob and ob.type == 'LAMP':
            la = ob.data
            nt_name = la.vray.nodetree
            if nt_name != '' and nt_name in bpy.data.node_groups:
                return bpy.data.node_groups[la.vray.nodetree], la, la
        return (None, None, None)


class VRayTreeNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayShaderTreeType'


##      ##  #######  ########  ##       ########  
##  ##  ## ##     ## ##     ## ##       ##     ## 
##  ##  ## ##     ## ##     ## ##       ##     ## 
##  ##  ## ##     ## ########  ##       ##     ## 
##  ##  ## ##     ## ##   ##   ##       ##     ## 
##  ##  ## ##     ## ##    ##  ##       ##     ## 
 ###  ###   #######  ##     ## ######## ########  

class VRayWorldNodeTree(bpy.types.NodeTree, VRayData):
    bl_label  = "V-Ray World Node Tree"
    bl_idname = 'VRayWorldNodeTree'
    bl_icon   = 'VRAY_LOGO'

    @classmethod
    def get_from_context(cls, context):
        world = None
        if hasattr(context.scene, 'world'):
            world = context.scene.world

        if world is None:
            return (None, None, None)

        ntreeName = world.vray.nodetree
        if ntreeName and ntreeName in bpy.data.node_groups:
            return bpy.data.node_groups[ntreeName], world, world

        return (None, None, None)


class VRayWorldNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayWorldNodeTree'

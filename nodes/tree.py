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

from pynodes_framework import parameter, base, group

from vb25.ui import classes


class VRayData():
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

class VRayTreeSockets(bpy.types.NodeSocket, base.NodeSocket):
    bl_idname = "VRayTreeSockets"
 
    parameter_types = [parameter.NodeParamFloat, parameter.NodeParamInt, parameter.NodeParamBool, parameter.NodeParamColor,
                       parameter.NodeParamVector, parameter.NodeParamPoint, parameter.NodeParamNormal, parameter.NodeParamMatrix,
                       parameter.NodeParamString]


class VRayNodeTree(bpy.types.NodeTree, base.NodeTree, VRayData):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayShaderTreeType'
    bl_icon   = 'MATERIAL'

    # !!! Associates trees with a socket type, needed for node group interfaces
    socket_type = VRayTreeSockets

    # Return a node tree from the context to be used in the editor
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma != None:
                if ma.vray.ntree:
                    return ma.vray.ntree, ma, ma
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

class VRayWorldNodeTree(bpy.types.NodeTree, base.NodeTree, VRayData):
    bl_label  = "V-Ray World Node Tree"
    bl_idname = 'VRayWorldNodeTree'
    bl_icon   = 'WORLD'

    @classmethod
    def get_from_context(cls, context):
        world = None
        if hasattr(context.scene, 'world'):
            world = context.scene.world

        if world is None:
            return (None, None, None)

        if world.vray.ntree:
            return world.vray.ntree, world, world

        return (None, None, None)


class VRayWorldNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayWorldNodeTree'


 #######  ########        ## ########  ######  ######## 
##     ## ##     ##       ## ##       ##    ##    ##    
##     ## ##     ##       ## ##       ##          ##    
##     ## ########        ## ######   ##          ##    
##     ## ##     ## ##    ## ##       ##          ##    
##     ## ##     ## ##    ## ##       ##    ##    ##    
 #######  ########   ######  ########  ######     ##    

class VRayNodeTreeObject(bpy.types.NodeTree, base.NodeTree, VRayData):
    bl_label  = "V-Ray Object Node Tree"
    bl_idname = 'VRayNodeTreeObject'
    bl_icon   = 'OBJECT_DATA'

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            if ob.vray.ntree:
                return ob.vray.ntree, ob, ob
        return (None, None, None)


class VRayObjectNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayNodeTreeObject'


##       ####  ######   ##     ## ######## 
##        ##  ##    ##  ##     ##    ##    
##        ##  ##        ##     ##    ##    
##        ##  ##   #### #########    ##    
##        ##  ##    ##  ##     ##    ##    
##        ##  ##    ##  ##     ##    ##    
######## ####  ######   ##     ##    ##      

class VRayNodeTreeLight(bpy.types.NodeTree, base.NodeTree, VRayData):
    bl_label  = "V-Ray Light Node Tree"
    bl_idname = 'VRayNodeTreeLight'
    bl_icon   = 'LAMP_SUN'

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type == 'LAMP':
            if ob.data.vray.ntree:
                return ob.data.vray.ntree, ob.data, ob.data
        return (None, None, None)


class VRayLightNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayNodeTreeLight'


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

def GetRegClasses():
    return (
        VRayNodeTree,
        VRayNodeTreeObject,
        VRayNodeTreeLight,
        VRayWorldNodeTree,
    )


def register():
    for regClass in GetRegClasses():
        # Only for NodeGroup:
        #  regClass.register_class()
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

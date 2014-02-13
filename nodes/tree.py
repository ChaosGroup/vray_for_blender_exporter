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

from pynodes_framework import parameter, base, group, category

from vb30.ui import classes


class VRayData():
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in classes.VRayEngines


class VRayTreeSockets(bpy.types.NodeSocket, base.NodeSocket):
    bl_idname = "VRayTreeSockets"

    parameter_types = [parameter.NodeParamFloat, parameter.NodeParamInt, parameter.NodeParamBool, parameter.NodeParamColor,
                       parameter.NodeParamVector, parameter.NodeParamPoint, parameter.NodeParamNormal, parameter.NodeParamMatrix,
                       parameter.NodeParamString]


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

class VRayNodeTree(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayNodeTreeMaterial'
    bl_icon   = 'VRAY_MATERIAL'

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
        return node_tree.bl_idname == 'VRayNodeTreeMaterial'


##      ##  #######  ########  ##       ########
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ########  ##       ##     ##
##  ##  ## ##     ## ##   ##   ##       ##     ##
##  ##  ## ##     ## ##    ##  ##       ##     ##
 ###  ###   #######  ##     ## ######## ########

class VRayNodeTreeWorld(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray World Node Tree"
    bl_idname = 'VRayNodeTreeWorld'
    bl_icon   = 'VRAY_WORLD'

    socket_type = VRayTreeSockets

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
        return node_tree.bl_idname == 'VRayNodeTreeWorld'


 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##

class VRayNodeTreeObject(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray Object Node Tree"
    bl_idname = 'VRayNodeTreeObject'
    bl_icon   = 'VRAY_OBJECT'

    socket_type = VRayTreeSockets

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

class VRayNodeTreeLight(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray Light Node Tree"
    bl_idname = 'VRayNodeTreeLight'
    bl_icon   = 'VRAY_LIGHT'

    socket_type = VRayTreeSockets

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


 ######   ######  ######## ##    ## ######## 
##    ## ##    ## ##       ###   ## ##       
##       ##       ##       ####  ## ##       
 ######  ##       ######   ## ## ## ######   
      ## ##       ##       ##  #### ##       
##    ## ##    ## ##       ##   ### ##       
 ######   ######  ######## ##    ## ######## 

class VRayNodeTreeScene(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray Scene Node Tree"
    bl_idname = 'VRayNodeTreeScene'
    bl_icon   = 'VRAY_RENDER_LAYERS'

    socket_type = VRayTreeSockets

    @classmethod
    def get_from_context(cls, context):
        if context.scene.vray.ntree:
            return context.scene.vray.ntree, context.scene, context.scene
        return (None, None, None)


class VRaySceneNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayNodeTreeScene'


######## ########  #### ########  #######  ########  
##       ##     ##  ##     ##    ##     ## ##     ## 
##       ##     ##  ##     ##    ##     ## ##     ## 
######   ##     ##  ##     ##    ##     ## ########  
##       ##     ##  ##     ##    ##     ## ##   ##   
##       ##     ##  ##     ##    ##     ## ##    ##  
######## ########  ####    ##     #######  ##     ## 

class VRayNodeTreeEditor(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree, VRayData):
    bl_label  = "V-Ray Node Tree Editor"
    bl_idname = 'VRayNodeTreeEditor'
    bl_icon   = 'NODETREE'

    socket_type = VRayTreeSockets

    @classmethod
    def get_from_context(cls, context):
        VRayExporter = context.scene.vray.Exporter

        listIndex = VRayExporter.ntreeListIndex if VRayExporter.ntreeListIndex >= 0 else 0

        if len(bpy.data.node_groups):
            ntree = bpy.data.node_groups[listIndex]
            if ntree:
                return ntree, context.scene, context.scene

        return (None, None, None)


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
        VRayNodeTreeWorld,
        VRayNodeTreeScene,

        VRayNodeTreeEditor,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)
        # regClass.register_categories()


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

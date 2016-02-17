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

from vb30.lib import BlenderUtils
from vb30.ui import classes


class VRayNodeTree(bpy.types.NodeTree):
    bl_update_event = True

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

class VRayNodeTreeMaterial(VRayNodeTree):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayNodeTreeMaterial'
    bl_icon   = 'VRAY_MATERIAL'

    bl_update_preview = True

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma and ma.vray.ntree:
                return ma.vray.ntree, None, None
        return (None, None, None)


##      ##  #######  ########  ##       ########
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ########  ##       ##     ##
##  ##  ## ##     ## ##   ##   ##       ##     ##
##  ##  ## ##     ## ##    ##  ##       ##     ##
 ###  ###   #######  ##     ## ######## ########

class VRayNodeTreeWorld(VRayNodeTree):
    bl_label  = "V-Ray World Node Tree"
    bl_idname = 'VRayNodeTreeWorld'
    bl_icon   = 'VRAY_WORLD'

    bl_update_preview = True

    @classmethod
    def get_from_context(cls, context):
        if hasattr(context.scene, 'world'):
            world = context.scene.world
            if world and world.vray.ntree:
                return world.vray.ntree, None, None
        return (None, None, None)



 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##

class VRayNodeTreeObject(VRayNodeTree):
    bl_label  = "V-Ray Object Node Tree"
    bl_idname = 'VRayNodeTreeObject'
    bl_icon   = 'VRAY_OBJECT'

    bl_update_preview = True

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in BlenderUtils.NonGeometryTypes:
            if ob.vray.ntree:
                return ob.vray.ntree, None, None
        return (None, None, None)


##       ####  ######   ##     ## ########
##        ##  ##    ##  ##     ##    ##
##        ##  ##        ##     ##    ##
##        ##  ##   #### #########    ##
##        ##  ##    ##  ##     ##    ##
##        ##  ##    ##  ##     ##    ##
######## ####  ######   ##     ##    ##

class VRayNodeTreeLight(VRayNodeTree):
    bl_label  = "V-Ray Light Node Tree"
    bl_idname = 'VRayNodeTreeLight'
    bl_icon   = 'VRAY_LIGHT'

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type == 'LAMP':
            if ob.data.vray.ntree:
                return ob.data.vray.ntree, None, None
        return (None, None, None)


 ######   ######  ######## ##    ## ########
##    ## ##    ## ##       ###   ## ##
##       ##       ##       ####  ## ##
 ######  ##       ######   ## ## ## ######
      ## ##       ##       ##  #### ##
##    ## ##    ## ##       ##   ### ##
 ######   ######  ######## ##    ## ########

class VRayNodeTreeScene(VRayNodeTree):
    bl_label  = "V-Ray Scene Node Tree"
    bl_idname = 'VRayNodeTreeScene'
    bl_icon   = 'VRAY_RENDER_LAYERS'

    @classmethod
    def get_from_context(cls, context):
        if context.scene.vray.ntree:
            return context.scene.vray.ntree, None, None
        return (None, None, None)


######## ########  #### ########  #######  ########
##       ##     ##  ##     ##    ##     ## ##     ##
##       ##     ##  ##     ##    ##     ## ##     ##
######   ##     ##  ##     ##    ##     ## ########
##       ##     ##  ##     ##    ##     ## ##   ##
##       ##     ##  ##     ##    ##     ## ##    ##
######## ########  ####    ##     #######  ##     ##

class VRayNodeTreeEditor(VRayNodeTree):
    bl_label  = "V-Ray Node Tree Editor"
    bl_idname = 'VRayNodeTreeEditor'
    bl_icon   = 'NODETREE'

    @classmethod
    def get_from_context(cls, context):
        VRayExporter = context.scene.vray.Exporter

        listIndex = VRayExporter.ntreeListIndex if VRayExporter.ntreeListIndex >= 0 else 0
        nNodeGroups = len(bpy.data.node_groups)

        if nNodeGroups:
            if listIndex >= nNodeGroups:
                VRayExporter.ntreeListIndex = 0
                listIndex                   = 0

            ntree = bpy.data.node_groups[listIndex]
            if ntree:
                return ntree, context.scene, context.scene

        return (None, None, None)


class VRayNodeTreeMaterialEditor(VRayNodeTree):
    bl_label  = "V-Ray Material Editor"
    bl_idname = 'VRayNodeTreeMaterialEditor'
    bl_icon   = 'MATERIAL'

    @classmethod
    def get_from_context(cls, context):
        VRayExporter = context.scene.vray.Exporter

        listIndex = VRayExporter.materialListIndex if VRayExporter.materialListIndex >= 0 else 0
        numMaterials = len(bpy.data.materials)

        if numMaterials:
            if listIndex >= numMaterials:
                VRayExporter.materialListIndex = 0
                listIndex                   = 0

            material = bpy.data.materials[listIndex]
            if material:
                return material.vray.ntree, material, material

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
        VRayNodeTreeMaterial,
        VRayNodeTreeObject,
        VRayNodeTreeLight,
        VRayNodeTreeWorld,
        VRayNodeTreeScene,

        VRayNodeTreeEditor,
        VRayNodeTreeMaterialEditor,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

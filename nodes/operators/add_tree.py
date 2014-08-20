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

import os

import bpy

from vb30.lib import LibUtils
from vb30.lib import BlenderUtils

from .. import tree_defaults
from .. import tools as NodesTools


class VRAY_OT_add_nodetree_light(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_light"
    bl_label       = "Add Light Nodetree"
    bl_description = "Add light nodetree"

    def execute(self, context):
        tree_defaults.AddLampNodeTree(context.object.data)
        bpy.ops.vray.show_ntree(data='OBJECT')
        return {'FINISHED'}


class VRAY_OT_add_nodetree_scene(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_scene"
    bl_label       = "Add Scene Nodetree"
    bl_description = "Add scene nodetree"

    def execute(self, context):
        tree_defaults.AddSceneNodeTree(context.scene)
        bpy.ops.vray.show_ntree(data='SCENE')
        return {'FINISHED'}


class VRAY_OT_add_nodetree_object(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_object"
    bl_label       = "Add Object Nodetree"
    bl_description = "Add object nodetree"

    def execute(self, context):
        tree_defaults.AddObjectNodeTree(context.object)
        bpy.ops.vray.show_ntree(data='OBJECT')
        return {'FINISHED'}


class VRAY_OT_add_nodetree_object_lamp(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_object_lamp"
    bl_label       = "Add Object / Lamp Nodetree"
    bl_description = "Add object / lamp nodetree"

    def execute(self, context):
        ob = context.object

        if ob.type in BlenderUtils.NonGeometryTypes:
            if ob.type == 'LAMP':
                tree_defaults.AddLampNodeTree(ob.data)
            else:
                self.report({'ERROR'}, "Object type doesn't support node tree!")
                return {'CANCELLED'}
        else:
            tree_defaults.AddObjectNodeTree(ob)

        bpy.ops.vray.show_ntree(data='OBJECT')

        return {'FINISHED'}


class VRAY_OT_add_nodetree_world(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_world"
    bl_label       = "Add World Nodetree"
    bl_description = "Add world nodetree"

    def execute(self, context):
        tree_defaults.AddWorldNodeTree(context.scene.world)
        bpy.ops.vray.show_ntree(data='WORLD')
        return {'FINISHED'}


class VRAY_OT_add_nodetree_material(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_material"
    bl_label       = "Add Material Nodetree"
    bl_description = "Add material nodetree"

    def execute(self, context):
        if hasattr(context, 'material') and context.material:
            tree_defaults.AddMaterialNodeTree(context.material)

        elif hasattr(context, 'active_object') and context.active_object:
            ob = context.active_object

            if ob.type in BlenderUtils.NonGeometryTypes:
                self.report({'ERROR'}, "Object type doesn't support materials!")
                return {'CANCELLED'}

            empty_slot = None
            for s in ob.material_slots:
                if not s.material:
                    self.report({'INFO'}, "New material is added to existing slot")
                    empty_slot = s
                    break

            if not empty_slot:
                self.report({'INFO'}, "New material is added to new slot")
                bpy.ops.object.material_slot_add()
                empty_slot = ob.material_slots[-1]

            new_ma = bpy.data.materials.new("Material")
            tree_defaults.AddMaterialNodeTree(new_ma)
            empty_slot.material = new_ma

        bpy.ops.vray.show_ntree(data='MATERIAL')

        return {'FINISHED'}


class VRAY_OT_del_nodetree(bpy.types.Operator):
    bl_idname      = "vray.del_nodetree"
    bl_label       = "Delete Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayExporter = context.scene.vray.Exporter

        selectedNodeTree = VRayExporter.ntreeListIndex
        if selectedNodeTree == -1:
            return {'CANCELLED'}

        ntree = bpy.data.node_groups[selectedNodeTree]
        ntree.use_fake_user = False
        ntree.user_clear()
        bpy.data.node_groups.remove(ntree)

        VRayExporter.ntreeListIndex -= 1
        if VRayExporter.ntreeListIndex == -1 and len(bpy.data.node_groups):
            VRayExporter.ntreeListIndex = 0

        return {'FINISHED'}


class VRayOpRenameTo(bpy.types.Operator):
    bl_idname      = "vray.nodetree_rename_to"
    bl_label       = "Rename Node Tree"
    bl_description = "Rename node tree"

    to_data = bpy.props.EnumProperty(
        items = (
            ('MATERIAL', "Material", ""),
            ('OBJECT',   "Object",   ""),
            ('LAMP',     "Lamp",     ""),
            ('SCENE',    "Scene",    ""),
            ('WORLD',    "World",    ""),
        ),
        default = 'MATERIAL'
    )

    ntree = bpy.props.StringProperty()

    def execute(self, context):
        data = None
        nt   = None

        if self.to_data == 'MATERIAL':
            slot = context.material_slot
            if not slot.material:
                return {'CANCELLED'}
            data = slot.material

        elif self.to_data == 'OBJECT':
            data = context.active_object

        elif self.to_data == 'LAMP':
            data = context.active_object.data

        elif self.to_data == 'SCENE':
            data = context.scene

        elif self.to_data == 'WORLD':
            data = context.world

        if not data:
            return {'CANCELLED'}

        data.vray.ntree.name = data.name

        return {'FINISHED'}


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_OT_add_nodetree_scene,
        VRAY_OT_add_nodetree_light,
        VRAY_OT_add_nodetree_object,
        VRAY_OT_add_nodetree_object_lamp,
        VRAY_OT_add_nodetree_material,
        VRAY_OT_add_nodetree_world,

        VRAY_OT_del_nodetree,

        VRayOpRenameTo,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

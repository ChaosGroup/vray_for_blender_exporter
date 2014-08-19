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


def SelectNtreeInEditor(context, ntreeName):
    VRayExporter = context.scene.vray.Exporter
    VRayExporter.ntreeListIndex = bpy.data.node_groups.find(ntreeName)

    for area in context.screen.areas:
        if area.type == 'NODE_EDITOR':
            area.tag_redraw()


class VRayOpSelectNtreeInEditor(bpy.types.Operator):
    bl_idname      = "vray.select_ntree_in_editor"
    bl_label       = "Select Node Tree In Editor"
    bl_description = "Select node tree in global editor"

    # XXX: Segfault in WM_operator_properties_default()
    # ntree = bpy.props.PointerProperty(
    #     type = bpy.types.NodeTree,
    # )
    ntree = bpy.props.StringProperty()

    def execute(self, context):
        if not self.ntree:
            return {'CANCELLED'}

        SelectNtreeInEditor(context, self.ntree)

        return {'FINISHED'}


class VRayOpShowNtree(bpy.types.Operator):
    bl_idname = "vray.show_ntree"
    bl_label = "Show Node Tree"

    data = bpy.props.EnumProperty(
        items = (
            ('MATERIAL', "Material", ""),
            ('OBJECT',   "Object",   ""),
            ('LAMP',     "Lamp",     ""),
            ('WORLD',    "World",    ""),
            ('SCENE',    "Scene",    ""),
        ),
        default = 'MATERIAL'
    )

    def execute(self, context):
        ntree = None

        ob = None
        if hasattr(context, 'active_object'):
            ob = context.active_object
        elif hasattr(context, 'object'):
            ob = context.object

        if self.data == 'MATERIAL':
            if not ob:
                return {'CANCELLED'}
            if not len(ob.material_slots):
                return {'CANCELLED'}
            ma = ob.material_slots[ob.active_material_index].material
            if not ma:
                return {'CANCELLED'}
            ntree = ma.vray.ntree

        elif self.data == 'OBJECT':
            if ob.type in BlenderUtils.NonGeometryTypes:
                if ob.type == 'LAMP':
                    ntree = ob.data.vray.ntree
            else:
                ntree = ob.vray.ntree

        elif self.data == 'WORLD':
            ntree = context.scene.world.vray.ntree

        elif self.data == 'SCENE':
            ntree = context.scene.vray.ntree

        if ntree:
            SelectNtreeInEditor(context, ntree.name)

        return {'FINISHED'}


def ShowNtreeItems(layout):
    layout.operator("vray.show_ntree", text="Material",        icon='MATERIAL'   ).data = 'MATERIAL'
    layout.operator("vray.show_ntree", text="Object",          icon='OBJECT_DATA').data = 'OBJECT'
    layout.operator("vray.show_ntree", text="Environment",     icon='WORLD'      ).data = 'WORLD'
    layout.operator("vray.show_ntree", text="Render Channels", icon='SCENE_DATA' ).data = 'SCENE'


class VRayMenuShowNtree(bpy.types.Menu):
    bl_label = "Show Node Tree In Editor"
    bl_idname = "vray.show_ntree_menu"

    def draw(self, context):
        ShowNtreeItems(self.layout)


class VRayPieShowNtree(bpy.types.Menu):
    bl_label = "Show Node Tree In Editor"
    bl_idname = "vray.show_ntree_pie"

    def draw(self, context):
        ShowNtreeItems(self.layout.menu_pie())


class VRayOpBitmapBufferToImageEditor(bpy.types.Operator):
    bl_idname = "vray.show_node_image"
    bl_label = "Show Bitmap Buffer Image"
    bl_options = {'UNDO'}

    def execute(self, context):
        node = context.active_node

        if not node:
            return {'CANCELLED'}

        if node.bl_idname in {'VRayNodeBitmapBuffer'}:
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = node.texture.image
                    break

        return {'FINISHED'}


def GetRegClasses():
    return (
        VRayOpBitmapBufferToImageEditor,
        VRayOpSelectNtreeInEditor,

        VRayOpShowNtree,
        VRayMenuShowNtree,
        VRayPieShowNtree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

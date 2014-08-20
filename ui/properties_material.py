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

from vb30.ui      import classes
from vb30.lib     import DrawUtils
from vb30.plugins import PLUGINS


def RenderMaterialPanel(mat, context, layout):
    if not mat:
        return

    VRayMaterial = mat.vray

    layout.separator()
    layout.prop(mat, "diffuse_color", text="Viewport Color")

    layout.separator()

    classes.NtreeWidget(layout, VRayMaterial, "Shading Tree", "vray.add_nodetree_material", 'MATERIAL')

    if not classes.TreeHasNodes(VRayMaterial.ntree):
        return

    activeNode = VRayMaterial.ntree.nodes[-1]

    layout.separator()
    classes.DrawNodePanel(context, layout, activeNode, PLUGINS)


class VRAY_MP_context_material(classes.VRayMaterialPanel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return (context.material or context.object) and classes.PollBase(cls, context)

    def draw(self, context):
        layout = self.layout

        mat = context.material

        ob = context.object
        slot = context.material_slot
        space = context.space_data

        if ob:
            row = layout.row()

            row.template_list("VRayListMaterialSlots", "", ob, "material_slots", ob, "active_material_index", rows=4)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ZOOMIN', text="")
            col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

            col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        if ob:
            layout.template_ID(ob, "active_material", new="material.new")
        elif mat:
            layout.template_ID(space, "pin_id")

        if context.scene.render.engine != 'VRAY_RENDER_PREVIEW':
            RenderMaterialPanel(mat, context, layout)


class VRAY_MP_preview(classes.VRayMaterialPanel):
    bl_label = "Preview"

    COMPAT_ENGINES = {'VRAY_RENDER_PREVIEW'}

    def draw(self, context):
        self.layout.template_preview(context.material, show_buttons=True)


class VRAY_MP_preview_material(classes.VRayMaterialPanel):
    bl_label = "Material"

    COMPAT_ENGINES = {'VRAY_RENDER_PREVIEW'}

    @classmethod
    def poll_custom(cls, context):
        if not context.material:
            return False
        return context.material or context.object

    def draw(self, context):
        layout = self.layout

        mat = context.material

        RenderMaterialPanel(mat, context, layout)


def GetRegClasses():
    return (
        VRAY_MP_preview,
        VRAY_MP_context_material,
        VRAY_MP_preview_material,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

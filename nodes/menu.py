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


class VRAY_OT_AddTemplateMaterial(bpy.types.Operator):
    bl_idname      = 'vray.node_add_template_material'
    bl_label       = "Add Simple Material"
    bl_description = "Add a simple material"
    bl_options     = {'REGISTER', 'UNDO'}


    def execute(self, context):
        return {'FINISHED'}


class NODE_MT_vray_templates(bpy.types.Menu):
    bl_idname      = 'NODE_MT_vray_templates'
    bl_space_type  = 'NODE_EDITOR'
    bl_label       = "Templates"
    bl_description = "List of V-Ray node templates"

    def draw(self, context):
        layout = self.layout
        layout.operator('vray.node_add_template_material', icon='MATERIAL')


def vray_node_templates_menu(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.scale_x = 1.3
    row.menu('NODE_MT_vray_templates', icon='VRAY_LOGO')


def GetRegClasses():
    return (
        VRAY_OT_AddTemplateMaterial,

        NODE_MT_vray_templates,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.NODE_HT_header.append(vray_node_templates_menu)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.NODE_HT_header.remove(vray_node_templates_menu)

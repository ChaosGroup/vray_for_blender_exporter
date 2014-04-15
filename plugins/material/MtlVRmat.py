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

from vb30.vray_tools.VRaySceneParser import GetMaterialsNames
from vb30.vray_tools.VrmatParser     import GetXMLMaterialsNames


TYPE = 'MATERIAL'
ID   = 'MtlVRmat'
NAME = "VRmat"
DESC = "VRmat material"

PluginParams = (
    {
        'attr' : 'filename',
        'name' : "Filepath",
        'desc' : "Filepath",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'mtlname',
        'name' : "Name",
        'desc' : "Material name",
        'type' : 'STRING',
        'default' : "",
    },

    {
        'attr' : 'expanded_material',
        'name' : "Material",
        'desc' : "Expanded material",
        'skip' : True,
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'expanded',
        'name' : "Expanded",
        'desc' : "Material is expanded to nodes",
        'type' : 'BOOL',
        'options' : 'HIDDEN',
        'skip' : True,
        'default' : False,
    },
)


def nodeDraw(context, layout, MtlVRmat):
    split = layout.split(percentage=0.2, align=True)
    split.column().label("File:")
    split.column().prop(MtlVRmat, 'filename', text="")

    split = layout.split(percentage=0.2, align=True)
    split.column().label("Name:")
    row = split.column().row(align=True)
    row.prop(MtlVRmat, 'mtlname', text="")
    row.operator("vray.get_vrscene_material_name", text="", icon='IMASEL')


class VRayMaterialNameMenu(bpy.types.Menu):
    bl_label = "Select Material Name"
    bl_idname = "VRayMaterialNameMenu"

    ma_list = []

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()

        for i,maName in enumerate(self.ma_list):
            if i and i % 15 == 0:
                sub = row.column()
            sub.operator("vray.set_vrscene_material_name", text=maName).name = maName


class VRaySetMaterialName(bpy.types.Operator):
    bl_idname      = "vray.set_vrscene_material_name"
    bl_label       = "Set Material Name"
    bl_description = "Set material name from *.vrscene file"

    name = bpy.props.StringProperty()

    def execute(self, context):
        node = context.active_node
        if not node:
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        MtlVRmat.mtlname = self.name

        return {'FINISHED'}


class VRayGetMaterialName(bpy.types.Operator):
    bl_idname      = "vray.get_vrscene_material_name"
    bl_label       = "Get Material Name"
    bl_description = "Get material name from *.vrscene file"

    def execute(self, context):
        node = context.active_node
        if not node:
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        if not MtlVRmat.filename:
            return {'CANCELLED'}

        filePath = os.path.normpath(bpy.path.abspath(MtlVRmat.filename))
        if not os.path.exists(filePath):
            return {'CANCELLED'}

        if filePath.endswith(".vrscene"):
            VRayMaterialNameMenu.ma_list = GetMaterialsNames(filePath)
        else:
            VRayMaterialNameMenu.ma_list = GetXMLMaterialsNames(filePath)

        bpy.ops.wm.call_menu(name=VRayMaterialNameMenu.bl_idname)

        return {'FINISHED'}


def GetRegClasses():
    return (
        VRayMaterialNameMenu,
        VRayGetMaterialName,
        VRaySetMaterialName,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

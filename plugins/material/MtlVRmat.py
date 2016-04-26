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

from pprint import pprint

import bpy

from vb30.vray_tools.VRaySceneParser import GetMaterialsNames, ParseVrscene
from vb30.vray_tools.VrmatParser     import GetXMLMaterialsNames, ParseVrmat

from vb30.nodes import importing as NodesImport
from vb30.nodes import tools     as NodesTools

from vb30.debug import Debug

from vb30.lib import ExportUtils
from vb30.lib import PluginUtils

PluginUtils.loadPluginOnModule(globals(), __name__)


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

    node = None

    def execute(self, context):
        if not context.node:
            Debug.PrintError("No active node!")
            return {'CANCELLED'}

        if context.node.bl_idname != "VRayNodeMtlVRmat":
            Debug.PrintError("Selected node is not of type VRayNodeMtlVRmat!")
            return {'CANCELLED'}

        MtlVRmat = context.node.MtlVRmat
        if not MtlVRmat.filename:
            Debug.PrintError("Filepath is not set!")
            return {'CANCELLED'}

        filePath = os.path.normpath(bpy.path.abspath(MtlVRmat.filename))
        if not os.path.exists(filePath):
            Debug.PrintError("File doesn't exist!")
            return {'CANCELLED'}

        if filePath.endswith(".vrscene"):
            VRayMaterialNameMenu.ma_list = GetMaterialsNames(filePath)
        else:
            VRayMaterialNameMenu.ma_list = GetXMLMaterialsNames(filePath)

        bpy.ops.wm.call_menu(name=VRayMaterialNameMenu.bl_idname)

        return {'FINISHED'}


class VRayMaterialCollapse(bpy.types.Operator):
    bl_idname      = "vray.material_ntree_save"
    bl_label       = "Expand Material"
    bl_description = "Save expanded material to the *.vrscene file"

    def execute(self, context):
        return {'CANCELLED'}


class VRayMaterialExpand(bpy.types.Operator):
    bl_idname      = "vray.material_ntree_load"
    bl_label       = "Expand Material"
    bl_description = "Expand selected material from the *.vrscene file"

    def execute(self, context):
        node = context.node
        if not node:
            Debug.PrintError("No active node!")
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            Debug.PrintError("Selected node is not of type VRayNodeMtlVRmat!")
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        if not MtlVRmat.filename:
            Debug.PrintError("Filepath is not set!")
            return {'CANCELLED'}

        if not MtlVRmat.mtlname:
            Debug.PrintError("Material is not chosen!")
            return {'CANCELLED'}

        filePath = os.path.normpath(bpy.path.abspath(MtlVRmat.filename))
        if not os.path.exists(filePath):
            Debug.PrintError("File doesn't exist!")
            return {'CANCELLED'}

        namePrefix  = ""
        vrsceneDict = []
        if filePath.endswith(".vrscene"):
            vrsceneDict = ParseVrscene(filePath)
        else:
            vrsceneDict = ParseVrmat(filePath)
            namePrefix  = "/"

        # Preview data from the file
        #
        # for pluginDesc in vrsceneDict:
        #     pluginID    = pluginDesc['ID']
        #     pluginName  = pluginDesc['Name']
        #     pluginAttrs = pluginDesc['Attributes']
        #
        #     print("Plugin:")
        #     print("  Type: %s" % pluginID)
        #     print("  Name: %s" % pluginName)
        #     print("  Attributes:")
        #     for attrName in pluginAttrs:
        #         print("    %s = %s" % (attrName, pluginAttrs[attrName]))

        # Find requested material plugin
        #
        mtlName     = namePrefix + MtlVRmat.mtlname
        mtlPlugDesc = NodesImport.getPluginByName(vrsceneDict, mtlName)

        if not mtlPlugDesc:
            print("Requested material is not found!")
            return {'CANCELLED'}

        ntree = context.space_data.edit_tree

        # Now lets start creating nodes
        #
        mtlNode = NodesImport.createNode(ntree, node, vrsceneDict, mtlPlugDesc)

        # Connect material output to our node
        #
        ntree.links.new(mtlNode.outputs['Material'], node.inputs['Material'])

        NodesTools.rearrangeTree(ntree, node)

        return {'FINISHED'}


def nodeDraw(context, layout, MtlVRmat):
    split = layout.split(percentage=0.2, align=True)
    split.column().label("File:")
    split.column().prop(MtlVRmat, 'filename', text="")

    split = layout.split(percentage=0.2, align=True)
    split.column().label("Name:")
    row = split.column().row(align=True)
    row.prop(MtlVRmat, 'mtlname', text="")
    row.operator("vray.get_vrscene_material_name", text="", icon='IMASEL')

    # layout.separator()
    # split = layout.split()
    # row = split.row(align=True)
    # row.operator("vray.material_ntree_load", text="Load", icon='FILE_FOLDER')
    # row.operator("vray.material_ntree_save", text="Save", icon='FILE_TICK')


def GetRegClasses():
    return (
        VRayMaterialCollapse,
        VRayMaterialExpand,
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

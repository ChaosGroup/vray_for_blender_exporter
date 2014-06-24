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


TYPE = 'SETTINGS'
ID   = 'Includer'
NAME = 'Includer'
DESC = "Include additional vrscene files"


class IncluderList(bpy.types.PropertyGroup):
    scene = bpy.props.StringProperty(
        name = "Filepath",
        subtype = 'FILE_PATH',
        description = "Path to a *.vrscene file"
    )

    use = bpy.props.BoolProperty(
        name = "",
        description = "Use scene",
        default = True
    )


class Includer(bpy.types.PropertyGroup):
    use = bpy.props.BoolProperty(
        name        = "Use Includer",
        description = "Add additional *.vrscene files",
        default     = False
    )

    nodes = bpy.props.CollectionProperty(
        name = "Scene Name",
        type =  IncluderList,
        description = "Custom name scene"
    )

    nodes_selected= bpy.props.IntProperty(
        name = "Scene Index",
        default = -1,
        min = -1,
        max = 100
    )


class VRAY_OT_includer_add(bpy.types.Operator):
    bl_idname=      'vray.includer_add'
    bl_label=       "Add Include"
    bl_description= "Add Include *.vrsene"

    def execute(self, context):
        vs= context.scene.vray
        module= vs.Includer

        module.nodes.add()
        module.nodes[-1].name= "Include Scene"

        return {'FINISHED'}


class VRAY_OT_includer_remove(bpy.types.Operator):
    bl_idname=      'vray.includer_remove'
    bl_label=       "Remove Include"
    bl_description= "Remove Include *.vrsene"

    def execute(self, context):
        vs= context.scene.vray
        module= vs.Includer

        if module.nodes_selected >= 0:
           module.nodes.remove(module.nodes_selected)
           module.nodes_selected-= 1

        return {'FINISHED'}


class VRAY_OT_includer_up(bpy.types.Operator):
    bl_idname=      'vray.includer_up'
    bl_label=       "Up Include"
    bl_description= "Up Include *.vrsene"

    def execute(self, context):
        vs= context.scene.vray
        module= vs.Includer

        if module.nodes_selected <= 0:
            return {'CANCELLED'}

        module.nodes.move(module.nodes_selected,
                                 module.nodes_selected - 1)
        module.nodes_selected-= 1

        return {'FINISHED'}


class VRAY_OT_includer_down(bpy.types.Operator):
    bl_idname=      'vray.includer_down'
    bl_label=       "Down Include"
    bl_description= "Down Include *.vrsene"

    def execute(self, context):
        vs= context.scene.vray
        module= vs.Includer

        if module.nodes_selected <= 0:
            return {'CANCELLED'}

        module.nodes.move(module.nodes_selected,
                                 module.nodes_selected + 1)
        module.nodes_selected+= 1

        return {'FINISHED'}


def GetRegClasses():
    return (
        IncluderList,
        Includer,

        VRAY_OT_includer_add,
        VRAY_OT_includer_remove,
        VRAY_OT_includer_up,
        VRAY_OT_includer_down,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    setattr(bpy.types.VRayScene, 'Includer', bpy.props.PointerProperty(
        name = "Includes",
        type =  Includer,
        description = "Include additional *.vrscene files"
    ))


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

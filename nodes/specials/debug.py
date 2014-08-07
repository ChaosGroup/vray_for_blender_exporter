#
# V-Ray/Blender
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

from ..        import tree
from ..sockets import AddInput, AddOutput
from ..operators import sockets as SocketOperators


class VRaySocketAny(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketAny'
    bl_label  = 'Any data socket'

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    value = bpy.props.StringProperty(
        name = "Data",
        description = "Data",
        default = ""
    )

    def draw(self, context, layout, node, text):
        if node.bl_idname == 'VRayNodeDebugSwitch':
            # NOTE: label ends with digit
            if node.input_index == text[-1]:
                text = '%s *' % text
        layout.label(text)

    def draw_color(self, context, node):
        return (0.3, 0.3, 0.3, 1.000)


class VRayNodeDebugSwitch(bpy.types.Node):
    bl_idname = 'VRayNodeDebugSwitch'
    bl_label  = 'Switch'
    bl_icon   = 'NONE'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    input_index = bpy.props.EnumProperty(
        name        = "Input",
        description = "Input index",
        items = (
            ('0', "0", ""),
            ('1', "1", ""),
            ('2', "2", ""),
            ('3', "3", ""),
            ('4', "4", ""),
        ),
        default = '0'
    )

    def init(self, context):
        AddInput(self, 'VRaySocketAny', "Input 0")
        AddInput(self, 'VRaySocketAny', "Input 1")
        AddInput(self, 'VRaySocketAny', "Input 2")
        AddInput(self, 'VRaySocketAny', "Input 3")
        AddInput(self, 'VRaySocketAny', "Input 4")

        AddOutput(self, 'VRaySocketAny', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'input_index', expand=True)


def GetRegClasses():
    return (
        VRaySocketAny,
        VRayNodeDebugSwitch,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

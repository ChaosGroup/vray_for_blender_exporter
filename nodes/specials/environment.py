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
from ..sockets import AddInput, AddOutput, VRaySocketColorMult


class VRayNodeWorldOutput(bpy.types.Node):
    bl_idname = 'VRayNodeWorldOutput'
    bl_label  = 'World Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def init(self, context):
        AddInput(self, 'VRaySocketObject', "Environment")
        AddInput(self, 'VRaySocketObject', "Effects")



class VRaySocketEnvironment(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketEnvironment'
    bl_label  = 'Environment socket'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    multiplier = bpy.props.FloatProperty(
        name        = "Multiplier",
        description = "Color / texture multiplier",
        min         = 0.0,
        default     = 1.0
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.prop(self, 'multiplier', text=text)
        else:
            row = layout.row(align=True)
            row.prop(self, 'multiplier', text=text)
            rowCol = row.row()
            rowCol.scale_x = 0.3
            rowCol.prop(self, 'value', text="")

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRaySocketEnvironmentOverride(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketEnvironmentOverride'
    bl_label  = 'Environment override socket'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    use = bpy.props.BoolProperty(
        name        = "Use",
        description = "Use override",
        default     = False
    )

    multiplier = bpy.props.FloatProperty(
        name        = "Multiplier",
        description = "Color / texture multiplier",
        min         = 0.0,
        default     = 1.0
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            split = layout.split()
            row = split.row(align=True)
            row.active = self.use
            row.prop(self, 'use', text="")
            row.prop(self, 'multiplier', text=text)
        else:
            row = layout.row(align=True)
            row.active = self.use
            row.prop(self, 'use', text="")
            row.prop(self, 'multiplier', text=text)
            rowCol = row.row()
            rowCol.scale_x = 0.3
            rowCol.prop(self, 'value', text="")

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRayNodeEnvironment(bpy.types.Node):
    bl_idname = 'VRayNodeEnvironment'
    bl_label  = 'Environment'
    bl_icon   = 'WORLD'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def init(self, context):
        AddInput(self, 'VRaySocketEnvironment',         "Background", 'bg_tex', (0.0, 0.0, 0.0))
        AddInput(self, 'VRaySocketEnvironmentOverride', "GI",         'gi_tex')
        AddInput(self, 'VRaySocketEnvironmentOverride', "Reflection", 'reflect_tex')
        AddInput(self, 'VRaySocketEnvironmentOverride', "Refraction", 'refract_tex')

        AddOutput(self, 'VRaySocketObject', "Environment")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRaySocketEnvironment,
        VRaySocketEnvironmentOverride,
        VRayNodeWorldOutput,
        VRayNodeEnvironment,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

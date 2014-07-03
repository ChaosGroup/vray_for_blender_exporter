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


class VRayNodeWorldOutput(bpy.types.Node):
    bl_idname = 'VRayNodeWorldOutput'
    bl_label  = 'World Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def init(self, context):
        AddInput(self, 'VRaySocketObject', "Environment")
        AddInput(self, 'VRaySocketObject', "Effects")


class VRayNodeEnvironment(bpy.types.Node):
    bl_idname = 'VRayNodeEnvironment'
    bl_label  = 'Environment'
    bl_icon   = 'WORLD'

    gi_tex = bpy.props.BoolProperty(
        name        = "Override GI",
        description = "Override environment for GI",
        default     = False
    )

    reflect_tex = bpy.props.BoolProperty(
        name        = "Override Reflect",
        description = "Override environment for reflection",
        default     = False
    )

    refract_tex = bpy.props.BoolProperty(
        name        = "Override Refract",
        description = "Override environment for refraction",
        default     = False
    )

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def init(self, context):
        AddInput(self, 'VRaySocketColor',    "Background", 'bg_tex', (0.0, 0.0, 0.0))
        AddInput(self, 'VRaySocketColorUse', "GI",         'gi_tex')
        AddInput(self, 'VRaySocketColorUse', "Reflection", 'reflect_tex')
        AddInput(self, 'VRaySocketColorUse', "Refraction", 'refract_tex')

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
        VRayNodeWorldOutput,
        VRayNodeEnvironment,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

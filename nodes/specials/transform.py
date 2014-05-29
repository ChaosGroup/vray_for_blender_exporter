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
import mathutils

from ..sockets import AddInput, AddOutput


class VRayNodeTransform(bpy.types.Node):
    bl_idname = 'VRayNodeTransform'
    bl_label  = 'Transform'
    bl_icon   = 'AXIS_TOP'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    rotate = bpy.props.FloatVectorProperty(
        name        = "Rotation",
        description = "Rotation",
        size        = 3,
        unit        = 'ROTATION',
        default     = (0.0, 0.0, 0.0)
    )

    offset = bpy.props.FloatVectorProperty(
        name        = "Offset",
        description = "Offset",
        size        = 3,
        unit        = 'LENGTH',
        default     = (0.0, 0.0, 0.0)
    )

    scale = bpy.props.FloatVectorProperty(
        name        = "Scale",
        description = "Scale",
        size        = 3,
        unit        = 'AREA',
        default     = (1.0, 1.0, 1.0)
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketTransform', "Transform")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'rotate')
        layout.prop(self, 'offset')
        layout.prop(self, 'scale')

    def getTransform(self):
        mat_offs = mathutils.Matrix.Translation(self.offset)

        mat_rot  = mathutils.Matrix.Rotation(self.rotate[0], 4, 'X') * \
                   mathutils.Matrix.Rotation(self.rotate[1], 4, 'Y') * \
                   mathutils.Matrix.Rotation(self.rotate[2], 4, 'Z')

        mat_sca  = mathutils.Matrix.Scale(self.scale[0], 4, (1.0, 0.0, 0.0)) * \
                   mathutils.Matrix.Scale(self.scale[1], 4, (0.0, 1.0, 0.0)) * \
                   mathutils.Matrix.Scale(self.scale[2], 4, (0.0, 0.0, 1.0))

        tm = mat_offs * mat_rot * mat_sca

        return tm


class VRayNodeMatrix(bpy.types.Node):
    bl_idname = 'VRayNodeMatrix'
    bl_label  = 'Matrix'
    bl_icon   = 'AXIS_TOP'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    rotate = bpy.props.FloatVectorProperty(
        name        = "Rotation",
        description = "Rotation",
        size        = 3,
        unit        = 'ROTATION',
        default     = (0.0, 0.0, 0.0)
    )

    scale = bpy.props.FloatVectorProperty(
        name        = "Scale",
        description = "Scale",
        size        = 3,
        unit        = 'AREA',
        default     = (1.0, 1.0, 1.0)
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketTransform', "Matrix")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'rotate')
        layout.prop(self, 'scale')

    def getMatrix(self):
        mat_rot  = mathutils.Matrix.Rotation(self.rotate[0], 3, 'X') * \
                   mathutils.Matrix.Rotation(self.rotate[1], 3, 'Y') * \
                   mathutils.Matrix.Rotation(self.rotate[2], 3, 'Z')

        mat_sca  = mathutils.Matrix.Scale(self.scale[0], 3, (1.0, 0.0, 0.0)) * \
                   mathutils.Matrix.Scale(self.scale[1], 3, (0.0, 1.0, 0.0)) * \
                   mathutils.Matrix.Scale(self.scale[2], 3, (0.0, 0.0, 1.0))

        tm = mat_rot * mat_sca

        return tm


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayNodeTransform,
        VRayNodeMatrix,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

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

from . import convert

from vb30 import debug


class VRayOperatorConvertMaterial(bpy.types.Operator):
    bl_idname      = "vray.convert_scene"
    bl_label       = "Convert To Nodes"
    bl_description = "Convert scene to nodes"

    def execute(self, context):
        debug.PrintInfo('Executing operator: "%s"' % self.bl_label)

        VRayScene = context.scene.vray
        VRayConverter = VRayScene.VRayConverter

        try:
            if VRayConverter.convert_from == 'INTERNAL':
                convert.convert_bi()
            convert.ConvertScene(context.scene)
        except Exception as e:
            debug.ExceptionInfo(e)
            self.report({'ERROR'}, "%s" % e)
            return {'CANCELLED'}

        return {'FINISHED'}


def GetRegClasses():
    return (
        VRayOperatorConvertMaterial,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

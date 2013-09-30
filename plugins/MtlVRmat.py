#
# V-Ray/Blender
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


TYPE = 'MATERIAL'

ID   = 'MtlVRmat'
NAME = 'MtlVRmat'
UI   = "VisMat"
DESC = "VisMat material"

PARAMS = (
    'filename',
    'mtlname',
)


def add_properties(rna_pointer):
    class MtlVRmat(bpy.types.PropertyGroup):
        filename = bpy.props.StringProperty(
            name        = "Filepath",
            description = "",
            subtype     = 'FILE_PATH',
            default     = ""
        )

        mtlname = bpy.props.StringProperty(
            name        = "Material Name",
            description = "",
            default     = ""
        )

        expanded = bpy.props.BoolProperty(
            name        = "Expanded",
            description = "Material is expanded to nodes",
            default     = False
        )

    bpy.utils.register_class(MtlVRmat)

    rna_pointer.MtlVRmat = bpy.props.PointerProperty(
        name        = "MtlVRmat",
        type        =  MtlVRmat,
        description = "V-Ray MtlVRmat settings"
    )


def write(bus, VRayBRDF=None, base_name=None):
    pass


def gui(context, layout, MtlVRmat, material=None, node=None):
    layout.prop(MtlVRmat, 'filename')
    layout.prop(MtlVRmat, 'mtlname')


def register():
    pass


def unregister():
    pass

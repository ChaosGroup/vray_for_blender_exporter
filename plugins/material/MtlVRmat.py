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
    layout.prop(MtlVRmat, 'filename')
    layout.prop(MtlVRmat, 'mtlname')


# TODO: custom export function

#
# V-Ray For Blender
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


TYPE = 'TEXTURE'
ID   = 'TexVoxelData'
NAME = 'Voxel Data'
DESC = "Voxel data texture"

PluginParams = (
    {
        'attr' : 'interpolation',
        'desc' : "Interpolation type",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'out_color',
        'desc' : "Color",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'out_density',
        'desc' : "Density",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'out_flame',
        'desc' : "Flame intensity",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },

    {
        'attr' : 'domain',
        'name' : "Domain",
        'desc' : "Simulation domain",
        'type' : 'PLUGIN',
        'skip' : True,
        'default' : "",
    },
)

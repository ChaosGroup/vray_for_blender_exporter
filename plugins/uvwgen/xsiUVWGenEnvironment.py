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


TYPE = 'UVWGEN'
ID   = 'xsiUVWGenEnvironment'
NAME = 'Environment (XSI)'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvw_matrix',
        'desc' : "Transformation of the input directions",
        'type' : 'MATRIX',
        'default' : None,
    },
    {
        'attr' : 'uvw_transform',
        'desc' : "Transformation of the resulting UVW coordinates",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'mapping_type',
        'desc' : "spherical(0), cylindrical(1), cubic strip(2), cubic cross sideways(3), cubic cross(4)",
        'type' : 'INT',
        'default' : 1,
    },
)

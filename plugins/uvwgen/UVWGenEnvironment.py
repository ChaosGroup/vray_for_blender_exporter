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
ID   = 'UVWGenEnvironment'
NAME = 'Environment'
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
        'desc' : 'One of "angular", "cubic", "spherical", "mirror_ball", "screen", "max_spherical", "spherical_vray", "max_cylindrical" or "max_shrink_wrap"',
        'type' : 'STRING',
        'default' : "spherical",
    },
    {
        'attr' : 'wrap_u',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrap_v',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrap_w',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_u',
        'desc' : "1 to crop in the u-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_v',
        'desc' : "1 to crop in the v-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_w',
        'desc' : "1 to crop in the w-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'duvw_scale',
        'desc' : "Additional scale factor for the texture derivatives",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ground_on',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    # {
    #     'attr' : 'ground_position',
    #     'desc' : "",
    #     'type' : 'VECTOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'ground_radius',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1000,
    },
)

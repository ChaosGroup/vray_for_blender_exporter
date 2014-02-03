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

from vb30.lib import ExportUtils


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
        'desc' : 'Mapping type',
        'type' : 'ENUM',
        'items' : (
            ('angular', "Angular", ""),
            ('cubic', "Cubic", ""),
            ('spherical', "Spherical", ""),
            ('mirror_ball', "Mirror Ball", ""),
            ('screen', "Screen", ""),
            ('max_spherical', "Spherical (3ds max)", ""),
            ('spherical_vray', "Spherical (V-Ray)", ""),
            ('max_cylindrical', "Cylindrical (3ds max)", ""),
            ('max_shrink_wrap', "Shrink Wrap (3ds max)", ""),
        ),
        'default' : 'spherical',
    },
    {
        'attr' : 'wrap_u',
        'desc' : "Wrap U",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Wrapping", ""),
            ('1', "Wrap", ""),
            ('2', "Mirror Tile", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'wrap_v',
        'desc' : "Wrap V",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Wrapping", ""),
            ('1', "Wrap", ""),
            ('2', "Mirror Tile", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'wrap_w',
        'desc' : "Wrap W",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Wrapping", ""),
            ('1', "Wrap", ""),
            ('2', "Mirror Tile", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'crop_u',
        'desc' : "Crop in the u-direction",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'crop_v',
        'desc' : "Crop in the v-direction",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'crop_w',
        'desc' : "Crop in the w-direction",
        'type' : 'BOOL',
        'default' : False,
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


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'mapping_type' : '"%s"' % propGroup.mapping_type,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

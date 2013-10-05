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

from vb25.lib   import ExportUtils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'TEXTURE'
ID   = 'TexTiles'
NAME = 'Tiles'
DESC = ""

PluginParams = (
    {
        'attr' : 'compatibility_with',
        'desc' : "This is used to differentiate between textures exported from different applications",
        'type' : 'ENUM',
        'items' : (
            ('0', "3ds Max", ""),
            ('1', "Maya", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'alpha_from_intensity',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "Self", "The alpha is taken from the alpha"),
            ('1', "Maya", "The resulting alpha is the color intensity (if compatibility_with is 0) or the color luminance (if compatibility_with is 1)"),
            ('2', "Force 1.0", "The alpha is forced to 1.0f"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'invert',
        'desc' : "If true, the resulting texture color will be inverted",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'invert_alpha',
        'desc' : "If true and invert is on, the resulting texture alpha will be inverted too. If false, just the color will be inverted",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'color_mult',
        'desc' : "A multiplier for the texture color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'color_offset',
        'desc' : "An additional offset for the texture color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'alpha_mult',
        'desc' : "A multiplier for the texture alpha",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'alpha_offset',
        'desc' : "An additional offset for the texture alpha",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'nouvw_color',
        'desc' : "The color when there are no valid uvw coordinates",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5, 1),
    },
    {
        'attr' : 'color',
        'desc' : "The resulting color",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'out_transparency',
        'desc' : "The resulting transparency",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'out_alpha',
        'desc' : "The resulting alpha",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'out_intensity',
        'desc' : "The resulting intensity",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'uvwgen',
        'desc' : "The uvw generator for the texture",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'placement_type',
        'desc' : "The way the valid portion of the texture is applied: 0 - the whole texture is valid, 1 - crop, 2 -place",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'u',
        'desc' : "U coordinate of the valid texture sector",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'v',
        'desc' : "V coordinate of the valid texture sector",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'w',
        'desc' : "Width of the valid texture sector",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'h',
        'desc' : "Height of the valid texture sector",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'jitter',
        'desc' : "Amount of random placement variation",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'tile_u',
        'desc' : "If true there is horizontal tiling",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'tile_v',
        'desc' : "If true there is vertical tiling",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'uv_noise_on',
        'desc' : "If true the noise is enabled",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'uv_noise_animate',
        'desc' : "If true the noise is animated",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'uv_noise_amount',
        'desc' : "UV noise amount",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'uv_noise_levels',
        'desc' : "UV noise iterations",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'uv_noise_size',
        'desc' : "UV noise size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'un_noise_phase',
        'desc' : "UV noise phase",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'color_mortar',
        'desc' : "Mortar color",
        'type' : 'TEXTURE',
        'default' : (0.7, 0.7, 0.7, 1),
    },
    {
        'attr' : 'color_tiles',
        'desc' : "Tiles color",
        'type' : 'TEXTURE',
        'default' : (0.6, 0.5, 0.4, 1),
    },
    {
        'attr' : 'horizontal_count',
        'desc' : "Tiles horizontal count",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'vertical_count',
        'desc' : "Tiles vertical count",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'color_variance',
        'desc' : "Color variance",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'horizontal_gap',
        'desc' : "Horizontal gap between tiles",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'vertical_gap',
        'desc' : "Vertical gap between tiles",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'pattern_type',
        'desc' : "Tiles pattern: 0-Custom Tiles, 1-Running Bond, 2-Common Flemish Bond, 3-English Bond, 4-1/2 Running Bond, 5-Stack Bond, 6-Fine Running Bond, 7-Fine Stack Bond",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'line_shift',
        'desc' : "Line shift",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'random_shift',
        'desc' : "Random shift",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'edge_roughness',
        'desc' : "Edge roughness",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'holes',
        'desc' : "Holes",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'random_seed',
        'desc' : "Random seed",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'fade_variance',
        'desc' : "Fade variance",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'row_modify',
        'desc' : "if 1 - custom row parameters",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'column_modify',
        'desc' : "if 1 - custom column parameters",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'per_row',
        'desc' : "every per_row row is modified by corresponding change value",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'row_change',
        'desc' : "row change value modifying the number of tiles in affected rows",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'per_column',
        'desc' : "every per_column column is modified by corresponding change value",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'column_change',
        'desc' : "column change value modifying the number of tiles in affected columns",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

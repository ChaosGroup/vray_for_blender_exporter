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
from vb25.ui.ui import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'TEXTURE'
ID   = 'TexSplat'
NAME = 'TexSplat'
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
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
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
        'attr' : 'color1',
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'color2',
        'desc' : "Second color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'size',
        'desc' : "Size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'iterations',
        'desc' : "Number of iterations for the fractal generator",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'threshold',
        'desc' : "Threshold",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'smoothing',
        'desc' : "Transition smoothing",
        'type' : 'FLOAT',
        'default' : 0.02,
    },
)

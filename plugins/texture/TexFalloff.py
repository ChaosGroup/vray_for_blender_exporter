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
ID   = 'TexFalloff'
NAME = 'Falloff'
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
        'attr' : 'type',
        'desc' : "Type (0 - towards/away, 1 - perpendicular/parallel, 2 - Fresnel, 3 - shadow/light, 4 - distance blend)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'direction_type',
        'desc' : "Direction type (0 - viewZ, 1 - viewX, 2 - viewY, 3 - explicit, 4 - localX, 5 - localY, 6 - localZ, 7 - worldX, 8 - worldY, 9 - worldZ)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'fresnel_ior',
        'desc' : "IOR for the Fresnel falloff type",
        'type' : 'FLOAT',
        'default' : 1.6,
    },
    {
        'attr' : 'dist_extrapolate',
        'desc' : "Extrapolate for the distance blend falloff type",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dist_near',
        'desc' : "Near distance for the distance blend falloff type",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'dist_far',
        'desc' : "Far distance for the distance blend falloff type",
        'type' : 'FLOAT',
        'default' : 100,
    },
    {
        'attr' : 'explicit_dir',
        'desc' : "Direction for the explicit direction type",
        'type' : 'VECTOR',
        'default' : (0, 0, 1),
    },
    {
        'attr' : 'blend_output',
        'desc' : "The blending amount, based on the parameters",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'use_blend_input',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'blend_input',
        'desc' : "If specified and use_blend_input is true, the final blending amount will be taken from this texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
)

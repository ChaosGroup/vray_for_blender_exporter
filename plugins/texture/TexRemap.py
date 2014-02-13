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


TYPE = 'TEXTURE'
ID   = 'TexRemap'
NAME = 'Remap'
DESC = "Remap values"

PluginParams = (
    {
        'attr' : 'input_value',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'input_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'out_value',
        'desc' : "the output value, depending on input_value and color params",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'out_color',
        'desc' : "the output color, depending on input_value/input_color and float params",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },

    {
        'attr' : 'type',
        'desc' : "type of conversion: 0:RemapValue, 1:RemapColor, 2:RemapHSV",
        'type' : 'ENUM',
        'items' : (
            ('0', "Value", ""),
            ('1', "Color", ""),
            ('2', "HSV", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'input_bias',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'input_min',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'input_max',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'output_min',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'output_max',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },

    {
        'attr' : 'float_positions',
        'desc' : "positions of the given float values",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'float_values',
        'desc' : "the given float values",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'float_types',
        'desc' : "interpolation types for the floats",
        'type' : 'INT',
        'default' : 1,
    },

    {
        'attr' : 'color_positions',
        'desc' : "the given float values",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'color_colors',
        'desc' : "the given colors",
        'type' : 'TEXTURE',
        'default' : (1.0,1.0,1.0),
    },
    {
        'attr' : 'color_types',
        'desc' : "interpolation types for the colors",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'red_positions',
        'desc' : "positions of the given values for the red channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'red_values',
        'desc' : "the given values for the red channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'red_types',
        'desc' : "interpolation types for the red channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'green_positions',
        'desc' : "positions of the given values for the green channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'green_values',
        'desc' : "the given values for the green channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'green_types',
        'desc' : "interpolation types for the green channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'blue_positions',
        'desc' : "positions of the given values for the blue channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'blue_values',
        'desc' : "the given values for the blue channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'blue_types',
        'desc' : "interpolation types for the blue channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'hue_positions',
        'desc' : "positions of the given values for the hue channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'hue_values',
        'desc' : "the given values for the hue channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hue_types',
        'desc' : "interpolation types for the hue channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'saturation_positions',
        'desc' : "positions of the given values for the saturation channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'saturation_values',
        'desc' : "the given values for the saturation channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'saturation_types',
        'desc' : "interpolation types for the saturation channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'value_positions',
        'desc' : "positions of the given values for the value channel",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'value_values',
        'desc' : "the given values for the value channel",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'value_types',
        'desc' : "interpolation types for the value channel",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'alpha_from_intensity',
        'desc' : "If true, the resulting alpha is the color intensity; otherwise the alpha is taken from the colors",
        'type' : 'BOOL',
        'default' : False,
    },
)


PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "type", "expand" : true }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "input_bias" }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "input_min" },
            { "name" : "input_max" }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "output_min" },
            { "name" : "output_max" }
        ]
    },
    
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "alpha_from_intensity" }
        ]
    }
]}
"""

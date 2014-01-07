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
ID   = 'ColorCorrect'
NAME = 'Color Correct'
DESC = "Color correct"

PluginParams = (
    {
        'attr' : 'source_color',
        'desc' : "Source color",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'texture_map',
        'desc' : "The texture being color corrected",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'preprocess',
        'desc' : "true to enable preprocessing",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'pre_brightness',
        'desc' : "Added to the texture brightness",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'pre_contrast',
        'desc' : "Contrast",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'pre_gamma',
        'desc' : "Gamma",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'pre_mono',
        'desc' : "true to convert to grayscale",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'pre_invert',
        'desc' : "true to invert the input color",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'pre_unmult_alpha',
        'desc' : "true to unmultiply alpha",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'pre_clamp',
        'desc' : "true to clamp the input color",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'pre_clamp_min',
        'desc' : "low clamp value",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'pre_clamp_max',
        'desc' : "high clamp value",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'pre_clamp_normalize',
        'desc' : "true to normalize the clamped input to 0.0-1.0",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'hsl_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'hsl_hue_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'hsl_hue_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsl_saturation_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsl_saturation_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'hsl_lightness_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsl_lightness_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'hsv_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'hsv_hue_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'hsv_hue_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsv_saturation_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsv_saturation_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'hsv_value_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'hsv_value_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'rgba_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'red_channel',
        'desc' : "Red channel",
        'type' : 'ENUM',
        'items' : (
            ('0', "Red", ""),
            ('1', "Green", ""),
            ('2', "Blue", ""),
            ('3', "Alpha", ""),
            ('4', "Intensity", ""),
            ('5', "In Red", ""),
            ('6', "In Green", ""),
            ('7', "In Blue", ""),
            ('8', "In Alpha", ""),
            ('9', "In Intensity", ""),
            ('10', "HSL Hue", ""),
            ('11', "HSL Saturation", ""),
            ('12', "HSL Lightness", ""),
            ('13', "HSV Hue", ""),
            ('14', "HSV Saturation", ""),
            ('15', "HSV Value", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'red_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'red_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'green_channel',
        'desc' : "Green channel",
        'type' : 'ENUM',
        'items' : (
            ('0', "Red", ""),
            ('1', "Green", ""),
            ('2', "Blue", ""),
            ('3', "Alpha", ""),
            ('4', "Intensity", ""),
            ('5', "In Red", ""),
            ('6', "In Green", ""),
            ('7', "In Blue", ""),
            ('8', "In Alpha", ""),
            ('9', "In Intensity", ""),
            ('10', "HSL Hue", ""),
            ('11', "HSL Saturation", ""),
            ('12', "HSL Lightness", ""),
            ('13', "HSV Hue", ""),
            ('14', "HSV Saturation", ""),
            ('15', "HSV Value", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'green_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'green_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'blue_channel',
        'desc' : "Blue channel",
        'type' : 'ENUM',
        'items' : (
            ('0', "Red", ""),
            ('1', "Green", ""),
            ('2', "Blue", ""),
            ('3', "Alpha", ""),
            ('4', "Intensity", ""),
            ('5', "In Red", ""),
            ('6', "In Green", ""),
            ('7', "In Blue", ""),
            ('8', "In Alpha", ""),
            ('9', "In Intensity", ""),
            ('10', "HSL Hue", ""),
            ('11', "HSL Saturation", ""),
            ('12', "HSL Lightness", ""),
            ('13', "HSV Hue", ""),
            ('14', "HSV Saturation", ""),
            ('15', "HSV Value", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'blue_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'blue_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'alpha_channel',
        'desc' : "Alpha channel",
        'type' : 'ENUM',
        'items' : (
            ('0', "Red", ""),
            ('1', "Green", ""),
            ('2', "Blue", ""),
            ('3', "Alpha", ""),
            ('4', "Intensity", ""),
            ('5', "In Red", ""),
            ('6', "In Green", ""),
            ('7', "In Blue", ""),
            ('8', "In Alpha", ""),
            ('9', "In Intensity", ""),
            ('10', "HSL Hue", ""),
            ('11', "HSL Saturation", ""),
            ('12', "HSL Lightness", ""),
            ('13', "HSV Hue", ""),
            ('14', "HSV Saturation", ""),
            ('15', "HSV Value", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'alpha_offset',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'alpha_gain',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'premultiply_new_alpha',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'postprocess',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'post_mono',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'post_invert',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'post_clamp',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'post_clamp_min',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'post_clamp_max',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'post_clamp_normalize',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
)


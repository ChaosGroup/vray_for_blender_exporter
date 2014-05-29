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
ID   = 'ColorCorrection'
NAME = 'Color Correction'
DESC = "Color correction"

PluginParams = (
    {
        'attr' : 'source_color',
        'desc' : "Source color",
        'type' : 'ACOLOR',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'texture_map',
        'desc' : "The texture being color corrected",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'rewire_red',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Red", ""),
            ('1',  "Green", ""),
            ('2',  "Blue", ""),
            ('3',  "Alpha", ""),
            ('4',  "Redinv", ""),
            ('5',  "Greeninv", ""),
            ('6',  "Blueinv", ""),
            ('7',  "Alphainv", ""),
            ('8',  "Monochrome", ""),
            ('9',  "One", ""),
            ('10', "Zero", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'rewire_green',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Red", ""),
            ('1',  "Green", ""),
            ('2',  "Blue", ""),
            ('3',  "Alpha", ""),
            ('4',  "Redinv", ""),
            ('5',  "Greeninv", ""),
            ('6',  "Blueinv", ""),
            ('7',  "Alphainv", ""),
            ('8',  "Monochrome", ""),
            ('9',  "One", ""),
            ('10', "Zero", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'rewire_blue',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Red", ""),
            ('1',  "Green", ""),
            ('2',  "Blue", ""),
            ('3',  "Alpha", ""),
            ('4',  "Redinv", ""),
            ('5',  "Greeninv", ""),
            ('6',  "Blueinv", ""),
            ('7',  "Alphainv", ""),
            ('8',  "Monochrome", ""),
            ('9',  "One", ""),
            ('10', "Zero", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'rewire_alpha',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Red", ""),
            ('1',  "Green", ""),
            ('2',  "Blue", ""),
            ('3',  "Alpha", ""),
            ('4',  "Redinv", ""),
            ('5',  "Greeninv", ""),
            ('6',  "Blueinv", ""),
            ('7',  "Alphainv", ""),
            ('8',  "Monochrome", ""),
            ('9',  "One", ""),
            ('10', "Zero", ""),
        ),
        'default' : '3',
    },
    {
        'attr' : 'hue_shift',
        'desc' : "added to the color hue",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'saturation',
        'desc' : "added to the color saturation",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'hue_tint',
        'desc' : "Hue tint",
        'type' : 'ACOLOR',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'tint_strength',
        'desc' : "default = 0",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'brightness',
        'desc' : "default = 0.0 - value is added to the texture brightness",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'contrast',
        'desc' : "default = 1.0f",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'lightness_mode',
        'desc' : "Lightness mode",
        'type' : 'ENUM',
        'items' : (
            ("0", "Standard", ""),
            ("1", "Advanced", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'adv_brightness',
        'desc' : "Color multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'adv_contrast',
        'desc' : "Color contrast",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'adv_base',
        'desc' : "Contrast base",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'adv_offset',
        'desc' : "Color offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'adv_use_red',
        'desc' : "true to use the red component ov the adv_rgb_* parameters",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adv_use_green',
        'desc' : "true to use the green component ov the adv_rgb_* parameters",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adv_use_blue',
        'desc' : "true to use the blue component ov the adv_rgb_* parameters",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adv_rgb_brightness',
        'desc' : "Color multiplier rgb",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'adv_rgb_contrast',
        'desc' : "Color contrast rgb",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'adv_rgb_base',
        'desc' : "Contrast base rgb",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'adv_rgb_offset',
        'desc' : "Color offset rgb",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
)

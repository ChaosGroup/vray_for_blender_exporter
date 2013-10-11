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
ID   = 'TexAColorOp'
NAME = 'Color Operations'
DESC = "Color operations"

PluginParams = (
    {
        'attr' : 'color_a',
        'desc' : "The first color",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'color_b',
        'desc' : "The second color",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'mult_a',
        'desc' : "Multiplier for the first color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'mult_b',
        'desc' : "Multiplier for the second color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'result_alpha',
        'desc' : "The alpha for the result; if not specified, the resulting alpha taken from the first color)",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'mode',
        'name' : "Output Mode",
        'desc' : "Which output should be considered for the 'Output'",
        'type' : 'ENUM',
        'items' : (
        	('0', "Result A", ""),
        	('1', "Result B", ""),
        	('2', "Product", ""),
        	('3', "Sum", ""),
        	('4', "Difference", ""),
        	('5', "Power", ""),
        	('6', "Division", ""),
        	('7', "Minimum", ""),
        	('8', "Maximum", ""),
        	('9', "Absolute Difference", ""),
    	),
        'default' : '0',
    },
    {
        'attr' : 'product',
        'desc' : "(color_a*mult_a)*(color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'division',
        'desc' : "(color_a*mult_a)/(color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'minimum',
        'desc' : "Min(color_a*mult_a , color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'maximum',
        'desc' : "Max(color_a*mult_a , color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'sum',
        'desc' : "(color_a*mult_a)+(color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'difference',
        'desc' : "(color_a*mult_a)-(color_b*mult_b)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'result_a',
        'desc' : "color_a*mult_a",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'result_b',
        'desc' : "color_b*mult_b",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'red',
        'desc' : "(color_a*mult_a).r",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'green',
        'desc' : "(color_a*mult_a).g",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'blue',
        'desc' : "(color_a*mult_a).b",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'alpha',
        'desc' : "(color_a*mult_a).a",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'intensity',
        'desc' : "mult_a*(color_a.r+color_a.g+color_a.b)/3.0",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'power',
        'desc' : "(color_a*mult_a)^mult_b",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
)

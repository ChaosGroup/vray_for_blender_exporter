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
ID   = 'TexTemperature'
NAME = 'Temperature'
DESC = "Temperature"

PluginParams = (
    {
        'attr' : 'color_mode',
        'name' : "Mode",
        'desc' : "Choose color or temperature mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Color",       "Use color"),
            ('1', "Temperature", "Use temperature"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'temperature',
        'desc' : "Material temperature in kelvins",
        'type' : 'FLOAT_TEXTURE',
        'default' : 6500,
        'ui' : {
            'min' : 0.0,
            'max' : 100000,
        },
    },
    {
        'attr' : 'color',
        'desc' : "Texture color",
        'type' : 'COLOR',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'rgb_multiplier',
        'desc' : "Color multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'alpha',
        'desc' : "Alpha color channel",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'gamma_correction',
        'desc' : "Gamma correction value",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "color_mode" }
        ]
    },

    {   "layout" : "COLUMN",
        "align" : false,
        "attrs" : [
            { "name" : "rgb_multiplier" },
            { "name" : "gamma_correction" },
            { "name" : "alpha" }
        ]
    }
]}
"""

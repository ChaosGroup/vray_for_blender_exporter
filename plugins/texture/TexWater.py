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
ID   = 'TexWater'
NAME = 'Water'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvwgen',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },

    {
        'attr' : 'height_mult',
        'desc' : "multiplier for the height of the water",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'wind_direction',
        'desc' : "direction of the wind",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'wind_magnitude',
        'desc' : "magnitude of the wind",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'wind_direction_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'choppy_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'movement_rate',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'seed',
        'desc' : "Used to produce different waters",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'resolution',
        'desc' : "Resolution -> real resolution is 2^res",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'patch_size',
        'desc' : "Size of the patch -> real resolution is 2^res",
        'type' : 'FLOAT',
        'default' : 128,
    },

    {
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "height_mult" },
                    { "name" : "choppy_mult" }
                ]
            },
            {   "layout" : "COLUMN",
                    "align" : true,
                    "attrs" : [
                        { "name" : "wind_direction" },
                        { "name" : "wind_direction_mult" },
                        { "name" : "wind_magnitude" }
                    ]
                }
        ]
    },

    {   "layout" : "COLUMN",
        "align" : false,
        "attrs" : [
            { "name" : "movement_rate" }
        ]
    },

    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "resolution" },
            { "name" : "patch_size" }
        ]
    },

    {   "layout" : "COLUMN",
        "align" : false,
        "attrs" : [
            { "name" : "seed" },
            { "name" : "use_3d_mapping" }
        ]
    }
]}
"""

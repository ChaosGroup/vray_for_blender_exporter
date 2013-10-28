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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexCellular'
NAME = 'Cellular'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)

PluginParams.extend([
    {
        'attr' : 'center_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'edge_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'bg_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'spread',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'density',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'type',
        'desc' : "Type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Dots", ""),
            ('1', "Chips", ""),
            ('2', "Cells", ""),
            ('3', "Chess Cells", ""),
            ('4', "Plasma", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'low',
        'desc' : "Low threshold (for the bg color)",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'middle',
        'desc' : "Middle threshold (for the edge color)",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'high',
        'desc' : "High threshold (for the center color)",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'fractal',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'fractal_iterations',
        'desc' : "The number of fractal iterations",
        'type' : 'FLOAT',
        'default' : 3,
    },
    {
        'attr' : 'fractal_roughness',
        'desc' : "The fractal roughness (0.0f is very rough; 1.0 is smooth - i.e. no fractal)",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'components',
        'desc' : "Outputs (F(1), F(2), F(3)) (the distances to the three closest points in the cellular context) as a Vector",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "type" }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Cell Characteristics" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "size" },
                    { "name" : "spread" },
                    { "name" : "density" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "fractal" },
                    { "name" : "fractal_iterations", "label" : "Iterations" },
                    { "name" : "fractal_roughness", "label" : "Roughness" }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Thresholds" },

    {   "layout" : "ROW",
        "align" : true,
        "attrs" : [
            { "name" : "low" },
            { "name" : "middle" },
            { "name" : "high" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)

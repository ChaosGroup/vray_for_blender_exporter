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
ID   = 'TexTiles'
NAME = 'Tiles'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)

PluginParams.extend([
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
        'desc' : "Tiles pattern",
        'type' : 'ENUM',
        'items' : (
            ('0', "Custom Tiles",        "Custom Tiles."),
            ('1', "Running Bond",        "Running Bond."),
            ('2', "Common Flemish Bond", "Common Flemish Bond."),
            ('3', "English Bond",        "English Bond."),
            ('4', "1/2 Running Bond",    "1/2 Running Bond."),
            ('5', "Stack Bond",          "Stack Bond."),
            ('6', "Fine Running Bond",   "Fine Running Bond."),
            ('7', "Fine Stack Bond",     "Fine Stack Bond.")
        ),
        'default' : '0',
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
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "pattern_type" }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Tiles Setup" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "horizontal_count" },
                    { "name" : "vertical_count" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "color_variance" },
                    { "name" : "fade_variance" }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Grout Setup" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "horizontal_gap", "label" : "H. Gap" },
                    { "name" : "vertical_gap", "label" : "V. Gap" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "holes" },
                    { "name" : "edge_roughness", "label" : "Edge rough." }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Custom Setup" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "column_modify" },
                    { "name" : "per_column" },
                    { "name" : "column_change" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "row_modify" },
                    { "name" : "per_row" },
                    { "name" : "row_change" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "line_shift" },
            { "name" : "random_shift" }
        ]
    },

    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "random_seed" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)

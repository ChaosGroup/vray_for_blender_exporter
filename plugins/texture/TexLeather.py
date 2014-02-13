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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexLeather'
NAME = 'Leather'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)
PluginParams.extend([
    # {
    #     'attr' : 'cell_color',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (1, 1, 1),
    # },
    {
        'attr' : 'cell_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.375, 0.157, 0.059),
    },
    # {
    #     'attr' : 'cell_color_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    # {
    #     'attr' : 'crease_color',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'crease_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.235, 0.118, 0.0),
    },
    # {
    #     'attr' : 'crease_color_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'size',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'density',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'spottyness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.1,
    },
    {
        'attr' : 'randomness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'threshold',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.83,
    },
    {
        'attr' : 'creases',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },

])

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "size" },
                    { "name" : "density" },
                    { "name" : "spottyness" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "randomness" },
                    { "name" : "threshold" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "creases" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)

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
import mathutils

from vb25.lib import ExportUtils


TYPE = 'BRDF'
ID   = 'BRDFMirror'
NAME = 'Mirror'
DESC = ""

PluginParams = (
    {
        'attr' : 'color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'color_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'transparency',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'transparency_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'back_side',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'trace_reflections',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'trace_depth',
        'desc' : "The maximum reflection depth (-1 is controlled by the global options)",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'affect_alpha',
        'desc' : "Specifies how render channels are propagated through the BRDF",
        'type' : 'ENUM',
        'items' : (
            ('0', "Color Only",   "The transperency will affect only the RGB channel of the final render"),
            ('1', "Color+Alpha",  "This will cause the material to transmit the alpha of the reflected objects, instead of displaying an opaque alpha"),
            ('2', "All Channels", "All channels and render elements will be affected by the transperency of the material"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'reflect_exit_color',
        'desc' : "The color to use when the maximum depth is reached",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'reflect_dim_distance',
        'desc' : "How much to dim reflection as length of rays increases",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'reflect_dim_distance_on',
        'desc' : "True to enable dim distance",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reflect_dim_distance_falloff',
        'desc' : "Fall off for the dim distance",
        'type' : 'FLOAT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "cutoff" }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "trace_reflections" },
            { "name" : "trace_depth", "active" : { "prop" : "trace_reflections" } }
        ]
    },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "trace_reflections" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "reflect_dim_distance_on", "label" : "Dim Distance" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "active" : { "prop" : "reflect_dim_distance_on" },
                "attrs" : [
                    { "name" : "reflect_dim_distance", "label" : "Distance" },
                    { "name" : "reflect_dim_distance_falloff", "label" : "Falloff" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "reflect_exit_color" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "affect_alpha" },
            { "name" : "back_side" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'color' : mathutils.Color((0.0, 0.0, 0.0)),
        'color_tex_mult' : 1.0,
        'transparency' : mathutils.Color((0.0, 0.0, 0.0)),
        'transparency_tex_mult' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

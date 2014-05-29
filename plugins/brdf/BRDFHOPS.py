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
import mathutils

from vb30.lib import ExportUtils


TYPE = 'BRDF'
ID   = 'BRDFHOPS'
NAME = 'HOPS'
DESC = ""

PluginParams = (
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
        'default' : (0, 0, 0),
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
    {
        'attr' : 'glossyAsGI',
        'name' : "Glossy As GI",
        'desc' : "Determines if the glossy rays are treated by V-Ray as GI rays",
        'type' : 'ENUM',
        'items' : (
            ('0', "Never",  "Never"),
            ('1', "GI" ,    "Only for rays that are already marked as GI"),
            ('2', "Always", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'csv_path',
        'desc' : "",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'csv_color_filter',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'flakes_csv_path',
        'desc' : "",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'coat_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'coat_strength',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.05,
    },
    {
        'attr' : 'coat_glossiness',
        'desc' : "The glossiness of the coat layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'coat_bump_float',
        'desc' : "Bump texture for the coat layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'coat_bump_color',
        'desc' : "Bump texture for the coat layer (color version)",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'coat_bump_amount',
        'desc' : "Bump amount for the coat layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'coat_bump_type',
        'desc' : "The type of bump mapping",
        'type' : 'ENUM',
        'items' : (
            ('0', "Bump",              ""),
            ('1', "Normal (Tangent)" , ""),
            ('2', "Normal (Object)",   ""),
            ('3', "Normal (Camera)",   ""),
            ('4', "Normal (World)",    ""),
            ('5', "From Bump Output",  ""),
            ('6', "Explicit Normal",   ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'coat_traceReflections',
        'desc' : "Toggle reflections for coat layer",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'coat_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'flake_scale',
        'desc' : "Flake scale - aparent flakes size in the real world",
        'type' : 'FLOAT',
        'default' : 0.005,
    },
    {
        'attr' : 'flake_size',
        'desc' : "Flake size multiplier (larger values = more flake overlap)",
        'type' : 'FLOAT',
        'default' : 0.125,
    },
    {
        'attr' : 'flake_traceReflections',
        'desc' : "Toggle reflections for flake layer",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'doubleSided',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'flake_glossiness',
        'desc' : "Flake glossiness (only if reflections are enabled)",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'environment_override',
        'desc' : "Environment override texture",
        'type' : 'TEXTURE',
        'option' : ['LINKED_ONLY'],
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },

    {
        'attr' : 'enabled_layers',
        'desc' : "Enabled layers OR mask (1 - base, 2 - flakes, 4 - coat)",
        'type' : 'INT',
        'skip' : True,
        'default' : 7,
    },
    {
        'attr' : 'enabled_layers_base',
        'name' : "Base",
        'desc' : "Enabled Base layer",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
    {
        'attr' : 'enabled_layers_flakes',
        'name' : "Flakes",
        'desc' : "Enabled Flakes layer",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
    {
        'attr' : 'enabled_layers_coat',
        'name' : "Coat",
        'desc' : "Enabled Coat layer",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "csv_path" },
            { "name" : "flakes_csv_path" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "enabled_layers_base" },
            { "name" : "enabled_layers_flakes" },
            { "name" : "enabled_layers_coat" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SEPARATOR",
        "label" : "Coat Layer" },

    {   "layout" : "ROW",
        "active" : { "prop" : "enabled_layers_base" },
        "attrs" : [
            { "name" : "coat_bump_type", "label" : "Bump Type" }
        ]
    },

    {   "layout" : "ROW",
        "active" : { "prop" : "enabled_layers_base" },
        "attrs" : [
            { "name" : "coat_subdivs", "label" : "Subdivs" },
            { "name" : "coat_traceReflections", "label" : "Trace Reflections" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SEPARATOR",
        "label" : "Flake Layer" },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "enabled_layers_flakes" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_scale", "label" : "Scale" },
                    { "name" : "flake_size", "label" : "Size" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_glossiness", "label" : "Glossiness" },
                    { "name" : "flake_traceReflections", "label" : "Trace Reflections" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "subdivs" },
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

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "reflect_exit_color" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "csv_color_filter" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "affect_alpha" },
            { "name" : "glossyAsGI" },
            { "name" : "back_side" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'transparency' : mathutils.Color((0.0, 0.0, 0.0)),
        'transparency_tex_mult' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

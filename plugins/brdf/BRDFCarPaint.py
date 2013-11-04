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


TYPE = 'BRDF'
ID   = 'BRDFCarPaint'
NAME = 'Car Paint'
DESC = "Car paint imitation"

PluginParams = (
    {
        'attr' : 'base_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.3, 0.4, 0.5),
    },
    {
        'attr' : 'base_reflection',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'base_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.6,
    },
    {
        'attr' : 'base_bump_float',
        'desc' : "Bump texture for the base layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'base_bump_color',
        'desc' : "Bump texture for the base layer (color version)",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'base_bump_amount',
        'desc' : "Bump amount for the base layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'base_bump_type',
        'desc' : "The type of bump mapping (see BRDFBump for more details)",
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
        'attr' : 'base_traceReflections',
        'desc' : "Toggle reflections for base layer",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'flake_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.3, 0.4, 0.8),
    },
    {
        'attr' : 'flake_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'flake_orientation',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.3,
    },
    {
        'attr' : 'flake_density',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_scale',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'flake_size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_map_size',
        'desc' : "The size of the internal flakes map",
        'type' : 'INT',
        'default' : 1024,
    },
    {
        'attr' : 'flake_filtering_mode',
        'desc' : "Flake filtering mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Simple", ""),
            ('1', "Directional", ""),

        ),
        'default' : '1',
    },
    {
        'attr' : 'flake_seed',
        'desc' : "The random seed for the flakes",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'flake_uvwgen',
        'desc' : "",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'flake_traceReflections',
        'desc' : "Toggle reflections for flake layer",
        'type' : 'BOOL',
        'default' : True,
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
        'default' : 0.0,
    },
    {
        'attr' : 'coat_bump_color',
        'desc' : "Bump texture for the coat layer (color version)",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'coat_bump_amount',
        'desc' : "Bump amount for the coat layer",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
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
        'default' : True,
    },
    {
        'attr' : 'traceReflections',
        'name' : "Trace Reflections",
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'doubleSided',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'cutoff_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'mapping_type',
        'desc' : "The mapping method for the flakes",
        'type' : 'ENUM',
        'items' : (
            ('0', "Explicit",  "Explicit mapping channel"),
            ('1', "Triplanar", "Triplanar projection in object space"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'mapping_channel',
        'desc' : "The mapping channel",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'environment_override',
        'desc' : "Environment override texture",
        'type' : 'TEXTURE',
        'default' : (1.0,1.0,1.0),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SEPARATOR",
        "label" : "Coat Layer" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "coat_bump_type", "label" : "Bump Type" },
            { "name" : "coat_traceReflections", "label" : "Trace Reflections" }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Flake Layer" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_density", "label" : "Density" },
                    { "name" : "flake_scale", "label" : "Scale" },
                    { "name" : "flake_size", "label" : "Size" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_filtering_mode", "label" : "" },
                    { "name" : "flake_map_size", "label" : "Map Size" },
                    { "name" : "flake_seed", "label" : "Seed" },
                    { "name" : "flake_traceReflections", "label" : "Trace Reflections" }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Base Layer" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "base_bump_type", "label" : "Bump Type" },
            { "name" : "base_traceReflections", "label" : "Trace Reflections" }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Options" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "subdivs" },
                    { "name" : "cutoff_threshold", "label" : "Cutoff" },
                    { "name" : "doubleSided" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "mapping_type", "label" : "" },
                    { "name" : "mapping_channel" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "environment_priority" }
        ]
    }
]}
"""

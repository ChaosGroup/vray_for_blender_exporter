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

import TexCommonParams3dsMax


TYPE = 'TEXTURE'
ID   = 'TexFalloff'
NAME = 'Falloff'
DESC = ""

PluginParams = list(TexCommonParams3dsMax.PluginParams)

PluginParams.extend([
    {
        'attr' : 'color1',
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color2',
        'desc' : "Second color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },

    {
        'attr' : 'type',
        'desc' : "Type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Towards / Away", ""),
            ('1', "Perpendicular / Parallel", ""),
            ('2', "Fresnel", ""),
            ('3', "Shadow / Light", ""),
            ('4', "Distance Blend", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'direction_type',
        'desc' : "Direction type",
        'type' : 'ENUM',
        'items' : (
            ('0', "View Z",   ""),
            ('1', "View X",   ""),
            ('2', "View Y",   ""),
            ('3', "Explicit", ""),
            ('4', "Local X",  ""),
            ('5', "Local Y",  ""),
            ('6', "Local Z",  ""),
            ('7', "World X",  ""),
            ('8', "World Y",  ""),
            ('9', "World Z",  "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'fresnel_ior',
        'desc' : "IOR for the Fresnel falloff type",
        'type' : 'FLOAT',
        'default' : 1.6,
    },
    {
        'attr' : 'dist_extrapolate',
        'desc' : "Extrapolate for the distance blend falloff type",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dist_near',
        'desc' : "Near distance for the distance blend falloff type",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'dist_far',
        'desc' : "Far distance for the distance blend falloff type",
        'type' : 'FLOAT',
        'default' : 100,
    },
    {
        'attr' : 'explicit_dir',
        'desc' : "Direction for the explicit direction type",
        'type' : 'VECTOR',
        'default' : (0, 0, 1),
    },

    {
        'attr' : 'use_blend_input',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'blend_input',
        'desc' : "If specified and 'Use Blend Input' is true, the final blending amount will be taken from this texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'blend_output',
        'desc' : "The blending amount, based on the parameters",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "type" },
            { "name" : "direction_type" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "fresnel_ior" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "dist_near" },
                    { "name" : "dist_far" },
                    { "name" : "dist_extrapolate" }
                ]
            }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams3dsMax.PluginWidget)

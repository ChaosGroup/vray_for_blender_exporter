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
ID   = 'TexNoise'
NAME = 'Noise (Maya)'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },

    {
        'attr' : 'persistence',
        'desc' : "amplitude(i+1) = amplitude(i) / persistence",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'amplitude_ratio',
        'desc' : "amplitude(i+1) = amplitude(i) * amplitude_ratio",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'frequency_ratio',
        'desc' : "frequency(i+1) = frequency(i) * frequency_ratio",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'frequency1',
        'name' : "Frequency",
        'desc' : "The starting frequency",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'amplitude1',
        'name' : "Amplitude",
        'desc' : "The starting amplitude",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'octaves',
        'desc' : "",
        'type' : 'INT',
        'default' : 3,
    },
    {
        'attr' : 'noiseType',
        'desc' : "Noise type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Noise", ""),
            ('1', "Perlin Noise", ""),
            ('2', "Inflected Perlin Noise", ""),
            ('3', "Marble (With Perlin)", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'frequency_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'amplitude_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'inflection',
        'desc' : "Inflection",
        'type' : 'BOOL',
        'default' : False,
    },
    # {
    #     'attr' : 'color1',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    # {
    #     'attr' : 'color2',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (1, 1, 1),
    # },
    {
        'attr' : 'color1_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'color2_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'color1_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    # {
    #     'attr' : 'color2_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'clamp',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'dimensions',
        'desc' : "Two or Three dimensional noise",
        'type' : 'ENUM',
        'items' : (
            ('2', "2D", ""),
            ('3', "3D", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'time',
        'desc' : "The time of the noise, this will act as a third or fourth dimension to the noise generating function",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'threshold',
        'desc' : "Value added to the noise function, noise function values above 1.0 are clamped",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'scale',
        'desc' : "Scale for the noise UVW coordinates",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'origin',
        'desc' : "Translation for the noise UVW coordinates",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'implode',
        'desc' : "Amount of implode performed on the UVW coordinates",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'implode_center',
        'desc' : "The center of the implode effect",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "noiseType" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "dimensions", "expand" : true }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "clamp" },
            { "name" : "time" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "frequency1" },
                    { "name" : "frequency_ratio", "label" : "Ratio" },
                    { "name" : "frequency_mult", "label" : "Mult" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "amplitude1" },
                    { "name" : "amplitude_ratio", "label" : "Ratio" },
                    { "name" : "amplitude_mult", "label" : "Mult" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "persistence" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "octaves" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "inflection" },
            { "name" : "use_3d_mapping" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginTextureCommonParamsWidget)

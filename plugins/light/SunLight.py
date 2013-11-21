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


TYPE = 'LIGHT'
ID   = 'SunLight'
NAME = 'Sun'
DESC = ""

PluginParams = (
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'target_transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    
    {
        'attr' : 'turbidity',
        'desc' : "Determines the amount of dust in the air and affects the color of the sun and sky. Smaller values produce a clear/blue sky, larger values yellow and orange",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 2.0,
        },
        'default' : 3,
    },
    {
        'attr' : 'ozone',
        'desc' : "Affects the color of the sun light (between 0.0 and 1.0). Smaller values make the sunlight more yellow, larger values make it blue",
        'type' : 'FLOAT',
        'default' : 0.35,
    },
    {
        'attr' : 'water_vapour',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'intensity_multiplier',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'size_multiplier',
        'desc' : "Controls the visible size of the sun. Affects the appearance of the sun disc as seen by the camera and reflections, as well as the blurriness of the sun shadows",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'filter_color',
        'desc' : "Sunlight color. Used to add user control to light color definition",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'up_vector',
        'desc' : "",
        'type' : 'VECTOR',
        'default' : (0, 0, 1),
    },
    {
        'attr' : 'invisible',
        'desc' : "When on, this option makes the sun invisible, both to the camera and to reflections",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'horiz_illum',
        'desc' : "Specifies the intensity (in lx) of the illumination on horizontal surfaces coming from the sky",
        'type' : 'FLOAT',
        'default' : 25000,
    },
    {
        'attr' : 'sky_model',
        'desc' : "Selects the procedural model used to simulate the TexSky texture",
        'type' : 'ENUM',
        'items' : (
            ('0', "Preetham et al.", ""),
            ('1', "CIE Clear", ""),
            ('2', "CIE Overcast", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'shadows',
        'desc' : "true if the light casts shadows and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'atmos_shadows',
        'desc' : "true if the light casts shadows from atmosperics and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'shadowBias',
        'desc' : "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'shadow_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    # {
    #     'attr' : 'shadow_color',
    #     'desc' : "The shadow color. Anything but black is not physically accurate",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'shadow_color_tex',
        'desc' : "A color texture that if present will override the shadowColor parameter",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'photon_radius',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 50,
    },
    {
        'attr' : 'photonSubdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 500,
    },
    {
        'attr' : 'causticSubdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 1000,
    },
    {
        'attr' : 'diffuseMult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'causticMult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'enabled',
        'desc' : "true if the light is casting light (turned on) and false otherwise; it only makes sense to use this parameter if it is animated, or if another object depends on this node but it must not be rendered",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affectDiffuse',
        'desc' : "true if the light produces diffuse lighting and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affectSpecular',
        'desc' : "true if the light produces specular hilights and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'diffuse_contribution',
        'desc' : "Diffuse contribution for the light",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'specular_contribution',
        'desc' : "Specular contribution for the light",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'channels',
        'desc' : "Render channels the result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_raw',
        'desc' : "Render channels the raw diffuse result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_diffuse',
        'desc' : "Render channels the diffuse result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_specular',
        'desc' : "Render channels the specular result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "enabled" },
            { "name" : "invisible" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "filter_color", "label" : "" },
                    { "name" : "turbidity" },
                    { "name" : "ozone" },
                    { "name" : "water_vapour" },
                    { "name" : "intensity_multiplier" },
                    { "name" : "size_multiplier" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "shadows" },
                    { "name" : "atmos_shadows" },
                    { "name" : "shadowBias" },
                    { "name" : "shadow_subdivs" },
                    { "name" : "shadow_color_tex", "label" : "" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "sky_model", "label" : "Model" },
            { "name" : "horiz_illum" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "photon_radius" },
                    { "name" : "photonSubdivs" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "causticMult" },
                    { "name" : "causticSubdivs" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "diffuseMult" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "diffuse_contribution" },
                    { "name" : "specular_contribution" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "affectDiffuse" },
                    { "name" : "affectSpecular" }
                ]
            }
        ]
    }
]}
"""

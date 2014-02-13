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


TYPE = 'LIGHT'
ID   = 'LightMesh'
NAME = 'Mesh Light'
DESC = ""

PluginParams = (
    {
        'attr' : 'enabled',
        'desc' : "true if the light is casting light (turned on) and false otherwise; it only makes sense to use this parameter if it is animated, or if another object depends on this node but it must not be rendered",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'color',
        'desc' : "Color of the light",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color_tex',
        'desc' : "A color texture that if present will override the color parameter",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'shadows',
        'desc' : "true if the light casts shadows and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'shadowColor',
        'desc' : "The shadow color. Anything but black is not physically accurate",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'shadowColor_tex',
        'desc' : "A color texture that if present will override the shadowColor parameter",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'shadowBias',
        'desc' : "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces",
        'type' : 'FLOAT',
        'default' : 0,
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
        'desc' : "Multiplier for the diffuse photons",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'causticMult',
        'desc' : "Multiplier for the caustic photons",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'cutoffThreshold',
        'desc' : "Light cut-off threshold (speed optimization). If the light intensity for a point is below this threshold, the light will not be computed",
        'type' : 'FLOAT',
        'default' : 0.001,
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
        'attr' : 'bumped_below_surface_check',
        'desc' : "true if the bumped normal should be used to check if the light dir is below the surface",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'nsamples',
        'desc' : "Number of parameter samples for motion blur",
        'type' : 'INT',
        'default' : 0,
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
    {
        'attr' : 'use_global_light_level',
        'desc' : "true if the light should use the global light level setting",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'units',
        'desc' : "Units for the intensity (0 - default, 1 - lumens, 2 - lm/m/m/sr, 3 - watts, 4 - w/m/m/sr)",
        'type' : 'ENUM',
        'items' : (
            ('0', "Default", ""),
            ('1', "Lumens", ""),
            ('2', "Lm/m/m/sr", ""),
            ('3', "Watts", ""),
            ('4', "W/m/m/sr", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'intensity',
        'desc' : "Light intensity",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'intensity_tex',
        'desc' : "A float texture that if present will override the intensity parameter",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'storeWithIrradianceMap',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'invisible',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affectReflections',
        'desc' : "true if the light appears in reflections and false otherwise",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'noDecay',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'doubleSided',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'lightPortal',
        'desc' : "Specifies if the light is a portal light",
        'type' : 'ENUM',
        'items' : (
            ('0', "Normal Light", ""),
            ('1', "Portal", ""),
            ('2', "Simple Portal", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'objectID',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'geometry',
        'desc' : "",
        'type' : 'GEOMETRY',
        'default' : "",
    },
    {
        'attr' : 'ignoreLightNormals',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'tex',
        'desc' : "The light texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'use_tex',
        'desc' : "true if the texture should be used",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'tex_resolution',
        'desc' : "The internal texture resolution",
        'type' : 'INT',
        'default' : 256,
    },
    {
        'attr' : 'cache_tex',
        'desc' : "When this is true the texture will be cached at tex_resolution x tex_resolution and this cached texture will be used to determine the texture color for shadows rays, speeding up light evaluation, especially for complex procedural textures",
        'type' : 'BOOL',
        'default' : True,
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
                "attrs" : [
                    { "name" : "lightPortal", "label" : "Mode" },
                    { "name" : "units" },
                    { "name" : "color", "label" : "" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "intensity" },
                    { "name" : "subdivs" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "shadows" },
                    { "name" : "shadowBias" },
                    { "name" : "shadowColor", "label" : "" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "doubleSided" },
                    { "name" : "noDecay" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "photonSubdivs" },
                    { "name" : "diffuseMult" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "causticSubdivs" },
                    { "name" : "causticMult" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "storeWithIrradianceMap" },
                    { "name" : "bumped_below_surface_check" },
                    { "name" : "ignoreLightNormals" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "cutoffThreshold" },
                    { "name" : "nsamples" },
                    { "name" : "use_global_light_level" }
                ]
            }
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
                    { "name" : "affectSpecular" },
                    { "name" : "affectReflections" },
                    { "name" : "affectDiffuse" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                { "name" : "tex_resolution" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "cache_tex" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "objectID" }
        ]
    }
]}
"""


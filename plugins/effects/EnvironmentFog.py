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


TYPE = 'EFFECT'
ID   = 'EnvironmentFog'
NAME = 'Fog'
DESC = ""

PluginParams = (
    {
        'attr' : 'enabled',
        'desc' : "If false, disable the rendering",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'gizmos',
        'name' : 'Gizmo',
        'desc' : "List of gizmos",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'color',
        'desc' : "Fog color",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'color_mult',
        'desc' : "Fog color multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'color_tex',
        'name' : "Color",
        'desc' : "Fog texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'emission',
        'desc' : "Fog emission color",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'emission_tex',
        'name' : "Emission",
        'desc' : "Fog emission texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'emission_mult',
        'desc' : "Fog emission multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'emission_mult_tex',
        'name' : "Emission Mult",
        'desc' : "Fog emission texture multiplier",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'distance',
        'desc' : "Distance between fog particles",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'density',
        'desc' : "Fog density",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'density_tex',
        'name' : 'Density',
        'desc' : "Texture for fog density",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'opacity_mode',
        'desc' : "Treat density as opacity",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_height',
        'desc' : "Whether or not the height should be taken into account",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'height',
        'desc' : "Fog starting point along the Z-axis",
        'type' : 'FLOAT',
        'default' : 100,
    },
    {
        'attr' : 'subdivs',
        'desc' : "Fog subdivision",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'yup',
        'desc' : "if true, y is the up axis, not z",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'solid_mode',
        'desc' : "If true, this will cause to disable randomization when sampling and take 1 sample at 0.5 density",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'solid_threshold',
        'desc' : "Solid mode transparency threshold",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'jitter',
        'desc' : "If true, add a random offset when start sampling",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'shadow_opacity',
        'desc' : "volume opacity scale for shadow rays",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'scale',
        'desc' : "stretch aspect for the 3 axis, when the fog container must grow/shrink preserving its original density",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'fade_out_mode',
        'desc' : "Fade out mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Multiply", ""),
            ('1', "Substract", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'fade_out_radius',
        'desc' : "fade out effect for the edges",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'per_object_fade_out_radius',
        'desc' : "fade out effect for the edges per object",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'scatter_gi',
        'desc' : "Scatter global illumination",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'scatter_bounces',
        'desc' : "Number of GI bounces calculated inside the fog",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'simplify_gi',
        'desc' : "Simplify global illumination",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'step_size',
        'desc' : "Size of one step through the volume",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'max_steps',
        'desc' : "Maximum number of steps through the volume",
        'type' : 'INT',
        'default' : 1000,
    },
    {
        'attr' : 'tex_samples',
        'desc' : "Number of texture samples for each step through the volume",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'cutoff_threshold',
        'desc' : "Controls when the raymarcher will stop traversing the volume",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'light_mode',
        'desc' : "Light mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Lights", ""),
            ('1', "Per-Gizmo", "Per-gizmo lights"),
            ('2', "Override", "Override Per-Gizmo Lights"),
            ('3', "Intersect", "Intersect with per-gizmo lights"),
            ('4', "Add", "Add to per-gizmo lights"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'lights',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'use_shade_instance',
        'desc' : "True if the shade instance should be used when sampling textures",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_background',
        'desc' : "Affect background",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affect_reflections',
        'desc' : "true if the fog is visible to reflection rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affect_refractions',
        'desc' : "true if the fog is visible to refraction rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affect_shadows',
        'desc' : "true if the fog affects shadow rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affect_gi',
        'name' : 'Affect GI',
        'desc' : "true if the fog affects GI rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'affect_camera',
        'desc' : "true if the fog affects primary camera rays",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "use_height" },
            { "name" : "height", "active" : { "prop" : "use_height" } }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "subdivs" }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "distance" },
            { "name" : "density" }
        ]
    },
   
    {   "layout" : "SEPARATOR" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "simplify_gi" },
            { "name" : "scatter_gi" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "scatter_bounces", "active" : { "prop" : "scatter_gi" } }
        ]
    },
    
    {   "layout" : "SEPARATOR" },


    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "light_mode" },
            { "name" : "fade_out_mode" },
            { "name" : "fade_out_radius" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "step_size" },
                    { "name" : "max_steps" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "tex_samples" },
                    { "name" : "cutoff_threshold" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "affect_background" },
                    { "name" : "affect_camera" },
                    { "name" : "affect_gi" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "affect_reflections" },
                    { "name" : "affect_refractions" },
                    { "name" : "affect_shadows" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "use_shade_instance" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    bus['volumes'].add(pluginName)

    gizmos = overrideParams['gizmos']
    gizmosList = []

    if type(gizmos) is list:
        gizmosList.extend(gizmos)
    else:
        gizmosList.append(gizmos)

    overrideParams.update({
        'color' : mathutils.Color((0.0,0.0,0.0)),
        'color_mult' : 1.0,
        'emission' : mathutils.Color((0.0,0.0,0.0)),
        'emission_mult' : 1.0,
        'gizmos' : "List(%s)" % ",".join(gizmosList),
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

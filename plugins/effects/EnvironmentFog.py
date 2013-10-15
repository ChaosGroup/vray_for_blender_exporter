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
        'skip' : True,
        'default' : "",
    },
    # {
    #     'attr' : 'color',
    #     'desc' : "Fog color",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    # {
    #     'attr' : 'color_mult',
    #     'desc' : "Fog color multiplier",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'color_tex',
        'name' : "Color",
        'desc' : "Fog texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'emission',
    #     'desc' : "Fog emission color",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'emission_tex',
        'name' : "Emission",
        'desc' : "Fog emission texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'emission_mult',
    #     'desc' : "Fog emission multiplier",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
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
        'default' : 10,
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
        'default' : False,
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


def gui(context, layout, EnvironmentFog):
    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'use_height')
    col = split.column()
    col.prop(EnvironmentFog, 'height')

    layout.separator()
    layout.prop(EnvironmentFog, 'subdivs')

    layout.separator()
    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'distance')
    col = split.column()
    col.prop(EnvironmentFog, 'density')

    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'simplify_gi')
    col = split.column()
    col.prop(EnvironmentFog, 'scatter_gi')
    layout.prop(EnvironmentFog, 'scatter_bounces')

    layout.separator()
    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'fade_out_mode')
    col.prop(EnvironmentFog, 'fade_out_radius')

    layout.separator()
    layout.prop(EnvironmentFog, 'light_mode')

    layout.separator()
    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'step_size')
    col.prop(EnvironmentFog, 'max_steps')
    col = split.column()
    col.prop(EnvironmentFog, 'tex_samples')
    col.prop(EnvironmentFog, 'cutoff_threshold')

    layout.separator()
    split = layout.split()
    col = split.column()
    col.prop(EnvironmentFog, 'affect_background')
    col.prop(EnvironmentFog, 'affect_camera')
    col.prop(EnvironmentFog, 'affect_gi')
    col = split.column()
    col.prop(EnvironmentFog, 'affect_reflections')
    col.prop(EnvironmentFog, 'affect_refractions')
    col.prop(EnvironmentFog, 'affect_shadows')

    layout.separator()
    layout.prop(EnvironmentFog, 'use_shade_instance')


def writeDatablock(bus, pluginName, PluginParams, EnvironmentFog, mappedParams):
    ofile = bus['files']['environment']
    scene = bus['scene']
    
    ofile.write("\n%s %s {" % (ID, pluginName))
    ofile.write("\n\tgizmos=List(%s);" % ",".join(mappedParams['gizmos']))
    
    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, EnvironmentFog, mappedParams, PluginParams)

    ofile.write("\n}\n")

    bus['volumes'].add(pluginName)
    
    return pluginName

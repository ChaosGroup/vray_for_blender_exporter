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

from vb25.lib   import ExportUtils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'BRDF'
ID   = 'BRDFVRayMtl'
NAME = 'VRayMtl'
DESC = "Standart V-Ray BRDF"

PluginParams = (
    {
        'attr' : 'opacity',
        'desc' : "The opacity of the material",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'diffuse',
        'desc' : "The diffuse color of the material",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5, 1),
    },
    {
        'attr' : 'roughness',
        'desc' : "The roughness of the diffuse part of the material",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'self_illumination',
        'desc' : "The self-illumination color of the material",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'self_illumination_gi',
        'desc' : "true if the self-illumination should affect GI",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'brdf_type',
        'desc' : "The BRDF type (0 - Phong, 1 - Blinn, 2 - Ward)",
        'type' : 'ENUM',
        'items' : (
            ('0', "Phong", "Phong"),
            ('1', "Blinn", "Blinn"),
            ('2', "Ward",  "Ward"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'reflect',
        'desc' : "The reflection color of the material",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'reflect_glossiness',
        'desc' : "The glossiness of the reflections",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'hilight_glossiness',
        'desc' : "The glossiness of the hilights",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'hilight_glossiness_lock',
        'desc' : "true to use the reflection glossiness also for hilights (hilight_glossiness is ignored)",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'fresnel',
        'desc' : "true to enable fresnel reflections",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'fresnel_ior',
        'desc' : "The ior for calculating the Fresnel term",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.6,
    },
    {
        'attr' : 'fresnel_ior_lock',
        'desc' : "true to use the refraction ior also for the Fresnel term (fresnel_ior is ignored)",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'reflect_subdivs',
        'desc' : "Subdivs for glossy reflectons",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'reflect_trace',
        'desc' : "true to trace reflections and false to only do hilights",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'reflect_depth',
        'desc' : "The maximum depth for reflections",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'reflect_exit_color',
        'desc' : "The color to use when the maximum depth is reached",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'hilight_soften',
        'desc' : "How much to soften hilights and reflections at grazing light angles",
        'type' : 'FLOAT',
        'default' : 0,
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
        'attr' : 'reflect_affect_alpha',
        'name' : "Affect Alpha",
        'desc' : "Determines how reflections affect the alpha channel",
        'type' : 'ENUM',
        'items' : (
            ('0', "Color Only",   "The transperency will affect only the RGB channel of the final render"),
            ('1', "Color+Alpha",  "This will cause the material to transmit the alpha of the reflected objects, instead of displaying an opaque alpha"),
            ('2', "All Channels", "All channels and render elements will be affected by the transperency of the material"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'anisotropy',
        'desc' : "The anisotropy for glossy reflections, from -1 to 1 (0.0 is isotropic reflections)",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'anisotropy_rotation',
        'desc' : "The rotation of the anisotropy axes, from 0.0 to 1.0",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'anisotropy_derivation',
        'desc' : "What method to use for deriving anisotropy axes",
        'type' : 'ENUM',
        'items' : (
            ('0', "Local Axis", "Local object axis"),
            ('1', "UvwGen",     "The specified UVW generator"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'anisotropy_axis',
        'desc' : "Which local object axis to use when anisotropy_derivation is 0",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'anisotropy_uvwgen',
        'desc' : "The uvw generator to use for anisotropy when anisotropy_derivation is 1",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'refract',
        'desc' : "The refraction color of the material",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'refract_ior',
        'desc' : "The IOR for refractions",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.6,
    },
    {
        'attr' : 'refract_glossiness',
        'desc' : "Glossiness for refractions",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'refract_subdivs',
        'desc' : "Subdivs for glossy refractions",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'refract_trace',
        'desc' : "1 to trace refractions; 0 to disable them",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'refract_depth',
        'desc' : "The maximum depth for refractions",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'refract_exit_color',
        'desc' : "The color to use when maximum depth is reached when refract_exit_color_on is true",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'refract_exit_color_on',
        'desc' : "If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'refract_affect_alpha',
        'name' : "Affect Alpha",
        'desc' : "Determines how refractions affect the alpha channel",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Color Only",   "The transperency will affect only the RGB channel of the final render"),
            ('1',  "Color+Alpha",  "This will cause the material to transmit the alpha of the reflected objects, instead of displaying an opaque alpha"),
            ('2',  "All Channels", "All channels and render elements will be affected by the transperency of the material"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'refract_affect_shadows',
        'desc' : "true to enable the refraction to affect the shadows cast by the material (as transparent shadows)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dispersion_on',
        'desc' : "true to enable dispersion",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dispersion',
        'desc' : "abbe value",
        'type' : 'FLOAT',
        'default' : 50,
    },
    # {
    #     'attr' : 'fog_color',
    #     'desc' : "The absorption (fog) color",
    #     'type' : 'COLOR',
    #     'default' : (1, 1, 1),
    # },
    {
        'attr' : 'fog_color_tex',
        'desc' : "The absorption (fog) color texture",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'fog_mult',
        'desc' : "Multiplier for the absorption",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'fog_bias',
        'desc' : "Bias for the absorption",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'fog_unit_scale_on',
        'desc' : "Enable unit scale multiplication, when calculating absorption",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'translucency',
        'desc' : "Translucency mode",
        'type' : 'ENUM',
        'items': (
            ('0', "None", ""),
            ('1', "Hard (wax) model", ""),
            ('2', "Soft (water) model", ""),
            ('3', "Hybrid model", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'translucency_color',
        'desc' : "Filter color for the translucency effect",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'translucency_light_mult',
        'desc' : "A multiplier for the calculated lighting for the translucency effect",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'translucency_scatter_dir',
        'desc' : "Scatter direction (0.0f is backward, 1.0f is forward)",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'translucency_scatter_coeff',
        'desc' : "Scattering cone (0.0f - no scattering, 1.0f - full scattering",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'translucency_thickness',
        'desc' : "Maximum distance to trace inside the object",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'option_double_sided',
        'desc' : "true if the material is double-sided",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'option_reflect_on_back',
        'desc' : "true to compute reflections for back sides of objects",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'option_glossy_rays_as_gi',
        'desc' : "Specifies when to treat GI rays as glossy rays",
        'type' : 'ENUM',
        'items' : (
            ('0', "Never", "Never"),
            ('1', "GI Rays", "Only for rays that are already marked as GI rays"),
            ('2', "Always", "Always"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'option_cutoff',
        'desc' : "Specifies a cutoff threshold for tracing reflections/refractions",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'option_use_irradiance_map',
        'desc' : "false to perform local brute-force GI calculatons and true to use the current GI engine",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'option_energy_mode',
        'desc' : "Energy preservation mode for reflections and refractions",
        'type' : 'ENUM',
        'items' : (
            ('1', "Monochrome", ""),
            ('0', "Color", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'option_fix_dark_edges',
        'desc' : "true to fix dark edges for glossy reflections with low samples; only set this to false for compatibility with older versions",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'environment_override',
        'desc' : "Environment override texture",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "Environment override priority (used when several materials override it along a ray path)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'refl_interpolation_on',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'refl_imap_min_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'refl_imap_max_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'refl_imap_color_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'refl_imap_norm_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'refl_imap_samples',
        'desc' : "",
        'type' : 'INT',
        'default' : 20,
    },
    {
        'attr' : 'refr_interpolation_on',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'refr_imap_min_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'refr_imap_max_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'refr_imap_color_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'refr_imap_norm_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'refr_imap_samples',
        'desc' : "",
        'type' : 'INT',
        'default' : 20,
    },
)


def gui(context, layout, BRDFVRayMtl, node=None):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    layout.label(text="Reflections:")

    layout.prop(BRDFVRayMtl, 'brdf_type', expand=True)
    layout.separator()

    split = layout.split()
    row = split.row(align=True)
    row.prop(BRDFVRayMtl, 'reflect_subdivs', text="Subdivs")
    row.prop(BRDFVRayMtl, 'reflect_depth', text="Depth")
    
    split = layout.split()
    row = split.row()
    row.prop(BRDFVRayMtl, 'fresnel')
    row.prop(BRDFVRayMtl, 'fresnel_ior')

    layout.prop(BRDFVRayMtl, 'reflect_affect_alpha', text="Affect Channels")
    layout.prop(BRDFVRayMtl, 'anisotropy_derivation')

    layout.separator()
    layout.label(text="Refractions:")

    split = layout.split()
    row = split.row(align=True)
    row.prop(BRDFVRayMtl, 'refract_subdivs', text="Subdivs")
    row.prop(BRDFVRayMtl, 'refract_depth', text="Depth")

    split = layout.split()
    col = split.column(align=True)
    col.prop(BRDFVRayMtl, 'dispersion_on')
    col.prop(BRDFVRayMtl, 'dispersion')
    col = split.column(align=True)
    col.prop(BRDFVRayMtl, 'fog_mult',)
    col.prop(BRDFVRayMtl, 'fog_bias', slider=True)

    layout.prop(BRDFVRayMtl, 'refract_affect_shadows')
    layout.prop(BRDFVRayMtl, 'refract_affect_alpha', text="Affect Channels")

    layout.separator()
    layout.prop(BRDFVRayMtl, 'translucency')
    if BRDFVRayMtl.translucency != '0':
        split = layout.split()
        col = split.column()
        col.prop(BRDFVRayMtl, 'translucency_color', text="")
        col.prop(BRDFVRayMtl, 'translucency_thickness', text="Thickness")
        if wide_ui:
            col = split.column()
        col.prop(BRDFVRayMtl, 'translucency_scatter_coeff', text="Scatter coeff")
        col.prop(BRDFVRayMtl, 'translucency_scatter_dir', text="Fwd/Bck coeff")
        col.prop(BRDFVRayMtl, 'translucency_light_mult', text="Light multiplier")

    layout.separator()

    split = layout.split()
    col = split.column()
    col.prop(BRDFVRayMtl, 'reflect_trace')
    col.prop(BRDFVRayMtl, 'refract_trace')
    col.prop(BRDFVRayMtl, 'option_cutoff')
    if wide_ui:
        col = split.column()
    col.prop(BRDFVRayMtl, 'option_double_sided')
    col.prop(BRDFVRayMtl, 'option_reflect_on_back')
    col.prop(BRDFVRayMtl, 'option_use_irradiance_map')

    split= layout.split()
    if wide_ui:
        sub = split.column(align=True)
        sub.prop(BRDFVRayMtl, 'reflect_dim_distance_on', text="Dim reflect ray distance")
        sub_r = sub.row()
        sub_r.active = BRDFVRayMtl.reflect_dim_distance_on
        sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance', text="Distance")
        sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance_falloff', text="Falloff")
    else:
        sub = split.column(align=True)
        sub.prop(BRDFVRayMtl, 'reflect_dim_distance_on')
        sub_r = sub.column()
        sub_r.active = BRDFVRayMtl.reflect_dim_distance_on
        sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance', text="Distance")
        sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance_falloff', text="Falloff")

    layout.separator()
    split = layout.split()
    col = split.column()
    col.prop(BRDFVRayMtl, 'reflect_exit_color')
    if wide_ui:
        col = split.column()
    col.prop(BRDFVRayMtl, 'refract_exit_color')

    layout.separator()
    layout.prop(BRDFVRayMtl, 'option_glossy_rays_as_gi')
    layout.prop(BRDFVRayMtl, 'option_energy_mode')

    layout.separator()
    layout.prop(BRDFVRayMtl, 'environment_priority')

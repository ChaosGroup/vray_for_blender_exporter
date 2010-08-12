'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


import os
import bpy

from vb25.utils import *



class VRayMaterial(bpy.types.IDPropertyGroup):
    pass

class BRDFVRayMtl(bpy.types.IDPropertyGroup):
    pass

class BRDFLight(bpy.types.IDPropertyGroup):
    pass

class BRDFSSS2Complex(bpy.types.IDPropertyGroup):
    pass

class MtlWrapper(bpy.types.IDPropertyGroup):
    pass

class MtlRenderStats(bpy.types.IDPropertyGroup):
    pass

class MtlOverride(bpy.types.IDPropertyGroup):
    pass

bpy.types.Material.PointerProperty(
	attr= 'vray_material',
	type= VRayMaterial,
	name= "V-Ray Material Settings",
	description= "V-Ray material settings"
)

VRayMaterial.PointerProperty(
	attr= 'BRDFVRayMtl',
	type= BRDFVRayMtl,
	name= "BRDFVRayMtl",
	description= "V-Ray BRDFVRayMtl settings"
)

VRayMaterial.PointerProperty(
	attr= 'BRDFSSS2Complex',
	type= BRDFSSS2Complex,
	name= "BRDFSSS2Complex",
	description= "V-Ray BRDFSSS2Complex settings"
)

VRayMaterial.PointerProperty(
	attr= 'BRDFLight',
	type= BRDFLight,
	name= "BRDFLight",
	description= "V-Ray BRDFLight settings"
)

VRayMaterial.PointerProperty(
	attr= 'MtlRenderStats',
	type= MtlRenderStats,
	name= "MtlRenderStats",
	description= "V-Ray MtlRenderStats settings"
)

VRayMaterial.PointerProperty(
	attr= 'MtlWrapper',
	type= MtlWrapper,
	name= "MtlWrapper",
	description= "V-Ray MtlWrapper settings"
)

VRayMaterial.PointerProperty(
	attr= 'MtlOverride',
	type= MtlOverride,
	name= "MtlOverride",
	description= "V-Ray MtlOverride settings"
)



'''
  VRayMaterial
'''
VRayMaterial.EnumProperty(
	attr= 'type',
	name= "Type",
	description= "Material type.",
	items=(
		('MTL',  "Basic", "Basic V-Ray material."),
		('SSS',  "SSS",   "Fast SSS material."),
		('EMIT', "Light", "Light emitting material.")
	),
	default= 'MTL'
)

VRayMaterial.EnumProperty(
	attr= 'emitter_type',
	name= "Emitter type",
	description= "This determines the type of BRDF (the shape of the hilight).",
	items=(
		('MTL',  "Material",   ""),
		('MESH', "Mesh light",  "")
	),
	default= 'MTL'
)

VRayMaterial.BoolProperty(
	attr= 'two_sided',
	name= "Two sided material",
	description= "Simple \"Two sided\" material. Use nodes for advanced control.",
	default= False
)

VRayMaterial.FloatProperty(
	attr= 'two_sided_translucency',
	name= "Two sided translucency",
	description= "Translucency between front and back.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.5
)

VRayMaterial.BoolProperty(
	attr= 'use_wrapper',
	name= "Use material wrapper",
	description= "Use material wrapper options.",
	default= False
)

VRayMaterial.BoolProperty(
	attr= 'use_renderstats',
	name= "Use material render options",
	description= "Use material render options.",
	default= False
)

VRayMaterial.BoolProperty(
	attr= 'use_override',
	name= "Use override material",
	description= "Use override material.",
	default= False
)



'''
  BRDFVRayMtl
'''
BRDFVRayMtl.FloatVectorProperty(
	attr="fog_color",
	name="Fog color",
	description="Fog color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(1.0, 1.0, 1.0)
)

BRDFVRayMtl.FloatVectorProperty(
	attr="refract_color",
	name="Refraction color",
	description="Refraction color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

BRDFVRayMtl.FloatVectorProperty(
	attr="reflect_color",
	name="Reflection color",
	description="Reflection color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

BRDFVRayMtl.FloatVectorProperty(
	attr='reflect_exit_color',
	name="Reflection exit color",
	description="Reflection exit color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

BRDFVRayMtl.BoolProperty(
	attr="fresnel",
	name="Frensnel reflections",
	description="Enable frensnel reflections.",
	default= False
)

BRDFVRayMtl.BoolProperty(
	attr="fresnel_ior_lock",
	name="Frensnel reflections lock",
	description="",
	default= True
)

BRDFVRayMtl.FloatProperty(
	attr="fresnel_ior",
	name="Fresnel IOR",
	description="",
	min=0.0, max=10.0,
	soft_min=0.0, soft_max=10.0,
	default= 1.6
)

BRDFVRayMtl.IntProperty(
	attr= 'reflect_subdivs',
	name= "Reflection subdivs",
	description= "Subdivs for glossy reflections",
	min= 1,
	max= 256,
	default= 8
)

BRDFVRayMtl.IntProperty(
	attr= 'reflect_depth',
	name= "Reflections depth",
	description= "The maximum depth for reflections.",
	min= 1,
	max= 256,
	default= 5
)

BRDFVRayMtl.IntProperty(
	attr= 'refract_depth',
	name= "Refractions depth",
	description= "The maximum depth for refractions.",
	min= 1,
	max= 256,
	default= 5
)

BRDFVRayMtl.IntProperty(
	attr= 'refract_subdivs',
	name= "Refraction subdivs",
	description= "Subdivs for glossy refractions",
	min= 1,
	max= 256,
	default= 8
)

BRDFVRayMtl.FloatProperty(
	attr="roughness",
	name="Roughness",
	description="",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default= 0.0
)

BRDFVRayMtl.FloatProperty(
	attr="hilight_glossiness",
	name="Hilight gloss",
	description="",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default= 1.0
)

BRDFVRayMtl.BoolProperty(
	attr="hilight_glossiness_lock",
	name="Hilight glossiness lock",
	description="",
	default= True
)

BRDFVRayMtl.FloatProperty(
	attr= 'hilight_soften',
	name= "Hilight soften",
	description= "How much to soften hilights and reflections at grazing light angles",
	min= 0.0, max=1.0,
	soft_min= 0.0, soft_max=1.0,
	default= 0.0
)

BRDFVRayMtl.FloatProperty(
	attr= 'reflect_dim_distance',
	name= "reflect dim distance",
	description= "How much to dim reflection as length of rays increases",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1e+18
)

BRDFVRayMtl.BoolProperty(
	attr= 'reflect_dim_distance_on',
	name= "reflect dim distance on",
	description= "True to enable dim distance",
	default= False
)

BRDFVRayMtl.FloatProperty(
	attr= 'reflect_dim_distance_falloff',
	name= "reflect dim distance falloff",
	description= "Fall off for the dim distance",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0
)

BRDFVRayMtl.IntProperty(
	attr= 'anisotropy_derivation',
	name= "anisotropy derivation",
	description= "What method to use for deriving anisotropy axes (0 - local object axis; 1 - a specified uvw generator)",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 0
)

BRDFVRayMtl.IntProperty(
	attr= 'anisotropy_axis',
	name= "anisotropy axis",
	description= "Which local object axis to use when anisotropy_derivation is 0",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 2
)

BRDFVRayMtl.BoolProperty(
	attr="refract_affect_shadows",
	name="Affect shadows",
	description="",
	default= False
)

BRDFVRayMtl.BoolProperty(
	attr="refract_affect_alpha",
	name="Affect alpha",
	description="",
	default= False
)

BRDFVRayMtl.FloatProperty(
	attr= 'fog_mult',
	name= "Fog multiplier",
	description= "",
	min= 0.0, max= 10.0,
	soft_min= 0.0, soft_max= 1.0,
	precision= 4,
	default= 0.001
)

BRDFVRayMtl.BoolProperty(
	attr='fog_unit_scale_on',
	name="Fog unit scale",
	description="Enable unit scale multiplication, when calculating absorption",
	default= True
)

BRDFVRayMtl.FloatProperty(
	attr= 'fog_bias',
	name= "Fog bias",
	description= "",
	min= -100.0, max= 100.0,
	soft_min= -1.0, soft_max= 1.0,
	precision= 4,
	default= 0.0
)

BRDFVRayMtl.FloatProperty(
	attr="fog_ior",
	name="Fog bias",
	description="",
	min=0.0, max=10.0,
	soft_min=0.0, soft_max=1.0,
	default= 1.0
)

BRDFVRayMtl.FloatProperty(
	attr="anisotropy",
	name="Anisotropy",
	description="",
	min=-1.0, max=1.0,
	soft_min=-1.0, soft_max=1.0,
	default= 0.0
)

BRDFVRayMtl.FloatProperty(
	attr="anisotropy_rotation",
	name="Rotation",
	description="Anisotropy rotation",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default= 0.0
)

BRDFVRayMtl.EnumProperty(
	attr='brdf_type',
	name="BRDF type",
	description="This determines the type of BRDF (the shape of the hilight).",
	items=(
		("PHONG", "Phong", "Phong hilight/reflections."),
		("BLINN", "Blinn", "Blinn hilight/reflections."),
		("WARD",  "Ward",  "Ward hilight/reflections.")
	),
	default= 'BLINN'
)

BRDFVRayMtl.BoolProperty(
	attr="refract_trace",
	name="Trace refractions",
	description="",
	default= True
)

BRDFVRayMtl.FloatVectorProperty(
	attr= 'refract_exit_color',
	name= "refract exit color",
	description= "The color to use when maximum depth is reached when refract_exit_color_on is true",
	subtype= "COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0,0,0)
)

BRDFVRayMtl.BoolProperty(
	attr= 'refract_exit_color_on',
	name= "refract exit color on",
	description= "If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray",
	default= False
)

BRDFVRayMtl.BoolProperty( 
	attr= "reflect_trace", 
	name= "Trace reflections", 
	description= 'TODO.', 
	default= False
)

BRDFVRayMtl.BoolProperty(
	attr="option_reflect_on_back",
	name="Reflect on back side",
	description="",
	default= False
)

BRDFVRayMtl.BoolProperty(
	attr="option_double_sided",
	name="Double-sided",
	description="",
	default= True
)

# option_option_glossy_rays_as_gi: integer (Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always)
BRDFVRayMtl.EnumProperty(
	attr= 'option_glossy_rays_as_gi',
	name= 'Glossy rays as GI',
	description= "Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always",
	items=(
		("ALWAYS", "Always",            ""),
		("GI",     "Only for GI rays",  ""),
		("NEVER",  "Never",             "")
	),
	default= 'GI'
)

BRDFVRayMtl.FloatProperty(
	attr= 'option_cutoff',
	name= 'Cutoff',
	description= "Specifies a cutoff threshold for tracing reflections/refractions",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.001
)

# option_option_use_irradiance_map: BRDFVRayMtl.Bool (false to perform local brute-force GI calculatons and true to use the current GI engine)
BRDFVRayMtl.BoolProperty(
	attr= 'option_use_irradiance_map',
	name= 'Use irradiance map',
	description= "false to perform local brute-force GI calculatons and true to use the current GI engine",
	default= True
)

# option_option_energy_mode: integer (Energy preservation mode for reflections and refractions (0 - color, 1 - monochrome))
BRDFVRayMtl.EnumProperty(
	attr= 'option_energy_mode',
	name= 'Energy mode',
	description= "Energy preservation mode for reflections and refractions.",
	items=(("MONO",  "Monochrome", ""),
		   ("COLOR", "Color",      "")),
	default= 'COLOR'
)

# environment_override: acolor texture (Environment override texture)

# environment_priority: integer (Environment override priority (used when several materials override it along a ray path))
BRDFVRayMtl.IntProperty(
	attr= 'environment_priority',
	name= "Environment priority",
	description= "Environment override priority (used when several materials override it along a ray path)",
	min= 0,
	max= 10,
	default= 0
)

# translucency: integer (Translucency mode (0 - none))
BRDFVRayMtl.EnumProperty(
	attr= 'translucency',
	name= "Translucency",
	description= "Translucency mode",
	items=(
		("HYBRID", "Hybrid model",       ""),
		("SOFT",   "Soft (water) model", ""),
		("HARD",   "Hard (wax) model",   ""),
		("NONE",   "None",               "")
	),
	default= 'NONE'
)

# translucency_color: acolor texture (Filter color for the translucency effect) = AColor(1, 1, 1, 1)
BRDFVRayMtl.FloatVectorProperty(
	attr= 'translucency_color',
	name= 'Translucency_color',
	description= "Filter color for the translucency effect.",
	subtype= "COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0, 1.0, 1.0)
)

# translucency_light_mult: BRDFVRayMtl.Float (A multiplier for the calculated lighting for the translucency effect)
BRDFVRayMtl.FloatProperty(
	attr= 'translucency_light_mult',
	name= 'Translucency light mult',
	description= "A multiplier for the calculated lighting for the translucency effect",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# translucency_scatter_dir: BRDFVRayMtl.Float (Scatter direction (0.0f is backward, 1.0f is forward))
BRDFVRayMtl.FloatProperty(
	attr= 'translucency_scatter_dir',
	name= 'Translucency scatter dir',
	description= "Scatter direction (0.0 is backward, 1.0 is forward)",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.5
)

# translucency_scatter_coeff: BRDFVRayMtl.Float (Scattering cone (0.0f - no scattering, 1.0f - full scattering)
BRDFVRayMtl.FloatProperty(
	attr= 'translucency_scatter_coeff',
	name= 'Translucency scatter coeff',
	description= "Scattering cone (0.0 - no scattering, 1.0 - full scattering",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

# translucency_thickness: BRDFVRayMtl.Float (Maximum distance to trace inside the object)
BRDFVRayMtl.FloatProperty(
	attr= 'translucency_thickness',
	name= 'Translucency thickness',
	description= "Maximum distance to trace inside the object",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1e+18
)



'''
  Plugin: MtlRenderStats
'''
# base_mtl: plugin (Base material)

# camera_visibility: bool
MtlRenderStats.BoolProperty(
	attr= 'camera_visibility',
	name= 'Camera visibility',
	description= "TODO.",
	default= True
)

# reflections_visibility: MtlRenderStats.Bool
MtlRenderStats.BoolProperty(
	attr= 'reflections_visibility',
	name= 'Reflections visibility',
	description= "TODO.",
	default= True
)

# refractions_visibility: MtlRenderStats.Bool
MtlRenderStats.BoolProperty(
	attr= 'refractions_visibility',
	name= 'Refractions visibility',
	description= "TODO.",
	default= True
)

# gi_visibility: MtlRenderStats.Bool
MtlRenderStats.BoolProperty(
	attr= 'gi_visibility',
	name= 'GI visibility',
	description= "TODO.",
	default= True
)

# shadows_visibility: MtlRenderStats.Bool
MtlRenderStats.BoolProperty(
	attr= 'shadows_visibility',
	name= 'Shadows visibility',
	description= "TODO.",
	default= True
)

# visibility: float (Overall visibility)
MtlRenderStats.BoolProperty(
	attr= 'visibility',
	name= 'Overall visibility',
	description= "TODO.",
	default= True
)



'''
  Plugin: BRDFLight
'''
BRDFLight.BoolProperty( 
	attr= "emitOnBackSide", 
	name= "Emit on back side", 
	description= 'TODO.', 
	default= False
)


BRDFLight.BoolProperty( 
	attr= "compensateExposure", 
	name= "Compensate camera exposure", 
	description= 'TODO.', 
	default= False
)



'''
  Plugin: BRDFSSS2Complex
'''
BRDFSSS2Complex.IntProperty(
	attr= "prepass_rate",
	name= "Prepass rate", 
	description= "Sampling density for the illumination map.", 
	min= -10, 
	max=  10, 
	default= -1
)

BRDFSSS2Complex.FloatProperty(
	attr= "interpolation_accuracy", 
	name= "Interpolation accuracy", 
	description= "Interpolation accuracy for the illumination map; normally 1.0 is fine.", 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

BRDFSSS2Complex.FloatProperty(
	attr= "scale", 
	name= "Scale", 
	description= "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smalle.", 
	min= 0.0, 
	max= 1000.0, 
	soft_min= 0.0, 
	soft_max= 1000.0, 
	precision= 4, 
	default= 1
)

BRDFSSS2Complex.FloatProperty(
	attr= "ior", 
	name= "IOR", 
	description= 'TODO.', 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.5
)

BRDFSSS2Complex.FloatProperty(
	attr= "diffuse_amount", 
	name= "Diffuse amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 0.0
)

BRDFSSS2Complex.FloatProperty(
	attr= "scatter_radius_mult", 
	name= "Scatter radius", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

BRDFSSS2Complex.FloatVectorProperty( 
	attr= "overall_color", 
	name= "Overall color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1.0, 1.0, 1.0)
)

BRDFSSS2Complex.FloatVectorProperty( 
	attr= "diffuse_color", 
	name= "Diffuse color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

BRDFSSS2Complex.FloatVectorProperty( 
	attr= "sub_surface_color", 
	name= "Sub surface color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

BRDFSSS2Complex.FloatVectorProperty( 
	attr= "scatter_radius", 
	name= "Scatter radius", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.92, 0.52, 0.175)
)

BRDFSSS2Complex.FloatProperty(
	attr= "phase_function", 
	name= "Phase function", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0
)

BRDFSSS2Complex.FloatVectorProperty( 
	attr= "specular_color", 
	name= "Specular color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1.0, 1.0, 1.0)
)

BRDFSSS2Complex.IntProperty( 
	attr= "specular_subdivs", 
	name= "Specular subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

BRDFSSS2Complex.FloatProperty(
	attr= "specular_amount", 
	name= "Specular amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 1
)

BRDFSSS2Complex.FloatProperty(
	attr= "specular_glossiness", 
	name= "Specular glossiness", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.6
)



BRDFSSS2Complex.FloatProperty(
	attr= "cutoff_threshold", 
	name= "Cutoff threshold", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.01
)

BRDFSSS2Complex.BoolProperty(
	attr= 'trace_reflections',
	name= "Trace reflections",
	description= "TODO.",
	default= True
)

BRDFSSS2Complex.IntProperty( 
	attr= "reflection_depth", 
	name= "Reflection depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

BRDFSSS2Complex.EnumProperty(
	attr="single_scatter",
	name="Single scatter",
	description= 'TODO.', 
	items=(
		("NONE",   "None",                    ""),
		("SIMPLE", "Simple",                  ""),
		("SOLID",  "Raytraced (solid)",       ""),
		("REFR",   "Raytraced (refractive)",  "")
	),
	default= "SIMPLE"
)

BRDFSSS2Complex.IntProperty( 
	attr= "subdivs", 
	name= "Subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

BRDFSSS2Complex.IntProperty( 
	attr= "refraction_depth", 
	name= "Refraction depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

BRDFSSS2Complex.BoolProperty( 
	attr= "front_scatter", 
	name= "Front scatter", 
	description= 'TODO.', 
	default= True
)

BRDFSSS2Complex.BoolProperty( 
	attr= "back_scatter", 
	name= "Back scatter", 
	description= 'TODO.', 
	default= True
)

BRDFSSS2Complex.BoolProperty( 
	attr= "scatter_gi", 
	name= "Scatter GI", 
	description= 'TODO.', 
	default= False
)

BRDFSSS2Complex.FloatProperty(
	attr= "prepass_blur", 
	name= "Prepass blur", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1.2
)



'''
  Plugin: MtlWrapper
'''
# base_material: plugin (The base material)

# generate_gi: float (Controls the GI generated by the material.)
MtlWrapper.FloatProperty(
	attr= 'generate_gi',
	name= 'Generate GI',
	description= "Controls the GI generated by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# receive_gi: float (Controls the GI received by the material.)
MtlWrapper.FloatProperty(
	attr= 'receive_gi',
	name= 'Receive GI',
	description= "Controls the GI received by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# generate_caustics: float (Controls the caustics generated by the material.)
MtlWrapper.FloatProperty(
	attr= 'generate_caustics',
	name= 'Generate caustics',
	description= "Controls the caustics generated by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# receive_caustics: float (Controls the caustics received by the material.)
MtlWrapper.FloatProperty(
	attr= 'receive_caustics',
	name= 'Receive caustics',
	description= "Controls the caustics received by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# alpha_contribution: float (The contribution of the resulting color to the alpha channel.)
MtlWrapper.FloatProperty(
	attr= 'alpha_contribution',
	name= 'Alpha contribution',
	description= "The contribution of the resulting color to the alpha channel.",
	min= -1.0,
	max= 1.0,
	soft_min= -1.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# matte_surface: bool (Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.)
MtlWrapper.BoolProperty(
	attr= 'matte_surface',
	name= 'Matte surface',
	description= "Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.",
	default= False
)

# shadows: bool (Turn this on to make shadow visible on the matter surface.)
MtlWrapper.BoolProperty(
	attr= 'shadows',
	name= 'Shadows',
	description= "Turn this on to make shadow visible on the matter surface.",
	default= False
)

# affect_alpha: bool (Turn this on to make shadows affect the alpha contribution of the matte surface.)
MtlWrapper.BoolProperty(
	attr= 'affect_alpha',
	name= 'Affect alpha',
	description= "Turn this on to make shadows affect the alpha contribution of the matte surface.",
	default= False
)

# shadow_tint_color: color (Tint for the shadows on the matte surface.) = Color(0, 0, 0)
MtlWrapper.FloatVectorProperty( 
	attr= "shadow_tint_color", 
	name= "Shadow tint color", 
	description= 'Tint for the shadows on the matte surface.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.0, 0.0, 0.0)
)

# shadow_brightness: float (An optional brightness parameter for the shadows on the matte surface.A value of 0.0 will make the shadows completely invisible, while a value of 1.0 will show the full shadows.)
MtlWrapper.FloatProperty(
	attr= 'shadow_brightness',
	name= 'Shadow brightness',
	description= "An optional brightness parameter for the shadows on the matte surface.A value of 0.0 will make the shadows completely invisible, while a value of 1.0 will show the full shadows.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# reflection_amount: float (Shows the reflections of the base material.)
MtlWrapper.FloatProperty(
	attr= 'reflection_amount',
	name= 'Reflection amount',
	description= "Shows the reflections of the base material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# refraction_amount: float (Shows the refractions of the base material.)
MtlWrapper.FloatProperty(
	attr= 'refraction_amount',
	name= 'Refraction amount',
	description= "Shows the refractions of the base material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# gi_amount: float (Determines the amount of gi shadows.)
MtlWrapper.FloatProperty(
	attr= 'gi_amount',
	name= 'GI amount',
	description= "Determines the amount of gi shadows.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# no_gi_on_other_mattes: bool (This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.)
MtlWrapper.BoolProperty(
	attr= 'no_gi_on_other_mattes',
	name= 'No gi on other mattes',
	description= "This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.",
	default= True
)

# matte_for_secondary_rays: bool (Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc))
MtlWrapper.BoolProperty(
	attr= 'matte_for_secondary_rays',
	name= 'Matte for secondary rays',
	description= "Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc)",
	default= False
)

# gi_surface_id: integer (If two objects have different GI surface ids, the light cache samples of the two objects will not be blended)
MtlWrapper.IntProperty(
	attr= 'gi_surface_id',
	name= 'GI surface id',
	description= "If two objects have different GI surface ids, the light cache samples of the two objects will not be blended",
	min= 0,
	max= 10,
	default= 0
)

# gi_quality_multiplier: float (A multiplier for GI quality)
MtlWrapper.FloatProperty(
	attr= 'gi_quality_multiplier',
	name= 'GI quality multiplier',
	description= "A multiplier for GI quality",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# reflection_filter_tex: acolor texture = AColor(1, 1, 1, 1)
MtlWrapper.FloatVectorProperty( 
	attr= "reflection_filter_tex", 
	name= "Reflection filter",
	description= 'Reflection filter.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1.0, 1.0, 1.0)
)

# trace_depth: integer (The maximum reflection depth (-1 is controlled by the global options))
MtlWrapper.IntProperty(
	attr= 'trace_depth',
	name= 'Trace depth',
	description= "The maximum reflection depth (-1 is controlled by the global options)",
	min= -1,
	max= 1000,
	default= -1
)

# channels: plugin (Render channels the result of this BRDF will be written to), unlimited list



# '''
#   Presets
# '''
# SSS2= {
# 	'Skin_brown': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (169, 123, 92),
# 		'sub_surface_color':    (169, 123, 92),
# 		'scatter_radius':       (155, 94, 66),
# 		'scatter_radius_mult':  1.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.5
# 	},
# 	'Skin_pink': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (203, 169, 149),
# 		'sub_surface_color':    (203, 169, 149),
# 		'scatter_radius':       (177, 105, 84),
# 		'scatter_radius_mult':  1.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.5
# 	},
# 	'Skin_yellow': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (204, 165, 133),
# 		'sub_surface_color':    (204, 165, 133),
# 		'scatter_radius':       (177, 105, 84),
# 		'scatter_radius_mult':  1.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.5
# 	},
# 	'Milk_skimmed': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (230, 230, 210),
# 		'sub_surface_color':    (230, 230, 210),
# 		'scatter_radius':       (245, 184, 107),
# 		'scatter_radius_mult':  2.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.8
# 	},
# 	'Milk_whole': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (242, 239, 222),
# 		'sub_surface_color':    (242, 239, 222),
# 		'scatter_radius':       (188, 146,  90),
# 		'scatter_radius_mult':  2.0,
# 		'phase_function':       0.9,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.8
# 	},
# 	'Marble_white': {
# 		'ior':                  1.5,
# 		'diffuse_color':        (238, 233, 228),
# 		'sub_surface_color':    (238, 233, 228),
# 		'scatter_radius':       (235, 190, 160),
# 		'scatter_radius_mult':  1.0,
# 		'phase_function':       -0.25,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.7
# 	},
# 	'Ketchup': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (102, 28,  0),
# 		'sub_surface_color':    (102, 28,  0),
# 		'scatter_radius':       (176, 62, 50),
# 		'scatter_radius_mult':  1.0,
# 		'phase_function':       0.9,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.7
# 	},
# 	'Cream': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (224, 201, 117),
# 		'sub_surface_color':    (224, 201, 117),
# 		'scatter_radius':       (215, 153,  81),
# 		'scatter_radius_mult':  2.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.6
# 	},
# 	'Potato': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (224, 201, 117),
# 		'sub_surface_color':    (224, 201, 117),
# 		'scatter_radius':       (215, 153,  81),
# 		'scatter_radius_mult':  2.0,
# 		'phase_function':       0.8,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  0.8
# 	},
# 	'Spectration': {
# 		'ior':                  1.5,
# 		'diffuse_color':        (255, 255, 255),
# 		'sub_surface_color':    (255, 255, 255),
# 		'scatter_radius':       (  0,   0,   0),
# 		'scatter_radius_mult':  0.0,
# 		'phase_function':       0.0,
# 		'specular_amount':      0.0,
# 		'specular_glossiness':  0.0
# 	},
# 	'Water_clear': {
# 		'ior':                  1.3,
# 		'diffuse_color':        (  0,   0,   0),
# 		'sub_surface_color':    (  0,   0,   0),
# 		'scatter_radius':       (255, 255, 255),
# 		'scatter_radius_mult':  300.0,
# 		'phase_function':       0.95,
# 		'specular_amount':      1.0,
# 		'specular_glossiness':  1.0
# 	}
# }
# def generate_presets():
# 	for preset in SSS2:
# 		ofile= open("/home/bdancer/devel/vrayblender/exporter/vb25/presets/sss/%s.py"%(preset), 'w')
# 		ofile.write("import bpy\n")
# 		for param in SSS2[preset]:
# 			ps= SSS2[preset][param]
# 			if type(ps) == tuple:
# 				pss= ""
# 				for c in ps:
# 					pss+= "%.3f,"%(float(c / 255.0))
# 				ps= pss[:-1]
# 			s= "bpy.context.active_object.active_material.vray_material.BRDFSSS2Complex.%s = %s\n"%("%s"%(param), ps)
# 			ofile.write(s.replace(')','').replace('(',''))
# 		ofile.write("\n")
# 		ofile.close()
# generate_presets()



'''
  GUI
'''
narrowui= 200


def active_node_mat(mat):
    if mat:
        mat_node= mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat
    return None


def base_poll(cls, context):
	rd= context.scene.render
	return (context.material) and (rd.engine in cls.COMPAT_ENGINES)


class MATERIAL_MT_VRAY_presets(bpy.types.Menu):
	bl_label= "SSS Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "sss")
	preset_operator = "script.execute_preset"
	draw = bpy.types.Menu.draw_preset


class MaterialButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'material'


class MATERIAL_PT_VRAY_context_material(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = ""
	bl_show_header = False

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return context.object or base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		mat= active_node_mat(context.material)
		
		ob= context.object
		slot= context.material_slot
		space= context.space_data

		wide_ui= context.region.width > narrowui

		if ob:
			row = layout.row()
			row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
			col = row.column(align=True)
			col.operator("object.material_slot_add", icon='ZOOMIN', text="")
			col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")
			col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")
			if ob.mode == 'EDIT':
				row = layout.row(align=True)
				row.operator("object.material_slot_assign", text="Assign")
				row.operator("object.material_slot_select", text="Select")
				row.operator("object.material_slot_deselect", text="Deselect")

		if wide_ui:
			split = layout.split(percentage=0.65)

			if ob:
				split.template_ID(ob, "active_material", new="material.new")
				row = split.row()
				if slot:
					row.prop(slot, "link", text="")
				else:
					row.label()
			elif mat:
				split.template_ID(space, "pin_id")
				split.separator()
		else:
			if ob:
				layout.template_ID(ob, "active_material", new="material.new")
			elif mat:
				layout.template_ID(space, "pin_id")

		if mat:
			vray_material= mat.vray_material
			layout.prop(vray_material, 'type', expand=True)


class MATERIAL_PT_VRAY_preview(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Preview"
	bl_default_closed = False
	bl_show_header = True

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		self.layout.template_preview(context.material)


class MATERIAL_PT_VRAY_basic(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = 'Parameters'
	bl_default_closed = False
	bl_show_header = True

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		sce= context.scene
		ob= context.object

		mat= active_node_mat(context.material)
		vmat= mat.vray_material
				
		if vmat.type == 'MTL':
			vray_plugin= vmat.BRDFVRayMtl
			
			raym= mat.raytrace_mirror
			rayt= mat.raytrace_transparency

			row= layout.row()
			colL= row.column()
			colL.label(text="Diffuse")

			row= layout.row()
			colL= row.column()
			colR= row.column()
			colL.prop(mat, "diffuse_color", text="")

			colL.prop(mat, "roughness")
			colR.prop(mat, "alpha")

			row= layout.row()
			colL= row.column()
			colL.label(text="Reflection")

			row= layout.row()
			colL= row.column(align=True)
			colL.prop(vray_plugin, 'reflect_color', text="")
			if not vray_plugin.hilight_glossiness_lock:
				colL.prop(vray_plugin, 'hilight_glossiness', slider=True)
			colL.prop(raym, "gloss_factor", text="Reflection gloss")
			colL.prop(vray_plugin, 'reflect_subdivs', text="Subdivs")
			colL.prop(vray_plugin, 'reflect_depth', text="Depth")
			colR= row.column()
			colR.prop(vray_plugin, 'brdf_type', text="")
			colR.prop(vray_plugin, "hilight_glossiness_lock")

			if not vray_plugin.brdf_type == 'PHONG':
				colR.prop(vray_plugin, "anisotropy")
				colR.prop(vray_plugin, "anisotropy_rotation")
			colR.prop(vray_plugin, "fresnel")
			if vray_plugin.fresnel:
				colR.prop(vray_plugin, "fresnel_ior")

			split= layout.split()
			col= split.column()
			col.label(text="Refraction")
			if wide_ui:
				col= split.column()
			col.label(text="Fog")

			split= layout.split()
			col= split.column(align=True)
			col.prop(vray_plugin, "refract_color", text="")
			col.prop(rayt, "ior")
			col.prop(rayt, "gloss_factor", text="Glossiness")
			col.prop(vray_plugin, 'refract_subdivs', text="Subdivs")
			col.prop(vray_plugin, 'refract_depth', text="Depth")
			if wide_ui:
				col= split.column(align=True)
			col.prop(vray_plugin, "fog_color", text="")
			col.prop(vray_plugin, "fog_mult")
			col.prop(vray_plugin, "fog_bias")
			col.label(text="")
			col.prop(vray_plugin, "refract_affect_alpha")
			col.prop(vray_plugin, "refract_affect_shadows")

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(vray_plugin, 'translucency')
			if(vray_plugin.translucency != 'NONE'):
				split= layout.split()
				col= split.column()
				col.prop(vray_plugin, 'translucency_color', text="")
				col.prop(vray_plugin, 'translucency_thickness', text="Thickness")
				if wide_ui:
					col= split.column()
				col.prop(vray_plugin, 'translucency_scatter_coeff', text="Scatter coeff")
				col.prop(vray_plugin, 'translucency_scatter_dir', text="Fwd/Bck coeff")
				col.prop(vray_plugin, 'translucency_light_mult', text="Light multiplier")

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(vmat, "two_sided")
			if vmat.two_sided:
				if wide_ui:
					col= split.column()
				col.prop(vmat, "two_sided_translucency", slider=True, text="Translucency")

		elif vmat.type == 'EMIT':
			row= layout.row()
			colL= row.column()
			colL.label(text="Color")

			row= layout.row()
			col= row.column()
			col.prop(mat, "diffuse_color", text="")
			if wide_ui:
				col= row.column()
			col.prop(mat, "alpha")

			row= layout.row()
			colL= row.column()
			colL.label(text="Emitter")

			row= layout.row()
			col= row.column()
			col.prop(mat, "emitter", text="Type")
			if wide_ui:
				col= row.column()
			if not mat.emitter == 'MESH':
				col.prop(mat, "emit", text="Intensity")

			if(mat.emitter == 'MESH'):
				split= layout.split()
				col= split.column()
				col.prop(ob, 'lamp_portal_mode', text="Mode")
				if(ob.lamp_portal_mode == 'NORMAL'):
					col.prop(ob, 'lamp_units', text="Units")
					col.prop(ob, 'lamp_intensity', text="Intensity")
				col.prop(ob, 'lamp_subdivs')

				if wide_ui:
					col= split.column()
				col.prop(ob, 'lamp_invisible')
				col.prop(ob, 'lamp_affectDiffuse')
				col.prop(ob, 'lamp_affectSpecular')
				col.prop(ob, 'lamp_affectReflections')
				col.prop(ob, 'lamp_noDecay')

				col.prop(ob, 'lamp_doubleSided')
				col.prop(ob, 'lamp_storeWithIrradianceMap')
			else:
				row= layout.row()
				colL= row.column()
				colL.prop(mat, "emitOnBackSide")
				colL.prop(mat, "compensateExposure")

		elif vmat.type == 'SSS':
			vray_plugin= vmat.BRDFSSS2Complex
			
			row= layout.row()
			col= row.column()
			col.label(text='General')

			row= layout.row()
			col= row.column()
			col.menu("MATERIAL_MT_VRAY_presets", text="Presets")

			row= layout.row()
			colL= row.column()
			colR= row.column()

			colL.prop(vray_plugin, 'prepass_rate')
			colL.prop(vray_plugin, 'scale')
			colR.prop(vray_plugin, 'ior')
			colR.prop(vray_plugin, 'interpolation_accuracy', text='Accuracy')

			layout.separator()

			row= layout.row()
			col= row.column()
			col.label(text='Overall color')
			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'overall_color', text='')
			col= row.column()
			col.prop(vray_plugin, 'phase_function')

			row= layout.row()
			col= row.column()
			col.label(text='Diffuse color')
			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'diffuse_color', text='')
			col= row.column()
			col.prop(vray_plugin, 'diffuse_amount')

			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'sub_surface_color')
			col= row.column()
			col.label(text='')

			row= layout.row()
			col= row.column()
			col.label(text='Scatter color')
			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'scatter_radius', text='')
			col= row.column()
			col.prop(vray_plugin, 'scatter_radius_mult')

			layout.separator()

			row= layout.row()
			col= row.column()
			col.label(text='Specular layer')

			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'specular_color', text='')
			col.prop(vray_plugin, 'specular_subdivs', text='Subdivs')
			col= row.column()
			col.prop(vray_plugin, 'specular_amount', text='Amount')
			col.prop(vray_plugin, 'specular_glossiness', text='Glossiness')

			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'trace_reflections')
			if(vray_plugin.trace_reflections):
				col= row.column()
				col.prop(vray_plugin, 'reflection_depth')

			layout.separator()

			row= layout.row()
			col= row.column()
			col.label(text='Options:')
			row= layout.row()
			col= row.column()
			col.prop(vray_plugin, 'single_scatter', text='Type')
			col.prop(vray_plugin, 'subdivs')
			col.prop(vray_plugin, 'refraction_depth')
			col.prop(vray_plugin, 'cutoff_threshold')
			col= row.column()
			col.prop(vray_plugin, 'front_scatter')
			col.prop(vray_plugin, 'back_scatter')
			col.prop(vray_plugin, 'scatter_gi')
			col.prop(vray_plugin, 'prepass_blur')
		else:
			pass


class MATERIAL_PT_VRAY_options(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Options"
	bl_default_closed = True
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		ob= context.object

		mat= active_node_mat(context.material)
		vmat= mat.vray_material
		vray_plugin= vmat.BRDFVRayMtl

		layout= self.layout

		wide_ui= context.region.width > 200

		row= layout.row()
		col= row.column()
		col.prop(vray_plugin, "reflect_trace")
		col.prop(vray_plugin, "refract_trace")
		if(wide_ui):
			col= row.column()
		col.prop(vray_plugin, "option_double_sided")
		col.prop(vray_plugin, "option_reflect_on_back")
		col.prop(vray_plugin, 'option_use_irradiance_map')

		row= layout.row()
		col= row.column()
		col.prop(vray_plugin, 'option_glossy_rays_as_gi')
		col.prop(vray_plugin, 'option_energy_mode')

		row= layout.row()
		col= row.column()
		col.prop(vray_plugin, 'option_cutoff')
		if(wide_ui):
			col= row.column()
		col.prop(vray_plugin, 'environment_priority')


class MATERIAL_PT_VRAY_wrapper(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Wrapper"
	bl_default_closed = True
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		mat= active_node_mat(context.material)
		vmat= mat.vray_material
		self.layout.prop(vmat, "use_wrapper", text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object

		mat= active_node_mat(context.material)
		vmat= mat.vray_material
		vray_plugin= vmat.MtlWrapper
		
		layout= self.layout
		layout.active= vmat.use_wrapper

		split= layout.split()
		col= split.column()
		col.prop(vray_plugin, 'generate_gi')
		col.prop(vray_plugin, 'receive_gi')
		if(wide_ui):
			col= split.column()
		col.prop(vray_plugin, 'generate_caustics')
		col.prop(vray_plugin, 'receive_caustics')

		split= layout.split()
		col= split.column()
		col.prop(vray_plugin, 'gi_quality_multiplier')

		split= layout.split()
		col= split.column()
		col.label(text="Matte properties")

		split= layout.split()
		colL= split.column()
		colL.prop(vray_plugin, 'matte_surface')
		if wide_ui:
			colR= split.column()
		else:
			colR= colL
		colR.prop(vray_plugin, 'alpha_contribution')
		if vray_plugin.matte_surface:
			colR.prop(vray_plugin, 'reflection_amount')
			colR.prop(vray_plugin, 'refraction_amount')
			colR.prop(vray_plugin, 'gi_amount')
			colR.prop(vray_plugin, 'no_gi_on_other_mattes')

			colL.prop(vray_plugin, 'affect_alpha')
			colL.prop(vray_plugin, 'shadows')
			if(mat.shadows):
				colL.prop(vray_plugin, 'shadow_tint_color')
				colL.prop(vray_plugin, 'shadow_brightness')
			
		#col.prop(vray_plugin, 'alpha_contribution_tex')
		#col.prop(vray_plugin, 'shadow_brightness_tex')
		#col.prop(vray_plugin, 'reflection_filter_tex')

		split= layout.split()
		col= split.column()
		col.label(text="Miscellaneous")

		split= layout.split()
		col= split.column()
		col.prop(vray_plugin, 'gi_surface_id')
		col.prop(vray_plugin, 'trace_depth')
		if(wide_ui):
			col= split.column()
		col.prop(vray_plugin, 'matte_for_secondary_rays')


class MATERIAL_PT_VRAY_render(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Render"
	bl_default_closed = True
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		mat= active_node_mat(context.material)
		vray_plugin= mat.vray_material
		self.layout.prop(vray_plugin, "use_renderstats", text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		mat= active_node_mat(context.material)
		vmat= mat.vray_material
		rsmat= mat.vray_material.MtlRenderStats

		layout= self.layout
		layout.active= vmat.use_renderstats

		split= layout.split()
		col= split.column()
		col.prop(rsmat, 'visibility', text="Visible")

		split= layout.split()
		col= split.column()
		col.label(text="Visible to:")

		split= layout.split()
		sub= split.column()
		sub.active= rsmat.visibility
		sub.prop(rsmat, 'camera_visibility', text="Camera")
		sub.prop(rsmat, 'gi_visibility', text="GI")
		sub.prop(rsmat, 'shadows_visibility', text="Shadows")
		if wide_ui:
			sub= split.column()
			sub.active= rsmat.visibility
		sub.prop(rsmat, 'reflections_visibility', text="Reflections")
		sub.prop(rsmat, 'refractions_visibility', text="Refractions")

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


FloatProperty= bpy.types.Material.FloatProperty
IntProperty= bpy.types.Material.IntProperty
BoolProperty= bpy.types.Material.BoolProperty
EnumProperty= bpy.types.Material.EnumProperty
VectorProperty= bpy.types.Material.FloatVectorProperty



'''
  BRDFVRayMtl
'''
VectorProperty(
	attr="vray_fog_color",
	name="Fog color",
	description="Fog color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(1.0, 1.0, 1.0)
)

VectorProperty(
	attr="vray_refract_color",
	name="Refraction color",
	description="Refraction color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

VectorProperty(
	attr="vray_reflect_color",
	name="Reflection color",
	description="Reflection color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

BoolProperty(	attr="vray_fresnel",
				name="Frensnel reflections",
				description="Enable frensnel reflections.",
				default= False)

BoolProperty(	attr="vray_fresnel_ior_lock",
				name="Frensnel reflections lock",
				description="",
				default= True)

FloatProperty(  attr="vray_fresnel_ior",
				name="Fresnel IOR",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default= 1.6)

FloatProperty(  attr="vray_roughness",
				name="Roughness",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_hilightGlossiness",
				name="Hilight gloss",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 1.0)

BoolProperty(	attr="vray_hilightGlossiness_lock",
				name="Hilight glossiness lock",
				description="",
				default= True)

BoolProperty(	attr="vray_affect_shadows",
				name="Affect shadows",
				description="",
				default= False)

BoolProperty(	attr="vray_affect_alpha",
				name="Affect alpha",
				description="",
				default= False)

FloatProperty(  attr="vray_fog_color_mult",
				name="Fog multiplier",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 0.1)

FloatProperty(  attr="vray_fog_bias",
				name="Fog bias",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_fog_ior",
				name="Fog bias",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 1.0)

FloatProperty(  attr="vray_anisotropy",
				name="Anisotropy",
				description="",
				min=-1.0, max=1.0, soft_min=-1.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_anisotropy_rotation",
				name="Rotation",
				description="Anisotropy rotation",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 0.0)

EnumProperty(   attr="vray_brdf",
				name="BRDF",
				description="This determines the type of BRDF (the shape of the hilight).",
				items=(("PHONG", "Phong", "Phong hilight/reflections."),
					   ("BLINN", "Blinn", "Blinn hilight/reflections."),
					   ("WARD", "Ward",  "Ward hilight/reflections.")),
				default= "BLINN")


BoolProperty(
	attr="vray_trace_refractions",
	name="Trace refractions",
	description="",
	default= True
)

BoolProperty(
	attr="vray_trace_reflections",
	name="Trace reflections",
	description="",
	default= True
)

BoolProperty(
	attr="vray_back_side",
	name="Reflect on back side",
	description="",
	default= False
)

BoolProperty(
	attr="vray_double_sided",
	name="Double-sided",
	description="",
	default= True
)

# option_glossy_rays_as_gi: integer (Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always)
EnumProperty(
	attr= 'vb_mtl_glossy_rays_as_gi',
	name= 'Glossy rays as GI',
	description= "Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always",
	items=(("ALWAYS", "Always", ""),
		   ("GI",     "Only for GI rays",  ""),
		   ("NEVER",  "Never",  "")),
	default= 'GI'
)

# option_cutoff: float (Specifies a cutoff threshold for tracing reflections/refractions)
FloatProperty(
	attr= 'vb_mtl_cutoff',
	name= 'Cutoff',
	description= "Specifies a cutoff threshold for tracing reflections/refractions",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.001
)

# option_use_irradiance_map: bool (false to perform local brute-force GI calculatons and true to use the current GI engine)
BoolProperty(
	attr= 'vb_mtl_use_irradiance_map',
	name= 'Use irradiance map',
	description= "false to perform local brute-force GI calculatons and true to use the current GI engine",
	default= True
)

# option_energy_mode: integer (Energy preservation mode for reflections and refractions (0 - color, 1 - monochrome))
EnumProperty(
	attr= 'vb_mtl_energy_mode',
	name= 'Energy mode',
	description= "Energy preservation mode for reflections and refractions.",
	items=(("MONO",  "Monochrome", ""),
		   ("COLOR", "Color",      "")),
	default= 'COLOR'
)

# environment_override: acolor texture (Environment override texture)

# environment_priority: integer (Environment override priority (used when several materials override it along a ray path))
IntProperty(
	attr= 'vb_mtl_environment_priority',
	name= 'Environment priority',
	description= "Environment override priority (used when several materials override it along a ray path)",
	min= 0,
	max= 10,
	default= 0
)

# translucency: integer (Translucency mode (0 - none))
EnumProperty(
	attr= 'vray_translucency',
	name= 'Translucency',
	description= "Translucency mode",
	items=(("HYBRID", "Hybrid model", ""),
		   ("SOFT",   "Soft (water) model", ""),
		   ("HARD",   "Hard (wax) model", ""),
		   ("NONE",   "None",   "")),
	default= 'NONE'
)

# translucency_color: acolor texture (Filter color for the translucency effect) = AColor(1, 1, 1, 1)
VectorProperty(
	attr= 'vray_translucency_color',
	name= 'Translucency_color',
	description= "Filter color for the translucency effect.",
	subtype= "COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0, 0.0, 0.0)
)

# translucency_light_mult: float (A multiplier for the calculated lighting for the translucency effect)
FloatProperty(
	attr= 'vray_translucency_light_mult',
	name= 'Translucency light mult',
	description= "A multiplier for the calculated lighting for the translucency effect",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# translucency_scatter_dir: float (Scatter direction (0.0f is backward, 1.0f is forward))
FloatProperty(
	attr= 'vray_translucency_scatter_dir',
	name= 'Translucency scatter dir',
	description= "Scatter direction (0.0 is backward, 1.0 is forward)",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.5
)

# translucency_scatter_coeff: float (Scattering cone (0.0f - no scattering, 1.0f - full scattering)
FloatProperty(
	attr= 'vray_translucency_scatter_coeff',
	name= 'Translucency scatter coeff',
	description= "Scattering cone (0.0 - no scattering, 1.0 - full scattering",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

# translucency_thickness: float (Maximum distance to trace inside the object)
FloatProperty(
	attr= 'vray_translucency_thickness',
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
BoolProperty(
	attr= 'vb_mrs_camera_visibility',
	name= 'Camera visibility',
	description= "TODO.",
	default= True
)

# reflections_visibility: bool
BoolProperty(
	attr= 'vb_mrs_reflections_visibility',
	name= 'Reflections visibility',
	description= "TODO.",
	default= True
)

# refractions_visibility: bool
BoolProperty(
	attr= 'vb_mrs_refractions_visibility',
	name= 'Refractions visibility',
	description= "TODO.",
	default= True
)

# gi_visibility: bool
BoolProperty(
	attr= 'vb_mrs_gi_visibility',
	name= 'GI visibility',
	description= "TODO.",
	default= True
)

# shadows_visibility: bool
BoolProperty(
	attr= 'vb_mrs_shadows_visibility',
	name= 'Shadows visibility',
	description= "TODO.",
	default= True
)

# visibility: float (Overall visibility)
BoolProperty(
	attr= 'vb_mrs_visibility',
	name= 'Overall visibility',
	description= "TODO.",
	default= True
)



'''
  Plugin: BRDFLight
'''
BoolProperty( 
	attr= "vray_mtl_emitOnBackSide", 
	name= "Emit on back side", 
	description= 'TODO.', 
	default= False
)


BoolProperty( 
	attr= "vray_mtl_compensateExposure", 
	name= "Compensate camera exposure", 
	description= 'TODO.', 
	default= False
)



'''
  Plugin: BRDFSSS2Complex
'''
IntProperty( 
	attr= "vray_fsss_prepass_rate",
	name= "Prepass rate", 
	description= "Sampling density for the illumination map.", 
	min= -10, 
	max=  10, 
	default= -1
)

FloatProperty(
	attr= "vray_fsss_interpolation_accuracy", 
	name= "Interpolation accuracy", 
	description= "Interpolation accuracy for the illumination map; normally 1.0 is fine.", 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

FloatProperty(
	attr= "vray_fsss_scale", 
	name= "Scale", 
	description= "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smalle.", 
	min= 0.0, 
	max= 1000.0, 
	soft_min= 0.0, 
	soft_max= 1000.0, 
	precision= 4, 
	default= 1
)

FloatProperty(
	attr= "vray_fsss_ior", 
	name= "IOR", 
	description= 'TODO.', 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.5
)

FloatProperty(
	attr= "vray_fsss_diffuse_amount", 
	name= "Diffuse amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 0.0
)

FloatProperty(
	attr= "vray_fsss_scatter_radius_mult", 
	name= "Scatter radius", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

VectorProperty( 
	attr= "vray_fsss_overall_color", 
	name= "Overall color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1.0, 1.0, 1.0)
)

VectorProperty( 
	attr= "vray_fsss_diffuse_color", 
	name= "Diffuse color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

VectorProperty( 
	attr= "vray_fsss_sub_surface_color", 
	name= "Sub surface color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

VectorProperty( 
	attr= "vray_fsss_scatter_radius", 
	name= "Scatter radius", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.92, 0.52, 0.175)
)

FloatProperty(
	attr= "vray_fsss_phase_function", 
	name= "Phase function", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0
)

VectorProperty( 
	attr= "vray_fsss_specular_color", 
	name= "Specular color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1.0, 1.0, 1.0)
)

IntProperty( 
	attr= "vray_fsss_specular_subdivs", 
	name= "Specular subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

FloatProperty(
	attr= "vray_fsss_specular_amount", 
	name= "Specular amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 1
)

FloatProperty(
	attr= "vray_fsss_specular_glossiness", 
	name= "Specular glossiness", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.6
)

FloatProperty(
	attr= "vray_fsss_cutoff_threshold", 
	name= "Cutoff threshold", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.01
)

BoolProperty( 
	attr= "vray_fsss_trace_reflections", 
	name= "Trace reflections", 
	description= 'TODO.', 
	default= False
)

IntProperty( 
	attr= "vray_fsss_reflection_depth", 
	name= "Reflection depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

EnumProperty(
	attr="vray_fsss_single_scatter",
	name="Single scatter",
	description= 'TODO.', 
	items=(("NONE",   "None", ""),
		   ("SIMPLE", "Simple", ""),
		   ("SOLID",  "Raytraced (solid)", ""),
		   ("REFR",   "Raytraced (refractive)",  "")),
	default= "SIMPLE"
)

IntProperty( 
	attr= "vray_fsss_subdivs", 
	name= "Subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

IntProperty( 
	attr= "vray_fsss_refraction_depth", 
	name= "Refraction depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

BoolProperty( 
	attr= "vray_fsss_front_scatter", 
	name= "Front scatter", 
	description= 'TODO.', 
	default= True
)

BoolProperty( 
	attr= "vray_fsss_back_scatter", 
	name= "Back scatter", 
	description= 'TODO.', 
	default= True
)

BoolProperty( 
	attr= "vray_fsss_scatter_gi", 
	name= "Scatter gi", 
	description= 'TODO.', 
	default= False
)

FloatProperty(
	attr= "vray_fsss_prepass_blur", 
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
  Material
'''
EnumProperty(
	attr='vray_mtl_emitter',
	name='Emitter type',
	description='This determines the type of BRDF (the shape of the hilight).',
	items=(('MTL',  'Material',   ''),
		   ('MESH', 'Mesh light',  '')),
	default= 'MTL'
)

EnumProperty(
	attr= 'vray_mtl_type',
	name= 'Type',
	description= 'Material type.',
	items=(
		('MTL',  'Basic', 'Basic V-Ray material.'),
		('SSS',  'SSS',   'Fast SSS material.'),
		('EMIT', 'Light', 'Light emitting material.')
	),
	default= 'MTL'
)

BoolProperty(
	attr='vray_mtl_two_sided',
	name='Two sided material',
	description='Simple \'Two sided\' material. Use nodes for advanced control.',
	default= False
)

FloatProperty(
	attr= 'vray_mtlts_translucency',
	name= 'Translucency',
	description= 'Translucency between front and back.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.5
)

BoolProperty(
	attr='vray_mtl_use_wrapper',
	name='Use material wrapper',
	description='Use material wrapper options.',
	default= False
)


'''
  Plugin: MtlWrapper
'''
# base_material: plugin (The base material)
# generate_gi: float (Controls the GI generated by the material.)
FloatProperty(
	attr= 'vb_mwrap_generate_gi',
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
FloatProperty(
	attr= 'vb_mwrap_receive_gi',
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
FloatProperty(
	attr= 'vb_mwrap_generate_caustics',
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
FloatProperty(
	attr= 'vb_mwrap_receive_caustics',
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
FloatProperty(
	attr= 'vb_mwrap_alpha_contribution',
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
BoolProperty(
	attr= 'vb_mwrap_matte_surface',
	name= 'Matte surface',
	description= "Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.",
	default= False
)

# shadows: bool (Turn this on to make shadow visible on the matter surface.)
BoolProperty(
	attr= 'vb_mwrap_shadows',
	name= 'Shadows',
	description= "Turn this on to make shadow visible on the matter surface.",
	default= False
)

# affect_alpha: bool (Turn this on to make shadows affect the alpha contribution of the matte surface.)
BoolProperty(
	attr= 'vb_mwrap_affect_alpha',
	name= 'Affect alpha',
	description= "Turn this on to make shadows affect the alpha contribution of the matte surface.",
	default= False
)

# shadow_tint_color: color (Tint for the shadows on the matte surface.) = Color(0, 0, 0)
VectorProperty( 
	attr= "vb_mwrap_shadow_tint_color", 
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
FloatProperty(
	attr= 'vb_mwrap_shadow_brightness',
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
FloatProperty(
	attr= 'vb_mwrap_reflection_amount',
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
FloatProperty(
	attr= 'vb_mwrap_refraction_amount',
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
FloatProperty(
	attr= 'vb_mwrap_gi_amount',
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
BoolProperty(
	attr= 'vb_mwrap_no_gi_on_other_mattes',
	name= 'No gi on other mattes',
	description= "This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.",
	default= True
)

# matte_for_secondary_rays: bool (Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc))
BoolProperty(
	attr= 'vb_mwrap_matte_for_sec_rays',
	name= 'Matte for secondary rays',
	description= "Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc)",
	default= False
)

# gi_surface_id: integer (If two objects have different GI surface ids, the light cache samples of the two objects will not be blended)
IntProperty(
	attr= 'vb_mwrap_gi_surface_id',
	name= 'GI surface id',
	description= "If two objects have different GI surface ids, the light cache samples of the two objects will not be blended",
	min= 0,
	max= 10,
	default= 0
)

# gi_quality_multiplier: float (A multiplier for GI quality)
FloatProperty(
	attr= 'vb_mwrap_gi_quality_multiplier',
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

# trace_depth: integer (The maximum reflection depth (-1 is controlled by the global options))
IntProperty(
	attr= 'vb_mwrap_trace_depth',
	name= 'Trace depth',
	description= "The maximum reflection depth (-1 is controlled by the global options)",
	min= -1,
	max= 1000,
	default= -1
)

# channels: plugin (Render channels the result of this BRDF will be written to), unlimited list



'''
  Presets
'''
SSS2= {
	'Skin_brown': {
		'ior':                  1.3,
		'diffuse_color':        (169, 123, 92),
		'sub_surface_color':    (169, 123, 92),
		'scatter_radius':       (155, 94, 66),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Skin_pink': {
		'ior':                  1.3,
		'diffuse_color':        (203, 169, 149),
		'sub_surface_color':    (203, 169, 149),
		'scatter_radius':       (177, 105, 84),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Skin_yellow': {
		'ior':                  1.3,
		'diffuse_color':        (204, 165, 133),
		'sub_surface_color':    (204, 165, 133),
		'scatter_radius':       (177, 105, 84),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Milk_skimmed': {
		'ior':                  1.3,
		'diffuse_color':        (230, 230, 210),
		'sub_surface_color':    (230, 230, 210),
		'scatter_radius':       (245, 184, 107),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Milk_whole': {
		'ior':                  1.3,
		'diffuse_color':        (242, 239, 222),
		'sub_surface_color':    (242, 239, 222),
		'scatter_radius':       (188, 146,  90),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.9,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Marble_white': {
		'ior':                  1.5,
		'diffuse_color':        (238, 233, 228),
		'sub_surface_color':    (238, 233, 228),
		'scatter_radius':       (235, 190, 160),
		'scatter_radius_mult':  1.0,
		'phase_function':       -0.25,
		'specular_amount':      1.0,
		'specular_glossiness':  0.7
	},
	'Ketchup': {
		'ior':                  1.3,
		'diffuse_color':        (102, 28,  0),
		'sub_surface_color':    (102, 28,  0),
		'scatter_radius':       (176, 62, 50),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.9,
		'specular_amount':      1.0,
		'specular_glossiness':  0.7
	},
	'Cream': {
		'ior':                  1.3,
		'diffuse_color':        (224, 201, 117),
		'sub_surface_color':    (224, 201, 117),
		'scatter_radius':       (215, 153,  81),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.6
	},
	'Potato': {
		'ior':                  1.3,
		'diffuse_color':        (224, 201, 117),
		'sub_surface_color':    (224, 201, 117),
		'scatter_radius':       (215, 153,  81),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Spectration': {
		'ior':                  1.5,
		'diffuse_color':        (255, 255, 255),
		'sub_surface_color':    (255, 255, 255),
		'scatter_radius':       (  0,   0,   0),
		'scatter_radius_mult':  0.0,
		'phase_function':       0.0,
		'specular_amount':      0.0,
		'specular_glossiness':  0.0
	},
	'Water_clear': {
		'ior':                  1.3,
		'diffuse_color':        (  0,   0,   0),
		'sub_surface_color':    (  0,   0,   0),
		'scatter_radius':       (255, 255, 255),
		'scatter_radius_mult':  300.0,
		'phase_function':       0.95,
		'specular_amount':      1.0,
		'specular_glossiness':  1.0
	}
}

# def generate_preset():
# 	for preset in SSS2:
# 		ofile= open("/home/bdancer/devel/vrayblender/exporter/2.5/presets/sss/%s.py"%(preset), 'w')
# 		for param in SSS2[preset]:
# 			ps= SSS2[preset][param]
# 			if type(ps) == tuple:
# 				pss= ""
# 				for c in ps:
# 					pss+= "%.3f,"%(float(c / 255.0))
# 				ps= pss[:-1]
# 			s= "bpy.context.active_object.active_material.%s = %s\n"%("vray_fsss_%s"%(param), ps)
# 			ofile.write(s.replace(')','').replace('(',''))
# 		ofile.write('\n')
# 		ofile.close()
# generate_preset()



'''
  GUI
'''


narrowui= bpy.context.user_preferences.view.properties_width_check


def active_node_mat(mat):
    if mat:
        mat_node= mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat
    return None


class MATERIAL_MT_fsss_presets(bpy.types.Menu):
	bl_label= "SSS Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "sss")
	preset_operator = "script.execute_preset"
	draw = bpy.types.Menu.draw_preset


class MaterialButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'material'

	def poll(self, context):
		engine = context.scene.render.engine
		return (context.material) and (engine in self.COMPAT_ENGINES)


class MATERIAL_PT_vray_context_material(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = ""
	bl_show_header = False

	COMPAT_ENGINES = {'VRAY_RENDER'}

	def poll(self, context):
		engine = context.scene.render.engine
		return (context.material or context.object) and (engine in self.COMPAT_ENGINES)

	def draw(self, context):
		layout = self.layout

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
			layout.prop(mat, "vray_mtl_type", expand=True)


class MATERIAL_PT_vray_preview(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Preview"
	bl_default_closed = False
	bl_show_header = False

	COMPAT_ENGINES= set(['VRAY_RENDER'])

	def draw(self, context):
		self.layout.template_preview(context.material)


class MATERIAL_PT_vray_basic(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = 'Parameters'
	bl_default_closed = False
	bl_show_header = True

	COMPAT_ENGINES= set(['VRAY_RENDER'])

	def draw(self, context):
		layout= self.layout

		ob= context.object
		mat= active_node_mat(context.material)
		sce= context.scene
		wide_ui= context.region.width > narrowui

		if(mat.vray_mtl_type == 'MTL'):
			raym= mat.raytrace_mirror
			rayt= mat.raytrace_transparency

			row= layout.row()
			colL= row.column()
			colL.label(text="Diffuse")

			row= layout.row()
			colL= row.column()
			colR= row.column()
			colL.prop(mat, "diffuse_color", text="")

			colL.prop(mat, "vray_roughness")
			colR.prop(mat, "alpha")

			row= layout.row()
			colL= row.column()
			colL.label(text="Reflection")

			row= layout.row()
			colL= row.column(align=True)
			colL.prop(mat, "vray_reflect_color", text="")
			if(not mat.vray_hilightGlossiness_lock):
				colL.prop(mat, "vray_hilightGlossiness", slider=True)
			colL.prop(raym, "gloss_factor", text="Reflection gloss")
			colL.prop(raym, "gloss_samples", text="Subdivs")
			colL.prop(raym, "depth")
			colL.prop(raym, "gloss_threshold", text="Cutoff", slider=False)
			colR= row.column()
			colR.prop(mat, "vray_brdf", text="")
			colR.prop(mat, "vray_hilightGlossiness_lock")

			if(not mat.vray_brdf == 'PHONG'):
				colR.prop(mat, "vray_anisotropy")
				colR.prop(mat, "vray_anisotropy_rotation")
			colR.prop(mat, "vray_fresnel")
			if mat.vray_fresnel:
				colR.prop(mat, "vray_fresnel_ior")

			row= layout.row()
			colL= row.column()
			colL.label(text="Refraction")
			colR= row.column()
			colR.label(text="Fog")

			row= layout.row()
			colL= row.column(align=True)
			colL.prop(mat, "vray_refract_color", text="")
			colL.prop(rayt, "ior")
			colL.prop(rayt, "gloss_factor", text="Glossiness")
			colL.prop(rayt, "gloss_samples", text="Subdivs")
			colL.prop(rayt, "depth")
			colL.prop(rayt, "gloss_threshold", text="Cutoff", slider=False)

			colR= row.column(align=True)
			colR.prop(mat, "vray_fog_color", text="")
			colR.prop(mat, "vray_fog_color_mult")
			colR.prop(mat, "vray_fog_bias")
			colR.label(text="")
			colR.prop(mat, "vray_affect_alpha")
			colR.prop(mat, "vray_affect_shadows")

			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_translucency')
			if(mat.vray_translucency != 'NONE'):
				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_translucency_color', text="")
				col.prop(mat, 'vray_translucency_thickness', text="Thickness")
				if(wide_ui):
					col= row.column()
				col.prop(mat, 'vray_translucency_scatter_coeff', text="Scatter coeff")
				col.prop(mat, 'vray_translucency_scatter_dir', text="Fwd/Bck coeff")
				col.prop(mat, 'vray_translucency_light_mult', text="Light multiplier")

			row= layout.row()
			colL= row.column()
			colR= row.column()
			colL.prop(mat, "vray_mtl_two_sided")
			if(mat.vray_mtl_two_sided):
				colR.prop(mat, "vray_mtlts_translucency", slider=True)

		elif(mat.vray_mtl_type == 'EMIT'):
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
			col.prop(mat, "vray_mtl_emitter", text="Type")
			if wide_ui:
				col= row.column()
			if not mat.vray_mtl_emitter == 'MESH':
				col.prop(mat, "emit", text="Intensity")

			if(mat.vray_mtl_emitter == 'MESH'):
				split= layout.split()
				col= split.column()
				col.prop(ob, 'vray_lamp_portal_mode', text="Mode")
				if(ob.vray_lamp_portal_mode == 'NORMAL'):
					col.prop(ob, 'vray_lamp_units', text="Units")
					col.prop(ob, 'vray_lamp_intensity', text="Intensity")
				col.prop(ob, 'vray_lamp_subdivs')

				if wide_ui:
					col= split.column()
				col.prop(ob, 'vray_lamp_invisible')
				col.prop(ob, 'vray_lamp_affectDiffuse')
				col.prop(ob, 'vray_lamp_affectSpecular')
				col.prop(ob, 'vray_lamp_affectReflections')
				col.prop(ob, 'vray_lamp_noDecay')

				col.prop(ob, 'vray_lamp_doubleSided')
				col.prop(ob, 'vray_lamp_storeWithIrradianceMap')

				ob.vray_node_meshlight= True
			else:
				ob.vray_node_meshlight= False
				
				row= layout.row()
				colL= row.column()
				colL.prop(mat, "vray_mtl_emitOnBackSide")
				colL.prop(mat, "vray_mtl_compensateExposure")

		else: # SSS
			row= layout.row()
			col= row.column()
			col.label(text='General')

			row= layout.row()
			col= row.column()
			col.menu("MATERIAL_MT_fsss_presets", text="Presets")

			row= layout.row()
			colL= row.column()
			colR= row.column()

			colL.prop(mat, 'vray_fsss_prepass_rate')
			colL.prop(mat, 'vray_fsss_scale')
			colR.prop(mat, 'vray_fsss_ior')
			colR.prop(mat, 'vray_fsss_interpolation_accuracy', text='Accuracy')

			row= layout.row()
			col= row.column()
			col.label(text='')

			row= layout.row()
			col= row.column()
			col.label(text='Overall color')
			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_overall_color', text='')
			col= row.column()
			col.prop(mat, 'vray_fsss_phase_function')

			row= layout.row()
			col= row.column()
			col.label(text='Diffuse color')
			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_diffuse_color', text='')
			col= row.column()
			col.prop(mat, 'vray_fsss_diffuse_amount')

			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_sub_surface_color')
			col= row.column()
			col.label(text='')

			row= layout.row()
			col= row.column()
			col.label(text='Scatter color')
			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_scatter_radius', text='')
			col= row.column()
			col.prop(mat, 'vray_fsss_scatter_radius_mult')

			row= layout.row()
			col= row.column()
			col.label(text='')

			row= layout.row()
			col= row.column()
			col.label(text='Specular layer')

			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_specular_color', text='')
			col.prop(mat, 'vray_fsss_specular_subdivs', text='Subdivs')
			col= row.column()
			col.prop(mat, 'vray_fsss_specular_amount', text='Amount')
			col.prop(mat, 'vray_fsss_specular_glossiness', text='Glossiness')

			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_trace_reflections')
			if(mat.vray_fsss_trace_reflections):
				col= row.column()
				col.prop(mat, 'vray_fsss_reflection_depth')

			row= layout.row()
			col= row.column()
			col.label(text='')

			row= layout.row()
			col= row.column()
			col.label(text='Options')
			row= layout.row()
			col= row.column()
			col.prop(mat, 'vray_fsss_single_scatter', text='Type')
			col.prop(mat, 'vray_fsss_subdivs')
			col.prop(mat, 'vray_fsss_refraction_depth')
			col.prop(mat, 'vray_fsss_cutoff_threshold')
			col= row.column()
			col.prop(mat, 'vray_fsss_front_scatter')
			col.prop(mat, 'vray_fsss_back_scatter')
			col.prop(mat, 'vray_fsss_scatter_gi')
			col.prop(mat, 'vray_fsss_prepass_blur')


class MATERIAL_PT_vray_wrapper(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Wrapper"
	bl_default_closed = True
	
	COMPAT_ENGINES = set(['VRAY_RENDER'])

	def draw_header(self, context):
		mat= active_node_mat(context.material)
		self.layout.prop(mat, "vray_mtl_use_wrapper", text="")

	def draw(self, context):
		ob= context.object
		mat= active_node_mat(context.material)

		layout= self.layout
		layout.active= mat.vray_mtl_use_wrapper

		wide_ui= context.region.width > 200

		split= layout.split()
		col= split.column()
		col.prop(mat, 'vb_mwrap_generate_gi')
		col.prop(mat, 'vb_mwrap_receive_gi')
		if(wide_ui):
			col= split.column()
		col.prop(mat, 'vb_mwrap_generate_caustics')
		col.prop(mat, 'vb_mwrap_receive_caustics')

		split= layout.split()
		col= split.column()
		col.prop(mat, 'vb_mwrap_gi_quality_multiplier')

		split= layout.split()
		col= split.column()
		col.label(text="Matte properties")

		split= layout.split()
		colL= split.column()
		colL.prop(mat, 'vb_mwrap_matte_surface')
		if(wide_ui):
			colR= split.column()
		else:
			colR= colL
		colR.prop(mat, 'vb_mwrap_alpha_contribution')
		if(mat.vb_mwrap_matte_surface):
			colR.prop(mat, 'vb_mwrap_reflection_amount')
			colR.prop(mat, 'vb_mwrap_refraction_amount')
			colR.prop(mat, 'vb_mwrap_gi_amount')
			colR.prop(mat, 'vb_mwrap_no_gi_on_other_mattes')

			colL.prop(mat, 'vb_mwrap_affect_alpha')
			colL.prop(mat, 'vb_mwrap_shadows')
			if(mat.vb_mwrap_shadows):
				colL.prop(mat, 'vb_mwrap_shadow_tint_color')
				colL.prop(mat, 'vb_mwrap_shadow_brightness')
			
		#col.prop(mat, 'vb_mwrap_alpha_contribution_tex')
		#col.prop(mat, 'vb_mwrap_shadow_brightness_tex')
		#col.prop(mat, 'vb_mwrap_reflection_filter_tex')

		split= layout.split()
		col= split.column()
		col.label(text="Miscellaneous")

		split= layout.split()
		col= split.column()
		col.prop(mat, 'vb_mwrap_gi_surface_id')
		col.prop(mat, 'vb_mwrap_trace_depth')
		if(wide_ui):
			col= split.column()
		col.prop(mat, 'vb_mwrap_matte_for_sec_rays')


class MATERIAL_PT_vray_options(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Options"
	bl_default_closed = True
	
	COMPAT_ENGINES = set(['VRAY_RENDER'])

	def draw(self, context):
		ob= context.object
		mat= active_node_mat(context.material)

		layout= self.layout

		wide_ui= context.region.width > 200

		row= layout.row()
		col= row.column()
		col.prop(mat, "vray_trace_reflections")
		col.prop(mat, "vray_trace_refractions")
		if(wide_ui):
			col= row.column()
		col.prop(mat, "vray_double_sided")
		col.prop(mat, "vray_back_side")
		col.prop(mat, 'vb_mtl_use_irradiance_map')

		row= layout.row()
		col= row.column()
		col.prop(mat, 'vb_mtl_glossy_rays_as_gi')
		col.prop(mat, 'vb_mtl_energy_mode')

		row= layout.row()
		col= row.column()
		col.prop(mat, 'vb_mtl_cutoff')
		if(wide_ui):
			col= row.column()
		col.prop(mat, 'vb_mtl_environment_priority')


class MATERIAL_PT_vray_render(MaterialButtonsPanel, bpy.types.Panel):
	bl_label = "Render"
	bl_default_closed = True
	
	COMPAT_ENGINES = set(['VRAY_RENDER'])

	def draw(self, context):
		ob= context.object
		mat= active_node_mat(context.material)

		layout= self.layout

		wide_ui= context.region.width > 200

		split= layout.split()
		col= split.column()
		col.prop(mat, 'vb_mrs_visibility', text="Visible")

		split= layout.split()
		col= split.column()
		col.label(text="Visible to:")

		split= layout.split()
		sub= split.column()
		sub.active= mat.vb_mrs_visibility
		sub.prop(mat, 'vb_mrs_camera_visibility', text="Camera")
		sub.prop(mat, 'vb_mrs_gi_visibility', text="GI")
		sub.prop(mat, 'vb_mrs_shadows_visibility', text="Shadows")
		if(wide_ui):
			sub= split.column()
			sub.active= mat.vb_mrs_visibility
		sub.prop(mat, 'vb_mrs_reflections_visibility', text="Reflections")
		sub.prop(mat, 'vb_mrs_refractions_visibility', text="Refractions")



# bpy.types.register(MATERIAL_MT_fsss_presets)
# bpy.types.register(MATERIAL_PT_vray_context_material)
# bpy.types.register(MATERIAL_PT_vray_preview)
# bpy.types.register(MATERIAL_PT_vray_basic)
# bpy.types.register(MATERIAL_PT_vray_options)
# bpy.types.register(MATERIAL_PT_vray_wrapper)
# bpy.types.register(MATERIAL_PT_vray_render)

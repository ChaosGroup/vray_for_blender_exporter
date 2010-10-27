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


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class VRayMaterial(bpy.types.IDPropertyGroup):
    pass

bpy.types.Material.vray= PointerProperty(
	name= "V-Ray Material Settings",
	type=  VRayMaterial,
	description= "V-Ray material settings"
)


VRayMaterial.type= EnumProperty(
	name= "Type",
	description= "Material type.",
	items= (
		('MTL',"Standard","Standard V-Ray material."),
		('SSS',"SSS","Fast SSS material."),
		('EMIT',"Light","Light emitting material."),
		('VOL',"Volume","Volumetric material.")
	),
	default= 'MTL'
)

VRayMaterial.emitter_type= EnumProperty(
	name= "Emitter type",
	description= "This determines the type of BRDF (the shape of the hilight).",
	items= (
		('MTL',"Material",""),
		('MESH',"Mesh light","")
	),
	default= 'MTL'
)

VRayMaterial.two_sided= BoolProperty(
	name= "Two sided material",
	description= "Simple \"Two sided\" material. Use nodes for advanced control.",
	default= False
)

VRayMaterial.two_sided_translucency= FloatProperty(
	name= "Two sided translucency",
	description= "Translucency between front and back.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.5
)


'''
  BRDFVRayMtl
'''
class BRDFVRayMtl(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.BRDFVRayMtl= PointerProperty(
	name= "BRDFVRayMtl",
	type=  BRDFVRayMtl,
	description= "V-Ray BRDFVRayMtl settings"
)

BRDFVRayMtl.fog_color= FloatVectorProperty(
	name= "Fog color",
	description= "Fog color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

BRDFVRayMtl.refract_color= FloatVectorProperty(
	name= "Refraction color",
	description= "Refraction color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

BRDFVRayMtl.reflect_color= FloatVectorProperty(
	name= "Reflection color",
	description= "Reflection color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

BRDFVRayMtl.reflect_exit_color= FloatVectorProperty(
	name= "Reflection exit color",
	description= "Reflection exit color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

BRDFVRayMtl.fresnel= BoolProperty(
	name= "Frensnel reflections",
	description= "Enable frensnel reflections.",
	default= False
)

BRDFVRayMtl.fresnel_ior_lock= BoolProperty(
	name= "Frensnel reflections lock",
	description= "",
	default= False
)

BRDFVRayMtl.fresnel_ior= FloatProperty(
	name= "Fresnel IOR",
	description= "",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.6
)

BRDFVRayMtl.refract_ior= FloatProperty(
	name= "Refractions IOR",
	description= "The IOR for refractions.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.6
)

BRDFVRayMtl.reflect_subdivs= IntProperty(
	name= "Reflection subdivs",
	description= "Subdivs for glossy reflections",
	min= 1,
	max= 256,
	default= 8
)

BRDFVRayMtl.reflect_depth= IntProperty(
	name= "Reflections depth",
	description= "The maximum depth for reflections.",
	min= 1,
	max= 256,
	default= 5
)

BRDFVRayMtl.refract_depth= IntProperty(
	name= "Refractions depth",
	description= "The maximum depth for refractions.",
	min= 1,
	max= 256,
	default= 5
)

BRDFVRayMtl.refract_subdivs= IntProperty(
	name= "Refraction subdivs",
	description= "Subdivs for glossy refractions",
	min= 1,
	max= 256,
	default= 8
)

BRDFVRayMtl.roughness= FloatProperty(
	name= "Roughness",
	description= "",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.0
)

BRDFVRayMtl.hilight_glossiness= FloatProperty(
	name= "Hilight glossiness",
	description= "The glossiness of the hilights.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

BRDFVRayMtl.reflect_glossiness= FloatProperty(
	name= "Reflection glossiness",
	description= "The glossiness of the reflections.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

BRDFVRayMtl.refract_glossiness= FloatProperty(
	name= "Refraction glossiness",
	description= "The glossiness of the refractions.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

BRDFVRayMtl.hilight_glossiness_lock= BoolProperty(
	name= "Hilight glossiness lock",
	description= "",
	default= True
)

BRDFVRayMtl.hilight_soften= FloatProperty(
	name= "Hilight soften",
	description= "How much to soften hilights and reflections at grazing light angles",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.0
)

BRDFVRayMtl.reflect_dim_distance_on= BoolProperty(
	name= "reflect dim distance on",
	description= "True to enable dim distance",
	default= False
)

BRDFVRayMtl.reflect_dim_distance_falloff= FloatProperty(
	name= "reflect dim distance falloff",
	description= "Fall off for the dim distance",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0
)

BRDFVRayMtl.anisotropy_derivation= IntProperty(
	name= "anisotropy derivation",
	description= "What method to use for deriving anisotropy axes (0 - local object axis; 1 - a specified uvw generator)",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 0
)

BRDFVRayMtl.anisotropy_axis= IntProperty(
	name= "anisotropy axis",
	description= "Which local object axis to use when anisotropy_derivation is 0",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 2
)

BRDFVRayMtl.refract_affect_shadows= BoolProperty(
	name= "Affect shadows",
	description= "",
	default= False
)

BRDFVRayMtl.refract_affect_alpha= BoolProperty(
	name= "Affect alpha",
	description= "",
	default= False
)

BRDFVRayMtl.fog_mult= FloatProperty(
	name= "Fog multiplier",
	description= "",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 4,
	default= 0.001
)

BRDFVRayMtl.fog_unit_scale_on= BoolProperty(
	name= "Fog unit scale",
	description= "Enable unit scale multiplication, when calculating absorption",
	default= True
)

BRDFVRayMtl.fog_bias= FloatProperty(
	name= "Fog bias",
	description= "",
	min= -100.0,
	max= 100.0,
	soft_min= -1.0,
	soft_max= 1.0,
	precision= 4,
	default= 0.0
)

BRDFVRayMtl.fog_ior= FloatProperty(
	name= "Fog bias",
	description= "",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

BRDFVRayMtl.anisotropy= FloatProperty(
	name= "Anisotropy",
	description= "",
	min= -1.0,
	max= 1.0,
	soft_min= -1.0,
	soft_max= 1.0,
	default= 0.0
)

BRDFVRayMtl.anisotropy_rotation= FloatProperty(
	name= "Rotation",
	description= "Anisotropy rotation",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.0
)

BRDFVRayMtl.brdf_type= EnumProperty(
	name= "BRDF type",
	description= "This determines the type of BRDF (the shape of the hilight).",
	items= (
		('PHONG',"Phong","Phong hilight/reflections."),
		('BLINN',"Blinn","Blinn hilight/reflections."),
		('WARD',"Ward","Ward hilight/reflections.")
	),
	default= 'BLINN'
)

BRDFVRayMtl.refract_trace= BoolProperty(
	name= "Trace refractions",
	description= "",
	default= True
)

BRDFVRayMtl.refract_exit_color= FloatVectorProperty(
	name= "refract exit color",
	description= "The color to use when maximum depth is reached when refract_exit_color_on is true",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0,0,0)
)

BRDFVRayMtl.refract_exit_color_on= BoolProperty(
	name= "refract exit color on",
	description= "If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray",
	default= False
)

BRDFVRayMtl.reflect_trace= BoolProperty(
	name= "Trace reflections",
	description= 'TODO.',
	default= True
)

BRDFVRayMtl.option_reflect_on_back= BoolProperty(
	name= "Reflect on back side",
	description= "",
	default= False
)

BRDFVRayMtl.option_double_sided= BoolProperty(
	name= "Double-sided",
	description= "",
	default= True
)

BRDFVRayMtl.option_glossy_rays_as_gi= EnumProperty(
	name= "Glossy rays as GI",
	description= "Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always",
	items= (
		('ALWAYS',"Always",""),
		('GI',"Only for GI rays",""),
		('NEVER',"Never","")
	),
	default= 'GI'
)

BRDFVRayMtl.option_cutoff= FloatProperty(
	name= "Cutoff",
	description= "Specifies a cutoff threshold for tracing reflections/refractions",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.001
)

BRDFVRayMtl.option_use_irradiance_map= BoolProperty(
	name= "Use irradiance map",
	description= "false to perform local brute-force GI calculatons and true to use the current GI engine",
	default= True
)

BRDFVRayMtl.option_energy_mode= EnumProperty(
	name= "Energy mode",
	description= "Energy preservation mode for reflections and refractions.",
	items= (
		('MONO',"Monochrome",""),
		('COLOR',"Color","")
	),
	default= 'COLOR'
)

BRDFVRayMtl.environment_priority= IntProperty(
	name= "Environment priority",
	description= "Environment override priority (used when several materials override it along a ray path)",
	min= 0,
	max= 10,
	default= 0
)

BRDFVRayMtl.translucency= EnumProperty(
	name= "Translucency",
	description= "Translucency mode",
	items= (
		('HYBRID',"Hybrid model",""),
		('SOFT',"Soft (water) model",""),
		('HARD',"Hard (wax) model",""),
		('NONE',"None","")
	),
	default= 'NONE'
)

BRDFVRayMtl.translucency_color= FloatVectorProperty(
	name= "Translucency_color",
	description= "Filter color for the translucency effect.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

BRDFVRayMtl.translucency_light_mult= FloatProperty(
	name= "Translucency light mult",
	description= "A multiplier for the calculated lighting for the translucency effect",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

BRDFVRayMtl.translucency_scatter_dir= FloatProperty(
	name= "Translucency scatter dir",
	description= "Scatter direction (0.0 is backward, 1.0 is forward)",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.5
)

BRDFVRayMtl.translucency_scatter_coeff= FloatProperty(
	name= "Translucency scatter coeff",
	description= "Scattering cone (0.0 - no scattering, 1.0 - full scattering",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)



'''
  Plugin: MtlRenderStats
'''
class MtlRenderStats(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.MtlRenderStats= PointerProperty(
	name= "MtlRenderStats",
	type=  MtlRenderStats,
	description= "V-Ray MtlRenderStats settings"
)

MtlRenderStats.use= BoolProperty(
	name= "Use material render options",
	description= "Use material render options.",
	default= False
)

MtlRenderStats.camera_visibility= BoolProperty(
	name= "Camera visibility",
	description= "TODO.",
	default= True
)

MtlRenderStats.reflections_visibility= BoolProperty(
	name= "Reflections visibility",
	description= "TODO.",
	default= True
)

MtlRenderStats.refractions_visibility= BoolProperty(
	name= "Refractions visibility",
	description= "TODO.",
	default= True
)

MtlRenderStats.gi_visibility= BoolProperty(
	name= "GI visibility",
	description= "TODO.",
	default= True
)

MtlRenderStats.shadows_visibility= BoolProperty(
	name= "Shadows visibility",
	description= "TODO.",
	default= True
)

MtlRenderStats.visibility= BoolProperty(
	name= "Overall visibility",
	description= "TODO.",
	default= True
)


'''
  Plugin: BRDFLight
'''
class BRDFLight(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.BRDFLight= PointerProperty(
	name= "BRDFLight",
	type=  BRDFLight,
	description= "V-Ray BRDFLight settings"
)

BRDFLight.doubleSided= BoolProperty(
	name= "Double-sided",
	description= "If false, the light color is black for back-facing surfaces.",
	default= False
)

BRDFLight.emitOnBackSide= BoolProperty(
	name= "Emit on back side",
	description= 'TODO.',
	default= False
)

BRDFLight.compensateExposure= BoolProperty(
	name= "Compensate camera exposure",
	description= 'TODO.',
	default= False
)


'''
  Plugin: BRDFSSS2Complex
'''
class BRDFSSS2Complex(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.BRDFSSS2Complex= PointerProperty(
	name= "BRDFSSS2Complex",
	type=  BRDFSSS2Complex,
	description= "V-Ray BRDFSSS2Complex settings"
)

BRDFSSS2Complex.prepass_rate= IntProperty(
	name= "Prepass rate",
	description= "Sampling density for the illumination map.",
	min= -10,
	max= 10,
	default= -1
)

BRDFSSS2Complex.interpolation_accuracy= FloatProperty(
	name= "Interpolation accuracy",
	description= "Interpolation accuracy for the illumination map; normally 1.0 is fine.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1.0
)

BRDFSSS2Complex.scale= FloatProperty(
	name= "Scale",
	description= "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smalle.",
	min= 0.0,
	max= 1000.0,
	soft_min= 0.0,
	soft_max= 1000.0,
	precision= 4,
	default= 1
)

BRDFSSS2Complex.ior= FloatProperty(
	name= "IOR",
	description= 'TODO.',
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1.5
)

BRDFSSS2Complex.diffuse_amount= FloatProperty(
	name= "Diffuse amount",
	description= 'TODO.',
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0.0
)

BRDFSSS2Complex.scatter_radius_mult= FloatProperty(
	name= "Scatter radius",
	description= 'TODO.',
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1.0
)

BRDFSSS2Complex.overall_color= FloatVectorProperty(
	name= "Overall color",
	description= 'TODO.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

BRDFSSS2Complex.diffuse_color= FloatVectorProperty(
	name= "Diffuse color",
	description= 'TODO.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.5,0.5,0.5)
)

BRDFSSS2Complex.sub_surface_color= FloatVectorProperty(
	name= "Sub surface color",
	description= 'TODO.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.5,0.5,0.5)
)

BRDFSSS2Complex.scatter_radius= FloatVectorProperty(
	name= "Scatter radius",
	description= 'TODO.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.92,0.52,0.175)
)

BRDFSSS2Complex.phase_function= FloatProperty(
	name= "Phase function",
	description= 'TODO.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

BRDFSSS2Complex.specular_color= FloatVectorProperty(
	name= "Specular color",
	description= 'TODO.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

BRDFSSS2Complex.specular_subdivs= IntProperty(
	name= "Specular subdivs",
	description= 'TODO.',
	min= 0,
	max= 10,
	default= 8
)

BRDFSSS2Complex.specular_amount= FloatProperty(
	name= "Specular amount",
	description= 'TODO.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

BRDFSSS2Complex.specular_glossiness= FloatProperty(
	name= "Specular glossiness",
	description= 'TODO.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.6
)

BRDFSSS2Complex.cutoff_threshold= FloatProperty(
	name= "Cutoff threshold",
	description= 'TODO.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.01
)

BRDFSSS2Complex.trace_reflections= BoolProperty(
	name= "Trace reflections",
	description= "TODO.",
	default= True
)

BRDFSSS2Complex.reflection_depth= IntProperty(
	name= "Reflection depth",
	description= 'TODO.',
	min= 0,
	max= 10,
	default= 5
)

BRDFSSS2Complex.single_scatter= EnumProperty(
	name= "Single scatter",
	description= 'TODO.',
	items= (
		('NONE',"None",""),
		('SIMPLE',"Simple",""),
		('SOLID',"Raytraced (solid)",""),
		('REFR',"Raytraced (refractive)","")
	),
	default= "SIMPLE"
)

BRDFSSS2Complex.subdivs= IntProperty(
	name= "Subdivs",
	description= 'TODO.',
	min= 0,
	max= 10,
	default= 8
)

BRDFSSS2Complex.refraction_depth= IntProperty(
	name= "Refraction depth",
	description= 'TODO.',
	min= 0,
	max= 10,
	default= 5
)

BRDFSSS2Complex.front_scatter= BoolProperty(
	name= "Front scatter",
	description= 'TODO.',
	default= True
)

BRDFSSS2Complex.back_scatter= BoolProperty(
	name= "Back scatter",
	description= 'TODO.',
	default= True
)

BRDFSSS2Complex.scatter_gi= BoolProperty(
	name= "Scatter GI",
	description= 'TODO.',
	default= False
)

BRDFSSS2Complex.prepass_blur= FloatProperty(
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
class MtlWrapper(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.MtlWrapper= PointerProperty(
	name= "MtlWrapper",
	type=  MtlWrapper,
	description= "V-Ray MtlWrapper settings"
)

# MtlWrapper.BoolProperty(
# 	attr= 'use',
# 	name= "Use material wrapper",
# 	description= "Use material wrapper options.",
# 	default= False
# )

# # base_material: plugin (The base material)

# # generate_gi: float (Controls the GI generated by the material.)
# MtlWrapper.FloatProperty(
# 	attr= 'generate_gi',
# 	name= 'Generate GI',
# 	description= "Controls the GI generated by the material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # receive_gi: float (Controls the GI received by the material.)
# MtlWrapper.FloatProperty(
# 	attr= 'receive_gi',
# 	name= 'Receive GI',
# 	description= "Controls the GI received by the material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # generate_caustics: float (Controls the caustics generated by the material.)
# MtlWrapper.FloatProperty(
# 	attr= 'generate_caustics',
# 	name= 'Generate caustics',
# 	description= "Controls the caustics generated by the material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # receive_caustics: float (Controls the caustics received by the material.)
# MtlWrapper.FloatProperty(
# 	attr= 'receive_caustics',
# 	name= 'Receive caustics',
# 	description= "Controls the caustics received by the material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # alpha_contribution: float (The contribution of the resulting color to the alpha channel.)
# MtlWrapper.FloatProperty(
# 	attr= 'alpha_contribution',
# 	name= 'Alpha contribution',
# 	description= "The contribution of the resulting color to the alpha channel.",
# 	min= -1.0,
# 	max= 1.0,
# 	soft_min= -1.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # matte_surface: bool (Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.)
# MtlWrapper.BoolProperty(
# 	attr= 'matte_surface',
# 	name= 'Matte surface',
# 	description= "Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.",
# 	default= False
# )

# # shadows: bool (Turn this on to make shadow visible on the matter surface.)
# MtlWrapper.BoolProperty(
# 	attr= 'shadows',
# 	name= 'Shadows',
# 	description= "Turn this on to make shadow visible on the matter surface.",
# 	default= False
# )

# # affect_alpha: bool (Turn this on to make shadows affect the alpha contribution of the matte surface.)
# MtlWrapper.BoolProperty(
# 	attr= 'affect_alpha',
# 	name= 'Affect alpha',
# 	description= "Turn this on to make shadows affect the alpha contribution of the matte surface.",
# 	default= False
# )

# # shadow_tint_color: color (Tint for the shadows on the matte surface.) = Color(0, 0, 0)
# MtlWrapper.FloatVectorProperty( 
# 	attr= "shadow_tint_color", 
# 	name= "Shadow tint color", 
# 	description= 'Tint for the shadows on the matte surface.', 
# 	subtype= "COLOR", 
# 	min= 0.0, 
# 	max= 1.0, 
# 	soft_min= 0.0, 
# 	soft_max= 1.0, 
# 	default= (0.0, 0.0, 0.0)
# )

# # shadow_brightness: float (An optional brightness parameter for the shadows on the matte surface.A value of 0.0 will make the shadows completely invisible, while a value of 1.0 will show the full shadows.)
# MtlWrapper.FloatProperty(
# 	attr= 'shadow_brightness',
# 	name= 'Shadow brightness',
# 	description= "An optional brightness parameter for the shadows on the matte surface.A value of 0.0 will make the shadows completely invisible, while a value of 1.0 will show the full shadows.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # reflection_amount: float (Shows the reflections of the base material.)
# MtlWrapper.FloatProperty(
# 	attr= 'reflection_amount',
# 	name= 'Reflection amount',
# 	description= "Shows the reflections of the base material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # refraction_amount: float (Shows the refractions of the base material.)
# MtlWrapper.FloatProperty(
# 	attr= 'refraction_amount',
# 	name= 'Refraction amount',
# 	description= "Shows the refractions of the base material.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # gi_amount: float (Determines the amount of gi shadows.)
# MtlWrapper.FloatProperty(
# 	attr= 'gi_amount',
# 	name= 'GI amount',
# 	description= "Determines the amount of gi shadows.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # no_gi_on_other_mattes: bool (This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.)
# MtlWrapper.BoolProperty(
# 	attr= 'no_gi_on_other_mattes',
# 	name= 'No gi on other mattes',
# 	description= "This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.",
# 	default= True
# )

# # matte_for_secondary_rays: bool (Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc))
# MtlWrapper.BoolProperty(
# 	attr= 'matte_for_secondary_rays',
# 	name= 'Matte for secondary rays',
# 	description= "Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc)",
# 	default= False
# )

# # gi_surface_id: integer (If two objects have different GI surface ids, the light cache samples of the two objects will not be blended)
# MtlWrapper.IntProperty(
# 	attr= 'gi_surface_id',
# 	name= 'GI surface id',
# 	description= "If two objects have different GI surface ids, the light cache samples of the two objects will not be blended",
# 	min= 0,
# 	max= 10,
# 	default= 0
# )

# # gi_quality_multiplier: float (A multiplier for GI quality)
# MtlWrapper.FloatProperty(
# 	attr= 'gi_quality_multiplier',
# 	name= 'GI quality multiplier',
# 	description= "A multiplier for GI quality",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

# # reflection_filter_tex: acolor texture = AColor(1, 1, 1, 1)
# MtlWrapper.FloatVectorProperty( 
# 	attr= "reflection_filter_tex", 
# 	name= "Reflection filter",
# 	description= 'Reflection filter.', 
# 	subtype= "COLOR", 
# 	min= 0.0, 
# 	max= 1.0, 
# 	soft_min= 0.0, 
# 	soft_max= 1.0, 
# 	default= (1.0, 1.0, 1.0)
# )

# # trace_depth: integer (The maximum reflection depth (-1 is controlled by the global options))
# MtlWrapper.IntProperty(
# 	attr= 'trace_depth',
# 	name= 'Trace depth',
# 	description= "The maximum reflection depth (-1 is controlled by the global options)",
# 	min= -1,
# 	max= 1000,
# 	default= -1
# )

# # channels: plugin (Render channels the result of this BRDF will be written to), unlimited list

MtlWrapper.use= BoolProperty(
	name= "Use material wrapper",
	description= "Use material wrapper options.",
	default= False
)

MtlWrapper.generate_gi= FloatProperty(
	name= "Generate GI",
	description= "Controls the GI generated by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.receive_gi= FloatProperty(
	name= "Receive GI",
	description= "Controls the GI received by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.generate_caustics= FloatProperty(
	name= "Generate caustics",
	description= "Controls the caustics generated by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.receive_caustics= FloatProperty(
	name= "Receive caustics",
	description= "Controls the caustics received by the material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.alpha_contribution= FloatProperty(
	name= "Alpha contribution",
	description= "The contribution of the resulting color to the alpha channel.",
	min= -1.0,
	max= 1.0,
	soft_min= -1.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.matte_surface= BoolProperty(
	name= "Matte surface",
	description= "Makes the material appear as a matte material, which shows the background, instead of the base material, when viewed directly.",
	default= False
)

MtlWrapper.shadows= BoolProperty(
	name= "Shadows",
	description= "Turn this on to make shadow visible on the matter surface.",
	default= False
)

MtlWrapper.affect_alpha= BoolProperty(
	name= "Affect alpha",
	description= "Turn this on to make shadows affect the alpha contribution of the matte surface.",
	default= False
)

MtlWrapper.shadow_tint_color= FloatVectorProperty(
	name= "Shadow tint color",
	description= 'Tint for the shadows on the matte surface.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

MtlWrapper.shadow_brightness= FloatProperty(
	name= "Shadow brightness",
	description= "An optional brightness parameter for the shadows on the matte surface.A value of 0.0 will make the shadows completely invisible, while a value of 1.0 will show the full shadows.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.reflection_amount= FloatProperty(
	name= "Reflection amount",
	description= "Shows the reflections of the base material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.refraction_amount= FloatProperty(
	name= "Refraction amount",
	description= "Shows the refractions of the base material.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.gi_amount= FloatProperty(
	name= "GI amount",
	description= "Determines the amount of gi shadows.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.no_gi_on_other_mattes= BoolProperty(
	name= "No gi on other mattes",
	description= "This will cause the material to appear as a matte object in reflections, refractions, GI etc for other matte objects.",
	default= True
)

MtlWrapper.matte_for_secondary_rays= BoolProperty(
	name= "Matte for secondary rays",
	description= "Turn this on to make the material act as matte for all secondary rays (reflections, refractions, etc)",
	default= False
)

MtlWrapper.gi_surface_id= IntProperty(
	name= "GI surface id",
	description= "If two objects have different GI surface ids, the light cache samples of the two objects will not be blended",
	min= 0,
	max= 10,
	default= 0
)

MtlWrapper.gi_quality_multiplier= FloatProperty(
	name= "GI quality multiplier",
	description= "A multiplier for GI quality",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

MtlWrapper.reflection_filter_tex= FloatVectorProperty(
	name= "Reflection filter",
	description= 'Reflection filter.',
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

MtlWrapper.trace_depth= IntProperty(
	name= "Trace depth",
	description= "The maximum reflection depth (-1 is controlled by the global options)",
	min= -1,
	max= 1000,
	default= -1
)


'''
  MtlOverride
'''
class MtlOverride(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.MtlOverride= PointerProperty(
	name= "MtlOverride",
	type=  MtlOverride,
	description= "V-Ray MtlOverride settings"
)

MtlOverride.use= BoolProperty(
	name= "Use override material",
	description= "Use override material.",
	default= False
)


'''
  Plugin: LightMesh
'''
class LightMesh(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.LightMesh= PointerProperty(
	name= "LightMesh",
	type=  LightMesh,
	description= "Mesh light settings"
)

# LightMesh.BoolProperty(
# 	attr= 'enabled',
# 	name= "Enabled",
# 	description= "Light\'s on/off state.",
# 	default= True
# )

# LightMesh.EnumProperty(
# 	attr= 'lightPortal',
# 	name= "Light portal mode",
# 	description= "Specifies if the light is a portal light.",
# 	items=(
# 		('NORMAL',  "Normal light",   ""),
# 		('PORTAL',  "Portal",         ""),
# 		('SPORTAL', "Simple portal",  "")
# 	),
# 	default= 'NORMAL'
# )

# LightMesh.EnumProperty(
# 	attr= 'units',
# 	name= "Intensity units",
# 	description= "Units for the intensity.",
# 	items=(
# 		('DEFUALT',  "Default",   ""),
# 		('LUMENS',   "Lumens",    ""),
# 		('LUMM',     "Lm/m/m/sr", ""),
# 		('WATTSM',   "Watts",     ""),
# 		('WATM',     "W/m/m/sr", "")
# 	),
# 	default= 'DEFAULT'
# )

# LightMesh.FloatProperty(
# 	attr= 'intensity',
# 	name= "Intensity",
# 	description= "Light intensity.",
# 	min= 0.0,
# 	max= 10000000.0,
# 	soft_min= 0.0,
# 	soft_max= 100.0,
# 	precision= 2,
# 	default= 30
# )

# LightMesh.IntProperty(
# 	attr= 'causticSubdivs',
# 	name= "Caustic subdivs",
# 	description= "Caustic subdivs.",
# 	min= 1,
# 	max= 10000,
# 	default= 1000
# )

# LightMesh.IntProperty(
# 	attr= 'subdivs',
# 	name= "Subdivs",
# 	description= "The number of samples V-Ray takes to compute lighting.",
# 	min= 0,
# 	max= 256,
# 	default= 8
# )

# LightMesh.BoolProperty(
# 	attr= 'noDecay',
# 	name= "No decay",
# 	description= "TODO.",
# 	default= False
# )

# LightMesh.BoolProperty(
# 	attr= 'affectReflections',
# 	name= "Affect reflections",
# 	description= "true if the light appears in reflections and false otherwise",
# 	default= True
# )

# LightMesh.BoolProperty(
# 	attr= 'invisible',
# 	name= "Invisible",
# 	description= "TODO.",
# 	default= False
# )

# LightMesh.BoolProperty(
# 	attr= 'storeWithIrradianceMap',
# 	name= "Store with Irradiance Map",
# 	description= "TODO.",
# 	default= False
# )

# LightMesh.BoolProperty(
# 	attr= 'affectDiffuse',
# 	name= "Affect diffuse",
# 	description= "true if the light produces diffuse lighting and false otherwise",
# 	default= True
# )

# LightMesh.BoolProperty(
# 	attr= 'affectSpecular',
# 	name= "Affect dpecular",
# 	description= "true if the light produces specular hilights and false otherwise",
# 	default= True
# )

# LightMesh.BoolProperty(
# 	attr= 'doubleSided',
# 	name= "Double-sided",
# 	description= "TODO.",
# 	default= False
# )

LightMesh.enabled= BoolProperty(
	name= "Enabled",
	description= "Light\'s on/off state.",
	default= True
)

LightMesh.lightPortal= EnumProperty(
	name= "Light portal mode",
	description= "Specifies if the light is a portal light.",
	items= (
		('NORMAL',"Normal light",""),
		('PORTAL',"Portal",""),
		('SPORTAL',"Simple portal","")
	),
	default= 'NORMAL'
)

LightMesh.units= EnumProperty(
	name= "Intensity units",
	description= "Units for the intensity.",
	items= (
		('DEFUALT',"Default",""),
		('LUMENS',"Lumens",""),
		('LUMM',"Lm/m/m/sr",""),
		('WATTSM',"Watts",""),
		('WATM',"W/m/m/sr","")
	),
	default= 'DEFAULT'
)

LightMesh.intensity= FloatProperty(
	name= "Intensity",
	description= "Light intensity.",
	min= 0.0,
	max= 10000000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 2,
	default= 30
)

LightMesh.causticSubdivs= IntProperty(
	name= "Caustic subdivs",
	description= "Caustic subdivs.",
	min= 1,
	max= 10000,
	default= 1000
)

LightMesh.subdivs= IntProperty(
	name= "Subdivs",
	description= "The number of samples V-Ray takes to compute lighting.",
	min= 0,
	max= 256,
	default= 8
)

LightMesh.noDecay= BoolProperty(
	name= "No decay",
	description= "TODO.",
	default= False
)

LightMesh.affectReflections= BoolProperty(
	name= "Affect reflections",
	description= "true if the light appears in reflections and false otherwise",
	default= True
)

LightMesh.invisible= BoolProperty(
	name= "Invisible",
	description= "TODO.",
	default= False
)

LightMesh.storeWithIrradianceMap= BoolProperty(
	name= "Store with Irradiance Map",
	description= "TODO.",
	default= False
)

LightMesh.affectDiffuse= BoolProperty(
	name= "Affect diffuse",
	description= "true if the light produces diffuse lighting and false otherwise",
	default= True
)

LightMesh.affectSpecular= BoolProperty(
	name= "Affect dpecular",
	description= "true if the light produces specular hilights and false otherwise",
	default= True
)

LightMesh.doubleSided= BoolProperty(
	name= "Double-sided",
	description= "TODO.",
	default= False
)



'''
  Plugin: EnvironmentFog
'''
class EnvironmentFog(bpy.types.IDPropertyGroup):
    pass

VRayMaterial.EnvironmentFog= PointerProperty(
	name= "EnvironmentFog",
	type=  EnvironmentFog,
	description= "V-Ray EnvironmentFog settings"
)

EnvironmentFog.emission= FloatVectorProperty(
	name= "Emission",
	description= "Fog emission color",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0,0,0)
)

EnvironmentFog.color= FloatVectorProperty(
	name= "Color",
	description= "Fog color",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0,1.0,1.0)
)

EnvironmentFog.distance= FloatProperty(
	name= "Distance",
	description= "Distance between fog particles",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0.2
)

EnvironmentFog.density= FloatProperty(
	name= "Density",
	description= "Fog density",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1
)

EnvironmentFog.use_height= BoolProperty(
	name= "Use height",
	description= "Whether or not the height should be taken into account.",
	default= False
)

EnvironmentFog.height= FloatProperty(
	name= "Height",
	description= "Fog starting point along the Z-axis.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 100
)

EnvironmentFog.subdivs= IntProperty(
	name= "Subdivs",
	description= "Fog subdivision",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 8
)

EnvironmentFog.affect_background= BoolProperty(
	name= "Affect background",
	description= "Affect background",
	default= False
)

EnvironmentFog.yup= BoolProperty(
	name= "Y-up",
	description= "If true, y is the up axis, not z.",
	default= False
)

EnvironmentFog.fade_out_mode= EnumProperty(
	name= "Fade out mode",
	description= "Fade out mode.",
	items= (
		('SUBSTRACT',"Substract",""),
		('MULT',"Multiply","")
	),
	default= 'MULT'
)

EnvironmentFog.fade_out_radius= FloatProperty(
	name= "Fade out radius",
	description= "Fade out effect for the edges",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0
)

EnvironmentFog.per_object_fade_out_radius= BoolProperty(
	name= "Per object fade out radius",
	description= "Fade out effect for the edges per object",
	default= False
)

EnvironmentFog.use_fade_out_tex= BoolProperty(
	name= "Use fade out tex",
	description= "True if the fade_out_tex should be used for fade out computation.",
	default= True
)

EnvironmentFog.edge_fade_out= FloatProperty(
	name= "Edge fade out",
	description= "Used with the fade_out_tex, mimics Maya fluid's edge dropoff attribute",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0
)

EnvironmentFog.fade_out_type= IntProperty(
	name= "Fade out type",
	description= "0 - used for the gradients and the grid falloff(fadeout);1 - used for the sphere, cone and double cone types;2 - used for the cube type, the computations are done in the TexMayaFluidProcedural plug-in;",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 0
)

EnvironmentFog.scatter_gi= BoolProperty(
	name= "Scatter GI",
	description= "Scatter global illumination",
	default= True
)

EnvironmentFog.scatter_bounces= IntProperty(
	name= "Scatter bounces",
	description= "Number of GI bounces calculated inside the fog",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 8
)

EnvironmentFog.simplify_gi= BoolProperty(
	name= "Simplify GI",
	description= "Simplify global illumination",
	default= False
)

EnvironmentFog.step_size= FloatProperty(
	name= "Step size",
	description= "Size of one step through the volume",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1
)

EnvironmentFog.max_steps= IntProperty(
	name= "Max steps",
	description= "Maximum number of steps through the volume",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 1000
)

EnvironmentFog.tex_samples= IntProperty(
	name= "Texture samples",
	description= "Number of texture samples for each step through the volume",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 4
)

EnvironmentFog.cutoff_threshold= FloatProperty(
	name= "Cutoff",
	description= "Controls when the raymarcher will stop traversing the volume.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0.001
)

EnvironmentFog.light_mode= EnumProperty(
	name= "Light mode",
	description= "Light mode.",
	items= (
		('ADDGIZMO',"Add to per-gizmo lights",""),
		('INTERGIZMO',"Intersect with per-gizmo lights",""),
		('OVERGIZMO',"Override per-gizmo lights",""),
		('PERGIZMO',"Use per-gizmo lights",""),
		('NO',"No lights","")
	),
	default= 'PERGIZMO'
)

EnvironmentFog.use_shade_instance= BoolProperty(
	name= "Use shade instance",
	description= "True if the shade instance should be used when sampling textures.",
	default= False
)



# '''
#   Presets
# '''
# import os
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
# 			s= "bpy.context.active_object.active_material.vray.BRDFSSS2Complex.%s = %s\n"%("%s"%(param), ps)
# 			ofile.write(s.replace(')','').replace('(',''))
# 		ofile.write("\n")
# 		ofile.close()
# generate_presets()



'''
  GUI
'''
import properties_material
#properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER')
properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
del properties_material


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
	bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		rd= context.scene.render
		return (context.material or context.object) and (rd.engine in cls.COMPAT_ENGINES)
	
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
				if mat:
					row.prop(mat, "use_nodes", icon="NODETREE", text="")

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
			vray= mat.vray
			if wide_ui:
				layout.prop(vray, 'type', expand=True)
			else:
				layout.prop(vray, 'type')


# class MATERIAL_PT_VRAY_preview(MaterialButtonsPanel, bpy.types.Panel):
# 	bl_label = "Preview"
#	bl_options = {'DEFAULT_CLOSED'}
# 	bl_show_header = True

# 	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

# 	@classmethod
# 	def poll(cls, context):
# 		return base_poll(__class__, context)

# 	def draw(self, context):
# 		self.layout.template_preview(context.material)


class MATERIAL_PT_VRAY_basic(MaterialButtonsPanel, bpy.types.Panel):
	bl_label   = "Parameters"
	#bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		sce= context.scene
		ve= sce.vray.exporter
		ob= context.object

		mat= active_node_mat(context.material)
		vma= mat.vray
				
		if vma.type == 'MTL':
			BRDFVRayMtl= vma.BRDFVRayMtl
			
			raym= mat.raytrace_mirror
			rayt= mat.raytrace_transparency

			row= layout.row()
			colL= row.column()
			colL.label(text="Diffuse")

			split= layout.split()
			col= split.column()
			col.prop(mat, "diffuse_color", text="")
			col.prop(BRDFVRayMtl, 'roughness')
			if wide_ui:
				col= split.column()
			col.prop(mat, 'alpha')

			split= layout.split()
			col= split.column()
			col.label(text="Reflections")

			split= layout.split()
			col= split.column(align=True)
			col.prop(BRDFVRayMtl, 'reflect_color', text="")
			if not BRDFVRayMtl.hilight_glossiness_lock:
				col.prop(BRDFVRayMtl, 'hilight_glossiness', slider=True)
			col.prop(BRDFVRayMtl, "reflect_glossiness", text="Glossiness", slider=True)
			col.prop(BRDFVRayMtl, 'reflect_subdivs', text="Subdivs")
			col.prop(BRDFVRayMtl, 'reflect_depth', text="Depth")
			if wide_ui:
				col= split.column()
			col.prop(BRDFVRayMtl, 'brdf_type', text="")
			col.prop(BRDFVRayMtl, "hilight_glossiness_lock")

			if not BRDFVRayMtl.brdf_type == 'PHONG':
				col.prop(BRDFVRayMtl, "anisotropy")
				col.prop(BRDFVRayMtl, "anisotropy_rotation")
			col.prop(BRDFVRayMtl, "fresnel")
			if BRDFVRayMtl.fresnel:
				col.prop(BRDFVRayMtl, "fresnel_ior")

			split= layout.split()
			col= split.column(align=True)
			col.label(text="Refractions")
			col.prop(BRDFVRayMtl, 'refract_color', text="")
			col.prop(BRDFVRayMtl, 'refract_ior', text="IOR")
			col.prop(BRDFVRayMtl, 'refract_glossiness', text="Glossiness", slider=True)
			col.prop(BRDFVRayMtl, 'refract_subdivs', text="Subdivs")
			col.prop(BRDFVRayMtl, 'refract_depth', text="Depth")
			if wide_ui:
				col= split.column(align=True)
			col.label(text="Fog")
			col.prop(BRDFVRayMtl, 'fog_color', text="")
			col.prop(BRDFVRayMtl, 'fog_mult')
			col.prop(BRDFVRayMtl, 'fog_bias')
			col.label(text='')
			col.prop(BRDFVRayMtl, 'refract_affect_alpha')
			col.prop(BRDFVRayMtl, 'refract_affect_shadows')

			if not ve.compat_mode:
				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop(BRDFVRayMtl, 'translucency')
				if(BRDFVRayMtl.translucency != 'NONE'):
					split= layout.split()
					col= split.column()
					col.prop(BRDFVRayMtl, 'translucency_color', text="")
					col.prop(BRDFVRayMtl, 'translucency_thickness', text="Thickness")
					if wide_ui:
						col= split.column()
					col.prop(BRDFVRayMtl, 'translucency_scatter_coeff', text="Scatter coeff")
					col.prop(BRDFVRayMtl, 'translucency_scatter_dir', text="Fwd/Bck coeff")
					col.prop(BRDFVRayMtl, 'translucency_light_mult', text="Light multiplier")

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(vma, 'two_sided')
			if vma.two_sided:
				if wide_ui:
					col= split.column()
				col.prop(vma, 'two_sided_translucency', slider=True, text="Translucency")

		elif vma.type == 'EMIT':
			row= layout.row()
			colL= row.column()
			colL.label(text="Color")

			row= layout.row()
			col= row.column()
			col.prop(mat, 'diffuse_color', text="")
			if wide_ui:
				col= row.column()
			if not vma.emitter_type == 'MESH':
				col.prop(mat, 'alpha')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(vma, 'emitter_type')

			layout.separator()

			if vma.emitter_type == 'MESH':
				LightMesh= vma.LightMesh

				split= layout.split()
				col= split.column()
				col.prop(LightMesh, 'enabled', text="On")
				col.prop(LightMesh, 'lightPortal', text="Mode")
				if LightMesh.lightPortal == 'NORMAL':
					col.prop(LightMesh, 'units', text="Units")
					col.prop(LightMesh, 'intensity', text="Intensity")
				col.prop(LightMesh, 'subdivs')
				col.prop(LightMesh, 'causticSubdivs', text="Caustics")
				if wide_ui:
					col= split.column()
				col.prop(LightMesh, 'invisible')
				col.prop(LightMesh, 'affectDiffuse')
				col.prop(LightMesh, 'affectSpecular')
				col.prop(LightMesh, 'affectReflections')
				col.prop(LightMesh, 'noDecay')
				col.prop(LightMesh, 'doubleSided')
				col.prop(LightMesh, 'storeWithIrradianceMap')
			else:
				emit= vma.BRDFLight

				split= layout.split()
				col= split.column()
				col.prop(mat, 'emit', text="Intensity")
				if wide_ui:
					col= split.column()
				col.prop(emit, 'emitOnBackSide')
				col.prop(emit, 'compensateExposure', text="Compensate exposure")
				col.prop(emit, 'doubleSided')

		elif vma.type == 'SSS':
			BRDFSSS2Complex= vma.BRDFSSS2Complex

			split= layout.split()
			col= split.column()
			col.label(text='General')

			split= layout.split()
			col= split.column()
			col.menu('MATERIAL_MT_VRAY_presets', text="Presets")

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'prepass_rate')
			col.prop(BRDFSSS2Complex, 'scale')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'ior')
			col.prop(BRDFSSS2Complex, 'interpolation_accuracy', text='Accuracy')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.label(text='Overall color')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'overall_color', text='')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'phase_function')

			split= layout.split()
			col= split.column()
			col.label(text='Diffuse color')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'diffuse_color', text='')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'diffuse_amount')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'sub_surface_color')
			if wide_ui:
				col= split.column()

			split= layout.split()
			col= split.column()
			col.label(text='Scatter color')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'scatter_radius', text='')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'scatter_radius_mult')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.label(text='Specular layer')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'specular_color', text='')
			col.prop(BRDFSSS2Complex, 'specular_subdivs', text='Subdivs')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'specular_amount', text='Amount')
			col.prop(BRDFSSS2Complex, 'specular_glossiness', text='Glossiness')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'trace_reflections')
			if BRDFSSS2Complex.trace_reflections:
				if wide_ui:
					col= split.column()
				col.prop(BRDFSSS2Complex, 'reflection_depth')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.label(text='Options:')

			split= layout.split()
			col= split.column()
			col.prop(BRDFSSS2Complex, 'single_scatter', text='Type')
			col.prop(BRDFSSS2Complex, 'subdivs')
			col.prop(BRDFSSS2Complex, 'refraction_depth')
			col.prop(BRDFSSS2Complex, 'cutoff_threshold')
			if wide_ui:
				col= split.column()
			col.prop(BRDFSSS2Complex, 'front_scatter')
			col.prop(BRDFSSS2Complex, 'back_scatter')
			col.prop(BRDFSSS2Complex, 'scatter_gi')
			col.prop(BRDFSSS2Complex, 'prepass_blur')

		elif vma.type == 'VOL':
			EnvironmentFog= vma.EnvironmentFog

			split= layout.split()
			col= split.column()
			col.prop(EnvironmentFog, 'color')
			if wide_ui:
				col= split.column()
			col.prop(EnvironmentFog, 'emission')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(EnvironmentFog, 'distance')
			col.prop(EnvironmentFog, 'density')
			col.prop(EnvironmentFog, 'subdivs')
			col.prop(EnvironmentFog, 'scatter_gi')
			if EnvironmentFog.scatter_gi:
				col.prop(EnvironmentFog, 'scatter_bounces')
			col.prop(EnvironmentFog, 'use_height')
			if EnvironmentFog.use_height:
				col.prop(EnvironmentFog, 'height')
			if wide_ui:
				col= split.column()
			#col.prop(EnvironmentFog, 'fade_out_type')
			col.prop(EnvironmentFog, 'fade_out_radius')
			col.prop(EnvironmentFog, 'affect_background')
			col.prop(EnvironmentFog, 'use_shade_instance')
			col.prop(EnvironmentFog, 'simplify_gi')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(EnvironmentFog, 'light_mode')
			col.prop(EnvironmentFog, 'fade_out_mode')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(EnvironmentFog, 'step_size')
			col.prop(EnvironmentFog, 'max_steps')
			if wide_ui:
				col= split.column()
			col.prop(EnvironmentFog, 'tex_samples')
			col.prop(EnvironmentFog, 'cutoff_threshold')

			# We have per material setup
			#col.prop(EnvironmentFog, 'per_object_fade_out_radius')

			#col.prop(EnvironmentFog, 'emission_tex')
			#col.prop(EnvironmentFog, 'color_tex')
			#col.prop(EnvironmentFog, 'density_tex')

			#col.prop(EnvironmentFog, 'use_fade_out_tex')
			#col.prop(EnvironmentFog, 'fade_out_tex')
			#col.prop(EnvironmentFog, 'edge_fade_out')

			#col.prop(EnvironmentFog, 'yup')
		else:
			pass


class MATERIAL_PT_VRAY_options(MaterialButtonsPanel, bpy.types.Panel):
	bl_label   = "Options"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		vma= active_ma.vray
		return base_poll(__class__, context) and (vma.type == 'MTL')

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > 200
		
		ve= context.scene.vray.exporter
		ob= context.object
		ma= active_node_mat(context.material)
		
		BRDFVRayMtl= ma.vray.BRDFVRayMtl

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'reflect_trace')
		col.prop(BRDFVRayMtl, 'refract_trace')
		if ve.compat_mode:
			col.prop(BRDFVRayMtl, 'option_cutoff')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'option_double_sided')
		col.prop(BRDFVRayMtl, 'option_reflect_on_back')
		col.prop(BRDFVRayMtl, 'option_use_irradiance_map')

		if not ve.compat_mode:
			split= layout.split()
			col= split.column()
			col.prop(BRDFVRayMtl, 'option_glossy_rays_as_gi')
			col.prop(BRDFVRayMtl, 'option_energy_mode')

			split= layout.split()
			col= split.column()
			col.prop(BRDFVRayMtl, 'option_cutoff')
			if wide_ui:
				col= split.column()
			col.prop(BRDFVRayMtl, 'environment_priority')


class MATERIAL_PT_VRAY_override(MaterialButtonsPanel, bpy.types.Panel):
	bl_label   = "Override"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		vma= active_ma.vray
		return base_poll(__class__, context) and not (vma.type == 'EMIT' and vma.emitter_type == 'MESH') and not vma.type == 'VOL'

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		MtlOverride= ma.vray.MtlOverride
		self.layout.prop(MtlOverride, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		MtlOverride= ma.vray.MtlOverride
		
		layout= self.layout
		layout.active= MtlOverride.use

		split= layout.split()
		col= split.column()
		col.label(text="Coming soon!")
	

class MATERIAL_PT_VRAY_wrapper(MaterialButtonsPanel, bpy.types.Panel):
	bl_label   = "Wrapper"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		vma= active_ma.vray
		return base_poll(__class__, context) and not (vma.type == 'EMIT' and vma.emitter_type == 'MESH') and not vma.type == 'VOL'

	def draw_header(self, context):
		mat= active_node_mat(context.material)
		MtlWrapper= mat.vray.MtlWrapper
		self.layout.prop(MtlWrapper, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		MtlWrapper= ma.vray.MtlWrapper
		
		layout= self.layout
		layout.active= MtlWrapper.use

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'generate_gi')
		col.prop(MtlWrapper, 'receive_gi')
		if wide_ui:
			col= split.column()
		col.prop(MtlWrapper, 'generate_caustics')
		col.prop(MtlWrapper, 'receive_caustics')

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'gi_quality_multiplier')

		split= layout.split()
		col= split.column()
		col.label(text="Matte properties")

		split= layout.split()
		colL= split.column()
		colL.prop(MtlWrapper, 'matte_surface')
		if wide_ui:
			colR= split.column()
		else:
			colR= colL
		colR.prop(MtlWrapper, 'alpha_contribution')
		if MtlWrapper.matte_surface:
			colL.prop(MtlWrapper, 'affect_alpha')
			colL.prop(MtlWrapper, 'shadows')
			if MtlWrapper.shadows:
				colL.prop(MtlWrapper, 'shadow_tint_color')
				colL.prop(MtlWrapper, 'shadow_brightness')

			colR.prop(MtlWrapper, 'reflection_amount')
			colR.prop(MtlWrapper, 'refraction_amount')
			colR.prop(MtlWrapper, 'gi_amount')
			colR.prop(MtlWrapper, 'no_gi_on_other_mattes')

		split= layout.split()
		col= split.column()
		col.label(text="Miscellaneous")

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'gi_surface_id')
		col.prop(MtlWrapper, 'trace_depth')
		if wide_ui:
			col= split.column()
		col.prop(MtlWrapper, 'matte_for_secondary_rays')


class MATERIAL_PT_VRAY_render(MaterialButtonsPanel, bpy.types.Panel):
	bl_label   = "Render"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		vma= active_ma.vray
		return base_poll(__class__, context) and not (vma.type == 'EMIT' and vma.emitter_type == 'MESH') and not vma.type == 'VOL'

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		MtlRenderStats= ma.vray.MtlRenderStats
		self.layout.prop(MtlRenderStats, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		MtlRenderStats= ma.vray.MtlRenderStats

		layout= self.layout
		layout.active= MtlRenderStats.use

		split= layout.split()
		col= split.column()
		col.prop(MtlRenderStats, 'visibility', text="Visible")

		split= layout.split()
		col= split.column()
		col.label(text="Visible to:")

		split= layout.split()
		sub= split.column()
		sub.active= MtlRenderStats.visibility
		sub.prop(MtlRenderStats, 'camera_visibility', text="Camera")
		sub.prop(MtlRenderStats, 'gi_visibility', text="GI")
		sub.prop(MtlRenderStats, 'shadows_visibility', text="Shadows")
		if wide_ui:
			sub= split.column()
			sub.active= MtlRenderStats.visibility
		sub.prop(MtlRenderStats, 'reflections_visibility', text="Reflections")
		sub.prop(MtlRenderStats, 'refractions_visibility', text="Refractions")

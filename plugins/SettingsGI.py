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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''

TYPE= 'SETTINGS'

ID=   'SETTINGSGI'
NAME= 'Global Illumination'
PLUG= 'SettingsGI'
DESC= "Global illumination settings."

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class SettingsGI(bpy.types.IDPropertyGroup):
	pass

def add_properties(parent_struct):
	parent_struct.SettingsGI= PointerProperty(
		type= SettingsGI,
		name= NAME,
		description= DESC
	)

	SettingsGI.on= BoolProperty(
		name= "Enable GI",
		description= "Enable Global Illumination.",
		default= False
	)

	SettingsGI.primary_engine= EnumProperty(
		name= "Primary engine",
		description= "Primary diffuse bounces engines.",
		items= (
			('IM',  "Irradiance map", ""),
			# ('PM',  "Photon map", ""),
			('BF',  "Brute force", ""),
			('LC',  "Light cache", "")
		),
		default= 'IM'
	)

	SettingsGI.secondary_engine= EnumProperty(
		name= "Secondary engine",
		description= "Secondary diffuse bounces engines.",
		items= (
			('NONE',  "None", ""),
			# ('PM',    "Photon map", ""),
			('BF',    "Brute force", ""),
			('LC',    "Light cache", "")
		),
		default= 'LC'
	)

	SettingsGI.preset= EnumProperty(
		name= "Preset",
		description= "GI preset.",
		items= (
			# ('SALUTO',"SALuto",""),
			('DRAFT',"Draft",""),
			('QUAL',"Quality",""),
			('NONE',"None","")
		),
		default= 'NONE'
	)

	SettingsGI.primary_multiplier= FloatProperty(
		name= "Primary multiplier",
		description= "This value determines how much primary diffuse bounces contribute to the final image illumination.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsGI.secondary_multiplier= FloatProperty(
		name= "Secondary multiplier",
		description= "This determines the effect of secondary diffuse bounces on the scene illumination.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsGI.refract_caustics= BoolProperty(
		name= "Refract caustics",
		description= "This allows indirect lighting to pass through transparent objects (glass etc).",
		default= 1
	)

	SettingsGI.reflect_caustics= BoolProperty(
		name= "Reflect caustics",
		description= "This allows indirect light to be reflected from specular objects (mirrors etc).",
		default= 0
	)

	SettingsGI.saturation= FloatProperty(
		name= "Saturation",
		description= "Controls the saturation of the GI.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsGI.contrast= FloatProperty(
		name= "Contrast",
		description= "This parameter works together with Contrast base to boost the contrast of the GI solution.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsGI.contrast_base= FloatProperty(
		name= "Contrast base",
		description= "This parameter determines the base for the contrast boost.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.5
	)


	class SettingsDMCGI(bpy.types.IDPropertyGroup):
		pass

	SettingsGI.SettingsDMCGI= PointerProperty(
		name= "DMC GI",
		type=  SettingsDMCGI,
		description= "DMC GI settings."
	)

	SettingsDMCGI.depth= IntProperty(
		name= "Secondary bounces",
		description= "The number of light bounces that will be computed.",
		min= 1,
		max= 100,
		default= 3
	)

	SettingsDMCGI.subdivs= IntProperty(
		name= "Subdivs",
		description= "The number of samples used to approximate GI.",
		min= 1,
		max= 500,
		default= 8
	)


	class SettingsIrradianceMap(bpy.types.IDPropertyGroup):
		pass

	SettingsGI.SettingsIrradianceMap= PointerProperty(
		name= "Irradiance Map",
		type=  SettingsIrradianceMap,
		description= "Irradiance Map settings."
	)

	SettingsIrradianceMap.preset= EnumProperty(
		name= "Preset",
		description= "Build-in presets.",
		items= (
			('VLOW',"Very low",""),
			('LOW',"Low",""),
			('MEDIUM',"Medium",""),
			('MEDIUM_ANIM',"Medium animation",""),
			('HIGH',"High",""),
			('HIGH_ANIM',"High animation",""),
			('VHIGH',"Very high","")
		),
		default= "HIGH"
	)

	SettingsIrradianceMap.mode= EnumProperty(
		name= "Irradiance map mode",
		description= "Irradiance map mode.",
		items= (
			('SINGLE',"Single frame","A new irradiance map is created for each frame."),
			('INC',"Multiframe incremental","At the start of the rendering, the irradiance map is deleted, and then each frame incrementally adds to the irradiance map in memory."),
			('FILE',"From file","The irradiance map is loaded from a file."),
			('ADD',"Add to current map","A new irradiance map is created and added to the one in memory."),
			('INC',"Incremental add to current map","Each frame adds incrementally to the irradiance map in memory; the old map is not deleted."),
			('BUCKET',"Bucket mode","Each render region (bucket) calculates its own irradiance map independently of the rest."),
			('ANIM_PRE',"Animation (prepass)","Separate irradiance map is rendered and saved with a different name for each frame; no final image is rendered."),
			('ANIM_REND',"Animation (rendering)","Final rendering of animation using saved per-frame irradiance maps.")
		),
		default= "SINGLE"
	)

	SettingsIrradianceMap.lookupType= EnumProperty(
		name= "Sample lookup",
		description= "Method of choosing suitable points from the irradiance map to be used as basis for the interpolation.",
		items= (
			('QUAD',"Quad-balanced",""),
			('NEAREST',"Nearest",""),
			('OVERLAP',"Overlapping",""),
			('DENSITY',"Density-based","")
		),
		default= "OVERLAP"
	)

	SettingsIrradianceMap.interpolationType= EnumProperty(
		name= "Interpolation type",
		description= "Method for interpolating the GI value from the samples in the irradiance map.",
		items= (
			('VORONOI',"Least squares with Voronoi weights",""),
			('DELONE',"Delone triangulation",""),
			('LEAST',"Least squares fit",""),
			('WEIGHTED',"Weighted average","")
		),
		default= "LEAST"
	)

	SettingsIrradianceMap.detail_scale= EnumProperty(
		name= "Detail enhancement scale",
		description= "Build-in presets.",
		items= (
			('SCREEN',"Screen",""),
			('WORLD',"World","")
		),
		default= "SCREEN"
	)

	SettingsIrradianceMap.min_rate= IntProperty(
		name= "Min rate",
		description= "This value determines the resolution for the first GI pass.",
		min= -10,
		max= 1,
		default= -3
	)

	SettingsIrradianceMap.max_rate= IntProperty(
		name= "Max rate",
		description= "This value determines the resolution of the last GI pass.",
		min= -10,
		max= 1,
		default= 0
	)

	SettingsIrradianceMap.color_threshold= FloatProperty(
		name= "Color threshold",
		description= "This parameter controls how sensitive the irradiance map algorithm is to changes in indirect lighting.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.30
	)

	SettingsIrradianceMap.normal_threshold= FloatProperty(
		name= "Normal threshold",
		description= "This parameter controls how sensitive the irradiance map is to changes in surface normals and small surface details.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.10
	)

	SettingsIrradianceMap.distance_threshold= FloatProperty(
		name= "Distance threshold",
		description= "This parameter controls how sensitive the irradiance map is to distance between surfaces.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.10
	)

	SettingsIrradianceMap.show_calc_phase= BoolProperty(
		name= "Show calc. phase",
		description= "Show irradiance map calculations.",
		default= 1
	)

	SettingsIrradianceMap.show_direct_light= BoolProperty(
		name= "Show direct light",
		description= "Show direct light.",
		default= 1
	)

	SettingsIrradianceMap.show_samples= BoolProperty(
		name= "Show samples",
		description= "Show irradiance map samples.",
		default= 0
	)

	SettingsIrradianceMap.subdivs= IntProperty(
		name= "Hemispheric subdivs",
		description= "This controls the quality of individual GI samples.",
		min= 1,
		max= 500,
		default= 50
	)

	SettingsIrradianceMap.interp_samples= IntProperty(
		name= "Interpolation samples",
		description= "The number of GI samples that will be used to interpolate the indirect illumination at a given point.",
		min= 1,
		max= 100,
		default= 20
	)

	SettingsIrradianceMap.interp_frames= IntProperty(
		name= "Interpolation frames",
		description= "The number of frames that will be used to interpolate GI when the \"Mode\" is set to \"Animation (rendering)\"",
		min= 1,
		max= 50,
		default= 2
	)

	SettingsIrradianceMap.calc_interp_samples= IntProperty(
		name= "Calc. pass interpolation samples",
		description= "The number of already computed samples that will be used to guide the sampling algorithm.",
		min= 1,
		max= 30,
		default= 10
	)

	SettingsIrradianceMap.detail_enhancement= BoolProperty(
		name= "Detail enhancement",
		description= "Detail enhancement is a method for bringing additional detail to the irradiance map in the case where there are small details in the image.",
		default= 0
	)

	SettingsIrradianceMap.detail_subdivs_mult= FloatProperty(
		name= "Detail enhancement subdivs mult",
		description= "The number of samples taken for the high-precision sampling as a percentage of the irradiance map Hemispheric subdivs.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.30
	)

	SettingsIrradianceMap.detail_radius= FloatProperty(
		name= "Detail enhancement radius",
		description= "This determines the radius for the detail enhancement effect.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.06
	)

	SettingsIrradianceMap.multipass= BoolProperty(
		name= "Multipass",
		description= "When checked, this will cause V-Ray to use all irradiance map samples computed so far.",
		default= 0
	)

	SettingsIrradianceMap.multiple_views= BoolProperty(
		name= "Use camera path",
		description= "When this option is on, V-Ray will calculate the irradiance map samples for the entire camera path, instead of just the current view.",
		default= 0
	)

	SettingsIrradianceMap.randomize_samples= BoolProperty(
		name= "Randomize samples",
		description= "When it is checked, the image samples will be randomly jittered.",
		default= 1
	)

	SettingsIrradianceMap.check_sample_visibility= BoolProperty(
		name= "Check sample visibility",
		description= "This will cause V-Ray to use only those samples from the irradiance map, which are directly visible from the interpolated point.",
		default= 0
	)

	SettingsIrradianceMap.file= StringProperty(
		name= "Irradiance map file name",
		subtype= 'FILE_PATH',
		description= "Irradiance map file name."
	)

	SettingsIrradianceMap.auto_save= BoolProperty(
		name= "Auto save irradiance map",
		description= "Automatically save the irradiance map to the specified file at the end of the rendering.",
		default= 0
	)

	SettingsIrradianceMap.auto_save_file= StringProperty(
		name= "Irradiance map auto save file",
		subtype= 'FILE_PATH',
		description= "Irradiance map auto save file."
	)


	class SettingsLightCache(bpy.types.IDPropertyGroup):
		pass

	SettingsGI.SettingsLightCache= PointerProperty(
		name= "Light Cache",
		type=  SettingsLightCache,
		description= "Light Cache settings."
	)

	SettingsLightCache.mode= EnumProperty(
		name= "Light cache mode",
		description= "Light cache mode.",
		items= (
			('SINGLE',"Single frame",""),
			('FILE',"From file",""),
			('FLY',"Fly-through",""),
			('PPT',"Progressive path tracing","")
		),
		default= "SINGLE"
	)

	SettingsLightCache.subdivs= IntProperty(
		name= "Subdivs",
		description= "This determines how many paths are traced from the camera. The actual number of paths is the square of the subdivs.",
		min= 1,
		max= 65535,
		default= 1000
	)

	SettingsLightCache.scale= EnumProperty(
		name= "Light cache scale mode",
		description= "This parameter determines the units of the \"Sample size\" and the \"Filter size\"",
		items= (
			('SCREEN',  "Screen", ""),
			('WORLD',   "World", ""),
		),
		default= 'SCREEN'
	)

	SettingsLightCache.sample_size= FloatProperty(
		name= "Sample size",
		description= "This determines the spacing of the samples in the light cache.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 4,
		default= 0.02
	)

	SettingsLightCache.num_passes= IntProperty(
		name= "Number of passes",
		description= "The light cache is computed in several passes, which are then combined into the final light cache.",
		min= 1,
		max= 1000,
		default= 4
	)

	SettingsLightCache.num_passes_auto= BoolProperty(
		name= "Auto num. passes",
		description= "Set number of passes to threads number.",
		default= 0
	)

	SettingsLightCache.depth= IntProperty(
		name= "Depth",
		description= "Light cache depth.",
		min= 1,
		max= 1000,
		soft_min= 1,
		soft_max= 100,
		default= 100
	)

	SettingsLightCache.show_calc_phase= BoolProperty(
		name= "Show calc phase",
		description= "Turning this option on will show the paths that are traced.",
		default= 0
	)

	SettingsLightCache.store_direct_light= BoolProperty(
		name= "Store direct light",
		description= "With this option, the light cache will also store and interpolate direct light.",
		default= 1
	)

	SettingsLightCache.adaptive_sampling= BoolProperty(
		name= "Adaptive sampling",
		description= "When this option is on, V-Ray will store additional information about the incoming light for each light cache sample, and try to put more samples into the directions from which more light coming.",
		default= 0
	)

	SettingsLightCache.filter= BoolProperty(
		name= "Filter",
		description= "Enable render-time filter for the light cache.",
		default= 1
	)

	SettingsLightCache.filter_type= EnumProperty(
		name= "Filter type",
		description= "The filter determines how irradiance is interpolated from the samples in the light cache.",
		items= (
			('NEAREST',"Nearest",""),
			('FIXED',"Fixed","")
		),
		default= "NEAREST"
	)

	SettingsLightCache.filter_samples= IntProperty(
		name= "Samples",
		description= "How many of the nearest samples to look up from the light cache.",
		min= 1,
		max= 1000,
		default= 10
	)

	SettingsLightCache.filter_size= FloatProperty(
		name= "Size",
		description= "The size of the filter.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.02
	)

	SettingsLightCache.prefilter= BoolProperty(
		name= "Pre-filter",
		description= "Filter light cache sampler before rendering.",
		default= 0
	)

	SettingsLightCache.prefilter_samples= IntProperty(
		name= "Samples",
		description= "Number of samples.",
		min= 1,
		max= 1000,
		default= 40
	)

	SettingsLightCache.multiple_views= BoolProperty(
		name= "Use camera path",
		description= "When this option is on, V-Ray will calculate the light cache samples for the entire camera path, instead of just the current view, in the same way as this is done for the Fly-through mode.",
		default= 0
	)

	SettingsLightCache.use_for_glossy_rays= BoolProperty(
		name= "Use for glossy rays",
		description= "If this option is on, the light cache will be used to compute lighting for glossy rays as well, in addition to normal GI rays.",
		default= 0
	)

	SettingsLightCache.file= StringProperty(
		name= "Light cache file name",
		subtype= 'FILE_PATH',
		description= "Light cache file name."
	)

	SettingsLightCache.auto_save= BoolProperty(
		name= "Auto save light cache",
		description= "Light cache file name.",
		default= 0
	)

	SettingsLightCache.auto_save_file= StringProperty(
		name= "Light cache auto save file",
		subtype= 'FILE_PATH',
		description= "Light cache auto save file."
	)


	class SettingsPhotonMap(bpy.types.IDPropertyGroup):
		pass

	SettingsGI.SettingsPhotonMap= PointerProperty(
		name= "Photon Map",
		type=  SettingsPhotonMap,
		description= "Photon Map settings."
	)

	SettingsPhotonMap.convex_hull_estimate= BoolProperty(
		name= "Convex hull estimate",
		description= "TODO.",
		default= 0
	)

	SettingsPhotonMap.prefilter= BoolProperty(
		name= "Convert to irradiance map",
		description= "This will cause V-Ray to precompute the irradiance at the photon hit points stored in the photon map.",
		default= 0
	)

	SettingsPhotonMap.prefilter_samples= IntProperty(
		name= "Interpolate samples",
		description= "This controls how many irradiance samples will be taken from the photon map once it is converted to an irradiance map.",
		min= 1,
		max= 100,
		default= 10
	)

	SettingsPhotonMap.store_direct_light= BoolProperty(
		name= "Store direct light",
		description= "Store direct illumination in the photon map as well.",
		default= 1
	)

	SettingsPhotonMap.auto_search_distance= BoolProperty(
		name= "Auto search distance",
		description= "Try to compute a suitable distance within which to search for photons.",
		default= 1
	)

	SettingsPhotonMap.search_distance= FloatProperty(
		name= "Search distance",
		description= "Photon search distance.",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		default= 20.0
	)

	SettingsPhotonMap.retrace_corners= FloatProperty(
		name= "Retrace corners",
		description= "When this is greater than 0.0, V-Ray will use brute force GI near corners, instead of the photon map, in order to obtain a more accurate result and to avoid splotches in these areas. ",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	SettingsPhotonMap.retrace_bounces= IntProperty(
		name= "Retrace bounces",
		description= "Controls how many bounces will be made when retracing corners.",
		min= 1,
		max= 100,
		default= 10
	)

	SettingsPhotonMap.bounces= IntProperty(
		name= "Bounces",
		description= "The number of light bounces approximated by the photon map.",
		min= 1,
		max= 1000,
		default= 10
	)

	SettingsPhotonMap.multiplier= FloatProperty(
		name= "Multiplier",
		description= "This allows you to control the brightness of the photon map.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		default= 1.0
	)

	SettingsPhotonMap.max_photons= IntProperty(
		name= "Max photons",
		description= "This option specifies how many photons will be taken into consideration when approximating the irradiance at the shaded point.",
		min= 1,
		max= 10000,
		default= 30
	)

	SettingsPhotonMap.max_density= FloatProperty(
		name= "Max density",
		description= "This parameter allows you to limit the resolution (and thus the memory) of the photon map.",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		default= 0.0
	)

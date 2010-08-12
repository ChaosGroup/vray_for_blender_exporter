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

''' vb modules '''
from vb25.utils import *
from vb25.plugin_manager import *


FloatProperty= VRayScene.FloatProperty
IntProperty= VRayScene.IntProperty
BoolProperty= VRayScene.BoolProperty
StringProperty= VRayScene.StringProperty
EnumProperty= VRayScene.EnumProperty
CollectionProperty= VRayScene.CollectionProperty


'''
	SettingsGI
'''
BoolProperty(	attr="enable_gi",
				name="Enable GI",
				description="Enable Global Illumination.",
				default= False)

EnumProperty(   attr="vray_gi_primary_engine",
				name="Primary engine",
				description="Primary diffuse bounces engines.",
				items=(
					("IM",  "Irradiance map", ""),
					#("PM",  "Photon map", ""),
					("BF",  "Brute force", ""),
					("LC",  "Light cache", "")
				),
				default= "IM")

FloatProperty(  attr="vray_gi_primary_multiplier",
                name="Primary multiplier",
                description="This value determines how much primary diffuse bounces contribute to the final image illumination.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default=1.0)

EnumProperty(   attr="vray_gi_secondary_engine",
				name="Secondary engine",
				description="Secondary diffuse bounces engines.",
				items=(
					("NONE",  "None", ""),
					#("PM",    "Photon map", ""),
					("BF",    "Brute force", ""),
					("LC",    "Light cache", "")
				),
				default= "LC")

FloatProperty(  attr="vray_gi_secondary_multiplier",
                name="Secondary multiplier",
                description="This determines the effect of secondary diffuse bounces on the scene illumination.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default=1.0)

BoolProperty(   attr="vray_gi_refract_caustics",
                name="Refract caustics",
                description="This allows indirect lighting to pass through transparent objects (glass etc).",
                default= 1)

BoolProperty(   attr="vray_gi_reflect_caustics",
                name="Reflect caustics",
                description="This allows indirect light to be reflected from specular objects (mirrors etc).",
                default= 0)

FloatProperty(  attr="vray_gi_saturation",
                name="Saturation",
                description="Controls the saturation of the GI.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default=1.0)

FloatProperty(  attr="vray_gi_contrast",
                name="Contrast",
                description="This parameter works together with Contrast base to boost the contrast of the GI solution.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default=1.0)

FloatProperty(  attr="vray_gi_contrast_base",
                name="Contrast base",
                description="This parameter determines the base for the contrast boost.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default=0.5)


'''
	SettingsDMCSampler
'''
FloatProperty(  attr="vray_adaptive_threshold",
                name="Noise threshold",
                description="Controls V-Ray's judgement of when a blurry value is \"good enough\" to be used.",
                min=0.0, max=1.0, soft_min=0.001, soft_max=0.1, default=0.01, precision=3)

IntProperty(    attr="vray_adaptive_min_samples",
                name="Min samples",
                description="The minimum number of samples that must be made before the early termination algorithm is used.",
                min=1, max=100, default=8)

FloatProperty(  attr="vray_adaptive_amount",
                name="Adaptive amount",
                description="A value of 1.0 means full adaptation; a value of 0.0 means no adaptation.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.85, precision=2)

BoolProperty(   attr="vray_time_dependent",
                name="Time dependent",
                description="This make the samping pattern change with time.",
                default= 0)

FloatProperty(  attr="vray_subdivs_mult",
                name="Subdivs mult",
                description="This will multiply all subdivs values everywhere during rendering.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=1.0)


'''
	SettingsDMCGI
'''
IntProperty(    attr="vray_dmcgi_depth",
                name="Secondary bounces",
                description="The number of light bounces that will be computed.",
                min=1, max=100, default=3)

IntProperty(    attr="vray_dmcgi_subdivs",
                name="Subdivs",
                description="The number of samples used to approximate GI.",
                min=1, max=500, default=8)


'''
	SettingsIrradianceMap
'''
EnumProperty(   attr="vray_im_preset",
				name="Preset",
				description="Build-in presets.",
				items=(
					("VLOW",        "Very low", ""),
					("LOW",         "Low", ""),
					("MEDIUM",      "Medium", ""),
					("MEDIUM_ANIM", "Medium animation", ""),
					("HIGH",        "High", ""),
					("HIGH_ANIM",   "High animation", ""),
					("VHIGH",       "Very high", "")
				),
				default= "HIGH")

EnumProperty(   attr="vray_im_mode",
				name="Irradiance map mode",
				description="Irradiance map mode.",
				items=(
					("SINGLE",      "Single frame", "A new irradiance map is created for each frame."),
					("INC",         "Incremental", "At the start of the rendering, the irradiance map is deleted, and then each frame incrementally adds to the irradiance map in memory."),
					("FILE",        "From file", "The irradiance map is loaded from a file."),
					("ADD",         "Add", "A new irradiance map is created and added to the one in memory."),
					("INC",         "Add incremental", "Each frame adds incrementally to the irradiance map in memory; the old map is not deleted."),
					("BUCKET",      "Bucket mode", "Each render region (bucket) calculates its own irradiance map independently of the rest."),
					("ANIM_PRE",    "Animation (prepass)", "Separate irradiance map is rendered and saved with a different name for each frame; no final image is rendered."),
					("ANIM_REND",   "Animation (rendering)", "Final rendering of animation using saved per-frame irradiance maps.")
				),
				default= "SINGLE")

EnumProperty(   attr="vray_im_lookupType",
				name="Sample lookup",
				description="Method of choosing suitable points from the irradiance map to be used as basis for the interpolation.",
				items=(
					("QUAD",     "Quad-balanced", ""),
					("NEAREST",  "Nearest", ""),
					("OVERLAP",  "Overlapping", ""),
					("DENSITY",  "Density-based", "")
				),
				default= "OVERLAP")

EnumProperty(   attr="vray_im_interpolationType",
				name="Interpolation type",
				description="Method for interpolating the GI value from the samples in the irradiance map.",
				items=(
					("VORONOI",   "Least squares with Voronoi weights", ""),
					("DELONE",    "Delone triangulation", ""),
					("LEAST",     "Least squares fit", ""),
					("WEIGHTED",  "Weighted average", "")
				),
				default= "LEAST")

EnumProperty(   attr="vray_im_detail_scale",
				name="Detail enhancement scale",
				description="Build-in presets.",
				items=(
					("SCREEN",  "Screen", ""),
					("WORLD",   "World", "")
				),
				default= "SCREEN")

IntProperty(    attr="vray_im_min_rate",
                name="Min rate",
                description="This value determines the resolution for the first GI pass.",
                min=-10, max=1, default=-3)

IntProperty(    attr="vray_im_max_rate",
                name="Max rate",
                description="This value determines the resolution of the last GI pass.",
                min=-10, max=1, default=0)

FloatProperty(  attr="vray_im_color_threshold",
                name="Color threshold",
                description="This parameter controls how sensitive the irradiance map algorithm is to changes in indirect lighting.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.30)

FloatProperty(  attr="vray_im_normal_threshold",
                name="Normal threshold",
                description="This parameter controls how sensitive the irradiance map is to changes in surface normals and small surface details.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.10)

FloatProperty(  attr="vray_im_distance_threshold",
                name="Distance threshold",
                description="This parameter controls how sensitive the irradiance map is to distance between surfaces.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.10)

BoolProperty(   attr="vray_im_show_calc_phase",
                name="Show calc. phase",
                description="Show irradiance map calculations.",
                default= 1)

BoolProperty(   attr="vray_im_show_direct_light",
                name="Show direct light",
                description="Show direct light.",
                default= 1)

BoolProperty(   attr="vray_im_show_samples",
                name="Show samples",
                description="Show irradiance map samples.",
                default= 0)

IntProperty(    attr="vray_im_subdivs",
                name="Hemispheric subdivs",
                description="This controls the quality of individual GI samples.",
                min=1, max=500, default=50)

IntProperty(    attr="vray_im_interp_samples",
                name="Interpolation samples",
                description="The number of GI samples that will be used to interpolate the indirect illumination at a given point.",
                min=1, max=100, default=20)

IntProperty(    attr="vray_im_interp_frames",
                name="Interpolation frames",
                description="The number of frames that will be used to interpolate GI when the \"Mode\" is set to \"Animation (rendering)\"",
                min=1, max=50, default=2)

IntProperty(    attr="vray_im_calc_interp_samples",
                name="Calc. pass interpolation samples",
                description="The number of already computed samples that will be used to guide the sampling algorithm.",
                min=1, max=30, default=10)

BoolProperty(   attr="vray_im_detail_enhancement",
                name="Detail enhancement",
                description="Detail enhancement is a method for bringing additional detail to the irradiance map in the case where there are small details in the image.",
                default= 0)

FloatProperty(  attr="vray_im_detail_subdivs_mult",
                name="Detail enhancement subdivs mult",
                description="The number of samples taken for the high-precision sampling as a percentage of the irradiance map Hemispheric subdivs.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.30)

FloatProperty(  attr="vray_im_detail_radius",
                name="Detail enhancement radius",
                description="This determines the radius for the detail enhancement effect.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, default=0.06)

BoolProperty(   attr="vray_im_multipass",
                name="Multipass",
                description="When checked, this will cause V-Ray to use all irradiance map samples computed so far.",
                default= 0)

BoolProperty(   attr="vray_im_multiple_views",
                name="Use camera path",
                description="When this option is on, V-Ray will calculate the irradiance map samples for the entire camera path, instead of just the current view.",
                default= 0)

BoolProperty(   attr="vray_im_randomize_samples",
                name="Randomize samples",
                description="When it is checked, the image samples will be randomly jittered.",
                default= 1)

BoolProperty(   attr="vray_im_check_sample_visibility",
                name="Check sample visibility",
                description="This will cause V-Ray to use only those samples from the irradiance map, which are directly visible from the interpolated point.",
                default= 0)

StringProperty( attr="vray_im_file",
                name="Irradiance map file name",
				subtype= 'FILE_PATH',
                description="Irradiance map file name.")

BoolProperty(   attr="vray_im_auto_save",
                name="Auto save irradiance map",
                description="Automatically save the irradiance map to the specified file at the end of the rendering.",
                default= 0)

StringProperty( attr="vray_im_auto_save_file",
                name="Irradiance map auto save file",
				subtype= 'FILE_PATH',
                description="Irradiance map auto save file.")


'''
	SettingsLightCache
'''
EnumProperty(   attr="vray_lc_mode",
				name="Light cache mode",
				description="Light cache mode.",
				items=(
					("SINGLE",      "Single frame", ""),
					("FILE",        "From file", ""),
					("FLY",         "Fly-through", ""),
					("PPT",         "Progressive path tracing", "")
				),
				default= "SINGLE")

IntProperty(    attr="vray_lc_subdivs",
                name="Subdivs",
                description="This determines how many paths are traced from the camera. The actual number of paths is the square of the subdivs.",
                min=1, max=65535, default=1000)

FloatProperty(  attr="vray_lc_sample_size",
                name="Sample size",
                description="This determines the spacing of the samples in the light cache.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, precision=4, default=0.02)

EnumProperty(   attr="vray_lc_scale",
				name="Light cache scale mode",
				description="This parameter determines the units of the \"Sample size\" and the \"Filter size\"",
				items=(
					("SCREEN",  "Screen", ""),
					("WORLD",   "World", ""),
				),
				default= "SCREEN")

IntProperty(    attr="vray_lc_num_passes",
                name="Number of passes",
                description="The light cache is computed in several passes, which are then combined into the final light cache.",
                min=1, max=1000, default=4)

BoolProperty(   attr="vray_lc_num_passes_auto",
                name="Auto num. passes",
                description="Set number of passes to threads number.",
                default= 0)

IntProperty(    attr="vray_lc_depth",
                name="Depth",
                description="Light cache depth.",
                min=1, max=1000, soft_min=1, soft_max=100, default=100)

BoolProperty(   attr="vray_lc_show_calc_phase",
                name="Show calc phase",
                description="Turning this option on will show the paths that are traced.",
                default= 0)

BoolProperty(   attr="vray_lc_store_direct_light",
                name="Store direct light",
                description="With this option, the light cache will also store and interpolate direct light.",
                default= 1)

BoolProperty(   attr="vray_lc_adaptive_sampling",
                name="Adaptive sampling",
                description="When this option is on, V-Ray will store additional information about the incoming light for each light cache sample, and try to put more samples into the directions from which more light coming.",
                default= 0)

BoolProperty(   attr="vray_lc_filter",
                name="Filter",
                description="Enable render-time filter for the light cache.",
                default=1)

EnumProperty(   attr="vray_lc_filter_type",
				name="Filter type",
				description="The filter determines how irradiance is interpolated from the samples in the light cache.",
				items=(
					("NEAREST",  "Nearest", ""),
					("FIXED",    "Fixed", "")
				),
				default= "NEAREST")

IntProperty(    attr="vray_lc_filter_samples",
                name="Samples",
                description="How many of the nearest samples to look up from the light cache.",
                min=1, max=1000, default=10)

FloatProperty(  attr="vray_lc_filter_size",
                name="Size",
                description="The size of the filter.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, default=0.02)

BoolProperty(   attr="vray_lc_prefilter",
                name="Pre-filter",
                description="Filter light cache sampler before rendering.",
                default= 0)

IntProperty(    attr="vray_lc_prefilter_samples",
                name="Samples",
                description="Number of samples.",
                min=1, max=1000, default=40)

BoolProperty(   attr="vray_lc_multiple_views",
                name="Use camera path",
                description="When this option is on, V-Ray will calculate the light cache samples for the entire camera path, instead of just the current view, in the same way as this is done for the Fly-through mode.",
                default= 0)

BoolProperty(   attr="vray_lc_use_for_glossy_rays",
                name="Use for glossy rays",
                description="If this option is on, the light cache will be used to compute lighting for glossy rays as well, in addition to normal GI rays.",
                default= 0)

StringProperty( attr="vray_lc_file",
                name="Light cache file name",
				subtype= 'FILE_PATH',
                description="Light cache file name.")

BoolProperty(   attr="vray_lc_auto_save",
                name="Auto save light cache",
                description="Light cache file name.",
                default= 0)

StringProperty( attr="vray_lc_auto_save_file",
                name="Light cache auto save file",
				subtype= 'FILE_PATH',
				description="Light cache auto save file.")



'''
	SettingsPhotonMap
'''
BoolProperty(   attr="vray_pm_convex_hull_estimate",
                name="Convex hull estimate",
                description="",
                default= 0)
BoolProperty(   attr="vray_pm_prefilter",
                name="Convert to irradiance map",
                description="This will cause V-Ray to precompute the irradiance at the photon hit points stored in the photon map.",
                default= 0)
IntProperty(    attr="vray_pm_prefilter_samples",
                name="Interpolate samples",
                description="This controls how many irradiance samples will be taken from the photon map once it is converted to an irradiance map.",
                min=1, max=100, default=10)
BoolProperty(   attr="vray_pm_store_direct_light",
                name="Store direct light",
                description="Store direct illumination in the photon map as well.",
                default= 1)
BoolProperty(   attr="vray_pm_auto_search_distance",
                name="Auto search distance",
                description="Try to compute a suitable distance within which to search for photons.",
                default= 1)
FloatProperty(  attr="vray_pm_search_distance",
                name="Search distance",
                description="Photon search distance",
                min=0.0, max=1000.0, soft_min=0.0, soft_max=100.0, default=20.0)
FloatProperty(  attr="vray_pm_retrace_corners",
                name="Retrace corners",
                description="When this is greater than 0.0, V-Ray will use brute force GI near corners, instead of the photon map, in order to obtain a more accurate result and to avoid splotches in these areas. ",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)
IntProperty(    attr="vray_pm_retrace_bounces",
                name="Retrace bounces",
                description="Controls how many bounces will be made when retracing corners.",
                min=1, max=100, default=10)
IntProperty(    attr="vray_pm_bounces",
                name="Bounces",
                description="The number of light bounces approximated by the photon map.",
                min=1, max=1000, default=10)
FloatProperty(  attr="vray_pm_multiplier",
                name="Multiplier",
                description="This allows you to control the brightness of the photon map.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=1.0)
IntProperty(    attr="vray_pm_max_photons",
                name="Max photons",
                description="This option specifies how many photons will be taken into consideration when approximating the irradiance at the shaded point.",
                min=1, max=10000, default=30)
FloatProperty(  attr="vray_pm_max_density",
                name="Max density",
                description="This parameter allows you to limit the resolution (and thus the memory) of the photon map.",
                min=0.0, max=1000.0, soft_min=0.0, soft_max=100.0, default=0.0)


'''
	SettingsColorMapping
'''
EnumProperty(   attr="vray_cm_type",
				name="Color mapping type",
				description="Color mapping type.",
				items=(
					("LNR",   "Linear", ""),
					("EXP",   "Exponential", ""),
					("HSV",   "HSV exponential", ""),
					("INT",   "Intensity exponential", ""),
					("GCOR",  "Gamma correction", ""),
					("GINT",  "Intensity gamma", ""),
					("REIN",  "Reinhard", "")
				),
				default= "LNR")

BoolProperty(   attr="vray_affect_background",
                name="Affect background",
                description="Affect colors belonging to the background.",
                default= 1)

FloatProperty(  attr="vray_dark_mult",
                name="Dark multiplier",
                description="Multiplier for dark colors.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, default=1.0)

FloatProperty(  attr="vray_bright_mult",
                name="Bright multiplier",
                description="Multiplier for bright colors.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, default=1.0)

FloatProperty(  attr="vray_gamma",
                name="Gamma",
                description="Gamma correction for the output image regardless of the color mapping mode.",
                min=0.0, max=10.0, soft_min=1.0, soft_max=2.2, default=1.0)

BoolProperty(   attr="vray_clamp_output",
                name="Clamp output",
                description="Clamp colors after color mapping.",
                default= 1)

FloatProperty(  attr="vray_clamp_level",
                name="Clamp level",
                description="The level at which colors will be clamped.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=100.0, default=1.0)

BoolProperty(   attr="vray_subpixel_mapping",
                name="Sub-pixel mapping",
                description="This option controls whether color mapping will be applied to the final image pixels, or to the individual sub-pixel samples.",
                default= 0)

BoolProperty(   attr="vray_adaptation_only",
                name="Adaptation only",
                description="When this parameter is on, the color mapping will not be applied to the final image, however V-Ray will proceed with all its calculations as though color mapping is applied (e.g. the noise levels will be corrected accordingly).",
                default= 0)

BoolProperty(   attr="vray_linearWorkflow",
                name="Linear workflow",
                description="When this option is checked V-Ray will automatically apply the inverse of the Gamma correction that you have set in the Gamma field to all materials in scene.",
                default= 0)


'''
	SettingsCaustics
'''
BoolProperty(
	attr= "enable_caustics",
	name= "Enable caustics",
	description= "Enable caustics computation.",
	default= False
)


'''
	SettingsDefaultDisplacement
'''


'''
	SettingsImageSampler
'''
EnumProperty(   attr="vray_filter_type",
				name="Filter type",
				description="Antialiasing filter.",
				items=(
					("NONE",      "None", ""),
					("GAUSS",     "Gaussian", ""),
					("SINC",      "Sinc", ""),
					("CATMULL",   "CatmullRom", ""),
					("LANC",      "Lanczos", ""),
					("TRIANGLE",  "Triangle", ""),
					("BOX",       "Box", ""),
					("AREA",      "Area", "")
				),
				default= "")

FloatProperty(  attr="vray_filter_size",
                name="Filter size",
                description="Filter size.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=1.5)

EnumProperty(   attr="vray_is_type",
				name="Image sampler type",
				description="Image sampler type.",
				items=(
					("FXD",  "Fixed", ""),
					("DMC",  "Adaptive DMC", ""),
					("SBD",  "Adaptive subdivision", "")
				),
				default= "DMC")

IntProperty(    attr="vray_dmc_minSubdivs",
                name="Min subdivs",
                description="The initial (minimum) number of samples taken for each pixel.",
                min=1, max=100, default=1)

IntProperty(    attr="vray_dmc_maxSubdivs",
                name="Max subdivs",
                description="The maximum number of samples for a pixel.",
                min=1, max=100, default=4)

BoolProperty(   attr="vray_dmc_treshhold_use_dmc",
                name="Use DMC sampler threshold",
                description="Use threshold specified in the \"DMC sampler\"",
                default=1)

FloatProperty(  attr="vray_dmc_threshold",
                name="Color threshold",
                description="The threshold that will be used to determine if a pixel needs more samples.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.01)

BoolProperty(   attr="vray_dmc_show_samples",
                name="Show samples",
                description="Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
                default=0)

IntProperty(    attr="vray_fixed_subdivs",
                name="Subdivs",
                description="The number of samples per pixel.",
                min=1, max=100, default=1)

BoolProperty(   attr="vray_subdivision_show_samples",
                name="Show samples",
                description="Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
                default= 0)

BoolProperty(   attr="vray_subdivision_normals",
                name="Normals",
                description="This will supersample areas with sharply varying normals.",
                default= 0)

FloatProperty(  attr="vray_subdivision_normals_threshold",
                name="Normals threshold",
                description="Normals threshold.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.05)

BoolProperty(   attr="vray_subdivision_jitter",
                name="Randomize samples",
                description="Displaces the samples slightly to produce better antialiasing of nearly horizontal or vertical lines.",
                default= 1)

FloatProperty(  attr="vray_subdivision_threshold",
                name="Color threshold",
                description="Determines the sensitivity of the sampler to changes in pixel intensity.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.1)

BoolProperty(   attr="vray_subdivision_edges",
                name="Object outline",
                description="This will cause the image sampler to always supersample object edges.",
				default=0)

IntProperty(    attr="vray_subdivision_minRate",
                name="Min rate",
                description="Minimum number of samples per pixel.",
                min=-10, max=50, default=-1)

IntProperty(    attr="vray_subdivision_maxRate",
                name="Max rate",
                description="Maximum number of samples per pixel.",
                min=-10, max=50, default=2)



'''
	SettingsRaycaster
'''
IntProperty(    attr="vray_maxLevels",
                name="Max. tree depth",
                description="Maximum BSP tree depth.",
                min=50, max=100, default=80)

FloatProperty(  attr="vray_minLeafSize",
                name="Min. leaf size",
                description="Minimum size of a leaf node.",
                min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

FloatProperty(  attr="vray_faceLevelCoef",
                name="Face/level",
                description="Maximum amount of triangles in a leaf node.",
                min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default=1.0)

IntProperty(    attr="vray_dynMemLimit",
                name="Dynamic memory limit",
                description="RAM limit for the dynamic raycasters.",
                min=100, max=100000, default=400)


'''
	SettingsUnitsInfo
'''
FloatProperty(  attr= "vray_photometric_scale",
                name= "Photometric scale",
                description= "Photometric scale.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=1.0, precision=4, default=0.002)

FloatProperty(  attr= "vray_meters_scale",
                name= "Meters scale",
                description= "Meters scale.",
                min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, precision=3, default=1.0)



'''
	Exporter
'''
class VRayExporter(bpy.types.IDPropertyGroup):
	pass

VRayScene.PointerProperty(
	attr= 'exporter',
	type= VRayExporter,
	name= "V-Ray Exporter Settings",
	description= "V-Ray Exporter settings."
)

VRayExporter.BoolProperty(
	attr= "use_material_nodes",
	name= "Use Material Nodes",
	description= "Use material nodes.",
	default= False
)

VRayExporter.BoolProperty(
	attr= "image_to_blender",
	name= "Image To Blender",
	description= "Pass image to Blender on render end.",
	default= False
)

VRayExporter.BoolProperty(
	attr="log_window",
	name="Show Log Window",
	description="Show log window (Linux).",
	default= 0
)

VRayExporter.BoolProperty(
	attr= 'animation',
	name= "Animation",
	description= "Render animation.",
	default= 0
)

VRayExporter.BoolProperty(
	attr= 'active_layers',
	name= "Active Layers",
	description= "Render objects only from visible layers.",
	default= False
)

VRayExporter.BoolProperty(
	attr= 'auto_meshes',
	name= "Auto export meshes",
	description= "Export meshes automatically before render.",
	default= 0
)

VRayExporter.BoolProperty(
	attr= 'autorun',
	name= "Autorun",
	description= "Start V-Ray automatically after export.",
	default= 1
)

VRayExporter.BoolProperty(
	attr= 'debug',
	name= "Debug",
	description= "Enable script\'s debug output.",
	default= 0
)

# BoolProperty(   attr="vray_export_duplibase",
#                 name="vray_export_duplibase",
#                 description="",
#                 default= 0)

# IntProperty(    attr="vray_verboseLevel",
#                 name="vray_verboseLevel",
#                 description="",
#                 min=, max=, default=3)

# BoolProperty(   attr="vray_dr",
#                 name="vray_dr",
#                 description="",
#                 default= 0)

# BoolProperty(   attr="vray_export_bake",
#                 name="vray_export_bake",
#                 description="",
#                 default= 0)

# IntProperty(    attr="vray_dr_port",
#                 name="vray_dr_port",
#                 description="",
#                 min=, max=, default=20204)

# StringProperty( attr="vray_dr_hosts",
#                 name="vray_dr_hosts",
#                 description="")

# BoolProperty(   attr="vray_display",
#                 name="vray_display",
#                 description="",
#                 default= 1)


'''
	SettingsOutput
'''
# BoolProperty(   attr="vray_autosave",
#                 name="vray_autosave",
#                 description="",
#                 default= 1)

# BoolProperty(   attr="vray_autosave_alpha",
#                 name="vray_img_separateAlpha",
#                 description="",
#                 default= 1)


# BoolProperty(   attr="vray_stamp",
#                 name="vray_stamp",
#                 description="",
#                 default= 0)


'''
	SettingsOptions
'''
# geom_displacement: bool = true
# geom_doHidden: bool = true
# light_doLights: bool = true
# light_doDefaultLights: bool = true
# light_doHiddenLights: bool = true
# light_doShadows: bool = true
# light_onlyGI: bool = false
# gi_dontRenderImage: bool = false, Don't render final image
# mtl_reflectionRefraction: bool = true
# mtl_limitDepth: bool = false, Limit max depth
# mtl_maxDepth: integer = 5, Max. ray depth for reflections and refractions
# mtl_doMaps: bool = true
# mtl_filterMaps: bool = true
# mtl_transpMaxLevels: integer = 50, Max. transparency levels
# mtl_transpCutoff: float = 0.001, Transparency cutoff
# mtl_override_on: bool = false, Override material
# mtl_glossy: bool = true, Glossy effects
# geom_backfaceCull: bool = false, If true, back faces will be invisible to camera and shadow rays
# ray_bias: float = 0, Secondary ray bias
# misc_lowThreadPriority: bool = false
# IntProperty(    attr="vray_mtl_limitDepth",
#                 name="vray_mtl_limitDepth",
#                 description="",
#                 min=, max=, default=0)
# IntProperty(    attr="vray_mtl_transpMaxLevels",
#                 name="vray_mtl_transpMaxLevels",
#                 description="",
#                 min=, max=, default=50)
# FloatProperty(  attr="vray_mtl_transpCutoff",
#                 name="vray_mtl_transpCutoff",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=0.0100)
# IntProperty(    attr="vray_mtl_overall_type",
#                 name="vray_mtl_overall_type",
#                 description="",
#                 min=, max=, default=0)
# IntProperty(    attr="vray_mtl_maxDepth",
#                 name="vray_mtl_maxDepth",
#                 description="",
#                 min=, max=, default=5)
# BoolProperty(   attr="vray_mtl_reflect_refract",
#                 name="vray_mtl_reflect_refract",
#                 description="",
#                 default= 1)
# BoolProperty(   attr="vray_mtl_glossy",
#                 name="vray_mtl_glossy",
#                 description="",
#                 default= 1)
# BoolProperty(   attr="vray_mtl_doMaps",
#                 name="vray_mtl_doMaps",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_mtl_overall",
#                 name="vray_mtl_overall",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_mtl_limitDepth",
#                 name="vray_mtl_limitDepth",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_mtl_overall_type",
#                 name="vray_mtl_overall_type",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_mtl_overall_mat",
#                 name="vray_mtl_overall_mat",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_mtl_filterMaps",
#                 name="vray_mtl_filterMaps",
#                 description="",
#                 default= 0)

# BoolProperty(   attr="vray_geom_backfaceCull",
#                 name="vray_geom_backfaceCull",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_geom_displacement",
#                 name="vray_geom_displacement",
#                 description="",
#                 default= 1)
# BoolProperty(   attr="vray_geom_doHidden",
#                 name="vray_geom_doHidden",
#                 description="",
#                 default= 0)

# BoolProperty(   attr="vray_light_doShadows",
#                 name="vray_light_doShadows",
#                 description="",
#                 default= 1)

# BoolProperty(   attr="vray_light_doHiddenLights",
#                 name="vray_light_doHiddenLights",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_light_doLights",
#                 name="vray_light_doLights",
#                 description="",
#                 default= 1)

# FloatProperty(  attr="vray_ray_bias",
#                 name="vray_ray_bias",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=0.0)


'''
	SettingsRegionsGenerator
'''
EnumProperty(   attr="vray_rg_seqtype",
				name="Sequence type",
				description="Determines the order in which the regions are rendered.",
				items=(
					("HILBERT",   "Hilbert",   ""),
					("TRIANGLE",  "Triangulation",  "")
				),
				default= "TRIANGLE")

BoolProperty(   attr="vray_rg_reverse",
                name="Reverse",
                description="Reverses the region sequence order. ",
                default= 0)

EnumProperty(   attr="vray_rg_xymeans",
				name="XY means",
				description="XY means region width/height or region count.",
				items=(
					("SIZE",     "Region W/H",    ""),
					("BUCKETS",  "Region count",  "")
				),
				default= "SIZE")

IntProperty(    attr="vray_xc",
                name="X",
                description="Determines the maximum region width in pixels (Region W/H is selected) or the number of regions in the horizontal direction (when Region Count is selected)",
                min=1, max=100, default=32)

IntProperty(    attr="vray_yc",
                name="Y",
                description="Determines the maximum region height in pixels (Region W/H is selected) or the number of regions in the vertical direction (when Region Count is selected)",
                min=1, max=100, default=32)


'''
	SettingsDefaultDisplacement
'''
# BoolProperty(   attr="vray_displace_override_on",
#                 name="vray_displace_override_on",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_displace_relative",
#                 name="vray_displace_relative",
#                 description="",
#                 default= 0)
# BoolProperty(   attr="vray_displace_viewDependent",
#                 name="vray_displace_viewDependent",
#                 description="",
#                 default= 1)
# FloatProperty(  attr="vray_displace_edgeLength",
#                 name="vray_displace_edgeLength",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=4.0)
# FloatProperty(  attr="vray_displace_amount",
#                 name="vray_displace_amount",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=0.0100)
# IntProperty(    attr="vray_displace_maxSubdivs",
#                 name="vray_displace_maxSubdivs",
#                 description="",
#                 min=, max=, default=256)
# BoolProperty(   attr="vray_displace_tightBounds",
#                 name="vray_displace_tightBounds",
#                 description="",
#                 default= 1)


'''
	SettingsCaustics
'''
# BoolProperty(   attr="vray_caustics_on",
#                 name="vray_caustics_on",
#                 description="",
#                 default= 0)
# FloatProperty(  attr="vray_caustics_multiplier",
#                 name="vray_caustics_multiplier",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=1.0)
# IntProperty(    attr="vray_caustics_max_photons",
#                 name="vray_caustics_max_photons",
#                 description="",
#                 min=, max=, default=30)
# FloatProperty(  attr="vray_caustics_max_density",
#                 name="vray_caustics_max_density",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=0.0)
# FloatProperty(  attr="vray_caustics_search_distance",
#                 name="vray_caustics_search_distance",
#                 description="",
#                 min=, max=, soft_min=, soft_max=, default=0.05)



'''
	GUI
'''
narrowui= 200


class RENDER_CHANNELS_OT_add(bpy.types.Operator):
	bl_idname=      'render_channels.add'
	bl_label=       "Add Render Channel"
	bl_description= "Add render channel"

	def invoke(self, context, event):
		sce= context.scene
		vsce= sce.vray_scene

		render_channels= vsce.render_channels

		render_channels.add()
		render_channels[-1].name= "RenderChannel"

		return{'FINISHED'}


class RENDER_CHANNELS_OT_del(bpy.types.Operator):
	bl_idname=      'render_channels.remove'
	bl_label=       "Remove Render Channel"
	bl_description= "Remove render channel"

	def invoke(self, context, event):
		sce= context.scene
		vsce= sce.vray_scene
		
		render_channels= vsce.render_channels
		
		if vsce.render_channels_index >= 0:
		   render_channels.remove(vsce.render_channels_index)
		   vsce.render_channels_index-= 1

		return{'FINISHED'}


def base_poll(cls, context):
	rd= context.scene.render
	return (rd.use_game_engine == False) and (rd.engine in cls.COMPAT_ENGINES)


class RenderButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render'


class RENDER_PT_vray_dimensions(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Dimensions"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout = self.layout

		scene = context.scene
		rd = scene.render
		wide_ui = context.region.width > narrowui

		row = layout.row().split()
		sub = row.row(align=True).split(percentage=0.75)
		sub.menu("RENDER_MT_presets", text="Presets")
		sub.operator("render.preset_add", text="Add")

		split = layout.split()

		col = split.column()
		sub = col.column(align=True)
		sub.label(text="Resolution:")
		sub.prop(rd, "resolution_x", text="X")
		sub.prop(rd, "resolution_y", text="Y")
		sub.prop(rd, "resolution_percentage", text="")

		sub.label(text="Aspect Ratio:")
		sub.prop(rd, "pixel_aspect_x", text="X")
		sub.prop(rd, "pixel_aspect_y", text="Y")

		row = col.row()
		row.prop(rd, "use_border", text="Border")
		sub = row.row()
		sub.active = rd.use_border
		sub.prop(rd, "crop_to_border", text="Crop")

		if wide_ui:
			col = split.column()
		sub = col.column(align=True)
		sub.label(text="Frame Range:")
		sub.prop(scene, "frame_start", text="Start")
		sub.prop(scene, "frame_end", text="End")
		sub.prop(scene, "frame_step", text="Step")

		sub.label(text="Frame Rate:")
		sub.prop(rd, "fps")
		sub.prop(rd, "fps_base", text="/")


class RENDER_PT_vray_output(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Output"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout = self.layout

		rd = context.scene.render
		wide_ui = context.region.width > narrowui

		layout.prop(rd, "output_path", text="")

		split = layout.split()
		col = split.column()
		col.prop(rd, "file_format", text="")
		col.row().prop(rd, "color_mode", text="Color", expand=True)

		if wide_ui:
			col = split.column()
		col.prop(rd, "use_file_extension")
		col.prop(rd, "use_overwrite")
		col.prop(rd, "use_placeholder")

		if rd.file_format in ('AVIJPEG', 'JPEG'):
			split = layout.split()
			split.prop(rd, "file_quality", slider=True)

		elif rd.file_format == 'OPENEXR':
			split = layout.split()

			col = split.column()
			col.label(text="Codec:")
			col.prop(rd, "exr_codec", text="")

			if wide_ui:
				subsplit = split.split()
				col = subsplit.column()
			col.prop(rd, "exr_half")
			col.prop(rd, "exr_zbuf")

			if wide_ui:
				col = subsplit.column()
			col.prop(rd, "exr_preview")

		elif rd.file_format == 'JPEG2000':
			split = layout.split()
			col = split.column()
			col.label(text="Depth:")
			col.row().prop(rd, "jpeg2k_depth", expand=True)

			if wide_ui:
				col = split.column()
			col.prop(rd, "jpeg2k_preset", text="")
			col.prop(rd, "jpeg2k_ycc")

		elif rd.file_format in ('CINEON', 'DPX'):
			split = layout.split()
			col = split.column()
			col.prop(rd, "cineon_log", text="Convert to Log")

			if wide_ui:
				col = split.column(align=True)
			col.active = rd.cineon_log
			col.prop(rd, "cineon_black", text="Black")
			col.prop(rd, "cineon_white", text="White")
			col.prop(rd, "cineon_gamma", text="Gamma")

		elif rd.file_format == 'TIFF':
			split = layout.split()
			split.prop(rd, "tiff_bit")

		elif rd.file_format == 'QUICKTIME_CARBON':
			split = layout.split()
			split.operator("scene.render_set_quicktime_codec")

		elif rd.file_format == 'QUICKTIME_QTKIT':
			split = layout.split()
			col = split.column()
			col.prop(rd, "quicktime_codec_type")
			col.prop(rd, "quicktime_codec_spatial_quality", text="Quality")


class RENDER_PT_vray_render(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Render"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray_scene
		ve= vs.exporter

		split= layout.split()
		col= split.column()
		col.operator("render.render", text="Image", icon='RENDER_STILL')

		if not ve.auto_meshes:
			if wide_ui:
				col= split.column()
			col.operator("vray_export_meshes", icon='OUTLINER_OB_MESH')

		split= layout.split()
		col= split.column()
		col.label(text="Globals:")
		col.prop(vs, "enable_gi", text="GI")
		col.prop(vs, "enable_caustics", text="Caustics")
		if wide_ui:
			col= split.column()
		col.label(text="Pipeline:")
		col.prop(ve, 'animation')
		col.prop(ve, 'active_layers')
		col.prop(ve, 'use_material_nodes')
		col.prop(ve, 'image_to_blender')

		split= layout.split()
		col= split.column()
		col.label(text="Exporter:")
		col.prop(ve, "autorun")
		col.prop(ve, "auto_meshes")
		col.prop(ve, "debug")



class RENDER_PT_vray_cm(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Color mapping"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		scene= context.scene.vray_scene
		rd= context.scene.render
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop(scene, "vray_cm_type", text="Type")
		if(scene.vray_cm_type == 'REIN'):
			col.prop(scene, "vray_dark_mult", text="Multiplier")
			col.prop(scene, "vray_bright_mult",  text="Burn")
		elif(scene.vray_cm_type in ('GCOR', 'GINT')):
			col.prop(scene, "vray_bright_mult", text="Multiplier")
			col.prop(scene, "vray_dark_mult", text="Inverse gamma")
		else:
			col.prop(scene, "vray_bright_mult")
			col.prop(scene, "vray_dark_mult")
		col.prop(scene, "vray_gamma")

		if(wide_ui):
			col= split.column()
		col.prop(scene, "vray_affect_background")
		col.prop(scene, "vray_subpixel_mapping")
		col.prop(scene, "vray_adaptation_only")
		col.prop(scene, "vray_linearWorkflow")
		col.prop(scene, "vray_clamp_output")
		if(scene.vray_clamp_output):
			col.prop(scene, "vray_clamp_level")



class RENDER_PT_vray_aa(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Image sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		colL= split.column()
		colL.prop(scene, "vray_is_type", text="Type")

		split= layout.split()
		colL= split.column()
		colL.label(text="Parameters:")

		split= layout.split()
		colL= split.column()

		if(scene.vray_is_type == 'FXD'):
			colL.prop(scene, "vray_fixed_subdivs")
		elif(scene.vray_is_type == 'DMC'):
			colL.prop(scene, "vray_dmc_minSubdivs")
			colL.prop(scene, "vray_dmc_maxSubdivs")

			colR= split.column()
			colR.prop(scene, "vray_dmc_treshhold_use_dmc", text= "Use DMC sampler thresh.")
			if(not scene.vray_dmc_treshhold_use_dmc):
				colR.prop(scene, "vray_dmc_threshold")
			colR.prop(scene, "vray_dmc_show_samples")
		else:
			colL.prop(scene, "vray_subdivision_minRate")
			colL.prop(scene, "vray_subdivision_maxRate")
			colL.prop(scene, "vray_subdivision_threshold")

			colR= split.column()
			colR.prop(scene, "vray_subdivision_edges")
			colR.prop(scene, "vray_subdivision_normals")
			if(scene.vray_subdivision_normals):
				colR.prop(scene, "vray_subdivision_normals_threshold")
			colR.prop(scene, "vray_subdivision_jitter")
			colR.prop(scene, "vray_subdivision_show_samples")

		split= layout.split()
		colL= split.column()
		colR= split.column()
		colL.label(text="Filter type:")
		colR.prop(scene, "vray_filter_type", text="")
		if(not scene.vray_filter_type == 'NONE'):
			colR.prop(scene, "vray_filter_size")


class RENDER_PT_vray_dmc(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "DMC Sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		col= split.column()
		col.prop(scene, "vray_adaptive_threshold")
		col.prop(scene, "vray_subdivs_mult")
		col.prop(scene, "vray_time_dependent")

		if wide_ui:
			col= split.column()
		col.prop(scene, "vray_adaptive_amount")
		col.prop(scene, "vray_adaptive_min_samples")


class RENDER_PT_vray_gi(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Global Illumination"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		vs= context.scene.vray_scene
		return (base_poll(__class__, context) and vs.enable_gi)

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		colL= split.column()
		colL.label(text="GI caustics:")
		sub= colL.column()
		sub.prop(scene, "vray_gi_reflect_caustics", text="Reflect")
		sub.prop(scene, "vray_gi_refract_caustics", text="Refract")

		colR= split.column()
		colR.label(text="Post-processing:")
		sub= colR.column()
		sub.prop(scene, "vray_gi_saturation")
		sub.prop(scene, "vray_gi_contrast")
		sub.prop(scene, "vray_gi_contrast_base")

		layout.label(text="Primary engine:")
		split= layout.split(percentage=0.35)
		colL= split.column()
		colL.prop(scene, "vray_gi_primary_multiplier", text="Mult")
		colR= split.column()
		colR.prop(scene, "vray_gi_primary_engine", text="")

		layout.label(text="Secondary engine:")
		split= layout.split(percentage=0.35)
		colL= split.column()
		colL.prop(scene, "vray_gi_secondary_multiplier", text="Mult")
		colR= split.column()
		colR.prop(scene, "vray_gi_secondary_engine", text="")


class RENDER_PT_vray_gi_im(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Irradiance Map"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		scene= context.scene.vray_scene
		return (base_poll(__class__, context) and scene.enable_gi and scene.vray_gi_primary_engine == 'IM')

	def draw(self, context):
		layout= self.layout
		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		colR= split.column()
		colR.prop(scene, "vray_im_mode", text="Mode")

		if scene.vray_im_mode not in ('FILE', 'ANIM_REND'):
			split= layout.split()
			split.column().prop(scene, "vray_im_preset")

			if scene.vray_im_preset == 'SALUTO':
				split= layout.split()
				split.column().label(text="Please, refer to http://saluto.blogspot.com/ for more info.")

			split= layout.split()
			split.label(text="Basic parameters:")

			split= layout.split()
			colL= split.column(align=True)
			colL.prop(scene,"vray_im_min_rate")
			colL.prop(scene,"vray_im_max_rate")
			colL.prop(scene,"vray_im_subdivs", text= "HSph. subdivs")
			colM= split.column(align=True)
			colM.prop(scene,"vray_im_color_threshold", text="Clr thresh", slider=True)
			colM.prop(scene,"vray_im_normal_threshold", text="Nrm thresh", slider=True)
			colM.prop(scene,"vray_im_distance_threshold", text="Dist thresh", slider=True)

			split= layout.split()
			split.column().prop(scene,"vray_im_interp_samples", text= "Interp. samples")
			split.column()

			split= layout.split()
			split.label(text="Advanced parameters:")

			split= layout.split(percentage=0.7)
			colL= split.column()
			colL.prop(scene,"vray_im_interpolationType", text="Interp. type")
			colL.prop(scene,"vray_im_lookupType")
			colL.prop(scene,"vray_im_calc_interp_samples")
			colR= split.column()
			colR.prop(scene,"vray_im_multipass")
			colR.prop(scene,"vray_im_randomize_samples", text="Randomize")
			colR.prop(scene,"vray_im_check_sample_visibility", text="Check sample")

		elif scene.vray_im_mode == 'ANIM_REND':
			split= layout.split()
			split.label(text="Basic parameters:")

			split= layout.split()
			colL= split.column()
			colL.prop(scene,"vray_im_interp_frames")

		split= layout.split()
		split.label(text="Detail enhancement:")

		split= layout.split(percentage=0.12)
		split.column().prop(scene, "vray_im_detail_enhancement", text="On")
		sub= split.column().row()
		sub.active= scene.vray_im_detail_enhancement
		sub.prop(scene, "vray_im_detail_radius", text="R")
		sub.prop(scene, "vray_im_detail_subdivs_mult", text="Subdivs", slider=True)
		sub.prop(scene, "vray_im_detail_scale", text="")

		if scene.vray_im_mode not in ('FILE', 'ANIM_REND'):
			split= layout.split()
			split.label(text="Options:")
			row= layout.split().row()
			row.prop(scene,"vray_im_show_calc_phase")
			sub= row.column().row()
			sub.active= scene.vray_im_show_calc_phase
			sub.prop(scene,"vray_im_show_direct_light")
			sub.prop(scene,"vray_im_show_samples")
			sub.prop(scene,"vray_im_multiple_views", text="Camera path")

		split= layout.split()
		split.label(text="Files:")
		split= layout.split(percentage=0.25)
		colL= split.column()
		colR= split.column()
		if scene.vray_im_mode in ('FILE', 'ANIM_REND'):
			colL.label(text="Map file name:")
			colR.prop(scene,"vray_im_file", text="")
		else:
			colL.prop(scene,"vray_im_auto_save", text="Auto save")
			colR.active= scene.vray_im_auto_save
			colR.prop(scene,"vray_im_auto_save_file", text="")


class RENDER_PT_vray_gi_bf(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Brute Force"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		scene= context.scene.vray_scene
		return (base_poll(__class__, context) and scene.enable_gi and (scene.vray_gi_primary_engine == 'BF' or scene.vray_gi_secondary_engine == 'BF'))

	def draw(self, context):
		layout= self.layout
		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		split.column().prop(scene, "vray_dmcgi_subdivs")
		if scene.vray_gi_secondary_engine == 'BF':
			split.column().prop(scene, "vray_dmcgi_depth")


class RENDER_PT_vray_gi_lc(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Light Cache"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		scene= context.scene.vray_scene
		return (base_poll(__class__, context) and scene.enable_gi and (scene.vray_gi_primary_engine == 'LC' or scene.vray_gi_secondary_engine == 'LC'))

	def draw(self, context):
		layout= self.layout
		scene= context.scene.vray_scene
		rd= context.scene.render

		split= layout.split()
		colR= split.column()
		colR.prop(scene, "vray_lc_mode", text="Mode")

		if not scene.vray_lc_mode == 'FILE':
			layout.label(text="Calculation parameters:")
			split= layout.split(percentage=0.6)
			colL= split.column()
			colL.prop(scene, "vray_lc_subdivs")
			colL.prop(scene, "vray_lc_sample_size")
			colL.prop(scene, "vray_lc_scale", text="Sample scale")
			if not scene.vray_lc_num_passes_auto:
				colL.prop(scene, "vray_lc_num_passes")
			colL.prop(scene, "vray_lc_depth", slider= True)
			colR= split.column()
			colR.prop(scene, "vray_lc_store_direct_light")
			colR.prop(scene, "vray_lc_adaptive_sampling")
			colR.prop(scene, "vray_lc_show_calc_phase")
			colR.prop(scene, "vray_lc_num_passes_auto")

		layout.label(text="Reconstruction parameters:")
		if not scene.vray_lc_mode == 'FILE':
			split= layout.split(percentage=0.2)
			split.column().prop(scene, "vray_lc_filter")
			sub= split.column().row()
			sub.active= scene.vray_lc_filter
			sub.prop(scene, "vray_lc_filter_type", text="Type")
			if scene.vray_lc_filter_type == 'NEAREST':
				sub.prop(scene, "vray_lc_filter_samples")
			else:
				sub.prop(scene, "vray_lc_filter_size")

		split= layout.split(percentage=0.2)
		split.column().prop(scene, "vray_lc_prefilter")
		colR= split.column()
		colR.active= scene.vray_lc_prefilter
		colR.prop(scene, "vray_lc_prefilter_samples")

		split= layout.split()
		split.column().prop(scene, "vray_lc_use_for_glossy_rays")
		split.column().prop(scene, "vray_lc_multiple_views")

		split= layout.split()
		split.label(text="Files:")
		split= layout.split(percentage=0.25)
		colL= split.column()
		colR= split.column()
		if scene.vray_lc_mode == 'FILE':
			colL.label(text="Map file name:")
			colR.prop(scene,"vray_lc_file", text="")
		else:
			colL.prop(scene,"vray_lc_auto_save", text="Auto save")
			colR.active= scene.vray_lc_auto_save
			colR.prop(scene,"vray_lc_auto_save_file", text="")


class RENDER_PT_vray_Layers(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Channels"
	bl_default_closed = True

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui = context.region.width > narrowui
		layout= self.layout
		
		sce= context.scene
		vsce= sce.vray_scene

		render_channels= vsce.render_channels

		split= layout.split()
		row= split.row()
		row.template_list(vsce, 'render_channels', vsce, 'render_channels_index', rows= 3)
		col= row.column(align=True)
		col.operator('render_channels.add',    text="", icon="ZOOMIN")
		col.operator('render_channels.remove', text="", icon="ZOOMOUT")

		if vsce.render_channels_index >= 0 and len(render_channels) > 0:
			render_channel= render_channels[vsce.render_channels_index]
		
			layout.separator()

			layout.prop(render_channel, 'name')
			layout.prop(render_channel, 'type', text="Type")

			layout.separator()

			if render_channel.type != 'NONE':
				plugin= get_plugin(CHANNEL_PLUGINS, render_channel.type)
				if plugin is not None:
					render_channel_data= getattr(render_channel,plugin.PLUG)

					if render_channel.name == "" or render_channel.name == "RenderChannel":
						def get_unique_name():
							for chan in render_channels:
								if render_channel_data.name == chan.name:
									return render_channel_data.name + " (enter unique name)"
							return render_channel_data.name
						render_channel.name= get_unique_name()
					
					plugin.draw(getattr(render_channel,plugin.PLUG), layout, wide_ui)


class RENDER_PT_vray_about(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "About"
	bl_default_closed = True

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		split= layout.split()
		col= split.column()
		col.label(text="V-Ray/Blender 2.5 (git)")
		col.separator()
		col.label(text="Author: Andrey M. Izrantsev")
		col.label(text="URL: http://vray.cgdo.ru")
		col.label(text="Email: izrantsev@gmail.com")
		col.separator()
		col.label(text="IRC: irc.freenode.net #vrayblender")
		col.separator()
		col.label(text="V-Ray(R) is a registered trademark of Chaos Group Ltd.")


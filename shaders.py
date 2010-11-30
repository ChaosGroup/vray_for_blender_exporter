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


''' Blender modules '''
import bpy

''' vb modules '''
from vb25.utils import *


MODULES= {
	'SettingsRaycaster': (
		'maxLevels',
		'minLeafSize',
		'faceLevelCoef',
		'dynMemLimit',
	),
	
	'SettingsUnitsInfo': (
		'meters_scale',
		'photometric_scale'
	),

	'SettingsDMCSampler': (
		'time_dependent',
		'adaptive_amount',
		'adaptive_threshold',
		'adaptive_min_samples',
		'subdivs_mult'
	),

	'SettingsImageSampler': (
		'fixed_subdivs',
		'dmc_minSubdivs',
		'dmc_threshold',
		'dmc_show_samples',
		'subdivision_minRate',
		'subdivision_maxRate',
		'subdivision_threshold',
		'subdivision_edges',
		'subdivision_normals',
		'subdivision_normals_threshold',
		'subdivision_jitter',
		'subdivision_show_samples'
	),

	'SettingsColorMapping': (
		'affect_background',
		'dark_mult',
		'bright_mult',
		'gamma',
		'subpixel_mapping',
		'clamp_output',
		'clamp_level',
		'adaptation_only',
		'linearWorkflow'
	),

	'SettingsDefaultDisplacement': (
		'override_on',
		'edgeLength',
		'viewDependent',
		'maxSubdivs',
		'tightBounds',
		'amount',
		'relative'
	),
	
	'SettingsRegionsGenerator': (
        'xc',
        'yc',
        # 'xymeans',
        # 'seqtype',
        'reverse'
	)
}

OBJECT_PARAMS= {
	'GeomDisplacedMesh': (
		'displacement_amount',
		'displacement_shift',
		'water_level',
        'use_globals',
        'view_dep',
        'edge_length',
        'max_subdivs',
        'keep_continuity',
        'map_channel',
        'use_bounds',
        'min_bound',
        'max_bound',
        'resolution',
        'precision',
        'tight_bounds',
        'filter_texture',
        'filter_blur'
	),
	'EnvironmentFog': (
		#'gizmos',
		'emission',
		#'emission_tex',
		'color',
		#'color_tex',
		'distance',
		'density',
		#'density_tex',
		'use_height',
		'height',
		'subdivs',
		'affect_background',
		'yup',
		'fade_out_radius',
		'per_object_fade_out_radius',
		'use_fade_out_tex',
		#'fade_out_tex',
		'edge_fade_out',
		'fade_out_type',
		'scatter_gi',
		'scatter_bounces',
		'simplify_gi',
		'step_size',
		'max_steps',
		'tex_samples',
		'cutoff_threshold',
		'light_mode',
		#'lights',
		'use_shade_instance'
	),
	
	'BRDFSSS2Complex': (
		'prepass_rate',
		'interpolation_accuracy',
		'scale',
		'ior',
		#'overall_color',
		#'diffuse_color',
		#'diffuse_amount',
		#'sub_surface_color',
		#'scatter_radius',
		'scatter_radius_mult',
		'phase_function',
		#'specular_color',
		#'specular_amount',
		#'specular_glossiness',
		'specular_subdivs',
		'cutoff_threshold',
		'trace_reflections',
		'reflection_depth',
		#'single_scatter',
		'subdivs',
		'refraction_depth',
		'front_scatter',
		'back_scatter',
		'scatter_gi',
		'prepass_blur'
		#'channels'
	),

	'BRDFVRayMtl': (
		# 'opacity',
		# 'diffuse',
		# 'roughness',
		## 'brdf_type',
		# 'reflect',
		# 'reflect_glossiness',
		# 'hilight_glossiness',
		'hilight_glossiness_lock',
		'fresnel',
		'fresnel_ior',
		'fresnel_ior_lock',
		'reflect_subdivs',
		'reflect_trace',
		'reflect_depth',
		'reflect_exit_color',
		'hilight_soften',
		# 'reflect_dim_distance',
		'reflect_dim_distance_on',
		'reflect_dim_distance_falloff',
		'anisotropy',
		'anisotropy_rotation',
		'anisotropy_derivation',
		'anisotropy_axis',
		# 'anisotropy_uvwgen',
		# 'refract',
		'refract_ior',
		'refract_glossiness',
		'refract_subdivs',
		'refract_trace',
		'refract_depth',
		'refract_exit_color',
		'refract_exit_color_on',
		'refract_affect_alpha',
		'refract_affect_shadows',
		'fog_color',
		'fog_mult',
		'fog_bias',
		'fog_unit_scale_on',
		'translucency',
		# 'translucency_color',
		'translucency_light_mult',
		'translucency_scatter_dir',
		'translucency_scatter_coeff',
		'translucency_thickness',
		'option_double_sided',
		'option_reflect_on_back',
		'option_glossy_rays_as_gi',
		'option_cutoff',
		'option_use_irradiance_map',
		'option_energy_mode',
		# 'environment_override',
		'environment_priority',
	),
	
	'CameraPhysical': (
		'film_width',
		'focal_length',
		'zoom_factor',
		'distortion',
		'distortion_type',
		'f_number',
		'lens_shift',
		'shutter_speed',
		'shutter_angle',
		'shutter_offset',
		'latency',
		'ISO',
		'dof_display_threshold',
		'exposure',
		'vignetting',
		'blades_enable',
		'blades_num',
		'blades_rotation',
		'center_bias',
		'anisotropy',
		'use_dof',
		'use_moblur',
		'subdivs'
		#'lens_file',
		#'horizontal_shift'
	),

	'LightOmni': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		#'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		'decay'
	),

	'LightSphere': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		'noDecay',
		'radius',
		'sphere_segments'
	),

	'LightRectangle': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		#'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		'noDecay'
	),

	'LightDirect': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		'intensity',
		#'intensity_tex',
		'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		'beamRadius'
	),

	'SunLight': (
		'turbidity',
		'ozone',
		'water_vapour',
		'intensity_multiplier',
		'size_multiplier',
		#'up_vector',
		'invisible',
		'horiz_illum',
		#'sky_model',
		'shadows',
		#'atmos_shadows',
		'shadowBias',
		'shadow_subdivs',
		'shadow_color',
		#'shadow_color_tex',
		#'photon_radius',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'enabled'
	),	

	'LightIES': (
		'enabled',
		'intensity',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		'shadowSubdivs',
		'ies_file',
		#'filter_color',
		'soft_shadows',
		#'area_speculars'
	),

	'LightDome': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		#'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'channels',
		#'channels_raw',
		#'channels_diffuse',
		#'channels_specular',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		#'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		#'dome_tex',
		#'use_dome_tex',
		#'tex_resolution',
		#'dome_targetRadius',
		#'dome_emitRadius',
		#'dome_spherical',
		#'tex_adaptive',
		#'dome_rayDistance',
		#'dome_rayDistanceMode',
	),

	'LightSpot': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		#'coneAngle',
		#'penumbraAngle',
		#'dropOff',
		#'falloffType',
		'decay',
		#'barnDoor',
		#'barnDoorLeft',
		#'barnDoorRight',
		#'barnDoorTop',
		#'barnDoorBottom',
		#'useDecayRegions',
		#'startDistance1',
		#'endDistance1',
		#'startDistance2',
		#'endDistance2',
		#'startDistance3',
		#'endDistance3'
	),

	'LightMesh': (
		'enabled',
		# 'transform',
		'color',
		# 'color_tex',
		# 'shadows',
		# 'shadowColor',
		# 'shadowColor_tex',
		# 'shadowBias',
		# 'photonSubdivs',
		'causticSubdivs',
		# 'diffuseMult',
		# 'causticMult',
		# 'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		# 'bumped_below_surface_check',
		# 'nsamples',
		# 'diffuse_contribution',
		# 'specular_contribution',
		# 'channels',
		# 'channels_raw',
		# 'channels_diffuse',
		# 'channels_specular',
		'units',
		'intensity',
		# 'intensity_tex',
		'subdivs',
		'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		'noDecay',
		'doubleSided',
		'lightPortal',
		'geometry',
		# 'ignoreLightNormals',
		# 'tex',
		# 'use_tex',
		# 'tex_resolution',
		# 'cache_tex'
	),

	'TexSky': (
		#'transform',
		#'target_transform',
		'turbidity',
		'ozone',
		'water_vapour',
		'intensity_multiplier',
		'size_multiplier',
		#'up_vector',
		'invisible',
		'horiz_illum',
		'sky_model',
		'sun'
	),

	'MtlWrapper': (
		#'base_material',
		'generate_gi',
		'receive_gi',
		'generate_caustics',
		'receive_caustics',
		'alpha_contribution',
		'matte_surface',
		'shadows',
		'affect_alpha',
		'shadow_tint_color',
		'shadow_brightness',
		'reflection_amount',
		'refraction_amount',
		'gi_amount',
		'no_gi_on_other_mattes',
		'matte_for_secondary_rays',
		'gi_surface_id',
		'gi_quality_multiplier',
		#'alpha_contribution_tex',
		#'shadow_brightness_tex',
		#'reflection_filter_tex',
		'trace_depth',
		#'channels'
	),

	'MtlRenderStats': (
		'camera_visibility',
		'reflections_visibility',
		'refractions_visibility',
		'gi_visibility',
		'shadows_visibility',
		'visibility'
	)
}

TEX_TYPES= ('IMAGE', 'VRAY')

UNITS= {
	'DEFAULT' : 0,
	'LUMENS'  : 1,
	'LUMM'    : 2,
	'WATTSM'  : 3,
	'WATM'    : 4
}

LIGHT_PORTAL= {
	'NORMAL':  0,
	'PORTAL':  1,
	'SPORTAL': 2
}

SKY_MODEL= {
	'CIEOVER'  : 2,
	'CIECLEAR' : 1,
	'PREETH'   : 0
}

PROXY_ANIM_TYPE= {
	'LOOP'     : 0,
	'ONCE'     : 1,
	'PINGPONG' : 2,
	'STILL'    : 3
}

AA_FILTER_TYPE= {
	'AREA'     : '\nFilterArea {',
	'BOX'      : '\nFilterBox {',
	'TRIANGLE' : '\nFilterTriangle {',
	'LANC'     : '\nFilterLanczos {',
	'SINC'     : '\nFilterSinc {',
	'GAUSS'    : '\nFilterGaussian {',
	'CATMULL'  : '\nFilterCatmullRom {'
}

PHYS= {
	"STILL":     0,
	"CINEMATIC": 1,
	"VIDEO":     2
}

SEQTYPE= {
	'HILBERT':   5,
	'TRIANGLE':  4,
	'IOSPIRAL':  3,
	'TBCHECKER': 2,
	'LRWIPE':    1,
	'TBWIPE':    0
}

XYMEANS= {
	'BUCKETS': 1,
	'SIZE':    0
}

COLOR_MAPPING_TYPE= {
	'LNR':  0,
	'EXP':  1,
	'HSV':  2,
	'INT':  3,
	'GCOR': 4,
	'GINT': 5,
	'REIN': 6
}

IMAGE_SAMPLER_TYPE= {
	'FXD': 0,
	'DMC': 1,
	'SBD': 2
}

PRIMARY= {
	"IM":  0,
	"PM":  1,
	"BF":  2,
	"LC":  3
}

SECONDARY= {
	"NONE":  0,
	"PM":    1,
	"BF":    2,
	"LC":    3
}

SCALE= {
	"SCREEN":  0,
	"WORLD":   1
}

IM_MODE= {
	"SINGLE":    0,
	"INC":       1,
	"FILE":      2,
	"ADD":       3,
	"ADD_INC":   4,
	"BUCKET":    5,
	"ANIM_PRE":  6,
	"ANIM_REND": 7
}

INT_MODE= {
	"VORONOI":   0,
	"LEAST":     1,
	"DELONE":    2,
	"WEIGHTED":  3
}

LOOK_TYPE= {
	"QUAD":     0,
	"NEAREST":  1,
	"OVERLAP":  2,
	"DENSITY":  3
}

LC_FILT= {
	"NEAREST": 0,
	"FIXED":   1
}

LC_MODE= {
	"SINGLE":  0,
	"FILE":    1,
	"FLY":     2,
	"PPT":     3
}

BRDF_TYPE= {
	'PHONG': 0,
	'BLINN': 1,
	'WARD':  2
}

TRANSLUCENSY= {
	"HYBRID": 3,
	"SOFT":   2,
	"HARD":   1,
	"NONE":   0
}

GLOSSY_RAYS= {
	'ALWAYS': 2,
	'GI':     1,
	'NEVER':  0
}

ENERGY_MODE= {
	'MONO':  1,
	'COLOR': 0
}

# BLEND_TYPE= {
# 	'MIX':          0,
# 	'ADD':          4,
# 	'SUBTRACT':     5,
# 	'MULTIPLY':     6,
# 	'SCREEN':       0,
# 	'OVERLAY':      1,
# 	'DIFFERENCE':   7,
# 	'DIVIDE':       0,
# 	'DARKEN':       9,
# 	'LIGHTEN':      8,
# 	'HUE':          0,
# 	'SATURATION':  10,
# 	'VALUE':        0,
# 	'COLOR':        0,
# 	'SOFT LIGHT':   0,
# 	'LINEAR LIGHT': 0
# }

BLEND_MODES= {
	'NONE':         '0',
	'STENCIL':      '1',

	'OVER':         '1',
	'IN':           '2',
	'OUT':          '3',
	'ADD':          '4',
	'SUBSTRACT':    '5',
	'MULTIPLY':     '6',
	'DIFFERENCE':   '7',
	'LIGHTEN':      '8',
	'DARKEN':       '9',
	'SATURATE':    '10',
	'DESATUREATE': '11',
	'ILLUMINATE':  '12',
}


def multiply_texture(ofile,sce, input_texture_name, mult_value, suffix= None):
	if mult_value == 1.0:
		return input_texture_name

	# tex_name= "TexMult_%s" % input_texture_name
	# if suffix:
	# 	tex_name+= suffix
	tex_name= get_random_string()
		
	ofile.write("\nTexAColorOp %s {" % tex_name)
	ofile.write("\n\tcolor_a= %s;" % input_texture_name)
	if mult_value > 1.0:
		ofile.write("\n\tmult_a= %s;" % a(sce,mult_value))
	else:
		ofile.write("\n\tmult_a= 1.0;")
		ofile.write("\n\tresult_alpha= %s;" % a(sce,mult_value))
	ofile.write("\n}\n")
				
	return tex_name


def stencil_texture(ofile,sce, textureA, textureB, mode, factor, name= None):
	tex_name= "Stencil_%s_%s" % (textureA, textureB)
	if name:
		tex_name= name
	
	ofile.write("\nTexBlend %s {" % tex_name)
	ofile.write("\n\tcolor_a= %s;" % textureA)
	ofile.write("\n\tcolor_b= %s;" % textureB)
	ofile.write("\n\tblend_amount= %s::out_intensity;"%(texlayered_names[stencil]))
	ofile.write("\n\tcomposite= %d;"%(0))
	ofile.write("\n}\n")

	return tex_name


def blend_texture(ofile,sce, textureA, textureB, mode, factor):
	tex_name= "stackmix_%s"%(tex)
	
	ofile.write("\nTexLayered stackmix_a_%s {"%(tex))
	ofile.write("\n\ttextures= List(%s,%s);"%(color1,color2))
	ofile.write("\n\tblend_modes= List(1,%s);"%(mode))
	ofile.write("\n}\n")
	ofile.write("\nTexMix stackmix_%s {"%(tex))
	ofile.write("\n\tcolor2= stackmix_a_%s;"%(tex))
	ofile.write("\n\tcolor1= %s;"%(color1))
	ofile.write("\n\tmix_amount= %s;"%(factor))
	ofile.write("\n}\n")
		
	return tex_name


def write_TexAColorOp(ofile, sce, tex, mult, tex_name= None):
	brdf_name= "TexAColorOp_%s"%(tex_name if tex_name else tex)

	ofile.write("\nTexAColorOp %s {"%(brdf_name))
	ofile.write("\n\tcolor_a= %s;"%(a(sce,tex)))
	ofile.write("\n\tmult_a= %s;"%(a(sce,mult)))
	ofile.write("\n}\n")

	return brdf_name


def write_TexInvert(ofile, tex):
	tex_name= "TexInvert_%s"%(tex)

	ofile.write("\nTexInvert %s {"%(tex_name))
	ofile.write("\n\ttexture= %s;"%(tex))
	ofile.write("\n}\n")

	return tex_name


def write_TexCompMax(ofile, name, sourceA, sourceB, operator):
	OPERATOR= {
		'Add':        0,
		'Substract':  1,
		'Difference': 2,
		'Multiply':   3,
		'Divide':     4,
		'Minimum':    5,
		'Maximum':    6
	}

	tex_name= "TexCompMax_%s"%(name)

	ofile.write("\nTexCompMax %s {"%(tex_name))
	ofile.write("\n\tsourceA= %s;"%(sourceA))
	ofile.write("\n\tsourceB= %s;"%(sourceB))
	ofile.write("\n\toperator= %d;"%(OPERATOR[operator]))
	ofile.write("\n}\n")

	return tex_name


def write_TexFresnel(ofile, sce, ma, ma_name, tex_vray):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {"%(tex_name))
	if tex_vray["reflect"]:
		ofile.write("\n\tblack_color= %s;"%(tex_vray["reflect"]))
	else:
		ofile.write("\n\tblack_color= %s;"%(a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior)))
	ofile.write("\n}\n")

	return tex_name


def write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray):
	rm= ma.raytrace_mirror

	brdf_name= "BRDFMirror_%s"%(ma_name)

	ofile.write("\nBRDFMirror %s {"%(brdf_name))
	if(tex_vray['color']):
		ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	if(tex_vray['reflect']):
		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tback_side= %d;"%(ma.vray_back_side))
	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
	ofile.write("\n\ttrace_depth= %i;"%(rm.depth))
	ofile.write("\n\tcutoff= %.6f;"%(0.01))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray):
	rm= ma.raytrace_mirror

	brdf_name= "BRDFGlossy_%s"%(ma_name)

	if(ma.vray_brdf == 'PHONG'):
		ofile.write("\nBRDFPhong %s {"%(brdf_name))
	elif(ma.vray_brdf == 'WARD'):
		ofile.write("\nBRDFWard %s {"%(brdf_name))
	else:
		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_reflect_color)))))
	ofile.write("\n\tsubdivs= %i;"%(rm.gloss_samples))

	if(tex_vray['reflect']):
		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(
			1.0 - ma.vray_reflect_color[0],
			1.0 - ma.vray_reflect_color[1],
			1.0 - ma.vray_reflect_color[2]))))

	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,rm.gloss_factor)))
	ofile.write("\n\thilightGlossiness= %s;"%(a(sce,ma.vray_hilightGlossiness)))
	if(tex_vray['reflect_glossiness']):
		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['reflect_glossiness'])))
	if(tex_vray['hilight_glossiness']):
		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['hilight_glossiness'])))
	ofile.write("\n\tback_side= %s;"%(a(sce,ma.vray_back_side)))
	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rm.depth)))
	if(not ma.vray_brdf == 'PHONG'):
		ofile.write("\n\tanisotropy= %s;"%(a(sce,ma.vray_anisotropy)))
		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,ma.vray_anisotropy_rotation)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,rm.gloss_threshold)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlass_%s"%(ma_name)

	ofile.write("\nBRDFGlass %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlassGlossy_%s"%(ma_name)

	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tglossiness= %s;"%(a(sce,rt.gloss_factor)))
	ofile.write("\n\tsubdivs= %i;"%(rt.gloss_samples))
	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray):
	brdf_name= "BRDFDiffuse_%s"%(ma_name)

	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	ofile.write("\n\troughness= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(ma.vray_roughness,ma.vray_roughness,ma.vray_roughness))))
	if(tex_vray['color']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['color']))
	ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency_tex= %s;"%(a(sce,tex_vray['alpha'])))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDF(ofile, sce, ma, ma_name, tex_vray):
	def bool_color(color, level):
		for c in color:
			if c > level:
				return True
		return False

	rm= ma.raytrace_mirror
	rt= ma.raytrace_transparency

	brdfs= []

	if(tex_vray['reflect']):
		tex_vray['reflect']= write_TexInvert(tex_vray['reflect'])

	if(ma.vray_fresnel):
		tex_vray['reflect']= write_TexFresnel(ofile, sce, ma, ma_name, tex_vray)

	if(tex_vray['reflect'] or bool_color(ma.vray_reflect_color, 0.0)):
		if(rm.gloss_factor < 1.0 or tex_vray['reflect_glossiness']):
			brdf_name= write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray)
		brdfs.append(brdf_name)

	if(tex_vray['refract'] or bool_color(ma.vray_refract_color, 0.0)):
		if(rt.gloss_factor < 1.0 or tex_vray['refract_glossiness']):
			brdf_name= write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray)
	else:
		brdf_name= write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray)
	brdfs.append(brdf_name)

	if(len(brdfs) == 1):
		brdf_name= brdfs[0]
	else:
		brdf_name= "BRDFLayered_%s"%(ma_name)

		ofile.write("\nBRDFLayered %s {"%(brdf_name))
		ofile.write("\n\tbrdfs= List(")
		brdfs_out= ""
		for brdf in brdfs:
			brdfs_out+= "\n\t\t%s,"%(brdf)
		ofile.write(brdfs_out[0:-1])
		ofile.write("\n\t);")
		ofile.write("\n\tadditive_mode= %s;"%(0)); # For shellac
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
		if(tex_vray['alpha']):
			ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['alpha']))
		ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFGlossy_%s"%(ma_name)

	if BRDFVRayMtl.brdf_type == 'PHONG':
		ofile.write("\nBRDFPhong %s {"%(brdf_name))
	elif BRDFVRayMtl.brdf_type == 'WARD':
		ofile.write("\nBRDFWard %s {"%(brdf_name))
	else:
		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	ofile.write("\n\tsubdivs= %i;"%(BRDFVRayMtl.reflect_subdivs))

	if tex_vray['reflect']:
		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))

	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	if BRDFVRayMtl.hilight_glossiness_lock:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	else:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.hilight_glossiness)))
	if tex_vray['reflect_glossiness']:
		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['reflect_glossiness'])))
	if tex_vray['hilight_glossiness']:
		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['hilight_glossiness'])))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	if BRDFVRayMtl.brdf_type != 'PHONG':
		ofile.write("\n\tanisotropy= %s;"%(a(sce,BRDFVRayMtl.anisotropy)))
		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,BRDFVRayMtl.anisotropy_rotation)))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFMirror_%s"%(ma_name)

	ofile.write("\nBRDFMirror %s {"%(brdf_name))
	if tex_vray['color']:
		ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	if tex_vray['reflect']:
		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFGlass_%s"%(ma_name)

	ofile.write("\nBRDFGlass %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tior= %s;"%(a(sce,BRDFVRayMtl.refract_ior)))
	ofile.write("\n\taffect_shadows= %d;"%(BRDFVRayMtl.refract_affect_shadows))
	ofile.write("\n\taffect_alpha= %d;"%(BRDFVRayMtl.refract_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(BRDFVRayMtl.refract_trace))
	ofile.write("\n\ttrace_depth= %s;"%(BRDFVRayMtl.refract_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlassGlossy_%s"%(ma_name)

	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tglossiness= %s;"%(a(sce,BRDFVRayMtl.refract_glossiness)))
	ofile.write("\n\tsubdivs= %i;"%(BRDFVRayMtl.refract_subdivs))
	ofile.write("\n\tior= %s;"%(a(sce,BRDFVRayMtl.refract_ior)))
	ofile.write("\n\taffect_shadows= %d;"%(BRDFVRayMtl.refract_affect_shadows))
	ofile.write("\n\taffect_alpha= %d;"%(BRDFVRayMtl.refract_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(BRDFVRayMtl.refract_trace))
	ofile.write("\n\ttrace_depth= %s;"%(BRDFVRayMtl.refract_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFLight(ofile, sce, ma, ma_name, tex_vray):
	brdf_name= "BRDFLight_%s"%(ma_name)

	if(tex_vray['color']):
		color= tex_vray['color']
	else:
		color= "Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color))

	if(tex_vray['alpha']):
		alpha= write_TexInvert(ofile, sce,tex_vray['alpha'])
		color= write_TexCompMax(ofile, sce,"%s_alpha"%(brdf_name), alpha, color)

	light= ma.vray.BRDFLight

	ofile.write("\nBRDFLight %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,color)))
	ofile.write("\n\tcolorMultiplier= %s;"%(a(sce,ma.emit * 10)))
	ofile.write("\n\tcompensateExposure= %s;"%(a(sce,light.compensateExposure)))
	ofile.write("\n\temitOnBackSide= %s;"%(a(sce,light.emitOnBackSide)))
	ofile.write("\n\tdoubleSided= %s;"%(a(sce,light.doubleSided)))

	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency= %s;"%(a(sce,tex_vray['alpha'])))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))

	ofile.write("\n}\n")

	return brdf_name


def write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl
		
	brdf_name= "BRDFDiffuse_%s"%(ma_name)

	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	ofile.write("\n\troughness= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(BRDFVRayMtl.roughness))))
	if(tex_vray['color']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['color']))
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha))))
	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency_tex= %s;"%(a(sce,tex_vray['alpha'])))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDF(ofile, sce, ma, ma_name, tex_vray):
	def bool_color(color):
		for c in color:
			if c > 0.0:
				return True
		return False

	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdfs= []

	if tex_vray['reflect']:
		tex_vray['reflect']= write_TexInvert(tex_vray['reflect'])

	if tex_vray['reflect'] or bool_color(BRDFVRayMtl.reflect_color):
		if BRDFVRayMtl.reflect_glossiness < 1.0 or tex_vray['reflect_glossiness']:
			brdf_name= write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray)
		brdfs.append(brdf_name)

	if tex_vray['refract'] or bool_color(BRDFVRayMtl.refract_color):
		if BRDFVRayMtl.refract_glossiness < 1.0 or tex_vray['refract_glossiness']:
			brdf_name= write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray)
	else:
		brdf_name= write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray)
	brdfs.append(brdf_name)

	if len(brdfs) == 1:
		brdf_name= brdfs[0]
	else:
		brdf_name= "BRDFLayered_%s"%(ma_name)
		ofile.write("\nBRDFLayered %s {"%(brdf_name))
		ofile.write("\n\tbrdfs= List(%s);"%(','.join(brdfs)))
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha))))
		if tex_vray['alpha']:
			ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['alpha']))
		ofile.write("\n}\n")

	return brdf_name

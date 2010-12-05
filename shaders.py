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
from vb25.plugin_manager import *


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
		#'opacity',
		#'iffuse',
		#'roughness',
		##'brdf_type',
		#'reflect',
		#'reflect_glossiness',
		#'hilight_glossiness',
		'hilight_glossiness_lock',
		'fresnel',
		#'fresnel_ior',
		'fresnel_ior_lock',
		'reflect_subdivs',
		'reflect_trace',
		'reflect_depth',
		'reflect_exit_color',
		'hilight_soften',
		##'reflect_dim_distance',
		'reflect_dim_distance_on',
		'reflect_dim_distance_falloff',
		#anisotropy',
		#anisotropy_rotation',
		'anisotropy_derivation',
		'anisotropy_axis',
		##'anisotropy_uvwgen',
		#'refract',
		#'refract_ior',
		'dispersion_on',
		'dispersion',
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
		#'translucency_color',
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
		##'environment_override',
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

CAMERA_TYPE= {
	'DEFAULT':            0,
	'SPHERIFICAL':        1,
	'CYLINDRICAL_POINT':  2,
	'CYLINDRICAL_ORTHO':  3,
	'BOX':                4,
	'FISH_EYE':           5,
	'WARPED_SPHERICAL':   6,
	'ORTHOGONAL':         7,
	'PINHOLE':            8
}

BITMAP_FILTER_TYPE= {
	'NONE':   0,
	'MIPMAP': 1,
	'AREA':   2
}

BLEND_MODES= {
	'NONE':         '0',
	'STENCIL':      '1',
	'OVER':         '1',
	'IN':           '2',
	'OUT':          '3',
	'ADD':          '4',
	'SUBTRACT':     '5',
	'MULTIPLY':     '6',
	'DIFFERENCE':   '7',
	'LIGHTEN':      '8',
	'DARKEN':       '9',
	'SATURATE':    '10',
	'DESATUREATE': '11',
	'ILLUMINATE':  '12',
}

TRANS_ENV_MAPPING= {
	'SPHERE': 'spherical',
	'VIEW':   'screen',
	'GLOBAL': 'screen',
	'OBJECT': 'cubic',
	'TUBE':   'mirror_ball',
	'ANGMAP': 'angular'
}

ENV_MAPPING_TYPE= {
	'SPHERE': 'spherical',
	'VIEW':   'screen',
	'GLOBAL': 'screen',
	'OBJECT': 'cubic',
	'TUBE':   'mirror_ball',
	'ANGMAP': 'angular'
}

ENVIRONMENT_MAPPING= {
	'SPHERE':   'spherical',
	'ANGLULAR': 'angular',
	'SCREEN':   'screen',
	'TUBE':     'max_cylindrical',
	'CUBIC':    'cubic',
	'MBALL':    'mirror_ball',
}

PROJECTION_MAPPING= {
	'FLAT':   1,
	'SPHERE': 2,
	'TUBE':   3,
	'BALL':   4,
	'CUBE':   5,
	'TRI':    6,
	'PERS':   8,
}


def multiply_texture(ofile, sce, input_texture_name, mult_value):
	if mult_value == 1.0:
		return input_texture_name

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


def write_UVWGenProjection(ofile, sce, params):
	ob= params.get('object')
	slot= params.get('slot')
	texture= params.get('texture')

	uvw_name= params['name'] + 'UVP'

	VRayTexture= texture.vray
	VRayTexture.uvwgen= uvw_name

	if VRayTexture.object:
		ob= get_data_by_name(sce, 'objects', VRayTexture.object)

	ofile.write("\nUVWGenProjection %s {" % uvw_name)
	ofile.write("\n\ttype= %d;" % PROJECTION_MAPPING[VRayTexture.mapping])
	if ob:
		mt= mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
		mt*= ob.matrix_world.copy().invert() 
		ofile.write("\n\tuvw_transform= %s; // %s" % (a(sce,transform(mt)),ob.name))
	ofile.write("\n}\n")

	return uvw_name


def write_UVWGenChannel(ofile, sce, params):
	slot= params.get('slot')
	texture= params.get('texture')

	uvw_name= params['name'] + 'UVC'

	VRaySlot= texture.vray_slot
	VRayTexture= texture.vray
	VRaySlot.uvwgen= uvw_name

	uvwgen= write_UVWGenProjection(ofile, sce, params) if VRayTexture.texture_coords == 'ORCO' else None

	ofile.write("\nUVWGenChannel %s {" % uvw_name)
	ofile.write("\n\twrap_u= %d;" % (2 if texture.use_mirror_x else 0))
	ofile.write("\n\twrap_v= %d;" % (2 if texture.use_mirror_y else 0))
	ofile.write("\n\tuvw_transform= interpolate((%i, Transform(" % sce.frame_current)
	ofile.write("\n\t\tMatrix(")
	ofile.write("\n\t\t\tVector(1.0,0.0,0.0)*%.3f," % (texture.repeat_x if VRayTexture.tile in ('TILEUV','TILEU') else 1.0))
	ofile.write("\n\t\t\tVector(0.0,1.0,0.0)*%.3f," % (texture.repeat_y if VRayTexture.tile in ('TILEUV','TILEV') else 1.0))
	ofile.write("\n\t\t\tVector(0.0,0.0,1.0)")
	ofile.write("\n\t\t),")
	ofile.write("\n\t\tVector(%.3f,%.3f,0.0)" % ((slot.offset[0], slot.offset[1]) if slot else (1.0,1.0)))
	ofile.write("\n\t)));")
	if uvwgen:
		ofile.write("\n\tuvwgen= %s;" % uvwgen)
	else:
		ofile.write("\n\tuvw_channel= %d;" % (1)) # TODO
	ofile.write("\n}\n")

	return uvw_name


def write_UVWGenEnvironment(ofile, sce, params):
	slot= params.get('slot')
	texture= params.get('texture')

	VRaySlot= texture.vray_slot
	VRayTexture= texture.vray

	uvw_name= get_random_string()
	
	ofile.write("\nUVWGenEnvironment %s {" % uvw_name)
	if 'rotate' in params:
		ofile.write("\n\tuvw_matrix= %s;" % transform(mathutils.Matrix.Rotation(math.radians(params['rotate']['angle']), 4, params['rotate']['axis'])))
	ofile.write("\n\tmapping_type= \"%s\";" % ENVIRONMENT_MAPPING[VRayTexture.environment_mapping])
	ofile.write("\n}\n")
	
	return uvw_name


def write_BitmapBuffer(ofile, sce, params):
	slot= params.get('slot')
	texture= params.get('texture')

	BitmapBuffer= texture.image.vray.BitmapBuffer

	filename= get_full_filepath(sce,texture.image.filepath)
	if not sce.vray.VRayDR.on:
		if not os.path.exists(filename) or not texture.image.filepath:
			print("V-Ray/Blender: %s Texture: %s => Image file does not exists!"%(color("Error!",'red'),texture.name))
			return None

	if texture.image.source == 'SEQUENCE':
		bitmap_name= get_random_string()
	else:
		bitmap_name= 'IM' + clean_string("".join(os.path.basename(filename).split('.')[:-1]))
		if 'filters' in params:
			if bitmap_name in params['filters']['exported_bitmaps']:
				return bitmap_name
			params['filters']['exported_bitmaps'].append(bitmap_name)

	ofile.write("\nBitmapBuffer %s {" % bitmap_name)
	ofile.write("\n\tfile= \"%s\";" % filename)
	if BitmapBuffer.use_input_gamma:
		ofile.write("\n\tgamma= %s;" % p(sce.vray.SettingsColorMapping.input_gamma))
	else:
		ofile.write("\n\tgamma= %s;" % a(sce,BitmapBuffer.gamma))
	if texture.image.source == 'SEQUENCE':
		ofile.write("\n\tframe_sequence= 1;")
		ofile.write("\n\tframe_number= %s;" % a(sce,sce.frame_current))
		ofile.write("\n\tframe_offset= %i;" % texture.image_user.frame_offset)
	ofile.write("\n\tfilter_type= %d;" % BITMAP_FILTER_TYPE[BitmapBuffer.filter_type])
	ofile.write("\n\tfilter_blur= %.3f;" % BitmapBuffer.filter_blur)
	ofile.write("\n}\n")

	return bitmap_name


def write_TexBitmap(ofile, sce, params):
	PLACEMENT_TYPE= {
		'FULL':  0,
		'CROP':  1,
		'PLACE': 2
	}

	TILE= {
		'NOTILE': 0,
		'TILEUV': 1,
		'TILEU':  2,
		'TILEV':  3,
	}

	slot= params.get('slot')
	texture= params.get('texture')

	VRayTexture= texture.vray
	VRaySlot=    texture.vray_slot

	if not texture.image:
		print("V-Ray/Blender: %s Image is not set! (%s)"%(color("Error!",'red'),texture.name))
		return "Texture_no_texture"

	tex_name= 'TE' + clean_string(texture.name)

	if VRayTexture.texture_coords == 'ORCO':
		if 'object' in params:
			tex_name= 'OB' + clean_string(params['object'].name) + tex_name

	if 'filters' in params:
		if tex_name in params['filters']['exported_textures']:
			debug(sce, "Filters: %s" % params['filters'])
			return tex_name
		params['filters']['exported_textures'].append(tex_name)

	bitmap= write_BitmapBuffer(ofile, sce, params)

	if bitmap is None:
		return None
	
	if 'environment' in params:
		uvwgen= write_UVWGenEnvironment(ofile, sce, params)
	else:
		uvwgen= write_UVWGenChannel(ofile, sce, params)

	ofile.write("\nTexBitmap %s {" % tex_name)
	ofile.write("\n\tbitmap= %s;" % bitmap)
	ofile.write("\n\tuvwgen= %s;" % uvwgen)
	if 'material' in params:
		ofile.write("\n\tnouvw_color= AColor(%.3f,%.3f,%.3f,1.0);" % tuple(params['material'].diffuse_color))
	ofile.write("\n\ttile= %d;" % TILE[VRayTexture.tile])
	ofile.write("\n\tu= %s;" % texture.crop_min_x)
	ofile.write("\n\tv= %s;" % texture.crop_min_y)
	ofile.write("\n\tw= %s;" % texture.crop_max_x)
	ofile.write("\n\th= %s;" % texture.crop_max_y)
	ofile.write("\n\tplacement_type= %i;" % PLACEMENT_TYPE[texture.vray.placement_type])
	if slot:
		ofile.write("\n\tinvert= %d;"%(slot.invert))
	ofile.write("\n}\n")

	return tex_name


def write_TexPlugin(ofile, sce, params):
	if 'texture' in params:
		VRayTexture= params['texture'].vray
		plugin= get_plugin(TEX_PLUGINS, VRayTexture.type)
		if plugin:
			return plugin.write(ofile, sce, params)


def write_texture(ofile, sce, params):
	texture= params['texture']

	texture_name= 'TE' + clean_string(texture.name)
	if 'material' in params:
		texture_name= 'MA' + clean_string(params['material'].name) + texture_name
	if 'mapto' in params:
		texture_name+= 'TS' + params['mapto']

	params['name']= texture_name

	if texture.type == 'IMAGE':
		texture_name= write_TexBitmap(ofile, sce, params)
	elif texture.type == 'VRAY':
		texture_name= write_TexPlugin(ofile, sce, params)
	else:
		texture_name= None
		print("V-Ray/Blender: Texture type [%s] is currently unsupported." % texture.type)

	if texture_name is None:
		return "Texture_no_texture"

	# for key in ('object','material','mapto','texture','slot'):
	# 	if key in params: del params[key]

	return texture_name


def write_TexAColorOp(ofile, sce, color_a, mult):
	tex_name= get_random_string()
	ofile.write("\nTexAColorOp %s {" % tex_name)
	ofile.write("\n\tcolor_a= %s;" % color_a)
	ofile.write("\n\tmult_a= %s;" % a(sce,mult))
	ofile.write("\n}\n")
	return tex_name


def write_TexInvert(ofile, tex):
	tex_name= get_random_string()
	ofile.write("\nTexInvert %s {" % tex_name)
	ofile.write("\n\ttexture= %s;" % tex)
	ofile.write("\n}\n")
	return tex_name


def write_TexCompMax(ofile, sce, params):
	OPERATOR= {
		'Add':        0,
		'Substract':  1,
		'Difference': 2,
		'Multiply':   3,
		'Divide':     4,
		'Minimum':    5,
		'Maximum':    6
	}

	tex_name= "TexCompMax_%s"%(params['name'])

	ofile.write("\nTexCompMax %s {" % tex_name)
	ofile.write("\n\tsourceA= %s;" % params['sourceA'])
	ofile.write("\n\tsourceB= %s;" % params['sourceB'])
	ofile.write("\n\toperator= %d;" % OPERATOR[params['operator']])
	ofile.write("\n}\n")

	return tex_name


def write_TexFresnel(ofile, sce, ma, ma_name, textures):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {" % tex_name)
	if 'reflect' in textures:
		ofile.write("\n\tblack_color= %s;" % textures['reflect'])
	else:
		ofile.write("\n\tblack_color= %s;" % a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color]))))
	ofile.write("\n\tfresnel_ior= %s;" % a(sce,ma.vray.BRDFVRayMtl.fresnel_ior))
	ofile.write("\n}\n")

	return tex_name


def write_BRDFGlossy(ofile, sce, ma, ma_name, textures):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= get_random_string()

	if BRDFVRayMtl.brdf_type == 'PHONG':
		ofile.write("\nBRDFPhong %s {"%(brdf_name))
	elif BRDFVRayMtl.brdf_type == 'WARD':
		ofile.write("\nBRDFWard %s {"%(brdf_name))
	else:
		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	ofile.write("\n\tsubdivs= %i;"%(BRDFVRayMtl.reflect_subdivs))

	if 'reflect' in textures:
		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(textures['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))

	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	if BRDFVRayMtl.hilight_glossiness_lock:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	else:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.hilight_glossiness)))
	if 'reflect_glossiness' in textures:
		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(textures['reflect_glossiness'])))
	if 'hilight_glossiness' in textures:
		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(textures['hilight_glossiness'])))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	if BRDFVRayMtl.brdf_type != 'PHONG':
		ofile.write("\n\tanisotropy= %s;"%(a(sce,BRDFVRayMtl.anisotropy)))
		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,BRDFVRayMtl.anisotropy_rotation)))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFMirror(ofile, sce, ma, ma_name, textures):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= get_random_string()

	ofile.write("\nBRDFMirror %s {"%(brdf_name))
	if textures['color']:
		ofile.write("\n\tcolor= %s;"%(textures['color']))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	if textures['reflect']:
		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(textures['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlass(ofile, sce, ma, ma_name, textures):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= get_random_string()

	ofile.write("\nBRDFGlass %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.refract_color)))))
	if 'refract' in textures:
		ofile.write("\n\tcolor_tex= %s;"%(textures['refract']))
	ofile.write("\n\tior= %s;"%(a(sce,BRDFVRayMtl.refract_ior)))
	ofile.write("\n\taffect_shadows= %d;"%(BRDFVRayMtl.refract_affect_shadows))
	ofile.write("\n\taffect_alpha= %d;"%(BRDFVRayMtl.refract_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(BRDFVRayMtl.refract_trace))
	ofile.write("\n\ttrace_depth= %s;"%(BRDFVRayMtl.refract_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlassGlossy(ofile, sce, ma, ma_name, textures):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= get_random_string()

	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.refract_color)))))
	if 'refract' in textures:
		ofile.write("\n\tcolor_tex= %s;"%(textures['refract']))
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


def write_BRDFDiffuse(ofile, sce, ma, ma_name, textures):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl
		
	brdf_name= get_random_string()

	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	ofile.write("\n\troughness= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(BRDFVRayMtl.roughness))))
	if 'diffuse' in textures:
		ofile.write("\n\tcolor_tex= %s;" % textures['diffuse'])
	ofile.write("\n\ttransparency= %s;" % a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha)))
	if 'opacity' in textures:
		ofile.write("\n\ttransparency_tex= %s;" % textures['opacity'])
	ofile.write("\n}\n")

	return brdf_name


def write_BRDF(ofile, sce, ma, ma_name, textures):
	def bool_color(color):
		for c in color:
			if c > 0.0:
				return True
		return False

	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdfs= []

	reflect= None

	if 'reflect' in textures:
		reflect= write_TexInvert(textures['reflect'])

	if reflect or bool_color(BRDFVRayMtl.reflect_color):
		if BRDFVRayMtl.reflect_glossiness < 1.0 or 'reflect_glossiness' in textures:
			brdf_name= write_BRDFGlossy(ofile, sce, ma, ma_name, textures['mapto'])
		else:
			brdf_name= write_BRDFMirror(ofile, sce, ma, ma_name, textures['mapto'])
		brdfs.append(brdf_name)

	if 'refract' in textures or bool_color(BRDFVRayMtl.refract_color):
		if BRDFVRayMtl.refract_glossiness < 1.0 or 'refract_glossiness' in textures:
			brdf_name= write_BRDFGlassGlossy(ofile, sce, ma, ma_name, textures['mapto'])
		else:
			brdf_name= write_BRDFGlass(ofile, sce, ma, ma_name, textures['mapto'])
	else:
		brdf_name= write_BRDFDiffuse(ofile, sce, ma, ma_name, textures['mapto'])
	brdfs.append(brdf_name)

	if len(brdfs) == 1:
		brdf_name= brdfs[0]
	else:
		brdf_name= "BRDFLayered_%s"%(ma_name)
		ofile.write("\nBRDFLayered %s {"%(brdf_name))
		ofile.write("\n\tbrdfs= List(%s);"%(','.join(brdfs)))
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha))))
		if 'opacity' in textures:
			ofile.write("\n\ttransparency_tex= %s;" % textures['opacity'])
		ofile.write("\n}\n")

	return brdf_name


def write_BRDFLight(ofile, sce, ma, ma_name, mapped_params):
	textures= mapped_params['mapto']

	brdf_name= "BRDFLight_%s"%(ma_name)

	light= ma.vray.BRDFLight

	ofile.write("\nBRDFLight %s {"%(brdf_name))

	if 'diffuse' in textures:
		color= textures['diffuse']
		if 'opacity' in textures:
			alpha= write_TexInvert(ofile, sce, textures['opacity'])
			color= write_TexCompMax(ofile, sce, {'name': "%s_alpha" % brdf_name,
												 'sourceA': alpha,
												 'sourceB': color,
												 'opertor': 'Multiply'})
		ofile.write("\n\tcolor= %s;" % color)
	else:
		ofile.write("\n\tcolor= %s;" % a(sce, ma.diffuse_color))

	ofile.write("\n\tcolorMultiplier= %s;" % a(sce, ma.emit * 10))
	ofile.write("\n\tcompensateExposure= %s;" % p(light.compensateExposure))
	ofile.write("\n\temitOnBackSide= %s;" % p(light.emitOnBackSide))
	ofile.write("\n\tdoubleSided= %s;" % p(light.doubleSided))

	if 'opacity' in textures:
		ofile.write("\n\ttransparency= %s;" % textures['opacity'])
	else:
		ofile.write("\n\ttransparency= %s;" % a(sce,"Color(1.0,1.0,1.0)*%.6f" % (1.0 - ma.alpha)))

	ofile.write("\n}\n")

	return brdf_name

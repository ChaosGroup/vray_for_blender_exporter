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


''' Python modules  '''
import os
import sys
import tempfile
import math
import subprocess
import time
import shutil
import filecmp
import socket

''' Blender modules '''
import bpy
import mathutils


PLATFORM= sys.platform
HOSTNAME= socket.gethostname()

none_matrix= mathutils.Matrix(
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0]
)

MODULES= {
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
		'overall_color',
		'diffuse_color',
		'diffuse_amount',
		'sub_surface_color',
		'scatter_radius',
		'scatter_radius_mult',
		'phase_function',
		'specular_color',
		'specular_amount',
		'specular_glossiness',
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
		'opacity',
		'diffuse',
		'roughness',
		# 'brdf_type',
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
		'translucency_color',
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

BLEND_TYPE= {
	'MIX':          0,
	'ADD':          4,
	'SUBTRACT':     5,
	'MULTIPLY':     6,
	'SCREEN':       0,
	'OVERLAY':      1,
	'DIFFERENCE':   7,
	'DIVIDE':       0,
	'DARKEN':       9,
	'LIGHTEN':      8,
	'HUE':          0,
	'SATURATION':  10,
	'VALUE':        0,
	'COLOR':        0,
	'SOFT LIGHT':   0,
	'LINEAR LIGHT': 0
}

TEX_TYPES= ('IMAGE', 'VRAY')

# Enum currently doesn't extract value index,
# so...
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


def	debug(sce, s):
	ve= sce.vray.exporter
	if ve.debug:
		print("V-Ray/Blender: %s"%(s))

def p(t):
	if type(t) == type(True):
		return "%i"%(t)
	elif type(t) == type(1):
		return "%i"%(t)
	elif type(t) == type(1.0):
		return "%.6f"%(t)
	elif str(type(t)) == "<class 'color'>":
		return "Color(%.3f,%.3f,%.3f)"%(tuple(t))
	elif str(type(t)) == "<class 'vector'>":
		return "Color(%.3f,%.3f,%.3f)"%(tuple(t))
	elif type(t) == type(""):
		if(t == "True"):
			return "1"
		elif(t == "False"):
			return "0"
		else:
			return t
	else:
		return "%s"%(t)

def a(sce,t):
	return "interpolate((%i,%s))"%(sce.frame_current,p(t))

def transform(m):
	return "Transform(Matrix(Vector(%f, %f, %f),Vector(%f, %f, %f),Vector(%f, %f, %f)),Vector(%f, %f, %f))"\
            %(m[0][0], m[0][1], m[0][2],\
              m[1][0], m[1][1], m[1][2],\
              m[2][0], m[2][1], m[2][2],\
              m[3][0], m[3][1], m[3][2])

def clean_string(s):
	s= s.replace("+", "p")
	s= s.replace("-", "m")
	for i in range(len(s)):
		c= s[i]
		if not ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')):
			s= s.replace(c, "_")
	return s

def rel_path(filepath):
	if filepath[:2] == "//":
		return True
	else:
		return False

def get_filename(fn):
	(filepath, filename)= os.path.split(bpy.path.abspath(fn))
	return filename

def get_full_filepath(sce,filepath):
	VRayDR= sce.vray.VRayDR

	src_file= os.path.normpath(bpy.path.abspath(filepath))
	src_filename= os.path.split(src_file)[1]

	if VRayDR.on:
		dest_path= os.path.normpath(bpy.path.abspath(VRayDR.shared_dir))

		if dest_path == "":
			return src_file
		
		blendfile_name= os.path.split(bpy.data.filepath)[1][:-6]

		dest_path= os.path.join(dest_path, blendfile_name + os.sep)
		if not os.path.exists(dest_path):
			os.mkdir(dest_path)

		dest_file= os.path.join(dest_path,src_filename)
		if os.path.isfile(src_file):
			if os.path.exists(dest_file):
				if not filecmp.cmp(dest_file,src_file):
					debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
					shutil.copy(src_file,dest_path)
			else:
				debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
				shutil.copy(src_file,dest_path)

		if VRayDR.type == 'UU':
			return dest_file
		elif VRayDR.type == 'WU':
			return "..%s%s%s%s"%(os.sep, blendfile_name, os.sep, src_filename)
		else:
			return "//%s/%s"%(HOSTNAME, rel_path)

	return src_file

def get_render_file_format(ve,file_format):
	if ve.image_to_blender:
		return 'exr'
	if file_format in ('JPEG','JPEG2000'):
		file_format= 'jpg'
	elif file_format in ('OPEN_EXR','IRIS','CINEON'):
		file_format= 'exr'
	elif file_format == 'MULTILAYER':
		file_format= 'vrimg'
	elif file_format in ('TARGA', 'TARGA_RAW'):
		file_format= 'tga'
	else:
		file_format= 'png'
	return file_format.lower()
	
def get_name(data, prefix= None, dupli_name= None):
	name= data.name
	if dupli_name:
		name= "%s_%s"%(dupli_name,name)
	if prefix:
		name= "%s_%s"%(prefix,name)
	if data.library:
		name+= "_%s"%(get_filename(data.library.filepath))
	return clean_string(name)

def object_on_visible_layers(sce,ob):
	for l in range(20):
		if ob.layers[l] and sce.layers[l]:
			return True
	return False

def vb_script_path():
	for vb_path in bpy.utils.script_paths(os.path.join('io','vb25')):
		if vb_path:
			return vb_path
	return ''

def proxy_creator(hq_filepath, vrmesh_filepath, append= False):
	pc_binary= "vb_proxy"
	if PLATFORM == 'win32':
		pc_binary+= ".exe"
	if vb_script_path():
		p= os.path.join(vb_script_path(),pc_binary)
		if os.path.exists(p):
			pc_binary= p

	params= []
	params.append(pc_binary)
	if append:
		params.append('--append')
	params.append(hq_filepath)
	params.append(vrmesh_filepath)

	os.system(' '.join(params))

def vb_binary_path(sce):
	vray_bin= "vray"
	if PLATFORM == 'win32':
		vray_bin+= ".exe"
	vray_path= vray_bin

	VRayExporter= sce.vray.exporter
	if not VRayExporter.detect_vray:
		if VRayExporter.vray_binary == "":
			debug(sce,"V-Ray binary is not set!")
			return vray_bin
		else:
			return bpy.path.abspath(VRayExporter.vray_binary)
	
	vray_env_path= os.getenv('VRAY_PATH')

	if vray_env_path is None:
		for maya in ('2011','2010','2009','2008'):
			for arch in ('x64','x86'):
				vray_env_path= os.getenv("VRAY_FOR_MAYA%s_MAIN_%s"%(maya,arch))
				if vray_env_path:
					break
			if vray_env_path:
				break
		if vray_env_path:
			vray_env_path= os.path.join(vray_env_path,'bin')

	if vray_env_path:
		if PLATFORM == "win32":
			if vray_env_path[0:1] == ";":
				vray_env_path= vray_env_path[1:]
			if vray_env_path[0:1] == "\"":
				vray_env_path= vray_env_path[1:-1]
		else:
			if vray_env_path[0:1] == ":":
				vray_env_path= vray_env_path[1:]
		vray_path=  os.path.join(vray_env_path, vray_bin)

	return vray_path

def get_plugin(plugins, plugin_id):
	for plugin in plugins:
		if plugin.ID == plugin_id:
			return plugin
	return None

def get_filenames(sce, filetype):
	def create_dir(directory):
		if not os.path.exists(directory):
			print("V-Ray/Blender: Path doesn't exist, trying to create...")
			print("V-Ray/Blender: Creating directory: %s"%(directory))
			try:
				os.mkdir(directory)
			except:
				print("V-Ray/Blender: Creating directory \"%s\" failed!"%(directory))
				directory= tempfile.gettempdir()
				print("V-Ray/Blender: Using default exporting path: \"%s\""%(directory))
		return directory

	ve= sce.vray.exporter
	VRayDR= sce.vray.VRayDR
	
	(blendfile_path, blendfile_name)= os.path.split(bpy.data.filepath)
	blendfile_name= blendfile_name[:-6]

	default_dir= tempfile.gettempdir()
	export_dir= default_dir

	export_file= 'scene'
	if ve.output_unique:
		export_file= blendfile_name

	if VRayDR.on:
		export_dir= os.path.join(bpy.path.abspath(VRayDR.shared_dir), blendfile_name + os.sep)
	else:
		if ve.output == 'USER':
			if ve.output_dir == "":
				export_dir= default_dir
			else:
				export_dir= bpy.path.abspath(ve.output_dir)
		elif ve.output == 'SCENE':
			export_dir= blendfile_path

		if ve.output != 'USER':
			export_dir= os.path.join(export_dir,"vb25")

	filepath= export_dir

	if filetype in ('scene', 'geometry', 'materials', 'lights', 'nodes', 'camera'):
		filepath= os.path.join(create_dir(export_dir), "%s_%s.vrscene" % (export_file,filetype))

	elif filetype == 'lightmaps':
		filepath= create_dir(os.path.join(export_dir,filetype))

	elif filetype == 'output':
		if blendfile_name == 'startup.blend':
			filepath= create_dir(export_dir)
		else:
			filepath= create_dir(bpy.path.abspath(sce.render.filepath))

	debug(sce,"Filepath (%s): %s" % (filetype,filepath))

	return filepath


# TODO: add to scene converter
# BLEND_TYPE= {
# 	'MIX':          1,
# 	'ADD':         4,
# 	'SUBTRACT':    5,
# 	'MULTIPLY':    6,
# 	'SCREEN':       1,
# 	'OVERLAY':     1,
# 	'DIFFERENCE':  7,
# 	'DIVIDE':       1,
# 	'DARKEN':      9,
# 	'LIGHTEN':     8,
# 	'HUE':          1,
# 	'SATURATION': 10,
# 	'VALUE':        1,
# 	'COLOR':        1,
# 	'SOFT LIGHT':   1,
# 	'LINEAR LIGHT': 1
# }


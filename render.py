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
import math
import os
import string
import subprocess
import sys
import tempfile
import time

''' Blender modules '''
import bpy
import mathutils

''' vb modules '''
from vb25.utils import *
from vb25.shaders import *
from vb25.plugin_manager import *


VERSION= '2.5'


'''
  VRAY MODULES
'''
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
	
	'SettingsRegionsGenerator': (
        'xc',
        'yc',
        # 'xymeans',
        # 'seqtype',
        'reverse'
	)
}

OBJECT_PARAMS= {
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
		# 'translucency_thickness',
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
		'units',
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

TEX_TYPES= ('IMAGE', 'PLUGIN')

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
	"DELONE":    1,
	"LEAST":     2,
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



'''
  MESHES
'''
def write_geometry(sce, geometry_file):
	vsce= sce.vray
	ve= vsce.exporter

	# For getting unique IDs for UV names
	uv_layers= []
	for ma in bpy.data.materials:
		for slot in ma.texture_slots:
			if(slot):
				if(slot.texture):
					if slot.texture.type in TEX_TYPES:
						if slot.texture_coords in ('UV'):
							if slot.uv_layer not in uv_layers:
								uv_layers.append(slot.uv_layer)

	try:
		print("V-Ray/Blender: Special build detected - using custom operator.")
		bpy.ops.scene.scene_export(
			vb_geometry_file= geometry_file,
			vb_active_layers= ve.active_layers,
			vb_animation= ve.animation
		)

	except:
		print("V-Ray/Blender: Exporting meshes...")
		
		# Used when exporting dupli, particles etc.
		exported_meshes= []

		def write_mesh(exported_meshes, ob):
			me= ob.create_mesh(sce, True, 'RENDER')

			me_name= get_name(ob.data, 'Geom')

			if me_name in exported_meshes:
				return

			exported_meshes.append(me_name)

			if ve.debug:
				print("V-Ray/Blender: [%i]\n  Object: %s\n    Mesh: %s"
					  %(sce.frame_current,
						ob.name,
						ob.data.name))
			else:
				if(PLATFORM == "win32"):
					sys.stdout.write("V-Ray/Blender: [%i] Mesh: %s                              \r"
									 %(sce.frame_current, ob.data.name))
				else:
					sys.stdout.write("V-Ray/Blender: [%i] Mesh: \033[0;32m%s\033[0m                              \r"
									 %(sce.frame_current, ob.data.name))
				sys.stdout.flush()

			ofile.write("\nGeomStaticMesh %s {"%(me_name))

			ofile.write("\n\tvertices= interpolate((%d, ListVector("%(sce.frame_current))
			for v in me.verts:
				if(v.index):
					ofile.write(",")
				ofile.write("Vector(%.6f,%.6f,%.6f)"%(tuple(v.co)))
			ofile.write(")));")

			ofile.write("\n\tfaces= interpolate((%d, ListInt("%(sce.frame_current))
			for f in me.faces:
				if(f.index):
					ofile.write(",")
				if(len(f.verts) == 4):
					ofile.write("%d,%d,%d,%d,%d,%d"%(
						f.verts[0], f.verts[1], f.verts[2],
						f.verts[2], f.verts[3], f.verts[0]))
				else:
					ofile.write("%d,%d,%d"%(
						f.verts[0], f.verts[1], f.verts[2]))
			ofile.write(")));")

			ofile.write("\n\tface_mtlIDs= ListInt(")
			for f in me.faces:
				if(f.index):
					ofile.write(",")
				if(len(f.verts) == 4):
					ofile.write("%d,%d"%(
						f.material_index, f.material_index))
				else:
					ofile.write("%d"%(
						f.material_index))
			ofile.write(");")

			ofile.write("\n\tnormals= interpolate((%d, ListVector("%(sce.frame_current))
			for f in me.faces:
				if(f.index):
					ofile.write(",")

				if(len(f.verts) == 4):
					verts= (0,1,2,2,3,0)
				else:
					verts= (0,1,2)

				comma= 0
				for v in verts:
					if(comma):
						ofile.write(",")
					comma= 1

					if(f.smooth):
						ofile.write("Vector(%.6f,%.6f,%.6f)"%(
							tuple(me.verts[f.verts[v]].normal)
							))
					else:
						ofile.write("Vector(%.6f,%.6f,%.6f)"%(
							tuple(f.normal)
							))
			ofile.write(")));")

			ofile.write("\n\tfaceNormals= ListInt(")
			k= 0
			for f in me.faces:
				if(f.index):
					ofile.write(",")

				if(len(f.verts) == 4):
					verts= 6
				else:
					verts= 3

				for v in range(verts):
					if(v):
						ofile.write(",")
					ofile.write("%d"%(k))
					k+= 1
			ofile.write(");")

			if(len(me.uv_textures)):
				ofile.write("\n\tmap_channels= List(")

				for uv_texture, uv_texture_idx in zip(me.uv_textures, range(len(me.uv_textures))):
					if(uv_texture_idx):
						ofile.write(",")

					uv_layer_index= 1
					try:
						uv_layer_index= uv_layers.index(uv_texture.name)
					except:
						pass

					ofile.write("\n\t\t// %s"%(uv_texture.name))
					ofile.write("\n\t\tList(%d,ListVector("%(uv_layer_index))

					for f in range(len(uv_texture.data)):
						if(f):
							ofile.write(",")

						face= uv_texture.data[f]

						for i in range(len(face.uv)):
							if(i):
								ofile.write(",")

							ofile.write("Vector(%.6f,%.6f,0.0)"%(
								face.uv[i][0],
								face.uv[i][1]
							))

					ofile.write("),ListInt(")
					u = -1
					u0= -1
					for f in range(len(uv_texture.data)):
						if(f):
							ofile.write(",")

						face= uv_texture.data[f]

						verts= 3
						if(len(face.uv) == 4):
							verts= 6
							u= u0
						else:
							if(len(uv_texture.data[f-1].uv) == 4):
								u= u0

						for i in range(verts):
							if(i):
								ofile.write(",")

							if(verts == 6):
								if(i == 5):
									u0= u
									u-= 4
								if(i != 3):
									u+= 1
							else:
								u+= 1
								u0= u

							ofile.write("%d"%(u))

					ofile.write("))")

				ofile.write(");")

			ofile.write("\n}\n")

		ofile= open(geometry_file, 'w')
		ofile.write("// V-Ray/Blender %s\n"%(VERSION))
		ofile.write("// Geometry file\n")

		timer= time.clock()

		STATIC_OBJECTS= []
		DYNAMIC_OBJECTS= []

		cur_frame= sce.frame_current
		sce.set_frame(sce.frame_start)

		for ob in sce.objects:
			if ob.type in ('LAMP','CAMERA','ARMATURE','EMPTY'):
				continue

			if ob.data.vray.GeomMeshFile.use:
				continue

			if ve.active_layers:
				if not object_on_visible_layers(sce,ob):
					continue

			dynamic= False
			if ob.data.animation_data:
				dynamic= True
			else:
				for m in ob.modifiers:
					# TODO:
					# Add more modifiers
					# Add detector to custom build
					if m.type in ('ARMATURE', 'SOFT_BODY'):
						dynamic= True
						break

			if dynamic:
				DYNAMIC_OBJECTS.append(ob)
			else:
				STATIC_OBJECTS.append(ob)

		for ob in STATIC_OBJECTS:
			write_mesh(exported_meshes,ob)

		if ve.animation and len(DYNAMIC_OBJECTS):
			f= sce.frame_start
			while(f <= sce.frame_end):
				exported_meshes= []
				sce.set_frame(f)
				for ob in DYNAMIC_OBJECTS:
					write_mesh(exported_meshes,ob)
				f+= sce.frame_step
		else:
			for ob in DYNAMIC_OBJECTS:
				write_mesh(exported_meshes,ob)

		sce.set_frame(cur_frame)

		exported_meshes= []

		STATIC_OBJECTS= []
		DYNAMIC_OBJECTS= []

		ofile.close()
		print("V-Ray/Blender: Exporting meshes... done [%s]                    "%(time.clock() - timer))


def write_mesh_displace(ofile, mesh, params):
	plugin= 'GeomDisplacedMesh'
	name= "%s_%s" % (plugin, mesh)

	ofile.write("\n%s %s {"%(plugin,name))
	ofile.write("\n\tmesh= %s;" % mesh)
	ofile.write("\n\tdisplacement_tex_color= %s;"%(params['texture']))
	# for param in OBJECT_PARAMS[plugin]:
	# 	ofile.write("\n\t%s= %s;"%(param,a(sce,getattr(params['slot'],param))))
	ofile.write("\n}\n")

	return name


def write_GeomMayaHair(ofile, ob, ps, yhname):
	num_hair_vertices= []
	hair_vertices=     []
	widths=            []

	for particle in ps.particles:
		num_hair_vertices.append(str(len(particle.is_hair)))
		for segment in particle.is_hair:
			hair_vertices.append("Vector(%.6f,%.6f,%.6f)" % tuple(segment.co))
			widths.append(str(0.001))

	ofile.write("\nGeomMayaHair %s {"%(name))
	ofile.write("\n\tnum_hair_vertices= interpolate((%d,ListInt(%s)));"%(sce.frame_current, ','.join(num_hair_vertices)))
	ofile.write("\n\thair_vertices= interpolate((%d,ListVector(%s)));"%(sce.frame_current,  ','.join(hair_vertices)))
	ofile.write("\n\twidths= interpolate((%d,ListFloat(%s)));"%(sce.frame_current,          ','.join(widths)))
	ofile.write("\n}\n")


def write_mesh_file(ofile, exported_proxy, ob):
	proxy= od.data.vray.GeomMeshFile
	proxy_name= "Proxy_%s" % clean_string(os.path.basename(proxy.file))

	if proxy_name not in exported_proxy:
		exported_proxy.append(proxy_name)
		
		ofile.write("\nGeomMeshFile %s {"%(proxy_name))
		ofile.write("\n\tfile= \"%s\";"%(get_full_filepath(proxy.file)))
		ofile.write("\n\tanim_speed= %i;"%(proxy.anim_speed))
		ofile.write("\n\tanim_type= %i;"%(PROXY_ANIM_TYPE[proxy.anim_type]))
		ofile.write("\n\tanim_offset= %i;"%(proxy.anim_offset))
		ofile.write("\n}\n")

	return proxy_name



'''
  MATERIALS
'''
def write_multi_material(ofile, ob):
	mtl_name= "Material_%s"%(get_name(ob,"Data"))

	mtls_list= []
	ids_list=  []

	for i,slot in enumerate(ob.material_slots):
		ma_name= "Material_no_material"
		if slot.material is not None:
			ma_name= get_name(slot.material, 'Material')
			
		mtls_list.append(ma_name)
		ids_list.append(str(i))

	ofile.write("\nMtlMulti %s {"%(mtl_name))
	ofile.write("\n\tmtls_list= List(%s);"%(','.join(mtls_list)))
	ofile.write("\n\tids_list= ListInt(%s);"%(','.join(ids_list)))
	ofile.write("\n}\n")

	return mtl_name


def write_UVWGenChannel(ofile, tex, tex_name, ob= None):
	uvw_name= "%s_UVWGenChannel_%s"%(tex_name, get_name(tex))
	
	ofile.write("\nUVWGenChannel %s {"%(uvw_name))
	ofile.write("\n\tuvw_channel= %d;"%(1))
	ofile.write("\n\tuvw_transform= Transform(")
	ofile.write("\n\t\tMatrix(")
	ofile.write("\n\t\t\tVector(1.0,0.0,0.0)*%s,"%(tex.repeat_x))
	ofile.write("\n\t\t\tVector(0.0,1.0,0.0)*%s,"%(tex.repeat_y))
	ofile.write("\n\t\t\tVector(0.0,0.0,1.0)")
	ofile.write("\n\t\t),")
	ofile.write("\n\t\tVector(0.0,0.0,0.0)") # xoffset, yoffset, 0.0
	ofile.write("\n\t);")
	ofile.write("\n}\n")

	return uvw_name


def write_UVWGenEnvironment(ofile, tex, tex_name,  mapping, param= None):
	MAPPING_TYPE= {
		'SPHERE': 'spherical',
		'VIEW':   'screen',
		'GLOBAL': 'screen',
		'OBJECT': 'cubic',
		'TUBE':   'mirror_ball',
		'ANGMAP': 'angular'
	}

	uvw_name= "uv_env_%s_%s"%(tex_name, MAPPING_TYPE[mapping])
	
	ofile.write("\nUVWGenEnvironment %s {"%(uvw_name))
	if(param):
		ofile.write("\n\tuvw_transform= %s;"%(transform(mathutils.RotationMatrix(params[0], 4, 'Z'))))
	ofile.write("\n\tmapping_type= \"%s\";"%(MAPPING_TYPE[mapping]))
	ofile.write("\n\twrap_u= 1;")
	ofile.write("\n\twrap_v= 1;")
	ofile.write("\n\tcrop_u= 0;")
	ofile.write("\n\tcrop_v= 0;")
	ofile.write("\n}\n")
	
	return uvw_name


def write_BitmapBuffer(ofile, exported_bitmaps, tex, tex_name, ob= None):
	filename= get_full_filepath(tex.image.filepath)
	bitmap_name= "BitmapBuffer_%s_%s"%(tex_name, clean_string(os.path.basename(filename)))

	if not os.path.exists(filename):
		debug(sce,"Error! Image file does not exists! (%s)"%(filename))
		return None

	if exported_bitmaps is not None:
		if bitmap_name in exported_bitmaps:
			return bitmap_name
		exported_bitmaps.append(bitmap_name)

	ofile.write("\nBitmapBuffer %s {"%(bitmap_name))
	ofile.write("\n\tfile= %s;"%(a(sce,"\"%s\""%(filename))))
	ofile.write("\n\tgamma= %.6f;"%(1.0))

	filter_type= 0
	if tex.use_interpolation:
		if tex.filter_type == 'BOX':
			filter_type= 1
		else:
			filter_type= 2
	ofile.write("\n\tfilter_type= %d;"%(filter_type))

	ofile.write("\n\tfilter_blur= %.3f;"%(tex.filter_size))
	ofile.write("\n}\n")

	return bitmap_name


def write_TexBitmap(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, ob= None, env= None, env_type= None):
	tex_name= "Texture_no_texture"

	if slot:
		tex= slot.texture

	if tex.image:
		tex_name= get_name(tex,"Texture")
		if ma:
			tex_name= "%s_%s"%(tex_name, get_name(ma,"Material"))

		if env:
			uv_name= write_UVWGenEnvironment(ofile, tex, tex_name, slot.texture_coords)
		else:
			uv_name= write_UVWGenChannel(ofile, tex, tex_name, ob)

		bitmap_name= write_BitmapBuffer(ofile, exported_bitmaps, tex, tex_name, ob)

		if(bitmap_name):
			ofile.write("\nTexBitmap %s {"%(tex_name))
			ofile.write("\n\tbitmap= %s;"%(bitmap_name))
			ofile.write("\n\tuvwgen= %s;"%(uv_name))
			ofile.write("\n\tnouvw_color= AColor(0,0,0,0);")
			if not env:
				if(tex.extension == 'REPEAT'):
					ofile.write("\n\ttile= %d;"%(1))
				else:
					ofile.write("\n\ttile= %d;"%(0))
			if(slot):
				ofile.write("\n\tinvert= %d;"%(slot.invert))
			ofile.write("\n}\n")
		else:
			return "Texture_no_texture"

	else:
		debug(sce,"Error! Image file is not set! (%s)"%(tex.name))

	return tex_name


def write_TexAColorOp(ofile, tex, mult, tex_name= None):
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


def write_TexCompMax(ofile, name, sourceA, sourceB):
	tex_name= "TexCompMax_%s"%(name)

	ofile.write("\nTexCompMax %s {"%(tex_name))
	ofile.write("\n\tsourceA= %s;"%(sourceA))
	ofile.write("\n\tsourceB= %s;"%(sourceB))
	ofile.write("\n\toperator= %d;"%(3)) # 0:Add, 1:Subtract, 2:Difference, 3:Multiply, 4:Divide, 5:Minimum, 6:Maximum
	ofile.write("\n}\n")

	return tex_name


def write_TexPlugin(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, ob= None, env= None, env_type= None):
	tex_name= "Texture_no_texture"

	if slot:
		tex= slot.texture

	vtex= tex.vray_texture

	if tex:
		plugin= get_plugin(TEX_PLUGINS, vtex.type)
		if plugin is not None:
			tex_name= plugin.write(ofile, sce, tex)

	return tex_name


def write_texture(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, env= None):
	if slot:
		tex= slot.texture
		
	tex_name= "Texture_no_texture"

	if tex.type == 'IMAGE':
		tex_name= write_TexBitmap(ofile, exported_bitmaps= exported_bitmaps, ma= ma, slot= slot, tex= tex, env= env)
	elif tex.type == 'VRAY':
		tex_name= write_TexPlugin(ofile, ma= ma, slot= slot, tex= tex, env= env)
	else:
		pass

	return tex_name


def write_textures(ofile, exported_bitmaps, ma, ma_name):
	vraytex= {}
	vraytex['color']= []
	vraytex['bump']= []
	vraytex['normal']= []
	vraytex['reflect']= []
	vraytex['reflect_glossiness']= []
	vraytex['hilight_glossiness']= []
	vraytex['refract']= []
	vraytex['reflect_glossiness']= []
	vraytex['alpha']= []
	vraytex['emit']= []
	vraytex['displace']= []
	vraytex['roughness']= []

	vraymat= {}
	vraymat['color']= None
	vraymat['color_mult']= 0.0
	vraymat['emit']= None
	vraymat['emit_mult']= 0.0
	vraymat['bump']= None
	vraymat['bump_amount']= 0.0
	vraymat['normal']= None
	vraymat['normal_amount']= 0.0
	vraymat['reflect']= None
	vraymat['reflect_mult']= 0.0
	vraymat['roughness']= None
	vraymat['roughness_mult']= 0.0
	vraymat['reflect_glossiness']= None
	vraymat['reflect_glossiness_mult']= 0.0
	vraymat['hilight_glossiness']= None
	vraymat['hilight_glossiness_mult']= 0.0
	vraymat['refract']= None
	vraymat['refract_mult']= 0.0
	vraymat['refract_glossiness']= None
	vraymat['refract_glossiness_mult']= 0.0
	vraymat['roughness_mult']= 0.0
	vraymat['alpha']= None
	vraymat['alpha_mult']= 0.0
	vraymat['displace']= None
	vraymat['displace_amount']= 0.0

	for slot_idx,slot in enumerate(ma.texture_slots):
		if ma.use_textures[slot_idx] and slot:
			if slot.texture:
				if slot.texture.type in TEX_TYPES:
					if slot.use_map_color_diffuse:
						vraytex['color'].append(slot)
						vraymat['color_mult']+= slot.diffuse_color_factor
					if slot.use_map_emit:
						vraytex['emit'].append(slot)
						vraymat['emit_mult']+= slot.emit_factor
					if slot.use_map_alpha:
						vraytex['alpha'].append(slot)
						vraymat['alpha_mult']+= slot.alpha_factor
					if slot.use_map_hardness:
						vraytex['roughness'].append(slot)
						vraymat['roughness_mult']+= slot.hardness_factor
					if slot.use_map_color_spec:
						vraytex['reflect_glossiness'].append(slot)
						vraymat['reflect_glossiness_mult']+= slot.specular_factor
					if slot.use_map_specular:
						vraytex['hilight_glossiness'].append(slot)
						vraymat['hilight_glossiness_mult']+= slot.colorspec_factor
					if slot.use_map_raymir:
						vraytex['reflect'].append(slot)
						vraymat['reflect_mult']+= slot.raymir_factor
					if slot.use_map_translucency:
						vraytex['refract'].append(slot)
						vraymat['refract_mult']+= slot.translucency_factor
					if slot.use_map_normal:
						if slot.texture.use_normal_map:
							vraytex['normal'].append(slot)
							vraymat['normal_amount']+= slot.normal_factor
						else:
							vraytex['bump'].append(slot)
							vraymat['bump_amount']+= slot.normal_factor
					if slot.use_map_displacement:
						vraytex['displace'].append(slot)
						vraymat['displace_amount']+= slot.displacement_factor

	for textype in vraytex:
		if len(vraytex[textype]):
			if len(vraytex[textype]) == 1:
				slot= vraytex[textype][0]
				tex= slot.texture

				debug(sce,"  Slot: %s"%(textype))
				debug(sce,"    Texture: %s"%(tex.name))

				vraymat[textype]= write_texture(ofile, exported_bitmaps, ma, slot)

				if textype == 'color':
					if slot.use_stencil:
						tex_name= "TexBlend_%s_%s"%(ma_name,vraymat[textype])
						ofile.write("\nTexBlend %s {"%(tex_name))
						ofile.write("\n\tcolor_a= %s;"%(a(sce,"AColor(%.3f,%.3f,%.3f,1.0)"%(tuple(ma.diffuse_color)))))
						ofile.write("\n\tcolor_b= %s;"%(vraymat[textype]))
						ofile.write("\n\tblend_amount= %s::out_alpha;"%(vraymat[textype]))
						ofile.write("\n\tcomposite= %d;"%(0))
						ofile.write("\n}\n")
						vraymat[textype]= tex_name
					if slot.diffuse_color_factor < 1.0:
						tex_name= "TexCombineColor_%s_%s"%(ma_name,vraymat[textype])
						ofile.write("\nTexCombineColor %s {"%(tex_name))
						ofile.write("\n\tcolor= %s;"%(a(sce,"AColor(%.3f,%.3f,%.3f,1.0)"%(tuple(ma.diffuse_color)))))
						ofile.write("\n\ttexture= %s;"%(vraymat[textype]))
						ofile.write("\n\ttexture_multiplier= %s;"%(a(sce,slot.diffuse_factor)))
						ofile.write("\n}\n")
						vraymat[textype]= tex_name

			else:
				BLEND_MODES= {
					'NONE':         0,
					'OVER':         1,
					'IN':           2,
					'OUT':          3,
					'ADD':          4,
					'SUBSTRACT':    5,
					'MULTIPLY':     6,
					'DIFFERENCE':   7,
					'LIGHTEN':      8,
					'DARKEN':       9,
					'SATURATE':    10,
					'DESATURATE':  11,
					'ILLUMINATE':  12
				}

				stencil= 0
				texlayered_modes= []
				texlayered_names= []

				for slot in vraytex[textype]:
					tex= slot.texture

					tex_name= write_texture(ofile, exported_bitmaps, ma, slot)

					texlayered_names.append(tex_name) # For stencil
					texlayered_modes.append(slot.blend_type)

					debug(sce,"  Slot: %s"%(textype))
					debug(sce,"    Texture: %s [mode: %s]"%(tex.name, slot.blend_type))
					
					if slot.use_stencil:
						stencil= vraytex[textype].index(slot)

				if stencil:
					tex_name= clean_string("Stencil_%s_%s_%s"%(textype, texlayered_names[stencil-1], texlayered_names[stencil+1]))
					ofile.write("\nTexBlend %s {"%(tex_name))
					ofile.write("\n\tcolor_a= %s;"%(texlayered_names[stencil-1]))
					ofile.write("\n\tcolor_b= %s;"%(texlayered_names[stencil+1]))
					ofile.write("\n\tblend_amount= %s::out_intensity;"%(texlayered_names[stencil]))
					ofile.write("\n\tcomposite= %d;"%(0))
					ofile.write("\n}\n")
				else:
					tex_name= "TexLayered_%s"%(textype)
					ofile.write("\nTexLayered %s {"%(tex_name))
					ofile.write("\n\ttextures= List(%s);"%(','.join(texlayered_names)))
					ofile.write("\n\tblend_modes= List(0, %s);"%(','.join(texlayered_modes)))
					ofile.write("\n}\n")

				vraymat[textype]= tex_name

	return vraymat


def write_BRDFVRayMtl(ofile, ma, ma_name, tex_vray):
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

	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFVRayMtl_%s"%(ma_name)

	ofile.write("\nBRDFVRayMtl %s {"%(brdf_name))
	ofile.write("\n\tbrdf_type= %s;"%(a(sce,BRDF_TYPE[BRDFVRayMtl.brdf_type])))

	if(tex_vray['alpha']):
		ofile.write("\n\topacity= %s::out_intensity;"%(tex_vray['alpha']))
	else:
		ofile.write("\n\topacity= %s;"%(a(sce,"%.6f"%(ma.alpha))))

	if(tex_vray['roughness']):
		ofile.write("\n\troughness= %s::out_intensity;"%(tex_vray['roughness']))
	else:
		ofile.write("\n\troughness= %s;"%(a(sce,"%.6f"%(BRDFVRayMtl.roughness))))

	if(tex_vray['color']):
		ofile.write("\n\tdiffuse= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tdiffuse= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.diffuse_color)))))

	if(tex_vray['reflect']):
		ofile.write("\n\treflect= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\treflect= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(BRDFVRayMtl.reflect_color)))))

	if(tex_vray['reflect_glossiness']):
		ofile.write("\n\treflect_glossiness= %s::out_intensity;"%(tex_vray['reflect_glossiness']))
	else:
		ofile.write("\n\treflect_glossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))

	if(tex_vray['hilight_glossiness']):
		ofile.write("\n\thilight_glossiness= %s::out_intensity;"%(tex_vray['hilight_glossiness']))
	else:
		ofile.write("\n\thilight_glossiness= %s;"%(a(sce,BRDFVRayMtl.hilight_glossiness)))

	if(tex_vray['refract']):
		ofile.write("\n\trefract= %s;"%(tex_vray['refract']))
	else:
		ofile.write("\n\trefract= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(BRDFVRayMtl.refract_color)))))

	for param in OBJECT_PARAMS['BRDFVRayMtl']:
		if param not in ('refract','opacity','diffuse','reflect','reflect_glossiness','hilight_glossiness','refract'):
			if param == 'translucency':
				value= TRANSLUCENSY[BRDFVRayMtl.translucency]
			elif param == 'option_glossy_rays_as_gi':
				value= GLOSSY_RAYS[BRDFVRayMtl.option_glossy_rays_as_gi]
			elif param == 'option_energy_mode':
				value= ENERGY_MODE[BRDFVRayMtl.option_energy_mode]
			else:
				value= getattr(BRDFVRayMtl,param)
			ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFBump(ofile, base_brdf, tex_vray):
	brdf_name= "BRDFBump_%s"%(base_brdf)

	ofile.write("\nBRDFBump %s {"%(brdf_name))
	ofile.write("\n\tbase_brdf= %s;"%(base_brdf))
	if(tex_vray['normal']):
		ofile.write("\n\tbump_tex_color= %s;"%(tex_vray['normal']))
		ofile.write("\n\tbump_tex_mult= %.6f;"%(tex_vray['normal_amount']))
	else:
		ofile.write("\n\tbump_tex_color= %s;"%(tex_vray['bump']))
		ofile.write("\n\tbump_tex_mult= %.6f;"%(tex_vray['bump_amount']))
	ofile.write("\n\tbump_shadows= 1;")
	if(tex_vray['normal']):
		ofile.write("\n\tmap_type= 2;")
	else:
		ofile.write("\n\tmap_type= 0;")
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFSSS2Complex(ofile, ma, ma_name, tex_vray):
	SINGLE_SCATTER= {
		'NONE':   0,
		'SIMPLE': 1,
		'SOLID':  2,
		'REFR':   3
	}

	BRDFSSS2Complex= ma.vray.BRDFSSS2Complex

	brdf_name= "BRDFSSS2Complex_%s"%(ma_name)

	ofile.write("\nBRDFSSS2Complex %s {"%(brdf_name))
	for param in OBJECT_PARAMS['BRDFSSS2Complex']:
		if param == 'single_scatter':
			value= SINGLE_SCATTER[BRDFSSS2Complex.single_scatter]
		else:
			value= getattr(BRDFSSS2Complex,param)
		ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	return brdf_name


def	write_material(ma, filters, object_params, ofile, name= None):
	ma_name= get_name(ma,"Material")
	if name:
		ma_name= name

	vma= ma.vray
	
	brdf_name= "BRDFDiffuse_no_material"

	tex_vray= write_textures(ofile, filters['exported_bitmaps'], ma, ma_name)

	if vma.type == 'EMIT':
		if vma.emitter_type == 'MESH':
			object_params['meshlight']['on']= True
			object_params['meshlight']['material']= ma
			object_params['meshlight']['texture']= tex_vray['emit'] if tex_vray['emit'] else tex_vray['color']
			return
	elif vma.type == 'VOL':
		object_params['volume']= {}
		for param in OBJECT_PARAMS['EnvironmentFog']:
			object_params['volume'][param]= getattr(vma.EnvironmentFog,param)
		return

	if tex_vray['displace']:
		object_params['displace']['texture']= tex_vray['displace']
		object_params['displace']['params']= []

	if ma in filters['exported_materials']:
		return
	else:
		filters['exported_materials'].append(ma)

	if vma.type == 'MTL':
		if sce.vray.exporter.compat_mode:
		 	brdf_name= write_BRDF(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFVRayMtl(ofile, ma, ma_name, tex_vray)
	elif vma.type == 'SSS':
		brdf_name= write_BRDFSSS2Complex(ofile, ma, ma_name, tex_vray)
	elif vma.type == 'EMIT' and vma.emitter_type == 'MTL':
		brdf_name= write_BRDFLight(ofile, sce, ma, ma_name, tex_vray)

	if vma.type not in ('EMIT','VOL'):
		if tex_vray['bump'] or tex_vray['normal']:
			brdf_name= write_BRDFBump(ofile, brdf_name, tex_vray)

	# Very ugly :(
	# TODO: Convert to stack
	if(vma.two_sided and vma.MtlWrapper.use and vma.MtlRenderStats.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		wrap_material= "MtlWrapper_%s"%(ma_name)
		wrap_base= ts_material
		rstat_material= ma_name
		rstat_base= wrap_material
	elif(vma.two_sided and vma.MtlRenderStats.use and not vma.MtlWrapper.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		rstat_base= ts_material
		rstat_material= ma_name
	elif(vma.two_sided and vma.MtlWrapper.use and not vma.MtlRenderStats.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		wrap_base= ts_material
		wrap_material= ma_name
	elif(not vma.two_sided and vma.MtlWrapper.use and vma.MtlRenderStats.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		wrap_material= "MtlWrapper_%s"%(ma_name)
		wrap_base= base_material
		rstat_material= ma_name
		rstat_base= wrap_material
	elif(not vma.two_sided and vma.MtlWrapper.use and not vma.MtlRenderStats.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		wrap_base= base_material
		wrap_material= ma_name
	elif(not vma.two_sided and not vma.MtlWrapper.use and vma.MtlRenderStats.use):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		rstat_material= ma_name
		rstat_base= base_material
	elif(vma.two_sided):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= ma_name
	else:
		base_material= ma_name

	ofile.write("\nMtlSingleBRDF %s {"%(base_material))
	ofile.write("\n\tbrdf= %s;"%(brdf_name))
	ofile.write("\n}\n")

	if vma.two_sided:
		ofile.write("\nMtl2Sided %s {"%(ts_material))
		ofile.write("\n\tfront= %s;"%(base_material))
		ofile.write("\n\tback= %s;"%(base_material))
		ofile.write("\n\ttranslucency= Color(1.0,1.0,1.0)*%.3f;"%(vma.two_sided_translucency))
		ofile.write("\n\tforce_1sided= 1;")
		ofile.write("\n}\n")

	if vma.MtlWrapper.use:
		ofile.write("\nMtlWrapper %s {"%(wrap_material))
		ofile.write("\n\tbase_material= %s;"%(wrap_base))
		for param in OBJECT_PARAMS['MtlWrapper']:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vma.MtlWrapper,param))))
		ofile.write("\n}\n")
		
	if vma.MtlRenderStats.use:
		ofile.write("\nMtlRenderStats %s {"%(rstat_material))
		ofile.write("\n\tbase_mtl= %s;"%(rstat_base))
		for param in OBJECT_PARAMS['MtlRenderStats']:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vma.MtlRenderStats,param))))
		ofile.write("\n}\n")


def write_materials(ofile,ob,filters,object_params):
	def get_brdf_type(ma):
		vma= ma.vray
		if vma.type == 'MTL':
			return 'BRDFVRayMtl'
		elif vma.type == 'SSS':
			return 'BRDFSSS2Complex'
		elif vma.type == 'EMIT':
			return 'BRDFLight'
		else:
			return ''

	def get_node_name(nt, node):
		nt_name= get_name(nt,"NodeTree")
		node_name= "%s_%s"%(nt_name, clean_string(node.name))
		return node_name

	def find_connected_node(nt, ns):
		for n in nt.links:
			if(n.to_socket == ns):
				return n.from_node
		return None

	def write_node(ofile, ma, nt, no):
		debug(sce,"  Writing node: %s [%s]"%(no.name, no.type))
		
		if(no.type == 'OUTPUT'):
			brdf_name= "BRDFDiffuse_no_material"

			for ns in no.inputs:
				if(ns.name == 'Color'):
					color= find_connected_node(nt, ns)
					brdf_name= "%s_%s_%s"%(ma.name, nt.name, color.name)

			ofile.write("\nMtlSingleBRDF %s {"%(get_name(ma,'Material')))
			ofile.write("\n\tbrdf= %s;"%(clean_string(brdf_name)))
			ofile.write("\n}\n")

		elif(no.type in ('MATERIAL','MATERIAL_EXT')):
			write_material(no.material, filters, object_params, ofile)

		elif(no.type == 'MIX_RGB'):
			color1= "BRDFDiffuse_no_material"
			color2= "BRDFDiffuse_no_material"
			fac= "Color(0.5,0.5,0.5)"

			brdf_name= "%s_%s_%s"%(ma.name, nt.name, no.name)

			for ns in no.inputs:
				if(ns.name == 'Color1'):
					node_color1= find_connected_node(nt, ns)
				elif(ns.name == 'Color2'):
					node_color2= find_connected_node(nt, ns)
				else:
					fac= "Color(1.0,1.0,1.0)*%.3f"%(1.0 - ns.default_value[0])
					node_fac= find_connected_node(nt, ns)

			if(node_color1):
				if(node_color1.type in ('MATERIAL','MATERIAL_EXT')):
					color1= get_name(node_color1.material,'%s_Material' % get_brdf_type(node_color1.material))

			if(node_color2):
				if(node_color2.type in ('MATERIAL','MATERIAL_EXT')):
					color2= get_name(node_color2.material,'%s_Material' % get_brdf_type(node_color2.material))
				
			if(node_fac):
				if(node_fac.type == 'TEXTURE'):
					weights= write_texture(ofile, ma= ma, tex= node_fac.texture)
			else:
				weights= "weights_%s"%(clean_string(brdf_name))
				ofile.write("\nTexAColor %s {"%(weights))
				ofile.write("\n\tuvwgen= UVWGenChannel_default;")
				ofile.write("\n\ttexture= %s;"%(fac))
				ofile.write("\n}\n")

			ofile.write("\nBRDFLayered %s {"%(clean_string(brdf_name)))
			ofile.write("\n\tbrdfs= List(%s, %s);"%(color1, color2))
			ofile.write("\n\tweights= List(%s, TexAColor_default_blend);"%(weights))
			ofile.write("\n\tadditive_mode= 0;") # Shellac
			ofile.write("\n}\n")
				
		elif(no.type == 'TEXTURE'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		elif(no.type == 'INVERT'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(no.name,no.type))

	if len(ob.material_slots):
		for slot in ob.material_slots:
			ma= slot.material
			if ma:
				if sce.vray.exporter.use_material_nodes and ma.use_nodes and hasattr(ma.node_tree, 'links'):
					debug(sce,"Writing node material: %s"%(ma.name))
					nt= ma.node_tree
					for n in nt.nodes:
						if(n.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT')):
							write_node(ofile, ma, nt, n)
						else:
							debug(sce,"Node: %s (unsupported node type: %s)"%(n.name, n.type))
				else:
					write_material(ma, filters, object_params, ofile)

	ma_name= "Material_no_material"
	if len(ob.material_slots):
		if len(ob.material_slots) == 1:
			if ob.material_slots[0].material is not None:
				ma_name= get_name(ob.material_slots[0].material, "Material")
		else:
			ma_name= write_multi_material(ofile, ob)
	return ma_name


def write_LightMesh(ofile, ob, params, name, geometry, matrix):
	plugin= 'LightMesh'

	ma=  params['material']
	tex= params['texture']

	light= getattr(ma.vray,plugin)

	ofile.write("\n%s %s {" % (plugin,name))
	ofile.write("\n\ttransform= %s;"%(a(sce,transform(matrix))))
	for param in OBJECT_PARAMS[plugin]:
		if param == 'color':
			if tex:
				ofile.write("\n\tcolor= %s;"%(tex))
			else:
				ofile.write("\n\tcolor= %s;"%(a(sce,ma.diffuse_color)))
		elif param == 'geometry':
			ofile.write("\n\t%s= %s;"%(param, geometry))
		elif param == 'units':
			ofile.write("\n\t%s= %i;"%(param, UNITS[light.units]))
		elif param == 'lightPortal':
			ofile.write("\n\t%s= %i;"%(param, LIGHT_PORTAL[light.lightPortal]))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(light,param))))
	ofile.write("\n}\n")


def write_object(ob, params, add_params= None):
	props= {
		'filters': None,
		'types':   None,
		'files':   None,

		'visible': True,

		'dupli':        False,
		'dupli_group':  False,
		'dupli_name':   None,

		'matrix': None,
	}

	for key in params:
		props[key]= params[key]

	if add_params is not None:
		for key in add_params:
			props[key]= add_params[key]

	ofile= props['files']['nodes']

	ve= sce.vray.exporter

	# TMP
	types= props['types']
	files= props['files']
	
	# if ob in props['filters']['exported_nodes']:
	#  	continue
	# props['filters']['exported_nodes'].append(ob)

	object_params= {
		'meshlight': {
			'on':       False,
			'material': None
		},
		'displace': {
			'texture':  None,
			'params':   None
		},
		'volume': None
	}

	node_name= get_name(ob,"Node",dupli_name= props['dupli_name'])
	ma_name= write_materials(props['files']['materials'],ob,props['filters'],object_params)

	debug(sce, "Object[%s]: %s" % (ob.name,object_params))

	vo= ob.vray
	vd= ob.data.vray

	node_geometry= get_name(ob.data,"Geom")
	if hasattr(vd,'GeomMeshFile'):
		if vd.GeomMeshFile.use:
			node_geometry= write_mesh_file(ofile, props['filters']['exported_proxy'], ob)

	if object_params['displace']['texture'] is not None:
		node_geometry= write_mesh_displace(ofile, node_geometry, object_params['displace'])

	node_matrix= ob.matrix_world
	if props['matrix'] is not None:
		if props['dupli_group']:
			node_matrix= props['matrix'] * ob.matrix_world
		else:
			node_matrix= props['matrix']

	if object_params['meshlight']['on']:
		write_LightMesh(files['lamps'], ob, object_params['meshlight'], node_name, node_geometry, node_matrix)
		return

	if object_params['volume'] is not None:
		if ma_name not in types['volume'].keys():
			types['volume'][ma_name]= {}
			types['volume'][ma_name]['params']= object_params['volume']
			types['volume'][ma_name]['gizmos']= []
		if ob not in types['volume'][ma_name]:
			types['volume'][ma_name]['gizmos'].append(write_EnvFogMeshGizmo(files['nodes'], node_name, node_geometry, node_matrix))
		return

	MtlRenderStats= vo.MtlRenderStats
	render_stats= {
		'camera_visibility':      MtlRenderStats.camera_visibility,
		'reflections_visibility': MtlRenderStats.reflections_visibility,
		'refractions_visibility': MtlRenderStats.refractions_visibility,
		'gi_visibility':          MtlRenderStats.gi_visibility,
		'shadows_visibility':     MtlRenderStats.shadows_visibility,
		'visibility':             MtlRenderStats.visibility
	}

	def write_node(ofile,name,geometry,material,object_id,visibility,transform_matrix):
		ofile.write("\nNode %s {"%(name))
		ofile.write("\n\tobjectID= %d;"%(object_id))
		ofile.write("\n\tgeometry= %s;"%(geometry))
		ofile.write("\n\tmaterial= %s;"%(material))
		ofile.write("\n\tvisible= %s;"%(a(sce,visibility)))
		ofile.write("\n\ttransform= %s;"%(a(sce,transform(transform_matrix))))
		ofile.write("\n}\n")

	if len(ob.particle_systems):
		use_render_emitter= False
		for ps in ob.particle_systems:
			if ps.settings.type == 'HAIR':
				if ps.settings.use_render_emitter:
					use_render_emitter= True
				if ve.use_hair:
					hair_geom_name= "HAIR_%s" % ps.name
					hair_node_name= "%s_%s" % (node_name,hair_geom_name)
					write_GeomMayaHair(ofile,ob,ps,hair_geom_name)
					write_node(ofile, hair_node_name, hair_geom_name, get_name(ob.material_slots[ps.material].material,"Material"), ob.pass_index, props['visible'], node_matrix)
		if use_render_emitter:
			write_node(ofile,node_name,node_geometry,ma_name,ob.pass_index,props['visible'],node_matrix)
	else:
		write_node(ofile,node_name,node_geometry,ma_name,ob.pass_index,props['visible'],node_matrix)


def write_environment(ofile, volumes= None):
	wo= sce.world

	bg_tex= None
	gi_tex= None
	reflect_tex= None
	refract_tex= None

	bg_tex_mult= 1.0
	gi_tex_mult= 1.0
	reflect_tex_mult= 1.0
	refract_tex_mult= 1.0

	for slot in wo.texture_slots:
		if slot:
			if slot.texture:
				if slot.texture.type in TEX_TYPES:
					if slot.use_map_blend:
						bg_tex= write_texture(ofile, slot= slot, env=True)
						bg_tex_mult= slot.blend_factor
					if slot.use_map_horizon:
						gi_tex= write_texture(ofile, slot= slot, env=True)
						gi_tex_mult= slot.horizon_factor
					if slot.use_map_zenith_up:
						reflect_tex= write_texture(ofile, slot= slot, env=True)
						reflect_tex_mult= slot.zenith_up_factor
					if slot.use_map_zenith_down:
						refract_tex= write_texture(ofile, slot= slot, env=True)
						refract_tex_mult= slot.zenith_down_factor

	ofile.write("\nSettingsEnvironment {")
	ofile.write("\n\tbg_color= %s;"%(a(sce,wo.vray.bg_color)))
	if bg_tex:
		ofile.write("\n\tbg_tex= %s;"%(bg_tex))
		ofile.write("\n\tbg_tex_mult= %s;"%(a(sce,bg_tex_mult)))
	if wo.vray.gi_override:
		ofile.write("\n\tgi_color= %s;"%(a(sce,wo.vray.gi_color)))
	if gi_tex:
		ofile.write("\n\tgi_tex= %s;"%(gi_tex))
		ofile.write("\n\tgi_tex_mult= %s;"%(a(sce,gi_tex_mult)))
	if wo.vray.reflection_override:
		ofile.write("\n\treflect_color= %s;"%(a(sce,wo.vray.reflection_color)))
	if reflect_tex:
		ofile.write("\n\treflect_tex= %s;"%(reflect_tex))
		ofile.write("\n\treflect_tex_mult= %s;"%(a(sce,reflect_tex_mult)))
	if wo.vray.refraction_override:
		ofile.write("\n\trefract_color= %s;"%(a(sce,wo.vray.refraction_color)))
	if refract_tex:
		ofile.write("\n\trefract_tex= %s;"%(refract_tex))
		ofile.write("\n\trefract_tex_mult= %s;"%(a(sce,refract_tex_mult)))
	if volumes:
		ofile.write("\n\tenvironment_volume= List(%s);"%(','.join(volumes)))
	ofile.write("\n}\n")


def write_EnvironmentFog(ofile,volume,material):
	LIGHT_MODE= {
		'ADDGIZMO':    4,
		'INTERGIZMO':  3,
		'OVERGIZMO':   2,
		'PERGIZMO':    1,
		'NO':          0
	}

	plugin= 'EnvironmentFog'
	name= "%s_%s" % (plugin,material)

	ofile.write("\n%s %s {"%(plugin,name))
	ofile.write("\n\tgizmos= List(%s);" % ','.join(volume[material]['gizmos']))
	#ofile.write("\n\tdensity_tex= Texture_Test_Checker::out_intensity;")
	for param in volume[material]['params']:
		value= volume[material]['params'][param]
		if param == 'light_mode':
			value= LIGHT_MODE[value]
		ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	return name


def write_EnvFogMeshGizmo(ofile, node_name, node_geometry, node_matrix):
	plugin= 'EnvFogMeshGizmo'
	name= "%s_%s" % (plugin,node_name)

	ofile.write("\n%s %s {"%(plugin,name))
	ofile.write("\n\ttransform= %s;"%(a(sce,transform(node_matrix))))
	ofile.write("\n\tgeometry= %s;"%(node_geometry))
	#ofile.write("\n\tlights= %s;"%())
	#ofile.write("\n\tfade_out_radius= %s;"%())
	ofile.write("\n}\n")

	return name


def write_lamp(ob, params, add_params= None):
	ofile= params['files']['lamps']
	
	lamp= ob.data
	vl= lamp.vray

	lamp_type= None
	lamp_name= ob.name
	lamp_matrix= ob.matrix_world

	if add_params is not None:
		if 'dupli_name' in add_params:
			lamp_name= "%s_%s" % (add_params['dupli_name'],lamp_name)
		if 'matrix' in add_params:
			lamp_matrix= add_params['matrix']

	if lamp.type == 'POINT':
		if vl.radius > 0:
			lamp_type= 'LightSphere'
		else:
			lamp_type= 'LightOmni'
	elif lamp.type == 'SPOT':
		if vl.spot_type == 'SPOT':
			lamp_type= 'LightSpot'
		else:
			lamp_type= 'LightIES'
	elif lamp.type == 'SUN':
		if vl.direct_type == 'DIRECT':
			lamp_type= 'LightDirect'
		else:
			lamp_type= 'SunLight'
	elif lamp.type == 'AREA':
		lamp_type= 'LightRectangle'
	elif lamp.type == 'HEMI':
		lamp_type= 'LightDome'
	else:
		return

	ofile.write("\n%s %s_%s {"%(lamp_type,lamp_type,clean_string(lamp_name)))

	if lamp_type == 'SunLight':
		ofile.write("\n\tsky_model= %i;"%(SKY_MODEL[vl.sky_model]))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(lamp.color)))))
		if lamp_type != 'LightIES':
			ofile.write("\n\tunits= %i;"%(UNITS[vl.units]))

	if lamp_type == 'LightRectangle':
		if lamp.shape == 'RECTANGLE':
			ofile.write("\n\tu_size= %s;"%(a(sce,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(sce,lamp.size_y/2)))
		else:
			ofile.write("\n\tu_size= %s;"%(a(sce,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(sce,lamp.size/2)))
		ofile.write("\n\tlightPortal= %i;"%(LIGHT_PORTAL[vl.lightPortal]))

	for param in OBJECT_PARAMS[lamp_type]:
		if lamp_type == 'LightIES':
			if param == 'intensity':
				ofile.write("\n\tpower= %s;"%(a(sce,vl.intensity)))
				continue
			elif param == 'ies_file':
				ofile.write("\n\t%s= \"%s\";"%(param,get_full_filepath(vl.ies_file)))
				continue
		if param == 'shadow_subdivs':
			ofile.write("\n\tshadow_subdivs= %s;"%(a(sce,vl.subdivs)))
		elif param == 'shadow_color':
			ofile.write("\n\tshadow_color= %s;"%(a(sce,vl.shadowColor)))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vl,param))))

	ofile.write("\n\ttransform= %s;"%(a(sce,transform(lamp_matrix))))
	ofile.write("\n}\n")


def write_camera(sce, ofile, camera= None):
	ca= camera if camera is not None else sce.camera

	if ca is not None:
		VRayCamera= ca.data.vray
		SettingsCamera= VRayCamera.SettingsCamera
		CameraPhysical= VRayCamera.CameraPhysical

		wx= sce.render.resolution_x * sce.render.resolution_percentage / 100
		wy= sce.render.resolution_y * sce.render.resolution_percentage / 100

		aspect= float(wx) / float(wy)

		fov= ca.data.angle
		if aspect < 1.0:
			fov= fov * aspect

		ofile.write("\nRenderView RenderView {")
		ofile.write("\n\ttransform= %s;"%(a(sce,transform(ca.matrix_world))))
		ofile.write("\n\tfov= %s;"%(a(sce,fov)))
		ofile.write("\n\tclipping= 1;")
		ofile.write("\n\tclipping_near= %s;"%(a(sce,ca.data.clip_start)))
		ofile.write("\n\tclipping_far= %s;"%(a(sce,ca.data.clip_end)))
		ofile.write("\n}\n")

		if VRayCamera.mode == 'PHYSICAL':
			focus_distance= ca.data.dof_distance
			if focus_distance == 0.0:
				focus_distance= 200.0

			ofile.write("\nCameraPhysical {")
			ofile.write("\n\ttype= %d;"%(PHYS[CameraPhysical.type]))
			ofile.write("\n\ttargeted= 0;")
			ofile.write("\n\tspecify_focus= 1;")
			ofile.write("\n\tfocus_distance= %s;"%(a(sce,focus_distance)))
			ofile.write("\n\tspecify_fov= 1;")
			ofile.write("\n\tfov= %s;"%(a(sce,fov)))
			ofile.write("\n\twhite_balance= %s;"%(a(sce,"Color(%.3f,%.3f,%.3f)"%(tuple(CameraPhysical.white_balance)))))
			for param in OBJECT_PARAMS['CameraPhysical']:
				ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(CameraPhysical,param))))
			ofile.write("\n}\n")

		else:
			ofile.write("\nSettingsCamera {")
			ofile.write("\n\ttype= %i;"%(0))
			ofile.write("\n\tfov= %s;"%(a(sce,fov)))
			ofile.write("\n}\n")


def write_settings(sce,ofile):
	rd= sce.render
	
	VRayScene= sce.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR
	
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Scene file\n\n")

	for f in ('geometry', 'materials', 'lights', 'nodes', 'camera'):
		if VRayDR.on:
			ofile.write("#include \"%s\"\n" % ('..' + os.path.join(bpy.path.abspath(VRayExporter.output_dir),os.path.basename(get_filenames(sce,f)))))
		else:
			ofile.write("#include \"%s\"\n"%(os.path.basename(get_filenames(sce,f))))
			
	wx= rd.resolution_x * rd.resolution_percentage / 100
	wy= rd.resolution_y * rd.resolution_percentage / 100
		
	ofile.write("\nSettingsOutput {")
	ofile.write("\n\timg_separateAlpha= %d;"%(0))
	ofile.write("\n\timg_width= %s;"%(int(wx)))
	ofile.write("\n\timg_height= %s;"%(int(wy)))
	if VRayExporter.animation:
		ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(sce.camera.name),get_render_file_format(VRayExporter,rd.file_format)))
		ofile.write("\n\timg_dir= \"%s\";"%(get_filenames(sce,'output')))
		ofile.write("\n\timg_file_needFrameNumber= 1;")
		ofile.write("\n\tanim_start= %d;"%(sce.frame_start))
		ofile.write("\n\tanim_end= %d;"%(sce.frame_end))
		ofile.write("\n\tframe_start= %d;"%(sce.frame_start))
		ofile.write("\n\tframes_per_second= %d;"%(1.0) )
		ofile.write("\n\tframes= %d-%d;"%(sce.frame_start, sce.frame_end))
	ofile.write("\n\tframe_stamp_enabled= %d;"%(0))
	ofile.write("\n\tframe_stamp_text= \"%s\";"%("vb25 (git) | V-Ray Standalone %%vraycore | %%rendertime"))
	ofile.write("\n}\n")

	module= VRayScene.SettingsImageSampler
	if module.filter_type != 'NONE':
		ofile.write(AA_FILTER_TYPE[module.filter_type])
		ofile.write("\n\tsize= %.3f;"%(module.filter_size))
		ofile.write("\n}\n")

	for module in MODULES:
		vmodule= getattr(VRayScene, module)

		ofile.write("\n%s {"%(module))
		if module == 'SettingsImageSampler':
			ofile.write("\n\ttype= %d;"%(IMAGE_SAMPLER_TYPE[vmodule.type]))
		elif module == 'SettingsColorMapping':
			ofile.write("\n\ttype= %d;"%(COLOR_MAPPING_TYPE[vmodule.type]))
		elif module == 'SettingsRegionsGenerator':
			ofile.write("\n\tseqtype= %d;"%(SEQTYPE[vmodule.seqtype]))
			ofile.write("\n\txymeans= %d;"%(XYMEANS[vmodule.xymeans]))

		for param in MODULES[module]:
			ofile.write("\n\t%s= %s;"%(param, p(getattr(vmodule, param))))
		ofile.write("\n}\n")

	for plugin in SETTINGS_PLUGINS:
		if hasattr(VRayScene,plugin.PLUG):
			rna_pointer= getattr(VRayScene,plugin.PLUG)
			if hasattr(plugin,'write'):
				plugin.write(ofile,sce,rna_pointer)

	dmc= VRayScene.SettingsDMCSampler
	gi=  VRayScene.SettingsGI
	im=  VRayScene.SettingsGI.SettingsIrradianceMap
	lc=  VRayScene.SettingsGI.SettingsLightCache
	bf=  VRayScene.SettingsGI.SettingsDMCGI
	if gi.on:
		ofile.write("\nSettingsGI {")
		ofile.write("\n\ton= 1;")
		ofile.write("\n\tprimary_engine= %s;"%(PRIMARY[gi.primary_engine]))
		ofile.write("\n\tsecondary_engine= %s;"%(SECONDARY[gi.secondary_engine]))
		ofile.write("\n\tprimary_multiplier= %s;"%(gi.primary_multiplier))
		ofile.write("\n\tsecondary_multiplier= %s;"%(gi.secondary_multiplier))
		ofile.write("\n\treflect_caustics= %s;"%(p(gi.reflect_caustics)))
		ofile.write("\n\trefract_caustics= %s;"%(p(gi.refract_caustics)))
		ofile.write("\n\tsaturation= %.6f;"%(gi.saturation))
		ofile.write("\n\tcontrast= %.6f;"%(gi.contrast))
		ofile.write("\n\tcontrast_base= %.6f;"%(gi.contrast_base))
		ofile.write("\n}\n")

		ofile.write("\nSettingsIrradianceMap {")
		ofile.write("\n\tmin_rate= %i;"%(im.min_rate))
		ofile.write("\n\tmax_rate= %i;"%(im.max_rate))
		ofile.write("\n\tsubdivs= %i;"%(im.subdivs))
		ofile.write("\n\tinterp_samples= %i;"%(im.interp_samples))
		ofile.write("\n\tinterp_frames= %i;"%(im.interp_frames))
		ofile.write("\n\tcalc_interp_samples= %i;"%(im.calc_interp_samples))
		ofile.write("\n\tcolor_threshold= %.6f;"%(im.color_threshold))
		ofile.write("\n\tnormal_threshold= %.6f;"%(im.normal_threshold))
		ofile.write("\n\tdistance_threshold= %.6f;"%(im.distance_threshold))
		ofile.write("\n\tdetail_enhancement= %i;"%(im.detail_enhancement))
		ofile.write("\n\tdetail_radius= %.6f;"%(im.detail_radius))
		ofile.write("\n\tdetail_subdivs_mult= %.6f;"%(im.detail_subdivs_mult))
		ofile.write("\n\tdetail_scale= %i;"%(SCALE[im.detail_scale]))
		ofile.write("\n\tinterpolation_mode= %i;"%(INT_MODE[im.interpolationType]))
		ofile.write("\n\tlookup_mode= %i;"%(LOOK_TYPE[im.lookupType]))
		ofile.write("\n\tshow_calc_phase= %i;"%(im.show_calc_phase))
		ofile.write("\n\tshow_direct_light= %i;"%(im.show_direct_light))
		ofile.write("\n\tshow_samples= %i;"%(im.show_samples))
		ofile.write("\n\tmultipass= %i;"%(im.multipass))
		ofile.write("\n\tcheck_sample_visibility= %i;"%(im.check_sample_visibility))
		ofile.write("\n\trandomize_samples= %i;"%(im.randomize_samples))
		ofile.write("\n\tmode= %d;"%(IM_MODE[im.mode]))
		ofile.write("\n\tauto_save= %d;"%(im.auto_save))
		ofile.write("\n\tauto_save_file= \"%s\";"%(bpy.path.abspath(im.auto_save_file)))
		ofile.write("\n\tfile= \"%s\";"%(im.file))
		ofile.write("\n}\n")

		ofile.write("\nSettingsDMCGI {")
		ofile.write("\n\tsubdivs= %i;"%(bf.subdivs))
		ofile.write("\n\tdepth= %i;"%(bf.depth))
		ofile.write("\n}\n")

		ofile.write("\nSettingsLightCache {")
		ofile.write("\n\tsubdivs= %.0f;"%(lc.subdivs * dmc.subdivs_mult))
		ofile.write("\n\tsample_size= %.6f;"%(lc.sample_size))
		ofile.write("\n\tnum_passes= %i;"%(lc.num_passes))
		ofile.write("\n\tdepth= %i;"%(lc.depth))
		ofile.write("\n\tfilter_type= %i;"%(LC_FILT[lc.filter_type]))
		ofile.write("\n\tfilter_samples= %i;"%(lc.filter_samples))
		ofile.write("\n\tfilter_size= %.6f;"%(lc.filter_size))
		ofile.write("\n\tprefilter= %i;"%(lc.prefilter))
		ofile.write("\n\tprefilter_samples= %i;"%(lc.prefilter_samples))
		ofile.write("\n\tshow_calc_phase= %i;"%(lc.show_calc_phase))
		ofile.write("\n\tstore_direct_light= %i;"%(lc.store_direct_light))
		ofile.write("\n\tuse_for_glossy_rays= %i;"%(lc.use_for_glossy_rays))
		ofile.write("\n\tworld_scale= %i;"%(SCALE[lc.scale]))
		ofile.write("\n\tadaptive_sampling= %i;"%(lc.adaptive_sampling))
		ofile.write("\n\tmode= %d;"%(LC_MODE[lc.mode]))
		ofile.write("\n\tauto_save= %d;"%(lc.auto_save))
		ofile.write("\n\tauto_save_file= \"%s\";"%(bpy.path.abspath(lc.auto_save_file)))
		ofile.write("\n\tfile= \"%s\";"%(lc.file))
		ofile.write("\n}\n")

	ofile.write("\nSettingsEXR {")
	ofile.write("\n\tcompression= 0;") # 0 - default, 1 - no compression, 2 - RLE, 3 - ZIPS, 4 - ZIP, 5 - PIZ, 6 - pxr24
	ofile.write("\n\tbits_per_channel= 32;")
	ofile.write("\n}\n")

	# ofile.write("\nRTEngine {")
	# ofile.write("\n\tseparate_window= 1;")
	# ofile.write("\n\ttrace_depth= 3;")
	# ofile.write("\n\tuse_gi= 1;")
	# ofile.write("\n\tgi_depth= 3;")
	# ofile.write("\n\tgi_reflective_caustics= 1;")
	# ofile.write("\n\tgi_refractive_caustics= 1;")
	# ofile.write("\n\tuse_opencl= 0;")
	# ofile.write("\n}\n"	)	

	for channel in VRayScene.render_channels:
		plugin= get_plugin(CHANNEL_PLUGINS, channel.type)
		if plugin is not None:
			plugin.write(ofile, getattr(channel,plugin.PLUG), name= channel.name)

	ofile.write("\n")


def write_scene(sce):
	VRayScene= sce.vray
	VRayExporter= VRayScene.exporter

	ca= sce.camera
	vc= ca.data.vray.SettingsCamera

	files= {
		'lamps':     open(get_filenames(sce,'lights'), 'w'),
		'materials': open(get_filenames(sce,'materials'), 'w'),
		'nodes':     open(get_filenames(sce,'nodes'), 'w'),
		'camera':    open(get_filenames(sce,'camera'), 'w'),
		'scene':     open(get_filenames(sce,'scene'), 'w')
	}

	types= {
		'volume': {}
	}

	files['materials'].write("\nUVWGenChannel UVWGenChannel_default {")
	files['materials'].write("\n\tuvw_channel= 1;")
	files['materials'].write("\n\tuvw_transform= Transform(")
	files['materials'].write("\n\t\tMatrix(")
	files['materials'].write("\n\t\t\tVector(1.0,0.0,0.0)*5,")
	files['materials'].write("\n\t\t\tVector(0.0,1.0,0.0)*5,")
	files['materials'].write("\n\t\t\tVector(0.0,0.0,1.0)")
	files['materials'].write("\n\t\t),")
	files['materials'].write("\n\t\tVector(0.0,0.0,0.0)")
	files['materials'].write("\n\t);")
	files['materials'].write("\n}\n")
	files['materials'].write("\nTexChecker Texture_Test_Checker {")
	files['materials'].write("\n\tuvwgen= UVWGenChannel_default;")
	files['materials'].write("\n}\n")
	files['materials'].write("\nTexChecker Texture_no_texture {")
	files['materials'].write("\n\tuvwgen= UVWGenChannel_default;")
	files['materials'].write("\n}\n")
	files['materials'].write("\nBRDFDiffuse BRDFDiffuse_no_material {")
	files['materials'].write("\n\tcolor=Color(0.5, 0.5, 0.5);")
	files['materials'].write("\n}\n")
	files['materials'].write("\nMtlSingleBRDF Material_no_material {")
	files['materials'].write("\n\tbrdf= BRDFDiffuse_no_material;")
	files['materials'].write("\n}\n")
	files['materials'].write("\nTexAColor TexAColor_default_blend {")
	files['materials'].write("\n\tuvwgen= UVWGenChannel_default;")
	files['materials'].write("\n\ttexture= Color(1.0,1.0,1.0);")
	files['materials'].write("\n}\n")

	# ca= sce.camera
	# vca= ca.data.vray

	# if vca.hide_from_view:
	# 	if vca.hide_from_everything:
	# 		if vca.everything_auto:
	# 			auto_group= 'hidefrom_%s' % ca.name
	# 			try:
	# 				for group_ob in bpy.data.groups[auto_group].objects:
	# 					HIDE_FROM_VIEW.append(group_ob.name)
	# 			except:
	# 				debug(sce,"Group \"%s\" doesn\'t exist" % auto_group)
	# 		else:
	# 			HIDE_FROM_VIEW= vca.everything_objects.split(';')
	# 			for gr in vca.everything_groups.split(';'):
	# 				try:
	# 					for group_ob in bpy.data.groups[gr].objects:
	# 						HIDE_FROM_VIEW.append(group_ob.name)
	# 				except:
	# 					debug(sce,"Group \"%s\" doesn\'t exist" % gr)
	# 			debug(sce,"Hide from view \"%s\": %s" % (ca.name,HIDE_FROM_VIEW))
	# 	else:
	# 		pass
	# for ob in OBJECTS:
	# 	visible= True
	# 	if vca.hide_from_view:
	# 		if vca.hide_from_everything:
	# 			if ob.name in HIDE_FROM_VIEW:
	# 				visible= False

	def _write_object_dupli(ob, params, add_params= None):
		if ob.dupli_type in ('VERTS','FACES','GROUP'):
			ob.create_dupli_list(sce)
			for dup_id,dup_ob in enumerate(ob.dupli_list):
				dup_name= "%s_%s" % (ob.name,dup_id)
				_write_object(dup_ob.object, params, {'dupli': True, 'dupli_name': dup_name, 'matrix': dup_ob.matrix})
			ob.free_dupli_list()
		else:
			return

	def _write_object(ob, params, add_params= None):
		if ob.type == 'LAMP':
			write_lamp(ob,params,add_params)
		elif ob.type == 'EMPTY':
			_write_object_dupli(ob,params,add_params)
		else:
			_write_object_dupli(ob,params,add_params)
			write_object(ob,params,add_params)

	def write_frame():
		params= {}
		params['files']= files
		params['filters']= {
			'exported_bitmaps':   [],
			'exported_materials': [],
			'exported_proxy':     []
		}
		params['types']= types

		write_environment(params['files']['nodes']) # TEMP
		write_camera(sce,params['files']['camera'])
	
		for ob in sce.objects:
			if ob.type in ('CAMERA','ARMATURE'):
				continue

			if VRayExporter.active_layers:
				if not object_on_visible_layers(sce,ob):
					continue

			debug(sce,"[%s]: %s"%(ob.type,ob.name))
			debug(sce,"  Animated: %d"%(1 if ob.animation_data else 0))
			if hasattr(ob,'data'):
				if ob.data:
					debug(sce,"  Data animated: %d"%(1 if ob.data.animation_data else 0))
			if not VRayExporter.debug:
				if PLATFORM == "win32":
					sys.stdout.write("V-Ray/Blender: [%d] %s: %s                              \r"%(sce.frame_current, ob.type, ob.name))
				else:
					sys.stdout.write("V-Ray/Blender: [%d] %s: \033[0;32m%s\033[0m                              \r"%(sce.frame_current, ob.type, ob.name))
				sys.stdout.flush()

			_write_object(ob, params)

		del params

	sys.stdout.write("V-Ray/Blender: Writing scene...\n")
	timer= time.clock()

	if VRayExporter.animation:
		selected_frame= sce.frame_current
		f= sce.frame_start
		while(f <= sce.frame_end):
			sce.set_frame(f)
			write_frame()
			f+= sce.frame_step
		sce.set_frame(selected_frame)
	else:
		write_frame()

	if len(types['volume']):
		write_environment(files['nodes'],[write_EnvironmentFog(files['nodes'],types['volume'],vol) for vol in types['volume']])

	write_settings(sce,files['scene'])

	for key in files:
		files[key].close()

	sys.stdout.write("V-Ray/Blender: Writing scene done. [%s]                    \n" % (time.clock() - timer))
	sys.stdout.flush()



'''
  V-Ray Renderer
'''
class SCENE_OT_vray_export_meshes(bpy.types.Operator):
	bl_idname = "vray_export_meshes"
	bl_label = "Export meshes"
	bl_description = "Export Meshes"

	def invoke(self, context, event):
		sce= context.scene

		write_geometry(sce, get_filenames(sce,'geometry'))

		return{'FINISHED'}


class SCENE_OT_vray_create_proxy(bpy.types.Operator):
	bl_idname = "vray_create_proxy"
	bl_label = "Create proxy"
	bl_description = "Creates proxy from selection."

	def invoke(self, context, event):
		print("V-Ray/Blender: Proxy Creator is in progress...")

		return{'FINISHED'}


class SCENE_OT_vray_replace_proxy(bpy.types.Operator):
	bl_idname = "vray_replace_with_proxy"
	bl_label = "Replace with proxy"
	bl_description = "Create proxy and replace current object\'s mesh by simple mesh."

	def invoke(self, context, event):
		print("V-Ray/Blender: Proxy Creator is in progress...")

		return{'FINISHED'}


class VRayRenderer(bpy.types.RenderEngine):
	bl_idname  = 'VRAY_RENDER'
	bl_label   = 'V-Ray'
	bl_use_preview = False
	
	def render(self, scene):
		global sce

		sce= scene
		rd=  scene.render
		wo=  scene.world

		# TEMP
		if rd.display_mode != 'AREA':
			rd.display_mode= 'AREA'

		vsce= sce.vray
		ve= vsce.exporter
		dr= vsce.VRayDR

		if ve.auto_meshes:
			write_geometry(sce, get_filenames(sce,'geometry'))
		write_scene(sce)

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(get_filenames(sce,'output'),"render.%s" % get_render_file_format(ve,rd.file_format))
		load_file= os.path.join(get_filenames(sce,'output'),"render.%.4i.%s" % (sce.frame_current,get_render_file_format(ve,rd.file_format)))

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		if rd.use_border:
			x0= wx * rd.border_min_x
			y0= wy * (1.0 - rd.border_max_y)
			x1= wx * rd.border_max_x
			y1= wy * (1.0 - rd.border_min_y)

			if rd.use_crop_to_border:
				params.append('-crop=')
			else:
				params.append('-region=')
			params.append("%i;%i;%i;%i"%(x0,y0,x1,y1))

		params.append('-sceneFile=')
		params.append(get_filenames(sce,'scene'))

		params.append('-display=')
		params.append('1')

		if ve.image_to_blender:
			params.append('-autoclose=')
			params.append('1')

		params.append('-frames=')
		if ve.animation:
			params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))
		else:
			params.append("%d" % sce.frame_current)

		if dr.on:
			if len(dr.nodes):
				params.append('-distributed=')
				params.append('1')
				params.append('-portNumber=')
				params.append(str(dr.port))
				params.append('-renderhost=')
				params.append("\"%s\"" % ';'.join([n.address for n in dr.nodes]))
				
		params.append('-imgFile=')
		params.append(image_file)

		if ve.debug:
			print("V-Ray/Blender: Command: %s" % ' '.join(params))

		if ve.autorun:
			process= subprocess.Popen(params)

			while True:
				if self.test_break():
					try:
						process.kill()
					except:
						pass
					break

				if process.poll() is not None:
					try:
						if not ve.animation and ve.image_to_blender:
							# if rd.use_border and not rd.use_crop_to_border:
							# 	wx= rd.resolution_x * rd.resolution_percentage / 100
							# 	wy= rd.resolution_y * rd.resolution_percentage / 100
							result= self.begin_result(0, 0, int(wx), int(wy))
							result.layers[0].load_from_file(load_file)
							self.end_result(result)
					except:
						pass
					break

				time.sleep(0.05)
		else:
			print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")


class VRayRendererPreview(bpy.types.RenderEngine):
	bl_idname  = 'VRAY_RENDER_PREVIEW'
	bl_label   = 'V-Ray (preview)'
	bl_use_preview = True
	
	def render(self, scene):
		global sce
		
		sce= scene
		rd=  scene.render
		wo=  scene.world

		# TEMP
		if rd.display_mode != 'AREA':
			rd.display_mode= 'AREA'

		vsce= sce.vray
		ve= vsce.exporter

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(get_filenames(sce,'output'),"render.%s" % get_render_file_format(ve,rd.file_format))
		load_file= os.path.join(get_filenames(sce,'output'),"render.%.4i.%s" % (sce.frame_current,get_render_file_format(ve,rd.file_format)))
		
		if sce.name == "preview":
			image_file= os.path.join(get_filenames(sce,'output'),"preview.exr")
			load_file= image_file

			filters= {
				'exported_bitmaps':   [],
				'exported_materials': [],
				'exported_proxy':     []
			}
			object_params= {
				'meshlight': {
					'on':       False,
					'material': None
				},
				'displace': {
					'texture':  None,
					'params':   None
				},
				'volume': None
			}
			
			ofile= open(os.path.join(vb_path,"preview","preview_materials.vrscene"), 'w')
			ofile.write("\nSettingsOutput {")
			ofile.write("\n\timg_separateAlpha= 0;")
			ofile.write("\n\timg_width= %s;"%(int(wx)))
			ofile.write("\n\timg_height= %s;"%(int(wy)))
			ofile.write("\n}\n")

			for ob in sce.objects:
				if ob.type in ('LAMP','ARMATURE','EMPTY'):
					continue
				if ob.type == 'CAMERA':
					if ob.name == "Camera":
						write_camera(sce,ofile,ob)
				for ms in ob.material_slots:
					if ob.name == "preview":
						write_material(ms.material, filters, object_params, ofile, name="PREVIEW")
					elif ms.material.name in ("checkerlight","checkerdark"):
						write_material(ms.material, filters, object_params, ofile)
						
			ofile.close()
			del object_params
			del filters
		
			params.append('-sceneFile=')
			params.append(os.path.join(vb_path,"preview","preview.vrscene"))
			params.append('-display=')
			params.append("0")
			params.append('-imgFile=')
			params.append(image_file)
		else:
			if ve.auto_meshes:
				write_geometry(sce, get_filenames(sce,'geometry'))
			write_scene(sce)

			if(rd.use_border):
				x0= wx * rd.border_min_x
				y0= wy * (1.0 - rd.border_max_y)
				x1= wx * rd.border_max_x
				y1= wy * (1.0 - rd.border_min_y)

				region= "%i;%i;%i;%i"%(x0,y0,x1,y1)

				if(rd.use_crop_to_border):
					params.append('-crop=')
				else:
					params.append('-region=')
				params.append(region)

			params.append('-sceneFile=')
			params.append(get_filenames(sce,'scene'))

			params.append('-display=')
			params.append("1")

			if ve.image_to_blender:
				params.append('-autoclose=')
				params.append('1')

			if ve.animation:
				params.append('-frames=')
				params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))
			else:
				params.append('-frames=')
				params.append("%d" % sce.frame_current)

			params.append('-imgFile=')
			params.append(image_file)

		if ve.debug:
			print("V-Ray/Blender: Command: %s"%(params))

		if ve.autorun:
			process= subprocess.Popen(params)

			while True:
				if self.test_break():
					try:
						process.kill()
					except:
						pass
					break

				if process.poll() is not None:
					try:
						if not ve.animation:
							if ve.image_to_blender or sce.name == "preview":
								# if rd.use_border and not rd.use_crop_to_border:
								# 	wx= rd.resolution_x * rd.resolution_percentage / 100
								# 	wy= rd.resolution_y * rd.resolution_percentage / 100
								result= self.begin_result(0, 0, int(wx), int(wy))
								layer= result.layers[0]
								layer.load_from_file(load_file)
								self.end_result(result)
					except:
						pass
					break

				time.sleep(0.05)
		else:
			print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")


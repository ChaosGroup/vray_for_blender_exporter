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

''' Blender modules '''
import bpy
import mathutils

''' vb modules '''
from vb25.utils import *
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
	'DEFUALT' : 0,
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

AA_FILTER_TYPE= {
	'AREA'     : '\nFilterArea {',
	'BOX'      : '\nFilterBox {',
	'TRIANGLE' : '\nFilterTriangle {',
	'LANC'     : '\nFilterLanczos {',
	'SINC'     : '\nFilterSinc {',
	'GAUSS'    : '\nFilterGaussian {',
	'CATMULL'  : '\nFilterCatmullRom {'
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
def write_geometry(sce):
	vsce= sce.vray_scene
	ve= vsce.exporter

	# For getting unique IDs for UV names
	uv_layers= []
	for ma in bpy.data.materials:
		for slot in ma.texture_slots:
			if(slot):
				if(slot.texture):
					if slot.texture.type in TEX_TYPES:
						if slot.texture_coordinates in ('UV'):
							if slot.uv_layer not in uv_layers:
								uv_layers.append(slot.uv_layer)

	try:
		print("V-Ray/Blender: Special build detected - using custom operator.")
		bpy.ops.scene.scene_export(
			vb_geometry_file= filenames['geometry'],
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

			if(ve.debug):
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

		ofile= open(filenames['geometry'], 'w')
		ofile.write("// V-Ray/Blender %s\n"%(VERSION))
		ofile.write("// Geometry file\n")

		timer= time.clock()

		STATIC_OBJECTS= []
		DYNAMIC_OBJECTS= []

		cur_frame= sce.frame_current
		sce.frame_current= sce.frame_start

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
					if m.type in ('ARMATURE', 'SOFT_BODY'): # Add more modifiers
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
				#sce.frame_current= f
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


def write_mesh_displace(ofile, obj):
	obj_name= stripName(obj.data.name)
	out_name= "GeomDisp_%s"%(obj_name)
	s("vray_geometry_name", out_name, obj)

	amount= g("vray_displace_amount",obj) * g("vray_displace_amount_delim",obj)
	if(g("vray_displace_use_dispfac",obj)):
		amount= g("vray_displace_dispfac",obj) * g("vray_displace_amount_delim",obj)
	
	ofile.write("\nGeomDisplacedMesh %s {"%(out_name))
	ofile.write("\n\tmesh= %s;"%("Geom_%s"%(obj_name)))
	ofile.write("\n\tdisplacement_tex_color= %s;"%(g("vray_displace_tex",obj)))
	ofile.write("\n\tdisplacement_amount= %.5f;"%(amount))
	ofile.write("\n\tdisplacement_shift= %.6f;"%(g("vray_displace_shift",obj)))
	ofile.write("\n\tuse_globals= %d;"%(g("vray_displace_use_globals",obj)))
	ofile.write("\n\tview_dep= %d;"%(g("vray_displace_view_dep",obj)))
	ofile.write("\n\tedge_length= %.6f;"%(g("vray_displace_edgeLength",obj)))
	ofile.write("\n\tmax_subdivs= %d;"%(g("vray_displace_maxSubdivs",obj)))
	ofile.write("\n\tkeep_continuity= %d;"%(g("vray_displace_keep_continuity",obj)))
	ofile.write("\n\twater_level= %.6f;"%(g("vray_displace_water_level",obj)))
	ofile.write("\n}\n")


def write_mesh_file(ofile, exported_proxy, ob):
	ANIM_TYPE= {
		'LOOP'     : 0,
		'ONCE'     : 1,
		'PINGPONG' : 2,
		'STILL'    : 3
	}

	proxy= od.data.vray.GeomMeshFile
	
	proxy_name= "Proxy_%s" % clean_string(os.path.basename(proxy.file))

	if proxy_name not in exported_proxy:
		exported_proxy.append(proxy_name)
		
		ofile.write("\nGeomMeshFile %s {"%(proxy_name))
		ofile.write("\n\tfile= \"%s\";"%(get_full_filepath(proxy.file)))
		ofile.write("\n\tanim_speed= %i;"%(proxy.anim_speed))
		ofile.write("\n\tanim_type= %i;"%(ANIM_TYPE[proxy.anim_type]))
		ofile.write("\n\tanim_offset= %i;"%(proxy.anim_offset))
		ofile.write("\n}\n")

	return proxy_name



'''
  MATERIALS
'''
def write_multi_material(ofile, ob):
	mtl_name= "Material_%s"%(get_name(ob,"Data"))

	ids_list = ""
	mtls_list= ""
	i= 0
	
	for slot in ob.material_slots:
		ma_name= "Material_no_material"
		if slot.material is not None:
			ma_name= get_name(slot.material, 'Material')
			
		mtls_list+= "%s,"%(ma_name)
		ids_list += "%i,"%(i)
		i+= 1

	ofile.write("\nMtlMulti %s {"%(mtl_name))
	ofile.write("\n\tmtls_list= List(%s);"%(mtls_list[0:-1]))
	ofile.write("\n\tids_list= ListInt(%s);"%(ids_list[0:-1]))
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
	if(tex.interpolation):
		if(tex.filter == 'BOX'):
			filter_type= 1
		else:
			filter_type= 2
	ofile.write("\n\tfilter_type= %d;"%(filter_type))
	ofile.write("\n\tfilter_blur= %.3f;"%(tex.filter_size))

	ofile.write("\n}\n")

	return bitmap_name


def write_TexBitmap(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, ob= None, env= None, env_type= None):
	tex_name= "Texture_no_texture"

	if(slot):
		tex= slot.texture

	if(tex.image):
		tex_name= get_name(tex,"Texture")
		if(ma):
			tex_name= "%s_%s"%(tex_name, get_name(ma,"Material"))

		if(env):
			uv_name= write_UVWGenEnvironment(ofile, tex, tex_name, slot.texture_coordinates)
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
				ofile.write("\n\tinvert= %d;"%(slot.negate))
			ofile.write("\n}\n")
		else:
			return "Texture_no_texture"

	else:
		debug(sce,"Error! Image file is not set! (%s)"%(tex.name))

	return tex_name


def write_TexAColorOp(tex, mult, tex_name= None):
	brdf_name= "TexAColorOp_%s"%(tex)
	if(tex_name):
		brdf_name= "TexAColorOp_%s"%(tex_name)

	ofile.write("\nTexAColorOp %s {"%(brdf_name))
	ofile.write("\n\tcolor_a= %s;"%(a(sce,tex)))
	ofile.write("\n\tmult_a= %s;"%(a(sce,mult)))
	ofile.write("\n}\n")

	return brdf_name


def write_TexInvert(name):
	tex_name= "TexInvert_%s"%(name)

	ofile.write("\nTexInvert %s {"%(tex_name))
	ofile.write("\n\ttexture= %s;"%(tex))
	ofile.write("\n}\n")

	return tex_name


def write_TexCompMax(name, sourceA, sourceB):
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
	elif tex.type == 'PLUGIN':
		tex_name= write_TexPlugin(ofile, ma= ma, slot= slot, tex= tex, env= env)
	else:
		pass

	return tex_name


def write_textures(ofile, exported_bitmaps, ma, ma_name):
	out    = ""
	out_tex= ""

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
	vraymat['bump']= None
	vraymat['bump_amount']= 0.0
	vraymat['normal']= None
	vraymat['normal_amount']= 0.0
	vraymat['reflect']= None
	vraymat['reflect_mult']= 0.0
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

	for slot,slot_idx in zip(ma.texture_slots,range(len(ma.texture_slots))):
		if(ma.use_textures[slot_idx] and slot):
			if(slot.texture):
				if slot.texture.type in TEX_TYPES:
					if(slot.map_colordiff):
						vraytex['color'].append(slot)
						vraymat['color_mult']+= slot.colordiff_factor
					if(slot.map_emit):
						vraytex['emit'].append(slot)
						vraymat['emit_mult']+= slot.emit_factor
					if(slot.map_alpha):
						vraytex['alpha'].append(slot)
						vraymat['alpha_mult']+= slot.alpha_factor
					if(slot.map_hardness):
						vraytex['roughness'].append(slot)
						vraymat['roughness_mult']+= slot.hardness_factor
					if(slot.map_specular):
						vraytex['reflect_glossiness'].append(slot)
						vraymat['reflect_glossiness_mult']+= slot.specular_factor
					if(slot.map_colorspec): # map_vray_hilight
						vraytex['hilight_glossiness'].append(slot)
						vraymat['hilight_glossiness_mult']+= slot.colorspec_factor
					if(slot.map_raymir):
						vraytex['reflect'].append(slot)
						vraymat['reflect_mult']+= slot.raymir_factor
					if(slot.map_translucency):
						vraytex['refract'].append(slot)
						vraymat['refract_mult']+= slot.translucency_factor
					if(slot.map_normal):
						if(slot.texture.normal_map):
							vraytex['normal'].append(slot)
							vraymat['normal_amount']+= slot.normal_factor
						else:
							vraytex['bump'].append(slot)
							vraymat['bump_amount']+= slot.normal_factor
					if(slot.map_displacement):
						vraytex['displace'].append(slot)
						vraymat['displace_amount']+= slot.displacement_factor

	for textype in vraytex:
		if(len(vraytex[textype])):
			if(len(vraytex[textype]) == 1):
				slot= vraytex[textype][0]
				tex= slot.texture

				debug(sce,"  Slot: %s"%(textype))
				debug(sce,"    Texture: %s"%(tex.name))

				vraymat[textype]= write_texture(ofile, exported_bitmaps, ma, slot)

				if(textype == 'color'):
					if(slot.stencil):
						tex_name= "TexBlend_%s_%s"%(ma_name,vraymat[textype])
						ofile.write("\nTexBlend %s {"%(tex_name))
						ofile.write("\n\tcolor_a= %s;"%(a(sce,"AColor(%.3f,%.3f,%.3f,1.0)"%(tuple(ma.diffuse_color)))))
						ofile.write("\n\tcolor_b= %s;"%(vraymat[textype]))
						ofile.write("\n\tblend_amount= %s::out_alpha;"%(vraymat[textype]))
						ofile.write("\n\tcomposite= %d;"%(0))
						ofile.write("\n}\n")
						vraymat[textype]= tex_name
					if(slot.colordiff_factor < 1.0):
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

				out_texlayered      = ""
				out_texlayered_modes= ""

				for slot in vraytex[textype]:
					tex= slot.texture

					tex_name= write_texture(ofile, exported_bitmaps, ma, slot)

					texlayered_names.append(tex_name) # For stencil
					texlayered_modes.append(slot.blend_type)
					out_texlayered += "%s,"%(tex_name)

					debug(sce,"  Slot: %s"%(textype))
					debug(sce,"    Texture: %s [mode: %s]"%(tex.name, slot.blend_type))

					if(slot.stencil):
						stencil= vraytex[textype].index(slot)

				for i in range(1, len(texlayered_modes)):
					out_texlayered_modes+= "%s,"%(BLEND_TYPE[texlayered_modes[i]])

				if(stencil):
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
					ofile.write("\n\ttextures= List(%s);"%(out_texlayered[0:-1]))
					ofile.write("\n\tblend_modes= List(0, %s);"%(out_texlayered_modes[0:-1]))
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

	rm= ma.raytrace_mirror
	rt= ma.raytrace_transparency
	vma= ma.vray
	plug= vma.BRDFVRayMtl

	brdf_name= "BRDFVRayMtl_%s"%(ma_name)

	ofile.write("\nBRDFVRayMtl %s {"%(brdf_name))
	ofile.write("\n\tbrdf_type= %s;"%(a(sce,BRDF_TYPE[plug.brdf_type]))) # integer = 1, The BRDF type (0 - Phong, 1 - Blinn, 2 - Ward)

	if(tex_vray['alpha']): # float texture = 1, The opacity of the material
		ofile.write("\n\topacity= %s::out_intensity;"%(tex_vray['alpha']))
	else:
		ofile.write("\n\topacity= %s;"%(a(sce,"%.6f"%(ma.alpha))))

	if(tex_vray['color']): # acolor texture = AColor(0.5, 0.5, 0.5, 1), The diffuse color of the material
		ofile.write("\n\tdiffuse= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tdiffuse= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.diffuse_color)))))

	if(tex_vray['reflect']): # acolor texture = AColor(0, 0, 0, 1), The reflection color of the material
		ofile.write("\n\treflect= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\treflect= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(plug.reflect_color)))))

	if(tex_vray['reflect_glossiness']): # float texture = 1, The glossiness of the reflections
		ofile.write("\n\treflect_glossiness= %s::out_intensity;"%(tex_vray['reflect_glossiness']))
	else:
		ofile.write("\n\treflect_glossiness= %s;"%(a(sce,rm.gloss_factor)))

	if(tex_vray['hilight_glossiness']): # float texture = 1, The glossiness of the hilights
		ofile.write("\n\thilight_glossiness= %s::out_intensity;"%(tex_vray['hilight_glossiness']))
	else:
		ofile.write("\n\thilight_glossiness= %s;"%(a(sce,plug.hilight_glossiness)))

	if(tex_vray['refract']): # acolor texture = AColor(0, 0, 0, 1), The refraction color of the material
		ofile.write("\n\trefract= %s;"%(tex_vray['refract']))
	else:
		ofile.write("\n\trefract= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(plug.refract_color)))))

	for param in OBJECT_PARAMS['BRDFVRayMtl']:
		if param not in ('refract','opacity','diffuse','reflect','reflect_glossiness','hilight_glossiness','refract'):
			if param == 'refract_ior':
				value= rt.ior
			elif param == 'refract_glossiness':
				value= rt.gloss_factor
			elif param == 'translucency':
				value= TRANSLUCENSY[plug.translucency]
			elif param == 'option_glossy_rays_as_gi':
				value= GLOSSY_RAYS[plug.option_glossy_rays_as_gi]
			elif param == 'option_energy_mode':
				value= ENERGY_MODE[plug.option_energy_mode]
			else:
				value= getattr(plug,param)
			ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	# ofile.write("\n\troughness= %s;"%(a(sce,ma.vray_roughness))) # float texture = 0, The roughness of the diffuse part of the material
	# ofile.write("\n\treflect_subdivs= %s;"%(p(rm.gloss_samples))) # integer = 8, Subdivs for glossy reflectons
	# ofile.write("\n\treflect_trace= %s;"%(p(ma.vray_trace_reflections))) # bool = true, true to trace reflections and false to only do hilights
	# ofile.write("\n\treflect_depth= %s;"%(p(rm.depth))) # integer = 5, The maximum depth for reflections
	# ofile.write("\n\treflect_exit_color= %s;"%(a(sce,"Color(0, 0, 0)"))) # color = Color(0, 0, 0), The color to use when the maximum depth is reached
	# ofile.write("\n\treflect_dim_distance= %s;"%(a(sce,0.1))) # float = 1e+18, How much to dim reflection as length of rays increases
	# ofile.write("\n\treflect_dim_distance_on= %s;"%(a(sce,0))) # bool = false, True to enable dim distance
	# ofile.write("\n\treflect_dim_distance_falloff= %s;"%(a(sce,0))) # float = 0, Fall off for the dim distance
	# ofile.write("\n\thilight_glossiness_lock= %s;"%(1)) # bool = true, true to use the reflection glossiness also for hilights (hilight_glossiness is ignored)
	# ofile.write("\n\thilight_soften= %s;"%(a(sce,0))) # float = 0, How much to soften hilights and reflections at grazing light angles
	# ofile.write("\n\tfresnel= %s;"%(a(sce,ma.vray_fresnel))) # bool = false, true to enable fresnel reflections
	# ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior))) # float texture = 1.6, The ior for calculating the Fresnel term
	# ofile.write("\n\tfresnel_ior_lock= %s;"%(a(sce,ma.vray_fresnel_ior_lock))) # bool = true, true to use the refraction ior also for the Fresnel term (fresnel_ior is ignored)
	# ofile.write("\n\tanisotropy= %s;"%(a(sce,ma.vray_anisotropy))) # bool = true, true to use the refraction ior also for the Fresnel term (fresnel_ior is ignored)
	# ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,ma.vray_anisotropy_rotation))) # float texture = 0, The rotation of the anisotropy axes, from 0.0 to 1.0
	# ofile.write("\n\tanisotropy_derivation= %s;"%(a(sce,0))) # integer = 0, What method to use for deriving anisotropy axes (0 - local object axis; 1 - a specified uvw generator)
	# ofile.write("\n\tanisotropy_axis= %s;"%(a(sce,2))) # integer = 2, Which local object axis to use when anisotropy_derivation is 0
	# # ofile.write("\n\tanisotropy_uvwgen= %s;"%(a(sce,))) # plugin, The uvw generator to use for anisotropy when anisotropy_derivation is 1
	# ofile.write("\n\trefract_ior= %s;"%(a(sce,rt.ior))) # float texture = 1.6, The IOR for refractions
	# ofile.write("\n\trefract_glossiness= %s;"%(a(sce,rt.gloss_factor))) # float texture = 1, Glossiness for refractions
	# ofile.write("\n\trefract_subdivs= %s;"%(a(sce,rt.gloss_samples))) # integer = 8, Subdivs for glossy refractions
	# ofile.write("\n\trefract_trace= %s;"%(p(ma.vray_trace_refractions))) # bool = true, 1 to trace refractions; 0 to disable them
	# ofile.write("\n\trefract_depth= %s;"%(a(sce,rt.depth))) # integer = 5, The maximum depth for refractions
	# ofile.write("\n\trefract_exit_color= %s;"%(a(sce,"Color(0, 0, 0)"))) # color = Color(0, 0, 0), The color to use when maximum depth is reached when refract_exit_color_on is true
	# ofile.write("\n\trefract_exit_color_on= %s;"%(a(sce,0))) # bool = false, If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray
	# ofile.write("\n\trefract_affect_alpha= %s;"%(p(ma.vray_affect_alpha))) # integer = 0 (0 - opaque alpha; 1 - alpha is taken from refractions; 2 - all channels are propagated
	# ofile.write("\n\trefract_affect_shadows= %s;"%(p(ma.vray_affect_shadows))) # bool = false, true to enable the refraction to affect the shadows cast by the material (as transparent shadows)
	# ofile.write("\n\tfog_color= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.vray_fog_color))))) # color = Color(1, 1, 1), The absorption (fog) color
	# ofile.write("\n\tfog_mult= %s;"%(a(sce,ma.vray_fog_color_mult * 10))) # float = 1, Multiplier for the absorption
	# ofile.write("\n\tfog_bias= %s;"%(a(sce,ma.vray_fog_bias))) # float = 0, Bias for the absorption
	# ofile.write("\n\ttranslucency= %s;"%(a(sce,0))) # integer = 0, Translucency mode (0 - none)
	# ofile.write("\n\ttranslucency_color= %s;"%(a(sce,"AColor(1, 1, 1, 1)"))) # acolor texture = AColor(1, 1, 1, 1), Filter color for the translucency effect
	# ofile.write("\n\ttranslucency_light_mult= %s;"%(a(sce,1.0))) # float = 1, A multiplier for the calculated lighting for the translucency effect
	# ofile.write("\n\ttranslucency_scatter_dir= %s;"%(a(sce,0.5))) # float = 0.5, Scatter direction (0.0f is backward, 1.0f is forward)
	# ofile.write("\n\ttranslucency_scatter_coeff= %s;"%(a(sce,0.0))) # float = 0, Scattering cone (0.0f - no scattering, 1.0f - full scattering
	# ofile.write("\n\ttranslucency_thickness= %s;"%(a(sce,0.1))) # float = 0, Scattering cone (0.0f - no scattering, 1.0f - full scattering
	# ofile.write("\n\toption_double_sided= %s;"%(a(sce,ma.vray_double_sided))) # bool = true, true if the material is double-sided
	# ofile.write("\n\toption_reflect_on_back= %s;"%(a(sce,ma.vray_back_side))) # bool = false, true to compute reflections for back sides of objects
	# ofile.write("\n\toption_glossy_rays_as_gi= %s;"%(a(sce,1))) # integer = 1, Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always
	# ofile.write("\n\toption_cutoff= %s;"%(a(sce,0.001))) # float = 0.001, Specifies a cutoff threshold for tracing reflections/refractions
	# ofile.write("\n\toption_use_irradiance_map= %s;"%(a(sce,1))) # float = 0.001, Specifies a cutoff threshold for tracing reflections/refractions
	# ofile.write("\n\toption_energy_mode= %s;"%(a(sce,0))) # integer = 0, Energy preservation mode for reflections and refractions (0 - color, 1 - monochrome)
	# # ofile.write("\n\tenvironment_override= %s;"%(a(sce,))) # acolor texture, Environment override texture
	# ofile.write("\n\tenvironment_priority= %s;"%(a(sce,0))) # integer = 0, Environment override priority (used when several materials override it along a ray path)

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

	vma= ma.vray
	plug= vma.BRDFSSS2Complex

	brdf_name= "BRDFSSS2Complex_%s"%(ma_name)

	ofile.write("\nBRDFSSS2Complex %s {"%(brdf_name))
	for param in OBJECT_PARAMS['BRDFSSS2Complex']:
		if param == 'single_scatter':
			value= SINGLE_SCATTER[plug.single_scatter]
		else:
			value= getattr(plug,param)
		ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFLight(ofile, ma, ma_name, tex_vray):
	brdf_name= "BRDFLight_%s"%(ma_name)

	if(tex_vray['color']):
		color= tex_vray['color']
	else:
		color= "Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color))

	if(tex_vray['alpha']):
		alpha= exportTexInvert(tex_vray['alpha'])
		color= exportTexCompMax("%s_alpha"%(brdf_name), alpha, color)

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


def	write_material(ofile, exported_bitmaps, ma, name= None):
	ma_name= get_name(ma,"Material")
	if name:
		ma_name= name

	vma= ma.vray
	
	ofile.write("\n//\n// Material: %s\n//"%(ma.name))

	brdf_name= "BRDFDiffuse_no_material"

	tex_vray= write_textures(ofile, exported_bitmaps, ma, ma_name)

	if vma.type == 'MTL':
		brdf_name= write_BRDFVRayMtl(ofile, ma, ma_name, tex_vray)
	elif vma.type == 'SSS':
		brdf_name= write_BRDFSSS2Complex(ofile, ma, ma_name, tex_vray)
	elif vma.type == 'EMIT':
		if vma.emitter_type == 'MESH':
			return
		else:
			brdf_name= write_BRDFLight(ofile, ma, ma_name, tex_vray)
	else:
		return

	if vma.type != 'EMIT':
		if tex_vray['bump'] or tex_vray['normal']:
			brdf_name= write_BRDFBump(ofile, brdf_name, tex_vray)

	# Very ugly :(
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
		ofile.write("\n\ttranslucency= Color(%.3f, %.3f, %.3f);"%(vma.two_sided_translucency,vma.two_sided_translucency,vma.two_sided_translucency))
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


def write_materials(sce):
	vsce= sce.vray_scene
	ve= vsce.exporter
	
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
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

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
					fac= "Color(1.0,1.0,1.0)*%.3f"%(
						1.0 - ns.default_value[0])
					node_fac= find_connected_node(nt, ns)

			if(node_color1):
				if(node_color1.type in ('MATERIAL','MATERIAL_EXT')):
					color1= get_name(node_color1.material,'BRDFVRayMtl_Material')

			if(node_color2):
				if(node_color2.type in ('MATERIAL','MATERIAL_EXT')):
					color2= get_name(node_color2.material,'BRDFVRayMtl_Material')
				
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
			ofile.write("\n\tadditive_mode= 1;") # Shellac
			ofile.write("\n}\n")
				
		elif(no.type == 'TEXTURE'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		elif(no.type == 'INVERT'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(no.name,no.type))

	def export_material(ofile, exported_bitmaps, ma):
		if ve.use_material_nodes and ma.use_nodes and hasattr(ma.node_tree, 'links'):
			debug(sce,"Writing node material: %s"%(ma.name))

			nt= ma.node_tree

			for n in nt.nodes:
				if(n.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT')):
					write_node(ofile, ma, nt, n)
				else:
					debug(sce,"Node: %s (unsupported node type: %s)"%(n.name, n.type))

		else:
			write_material(ofile, exported_bitmaps, ma)
		

	print("V-Ray/Blender: Writing materials...")

	ofile= open(filenames['materials'], 'w')
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Materials file\n\n")

	ofile.write("\n//\n// Material for object without assigned material\n//")
	ofile.write("\nUVWGenChannel UVWGenChannel_default {")
	ofile.write("\n\tuvw_channel= 1;")
	ofile.write("\n\tuvw_transform= Transform(")
	ofile.write("\n\t\tMatrix(")
	ofile.write("\n\t\t\tVector(1.0,0.0,0.0)*10,")
	ofile.write("\n\t\t\tVector(0.0,1.0,0.0)*10,")
	ofile.write("\n\t\t\tVector(0.0,0.0,1.0)")
	ofile.write("\n\t\t),")
	ofile.write("\n\t\tVector(0.0,0.0,0.0)")
	ofile.write("\n\t);")
	ofile.write("\n}\n")
	ofile.write("\nTexChecker Texture_no_texture {")
	ofile.write("\n\tuvwgen= UVWGenChannel_default;")
	ofile.write("\n}\n")
	ofile.write("\nBRDFDiffuse BRDFDiffuse_no_material {")
	ofile.write("\n\tcolor=Color(0.5, 0.5, 0.5);")
	ofile.write("\n}\n")
	ofile.write("\nMtlSingleBRDF Material_no_material {")
	ofile.write("\n\tbrdf= BRDFDiffuse_no_material;")
	ofile.write("\n}\n")
	ofile.write("\nTexAColor TexAColor_default_blend {")
	ofile.write("\n\tuvwgen= UVWGenChannel_default;")
	ofile.write("\n\ttexture= Color(1.0,1.0,1.0);")
	ofile.write("\n}\n")
	ofile.write("\n//\n// Materials\n//")

	exported_bitmaps= []
	exported_nodes= []

	for ma in bpy.data.materials:
		if ma.users or ma.fake_user:
			export_material(ofile, exported_bitmaps, ma)

	exported_bitmaps= []
	exported_nodes= []

	ofile.close()
	print("V-Ray/Blender: Writing materials... done.")


def detect_meshlight(ob):
	if len(ob.material_slots) > 0:
		for slot in ob.material_slots:
			vma= slot.material.vray
			if vma.type == 'EMIT' and vma.emitter_type == 'MESH':
				return (True, slot.material)
	return (False, None)

def write_LightMesh(ofile, ob, ma, name, geometry):
	# TMP!
	exported_bitmaps= []
	tex_vray= write_textures(ofile, exported_bitmaps, ma, name)
	exported_bitmaps= []

	plugin= 'LightMesh'

	light= getattr(ma.vray,'LightMesh')

	ofile.write("\n%s %s {" % (plugin,name))
	for param in OBJECT_PARAMS[plugin]:
		if param == 'color':
			if tex_vray['color']:
				ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
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


'''
  NODES
'''
def write_nodes(sce):
	vsce= sce.vray_scene
	ve= vsce.exporter

	print("V-Ray/Blender: Writing nodes...")

	# Used when exporting dupli, particles etc.
	global exported_nodes
	global exported_proxy
	exported_nodes= []
	exported_proxy= []

	def write_node(ob, matrix= None, visible= True):
		if ob.name not in exported_nodes:
			exported_nodes.append(ob.name)

			vo= ob.vray
			vd= ob.data.vray

			if ve.debug:
				print("V-Ray/Blender: Processing object: %s"%(ob.name))
				print("V-Ray/Blender:   Animated: %d"%(1 if ob.animation_data else 0))
				if ob.data:
					print("V-Ray/Blender:   Mesh animated: %d"%(1 if ob.data.animation_data else 0))
			else:
				if PLATFORM == "win32":
					sys.stdout.write("V-Ray/Blender: [%d] Object: %s                              \r"%(sce.frame_current, ob.name))
				else:
					sys.stdout.write("V-Ray/Blender: [%d] Object: \033[0;32m%s\033[0m                              \r"%(sce.frame_current, ob.name))
				sys.stdout.flush()

			node_name= get_name(ob,"Node")

			node_geometry= get_name(ob.data,"Geom")

			if hasattr(vd,'GeomMeshFile'):
				if vd.GeomMeshFile.use:
					node_geometry= write_mesh_file(ofile, exported_proxy, ob)

			if matrix:
				node_matrix= matrix
			else:
				node_matrix= ob.matrix_world

			ma_name= "Material_no_material"
			if(len(ob.material_slots) > 0):
				if(len(ob.material_slots) == 1):
					if ob.material_slots[0].material is not None:
					 	ma_name= get_name(ob.material_slots[0].material, "Material")
				else:
					ma_name= write_multi_material(ofile, ob)

			(meshlight,meshlight_material)= detect_meshlight(ob)
			if meshlight:
				write_LightMesh(ofile, ob, meshlight_material, node_name, node_geometry)
			else:
				ofile.write("\nNode %s {"%(node_name))
				ofile.write("\n\tobjectID= %d;"%(ob.pass_index))
				ofile.write("\n\tgeometry= %s;"%(node_geometry))
				ofile.write("\n\tmaterial= %s;"%(ma_name))
				ofile.write("\n\tvisible= %s;"%(a(sce,visible)))
				ofile.write("\n\ttransform= %s;"%(a(sce,transform(node_matrix))))
				ofile.write("\n}\n")

	ofile= open(filenames['nodes'], 'w')
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Node file\n")

	timer= time.clock()

	OBJECTS= []

	ca= sce.camera
	vca= ca.data.VRayCamera

	render_stats= {
		
	}

	if vca.hide_from_view:
		if vca.hide_from_everything:
			if vca.everything_auto:
				auto_group= 'hidefrom_%s' % ca.name
				try:
					for group_ob in bpy.data.groups[auto_group].objects:
						HIDE_FROM_VIEW.append(group_ob.name)
				except:
					debug(sce,"Group \"%s\" doesn\'t exist" % auto_group)
			else:
				HIDE_FROM_VIEW= vca.everything_objects.split(';')
				for gr in vca.everything_groups.split(';'):
					try:
						for group_ob in bpy.data.groups[gr].objects:
							HIDE_FROM_VIEW.append(group_ob.name)
					except:
						debug(sce,"Group \"%s\" doesn\'t exist" % gr)
				debug(sce,"Hide from view \"%s\": %s" % (ca.name,HIDE_FROM_VIEW))
		else:
			pass

	for ob in sce.objects:
		if ob.type in ('LAMP','CAMERA','ARMATURE','EMPTY'):
			continue

		if ve.active_layers:
			if not object_on_visible_layers(sce,ob):
				continue

		OBJECTS.append(ob)

	if ve.animation:
		selected_frame= sce.frame_current
		f= sce.frame_start
		while(f <= sce.frame_end):
			exported_nodes= []
			sce.set_frame(f)
			for ob in OBJECTS:
				visible= True
				if vca.hide_from_view:
					if vca.hide_from_everything:
						if ob.name in HIDE_FROM_VIEW:
							visible= False

				write_node(ob, visible= visible)
			f+= sce.frame_step
		sce.set_frame(selected_frame)
	else:
		for ob in OBJECTS:
			visible= True
			if vca.hide_from_view:
				if vca.hide_from_everything:
					if ob.name in HIDE_FROM_VIEW:
						visible= False

			write_node(ob, visible= visible)

	exported_nodes= []
	exported_proxy= []

	OBJECTS= []
	# HIDE_FROM_VIEW= []

	ofile.close()
	print("V-Ray/Blender: Writing nodes... done [%s]                    "%(time.clock() - timer))


def write_lamps(sce):
	vsce= sce.vray_scene
	ve= vsce.exporter

	print("V-Ray/Blender: Writing lights...")

	ofile= open(filenames['lights'], 'w')
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Lights file\n")

	for ob in sce.objects:
		if ob.type == 'LAMP':
			if ve.active_layers:
				if not object_on_visible_layers(sce,ob):
					continue
		
			lamp= ob.data
			la_name= clean_string(ob.name)

			lamp_type= 'LightOmni'

			if(lamp.type == 'POINT'):
				if(lamp.vr_la_radius > 0):
					lamp_type= 'LightSphere'
				else:
					lamp_type= 'LightOmni'
			elif(lamp.type == 'SPOT'):
				if(lamp.vr_la_spot_type == 'SPOT'):
					lamp_type= 'LightSpot'
				else:
					lamp_type= 'LightIES'
			elif(lamp.type == 'SUN'):
				if(lamp.vr_la_direct_type == 'DIRECT'):
					lamp_type= 'LightDirect'
				else:
					lamp_type= 'SunLight'
			elif(lamp.type == 'AREA'):
				lamp_type= 'LightRectangle'
			elif(lamp.type == 'HEMI'):
				lamp_type= 'LightDome'
			else:
				continue

			ofile.write("\n%s %s_%s {"%(lamp_type,lamp_type,la_name))

			if(lamp_type == 'LightOmni'):
				pass
			elif(lamp_type == 'LightSphere'):
				pass
			elif(lamp_type == 'LightSpot'):
				pass
			elif(lamp_type == 'LightIES'):
				pass
			elif(lamp_type == 'LightDirect'):
				pass
			elif(lamp_type == 'SunLight'):
				pass
			elif(lamp_type == 'LightRectangle'):
				if(lamp.shape == 'RECTANGLE'):
					ofile.write("\n\tu_size= %s;"%(a(sce,lamp.size/2)))
					ofile.write("\n\tv_size= %s;"%(a(sce,lamp.size_y/2)))
				else:
					ofile.write("\n\tu_size= %s;"%(a(sce,lamp.size/2)))
					ofile.write("\n\tv_size= %s;"%(a(sce,lamp.size/2)))
				ofile.write("\n\tlightPortal= %i;"%(LIGHT_PORTAL[lamp.vr_la_lightPortal]))
			elif(lamp_type == 'LightDome'):
				pass

			for param in OBJECT_PARAMS[lamp_type]:
				if lamp_type == 'LightIES':
					if param == 'intensity':
						ofile.write("\n\tpower= %s;"%(a(sce,lamp.vr_la_intensity)))
						continue
					elif param == 'ies_file':
						ofile.write("\n\t%s= \"%s\";"%(param,get_full_filepath(lamp.vr_la_ies_file)))
						continue
				if param == 'shadow_subdivs':
					ofile.write("\n\tshadow_subdivs= %s;"%(a(sce,lamp.vr_la_subdivs)))
				elif param == 'shadow_color':
					ofile.write("\n\tshadow_color= %s;"%(a(sce,lamp.vr_la_shadowColor)))
				else:
					ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(lamp, "vr_la_%s"%(param)))))

			if lamp_type == 'SunLight':
				ofile.write("\n\tsky_model= %i;"%(SKY_MODEL[lamp.vr_la_sky_model]))
			else:
				ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(lamp.color)))))
				if lamp_type != 'LightIES':
					ofile.write("\n\tunits= %i;"%(UNITS[lamp.vr_la_units]))
			
			ofile.write("\n\ttransform= %s;"%(a(sce,transform(ob.matrix_world))))
			ofile.write("\n}\n")

	ofile.close()
	print("V-Ray/Blender: Writing lights... done.")


def write_camera(sce,camera= None, ofile= None):
	vsce= sce.vray_scene
	ve= vsce.exporter

	ca= sce.camera
	if camera is not None:
		ca= camera

	if ca is not None:
		print("V-Ray/Blender: Writing camera...")

		if ofile is None:
			ofile= open(filenames['camera'], 'w')
			ofile.write("// V-Ray/Blender %s\n"%(VERSION))
			ofile.write("// Camera/view file\n")

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100
		aspect= float(wx) / float(wy)
		
		ofile.write("\nSettingsOutput {")
		ofile.write("\n\timg_width= %s;"%(int(wx)))
		ofile.write("\n\timg_height= %s;"%(int(wy)))
		if ve.animation:
			ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(ca.name),get_render_file_format(ve,rd.file_format)))
			ofile.write("\n\timg_dir= \"%s\";"%(filenames['output']))
			ofile.write("\n\timg_file_needFrameNumber= 1;")
			ofile.write("\n\tanim_start= %d;"%(sce.frame_start))
			ofile.write("\n\tanim_end= %d;"%(sce.frame_end))
			ofile.write("\n\tframe_start= %d;"%(sce.frame_start))
			ofile.write("\n\tframes_per_second= %d;"%(1.0) )
			ofile.write("\n\tframes= %d-%d;"%(sce.frame_start, sce.frame_end))
		ofile.write("\n\tframe_stamp_enabled= %d;"%(0))
		ofile.write("\n\tframe_stamp_text= \"%s\";"%("V-Ray/Blender 2.5 (git) | V-Ray Standalone %%vraycore | %%rendertime"))
		ofile.write("\n}\n")

		def write_ca(sce,ca):
			fov= ca.data.angle
			if(aspect < 1.0):
				fov= fov*aspect

			bg_tex= None
			gi_tex= None
			reflect_tex= None
			refract_tex= None

			bg_tex_mult= 1.0
			gi_tex_mult= 1.0
			reflect_tex_mult= 1.0
			refract_tex_mult= 1.0

			for slot in wo.texture_slots:
				if(slot):
					if(slot.texture):
						if slot.texture.type in TEX_TYPES:
							if slot.map_blend:
								bg_tex= write_texture(ofile, slot= slot, env=True)
								bg_tex_mult= slot.blend_factor
							if slot.map_horizon:
								gi_tex= write_texture(ofile, slot= slot, env=True)
								gi_tex_mult= slot.horizon_factor
							if slot.map_zenith_up:
								reflect_tex= write_texture(ofile, slot= slot, env=True)
								reflect_tex_mult= slot.zenith_up_factor
							if slot.map_zenith_down:
								refract_tex= write_texture(ofile, slot= slot, env=True)
								refract_tex_mult= slot.zenith_down_factor

			ofile.write("\nSettingsEnvironment {")
			ofile.write("\n\tbg_color= %s;"%(a(sce,wo.vray_env_bg_color)))
			if(bg_tex):
				ofile.write("\n\tbg_tex= %s;"%(bg_tex))
				ofile.write("\n\tbg_tex_mult= %s;"%(a(sce,bg_tex_mult)))
			if(wo.vray_env_gi_override):
				ofile.write("\n\tgi_color= %s;"%(a(sce,wo.vray_env_gi_color)))
			if(gi_tex):
				ofile.write("\n\tgi_tex= %s;"%(gi_tex))
				ofile.write("\n\tgi_tex_mult= %s;"%(a(sce,gi_tex_mult)))
			if(wo.vray_env_reflection_override):
				ofile.write("\n\treflect_color= %s;"%(a(sce,wo.vray_env_reflection_color)))
			if(reflect_tex):
				ofile.write("\n\treflect_tex= %s;"%(reflect_tex))
				ofile.write("\n\treflect_tex_mult= %s;"%(a(sce,reflect_tex_mult)))
			if(wo.vray_env_refraction_override):
				ofile.write("\n\trefract_color= %s;"%(a(sce,wo.vray_env_refraction_color)))
			if(refract_tex):
				ofile.write("\n\trefract_tex= %s;"%(refract_tex))
				ofile.write("\n\trefract_tex_mult= %s;"%(a(sce,refract_tex_mult)))
			ofile.write("\n}\n")

			ofile.write("\nRenderView RenderView {")
			ofile.write("\n\ttransform= %s;"%(a(sce,transform(ca.matrix_world))))
			ofile.write("\n\tfov= %s;"%(a(sce,fov)))
			ofile.write("\n\tclipping= 1;")
			ofile.write("\n\tclipping_near= %s;"%(a(sce,ca.data.clip_start)))
			ofile.write("\n\tclipping_far= %s;"%(a(sce,ca.data.clip_end)))
			ofile.write("\n}\n")

			if(ca.data.vray_cam_mode == 'PHYSICAL'):
				PHYS= {
					"STILL":     0,
					"CINEMATIC": 1,
					"VIDEO":     2
				}

				focus_distance= ca.data.dof_distance
				if(focus_distance == 0.0):
					focus_distance= 200.0

				ofile.write("\nCameraPhysical {")
				ofile.write("\n\ttype= %d;"%(PHYS[ca.data.vray_cam_phys_type]))
				ofile.write("\n\ttargeted= 0;")
				ofile.write("\n\tspecify_focus= 1;")
				ofile.write("\n\tfocus_distance= %s;"%(a(sce,focus_distance)))
				ofile.write("\n\tspecify_fov= 1;")
				ofile.write("\n\tfov= %s;"%(a(sce,fov)))
				ofile.write("\n\twhite_balance= %s;"%(a(sce,"Color(%.3f,%.3f,%.3f)"%(tuple(ca.data.VRayCamera.white_balance)))))
				for param in OBJECT_PARAMS['CameraPhysical']:
					ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ca.data, "vray_cam_phys_%s"%(param)))))
				ofile.write("\n}\n")

			else:
				ofile.write("\nSettingsCamera {")
				ofile.write("\n\ttype= %i;"%(0))
				ofile.write("\n\tfov= %s;"%(a(sce,fov)))
				ofile.write("\n}\n")

		if ve.animation:
			selected_frame= sce.frame_current
			f= sce.frame_start
			while(f <= sce.frame_end):
				exported_nodes= []
				sce.set_frame(f)
				#sce.frame_current= f
				write_ca(sce,ca)
				f+= sce.frame_step
			sce.set_frame(selected_frame)
		else:
			write_ca(sce,ca)

		if ofile is None:
			ofile.close()
		print("V-Ray/Blender: Writing camera... done.")

	else:
		print("V-Ray/Blender: Error! No camera in the scene!")



def write_scene(sce):
	vsce= sce.vray_scene
	ve= vsce.exporter
	
	ofile= open(filenames['scene'], 'w')

	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Scene file\n\n")

	for f in ['geometry', 'materials', 'lights', 'nodes', 'camera']:
		ofile.write("#include \"%s\"\n"%(os.path.basename(filenames[f])))

	module= vsce.SettingsImageSampler
	if module.filter_type != 'NONE':
		ofile.write(AA_FILTER_TYPE[module.filter_type])
		ofile.write("\n\tsize= %.3f;"%(module.filter_size))
		ofile.write("\n}\n")

	for module in MODULES:
		vmodule= getattr(vsce, module)

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
		if hasattr(vsce,plugin.PLUG):
			rna_pointer= getattr(vsce,plugin.PLUG)
			if hasattr(plugin,'write'):
				plugin.write(ofile,sce,rna_pointer)

	dmc= vsce.SettingsDMCSampler
	gi= vsce.SettingsGI
	im= vsce.SettingsGI.SettingsIrradianceMap
	lc= vsce.SettingsGI.SettingsLightCache
	bf= vsce.SettingsGI.SettingsDMCGI
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
		#ofile.write("\n\tauto_save= %d;"%(im.auto_save))
		#ofile.write("\n\tauto_save_file= \"%s\";"%(os.path.join(filenames["lmapspath"], im.auto_save_file))
		#ofile.write("\n\tfile= \"%s\";"%(im.file))
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
		#ofile.write("\n\tauto_save= %d;"%(lc.auto_save))
		#ofile.write("\n\tauto_save_file= \"%s\";"%(os.path.join(filenames["lmapspath"], lc.auto_save_file))
		#ofile.write("\n\tfile= \"%s\";"%(lc.file))
		ofile.write("\n}\n")

	ofile.write("\nSettingsEXR {")
	ofile.write("\n\tcompression= 0;") # 0 - default, 1 - no compression, 2 - RLE, 3 - ZIPS, 4 - ZIP, 5 - PIZ, 6 - pxr24
	ofile.write("\n\tbits_per_channel= 32;")
	ofile.write("\n}\n")

	# ofile.write("\nRTEngine {")
	# ofile.write("\n\tseparate_window= 0;")
	# ofile.write("\n\ttrace_depth= 3;")
	# ofile.write("\n\tuse_gi= 1;")
	# ofile.write("\n\tgi_depth= 3;")
	# ofile.write("\n\tgi_reflective_caustics= 1;")
	# ofile.write("\n\tgi_refractive_caustics= 1;")
	# ofile.write("\n\tuse_opencl= 1;")
	# ofile.write("\n}\n"	)	

	for channel in vsce.render_channels:
		plugin= get_plugin(CHANNEL_PLUGINS, channel.type)
		if plugin is not None:
			plugin.write(ofile, getattr(channel,plugin.PLUG), name= channel.name)

	ofile.write("\n")
	ofile.close()


def get_filenames(sce):
	global filenames

	rd= sce.render

	default_path= tempfile.gettempdir()
	
	output_dir= bpy.path.abspath(rd.output_path)

	if 0:
		(blendpath, blendname)= os.path.split(bpy.data.filename)
	else:
		filename= "scene"
		filepath= default_path
		print("V-Ray/Blender: Using $TEMP directory: %s"%(filepath))

	basepath= ""
	texpath= ""

	if 0:
		# DR
		pass
	else:
		basepath= os.path.join(filepath, 'vb25')

	if not os.path.exists(basepath):
		print("V-Ray/Blender: Exporting path doesn't exist, trying to create...")
		print("V-Ray/Blender: Creating directory %s"%(basepath))
		try:
			os.mkdir(basepath)
		except:
			print("V-Ray/Blender: Creating directory \"%s\" failed!"%(basepath))
			basepath= default_path
			print("V-Ray/Blender: Using default export path: %s"%(basepath))

	basename= os.path.join(basepath, filename)

	output_dir= os.path.join(basepath, 'render')
	if not os.path.exists(output_dir):
		print("V-Ray/Blender: Render autosave path doesn\'t exist, trying to create...")
		print("V-Ray/Blender: Creating directory %s"%(output_dir))
		try:
			os.mkdir(output_dir)
		except:
			print("V-Ray/Blender: Creating directory \"%s\" failed!"%(output_dir))
			output_dir= default_path
			print("V-Ray/Blender: Using default render output path: %s"%(output_dir))

	# TODO: move to RNA
	filenames= {}
	filenames['name']= filename
	filenames['scene']= basename + ".vrscene"
	filenames['geometry']= basename + "_geometry.vrscene"
	filenames['materials']= basename + "_materials.vrscene"
	filenames['lights']= basename + "_lights.vrscene"
	filenames['nodes']= basename + "_nodes.vrscene"
	filenames['camera']= basename + "_camera.vrscene"
	filenames['path']= basepath
	filenames['output']= output_dir



'''
  V-Ray Renderer
'''
class SCENE_OT_vray_export_meshes(bpy.types.Operator):
	bl_idname = "vray_export_meshes"
	bl_label = "Export meshes"
	bl_description = "Export Meshes"

	def invoke(self, context, event):
		sce= context.scene

		get_filenames(sce)
		write_geometry(sce)

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
	bl_preview = False
	
	def render(self, scene):
		global sce
		global rd
		global wo

		sce= scene
		rd=  scene.render
		wo=  scene.world

		# TEMP
		if rd.display_mode != 'AREA':
			rd.display_mode= 'AREA'

		vsce= sce.vray_scene
		ve= vsce.exporter

		get_filenames(sce)

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(filenames['output'],"render.%s" % get_render_file_format(ve,rd.file_format))
		
		if sce.name == "preview":
			image_file= os.path.join(filenames['output'],"preview.exr")

			exported_bitmaps= []
			ofile= open(os.path.join(vb_path,"preview","preview_materials.vrscene"), 'w')
			for ob in sce.objects:
				if ob.type in ('LAMP','ARMATURE','EMPTY'):
					continue
				if ob.type == 'CAMERA':
					if ob.name == "Camera":
						write_camera(sce,ob,ofile)
				for ms in ob.material_slots:
					if ob.name == "preview":
						write_material(ofile, exported_bitmaps, ms.material, name="PREVIEW")
					elif ms.material.name in ("checkerlight","checkerdark"):
						write_material(ofile, exported_bitmaps, ms.material)
			ofile.close()
			exported_bitmaps= []
		
			params.append('-sceneFile=')
			params.append(os.path.join(vb_path,"preview","preview.vrscene"))
			params.append('-display=')
			params.append("0")
			params.append('-imgFile=')
			params.append(image_file)
		else:
			if ve.auto_meshes:
				write_geometry(sce)
			write_materials(sce)
			write_nodes(sce)
			write_lamps(sce)
			write_camera(sce)
			write_scene(sce)

			if(rd.use_border):
				x0= wx * rd.border_min_x
				y0= wy * (1.0 - rd.border_max_y)
				x1= wx * rd.border_max_x
				y1= wy * (1.0 - rd.border_min_y)

				region= "%i;%i;%i;%i"%(x0,y0,x1,y1)

				if(rd.crop_to_border):
					params.append('-crop=')
				else:
					params.append('-region=')
				params.append(region)

			params.append('-sceneFile=')
			params.append(filenames['scene'])

			if ve.image_to_blender:
				params.append('-autoclose=')
				params.append('1')

			if ve.animation:
				params.append('-frames=')
				params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))

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
								# if rd.use_border and not rd.crop_to_border:
								# 	wx= rd.resolution_x * rd.resolution_percentage / 100
								# 	wy= rd.resolution_y * rd.resolution_percentage / 100
								result= self.begin_result(0, 0, int(wx), int(wy))
								result.layers[0].load_from_file(image_file)
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
	bl_preview = True
	
	def render(self, scene):
		global sce
		global rd
		global wo

		sce= scene
		rd=  scene.render
		wo=  scene.world

		# TEMP
		if rd.display_mode != 'AREA':
			rd.display_mode= 'AREA'

		vsce= sce.vray_scene
		ve= vsce.exporter

		get_filenames(sce)

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(filenames['output'],"render.%s" % get_render_file_format(ve,rd.file_format))
		
		if sce.name == "preview":
			image_file= os.path.join(filenames['output'],"preview.exr")

			exported_bitmaps= []
			ofile= open(os.path.join(vb_path,"preview","preview_materials.vrscene"), 'w')
			for ob in sce.objects:
				if ob.type in ('LAMP','ARMATURE','EMPTY'):
					continue
				if ob.type == 'CAMERA':
					if ob.name == "Camera":
						write_camera(sce,ob,ofile)
				for ms in ob.material_slots:
					if ob.name == "preview":
						write_material(ofile, exported_bitmaps, ms.material, name="PREVIEW")
					elif ms.material.name in ("checkerlight","checkerdark"):
						write_material(ofile, exported_bitmaps, ms.material)
			ofile.close()
			exported_bitmaps= []
		
			params.append('-sceneFile=')
			params.append(os.path.join(vb_path,"preview","preview.vrscene"))
			params.append('-display=')
			params.append("0")
			params.append('-imgFile=')
			params.append(image_file)
		else:
			if ve.auto_meshes:
				write_geometry(sce)
			write_materials(sce)
			write_nodes(sce)
			write_lamps(sce)
			write_camera(sce)
			write_scene(sce)

			if(rd.use_border):
				x0= wx * rd.border_min_x
				y0= wy * (1.0 - rd.border_max_y)
				x1= wx * rd.border_max_x
				y1= wy * (1.0 - rd.border_min_y)

				region= "%i;%i;%i;%i"%(x0,y0,x1,y1)

				if(rd.crop_to_border):
					params.append('-crop=')
				else:
					params.append('-region=')
				params.append(region)

			params.append('-sceneFile=')
			params.append(filenames['scene'])

			if ve.image_to_blender:
				params.append('-autoclose=')
				params.append('1')

			if ve.animation:
				params.append('-frames=')
				params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))

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
								# if rd.use_border and not rd.crop_to_border:
								# 	wx= rd.resolution_x * rd.resolution_percentage / 100
								# 	wy= rd.resolution_y * rd.resolution_percentage / 100
								result= self.begin_result(0, 0, int(wx), int(wy))
								layer= result.layers[0]
								layer.load_from_file(image_file)
								self.end_result(result)
					except:
						pass
					break

				time.sleep(0.05)
		else:
			print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")


# bpy.types.register(SCENE_OT_vray_export_meshes)
# bpy.types.register(SCENE_OT_vray_create_proxy)
# bpy.types.register(SCENE_OT_vray_replace_proxy)
# bpy.types.register(VRayRenderer)

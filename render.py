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
PLATFORM= sys.platform

TEX_TYPES= ('IMAGE', 'PLUGIN')

none_matrix= mathutils.Matrix( [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0] )


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

UNITS= {
	'DEFUALT' : 0,
	'LUMENS'  : 1,
	'LUMM'    : 2,
	'WATTSM'  : 3,
	'WATM'    : 4
}

SKY_MODEL= {
	'CIEOVER'  : 2,
	'CIECLEAR' : 1,
	'PREETH'   : 0
}


def get_tex_plugin(plugin_type):
	for plugin in TEX_PLUGINS:
		if plugin.ID == plugin_type:
			return plugin
	return None


'''
  MESHES
'''
def write_geometry():
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
			vb_active_layers= sce.vray_export_active_layers,
			vb_animation= sce.vray_export_animation
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

			if(sce.vray_debug):
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

			if ob.data.vray_proxy:
				continue

			if sce.vray_export_active_layers:
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

		if sce.vray_export_animation and len(DYNAMIC_OBJECTS):
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
	
	proxy_name= "Proxy_%s" % clean_string(os.path.basename(ob.data.vray_proxy_file))

	if(proxy_name not in exported_proxy):
		exported_proxy.append(proxy_name)
		ofile.write("\nGeomMeshFile %s {"%(proxy_name))
		ofile.write("\n\tfile= \"%s\";"%(get_full_filepath(ob.data.vray_proxy_file)))
		ofile.write("\n\tanim_speed= %i;"%(ob.data.vray_proxy_anim_speed))
		ofile.write("\n\tanim_type= %i;"%(ANIM_TYPE[ob.data.vray_proxy_anim_type]))
		ofile.write("\n\tanim_offset= %i;"%(ob.data.vray_proxy_anim_offset))
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


def write_TexPlugin(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, ob= None, env= None, env_type= None):
	tex_name= "Texture_no_texture"

	if slot:
		tex= slot.texture

	vtex= tex.vray_texture

	if tex:
		plugin= get_tex_plugin(vtex.type)
		if plugin is not None:
			tex_name= plugin.write(ofile, sce, tex)

	return tex_name


def write_texture(ofile, exported_bitmaps= None, ma= None, slot= None, tex= None, env= None):
	if(slot):
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
	ofile.write("\n}\n")
	return brdf_name


def write_BRDFSSS2Complex(ofile, ma, ma_name, tex_vray):
	SCATTER= {
		"NONE":   0,
		"SIMPLE": 1,
		"SOLID":  2,
		"REFR":   3
	}

	brdf_name= "BRDFSSS2Complex_%s"%(ma_name)

	ofile.write("\nBRDFSSS2Complex %s {"%(brdf_name))
	ofile.write("\n\tsingle_scatter= %s;"%(a(sce,SCATTER[ma.vray_fsss_single_scatter])))
	for param in OBJECT_PARAMS['BRDFSSS2Complex']:
		ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ma, "vray_fsss_%s"%(param)))))
	ofile.write("\n}\n")

	return brdf_name


# def write_BRDFGlossy(ofile, ma, ma_name, tex_vray):
# 	rm= ma.raytrace_mirror

# 	brdf_name= "BRDFGlossy_%s"%(ma_name)

# 	if(ma.vray_brdf == 'PHONG'):
# 		ofile.write("\nBRDFPhong %s {"%(brdf_name))
# 	elif(ma.vray_brdf == 'WARD'):
# 		ofile.write("\nBRDFWard %s {"%(brdf_name))
# 	else:
# 		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

# 	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_reflect_color)))))
# 	ofile.write("\n\tsubdivs= %i;"%(rm.gloss_samples))

# 	if(tex_vray['reflect']):
# 		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
# 		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
# 	else:
# 		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(
# 			1.0 - ma.vray_reflect_color[0],
# 			1.0 - ma.vray_reflect_color[1],
# 			1.0 - ma.vray_reflect_color[2]))))

# 	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,rm.gloss_factor)))
# 	ofile.write("\n\thilightGlossiness= %s;"%(a(sce,ma.vray_hilightGlossiness)))
# 	if(tex_vray['reflect_glossiness']):
# 		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['reflect_glossiness'])))
# 	if(tex_vray['hilight_glossiness']):
# 		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['hilight_glossiness'])))
# 	ofile.write("\n\tback_side= %s;"%(a(sce,ma.vray_back_side)))
# 	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
# 	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rm.depth)))
# 	if(not ma.vray_brdf == 'PHONG'):
# 		ofile.write("\n\tanisotropy= %s;"%(a(sce,ma.vray_anisotropy)))
# 		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,ma.vray_anisotropy_rotation)))
# 	ofile.write("\n\tcutoff= %s;"%(a(sce,rm.gloss_threshold)))
# 	ofile.write("\n}\n")

# 	return brdf_name


# def write_BRDFGlass(ofile, ma, ma_name, tex_vray):
# 	rt= ma.raytrace_transparency

# 	brdf_name= "BRDFGlass_%s"%(ma_name)

# 	ofile.write("\nBRDFGlass %s {"%(brdf_name))
# 	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
# 	if(tex_vray['refract']):
# 		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
# 	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
# 	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
# 	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
# 	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
# 	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
# 	ofile.write("\n}\n")

# 	return brdf_name


# def write_BRDFGlassGlossy(ofile, ma, ma_name, tex_vray):
# 	rt= ma.raytrace_transparency

# 	brdf_name= "BRDFGlassGlossy_%s"%(ma_name)

# 	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
# 	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
# 	if(tex_vray['refract']):
# 		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
# 	ofile.write("\n\tglossiness= %s;"%(a(sce,rt.gloss_factor)))
# 	ofile.write("\n\tsubdivs= %i;"%(rt.gloss_samples))
# 	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
# 	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
# 	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
# 	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
# 	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
# 	ofile.write("\n}\n")

# 	return brdf_name


def write_BRDFVRayMtl(ofile, ma, ma_name, tex_vray):
	BRDFS= {
		'PHONG': 0,
		'BLINN': 1,
		'WARD':  2
	}

	rm= ma.raytrace_mirror
	rt= ma.raytrace_transparency

	brdf_name= "BRDFVRayMtl_%s"%(ma_name)

	ofile.write("\nBRDFVRayMtl %s {"%(brdf_name))

	# float texture = 1, The opacity of the material
	if(tex_vray['alpha']):
		ofile.write("\n\topacity= %s::out_intensity;"%(tex_vray['alpha']))
	else:
		ofile.write("\n\topacity= %s;"%(a(sce,"%.6f"%(ma.alpha))))

	# acolor texture = AColor(0.5, 0.5, 0.5, 1), The diffuse color of the material
	if(tex_vray['color']):
		ofile.write("\n\tdiffuse= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tdiffuse= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.diffuse_color)))))

	# float texture = 0, The roughness of the diffuse part of the material
	ofile.write("\n\troughness= %s;"%(a(sce,ma.vray_roughness)))

	# integer = 1, The BRDF type (0 - Phong, 1 - Blinn, 2 - Ward)
	ofile.write("\n\tbrdf_type= %s;"%(a(sce,BRDFS[ma.vray_brdf])))

	# acolor texture = AColor(0, 0, 0, 1), The reflection color of the material
	if(tex_vray['reflect']):
		ofile.write("\n\treflect= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\treflect= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.vray_reflect_color)))))

	# integer = 8, Subdivs for glossy reflectons
	ofile.write("\n\treflect_subdivs= %s;"%(p(rm.gloss_samples)))

	# bool = true, true to trace reflections and false to only do hilights
	ofile.write("\n\treflect_trace= %s;"%(p(ma.vray_trace_reflections)))

	# integer = 5, The maximum depth for reflections
	ofile.write("\n\treflect_depth= %s;"%(p(rm.depth)))

	# color = Color(0, 0, 0), The color to use when the maximum depth is reached
	ofile.write("\n\treflect_exit_color= %s;"%(a(sce,"Color(0, 0, 0)")))

	# float = 1e+18, How much to dim reflection as length of rays increases
	ofile.write("\n\treflect_dim_distance= %s;"%(a(sce,0.1)))

	# bool = false, True to enable dim distance
	ofile.write("\n\treflect_dim_distance_on= %s;"%(a(sce,0)))

	# float = 0, Fall off for the dim distance
	ofile.write("\n\treflect_dim_distance_falloff= %s;"%(a(sce,0)))
	# float texture = 1, The glossiness of the reflections
	if(tex_vray['reflect_glossiness']):
		ofile.write("\n\treflect_glossiness= %s::out_intensity;"%(tex_vray['reflect_glossiness']))
	else:
		ofile.write("\n\treflect_glossiness= %s;"%(a(sce,rm.gloss_factor)))

	# float texture = 1, The glossiness of the hilights
	if(tex_vray['hilight_glossiness']):
		ofile.write("\n\thilight_glossiness= %s::out_intensity;"%(tex_vray['hilight_glossiness']))
	else:
		ofile.write("\n\thilight_glossiness= %s;"%(a(sce,ma.vray_hilightGlossiness)))

	# bool = true, true to use the reflection glossiness also for hilights (hilight_glossiness is ignored)
	ofile.write("\n\thilight_glossiness_lock= %s;"%(1))

	# float = 0, How much to soften hilights and reflections at grazing light angles
	ofile.write("\n\thilight_soften= %s;"%(a(sce,0)))

	# bool = false, true to enable fresnel reflections
	ofile.write("\n\tfresnel= %s;"%(a(sce,ma.vray_fresnel)))

	# float texture = 1.6, The ior for calculating the Fresnel term
	ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior)))

	# bool = true, true to use the refraction ior also for the Fresnel term (fresnel_ior is ignored)
	#ofile.write("\n\tfresnel_ior_lock= %s;"%(a(sce,ma.vray_fresnel_ior_lock)))
	ofile.write("\n\tfresnel_ior_lock= %s;"%(0))

	# float texture = 0, The anisotropy for glossy reflections, from -1 to 1 (0.0 is isotropic reflections)
	ofile.write("\n\tanisotropy= %s;"%(a(sce,ma.vray_anisotropy)))

	# float texture = 0, The rotation of the anisotropy axes, from 0.0 to 1.0
	ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,ma.vray_anisotropy_rotation)))

	# integer = 0, What method to use for deriving anisotropy axes (0 - local object axis; 1 - a specified uvw generator)
	ofile.write("\n\tanisotropy_derivation= %s;"%(a(sce,0)))

	# integer = 2, Which local object axis to use when anisotropy_derivation is 0
	ofile.write("\n\tanisotropy_axis= %s;"%(a(sce,2)))

	# plugin, The uvw generator to use for anisotropy when anisotropy_derivation is 1
	#ofile.write("\n\tanisotropy_uvwgen= %s;"%(a(sce,)))

	# acolor texture = AColor(0, 0, 0, 1), The refraction color of the material
	if(tex_vray['refract']):
		ofile.write("\n\trefract= %s;"%(tex_vray['refract']))
	else:
		ofile.write("\n\trefract= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.vray_refract_color)))))

	# float texture = 1.6, The IOR for refractions
	ofile.write("\n\trefract_ior= %s;"%(a(sce,rt.ior)))

	# float texture = 1, Glossiness for refractions
	ofile.write("\n\trefract_glossiness= %s;"%(a(sce,rt.gloss_factor)))

	# integer = 8, Subdivs for glossy refractions
	ofile.write("\n\trefract_subdivs= %s;"%(a(sce,rt.gloss_samples)))

	# bool = true, 1 to trace refractions; 0 to disable them
	ofile.write("\n\trefract_trace= %s;"%(p(ma.vray_trace_refractions)))

	# integer = 5, The maximum depth for refractions
	ofile.write("\n\trefract_depth= %s;"%(a(sce,rt.depth)))

	# color = Color(0, 0, 0), The color to use when maximum depth is reached when refract_exit_color_on is true
	ofile.write("\n\trefract_exit_color= %s;"%(a(sce,"Color(0, 0, 0)")))

	# bool = false, If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray
	ofile.write("\n\trefract_exit_color_on= %s;"%(a(sce,0)))

	# integer = 0, Determines how refractions affect the alpha channel (0 - opaque alpha; 1 - alpha is taken from refractions; 2 - all channels are propagated
	ofile.write("\n\trefract_affect_alpha= %s;"%(p(ma.vray_affect_alpha)))

	# bool = false, true to enable the refraction to affect the shadows cast by the material (as transparent shadows)
	ofile.write("\n\trefract_affect_shadows= %s;"%(p(ma.vray_affect_shadows)))

	# color = Color(1, 1, 1), The absorption (fog) color
	ofile.write("\n\tfog_color= %s;"%(a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%(tuple(ma.vray_fog_color)))))

	# float = 1, Multiplier for the absorption
	ofile.write("\n\tfog_mult= %s;"%(a(sce,ma.vray_fog_color_mult * 10)))

	# float = 0, Bias for the absorption
	ofile.write("\n\tfog_bias= %s;"%(a(sce,ma.vray_fog_bias)))

	# integer = 0, Translucency mode (0 - none)
	ofile.write("\n\ttranslucency= %s;"%(a(sce,0)))

	# acolor texture = AColor(1, 1, 1, 1), Filter color for the translucency effect
	ofile.write("\n\ttranslucency_color= %s;"%(a(sce,"AColor(1, 1, 1, 1)")))

	# float = 1, A multiplier for the calculated lighting for the translucency effect
	ofile.write("\n\ttranslucency_light_mult= %s;"%(a(sce,1.0)))

	# float = 0.5, Scatter direction (0.0f is backward, 1.0f is forward)
	ofile.write("\n\ttranslucency_scatter_dir= %s;"%(a(sce,0.5)))

	# float = 0, Scattering cone (0.0f - no scattering, 1.0f - full scattering
	ofile.write("\n\ttranslucency_scatter_coeff= %s;"%(a(sce,0.0)))

	# float = 1e+18, Maximum distance to trace inside the object
	ofile.write("\n\ttranslucency_thickness= %s;"%(a(sce,0.1)))

	# bool = true, true if the material is double-sided
	ofile.write("\n\toption_double_sided= %s;"%(a(sce,ma.vray_double_sided)))

	# bool = false, true to compute reflections for back sides of objects
	ofile.write("\n\toption_reflect_on_back= %s;"%(a(sce,ma.vray_back_side)))

	# integer = 1, Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always
	ofile.write("\n\toption_glossy_rays_as_gi= %s;"%(a(sce,1)))

	# float = 0.001, Specifies a cutoff threshold for tracing reflections/refractions
	ofile.write("\n\toption_cutoff= %s;"%(a(sce,0.001)))

	# bool = true, false to perform local brute-force GI calculatons and true to use the current GI engine
	ofile.write("\n\toption_use_irradiance_map= %s;"%(a(sce,1)))

	# integer = 0, Energy preservation mode for reflections and refractions (0 - color, 1 - monochrome)
	ofile.write("\n\toption_energy_mode= %s;"%(a(sce,0)))

	# acolor texture, Environment override texture
	#ofile.write("\n\tenvironment_override= %s;"%(a(sce,)))

	# integer = 0, Environment override priority (used when several materials override it along a ray path)
	ofile.write("\n\tenvironment_priority= %s;"%(a(sce,0)))
	ofile.write("\n}\n")

	return brdf_name


def write_TexAColorOp(tex, mult, tex_name= None):
	brdf_name= "TexAColorOp_%s"%(tex)
	if(tex_name):
		brdf_name= "TexAColorOp_%s"%(tex_name)

	ofile.write("\nTexAColorOp %s {"%(brdf_name))
	ofile.write("\n\tcolor_a= %s;"%(a(sce,tex)))
	ofile.write("\n\tmult_a= %s;"%(a(sce,mult)))
	ofile.write("\n}\n")

	return brdf_name


# def write_BRDFMirror(ofile, ma, ma_name, tex_vray):
# 	rm= ma.raytrace_mirror

# 	brdf_name= "BRDFMirror_%s"%(ma_name)

# 	ofile.write("\nBRDFMirror %s {"%(brdf_name))
# 	if(tex_vray['color']):
# 		ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
# 	else:
# 		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
# 	if(tex_vray['reflect']):
# 		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
# 		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
# 	else:
# 		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
# 	ofile.write("\n\tback_side= %d;"%(ma.vray_back_side))
# 	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
# 	ofile.write("\n\ttrace_depth= %i;"%(rm.depth))
# 	ofile.write("\n\tcutoff= %.6f;"%(0.01))
# 	ofile.write("\n}\n")

# 	return brdf_name


def write_TexCompMax(name, sourceA, sourceB):
	tex_name= "TexCompMax_%s"%(name)

	ofile.write("\nTexCompMax %s {"%(tex_name))
	ofile.write("\n\tsourceA= %s;"%(sourceA))
	ofile.write("\n\tsourceB= %s;"%(sourceB))
	# 0:Add, 1:Subtract, 2:Difference, 3:Multiply, 4:Divide, 5:Minimum, 6:Maximum
	ofile.write("\n\toperator= %d;"%(3)) 
	ofile.write("\n}\n")

	return tex_name


def write_TexInvert(name):
	tex_name= "TexInvert_%s"%(name)

	ofile.write("\nTexInvert %s {"%(tex_name))
	ofile.write("\n\ttexture= %s;"%(tex))
	ofile.write("\n}\n")

	return tex_name


def write_TexFresnel(ofile, ma, ma_name, tex_vray):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {"%(tex_name))
	if(tex_vray["reflect"]):
		ofile.write("\n\tblack_color= %s;"%(tex_vray["reflect"]))
	else:
		ofile.write("\n\tblack_color= %s;"%(a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior)))
	ofile.write("\n}\n")

	return tex_name


def write_BRDFLight(ofile, ma, ma_name, tex_vray):
	brdf_name= "BRDFLight_%s"%(ma_name)

	if(tex_vray['color']):
		color= tex_vray['color']
	else:
		color= "Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color))

	if(tex_vray['alpha']):
		alpha= exportTexInvert(tex_vray['alpha'])
		color= exportTexCompMax("%s_alpha"%(brdf_name), alpha, color)

	ofile.write("\nBRDFLight %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"%s"%(color))))
	ofile.write("\n\tcolorMultiplier= %s;"%(a(sce,ma.emit * 10)))
	ofile.write("\n\tcompensateExposure= %s;"%(a(sce,ma.vray_mtl_compensateExposure)))

	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency= %s;"%(a(sce,tex_vray['alpha'])))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))

	ofile.write("\n\temitOnBackSide= %s;"%(a(sce,ma.vray_mtl_emitOnBackSide)))
	ofile.write("\n}\n")

	return brdf_name


# def write_BRDFDiffuse(ofile, ma, ma_name, tex_vray):
# 	brdf_name= "BRDFDiffuse_%s"%(ma_name)

# 	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
# 	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
# 	ofile.write("\n\troughness= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(ma.vray_roughness,ma.vray_roughness,ma.vray_roughness))))
# 	if(tex_vray['color']):
# 		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['color']))
# 	ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
# 	if(tex_vray['alpha']):
# 		ofile.write("\n\ttransparency_tex= %s;"%(a(sce,tex_vray['alpha'])))
# 	ofile.write("\n}\n")

# 	return brdf_name


# def write_BRDF(ofile, ma, ma_name, tex_vray):
# 	def bool_color(color, level):
# 		for c in color:
# 			if c > level:
# 				return True
# 		return False

# 	rm= ma.raytrace_mirror
# 	rt= ma.raytrace_transparency

# 	brdfs= []

# 	if(tex_vray['reflect']):
# 		tex_vray['reflect']= write_TexInvert(tex_vray['reflect'])

# 	if(ma.vray_fresnel):
# 		tex_vray['reflect']= write_TexFresnel(ofile, ma, ma_name, tex_vray)

# 	if(tex_vray['reflect'] or bool_color(ma.vray_reflect_color, 0.0)):
# 		if(rm.gloss_factor < 1.0 or tex_vray['reflect_glossiness']):
# 			brdf_name= write_BRDFGlossy(ofile, ma, ma_name, tex_vray)
# 		else:
# 			brdf_name= write_BRDFMirror(ofile, ma, ma_name, tex_vray)
# 		brdfs.append(brdf_name)

# 	if(tex_vray['refract'] or bool_color(ma.vray_refract_color, 0.0)):
# 		if(rt.gloss_factor < 1.0 or tex_vray['refract_glossiness']):
# 			brdf_name= write_BRDFGlassGlossy(ofile, ma, ma_name, tex_vray)
# 		else:
# 			brdf_name= write_BRDFGlass(ofile, ma, ma_name, tex_vray)
# 	else:
# 		brdf_name= write_BRDFDiffuse(ofile, ma, ma_name, tex_vray)
# 	brdfs.append(brdf_name)

# 	if(len(brdfs) == 1):
# 		brdf_name= brdfs[0]
# 	else:
# 		brdf_name= "BRDFLayered_%s"%(ma_name)

# 		ofile.write("\nBRDFLayered %s {"%(brdf_name))
# 		ofile.write("\n\tbrdfs= List(")
# 		brdfs_out= ""
# 		for brdf in brdfs:
# 			brdfs_out+= "\n\t\t%s,"%(brdf)
# 		ofile.write(brdfs_out[0:-1])
# 		ofile.write("\n\t);")
# 		ofile.write("\n\tadditive_mode= %s;"%(0)); # For shellac
# 		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
# 		if(tex_vray['alpha']):
# 			ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['alpha']))
# 		ofile.write("\n}\n")

# 	return brdf_name



def	write_material(ofile, exported_bitmaps, ma, name= None):
	ma_name= get_name(ma,"Material")
	if(name):
		ma_name= name

	if(ma.vray_mtl_two_sided and ma.vray_mtl_use_wrapper and ma.vray_mtl_renderstats):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		wrap_material= "MtlWrapper_%s"%(ma_name)
		wrap_base= ts_material
		rstat_material= ma_name
		rstat_base= wrap_material
		
	elif(ma.vray_mtl_two_sided and ma.vray_mtl_renderstats and not ma.vray_mtl_use_wrapper):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		rstat_base= ts_material
		rstat_material= ma_name
	
	elif(ma.vray_mtl_two_sided and ma.vray_mtl_use_wrapper and not ma.vray_mtl_renderstats):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= "Mtl2Sided_%s"%(ma_name)
		wrap_base= ts_material
		wrap_material= ma_name

	elif(ma.vray_mtl_use_wrapper and ma.vray_mtl_renderstats and not ma.vray_mtl_two_sided):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		wrap_material= "MtlWrapper_%s"%(ma_name)
		wrap_base= base_material
		rstat_material= ma_name
		rstat_base= wrap_material

	elif(ma.vray_mtl_two_sided):
		base_material= "MtlSingleBRDF_%s"%(ma_name)
		ts_material= ma_name

	else:
		base_material= ma_name
		
	
	ofile.write("\n//\n// Material: %s\n//"%(ma.name))

	brdf_name= "BRDFDiffuse_no_material"

	tex_vray= write_textures(ofile, exported_bitmaps, ma, ma_name)

	if(ma.vray_mtl_type == 'MTL'):
		brdf_name= write_BRDFVRayMtl(ofile, ma, ma_name, tex_vray)
	elif(ma.vray_mtl_type == 'SSS'):
		brdf_name= write_BRDFSSS2Complex(ofile, ma, ma_name, tex_vray)
	elif(ma.vray_mtl_type == 'EMIT'):
		brdf_name= write_BRDFLight(ofile, ma, ma_name, tex_vray)
	else:
		return

	if(not ma.vray_mtl_type == 'EMIT'):
		if(tex_vray['bump'] or tex_vray['normal']):
			brdf_name= write_BRDFBump(ofile, brdf_name, tex_vray)

	if(ma.vray_mtl_two_sided):
		ofile.write("\nMtlSingleBRDF %s {"%(base_material))
		ofile.write("\n\tbrdf= %s;"%(brdf_name))
		ofile.write("\n}\n")
		ofile.write("\nMtl2Sided %s {"%(ts_material))
		ofile.write("\n\tfront= MtlSingleBRDF_%s;"%(base_material))
		ofile.write("\n\tback= MtlSingleBRDF_%s;"%(base_material))
		ofile.write("\n\ttranslucency= Color(%.3f, %.3f, %.3f);"%(ma.vray_mtlts_translucency,ma.vray_mtlts_translucency,ma.vray_mtlts_translucency))
		ofile.write("\n\tforce_1sided= 1;")
		ofile.write("\n}\n")
	else:
		ofile.write("\nMtlSingleBRDF %s {"%(base_material))
		ofile.write("\n\tbrdf= %s;"%(brdf_name))
		ofile.write("\n}\n")

	if(ma.vray_mtl_use_wrapper):
		ofile.write("\nMtlWrapper %s {"%(wrap_material))
		ofile.write("\n\tbase_material= %s;"%(wrap_base))
		for param in OBJECT_PARAMS['MtlWrapper']:
			if(param == 'matte_for_secondary_rays'):
				ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ma, 'vb_mwrap_matte_for_sec_rays'))))
			else:
				ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ma, "vb_mwrap_%s"%(param)))))
		ofile.write("\n}\n")
		
	if(ma.vray_mtl_renderstats):
		ofile.write("\nMtlRenderStats %s {"%(rstat_material))
		ofile.write("\n\tbase_mtl= %s;"%(rstat_base))
		for param in OBJECT_PARAMS['MtlRenderStats']:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ma, "vb_mrs_%s"%(param)))))
		ofile.write("\n}\n")


def write_materials():
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
			#ofile.write("\n\tadditive_mode= 1;") # Shellac
			ofile.write("\n}\n")
				
		elif(no.type == 'TEXTURE'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		elif(no.type == 'INVERT'):
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(no.name,no.type))

	def export_material(ofile, exported_bitmaps, ma):
		if(sce.vray_export_use_mat_nodes and ma.use_nodes and hasattr(ma.node_tree, 'links')):
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
	ofile.write("\n//\n// Materials...\n//")

	exported_bitmaps= []
	exported_nodes= []

	for ma in bpy.data.materials:
		if(ma.users or ma.fake_user):
			export_material(ofile, exported_bitmaps, ma)

	exported_bitmaps= []
	exported_nodes= []

	ofile.close()
	print("V-Ray/Blender: Writing materials... done.")




'''
  NODES
'''
def write_nodes():
	print("V-Ray/Blender: Writing nodes...")

	# Used when exporting dupli, particles etc.
	global exported_nodes
	global exported_proxy
	exported_nodes= []
	exported_proxy= []

	def write_node(ob, matrix= None):
		if ob.name not in exported_nodes:
			exported_nodes.append(ob.name)

			if(sce.vray_debug):
				print("V-Ray/Blender: Processing object: %s"%(ob.name))
				print("V-Ray/Blender:   Animated: %d"%(1 if ob.animation_data else 0))
				if(ob.data):
					print("V-Ray/Blender:   Mesh animated: %d"%(1 if ob.data.animation_data else 0))
			else:
				if(PLATFORM == "win32"):
					sys.stdout.write("V-Ray/Blender: [%d] Object: %s                              \r"%(sce.frame_current, ob.name))
				else:
					sys.stdout.write("V-Ray/Blender: [%d] Object: \033[0;32m%s\033[0m                              \r"%(sce.frame_current, ob.name))
				sys.stdout.flush()

			node_geometry= get_name(ob.data,"Geom")
			if(hasattr(ob.data,'vray_proxy')):
				if ob.data.vray_proxy:
					node_geometry= write_mesh_file(ofile, exported_proxy, ob)

			if(matrix):
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

			ofile.write("\nNode %s {"%(get_name(ob,"Node")))
			ofile.write("\n\tobjectID= %d;"%(ob.pass_index))
			ofile.write("\n\tgeometry= %s;"%(node_geometry))
			ofile.write("\n\tmaterial= %s;"%(ma_name))
			ofile.write("\n\ttransform= %s;"%(a(sce,transform(node_matrix))))
			ofile.write("\n}\n")

	ofile= open(filenames['nodes'], 'w')
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Node file\n")

	timer= time.clock()

	OBJECTS= []
	# STATIC_OBJECTS= []
	# DYNAMIC_OBJECTS= []

	for ob in sce.objects:
		if ob.type in ('LAMP','CAMERA','ARMATURE','EMPTY'):
			continue

		if sce.vray_export_active_layers:
			if not object_on_visible_layers(sce,ob):
				continue

		OBJECTS.append(ob)
		# if ob.animation_data:
		# 	DYNAMIC_OBJECTS.append(ob)
		# else:
		# 	STATIC_OBJECTS.append(ob)

	# for ob in STATIC_OBJECTS:
	# 	write_node(ob)

	if(sce.vray_export_animation):
		selected_frame= sce.frame_current
		f= sce.frame_start
		while(f <= sce.frame_end):
			exported_nodes= []
			sce.set_frame(f)
			#sce.frame_current= f
			#for ob in DYNAMIC_OBJECTS:
			for ob in OBJECTS:
				write_node(ob)
			f+= sce.frame_step
		sce.set_frame(selected_frame)
	else:
		#for ob in DYNAMIC_OBJECTS:
		for ob in OBJECTS:
			write_node(ob)

	exported_nodes= []
	exported_proxy= []

	OBJECTS= []
	# STATIC_OBJECTS= []
	# DYNAMIC_OBJECTS= []

	ofile.close()
	print("V-Ray/Blender: Writing nodes... done [%s]                    "%(time.clock() - timer))


def write_lamps():
	print("V-Ray/Blender: Writing lights...")

	ofile= open(filenames['lights'], 'w')
	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Lights file\n")

	for ob in sce.objects:
		if ob.type == 'LAMP':
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
		if sce.vray_export_animation:
			ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(ca.name),get_render_file_format(rd.file_format)))
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
				ofile.write("\n\twhite_balance= %s;"%(a(sce,"Color(%.3f,%.3f,%.3f)"%(tuple(ca.data.vray_cam_phys_white_balance)))))
				for param in OBJECT_PARAMS['CameraPhysical']:
					ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(ca.data, "vray_cam_phys_%s"%(param)))))
				ofile.write("\n}\n")

			else:
				ofile.write("\nSettingsCamera {")
				ofile.write("\n\ttype= %i;"%(0))
				ofile.write("\n\tfov= %s;"%(a(sce,fov)))
				ofile.write("\n}\n")

		if sce.vray_export_animation:
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



def write_scene():
	ofile= open(filenames['scene'], 'w')

	ofile.write("// V-Ray/Blender %s\n"%(VERSION))
	ofile.write("// Scene file\n\n")

	for f in ["geometry", "materials", "lights", "nodes", "camera"]:
		ofile.write("#include \"%s\"\n"%(os.path.basename(filenames[f])))


	ofile.write("\nSettingsRegionsGenerator {")
	ofile.write("\n\txc= %s;"%(32))
	ofile.write("\n\tyc= %s;"%(32))
	ofile.write("\n\txymeans= 0;")
	ofile.write("\n\tseqtype= 4;")
	ofile.write("\n\treverse= 0;")
	ofile.write("\n}\n")


	AA_FILTER= {
		'AREA'     : '\nFilterArea {',
		'BOX'      : '\nFilterBox {',
		'TRIANGLE' : '\nFilterTriangle {',
		'LANC'     : '\nFilterLanczos {',
		'SINC'     : '\nFilterSinc {',
		'GAUSS'    : '\nFilterGaussian {',
		'CATMULL'  : '\nFilterCatmullRom {'
	}

	if(not sce.vray_filter_type == 'NONE'):
		ofile.write(AA_FILTER[sce.vray_filter_type])
		ofile.write("\n\tsize= %.3f;"%(sce.vray_filter_size))
		ofile.write("\n}\n")

	for module in MODULES:
		ofile.write("\n%s {"%(module))
		if(module == 'SettingsImageSampler'):
			if(sce.vray_is_type == 'FXD'):
				ofile.write("\n\ttype= %d;"%(0))
			elif(sce.vray_is_type == 'DMC'):
				ofile.write("\n\ttype= %d;"%(1))
			else:
				ofile.write("\n\ttype= %d;"%(2))
		elif(module == 'SettingsColorMapping'):
			CM= {
				'LNR': 0,
				'EXP':  1,
				'HSV':  2,
				'INT':  3,
				'GCOR': 4,
				'GINT': 5,
				'REIN': 6
			}
			ofile.write("\n\ttype= %d;"%(CM[sce.vray_cm_type]))

			
		for param in MODULES[module]:
			ofile.write("\n\t%s= %s;"%(param, p(getattr(sce, "vray_%s"%(param)))))
		ofile.write("\n}\n")

	if(sce.vray_gi_on):
		# Enum currently doesn't extract value index, only name,
		# so...
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

		def settingsIM():
			ofile.write("\nSettingsIrradianceMap {")
			ofile.write("\n\tmin_rate= %i;"%(sce.vray_im_min_rate))
			ofile.write("\n\tmax_rate= %i;"%(sce.vray_im_max_rate))
			ofile.write("\n\tsubdivs= %i;"%(sce.vray_im_subdivs))
			ofile.write("\n\tinterp_samples= %i;"%(sce.vray_im_interp_samples))
			ofile.write("\n\tinterp_frames= %i;"%(sce.vray_im_interp_frames))
			ofile.write("\n\tcalc_interp_samples= %i;"%(sce.vray_im_calc_interp_samples))
			ofile.write("\n\tcolor_threshold= %.6f;"%(sce.vray_im_color_threshold))
			ofile.write("\n\tnormal_threshold= %.6f;"%(sce.vray_im_normal_threshold))
			ofile.write("\n\tdistance_threshold= %.6f;"%(sce.vray_im_distance_threshold))
			ofile.write("\n\tdetail_enhancement= %i;"%(sce.vray_im_detail_enhancement))
			ofile.write("\n\tdetail_radius= %.6f;"%(sce.vray_im_detail_radius))
			ofile.write("\n\tdetail_subdivs_mult= %.6f;"%(sce.vray_im_detail_subdivs_mult))
			ofile.write("\n\tdetail_scale= %i;"%(SCALE[sce.vray_im_detail_scale]))
			ofile.write("\n\tinterpolation_mode= %i;"%(INT_MODE[sce.vray_im_interpolationType]))
			ofile.write("\n\tlookup_mode= %i;"%(LOOK_TYPE[sce.vray_im_lookupType]))
			ofile.write("\n\tshow_calc_phase= %i;"%(sce.vray_im_show_calc_phase))
			ofile.write("\n\tshow_direct_light= %i;"%(sce.vray_im_show_direct_light))
			ofile.write("\n\tshow_samples= %i;"%(sce.vray_im_show_samples))
			ofile.write("\n\tmultipass= %i;"%(sce.vray_im_multipass))
			ofile.write("\n\tcheck_sample_visibility= %i;"%(sce.vray_im_check_sample_visibility))
			ofile.write("\n\trandomize_samples= %i;"%(sce.vray_im_randomize_samples))
			ofile.write("\n\tmode= %d;"%(IM_MODE[sce.vray_im_mode]))
			#ofile.write("\n\tauto_save= %d;"%(sce.vray_im_auto_save))
			#ofile.write("\n\tauto_save_file= \"%s\";"%(os.path.join(filenames["lmapspath"], sce.vray_im_auto_save_file))
			#ofile.write("\n\tfile= \"%s\";"%(sce.vray_im_file))
			ofile.write("\n}\n")

		def settingsBF():
			ofile.write("\nSettingsDMCGI {")
			ofile.write("\n\tsubdivs= %i;"%(sce.vray_dmcgi_subdivs))
			ofile.write("\n\tdepth= %i;"%(sce.vray_dmcgi_depth))
			ofile.write("\n}\n")

		def settingsLC():
			ofile.write("\nSettingsLightCache {")
			ofile.write("\n\tsubdivs= %.0f;"%(sce.vray_lc_subdivs * sce.vray_subdivs_mult))
			ofile.write("\n\tsample_size= %.6f;"%(sce.vray_lc_sample_size))
			ofile.write("\n\tnum_passes= %i;"%(sce.vray_lc_num_passes))
			ofile.write("\n\tdepth= %i;"%(sce.vray_lc_depth))
			ofile.write("\n\tfilter_type= %i;"%(LC_FILT[sce.vray_lc_filter_type]))
			ofile.write("\n\tfilter_samples= %i;"%(sce.vray_lc_filter_samples))
			ofile.write("\n\tfilter_size= %.6f;"%(sce.vray_lc_filter_size))
			ofile.write("\n\tprefilter= %i;"%(sce.vray_lc_prefilter))
			ofile.write("\n\tprefilter_samples= %i;"%(sce.vray_lc_prefilter_samples))
			ofile.write("\n\tshow_calc_phase= %i;"%(sce.vray_lc_show_calc_phase))
			ofile.write("\n\tstore_direct_light= %i;"%(sce.vray_lc_store_direct_light))
			ofile.write("\n\tuse_for_glossy_rays= %i;"%(sce.vray_lc_use_for_glossy_rays))
			ofile.write("\n\tworld_scale= %i;"%(SCALE[sce.vray_lc_scale]))
			ofile.write("\n\tadaptive_sampling= %i;"%(sce.vray_lc_adaptive_sampling))
			ofile.write("\n\tmode= %d;"%(LC_MODE[sce.vray_lc_mode]))
			#ofile.write("\n\tauto_save= %d;"%(sce.vray_lc_auto_save))
			#ofile.write("\n\tauto_save_file= \"%s\";"%(os.path.join(filenames["lmapspath"], sce.vray_lc_auto_save_file))
			#ofile.write("\n\tfile= \"%s\";"%(sce.vray_lc_file))
			ofile.write("\n}\n")

		ofile.write("\nSettingsGI {")
		ofile.write("\n\ton= 1;")
		ofile.write("\n\tprimary_engine= %s;"%(PRIMARY[sce.vray_gi_primary_engine]))
		ofile.write("\n\tsecondary_engine= %s;"%(SECONDARY[sce.vray_gi_secondary_engine]))
		ofile.write("\n\tprimary_multiplier= %s;"%(sce.vray_gi_primary_multiplier))
		ofile.write("\n\tsecondary_multiplier= %s;"%(sce.vray_gi_secondary_multiplier))
		ofile.write("\n\treflect_caustics= %s;"%(p(sce.vray_gi_reflect_caustics)))
		ofile.write("\n\trefract_caustics= %s;"%(p(sce.vray_gi_refract_caustics)))
		ofile.write("\n\tsaturation= %.6f;"%(sce.vray_gi_saturation))
		ofile.write("\n\tcontrast= %.6f;"%(sce.vray_gi_contrast))
		ofile.write("\n\tcontrast_base= %.6f;"%(sce.vray_gi_contrast_base))
		ofile.write("\n}\n")

		if(PRIMARY[sce.vray_gi_primary_engine] == 0):
			settingsIM()

		if(PRIMARY[sce.vray_gi_primary_engine] == 1 and SECONDARY[sce.vray_gi_secondary_engine] == 1):
			settingsPM()
		else:
			if(PRIMARY[sce.vray_gi_primary_engine] == 1):
				pass
			if(SECONDARY[sce.vray_gi_secondary_engine] == 1):
				pass

		if(PRIMARY[sce.vray_gi_primary_engine] == 2 and SECONDARY[sce.vray_gi_secondary_engine] == 2):
			settingsBF()
		else:
			if(PRIMARY[sce.vray_gi_primary_engine] == 2):
				settingsBF()
			if(SECONDARY[sce.vray_gi_secondary_engine] == 2):
				settingsBF()

		if(PRIMARY[sce.vray_gi_primary_engine] == 3 and SECONDARY[sce.vray_gi_secondary_engine] == 3):
			settingsLC()
		else:
			if(PRIMARY[sce.vray_gi_primary_engine] == 3):
				settingsLC()
			if(SECONDARY[sce.vray_gi_secondary_engine] == 3):
				settingsLC()

	passes= sce.render.layers[0]

	if(passes.pass_color or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Color {")
		ofile.write("\n\tname=\"VRay_Color\";")
		ofile.write("\n\talias= 101;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_diffuse or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Diffuse {")
		ofile.write("\n\tname=\"VRay_Diffuse\";")
		ofile.write("\n\talias= 107;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_specular or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Specular {")
		ofile.write("\n\tname=\"VRay_Specular\";")
		ofile.write("\n\talias= 106;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_reflection or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Reflection {")
		ofile.write("\n\tname=\"VRay_Reflection\";")
		ofile.write("\n\talias= 102;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Reflection_Filter {")
		ofile.write("\n\tname=\"VRay_Reflection_Filter\";")
		ofile.write("\n\talias= 118;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Raw_Reflection {")
		ofile.write("\n\tname=\"VRay_Raw_Reflection\";")
		ofile.write("\n\talias= 119;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_refraction or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Refract {")
		ofile.write("\n\tname=\"VRay_Refract\";")
		ofile.write("\n\talias= 103;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Refraction_Filter {")
		ofile.write("\n\tname=\"VRay_Refraction_Filter\";")
		ofile.write("\n\talias= 120;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Raw_Refraction {")
		ofile.write("\n\tname=\"VRay_Raw_Refraction\";")
		ofile.write("\n\talias= 121;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_lightning or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Raw_Lightning {")
		ofile.write("\n\tname=\"VRay_Raw_Lightning\";")
		ofile.write("\n\talias= 111;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Total_Lightning {")
		ofile.write("\n\tname=\"VRay_Total_Lightning\";")
		ofile.write("\n\talias= 129;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Raw_Total_Lightning {")
		ofile.write("\n\tname=\"VRay_Raw_Total_Lightning\";")
		ofile.write("\n\talias= 130;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_shadow or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Shadow {")
		ofile.write("\n\tname=\"VRay_Shadow\";")
		ofile.write("\n\talias= 105;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Raw_Shadow {")
		ofile.write("\n\tname=\"VRay_Raw_Shadow\";")
		ofile.write("\n\talias= 112;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Matte_Shadow {")
		ofile.write("\n\tname=\"VRay_Matte_Shadow\";")
		ofile.write("\n\talias= 128;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_sss or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_SSS {")
		ofile.write("\n\tname=\"VRay_SSS\";")
		ofile.write("\n\talias= 133;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_z or sce.vray_passes):
		ofile.write("\nRenderChannelZDepth {")
		ofile.write("\n\tname=\"ZDepth\";")
		ofile.write("\n\tdepth_from_camera = %s;"%(p(sce.vray_zdepth_depth_camera)))
		ofile.write("\n\tdepth_white= %s;"%(sce.vray_zdepth_depth_white))
		ofile.write("\n\tdepth_black= %s;"%(sce.vray_zdepth_depth_black))
		ofile.write("\n\tdepth_clamp= %s;"%(p(sce.vray_zdepth_depth_clamp)))
		ofile.write("\n}")

	if(passes.pass_vector or sce.vray_passes):
		ofile.write("\nRenderChannelVelocity {")
		ofile.write("\n\tname=\"Velocity\";")
		ofile.write("\n\tdclamp_velocity = %s;"%(p(sce.vray_velocity_clamp_velocity)))
		ofile.write("\n\tmax_velocity= %s;"%(sce.vray_velocity_max_velocity))
		ofile.write("\n\tmax_velocity_last_frame= %s;"%(sce.vray_velocity_max_velocity_last_frame))
		ofile.write("\n\tignore_z= %s;"%(p(sce.vray_velocity_ignore_z)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Velocity {")
		ofile.write("\n\tname=\"VRay_Velocity\";")
		ofile.write("\n\talias= 113;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_normal or sce.vray_passes):
		ofile.write("\nRenderChannelNormals {")
		ofile.write("\n\tname=\"Normals\";")
		ofile.write("\n}")

	if(passes.pass_object_index or sce.vray_passes):
		ofile.write("\nRenderChannelRenderID {")
		ofile.write("\n\tname=\"RenderID\";")
		ofile.write("\n}")

	if(passes.pass_emit or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Emit {")
		ofile.write("\n\tname=\"VRay_Emit\";")
		ofile.write("\n\talias= 104;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_ao or sce.vray_passes):
		ofile.write("\nTexDirt TexDirt_ExtraTex_AO {")
		ofile.write("\n\twhite_color = AColor(1.000,1.000,1.000,1.000);")
		ofile.write("\n\tsubdivs = 16;")
		ofile.write("\n\tblack_color= AColor(0.000,0.000,0.000,1.000);")
		ofile.write("\n\tradius = %s;"%(sce.vray_texdirt_ao_radius))
		ofile.write("\n\tignore_for_gi = 1;")
		ofile.write("\n}")

		ofile.write("\nRenderChannelExtraTex AO {")
		ofile.write("\n\tname=\"AO\";")
		ofile.write("\n\tconsider_for_aa = %s;"%(p(sce.vray_extratex_consider_for_aa)))
		ofile.write("\n\taffect_matte_objects = %s;"%(p(sce.vray_extratex_affect)))
		ofile.write("\n\ttexmap = TexDirt_ExtraTex_AO;")
		ofile.write("\n\tfiltering= 1;")
		ofile.write("\n}")

	if(passes.pass_environment or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Environment {")
		ofile.write("\n\tname=\"VRay_Environment\";")
		ofile.write("\n\talias= 124;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(passes.pass_indirect or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_GI {")
		ofile.write("\n\tname=\"VRay_GI\";")
		ofile.write("\n\talias= 108;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Raw_GI {")
		ofile.write("\n\tname=\"VRay_Raw_GI\";")
		ofile.write("\n\talias= 110;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_bumb or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Bumb_Normal {")
		ofile.write("\n\tname=\"VRay_Bumb_Normal\";")
		ofile.write("\n\talias= 131;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_samplerate or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Samplerate {")
		ofile.write("\n\tname=\"VRay_Samplerate\";")
		ofile.write("\n\talias= 132;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_multimatte or sce.vray_passes):
		ofile.write("\nRenderChannelMultiMatte {")
		ofile.write("\n\tname=\"MultiMatte\";")
		ofile.write("\n\tred_id = %s;"%(sce.vray_multimatte_red_id))
		ofile.write("\n\tgreen_id = %s;"%(sce.vray_multimatte_green_id))
		ofile.write("\n\tblue_id= %s;"%(sce.vray_multimatte_blue_id))
		ofile.write("\n\tuse_mtl_id= %s;"%(p(sce.vray_multimatte_use_mtl_id)))
		ofile.write("\n}")

	if(sce.vray_pass_caustics or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Caustics {")
		ofile.write("\n\tname=\"VRay_Caustics\";")
		ofile.write("\n\talias= 109;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

	if(sce.vray_pass_wirecolor or sce.vray_passes):
		ofile.write("\nRenderChannelColor VRay_Wire_Color {")
		ofile.write("\n\tname=\"VRay_Wire_Color\";")
		ofile.write("\n\talias= 127;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Real_Color {")
		ofile.write("\n\tname=\"VRay_Real_Color\";")
		ofile.write("\n\talias= 122;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

		ofile.write("\nRenderChannelColor VRay_Alpha {")
		ofile.write("\n\tname=\"VRay_Real_Alpha\";")
		ofile.write("\n\talias= 125;")
		ofile.write("\n\tcolor_mapping= %s;"%(p(sce.vray_color_mapping)))
		ofile.write("\n}")

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

	ofile.write("\n")
	ofile.close()


def get_filenames():
	global filenames

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
		global sce
		global rd
		global wo

		sce= context.scene
		rd=  sce.render
		wo=  sce.world

		get_filenames()

		write_geometry()

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

		get_filenames()

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(filenames['output'],"render.%s" % get_render_file_format(rd.file_format))
		
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
			write_materials()
			write_nodes()
			write_lamps()
			write_camera(sce)
			write_scene()

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

			if sce.vray_export_img_to_blender:
				params.append('-autoclose=')
				params.append('1')

			if sce.vray_export_animation:
				params.append('-frames=')
				params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))

			params.append('-imgFile=')
			params.append(image_file)

		if(sce.vray_debug):
			print("V-Ray/Blender: Command: %s"%(params))

		if sce.vray_autorun:
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
						if not sce.vray_export_animation:
							if sce.vray_export_img_to_blender or sce.name == "preview":
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

		get_filenames()

		wx= rd.resolution_x * rd.resolution_percentage / 100
		wy= rd.resolution_y * rd.resolution_percentage / 100

		vb_path= vb_script_path()

		params= []
		params.append(vb_binary_path())

		image_file= os.path.join(filenames['output'],"render.%s" % get_render_file_format(rd.file_format))
		
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
			write_materials()
			write_nodes()
			write_lamps()
			write_camera(sce)
			write_scene()

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

			if sce.vray_export_img_to_blender:
				params.append('-autoclose=')
				params.append('1')

			if sce.vray_export_animation:
				params.append('-frames=')
				params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))

			params.append('-imgFile=')
			params.append(image_file)

		if(sce.vray_debug):
			print("V-Ray/Blender: Command: %s"%(params))

		if sce.vray_autorun:
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
						if not sce.vray_export_animation:
							if sce.vray_export_img_to_blender or sce.name == "preview":
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

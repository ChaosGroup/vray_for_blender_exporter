'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
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
from vb25.plugins import *

''' vb dev modules '''
from vb25.nodes import *


VERSION= '2.5.10'


'''
  MESHES
'''
def write_geometry(scene):
	VRayScene= scene.vray
	VRayExporter= VRayScene.exporter
	
	try:

		bpy.ops.vray.export_meshes(
			filepath= get_filenames(scene,'geometry')[:-11],
			use_active_layers= VRayExporter.mesh_active_layers,
			use_animation= VRayExporter.animation,
			use_instances= VRayExporter.use_instances,
			debug= VRayExporter.debug,
			check_animated= VRayExporter.check_animated,
		)
	except:
		def write_frame(bus):
			# Filters stores already exported data
			bus['filter']= {}
			bus['filter']['mesh']= []

			for ob in scene.objects:
				if ob.type in ('LAMP','CAMERA','ARMATURE','LATTICE','EMPTY'):
					continue

				# Skip proxy meshes
				if hasattr(ob.data, 'GeomMeshFile') and ob.data.vray.GeomMeshFile.use:
					continue

				if VRayExporter.mesh_active_layers:
					if not object_on_visible_layers(scene,ob):
						continue

				bus['node']= {}

				# Currently processes object
				bus['node']['object']= ob
				bus['node']['mesh']= None

				PLUGINS['GEOMETRY']['GeomStaticMesh'].write(bus)
			
		# Settings bus
		bus= {}

		# Plugins
		bus['plugins']= PLUGINS

		# Scene
		bus['scene']= scene

		# V-Ray uses UV indexes, Blender uses UV names
		# Here we store UV name->index map
		bus['uvs']= get_uv_layers_map(scene)

		# Output files
		bus['files']= {}
		bus['files']['geometry']= []
		for thread in range(scene.render.threads):
			bus['files']['geometry'].append(open(get_filenames(scene,'geometry')[:-11]+"_%.2i.vrscene"%(thread), 'w'))

		for geometry_file in bus['files']['geometry']:
			geometry_file.write("// V-Ray/Blender %s" % VERSION)
			geometry_file.write("\n// Geometry file\n")

		timer= time.clock()
		debug(scene, "Writing meshes...")

		if VRayExporter.animation:
			cur_frame= scene.frame_current
			scene.frame_set(scene.frame_start)
			f= scene.frame_start
			while(f <= scene.frame_end):
				exported_meshes= []
				scene.frame_set(f)
				write_frame(bus)
				f+= scene.frame_step
			scene.frame_set(cur_frame)
		else:
			write_frame(bus)

		for geometry_file in bus['files']['geometry']:
			geometry_file.write("\n// vim: set syntax=on syntax=c:\n\n")
			geometry_file.close()

		debug(scene, "Writing meshes... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))


def write_GeomMayaHair(ofile, ob, ps, name):
	num_hair_vertices= []
	hair_vertices=     []
	widths=            []

	for p,particle in enumerate(ps.particles):
		sys.stdout.write("V-Ray/Blender: Object: %s => Hair: %i\r" % (ob.name, p))
		sys.stdout.flush()
		num_hair_vertices.append(str(len(particle.hair)))
		for segment in particle.hair:
			hair_vertices.append("Vector(%.6f,%.6f,%.6f)" % tuple(segment.co))
			widths.append(str(0.01)) # TODO

	ofile.write("\nGeomMayaHair %s {"%(name))
	ofile.write("\n\tnum_hair_vertices= interpolate((%d,ListInt(%s)));"%(scene.frame_current, ','.join(num_hair_vertices)))
	ofile.write("\n\thair_vertices= interpolate((%d,ListVector(%s)));"%(scene.frame_current,  ','.join(hair_vertices)))
	ofile.write("\n\twidths= interpolate((%d,ListFloat(%s)));"%(scene.frame_current,          ','.join(widths)))
	ofile.write("\n}\n")


'''
  MATERIALS & TEXTURES
'''
def lamp_defaults(bus):
	scene= bus['scene']
	ob=    bus['node']['object']

	la= ob.data


def material_defaults(bus):
	scene= bus['scene']
	ma=    bus['material']

	VRayMaterial=    ma.vray
	BRDFVRayMtl=     VRayMaterial.BRDFVRayMtl
	BRDFSSS2Complex= VRayMaterial.BRDFSSS2Complex

	if VRayMaterial.type == 'EMIT':
		return {
			'diffuse':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),          0, 'NONE'),
			'opacity':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([ma.alpha]*3)),              0, 'NONE'),
		}
	
	elif VRayMaterial.type == 'SSS':
		return {
			'overall_color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),                   0, 'NONE'),
			'sub_surface_color':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.sub_surface_color)),  0, 'NONE'),
			'scatter_radius':      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.scatter_radius)),     0, 'NONE'),
			'diffuse_color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.diffuse_color)),      0, 'NONE'),
			'diffuse_amount':      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFSSS2Complex.diffuse_amount]*3)), 0, 'NONE'),
			'specular_color':      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.specular_color)),     0, 'NONE'),
			'specular_amount':     ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
			'specular_glossiness': ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
		}
		
	# elif VRayMaterial.type == 'VOL':
	# 	return {
	# 		'color_tex':    (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),           0, 'NONE'),
	# 		'emission_tex': (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(EnvironmentFog.emission)),    0, 'NONE'),
	# 		'density_tex':  (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([EnvironmentFog.density]*3)), 0, 'NONE'),
	# 	}

	else:
		return None

def write_lamp_textures(bus):
	ofile= bus['files']['lights']
	scene= bus['scene']
	ob=    bus['node']['object']

	la= ob.data
	
	VRayLamp= la.vray

	defaults= {
		'color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(la.color)),               0, 'NONE'),
		'intensity':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([VRayLamp.intensity]*3)), 0, 'NONE'),
		'shadowColor': (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(VRayLamp.shadowColor)),   0, 'NONE'),
	}

	bus['textures']= {
		'mapto': {},
	}
	
	for slot in la.texture_slots:
		if slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot= slot.texture.vray_slot
			VRayLight= VRaySlot.VRayLight
			
			for key in defaults:
				use_slot= False
				factor=   1.0
				
				if getattr(VRayLight, 'map_'+key):
					use_slot= True
					factor=   getattr(VRayLight, key+'_mult')

				if use_slot:
					if key not in bus['textures']['mapto']: # First texture
						bus['textures']['mapto'][key]= []
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
							bus['textures']['mapto'][key].append(defaults[key])
					params['mapto']=    key
					params['slot']=     slot
					params['texture']=  slot.texture
					params['factor']=   factor
					bus['textures']['mapto'][key].append((write_texture_factor(ofile, scene, params),
														slot.use_stencil,
														VRaySlot.blend_mode))
	if len(bus['textures']['mapto']):
		debug(scene, "Lamp \"%s\" texture stack: %s" % (la.name,bus['textures']['mapto']))
	
	for key in bus['textures']['mapto']:
		if len(bus['textures']['mapto'][key]):
			bus['textures']['mapto'][key]= write_TexOutput(
				ofile,
				stack_write_shaders(ofile, stack_collapse_layers(bus['textures']['mapto'][key])),
				{}
			)

	return bus['textures']


def write_material_textures(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ma=    bus['material']

	BRDFVRayMtl=     ma.vray.BRDFVRayMtl
	BRDFSSS2Complex= ma.vray.BRDFSSS2Complex
	# EnvironmentFog=  ma.vray.EnvironmentFog

	defaults= material_defaults(bus)

	bus['textures']= {
		'mapto': {},
		'values': {
			'normal_slot':       None,
			'displacement_slot': None,
		}
	}

	for i,slot in enumerate(ma.texture_slots):
		if ma.use_textures[i] and slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot= slot.texture.vray_slot
			for key in defaults:
				factor= 1.0
				use_slot= False
				if key == 'diffuse':
					if slot.use_map_color_diffuse:
						use_slot= True
						factor= slot.diffuse_color_factor
				elif key == 'overall_color' and ma.vray.type == 'SSS':
					if slot.use_map_color_diffuse:
						use_slot= True
						factor= slot.diffuse_color_factor
				elif key == 'reflect':
					if slot.use_map_raymir:
						use_slot= True
						factor= slot.raymir_factor
				elif key == 'opacity':
					if slot.use_map_alpha:
						use_slot= True
						factor= slot.alpha_factor
				elif key == 'normal':
					if slot.use_map_normal:
						use_slot= True
						factor= VRaySlot.normal_mult
						bus['textures']['values']['normal_slot']= slot
				else:
					if getattr(VRaySlot, 'map_'+key):
						use_slot= True
						factor= getattr(VRaySlot, key+'_mult')
						if key == 'displacement':
							bus['textures']['values']['displacement_slot']= slot

				if use_slot:
					if key not in bus['textures']['mapto']: # First texture
						bus['textures']['mapto'][key]= []
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
							bus['textures']['mapto'][key].append(defaults[key])
					params= {}
					params['mapto']=    key
					params['slot']=     slot
					params['texture']=  slot.texture
					params['factor']=   factor
					bus['textures']['mapto'][key].append(
						(write_texture_factor(ofile, scene, params), slot.use_stencil, VRaySlot.blend_mode)
					)

	if len(bus['textures']['mapto']):
		print_dict(scene, "Material \"%s\" texture stack" % ma.name, bus['textures']['mapto'])
	
	for key in bus['textures']['mapto']:
		if len(bus['textures']['mapto'][key]):
			bus['textures']['mapto'][key]= write_TexOutput(
				ofile,
				stack_write_shaders(ofile, stack_collapse_layers(bus['textures']['mapto'][key])),
				{} # TODO: TexOutput params
			)

	return bus['textures']


def write_BRDFSSS2Complex(ofile, ma, ma_name, textures):
	SINGLE_SCATTER= {
		'NONE':   0,
		'SIMPLE': 1,
		'SOLID':  2,
		'REFR':   3
	}

	BRDFSSS2Complex= ma.vray.BRDFSSS2Complex

	brdf_name= "BRDFSSS2Complex_%s"%(ma_name)

	ofile.write("\nBRDFSSS2Complex %s {" % brdf_name)

	for key in ('overall_color','diffuse_color','sub_surface_color','scatter_radius','specular_color'):
		ofile.write("\n\t%s= %s;" % (key, a(scene,textures[key]) if key in textures else a(scene,getattr(BRDFSSS2Complex,key))))

	for key in ('specular_amount','specular_glossiness','diffuse_amount'):
		ofile.write("\n\t%s= %s;" % (key, "%s::out_intensity" % textures[key] if key in textures else a(scene,getattr(BRDFSSS2Complex,key))))

	for param in OBJECT_PARAMS['BRDFSSS2Complex']:
		if param == 'single_scatter':
			value= SINGLE_SCATTER[BRDFSSS2Complex.single_scatter]
		else:
			value= getattr(BRDFSSS2Complex,param)
		ofile.write("\n\t%s= %s;"%(param, a(scene,value)))

	ofile.write("\n}\n")

	return brdf_name


# elif VRayMaterial.type == 'VOL':
# 	bus['node']['volume']= {}
# 	for param in OBJECT_PARAMS['EnvironmentFog']:
# 		if param == 'color':
# 			value= ma.diffuse_color
# 		else:
# 			value= getattr(VRayMaterial.EnvironmentFog,param)
# 		object_params['volume'][param]= value
# 	for param in ('color_tex','emission_tex','density_tex'):
# 		if param in textures['mapto']:
# 			object_params['volume'][param]= textures['mapto'][param]
# 	return None


def	write_material(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ob=    bus['node']['object']
	ma=    bus['material']

	ma_name= get_name(ma, prefix="MA")

	VRayMaterial= ma.vray
	
	brdf_name= "BRDFDiffuse_no_material"

	bus['textures']= {}

	textures= write_material_textures(bus)

	if VRayMaterial.type == 'EMIT' and VRayMaterial.emitter_type == 'MESH':
		bus['node']['meshlight']['on']= True
		bus['node']['meshlight']['material']= ma
		bus['node']['meshlight']['texture']= textures['mapto'].get('diffuse')
		return None

	if textures['values']['displacement_slot']:
		object_params['displace']['slot']=    textures['values']['displacement_slot']
		object_params['displace']['texture']= textures['mapto']['displacement']

	if ma in bus['filter']['material']:
		return ma_name
	else:
		bus['filter']['material'].append(ma)

	brdf_name= PLUGINS['BRDF'][VRayMaterial.type].write(bus)

	if bus['textures']['values']['normal_slot']:
		brdf_name= PLUGINS['BRDF']['BRDFBump'].write(bus)
		# {'file':      ofile,
		#  'scene':     scene,
		#  'base_brdf': brdf_name,
		#  'textures':  textures}

	complex_material= []
	for component in (VRayMaterial.Mtl2Sided.use, VRayMaterial.MtlWrapper.use,
					  VRayMaterial.MtlOverride.use, VRayMaterial.MtlRenderStats.use,
					  VRayMaterial.material_id_number):
		if component:
			complex_material.append("MtlComp_%.2d_%s"%(len(complex_material), ma_name))
	complex_material.append(ma_name)
	complex_material.reverse()

	ofile.write("\nMtlSingleBRDF %s {"%(complex_material[-1]))
	ofile.write("\n\tbrdf= %s;" % a(scene,brdf_name))
	ofile.write("\n}\n")

	if VRayMaterial.Mtl2Sided.use:
		base_material= complex_material.pop()
		ofile.write("\nMtl2Sided %s {"%(complex_material[-1]))
		ofile.write("\n\tfront= %s;"%(base_material))
		back= base_material
		if VRayMaterial.Mtl2Sided.back != "":
			if VRayMaterial.Mtl2Sided.back in bpy.data.materials:
				back= get_name(bpy.data.materials[VRayMaterial.Mtl2Sided.back],"Material")
		ofile.write("\n\tback= %s;"%(back))

		if VRayMaterial.Mtl2Sided.control == 'SLIDER':
			ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))
		elif VRayMaterial.Mtl2Sided.control == 'COLOR':
			ofile.write("\n\ttranslucency= %s;" % a(scene, VRayMaterial.Mtl2Sided.translucency_color))
		else:
			if VRayMaterial.Mtl2Sided.translucency_tex != "":
				if VRayMaterial.Mtl2Sided.translucency_tex in bpy.data.materials:
					ofile.write("\n\ttranslucency_tex= %s;"%(get_name(bpy.data.textures[VRayMaterial.Mtl2Sided.translucency_tex],"Texture")))
					ofile.write("\n\ttranslucency_tex_mult= %s;" % a(scene,VRayMaterial.Mtl2Sided.translucency_tex_mult))
			else:
				ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))

		ofile.write("\n\tforce_1sided= %d;" % VRayMaterial.Mtl2Sided.force_1sided)
		ofile.write("\n}\n")

	if VRayMaterial.MtlWrapper.use:
		base_material= complex_material.pop()
		ofile.write("\nMtlWrapper %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_material= %s;"%(base_material))
		for param in OBJECT_PARAMS['MtlWrapper']:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayMaterial.MtlWrapper,param))))
		ofile.write("\n}\n")

	if VRayMaterial.MtlOverride.use:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlOverride %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))

		for param in ('gi_mtl','reflect_mtl','refract_mtl','shadow_mtl'):
			override_material= getattr(VRayMaterial.MtlOverride, param)
			if override_material:
				if override_material in bpy.data.materials:
					ofile.write("\n\t%s= %s;"%(param, get_name(bpy.data.materials[override_material],"Material")))

		environment_override= VRayMaterial.MtlOverride.environment_override
		if environment_override:
			if environment_override in bpy.data.textures:
				ofile.write("\n\tenvironment_override= %s;" % get_name(bpy.data.textures[environment_override],"Texture"))

		ofile.write("\n\tenvironment_priority= %i;"%(VRayMaterial.MtlOverride.environment_priority))
		ofile.write("\n}\n")

	if VRayMaterial.MtlRenderStats.use:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlRenderStats %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))
		for param in OBJECT_PARAMS['MtlRenderStats']:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayMaterial.MtlRenderStats,param))))
		ofile.write("\n}\n")

	if VRayMaterial.material_id_number:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlMaterialID %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;" % base_mtl)
		ofile.write("\n\tmaterial_id_number= %i;" % VRayMaterial.material_id_number)
		#ofile.write("\n\tmaterial_id_color= %s;" % p(VRayMaterial.material_id_color))
		ofile.write("\n}\n")

	return ma_name


def write_materials(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ob=    bus['node']['object']

	mtls_list= []
	ids_list=  []

	mtl_name= get_name(ob, prefix="MA")

	ma_id= 0
	if len(ob.material_slots):
		for i,slot in enumerate(ob.material_slots):
			ma= slot.material
			if ma:
				if scene.vray.exporter.use_material_nodes and ma.use_nodes and hasattr(ma.node_tree, 'links'):
					debug(scene,"Node materials temporarily disabled...")
					#mtls_list.append(write_node_material(params))
				bus['material']= ma
				ma_name= write_material(bus)
				if ma_name:
					mtls_list.append(ma_name)
					ma_id+= 1
					ids_list.append(str(ma_id))

	if len(mtls_list) == 0:
		mtls_list.append("Material_no_material")
		ids_list.append("1")
	elif len(mtls_list) == 1:
		bus['node']['material']= mtls_list[0]
		return
					
	ofile.write("\nMtlMulti %s {" % mtl_name)
	ofile.write("\n\tmtls_list= List(%s);"%(','.join(mtls_list)))
	ofile.write("\n\tids_list= ListInt(%s);"%(','.join(ids_list)))
	ofile.write("\n}\n")

	bus['node']['material']= mtl_name


def write_lamp(bus):
	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']
	
	lamp= ob.data
	vl= lamp.vray

	lamp_type= None
	lamp_name= get_name(ob, prefix="LA")
	lamp_matrix= ob.matrix_world

	textures= write_lamp_textures(bus)['mapto']

	if bus['node']['dupli'].get('matrix'):
		lamp_matrix= bus['node']['dupli']['matrix']

	if bus['node']['particle'].get('matrix'):
		lamp_matrix= bus['node']['particle']['matrix']

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
			lamp_type= 'LightDirectMax'
		else:
			lamp_type= 'SunLight'
	elif lamp.type == 'AREA':
		lamp_type= 'LightRectangle'
	elif lamp.type == 'HEMI':
		lamp_type= 'LightDome'
	else:
		return

	ofile.write("\n%s %s {"%(lamp_type,lamp_name))

	if 'color' in textures:
		ofile.write("\n\tcolor_tex= %s;" % textures['color'])

		if lamp.type == 'SUN' and vl.direct_type == 'DIRECT':
			ofile.write("\n\tprojector_map= %s;" % textures['color'])

		if lamp.type == 'AREA':
			ofile.write("\n\trect_tex= %s;" % textures['color'])
		elif lamp.type == 'HEMI':
			ofile.write("\n\tdome_tex= %s;" % textures['color'])

		if lamp.type in ('AREA','HEMI'):
			ofile.write("\n\tuse_rect_tex= 1;")
			ofile.write("\n\ttex_adaptive= %.2f;" % (1.0))
			ofile.write("\n\ttex_resolution= %i;" % (512))

	if 'intensity' in textures:
		ofile.write("\n\tintensity_tex= %s;" % a(scene, "%s::out_intensity" % textures['intensity']))

	if 'shadowColor' in textures:
		if lamp.type == 'SUN' and vl.direct_type == 'DIRECT':
			ofile.write("\n\tshadowColor_tex= %s;" % textures['shadowColor'])
		else:
			ofile.write("\n\tshadow_color_tex= %s;" % textures['shadowColor'])
		
	if lamp_type == 'SunLight':
		ofile.write("\n\tsky_model= %i;"%(SKY_MODEL[vl.sky_model]))
	else:
		ofile.write("\n\tcolor= %s;"%(a(scene,"Color(%.6f, %.6f, %.6f)"%(tuple(lamp.color)))))
		if lamp_type != 'LightIES':
			ofile.write("\n\tunits= %i;"%(UNITS[vl.units]))

	if lamp_type == 'LightSpot':
		ofile.write("\n\tconeAngle= %s;" % a(scene,lamp.spot_size))
		ofile.write("\n\tpenumbraAngle= %s;" % a(scene, - lamp.spot_size * lamp.spot_blend))

	if lamp_type == 'LightRectangle':
		if lamp.shape == 'RECTANGLE':
			ofile.write("\n\tu_size= %s;"%(a(scene,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(scene,lamp.size_y/2)))
		else:
			ofile.write("\n\tu_size= %s;"%(a(scene,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(scene,lamp.size/2)))
		ofile.write("\n\tlightPortal= %i;"%(LIGHT_PORTAL[vl.lightPortal]))

	for param in OBJECT_PARAMS[lamp_type]:
		if param == 'shadow_subdivs':
			ofile.write("\n\tshadow_subdivs= %s;"%(a(scene,vl.subdivs)))
		elif param == 'shadowRadius' and lamp_type == 'LightDirectMax':
			ofile.write("\n\t%s= %s;" % (param, a(scene,vl.shadowRadius)))
			ofile.write("\n\tshadowRadius1= %s;" % a(scene,vl.shadowRadius))
			ofile.write("\n\tshadowRadius2= %s;" % a(scene,vl.shadowRadius))
		elif param == 'intensity' and lamp_type == 'LightIES':
			ofile.write("\n\tpower= %s;"%(a(scene,vl.intensity)))
		elif param == 'shadow_color':
			ofile.write("\n\tshadow_color= %s;"%(a(scene,vl.shadowColor)))
		elif param == 'ies_file':
			ofile.write("\n\t%s= \"%s\";"%(param,get_full_filepath(scene,lamp,vl.ies_file)))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(vl,param))))

	ofile.write("\n\ttransform= %s;"%(a(scene,transform(lamp_matrix))))
	ofile.write("\n}\n")


def get_visibility_lists(camera):
	VRayCamera= camera.data.vray

	visibility= {
		'all':     [],
		'camera':  [],
		'gi':      [],
		'reflect': [],
		'refract': [],
		'shadows': [],
	}

	if VRayCamera.hide_from_view:
		for hide_type in visibility:
			if getattr(VRayCamera, 'hf_%s' % hide_type):
				if getattr(VRayCamera, 'hf_%s_auto' % hide_type):
					visibility[hide_type]= generate_object_list(group_names_string= 'hf_%s' % camera.name)
				else:
					visibility[hide_type]= generate_object_list(getattr(VRayCamera, 'hf_%s_objects' % hide_type), getattr(VRayCamera, 'hf_%s_groups' % hide_type))

	return visibility


def write_settings(bus):
	ofile= bus['files']['scene']
	scene= bus['scene']
	
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR

	ofile.write("// Settings\n\n")

	for f in bus['files']:
		if VRayDR.on:
			if VRayDR.type == 'UU':
				ofile.write("#include \"%s\"\n" % get_filenames(scene,f))
			elif VRayDR.type == 'WU':
				ofile.write("#include \"%s\"\n" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),os.path.split(bpy.data.filepath)[1][:-6],os.path.basename(get_filenames(scene,f)))))
			else:
				ofile.write("#include \"%s\"\n" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),os.path.split(bpy.data.filepath)[1][:-6],os.path.basename(get_filenames(scene,f)))))
		else:
			ofile.write("#include \"%s\"\n"%(os.path.basename(get_filenames(scene,f))))

	for t in range(scene.render.threads):
		ofile.write("#include \"%s_%.2i.vrscene\"\n" % (os.path.basename(get_filenames(scene,'geometry'))[:-11], t))

	wx= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	wy= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

	ofile.write("\nSettingsOutput {")
	ofile.write("\n\timg_separateAlpha= %d;"%(0))
	ofile.write("\n\timg_width= %s;" % wx)
	if VRayScene.VRayBake.use:
		ofile.write("\n\timg_height= %s;" % wx)
	else:
		ofile.write("\n\timg_height= %s;" % wy)
	if VRayExporter.animation:
		ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(scene.camera.name),get_render_file_format(VRayExporter,scene.render.file_format)))
		ofile.write("\n\timg_dir= \"%s\";"%(get_filenames(scene,'output')))
		ofile.write("\n\timg_file_needFrameNumber= 1;")
		ofile.write("\n\tanim_start= %d;"%(scene.frame_start))
		ofile.write("\n\tanim_end= %d;"%(scene.frame_end))
		ofile.write("\n\tframe_start= %d;"%(scene.frame_start))
		ofile.write("\n\tframes_per_second= %d;"%(1.0) )
		ofile.write("\n\tframes= %d-%d;"%(scene.frame_start, scene.frame_end))
	ofile.write("\n\tframe_stamp_enabled= %d;"%(0))
	ofile.write("\n\tframe_stamp_text= \"%s\";"%("vb25 (git) | V-Ray Standalone %%vraycore | %%rendertime"))
	ofile.write("\n}\n")

	ofile.write("\nSettingsEXR SettingsEXR {")
	ofile.write("\n\tcompression= 0;") # 0 - default, 1 - no compression, 2 - RLE, 3 - ZIPS, 4 - ZIP, 5 - PIZ, 6 - pxr24
	ofile.write("\n\tbits_per_channel= %d;" % (16 if scene.render.use_exr_half else 32))
	ofile.write("\n}\n")

	ofile.write("\nSettingsJPEG SettingsJPEG {")
	ofile.write("\n\tquality= %d;" % scene.render.file_quality)
	ofile.write("\n}\n")

	ofile.write("\nSettingsPNG SettingsPNG {")
	ofile.write("\n\tcompression= %d;" % (int(scene.render.file_quality / 10) if scene.render.file_quality < 90 else 90))
	ofile.write("\n\tbits_per_channel= 16;")
	ofile.write("\n}\n")

	for key in PLUGINS['SETTINGS']:
		if key not in ('BakeView', 'RenderView'): # TODO: may be separate in own type
			plugin= PLUGINS['SETTINGS'][key]
			if hasattr(plugin, 'write'):
				plugin.write(bus)

	if VRayScene.render_channels_use:
		for render_channel in VRayScene.render_channels:
			if render_channel.use:
				plugin= PLUGINS['RENDERCHANNEL'].get(render_channel.type)
				if plugin:
					plugin.write(ofile, getattr(render_channel,plugin.PLUG), scene, render_channel.name)

	ofile.write("\n")


def write_node(bus):
	scene=      bus['scene']
	ofile=      bus['files']['nodes']
	ob=         bus['node']['object']
	visibility= bus['visibility']

	VRayScene= scene.vray
	SettingsOptions= VRayScene.SettingsOptions

	lights= []
	for lamp in [ob for ob in scene.objects if ob.type == 'LAMP']:
		VRayLamp= lamp.data.vray
		lamp_name= get_name(lamp, prefix="LA")
		if not object_on_visible_layers(scene,lamp) or lamp.hide_render:
			if not scene.vray.SettingsOptions.light_doHiddenLights:
				continue
		if VRayLamp.use_include_exclude:
			object_list= generate_object_list(VRayLamp.include_objects,VRayLamp.include_groups)
			if VRayLamp.include_exclude == 'INCLUDE':
				if ob in object_list:
					lights.append(lamp_name)
			else:
				if ob not in object_list:
					lights.append(lamp_name)
		else:
			lights.append(lamp_name)

	node_name= bus['node']['name']
	base_mtl= bus['node']['material']

	if SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
		base_mtl= get_name(bpy.data.materials[SettingsOptions.mtl_override], prefix="MA")

	material= "RS%s" % node_name

	ofile.write("\nMtlRenderStats %s {" % material)
	ofile.write("\n\tbase_mtl= %s;" % base_mtl)
	ofile.write("\n\tvisibility= %s;" % (0 if ob in visibility['all'] or bus['node']['visible'] == False else 1))
	ofile.write("\n\tcamera_visibility= %s;" % (0 if ob in visibility['camera'] else 1))
	ofile.write("\n\tgi_visibility= %s;" % (0 if ob in visibility['gi'] else 1))
	ofile.write("\n\treflections_visibility= %s;" % (0 if ob in visibility['reflect'] else 1))
	ofile.write("\n\trefractions_visibility= %s;" % (0 if ob in visibility['refract'] else 1))
	ofile.write("\n\tshadows_visibility= %s;" % (0 if ob in visibility['shadows'] else 1))
	ofile.write("\n}\n")

	ofile.write("\nNode %s {" % node_name)
	ofile.write("\n\tobjectID= %d;" % bus['node'].get('objectID',ob.pass_index))
	ofile.write("\n\tgeometry= %s;" % bus['node']['geometry'])
	ofile.write("\n\tmaterial= %s;" % material)
	ofile.write("\n\ttransform= %s;" % a(scene, transform(bus['node']['matrix'])))
	ofile.write("\n\tlights= List(%s);" % (','.join(lights)))
	ofile.write("\n}\n")


def write_object(bus):
	# print_dict(bus['scene'], 'BUS', bus)

	files= bus['files']
	ofile= bus['files']['nodes']
	scene= bus['scene']
	ob=    bus['node']['object']

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayObject=   ob.vray
	VRayData=     ob.data.vray

	bus['node']['name']=      get_name(ob, prefix="OB")
	bus['node']['geometry']=  get_name(ob.data, prefix="ME")
	bus['node']['matrix']=    ob.matrix_world

	# Don't override proxy material, if proxy has multi-material
	# if bus['override_material'] is not None and not (hasattr(VRayData,'GeomMeshFile') and VRayData.GeomMeshFile.use):
	# 	bus['node']['material']= bus['override_material']
	# else:
	# 	bus['node']['material']= write_materials(bus)

	# Write object materials
	write_materials(bus)

	PLUGINS['GEOMETRY']['GeomMeshFile'].write(bus)
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].write(bus)

	if bus['node']['dupli']:
		# if bus['node']['dupli']['type'] == 'GROUP':
		# 	bus['node']['matrix']= bus['node']['dupli']['matrix'] * bus['node']['matrix']
		# else:
		# 	bus['node']['matrix']= bus['node']['dupli']['matrix']
		bus['node']['matrix']= bus['node']['dupli']['matrix']

	if bus['node']['meshlight']:
		PLUGINS['GEOMETRY']['LightMesh'].write(bus)
		return

	# if object_params['volume'] is not None:
	# 	if ma_name not in types['volume'].keys():
	# 		types['volume'][ma_name]= {}
	# 		types['volume'][ma_name]['params']= object_params['volume']
	# 		types['volume'][ma_name]['gizmos']= []
	# 	if ob not in types['volume'][ma_name]:
	# 		types['volume'][ma_name]['gizmos'].append(write_EnvFogMeshGizmo(files['nodes'], node_name, node_geometry, node_matrix))
	# 	return

	complex_material= []
	complex_material.append(bus['node']['material'])
	for component in (VRayObject.MtlWrapper.use,VRayObject.MtlOverride.use,VRayObject.MtlRenderStats.use):
		if component:
			complex_material.append("ObjComp_%.2d_%s"%(len(complex_material), bus['node']['material']))
	complex_material.reverse()

	if VRayObject.MtlWrapper.use:
		base_material= complex_material.pop()
		ma_name= complex_material[-1]
		ofile.write("\nMtlWrapper %s {"%(ma_name))
		ofile.write("\n\tbase_material= %s;"%(base_material))
		for param in OBJECT_PARAMS['MtlWrapper']:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayObject.MtlWrapper,param))))
		ofile.write("\n}\n")

	if VRayObject.MtlOverride.use:
		base_mtl= complex_material.pop()
		ma_name= complex_material[-1]
		ofile.write("\nMtlOverride %s {"%(ma_name))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))

		for param in ('gi_mtl','reflect_mtl','refract_mtl','shadow_mtl'):
			override_material= getattr(VRayObject.MtlOverride, param)
			if override_material:
				if override_material in bpy.data.materials:
					ofile.write("\n\t%s= %s;"%(param, get_name(bpy.data.materials[override_material],"Material")))

		environment_override= VRayObject.MtlOverride.environment_override
		if environment_override:
			if environment_override in bpy.data.materials:
				ofile.write("\n\tenvironment_override= %s;" % get_name(bpy.data.textures[environment_override],"Texture"))

		ofile.write("\n\tenvironment_priority= %i;"%(VRayObject.MtlOverride.environment_priority))
		ofile.write("\n}\n")

	if VRayObject.MtlRenderStats.use:
		base_mtl= complex_material.pop()
		ma_name= complex_material[-1]
		ofile.write("\nMtlRenderStats %s {"%(ma_name))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))
		for param in OBJECT_PARAMS['MtlRenderStats']:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayObject.MtlRenderStats,param))))
		ofile.write("\n}\n")

	write_node(bus)


def _write_object_particles(bus):
	ob= bus['node']['object']

	if len(ob.particle_systems):
		for ps in ob.particle_systems:
			if ps.settings.use_render_emitter:
				write_node(bus)
				break

		for ps in ob.particle_systems:
			ps_material= "Material_no_material"
			ps_material_idx= ps.settings.material
			if len(ob.material_slots) >= ps_material_idx:
				ps_material= get_name(ob.material_slots[ps_material_idx - 1].material, "Material")

			if ps.settings.type == 'HAIR' and ps.settings.render_type == 'PATH':
				if VRayExporter.use_hair:
					hair_geom_name= "HAIR_%s" % ps.name
					hair_node_name= "%s_%s" % (ob.name,hair_geom_name)

					write_GeomMayaHair(bus)
			else:
				particle_objects= []
				if ps.settings.render_type == 'OBJECT':
					particle_objects.append(ps.settings.dupli_object)
				elif ps.settings.render_type == 'GROUP':
					particle_objects= ps.settings.dupli_group.objects
				else:
					continue

				for p,particle in enumerate(ps.particles):
					if PLATFORM == "linux2":
						sys.stdout.write("V-Ray/Blender: Object: \033[0;33m%s\033[0m => Particle: \033[0;32m%i\033[0m\r" % (ob.name, p))
					else:
						sys.stdout.write("V-Ray/Blender: Object: %s => Particle: %i\r" % (ob.name, p))
					sys.stdout.flush()

					location= particle.location
					size= particle.size
					if ps.settings.type == 'HAIR':
						location= particle.is_hair[0].co
						size*= 3

					part_transform= mathutils.Matrix.Scale(size, 3) * particle.rotation.to_matrix()
					part_transform.resize4x4()
					part_transform[3][0]= location[0]
					part_transform[3][1]= location[1]
					part_transform[3][2]= location[2]

					for p_ob in particle_objects:
						part_name= "EMITTER_%s_%s" % (clean_string(ps.name), p)
						if bus['node']['particle'].get('name'):
							part_name= "%s%s%s" %(bus['node']['particle']['name'],
												  clean_string(ps.name),
												  p)
												 
						if ps.settings.use_whole_group or ps.settings.use_global_dupli:
							part_transform= part_transform * p_ob.matrix_world

						part_visibility= True
						if ps.settings.type == 'EMITTER':
							if not particle.alive_state == 'ALIVE':
								part_visibility= False
							if particle.alive_state == 'DEAD' and ps.settings.use_dead:
								part_visibility= True
							if particle.alive_state == 'UNBORN' and ps.settings.show_unborn:
								part_visibility= True

						bus['node']['object']= p_ob
						bus['node']['base']= ob
						bus['node']['visible']= part_visibility
						bus['node']['particle']['name']= part_name
						bus['node']['particle']['material']= ps_material
						bus['node']['particle']['matrix']= part_transform

						_write_object(bus)

						bus['node']['object']= ob
						bus['node']['base']= ob
						bus['node']['visible']= True
						bus['node']['particle']= {}


def _write_object_dupli(bus):
	ob= bus['node']['object']

	if ob.dupli_type in ('VERTS','FACES','GROUP'):
		ob.create_dupli_list(bus['scene'])

		for dup_id,dup_ob in enumerate(ob.dupli_list):
			bus['node']['object']= dup_ob.object
			bus['node']['base']= ob
			bus['node']['dupli']['name']= "OB%sDO%s" % (ob.name,dup_id)
			bus['node']['dupli']['matrix']= dup_ob.matrix
			bus['node']['dupli']['type']= ob.dupli_type

			_write_object(bus)

			bus['node']['object']= ob
			bus['node']['base']= ob
			bus['node']['dupli']= {}

		ob.free_dupli_list()


def _write_object(bus):
	ob= bus['node']['object']

	if ob.type in ('CAMERA','ARMATURE','LATTICE'):
		return
	if ob.type == 'LAMP':
		write_lamp(bus)
	elif ob.type == 'EMPTY':
		_write_object_dupli(bus)
	else:
		write_object(bus)
		_write_object_particles(bus)
		_write_object_dupli(bus)


def write_scene(scene):
	VRayScene=       scene.vray
	VRayExporter=    VRayScene.exporter
	SettingsOptions= VRayScene.SettingsOptions

	# Settings bus
	bus= {}

	# Plugins
	bus['plugins']= PLUGINS

	# Scene
	bus['scene']= scene
	
	# V-Ray uses UV indexes, Blender uses UV names
	# Here we store UV name->index map
	bus['uvs']= get_uv_layers_map(scene)

	# Output files
	bus['files']= {}
	bus['files']['lights']=      open(get_filenames(scene,'lights'),      'w')
	bus['files']['materials']=   open(get_filenames(scene,'materials'),   'w')
	bus['files']['nodes']=       open(get_filenames(scene,'nodes'),       'w')
	bus['files']['camera']=      open(get_filenames(scene,'camera'),      'w')
	bus['files']['scene']=       open(get_filenames(scene,'scene'),       'w')
	bus['files']['environment']= open(get_filenames(scene,'environment'), 'w')

	# Some failsafe defaults
	bus['defaults']= {}
	bus['defaults']['material']= "Material_no_material"
	bus['defaults']['texture']= "Texture_no_texture"

	for key in bus['files']:
		bus['files'][key].write("// V-Ray/Blender %s" % VERSION)

	bus['files']['nodes'].write("\n// Nodes\n")
	bus['files']['lights'].write("\n// Lights\n")
	bus['files']['camera'].write("\n// Camera\n")
	bus['files']['environment'].write("\n// Environment\n")
	bus['files']['materials'].write("\n// Materials\n")

	bus['files']['materials'].write("\n// Default materials")
	bus['files']['materials'].write("\nUVWGenChannel UVWGenChannel_default {")
	bus['files']['materials'].write("\n\tuvw_channel= 1;")
	bus['files']['materials'].write("\n\tuvw_transform= Transform(")
	bus['files']['materials'].write("\n\t\tMatrix(")
	bus['files']['materials'].write("\n\t\t\tVector(1.0,0.0,0.0),")
	bus['files']['materials'].write("\n\t\t\tVector(0.0,1.0,0.0),")
	bus['files']['materials'].write("\n\t\t\tVector(0.0,0.0,1.0)")
	bus['files']['materials'].write("\n\t\t),")
	bus['files']['materials'].write("\n\t\tVector(0.0,0.0,0.0)")
	bus['files']['materials'].write("\n\t);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nTexChecker %s {" % bus['defaults']['texture'])
	bus['files']['materials'].write("\n\tuvwgen= UVWGenChannel_default;")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nBRDFDiffuse BRDFDiffuse_no_material {")
	bus['files']['materials'].write("\n\tcolor=Color(0.5, 0.5, 0.5);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nMtlSingleBRDF %s {" % bus['defaults']['material'])
	bus['files']['materials'].write("\n\tbrdf= BRDFDiffuse_no_material;")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nTexAColor TexAColor_default_blend {")
	bus['files']['materials'].write("\n\tuvwgen= UVWGenChannel_default;")
	bus['files']['materials'].write("\n\ttexture= AColor(1.0,1.0,1.0,1.0);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\n// Scene materials\n")

	def write_frame(bus):
		timer= time.clock()
		scene= bus['scene']

		debug(scene, "Writing frame %i..." % scene.frame_current)

		VRayScene= scene.vray
		
		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		# Filters stores already exported data
		bus['filter']= {}
		bus['filter']['proxy']=    []
		bus['filter']['bitmap']=   []
		bus['filter']['texture']=  []
		bus['filter']['material']= []

		# Special data types
		# For example, export VolumeFog or VRayToon from material settings
		# Stores ({'plugin': plugin.ID, 'objects': ({'object': ob, 'rna_pointer': settings_data}))
		bus['special_types']= []

		# Fake frame for "Camera loop"
		if VRayExporter.camera_loop:
			for key in bus['files']:
				if key in ('nodes','camera'):
					bus['files'][key].write("\n#time %.1f // %s\n" % (bus['camera_index'] + 1, bus['camera'].name))
		else:
			# Camera
			# Here for "Camera bind" support
			bus['camera']= scene.camera

		# Visibility list for "Hide from view" and "Camera loop" features
		bus['visibility']= get_visibility_lists(bus['camera'])

		# Hide from view debug data
		if VRayExporter.debug:
			print_dict(scene, "Hide from view", bus['visibility'])

		for ob in scene.objects:
			if ob.type in ('CAMERA','ARMATURE','LATTICE'):
				continue

			if VRayExporter.active_layers:
				if not object_on_visible_layers(scene,ob):
					if ob.type == 'LAMP':
						if not SettingsOptions.light_doHiddenLights:
							continue
					if not SettingsOptions.geom_doHidden:
						continue

			if ob.hide_render:
				if ob.type == 'LAMP':
					if not SettingsOptions.light_doHiddenLights:
						continue
				if not SettingsOptions.geom_doHidden:
					continue

			if PLATFORM == "linux2":
				debug(scene, "{0}: \033[0;32m{1:<32}\033[0m".format(ob.type, ob.name), True if VRayExporter.debug else False)
			else:
				debug(scene, "{0}: {1:<32}".format(ob.type, ob.name), True if VRayExporter.debug else False)

			bus['node']= {}

			# Currently processes object
			bus['node']['object']= ob

			# Object visibility
			bus['node']['visible']= ob

			# We will know if object has displace
			# only after material export
			bus['node']['displace']= {}

			# We will know if object is mesh light
			# only after material export
			bus['node']['meshlight']= {}

			# If object has particles or dupli
			bus['node']['base']= ob
			bus['node']['dupli']= {}
			bus['node']['particle']= {}

			_write_object(bus)

		PLUGINS['SETTINGS']['BakeView'].write(bus)
		PLUGINS['SETTINGS']['RenderView'].write(bus)
		PLUGINS['CAMERA']['SettingsCamera'].write(bus)
		PLUGINS['CAMERA']['CameraPhysical'].write(bus)

		debug(scene, "Writing frame {0}... done {1:<64}".format(scene.frame_current, "[%.2f]"%(time.clock() - timer)))

	timer= time.clock()

	debug(scene, "Writing scene...")

	if VRayExporter.animation:
		selected_frame= scene.frame_current
		f= scene.frame_start
		while(f <= scene.frame_end):
			scene.frame_set(f)
			write_frame(bus)
			f+= scene.frame_step
		scene.frame_set(selected_frame)
	else:
		if VRayExporter.camera_loop:
			cameras= [ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]
			if cameras:
				for i,camera in enumerate(cameras):
					bus['camera']= camera
					bus['camera_index']= i
					write_frame(bus)
		else:
			write_frame(bus)
		
	write_settings(bus)

	for key in bus['files']:
		bus['files'][key].write("\n// vim: set syntax=on syntax=c:\n\n")
		bus['files'][key].close()

	debug(scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))


def run(engine, scene):
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR

	vray_exporter=   get_vray_exporter_path()
	vray_standalone= get_vray_standalone_path(scene)

	resolution_x= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	resolution_y= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

	params= []
	params.append(vray_standalone)

	params.append('-sceneFile=')
	params.append(get_filenames(scene,'scene'))

	if scene.render.use_border:
		x0= resolution_x * scene.render.border_min_x
		y0= resolution_y * (1.0 - scene.render.border_max_y)
		x1= resolution_x * scene.render.border_max_x
		y1= resolution_y * (1.0 - scene.render.border_min_y)

		if scene.render.use_crop_to_border:
			params.append('-crop=')
		else:
			params.append('-region=')
		params.append("%i;%i;%i;%i"%(x0,y0,x1,y1))

	params.append('-frames=')
	if VRayExporter.animation:
		params.append("%d-%d,%d"%(scene.frame_start, scene.frame_end,int(scene.frame_step)))
	elif VRayExporter.camera_loop:
		cameras= [ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]
		if cameras:
			params.append("1-%d,1" % len(cameras))
	else:
		params.append("%d" % scene.frame_current)

	if VRayDR.on:
		if len(VRayDR.nodes):
			params.append('-distributed=')
			params.append('1')
			params.append('-portNumber=')
			params.append(str(VRayDR.port))
			params.append('-renderhost=')
			params.append("\"%s\"" % ';'.join([n.address for n in VRayDR.nodes]))

	if VRayExporter.auto_save_render or VRayExporter.image_to_blender:
		image_file= os.path.join(get_filenames(scene,'output'),
								 "render_%s.%s" % (clean_string(scene.camera.name),
												   get_render_file_format(VRayExporter,scene.render.file_format)))
		params.append('-imgFile=')
		params.append(image_file)

	if VRayExporter.display:
		params.append('-display=')
		params.append('1')

	if VRayExporter.image_to_blender:
		params.append('-autoclose=')
		params.append('1')

	if VRayExporter.autorun:
		if VRayExporter.detach:
			command= "(%s)&" % (' '.join(params))
			if PLATFORM == "linux2":
				if VRayExporter.log_window:
					command= "(xterm -T VRAYSTANDALONE -geometry 90x10 -e \"%s\")&" % (' '.join(params))
			if PLATFORM == "win32":
				command= "start \"VRAYSTANDALONE\" /B /BELOWNORMAL \"%s\" %s" % (params[0], ' '.join(params[1:]))
			os.system(command)

		else:
			process= subprocess.Popen(params)

			if VRayExporter.image_to_blender and VRayExporter.use_render_operator:
				load_file= os.path.join(get_filenames(scene,'output'),
										"render_%s.%.4i.%s" % (clean_string(scene.camera.name),
															   scene.frame_current,
															   get_render_file_format(VRayExporter,scene.render.file_format)))
				while True:
					if engine.test_break():
						try:
							process.kill()
						except:
							pass
						break

					if process.poll() is not None:
						try:
							if not VRayExporter.animation:
								result= engine.begin_result(0, 0, resolution_x, resolution_y)
								layer= result.layers[0]
								layer.load_from_file(load_file)
								engine.end_result(result)
						except:
							pass
						break

					time.sleep(0.1)

	else:
		debug(scene, "Enable \"Autorun\" option to start V-Ray automatically after export.")
		debug(scene, "Command: %s" % ' '.join(params))
	

def render(engine, scene):
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	
	if VRayExporter.auto_meshes:
		write_geometry(scene)

	write_scene(scene)
	run(engine, scene)

'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Saturday, 19 March 2011 [16:03]"

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
from vb25.utils   import *
from vb25.plugins import *
from vb25.texture import *

<<<<<<< HEAD

VERSION= '2.5.10'
=======
''' vb dev modules '''
from vb25.nodes   import *


VERSION= '2.5'


LIGHT_PARAMS= { # TEMP! REMOVE!
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

	'LightDirectMax': (
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
		'fallsize',
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
}


#### Data bus
# bus= {}

### Currently processed object
# bus['node']= {}
# bus['node']['object']= *ob
# bus['node']['displace']['data_pointer']= *tex
# bus['node']['displace']['texture']= vr_tex_name

### Currently processed material
# bus['material']= {}

## Material
# bus['material']['material']= *material

## If some texture need object mapping then material become object dependent
# bus['material']['orco_suffix']= ""

## Normal mapping settings pointer
# bus['material']['normal_slot']= *slot

## BRDFBump nomal mapping uvwgen
# bus['material']['normal_uvwgen']= string

### Texture stack
# bus['textures']=      {}
# bus['lamp_textures']= {}
# bus['env_textures']=  {}

### Currently processed texture
# bus['mtex']= {}
# bus['mtex']['slot']
# bus['mtex']['texture']
# bus['mtex']['factor']
# bus['mtex']['blend_mode']

### Exported data cache
# bus['cache']= {}

## Animated proxy data is proxy dependent so caching only type 'STILL'
# bus['cache']['proxy']=  []

## Animated bitmap data is bitmap dependent so caching only type 'FILE'
# bus['cache']['bitmap']= []

## 'ORCO' textures are object position dependent so caching only type 'UV'
# bus['cache']['texture_uv']= []
>>>>>>> devel


mesh_lights= []

'''
  MESHES
'''
def write_geometry_python(bus):
	scene= bus['scene']

	VRayScene= scene.vray
	VRayExporter= VRayScene.exporter

	def write_frame(bus):
		# Filters stores already exported data
		bus['filter']= {}
		bus['filter']['mesh']= []

<<<<<<< HEAD
	exported_meshes= []

	def write_mesh(exported_meshes, ob):
		me= ob.create_mesh(sce, True, 'RENDER')

		me_name= get_name(ob.data, "ME")

		if VRayExporter.use_instances:
			if me_name in exported_meshes:
				return
			exported_meshes.append(me_name)
		else:
			me_name= get_name(ob, "ME")

		if VRayExporter.debug:
			print("V-Ray/Blender: [%i]\n  Object: %s\n    Mesh: %s"
				  %(sce.frame_current,
					ob.name,
					ob.data.name))
		else:
			if PLATFORM == "linux2":
				sys.stdout.write("V-Ray/Blender: [%i] Mesh: \033[0;32m%s\033[0m                              \r"
								 %(sce.frame_current, ob.data.name))
			else:
				sys.stdout.write("V-Ray/Blender: [%i] Mesh: %s                              \r"
								 %(sce.frame_current, ob.data.name))
			sys.stdout.flush()

		ofile.write("\nGeomStaticMesh %s {"%(me_name))

		ofile.write("\n\tvertices= interpolate((%d, ListVector("%(sce.frame_current))
		for v in me.vertices:
			if(v.index):
				ofile.write(",")
			ofile.write("Vector(%.6f,%.6f,%.6f)"%(tuple(v.co)))
		ofile.write(")));")

		ofile.write("\n\tfaces= interpolate((%d, ListInt("%(sce.frame_current))
		for f in me.faces:
			if f.index:
				ofile.write(",")
			if len(f.vertices) == 4:
				ofile.write("%d,%d,%d,%d,%d,%d"%(
					f.vertices[0], f.vertices[1], f.vertices[2],
					f.vertices[2], f.vertices[3], f.vertices[0]))
			else:
				ofile.write("%d,%d,%d"%(
					f.vertices[0], f.vertices[1], f.vertices[2]))
		ofile.write(")));")

		ofile.write("\n\tface_mtlIDs= ListInt(")
		for f in me.faces:
			if f.index:
				ofile.write(",")
			if len(f.vertices) == 4:
				ofile.write("%d,%d"%(
					f.material_index + 1, f.material_index + 1))
			else:
				ofile.write("%d"%(
					f.material_index + 1))
		ofile.write(");")
=======
		for ob in scene.objects:
			if ob.type not in GEOM_TYPES:
				continue

			# Skip proxy meshes
			if hasattr(ob.data, 'GeomMeshFile') and ob.data.vray.GeomMeshFile.use:
				continue

			if VRayExporter.mesh_active_layers or bus['preview']:
				if not object_on_visible_layers(scene,ob):
					continue
>>>>>>> devel

			try:
				mesh= ob.to_mesh(scene, True, 'RENDER')
			except:
				mesh= ob.create_mesh(scene, True, 'RENDER')
			mesh_name= get_name(ob.data, prefix='ME')

			if VRayExporter.use_instances:
				if mesh_name in bus['filter']['mesh']:
					continue
				bus['filter']['mesh'].append(mesh_name)
			else:
				mesh_name= get_name(ob, prefix='ME')

			bus['node']= {}

			# Currently processes object
			bus['node']['object']= ob
			bus['node']['mesh']= mesh
			bus['node']['mesh_name']= mesh_name

			PLUGINS['GEOMETRY']['GeomStaticMesh'].write(bus)

	# Output files
	bus['files']['geometry']= []
	if bus['preview']:
		bus['files']['geometry'].append(open(bus['filenames']['geometry'], 'w'))
	else:
		for thread in range(scene.render.threads):
			bus['files']['geometry'].append(open(bus['filenames']['geometry'][:-11]+"_%.2i.vrscene"%(thread), 'w'))

	for geometry_file in bus['files']['geometry']:
		geometry_file.write("// V-Ray/Blender %s" % VERSION)
		geometry_file.write("\n// Geometry file\n")

	timer= time.clock()
	debug(scene, "Writing meshes...")

	if VRayExporter.animation and not VRayExporter.camera_loop:
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

	del bus['files']['geometry']
	
<<<<<<< HEAD
	for ob in sce.objects:
		if ob.type in ('LAMP','CAMERA','ARMATURE','EMPTY','LATTICE'):
			continue
		if ob.data.vray.GeomMeshFile.use:
			continue
		if VRayExporter.mesh_active_layers:
			if not object_on_visible_layers(sce,ob):
				continue
=======
	debug(scene, "Writing meshes... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))


def write_geometry(bus):
	scene=        bus['scene']
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	
	try:
		# Try calling V-Ray/Blender mesh export operator
		bpy.ops.vray.export_meshes(
			filepath=          bus['filenames']['geometry'][:-11],
			use_active_layers= VRayExporter.mesh_active_layers,
			use_animation=     VRayExporter.animation,
			use_instances=     VRayExporter.use_instances,
			debug=             VRayExporter.mesh_debug,
			check_animated=    VRayExporter.check_animated,
		)
>>>>>>> devel

	except:
		# Use python mesh export
		write_geometry_python(bus)


def write_GeomMayaHair(bus, ps, hair_geom_name):
	scene= bus['scene']
	ofile= bus['files']['nodes']
	ob=    bus['node']['object']

	VRayFur= ps.settings.vray.VRayFur

<<<<<<< HEAD
def write_geometry(sce):
	VRayScene= sce.vray
	VRayExporter= VRayScene.exporter

	geometry_file= get_filenames(sce,'geometry')

	try:
		bpy.ops.vray.export_meshes(
			filepath= geometry_file[:-11],
			use_active_layers= VRayExporter.mesh_active_layers,
			use_animation= VRayExporter.animation,
			use_instances= VRayExporter.use_instances,
			check_animated= VRayExporter.check_animated,
		)
	except:
		write_geometry_python(sce, geometry_file)


def write_GeomMayaHair(ofile, ob, ps, name):
=======
>>>>>>> devel
	num_hair_vertices= []
	hair_vertices=     []
	widths=            []

	for p,particle in enumerate(ps.particles):
		sys.stdout.write("%s: Object: %s => Hair: %s\r" % (color("V-Ray/Blender", 'green'), color(ob.name,'yellow'), color(p, 'green')))
		sys.stdout.flush()

		segments= len(particle.hair)
		num_hair_vertices.append( HexFormat(segments) )
		
		width= VRayFur.width / 2.0
		thin_start= int(VRayFur.thin_start / 100 * segments)
		thin_segments= segments - thin_start
		thin_step= width / (thin_segments + 1)
		for s,segment in enumerate(particle.hair):
			for c in segment.co:
				hair_vertices.append( HexFormat(c) )
			if bus['preview']:
				widths.append( HexFormat(0.01) )
			else:
				if VRayFur.make_thinner:
					if s > thin_start:
						width-= thin_step
				widths.append( HexFormat(width) )

	ofile.write("\nGeomMayaHair %s {" % hair_geom_name)
	ofile.write("\n\tnum_hair_vertices= interpolate((%d,ListIntHex(\"%s\")));"%(scene.frame_current,     ''.join(num_hair_vertices)))
	ofile.write("\n\thair_vertices= interpolate((%d,ListVectorHex(\"%s\")));"%(scene.frame_current,  ''.join(hair_vertices)))
	ofile.write("\n\twidths= interpolate((%d,ListFloatHex(\"%s\")));"%(scene.frame_current,          ''.join(widths)))
	ofile.write("\n}\n")



'''
  SETTINGS
'''
def write_settings(bus):
	ofile= bus['files']['scene']
	scene= bus['scene']
	
	VRayScene=      scene.vray
	VRayExporter=   VRayScene.exporter
	VRayDR=         VRayScene.VRayDR
	SettingsOutput= VRayScene.SettingsOutput

	for key in bus['filenames']:
		if key in ('output', 'output_filename', 'output_loadfile', 'lightmaps', 'scene', 'DR'):
			# Skip some files
			continue

		if VRayDR.on:
			if VRayDR.type == 'WW':
				ofile.write("\n#include \"//%s/%s/%s/%s\"" % (HOSTNAME, "RENDER", bus['filenames']['DR']['sub_dir'], bus['filenames'][key]))
			else:
				if key == 'geometry':
					for t in range(scene.render.threads):
						ofile.write("\n#include \"%s_%.2i.vrscene\"" % (bus['filenames']['DR']['prefix'] + os.sep + os.path.basename(bus['filenames']['geometry'][:-11]), t))

				else:
					ofile.write("\n#include \"%s\"" % (bus['filenames']['DR']['prefix'] + os.sep + os.path.basename(bus['filenames'][key])))

		else:
			if key == 'geometry':
				if bus['preview']:
					ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames']['geometry']))
				else:
					for t in range(scene.render.threads):
						ofile.write("\n#include \"%s_%.2i.vrscene\"" % (os.path.basename(bus['filenames']['geometry'][:-11]), t))
			else:
				ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames'][key]))
	ofile.write("\n")

	for key in PLUGINS['SETTINGS']:
		if key in ('BakeView', 'RenderView'):
			# Skip some plugins
			continue

		plugin= PLUGINS['SETTINGS'][key]
		if hasattr(plugin, 'write'):
			plugin.write(bus)

	if VRayScene.render_channels_use:
		for render_channel in VRayScene.render_channels:
			if render_channel.use:
				plugin= PLUGINS['RENDERCHANNEL'].get(render_channel.type)
				if plugin:
					plugin.write(ofile, getattr(render_channel,plugin.PLUG), scene, render_channel.name)

	if bus['preview']:
		# Material / texture preview settings
		bus['files']['scene'].write("\nSettingsColorMapping {")
		bus['files']['scene'].write("\n\ttype= 1;")
		bus['files']['scene'].write("\n\tsubpixel_mapping= 0;")
		bus['files']['scene'].write("\n\tclamp_output= 0;")
		bus['files']['scene'].write("\n\tadaptation_only= 0;")
		bus['files']['scene'].write("\n\tlinearWorkflow= 0;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsDMCSampler {")
		bus['files']['scene'].write("\n\tadaptive_amount= 0.85;")
		bus['files']['scene'].write("\n\tadaptive_threshold= 0.1;")
		bus['files']['scene'].write("\n\tsubdivs_mult= 0.1;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsOptions {")
		bus['files']['scene'].write("\n\tmtl_limitDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_maxDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_transpMaxLevels= 10;")
		bus['files']['scene'].write("\n\tmtl_transpCutoff= 0.1;")
		bus['files']['scene'].write("\n\tmtl_glossy= 1;")
		bus['files']['scene'].write("\n\tmisc_lowThreadPriority= 1;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsImageSampler {")
		bus['files']['scene'].write("\n\ttype= 0;") # Fastest result, but no AA :(
		bus['files']['scene'].write("\n\tfixed_subdivs= 1;")
		bus['files']['scene'].write("\n}\n")

	ofile.write("\n")



'''
  MATERIALS & TEXTURES
'''
def write_lamp_textures(bus):
	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']

<<<<<<< HEAD
	return {
		'color':       (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(la.color)),                 0, 'NONE'),
		'intensity':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([VRayLamp.intensity]*3)),   0, 'NONE'),
		'shadowColor': (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(VRayLamp.shadowColor)),     0, 'NONE'),
	}

def material_defaults(ma):
	VRayMaterial=    ma.vray
	BRDFVRayMtl=     VRayMaterial.BRDFVRayMtl
	BRDFSSS2Complex= VRayMaterial.BRDFSSS2Complex
	EnvironmentFog=  VRayMaterial.EnvironmentFog

	if VRayMaterial.type == 'MTL':
		return {
			'diffuse':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),          0, 'NONE'),
			'roughness': (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.roughness]*3)), 0, 'NONE'),
			'opacity':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([ma.alpha]*3)),              0, 'NONE'),

			'reflect_glossiness':  (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.reflect_glossiness]*3)), 0, 'NONE'),
			'hilight_glossiness':  (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.hilight_glossiness]*3)), 0, 'NONE'),
		
			'reflect':             (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFVRayMtl.reflect_color)),           0, 'NONE'),
			'anisotropy':          (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.anisotropy]*3)),          0, 'NONE'),
			'anisotropy_rotation': (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.anisotropy_rotation]*3)), 0, 'NONE'),
			'refract':             (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFVRayMtl.refract_color)),           0, 'NONE'),
			'refract_glossiness':  (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFVRayMtl.refract_glossiness]*3)),  0, 'NONE'),
			'translucency_color':  (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFVRayMtl.translucency_color)),      0, 'NONE'),

			'fresnel_ior':  ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
			'refract_ior':  ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
			'normal':       ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
			'displacement': ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
		}

	elif VRayMaterial.type == 'EMIT':
		return {
			'diffuse':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),          0, 'NONE'),
			'opacity':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([ma.alpha]*3)),              0, 'NONE'),
		}
	
	elif VRayMaterial.type == 'SSS':
		return {
			'overall_color':       (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),                   0, 'NONE'),
			'sub_surface_color':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.sub_surface_color)),  0, 'NONE'),
			'scatter_radius':      (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.scatter_radius)),     0, 'NONE'),
			'diffuse_color':       (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.diffuse_color)),      0, 'NONE'),
			'diffuse_amount':      (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFSSS2Complex.diffuse_amount]*3)), 0, 'NONE'),
			'specular_color':      (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.specular_color)),     0, 'NONE'),
			'specular_amount':     ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
			'specular_glossiness': ("AColor(0.0,0.0,0.0,1.0)", 0, 'NONE'),
		}
		
	elif VRayMaterial.type == 'VOL':
		return {
			'color_tex':    (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),           0, 'NONE'),
			'emission_tex': (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(EnvironmentFog.emission)),    0, 'NONE'),
			'density_tex':  (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([EnvironmentFog.density]*3)), 0, 'NONE'),
		}
	else:
		return {
			'diffuse':   (a(sce,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)),          0, 'NONE'),
		}
=======
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
>>>>>>> devel

	la= ob.data
	VRayLamp= la.vray

	defaults= {
		'color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(la.color)),               0, 'NONE'),
		'intensity':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([VRayLamp.intensity]*3)), 0, 'NONE'),
		'shadowColor': (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(VRayLamp.shadowColor)),   0, 'NONE'),
	}

	bus['lamp_textures']= {}
	
	for i,slot in enumerate(la.texture_slots):
		if slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot=    slot.texture.vray_slot
			VRayLight=   VRaySlot.VRayLight
			
			for key in defaults:
				use_slot= False
				factor=   1.0
				
				if getattr(VRayLight, 'map_'+key):
					use_slot= True
					factor=   getattr(VRayLight, key+'_mult')

				if use_slot:
					if key not in bus['lamp_textures']: # First texture
						bus['lamp_textures'][key]= []
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
<<<<<<< HEAD
							mapped_params['mapto'][key].append(defaults[key])
					params['mapto']=    key
					params['slot']=     slot
					params['texture']=  slot.texture
					params['factor']=   factor
					mapped_params['mapto'][key].append( [write_texture_factor(ofile, sce, params),
														 slot.use_stencil,
														 VRaySlot.blend_mode] )

	for key in mapped_params['mapto']:
		if len(mapped_params['mapto'][key]) == 2:
			if mapped_params['mapto'][key][1][2] == 'NONE':
				mapped_params['mapto'][key][1][2]= 'OVER'

	if len(mapped_params['mapto']):
		debug(sce, "V-Ray/Blender: Lamp \"%s\" texture stack: %s" % (la.name,mapped_params['mapto']))
=======
							bus['lamp_textures'][key].append(defaults[key])

					bus['mtex']= {}
					bus['mtex']['mapto']=   key
					bus['mtex']['slot']=    slot
					bus['mtex']['texture']= slot.texture
					bus['mtex']['factor']=  factor
					bus['mtex']['name']=    clean_string("LT%.2iSL%sTE%s" % (i,
																			 slot.name,
																			 slot.texture.name))

					# Write texture
					write_texture(bus)

					bus['lamp_textures'][key].append( [stack_write_texture(bus),
													   slot.use_stencil,
													   VRaySlot.blend_mode] )

	for key in bus['lamp_textures']:
		if len(bus['lamp_textures'][key]) == 2 and type(bus['lamp_textures'][key][0]) is tuple:
			if bus['lamp_textures'][key][1][2] == 'NONE':
				bus['lamp_textures'][key][1][2]= 'OVER'

	if VRayExporter.debug:
		if len(bus['lamp_textures']):
			print_dict(scene, "Lamp \"%s\" texture stack" % la.name, bus['lamp_textures'])
>>>>>>> devel
	
	for key in bus['lamp_textures']:
		if len(bus['lamp_textures'][key]):
			bus['lamp_textures'][key]= write_TexOutput(bus, stack_write_textures(bus, stack_collapse_layers(bus['lamp_textures'][key])), key)

	return bus['lamp_textures']


def write_material_textures(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ma=    bus['material']['material']

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter

	VRayMaterial= ma.vray

	mapped_params= PLUGINS['BRDF'][VRayMaterial.type].mapto(bus)

	# Mapped parameters
	bus['textures']= {}

	for i,slot in enumerate(ma.texture_slots):
		if ma.use_textures[i] and slot and slot.texture and (slot.texture.type in TEX_TYPES or slot.texture.use_nodes):
			VRaySlot=    slot.texture.vray_slot
			VRayTexture= slot.texture.vray

			for key in mapped_params:
				if getattr(VRaySlot, 'map_'+key):
					factor= getattr(VRaySlot, key+'_mult')
					
					if key not in bus['textures']: # If texture is first in stack
						bus['textures'][key]= []
						# If this texture will be blended over some value
						# we need to add this value
						# (for example, texture blended over diffuse color)
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
<<<<<<< HEAD
							mapped_params['mapto'][key].append(defaults[key])
					params['mapto']=    key
					params['slot']=     slot
					params['texture']=  slot.texture
					params['factor']=   factor
					mapped_params['mapto'][key].append( [write_texture_factor(ofile, sce, params),
														 slot.use_stencil,
														 VRaySlot.blend_mode] )

	for key in mapped_params['mapto']:
		if len(mapped_params['mapto'][key]) == 2 and type(mapped_params['mapto'][key][0]) is tuple:
			if mapped_params['mapto'][key][1][2] == 'NONE':
				mapped_params['mapto'][key][1][2]= 'OVER'

	if len(mapped_params['mapto']):
		debug(sce, "V-Ray/Blender: Material \"%s\" texture stack: %s" % (ma.name,mapped_params['mapto']))
	
	for key in mapped_params['mapto']:
		if len(mapped_params['mapto'][key]):
			mapped_params['mapto'][key]= write_TexOutput(
				ofile,
				stack_write_shaders(ofile, stack_collapse_layers(mapped_params['mapto'][key])),
				{} # TODO: TexOutput params
			)

	return mapped_params


def write_BRDFVRayMtl(ofile, ma, ma_name, mapped_params):
	defaults= material_defaults(ma)
=======
							bus['textures'][key].append(mapped_params[key])
>>>>>>> devel

					# Store slot for GeomDisplaceMesh
					if key == 'displacement':
						bus['node']['displacement_slot']= slot

					# Store slot for BRDFBump
					elif key == 'normal':
						bus['material']['normal_slot']= slot
						
					bus['mtex']= {}
					bus['mtex']['slot']=    slot
					bus['mtex']['texture']= slot.texture
					bus['mtex']['mapto']=   key
					bus['mtex']['factor']=  factor
					# bus['mtex']['name']=    clean_string("MT%.2iSL%sTE%s" % (i, slot.name, slot.texture.name))
					bus['mtex']['name']=    clean_string("MT%.2iTE%s" % (i, slot.texture.name))

					if VRayTexture.texture_coords == 'ORCO':
						bus['material']['orco_suffix']= get_name(get_orco_object(scene, bus['node']['object'], VRayTexture),
																 prefix='ORCO')

						bus['mtex']['name']+= bus['material']['orco_suffix']

<<<<<<< HEAD
	if 'opacity' in textures:
		ofile.write("\n\topacity= %s::out_intensity;" % textures['opacity'])
	else:
		ofile.write("\n\topacity= %s;" % a(sce,ma.alpha))

	for param in OBJECT_PARAMS['BRDFVRayMtl']:
		if param == 'translucency':
			value= TRANSLUCENSY[BRDFVRayMtl.translucency]
		elif param == 'anisotropy_rotation':
			value= BRDFVRayMtl.anisotropy_rotation / 360.0
		elif param == 'translucency_thickness':
			value= BRDFVRayMtl.translucency_thickness * 1000000000000
		elif param == 'option_glossy_rays_as_gi':
			value= GLOSSY_RAYS[BRDFVRayMtl.option_glossy_rays_as_gi]
		elif param == 'option_energy_mode':
			value= ENERGY_MODE[BRDFVRayMtl.option_energy_mode]
		else:
			value= getattr(BRDFVRayMtl,param)
		ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")
=======
					if VRayExporter.debug:
						print_dict(scene, "bus['mtex']", bus['mtex'])
>>>>>>> devel

					# Write texture
					write_texture(bus)

					# Append texture to stack and write texture with factor
					bus['textures'][key].append( [stack_write_texture(bus),
												  slot.use_stencil,
												  VRaySlot.blend_mode] )

	# In case we have only 1 texture blended over color
	# set its blend type to 'OVER' if its 'NONE'
	for key in bus['textures']:
		if len(bus['textures'][key]) == 2 and type(bus['textures'][key][0]) is tuple:
			if bus['textures'][key][1][2] == 'NONE':
				bus['textures'][key][1][2]= 'OVER'

	if VRayExporter.debug:
		if len(bus['textures']):
			print_dict(scene, "Material \"%s\" texture stack" % ma.name, bus['textures'])

	# Collapsing texture stack
	for key in bus['textures']:
		if len(bus['textures'][key]):
			bus['textures'][key]= write_TexOutput(bus, stack_write_textures(bus, stack_collapse_layers(bus['textures'][key])), key)

	if 'displacement' in bus['textures']:
		bus['node']['displacement_texture']= bus['textures']['displacement']

	if VRayExporter.debug:
		if len(bus['textures']):
			print_dict(scene, "Material \"%s\" textures" % ma.name, bus['textures'])

	return bus['textures']


def	write_material(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']

	ob=    bus['node']['object']
	base=  bus['node']['base']

	ma=    bus['material']['material']

	if base.dupli_type == 'GROUP':
		base_material_names= []
		for slot in base.material_slots:
			if slot and slot.material:
				base_material_names.append(slot.material.name)
		for base_ma in base_material_names:
			if base_ma.find(ma.name) != -1:
				slot= base.material_slots.get(base_ma)
				ma=   slot.material
				bus['material']['material']= ma

	VRayMaterial= ma.vray

	ma_name= get_name(ma, prefix='MA')

	# Check Toon before cache
	if VRayMaterial.VolumeVRayToon.use:
		bus['effects']['toon']['effects'].append(
			PLUGINS['SETTINGS']['SettingsEnvironment'].write_VolumeVRayToon_from_material(bus)
		)
		append_unique(bus['effects']['toon']['objects'], bus['node']['object'])

	# Write material textures
	write_material_textures(bus)

	# Check if material uses object mapping
	# In this case material is object dependend
	# because mapping is object dependent
	if bus['material']['orco_suffix']:
		ma_name+= bus['material']['orco_suffix']

	if not append_unique(bus['cache']['materials'], ma_name):
		return ma_name
	
	# Write material BRDF
	brdf= PLUGINS['BRDF'][VRayMaterial.type].write(bus)

	# Add BRDFBump if needed
	brdf= PLUGINS['BRDF']['BRDFBump'].write(bus, base_brdf= brdf)

	# Add wrapper / override / etc
	complex_material= []
	for component in (VRayMaterial.Mtl2Sided.use,
					  VRayMaterial.MtlWrapper.use,
					  VRayMaterial.MtlOverride.use,
					  VRayMaterial.MtlRenderStats.use,
					  VRayMaterial.material_id_number):
		if component:
			complex_material.append("MC%.2d_%s" % (len(complex_material), ma_name))
	complex_material.append(ma_name)
	complex_material.reverse()

	ofile.write("\nMtlSingleBRDF %s {"%(complex_material[-1]))
	ofile.write("\n\tbrdf= %s;" % a(scene, brdf))
	ofile.write("\n}\n")

	if VRayMaterial.Mtl2Sided.use:
		base_material= complex_material.pop()
		ofile.write("\nMtl2Sided %s {"%(complex_material[-1]))
		ofile.write("\n\tfront= %s;"%(base_material))
		back= base_material
		if VRayMaterial.Mtl2Sided.back:
			if VRayMaterial.Mtl2Sided.back in bpy.data.materials:
				back= get_name(bpy.data.materials[VRayMaterial.Mtl2Sided.back], prefix='MA')
		ofile.write("\n\tback= %s;"%(back))

		if VRayMaterial.Mtl2Sided.control == 'SLIDER':
			ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))
		elif VRayMaterial.Mtl2Sided.control == 'COLOR':
			ofile.write("\n\ttranslucency= %s;" % a(scene, VRayMaterial.Mtl2Sided.translucency_color))
		else:
			if VRayMaterial.Mtl2Sided.translucency_tex:
				if VRayMaterial.Mtl2Sided.translucency_tex in bpy.data.materials:
					ofile.write("\n\ttranslucency_tex= %s;"%(get_name(bpy.data.textures[VRayMaterial.Mtl2Sided.translucency_tex], prefix='TE')))
					ofile.write("\n\ttranslucency_tex_mult= %s;" % a(scene,VRayMaterial.Mtl2Sided.translucency_tex_mult))
			else:
				ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))

		ofile.write("\n\tforce_1sided= %d;" % VRayMaterial.Mtl2Sided.force_1sided)
		ofile.write("\n}\n")

	if VRayMaterial.MtlWrapper.use:
		base_material= complex_material.pop()
		ofile.write("\nMtlWrapper %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_material= %s;"%(base_material))
		for param in PLUGINS['MATERIAL']['MtlWrapper'].PARAMS:
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
					ofile.write("\n\t%s= %s;"%(param, get_name(bpy.data.materials[override_material], prefix='MA')))

		environment_override= VRayMaterial.MtlOverride.environment_override
		if environment_override:
			if environment_override in bpy.data.textures:
				ofile.write("\n\tenvironment_override= %s;" % get_name(bpy.data.textures[environment_override], prefix='TE'))

		ofile.write("\n\tenvironment_priority= %i;"%(VRayMaterial.MtlOverride.environment_priority))
		ofile.write("\n}\n")

	if VRayMaterial.MtlRenderStats.use:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlRenderStats %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))
		for param in PLUGINS['MATERIAL']['MtlRenderStats'].PARAMS:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayMaterial.MtlRenderStats,param))))
		ofile.write("\n}\n")

	if VRayMaterial.material_id_number:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlMaterialID %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;" % base_mtl)
		ofile.write("\n\tmaterial_id_number= %i;" % VRayMaterial.material_id_number)
		ofile.write("\n\tmaterial_id_color= %s;" % p(VRayMaterial.material_id_color))
		ofile.write("\n}\n")

	return ma_name


def write_materials(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']

	ob=    bus['node']['object']

<<<<<<< HEAD
	return mtl_name


def write_node_material(sce, ma, filters, object_params, ofile, ob, params):
	debug(sce,"Writing node material: %s"%(ma.name))

	def get_brdf_type(ma):
		vma= ma.vray
		if vma.type == 'MTL':
			if sce.vray.exporter.compat_mode:
				return 'BRDFLayered'
			else:
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
			if n.to_socket == ns:
				return n.from_node
		return None

	def write_node(ofile, ma, nt, no):
		debug(sce,"  Writing node: %s [%s]"%(no.name, no.type))

		if no.type == 'OUTPUT':
			brdf_name= "BRDFDiffuse_no_material"

			for ns in no.inputs:
				if ns.name == 'Color':
					color= find_connected_node(nt, ns)
					brdf_name= "%s_%s_%s"%(ma.name, nt.name, color.name)

			ofile.write("\nMtlSingleBRDF %s {"%(get_name(ma,'Material')))
			ofile.write("\n\tbrdf= %s;"%(clean_string(brdf_name)))
			ofile.write("\n}\n")

		elif no.type in ('MATERIAL','MATERIAL_EXT'):
			write_material(no.material, filters, object_params, ofile)

		elif no.type == 'MIX_RGB':
			color1= "BRDFDiffuse_no_material"
			color2= "BRDFDiffuse_no_material"
			fac= "Color(0.5,0.5,0.5)"
			weights= "TEDefaultBlend"
			
			brdf_name= "%s_%s_%s"%(ma.name, nt.name, no.name)

			for ns in no.inputs:
				if ns.name == 'Color1':
					node_color1= find_connected_node(nt, ns)
				elif ns.name == 'Color2':
					node_color2= find_connected_node(nt, ns)
				else:
					fac= "Color(1.0,1.0,1.0)*%.3f"%(1.0 - ns.default_value[0])
					node_fac= find_connected_node(nt, ns)

			if node_color1:
				if node_color1.type in ('MATERIAL','MATERIAL_EXT'):
					color1= get_name(node_color1.material,'%s_Material' % get_brdf_type(node_color1.material))

			if node_color2:
				if node_color2.type in ('MATERIAL','MATERIAL_EXT'):
					color2= get_name(node_color2.material,'%s_Material' % get_brdf_type(node_color2.material))

			if node_fac:
				if node_fac.type == 'TEXTURE':
					weights= write_texture(ofile, sce, {'material': ma,
														'texture': node_fac.texture})
			else:
				weights= "weights_%s"%(clean_string(brdf_name))
				ofile.write("\nTexAColor %s {"%(weights))
				ofile.write("\n\tuvwgen= UVWGenChannel_default;")
				ofile.write("\n\ttexture= %s;"%(fac))
				ofile.write("\n}\n")

			ofile.write("\nBRDFLayered %s {"%(clean_string(brdf_name)))
			ofile.write("\n\tbrdfs= List(%s,%s);"%(color1, color2))
			ofile.write("\n\tweights= List(%s,TEDefaultBlend);"%(weights))
			ofile.write("\n\tadditive_mode= 0;") # Shellac
			ofile.write("\n}\n")

		elif no.type == 'TEXTURE':
			tex_name= write_texture(ofile, sce, {'material': ma,
												 'texture': no.texture})

		elif no.type == 'INVERT':
			debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(no.name,no.type))

	nt= ma.node_tree
	for n in nt.nodes:
		if n.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT'):
			write_node(ofile, ma, nt, n)
		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(n.name, n.type))


def write_materials(ofile,ob,filters,object_params):
	uv_layers= object_params['uv_ids']
=======
	# Multi-material name
	mtl_name= get_name(ob, prefix='OBMA')
>>>>>>> devel

	# Collecting and exporting object materials
	mtls_list= []
	ids_list=  []
	ma_id= 0 # For cases with empty slots
	if len(ob.material_slots):
		for slot in ob.material_slots:
			ma= slot.material
			if ma:
<<<<<<< HEAD
				if sce.vray.exporter.use_material_nodes and ma.use_nodes and hasattr(ma.node_tree, 'links'):
					debug(sce,"Node materials temporarily disabled...")
					write_node_material(sce, ma, filters, object_params, ofile, ob, {'uv_ids': uv_layers})
				else:
					write_material(ma, filters, object_params, ofile, ob= ob, params= {'uv_ids': uv_layers})
=======
				bus['material']= {}
				bus['material']['material']= ma
>>>>>>> devel

				# Displace settings pointers
				bus['node']['displacement_slot']=    None
				bus['node']['displacement_texture']= None

				# Normal mapping settings pointer
				bus['material']['normal_slot']=      None

				# Set if any texture uses object mapping
				bus['material']['orco_suffix']=      ""

				if ma.use_nodes:
					mtls_list.append(write_node_material(bus))

				else:
					mtls_list.append(write_material(bus))
					ma_id+= 1
					ids_list.append(str(ma_id))

	# No materials assigned - use default material
	if len(mtls_list) == 0: 
		bus['node']['material']= bus['defaults']['material']

	# Only one material - no need to Multi-material
	elif len(mtls_list) == 1:
		bus['node']['material']= mtls_list[0]

	# Several materials assigned - need Mutli-material
	else:
		bus['node']['material']= mtl_name
		ofile.write("\nMtlMulti %s {" % mtl_name)
		ofile.write("\n\tmtls_list= List(%s);" % ','.join(mtls_list))
		ofile.write("\n\tids_list= ListInt(%s);" % ','.join(ids_list))
		ofile.write("\n}\n")


def write_lamp(bus):
	LIGHT_PORTAL= {
		'NORMAL':  0,
		'PORTAL':  1,
		'SPORTAL': 2,
	}
	SKY_MODEL= {
		'CIEOVER'  : 2,
		'CIECLEAR' : 1,
		'PREETH'   : 0,
	}
	UNITS= {
		'DEFAULT' : 0,
		'LUMENS'  : 1,
		'LUMM'    : 2,
		'WATTSM'  : 3,
		'WATM'    : 4,
	}

	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']

	lamp= ob.data
	VRayLamp= lamp.vray

	lamp_type= None
	lamp_name= get_name(ob, prefix='LA')
	lamp_matrix= ob.matrix_world

	textures= write_lamp_textures(bus)

	if bus['node']['dupli'].get('matrix'):
		lamp_matrix= bus['node']['dupli']['matrix']

	if bus['node']['particle'].get('matrix'):
		lamp_matrix= bus['node']['particle']['matrix']

	if lamp.type == 'POINT':
		if VRayLamp.radius > 0:
			lamp_type= 'LightSphere'
		else:
			lamp_type= 'LightOmni'
	elif lamp.type == 'SPOT':
		if VRayLamp.spot_type == 'SPOT':
			lamp_type= 'LightSpot'
		else:
			lamp_type= 'LightIES'
	elif lamp.type == 'SUN':
		if VRayLamp.direct_type == 'DIRECT':
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

		if lamp.type == 'SUN' and VRayLamp.direct_type == 'DIRECT':
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
		if lamp.type == 'SUN' and VRayLamp.direct_type == 'DIRECT':
			ofile.write("\n\tshadowColor_tex= %s;" % textures['shadowColor'])
		else:
			ofile.write("\n\tshadow_color_tex= %s;" % textures['shadowColor'])
		
	if lamp_type == 'SunLight':
		ofile.write("\n\tsky_model= %i;"%(SKY_MODEL[VRayLamp.sky_model]))
	else:
		if VRayLamp.color_type == 'RGB':
			color= lamp.color
		else:
			color= kelvin_to_rgb(VRayLamp.temperature)
		ofile.write("\n\tcolor= %s;" % a(scene, "Color(%.6f, %.6f, %.6f)"%(tuple(color))))
			
		if lamp_type != 'LightIES':
			ofile.write("\n\tunits= %i;"%(UNITS[VRayLamp.units]))

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
		ofile.write("\n\tlightPortal= %i;"%(LIGHT_PORTAL[VRayLamp.lightPortal]))

	for param in LIGHT_PARAMS[lamp_type]:
		if param == 'shadow_subdivs':
			ofile.write("\n\tshadow_subdivs= %s;"%(a(scene,VRayLamp.subdivs)))
		elif param == 'shadowRadius' and lamp_type == 'LightDirectMax':
			ofile.write("\n\t%s= %s;" % (param, a(scene,VRayLamp.shadowRadius)))
			ofile.write("\n\tshadowRadius1= %s;" % a(scene,VRayLamp.shadowRadius))
			ofile.write("\n\tshadowRadius2= %s;" % a(scene,VRayLamp.shadowRadius))
		elif param == 'intensity' and lamp_type == 'LightIES':
			ofile.write("\n\tpower= %s;"%(a(scene,VRayLamp.intensity)))
		elif param == 'shadow_color':
			ofile.write("\n\tshadow_color= %s;"%(a(scene,VRayLamp.shadowColor)))
		elif param == 'ies_file':
			ofile.write("\n\t%s= \"%s\";"%(param, get_full_filepath(bus,lamp,VRayLamp.ies_file)))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayLamp,param))))

	ofile.write("\n\ttransform= %s;"%(a(scene,transform(lamp_matrix))))
	ofile.write("\n}\n")


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
		lamp_name= get_name(lamp, prefix='LA')
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

<<<<<<< HEAD
	lights.extend(mesh_lights)
	
	base_mtl= material
	if sce.vray.SettingsOptions.mtl_override_on and sce.vray.SettingsOptions.mtl_override:
		base_mtl= get_name(bpy.data.materials[sce.vray.SettingsOptions.mtl_override],"Material")

	material= "HFV%s" % (name)
=======
	node_name= bus['node']['name']
	matrix=    bus['node']['matrix']
	base_mtl=  bus['node']['material']

	if SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
		material= get_name(bpy.data.materials[SettingsOptions.mtl_override], prefix='MA')

	material= "RS%s" % node_name
>>>>>>> devel

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
	if bus['node']['particle']:
		ofile.write("\n\tvisible= %s;" % a(scene, bus['node']['particle']['visible']))
	ofile.write("\n\ttransform= %s;" % a(scene, transform(matrix)))
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

	bus['node']['name']=      get_name(ob, prefix='OB')
	bus['node']['geometry']=  get_name(ob.data if VRayExporter.use_instances else ob, prefix='ME')
	bus['node']['matrix']=    ob.matrix_world

	# Skip if object is just dupli holder
	if ob.dupli_type == 'GROUP':
		return

<<<<<<< HEAD
	if props['material'] is not None:
		# Don't override proxy material (proxy could have multi-material)
		if hasattr(VRayData,'GeomMeshFile') and VRayData.GeomMeshFile.use:
			ma_name= write_materials(props['files']['materials'],ob,props['filters'],object_params)
		else:
			ma_name= props['material']
	else:
		ma_name= write_materials(props['files']['materials'],ob,props['filters'],object_params)

	node_geometry= get_name(ob, "ME")
	if VRayExporter.use_instances:
		node_geometry= get_name(ob.data, "ME")

	if hasattr(VRayData,'GeomMeshFile') and VRayData.GeomMeshFile.use:
		node_geometry= write_mesh_file(ofile, props['filters']['exported_proxy'], ob)
=======
	# Write object materials
	write_materials(bus)

	# VRayProxy
	PLUGINS['GEOMETRY']['GeomMeshFile'].write(bus)
>>>>>>> devel

	# Displace
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].write(bus)

	# Correct matrix if particles / dupli
	if bus['node']['particle']:
		bus['node']['name']=   bus['node']['particle']['name']
		bus['node']['matrix']= bus['node']['particle']['matrix']

	elif bus['node']['dupli']:
		# if bus['node']['dupli']['type'] == 'GROUP':
		# 	bus['node']['matrix']= bus['node']['dupli']['matrix'] * bus['node']['matrix']
		# else:
		# 	bus['node']['matrix']= bus['node']['dupli']['matrix']
		bus['node']['name']=   bus['node']['dupli']['name']
		bus['node']['matrix']= bus['node']['dupli']['matrix']

	# Mesh-light
	if PLUGINS['GEOMETRY']['LightMesh'].write(bus):
		return

	complex_material= []
	complex_material.append(bus['node']['material'])
	for component in (VRayObject.MtlWrapper.use,
					  VRayObject.MtlOverride.use,
					  VRayObject.MtlRenderStats.use):
		if component:
			complex_material.append("OC%.2d_%s" % (len(complex_material), bus['node']['material']))
	complex_material.reverse()

	if VRayObject.MtlWrapper.use:
		base_material= complex_material.pop()
		ma_name= complex_material[-1]
		ofile.write("\nMtlWrapper %s {"%(ma_name))
		ofile.write("\n\tbase_material= %s;"%(base_material))
		for param in PLUGINS['MATERIAL']['MtlWrapper'].PARAMS:
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
		for param in PLUGINS['MATERIAL']['MtlRenderStats'].PARAMS:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayObject.MtlRenderStats,param))))
		ofile.write("\n}\n")

<<<<<<< HEAD
	if len(ob.particle_systems):
		for ps in ob.particle_systems:
			if ps.settings.use_render_emitter:
				write_node(ofile,node_name,node_geometry,ma_name,ob.pass_index,props['visible'],node_matrix,ob,params)
				break
	else:
		write_node(ofile,node_name,node_geometry,ma_name,ob.pass_index,props['visible'],node_matrix,ob,params)
=======
	write_node(bus)
>>>>>>> devel


def _write_object_particles(bus):
	scene= bus['scene']
	ob=    bus['node']['object']

	emitter_node= bus['node']['name']

	VRayScene= scene.vray
	VRayExporter= VRayScene.exporter

	if len(ob.particle_systems):
		# Write particle emitter if needed
		for ps in ob.particle_systems:
			if ps.settings.use_render_emitter:
				write_node(bus)
				break

		# Write particles
		for ps in ob.particle_systems:
			ps_material= "MANOMATERIALISSET"
			ps_material_idx= ps.settings.material
			if len(ob.material_slots) >= ps_material_idx:
				ps_material= get_name(ob.material_slots[ps_material_idx - 1].material, prefix='MA')

			if ps.settings.type == 'HAIR' and ps.settings.render_type == 'PATH':
				if VRayExporter.use_hair:
					hair_geom_name= "HAIR%s" % ps.name
					hair_node_name= "OB%sHAIR%s" % (ob.name, hair_geom_name)

					write_GeomMayaHair(bus, ps, hair_geom_name)

					bus['node']['name']= hair_node_name
					bus['node']['geometry']= hair_geom_name
					bus['node']['material']= ps_material

					write_node(bus)

					bus['node']['name']= emitter_node
					
			else:
				particle_objects= []
				if ps.settings.render_type == 'OBJECT':
					particle_objects.append(ps.settings.dupli_object)
				elif ps.settings.render_type == 'GROUP':
					particle_objects= ps.settings.dupli_group.objects
				else:
					continue

				for p,particle in enumerate(ps.particles):
					sys.stdout.write("%s: Object: %s => Particle: %s\r" % (color("V-Ray/Blender", 'green'), color(ob.name,'yellow'), color(p, 'green')))
					sys.stdout.flush()

					location= particle.location
					size= particle.size
					if ps.settings.type == 'HAIR':
						location= particle.hair[0].co
						size*= 3

					part_transform= mathutils.Matrix.Scale(size, 3) * particle.rotation.to_matrix()

					if ps.settings.rotation_mode == 'OB_Z':
						part_transform*= mathutils.Matrix.Rotation(math.radians(90.0), 3, 'Y')
					elif ps.settings.rotation_mode == 'NOR':
						part_transform*= mathutils.Matrix.Rotation(math.radians(-90.0), 3, 'Y')

					part_transform.resize_4x4()

					# Location
					part_transform[3][0]= location[0]
					part_transform[3][1]= location[1]
					part_transform[3][2]= location[2]

					for p_ob in particle_objects:
						part_name= "EM%sP%s" % (clean_string(ps.name), p)

						if bus['node']['particle'].get('name'):
							part_name= "OB%sPS%sP%s" %(bus['node']['particle']['name'],
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
						bus['node']['particle']= {}
						bus['node']['particle']['name']= part_name
						bus['node']['particle']['material']= ps_material
						bus['node']['particle']['matrix']= part_transform
						bus['node']['particle']['visible']= part_visibility

						_write_object(bus)

						bus['node']['object']= ob
						bus['node']['base']= ob
						bus['node']['visible']= True
						bus['node']['particle']= {}


def _write_object_dupli(bus):
	ob= bus['node']['object']

	if ob.dupli_type in ('VERTS','FACES','GROUP'):
		ob.dupli_list_create(bus['scene'])

		for dup_id,dup_ob in enumerate(ob.dupli_list):
			bus['node']['object']= dup_ob.object
			bus['node']['base']= ob
			bus['node']['dupli']['name']= "OB%sDO%s" % (clean_string(ob.name), dup_id)
			bus['node']['dupli']['matrix']= dup_ob.matrix
			bus['node']['dupli']['type']= ob.dupli_type

			_write_object(bus)

			bus['node']['object']= ob
			bus['node']['base']= ob
			bus['node']['dupli']= {}

		ob.dupli_list_clear()


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


def write_scene(bus):
	scene= bus['scene']

	VRayScene=       scene.vray

	VRayExporter=    VRayScene.exporter
	SettingsOptions= VRayScene.SettingsOptions

	# Some failsafe defaults
	bus['defaults']= {}
	bus['defaults']['brdf']=     "BRDFNOBRDFISSET"
	bus['defaults']['material']= "MANOMATERIALISSET"
	bus['defaults']['texture']=  "TENOTEXTUREIESSET"
	bus['defaults']['uvwgen']=   "DEFAULTUVWC"
	bus['defaults']['blend']=    "TEDefaultBlend"

	for key in bus['files']:
		bus['files'][key].write("// V-Ray/Blender %s" % VERSION)

	bus['files']['scene'].write("\n// Settings\n")
	bus['files']['nodes'].write("\n// Nodes\n")
	bus['files']['lights'].write("\n// Lights\n")
	bus['files']['camera'].write("\n// Camera\n")
	bus['files']['environment'].write("\n// Environment\n")
	bus['files']['materials'].write("\n// Materials\n")
	bus['files']['textures'].write("\n// Textures\n")

	bus['files']['textures'].write("\n// Useful defaults")
	bus['files']['textures'].write("\nUVWGenChannel %s {" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n\tuvw_channel= 1;")
	bus['files']['textures'].write("\n\tuvw_transform= Transform(Matrix(Vector(1.0,0.0,0.0),Vector(0.0,1.0,0.0),Vector(0.0,0.0,1.0)),Vector(0.0,0.0,0.0));")
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nTexChecker %s {" % bus['defaults']['texture'])
	bus['files']['textures'].write("\n\tuvwgen= %s;" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nBRDFDiffuse %s {" % bus['defaults']['brdf'])
	bus['files']['textures'].write("\n\tcolor=Color(0.5,0.5,0.5);")
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nMtlSingleBRDF %s {" % bus['defaults']['material'])
	bus['files']['textures'].write("\n\tbrdf= %s;" % bus['defaults']['brdf'])
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nTexAColor %s {" % bus['defaults']['blend'])
	bus['files']['textures'].write("\n\tuvwgen= %s;" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n\ttexture= AColor(1.0,1.0,1.0,1.0);")
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\n// Scene textures")

	if bus['preview']:
		bus['files']['lights'].write("\nLightDirectMax LALamp_008 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 3.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tfallsize= 100.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(1.000000, 0.000000, -0.000000),")
		bus['files']['lights'].write("\n\t\t\tVector(0.000000, 0.000000, 1.000000),")
		bus['files']['lights'].write("\n\t\t\tVector(0.000000, -1.000000, 0.000000)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(1.471056, -14.735638, 3.274598));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightSpot LALamp_002 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 80.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tconeAngle= 1.3;")
		bus['files']['lights'].write("\n\tpenumbraAngle= -0.4;")
		bus['files']['lights'].write("\n\tshadows= 1;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 1;")
		bus['files']['lights'].write("\n\tshadowRadius= 0.000000;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 8;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tdecay= 1.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(-0.549843, 0.655945, 0.517116),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.733248, -0.082559, -0.674931),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.400025, -0.750280, 0.526365)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(-5.725639, -13.646054, 8.5));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 350.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tspecular_contribution= 0.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 4;")
		bus['files']['lights'].write("\n\tdecay= 2.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\n\t\t\tVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(15.685226, -7.460007, 3.0));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp_001 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 300.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 1;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 8;")
		bus['files']['lights'].write("\n\tdecay= 2.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\n\t\t\tVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(-10.500286, -12.464991, 4.0));")
		bus['files']['lights'].write("\n}\n")

	# Processed objects
	bus['objects']= []

	# Effects from material / object settings
	bus['effects']= {}
	bus['effects']['fog']= {}

	bus['effects']['toon']= {}
	bus['effects']['toon']['effects']= []
	bus['effects']['toon']['objects']= []

	# Prepare exclude for effects
	exclude_list= []
	VRayEffects=  VRayScene.VRayEffects
	if VRayEffects.use:
		for effect in VRayEffects.effects:
			if effect.use:
				if effect.type == 'FOG':
					EnvironmentFog= effect.EnvironmentFog
					fog_objects= generate_object_list(EnvironmentFog.objects, EnvironmentFog.groups)
					for ob in fog_objects:
						if not object_visible(bus, ob):
							continue
						if ob not in exclude_list:
							exclude_list.append(ob)

	for ob in scene.objects:
		if ob.type in ('CAMERA','ARMATURE','LATTICE'):
			continue

		if ob not in exclude_list:
			bus['objects'].append(ob)

	del exclude_list

	def write_frame(bus):
		timer= time.clock()
		scene= bus['scene']

		debug(scene, "Writing frame %i..." % scene.frame_current)

<<<<<<< HEAD
		else:
			ofile.write("\nRenderView RenderView {")
			ofile.write("\n\ttransform= %s;"%(a(sce,transform(ca.matrix_world))))
			ofile.write("\n\tfov= %s;"%(a(sce,fov)))
			if SettingsCamera.type not in ('SPHERIFICAL','BOX'):
				ofile.write("\n\tclipping= 1;")
				ofile.write("\n\tclipping_near= %s;"%(a(sce,ca.data.clip_start)))
				ofile.write("\n\tclipping_far= %s;"%(a(sce,ca.data.clip_end)))
			if ca.data.type == 'ORTHO':
				ofile.write("\n\torthographic= 1;")
				ofile.write("\n\torthographicWidth= %s;" % a(sce,ca.data.ortho_scale))
			ofile.write("\n}\n")

		ofile.write("\nSettingsCamera Camera {")
		if ca.data.type == 'ORTHO':
			ofile.write("\n\ttype= 7;")
			ofile.write("\n\theight= %s;" % a(sce,ca.data.ortho_scale))
		else:
			ofile.write("\n\ttype= %i;"%(CAMERA_TYPE[SettingsCamera.type]))
		ofile.write("\n\tfov= %s;"%(a(sce,fov)))
		ofile.write("\n}\n")
=======
		VRayScene=       scene.vray
>>>>>>> devel

		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		# Cache stores already exported data
		bus['cache']= {}
		bus['cache']['textures']=  []
		bus['cache']['materials']= []
		bus['cache']['displace']=  []

		bus['filter']= {} # TODO: Rename!
		bus['filter']['proxy']=    []
		bus['filter']['bitmap']=   []
		bus['filter']['texture']=  []
		bus['filter']['material']= []

		# Fake frame for "Camera loop"
		if VRayExporter.camera_loop:
			for key in bus['files']:
				if key in ('nodes','camera'):
					bus['files'][key].write("\n#time %.1f // %s\n" % (bus['camera_index'] + 1, bus['camera'].name))
		else:
			# Camera
			bus['camera']= scene.camera

		# Visibility list for "Hide from view" and "Camera loop" features
		bus['visibility']= get_visibility_lists(bus['camera'])

<<<<<<< HEAD
	ofile.write("\nSettingsOutput {")
	ofile.write("\n\timg_separateAlpha= %d;"%(0))
	ofile.write("\n\timg_width= %s;"%(int(wx)))
	if VRayScene.VRayBake.use:
		ofile.write("\n\timg_height= %s;"%(int(wx)))
	else:
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
		if hasattr(plugin,'write'):
			rna_pointer= getattr(VRayScene,plugin.PLUG)
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
		ofile.write("\n\tinterpolation_mode= %i;"%(INT_MODE[im.interpolation_mode]))
		ofile.write("\n\tlookup_mode= %i;"%(LOOK_TYPE[im.lookup_mode]))
		ofile.write("\n\tshow_calc_phase= %i;"%(im.show_calc_phase))
		ofile.write("\n\tshow_direct_light= %i;"%(im.show_direct_light))
		ofile.write("\n\tshow_samples= %i;"%(im.show_samples))
		ofile.write("\n\tmultipass= %i;"%(im.multipass))
		ofile.write("\n\tcheck_sample_visibility= %i;"%(im.check_sample_visibility))
		ofile.write("\n\trandomize_samples= %i;"%(im.randomize_samples))
		ofile.write("\n\tmode= %d;"%(IM_MODE[im.mode]))
		ofile.write("\n\tauto_save= %d;"%(im.auto_save))
		ofile.write("\n\tauto_save_file= \"%s\";"%(bpy.path.abspath(im.auto_save_file)))
		ofile.write("\n\tfile= \"%s\";"%(bpy.path.abspath(im.file)))
		ofile.write("\n\tdont_delete= false;")
		ofile.write("\n}\n")

		ofile.write("\nSettingsDMCGI {")
		ofile.write("\n\tsubdivs= %i;"%(bf.subdivs))
		ofile.write("\n\tdepth= %i;"%(bf.depth))
		ofile.write("\n}\n")

		ofile.write("\nSettingsLightCache {")
		ofile.write("\n\tsubdivs= %.0f;"%(lc.subdivs * dmc.subdivs_mult))
		ofile.write("\n\tsample_size= %.6f;"%(lc.sample_size))
		ofile.write("\n\tnum_passes= %i;"% (rd.threads if lc.num_passes_auto else lc.num_passes))
		ofile.write("\n\tdepth= %i;"%(lc.depth))
		ofile.write("\n\tfilter_type= %i;"%(LC_FILT[lc.filter_type]))
		ofile.write("\n\tfilter_samples= %i;"%(lc.filter_samples))
		ofile.write("\n\tfilter_size= %.6f;"%(lc.filter_size))
		ofile.write("\n\tprefilter= %i;"%(lc.prefilter))
		ofile.write("\n\tprefilter_samples= %i;"%(lc.prefilter_samples))
		ofile.write("\n\tshow_calc_phase= %i;"%(lc.show_calc_phase))
		ofile.write("\n\tstore_direct_light= %i;"%(lc.store_direct_light))
		ofile.write("\n\tuse_for_glossy_rays= %i;"%(lc.use_for_glossy_rays))
		ofile.write("\n\tworld_scale= %i;"%(SCALE[lc.world_scale]))
		ofile.write("\n\tadaptive_sampling= %i;"%(lc.adaptive_sampling))
		ofile.write("\n\tmode= %d;"%(LC_MODE[lc.mode]))
		ofile.write("\n\tauto_save= %d;"%(lc.auto_save))
		ofile.write("\n\tauto_save_file= \"%s\";"%(bpy.path.abspath(lc.auto_save_file)))
		ofile.write("\n\tfile= \"%s\";"%(bpy.path.abspath(lc.file)))
		ofile.write("\n\tretrace_enabled= %d;"%(lc.retrace_enabled))
		ofile.write("\n\tretrace_threshold= %.3f;"%(lc.retrace_threshold))
		ofile.write("\n\tdont_delete= false;")
		ofile.write("\n}\n")

	ofile.write("\nSettingsEXR {")
	ofile.write("\n\tcompression= 0;") # 0 - default, 1 - no compression, 2 - RLE, 3 - ZIPS, 4 - ZIP, 5 - PIZ, 6 - pxr24
	ofile.write("\n\tbits_per_channel= %d;" % (16 if rd.use_exr_half else 32))
	ofile.write("\n}\n")

	ofile.write("\nSettingsJPEG SettingsJPEG {")
	ofile.write("\n\tquality= %d;" % rd.file_quality)
	ofile.write("\n}\n")

	ofile.write("\nSettingsPNG SettingsPNG {")
	ofile.write("\n\tcompression= %d;" % int(rd.file_quality / 10))
	ofile.write("\n\tbits_per_channel= 16;")
	ofile.write("\n}\n")

	# ofile.write("\nRTEngine {")
	# ofile.write("\n\tseparate_window= 1;")
	# ofile.write("\n\ttrace_depth= 3;")
	# ofile.write("\n\tuse_gi= 1;")
	# ofile.write("\n\tgi_depth= 3;")
	# ofile.write("\n\tgi_reflective_caustics= 1;")
	# ofile.write("\n\tgi_refractive_caustics= 1;")
	# ofile.write("\n\tuse_opencl= 1;")
	# ofile.write("\n}\n")	

	for channel in VRayScene.render_channels:
		plugin= get_plugin(CHANNEL_PLUGINS, channel.type)
		if plugin:
			plugin.write(ofile, getattr(channel,plugin.PLUG), sce, channel.name)
=======
		# "Hide from view" debug data
		if VRayExporter.debug:
			print_dict(scene, "Hide from view", bus['visibility'])
>>>>>>> devel

		for ob in bus['objects']:
			if not object_visible(bus, ob):
				continue

			debug(scene, "{0}: {1:<32}".format(ob.type, color(ob.name, 'green')), VRayExporter.debug)

<<<<<<< HEAD
def write_scene(sce, bake= False):
	global mesh_lights

	# Reset mesh lights list
	mesh_lights= []
	
	VRayScene= sce.vray
	VRayExporter=    VRayScene.exporter
	SettingsOptions= VRayScene.SettingsOptions
=======
			# Node struct
			bus['node']= {}
>>>>>>> devel

			# Currently processes object
			bus['node']['object']= ob

			# Object visibility
			bus['node']['visible']= ob

			# We will know if object has displace
			# only after material export
			bus['node']['displace']= {}

<<<<<<< HEAD
	for key in files:
		files[key].write("// V-Ray/Blender %s\n" % VERSION)

	files['materials'].write("// Materials\n")
	files['materials'].write("\n// Default materials")
	files['materials'].write("\nUVWGenChannel UVWGenChannel_default {")
	files['materials'].write("\n\tuvw_channel= 1;")
	files['materials'].write("\n\tuvw_transform= Transform(")
	files['materials'].write("\n\t\tMatrix(")
	files['materials'].write("\n\t\t\tVector(1.0,0.0,0.0),")
	files['materials'].write("\n\t\t\tVector(0.0,1.0,0.0),")
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
	files['materials'].write("\n\ttexture= AColor(1.0,1.0,1.0,1.0);")
	files['materials'].write("\n}\n")
	files['materials'].write("\n// Scene materials\n")
	files['nodes'].write("// Nodes\n")
	files['lamps'].write("// Lights\n")
	files['camera'].write("// Camera & Environment\n")

	def _write_object_particles(ob, params, add_params= None):
		if len(ob.particle_systems):
			for ps in ob.particle_systems:
				ps_material= "Material_no_material"
				ps_material_idx= ps.settings.material
				if ps_material_idx <= len(ob.material_slots):
					ps_material= get_name(ob.material_slots[ps_material_idx - 1].material, "Material")

				if ps.settings.type == 'HAIR' and ps.settings.render_type == 'PATH':
					if VRayExporter.use_hair:
						hair_geom_name= "HAIR_%s" % ps.name
						hair_node_name= "%s_%s" % (ob.name,hair_geom_name)

						write_GeomMayaHair(params['files']['nodes'],ob,ps,hair_geom_name)
						write_node(params['files']['nodes'], hair_node_name, hair_geom_name, ps_material, ob.pass_index, True, ob.matrix_world, ob, params)
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
							location= particle.hair[0].co
							size*= 3

						part_transform= mathutils.Matrix.Scale(size, 3) * particle.rotation.to_matrix()
						part_transform.resize_4x4()
						part_transform[3][0]= location[0]
						part_transform[3][1]= location[1]
						part_transform[3][2]= location[2]

						for p_ob in particle_objects:
							part_name= "PS%sPA%s" % (clean_string(ps.name), p)
							if add_params is not None:
								if 'dupli_name' in add_params:
									part_name= '_'.join([add_params['dupli_name'],clean_string(ps.name),str(p)])
									
							if ps.settings.use_whole_group or ps.settings.use_global_dupli:
								part_transform= part_transform * p_ob.matrix_world

							part_visibility= True
							if ps.settings.type == 'EMITTER':
								part_visibility= True if particle.alive_state not in ('DEAD','UNBORN') else False

							_write_object(p_ob, params, {'dupli': True,
														 'dupli_name': part_name,
														 'visible': part_visibility,
														 'material': ps_material,
														 'matrix': part_transform})

	def _write_object_dupli(ob, params, add_params= None):
		if ob.dupli_type in ('VERTS','FACES','GROUP'):
			ob.create_dupli_list(sce)
			for dup_id,dup_ob in enumerate(ob.dupli_list):
				dup_name= "%s_%s" % (ob.name,dup_id)
				if ob.pass_index:
					params['objectID']= ob.pass_index
				_write_object(dup_ob.object, params, {'dupli': True,
													  'dupli_name': dup_name,
													  'matrix': dup_ob.matrix})
				if 'objectID' in params:
					del params['objectID']
			ob.free_dupli_list()

	def _write_object(ob, params, add_params= None):
		if ob.type in ('CAMERA','ARMATURE','LATTICE'):
			return
		if ob.type == 'LAMP':
			write_lamp(ob,params,add_params)
		elif ob.type == 'EMPTY':
			_write_object_dupli(ob,params,add_params)
		else:
			_write_object_particles(ob,params,add_params)
			_write_object_dupli(ob,params,add_params)
			write_object(ob,params,add_params)

	def write_frame(camera= None):
		params= {
			'scene': sce,
			'camera': camera,
			'files': files,
			'filters': {
				'exported_bitmaps':   [],
				'exported_textures':  [],
				'exported_materials': [],
				'exported_proxy':     [],
			},
			'types': types,
			'uv_ids': get_uv_layers(sce),
		}

		if camera:
			VRayCamera= ca.data.vray

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
							visibility[hide_type]= generate_object_list(group_names_string= 'hf_%s' % ca.name)
						else:
							visibility[hide_type]= generate_object_list(getattr(VRayCamera, 'hf_%s_objects' % hide_type), getattr(VRayCamera, 'hf_%s_groups' % hide_type))

			params['visibility']= visibility
			debug(sce, "Hide from view: %s" %  visibility)

		write_environment(params['files']['camera'])
		write_camera(sce,params['files']['camera'],bake= bake)

		for ob in sce.objects:
			if ob.type in ('CAMERA','ARMATURE','LATTICE'):
				continue

			if VRayExporter.active_layers:
				if not object_on_visible_layers(sce,ob):
					if not SettingsOptions.geom_doHidden:
						continue
				
			if ob.hide_render:
				if not SettingsOptions.geom_doHidden:
					continue

			for slot in ob.material_slots:
				if slot.material:
					VRayMaterial= slot.material.vray
					if VRayMaterial.type == 'EMIT' and VRayMaterial.emitter_type == 'MESH':
						node_name= get_name(ob,"Node")
						if node_name not in mesh_lights:
							mesh_lights.append(node_name)


		for ob in sce.objects:
			if ob.type in ('CAMERA','ARMATURE','LATTICE'):
				continue

			if VRayExporter.active_layers:
				if not object_on_visible_layers(sce,ob):
					if ob.type == 'LAMP':
						if VRayScene.use_hidden_lights:
							pass
					elif SettingsOptions.geom_doHidden:
						pass
					else:
						continue

			if ob.hide_render:
				if ob.type == 'LAMP':
					if not VRayScene.use_hidden_lights:
						continue
				else:
					if not SettingsOptions.geom_doHidden:
						continue
		
			debug(sce,"[%s]: %s"%(ob.type,ob.name))
			debug(sce,"  Animated: %d"%(1 if ob.animation_data else 0))
			if hasattr(ob,'data'):
				if ob.data:
					debug(sce,"  Data animated: %d"%(1 if ob.data.animation_data else 0))
			if not VRayExporter.debug:
				if PLATFORM == "linux2":
					sys.stdout.write("V-Ray/Blender: [%d] %s: \033[0;32m%s\033[0m                              \r"%(sce.frame_current, ob.type, ob.name))
				else:
					sys.stdout.write("V-Ray/Blender: [%d] %s: %s                              \r"%(sce.frame_current, ob.type, ob.name))
				sys.stdout.flush()
=======
			# We will know if object is mesh light
			# only after material export
			bus['node']['meshlight']= {}

			# If object has particles or dupli
			bus['node']['base']= ob
			bus['node']['dupli']= {}
			bus['node']['particle']= {}

			_write_object(bus)
>>>>>>> devel

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
			if bus['cameras']:
				for i,camera in enumerate(bus['cameras']):
					bus['camera']= camera
					bus['camera_index']= i
					write_frame(bus)
			else:
				debug(scene, "No cameras selected for \"Camera loop\"!", error= True)
				return True # Error
		else:
<<<<<<< HEAD
			_create_proxy(context.object)

		debug(context.scene, "Proxy generation total time: %.2f\n" % (time.clock() - timer))

		return{'FINISHED'}

bpy.utils.register_class(VRAY_OT_create_proxy)


class VRAY_OT_write_geometry(bpy.types.Operator):
	bl_idname      = "vray.write_geometry"
	bl_label       = "Export meshes"
	bl_description = "Export meshes."

	def execute(self, context):
		write_geometry(context.scene)
		return{'FINISHED'}
=======
			write_frame(bus)
		
	write_settings(bus)

	debug(scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))

	return False # No errors
>>>>>>> devel

bpy.utils.register_class(VRAY_OT_write_geometry)


def run(engine, bus):
	scene= bus['scene']

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR

	vray_exporter=   get_vray_exporter_path()
	vray_standalone= get_vray_standalone_path(scene)

	resolution_x= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	resolution_y= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

<<<<<<< HEAD
		if ve.auto_meshes:
			write_geometry(sce)
		
		write_scene(sce, bake= VRayBake.use)
=======
	params= []
	params.append(vray_standalone)

	params.append('-sceneFile=')
	params.append(bus['filenames']['scene'])
>>>>>>> devel

	if not scene.render.threads_mode == 'AUTO':
		params.append('-numThreads=')
		params.append(str(scene.render.threads))

	if bus['preview']:
		preview_file=     os.path.join(tempfile.gettempdir(), "preview.jpg")
		preview_loadfile= os.path.join(tempfile.gettempdir(), "preview.0000.jpg")

		params.append('-imgFile=')
		params.append(preview_file)
		params.append('-showProgress=')
		params.append('0')
		params.append('-display=')
		params.append('0')
		params.append('-autoclose=')
		params.append('1')
		params.append('-verboseLevel=')
		params.append('0')

	else:
		params.append('-verboseLevel=')
		params.append(VRayExporter.verboseLevel)

		if scene.render.use_border:
			x0= resolution_x * scene.render.border_min_x
			y0= resolution_y * (1.0 - scene.render.border_max_y)
			x1= resolution_x * scene.render.border_max_x
			y1= resolution_y * (1.0 - scene.render.border_min_y)

			if scene.render.use_crop_to_border:
				params.append('-crop=')
			else:
				params.append('-region=')
			params.append("%i;%i;%i;%i" % (x0,y0,x1,y1))

		params.append('-frames=')
		if VRayExporter.animation:
			params.append("%d-%d,%d"%(scene.frame_start, scene.frame_end,int(scene.frame_step)))
		elif VRayExporter.camera_loop:
			if bus['cameras']:
				params.append("1-%d,1" % len(bus['cameras']))
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
				params.append('-include=')
				params.append("\"%s\"" % (bus['filenames']['DR']['shared_dir'] + os.sep))

		if VRayExporter.auto_save_render or VRayExporter.image_to_blender:
			image_file= os.path.join(bus['filenames']['output'], bus['filenames']['output_filename'])
			
			params.append('-imgFile=')
			params.append(image_file)

		params.append('-display=')
		params.append(str(int(VRayExporter.display)))

		if VRayExporter.image_to_blender:
			params.append('-autoclose=')
			params.append('1')

<<<<<<< HEAD
			if not ve.animation and ve.image_to_blender:
				while True:
					if self.test_break():
						try:
							process.kill()
						except:
							pass
						break

					if process.poll() is not None:
						try:
							result= self.begin_result(0, 0, int(wx), int(wy))
							result.layers[0].load_from_file(load_file)
							self.end_result(result)
						except:
							pass
						break

					time.sleep(0.05)
		else:
			print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")
			print("V-Ray/Blender: Command: %s" % ' '.join(params))
=======
	if PLATFORM == "linux2":
		if VRayExporter.log_window:
			log_window= []
			log_window.append("xterm")
			log_window.append("-T")
			log_window.append("VRAYSTANDALONE")
			log_window.append("-geometry")
			log_window.append("90x10")
			log_window.append("-e")
			log_window.extend(params)
			params= log_window

	# if PLATFORM == "win32":
	# 	win_belownormal= []
	# 	win_belownormal.append("start")
	# 	win_belownormal.append("\"VRAYSTANDALONE\"")
	# 	win_belownormal.append("/B")
	# 	win_belownormal.append("/BELOWNORMAL")
	# 	win_belownormal.append("\"%s\"" % params[0])
	# 	win_belownormal.extend(params[1:])

	if not VRayExporter.autorun:
		debug(scene, "Command: %s" % ' '.join(params))

	if VRayExporter.autorun:
		process= subprocess.Popen(params)

		if bus['preview'] or VRayExporter.image_to_blender:
			load_file= preview_loadfile if bus['preview'] else os.path.join(bus['filenames']['output'], bus['filenames']['output_loadfile'])
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
>>>>>>> devel

	else:
		debug(scene, "Enable \"Autorun\" option to start V-Ray automatically after export.")
	

def render(engine, scene, preview= None):
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter

	# Settings bus
	bus= {}

	# Plugins
	bus['plugins']= PLUGINS

	# Scene
	bus['scene']= scene

	# Preview
	bus['preview']= preview
	
	# V-Ray uses UV indexes, Blender uses UV names
	# Here we store UV name->index map
	bus['uvs']= get_uv_layers_map(scene)

	# Output files
	bus['files']=     {}
	bus['filenames']= {}

	init_files(bus)

	# Camera loop
	bus['cameras']= [ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]

	if preview:
		write_geometry_python(bus)
	else:
		if VRayExporter.auto_meshes:
			write_geometry(bus)

<<<<<<< HEAD
			if not ve.animation and ve.image_to_blender or sce.name == "preview":
				while True:
					if self.test_break():
						try:
							process.kill()
						except:
							pass
						break

					if process.poll() is not None:
						try:
							result= self.begin_result(0, 0, wx, wy)
							layer= result.layers[0]
							layer.load_from_file(load_file)
							self.end_result(result)
						except:
							pass
						break

					time.sleep(0.05)
		else:
			print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")
			print("V-Ray/Blender: Command: %s" % ' '.join(params))


bpy.utils.register_class(VRayRenderer)
bpy.utils.register_class(VRayRendererPreview)

=======
	err= write_scene(bus)

	for key in bus['files']:
		bus['files'][key].write("\n// vim: set syntax=on syntax=c:\n\n")
		bus['files'][key].close()

	if not err:
		run(engine, bus)

	del bus
>>>>>>> devel

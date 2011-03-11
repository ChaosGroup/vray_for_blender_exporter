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
from vb25.utils   import *
from vb25.plugins import *
from vb25.texture import *

''' vb dev modules '''
from vb25.nodes import *


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

# Material
# bus['material']['material']= *material

# If some texture need object mapping then material become object dependent
# bus['material']['orco']= bool

# BRDFBump nomal mapping uvwgen
# bus['material']['normal_uvwgen']= string

# Texture stack
# bus['material']['textures']= {}

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

		for ob in scene.objects:
			if ob.type in ('LAMP','CAMERA','ARMATURE','LATTICE','EMPTY'):
				continue

			# Skip proxy meshes
			if hasattr(ob.data, 'GeomMeshFile') and ob.data.vray.GeomMeshFile.use:
				continue

			if VRayExporter.mesh_active_layers or bus['preview']:
				if not object_on_visible_layers(scene,ob):
					continue

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

	del bus['files']['geometry']
	
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

	except:
		# Use python mesh export
		write_geometry_python(bus)


def write_GeomMayaHair(bus, ps, hair_geom_name):
	scene= bus['scene']
	ofile= bus['files']['nodes']
	ob=    bus['node']['object']

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

	ofile.write("\nGeomMayaHair %s {" % hair_geom_name)
	ofile.write("\n\tnum_hair_vertices= interpolate((%d,ListInt(%s)));"%(scene.frame_current, ','.join(num_hair_vertices)))
	ofile.write("\n\thair_vertices= interpolate((%d,ListVector(%s)));"%(scene.frame_current,  ','.join(hair_vertices)))
	ofile.write("\n\twidths= interpolate((%d,ListFloat(%s)));"%(scene.frame_current,          ','.join(widths)))
	ofile.write("\n}\n")



'''
  SETTINGS
'''
def write_settings(bus):
	ofile= bus['files']['scene']
	scene= bus['scene']
	
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR

	for key in bus['filenames']:
		if key in ('output', 'lightmaps', 'scene'):
			# Skip paths and some files
			continue

		if key == 'geometry':
			if bus['preview']:
				ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames']['geometry']))
			else:
				for t in range(scene.render.threads):
					ofile.write("\n#include \"%s_%.2i.vrscene\"" % (os.path.basename(bus['filenames']['geometry'][:-11]), t))
			continue

		if VRayDR.on: # TODO: fix & improve
			if VRayDR.type == 'UU':
				ofile.write("\n#include \"%s\"" % bus['filenames'][key])

			elif VRayDR.type == 'WU':
				ofile.write("\n#include \"%s\"" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),
																os.path.split(bpy.data.filepath)[1][:-6],
																os.path.basename(bus['filenames'][key]))))

			else:
				ofile.write("\n#include \"%s\"" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),
																os.path.split(bpy.data.filepath)[1][:-6],
																os.path.basename(bus['filenames'][key]))))

		else:
			ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames'][key]))

	ofile.write("\n")

	wx= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	wy= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)
	
	ofile.write("\nSettingsOutput SettingsOutput {")
	ofile.write("\n\timg_noAlpha= %d;" % (0))
	ofile.write("\n\timg_width= %s;" % wx)
	ofile.write("\n\timg_height= %s;" % (wx if VRayScene.VRayBake.use else wy))
	if VRayExporter.animation:
		ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(scene.camera.name),get_render_file_format(VRayExporter,scene.render.file_format)))
		ofile.write("\n\timg_dir= \"%s\";" % bus['filenames']['output'])
		ofile.write("\n\timg_file_needFrameNumber= 1;")
		ofile.write("\n\tanim_start= %d;"%(scene.frame_start))
		ofile.write("\n\tanim_end= %d;"%(scene.frame_end))
		ofile.write("\n\tframe_start= %d;"%(scene.frame_start))
		ofile.write("\n\tframes_per_second= %d;"%(1.0) )
		ofile.write("\n\tframes= %d-%d;"%(scene.frame_start, scene.frame_end))
	ofile.write("\n\tframe_stamp_enabled= %d;"%(0))
	ofile.write("\n\tframe_stamp_text= \"%s\";" % ("V-Ray/Blender 2.0 | V-Ray Standalone %%vraycore | %%rendertime"))
	ofile.write("\n}\n")

	COMPRESSION= {
		'NONE':  1,
		'PXR24': 6,
		'ZIP':   4,
		'PIZ':   5,
		'RLE':   2,
	}
	ofile.write("\nSettingsEXR SettingsEXR {")
	ofile.write("\n\tcompression= %i;" % COMPRESSION[scene.render.exr_codec])
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
		if key not in ('BakeView', 'RenderView'):
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
		bus['files']['scene'].write("\n\tsubdivs_mult= 0.2;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsOptions {")
		bus['files']['scene'].write("\n\tmtl_limitDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_maxDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_transpMaxLevels= 10;")
		bus['files']['scene'].write("\n\tmtl_transpCutoff= 0.1;")
		bus['files']['scene'].write("\n\tmtl_override_on= 0;")
		bus['files']['scene'].write("\n\tmtl_glossy= 1;")
		bus['files']['scene'].write("\n\tmisc_lowThreadPriority= 1;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsImageSampler {")
		bus['files']['scene'].write("\n\ttype= 0;")
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

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter

	la= ob.data
	VRayLamp= la.vray

	defaults= {
		'color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(la.color)),               0, 'NONE'),
		'intensity':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([VRayLamp.intensity]*3)), 0, 'NONE'),
		'shadowColor': (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(VRayLamp.shadowColor)),   0, 'NONE'),
	}

	bus['lamp_textures']= {
		'mapto': {},
	}
	
	for i,slot in enumerate(la.texture_slots):
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
					if key not in bus['lamp_textures']: # First texture
						bus['lamp_textures'][key]= []
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
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

					bus['lamp_textures'][key].append( (write_factor(bus),
													   slot.use_stencil,
													   VRaySlot.blend_mode) )
	if VRayExporter.debug:
		if len(bus['lamp_textures']):
			debug(scene, "Lamp \"%s\" texture stack: %s" % (la.name,bus['lamp_textures']))
	
	for key in bus['lamp_textures']:
		if len(bus['lamp_textures'][key]):
			bus['lamp_textures'][key]= write_TexOutput(bus, stack_write_textures(bus, stack_collapse_layers(bus['lamp_textures'][key])), key)

	return bus['lamp_textures']


def write_material_textures(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ma=    bus['material']

	VRayScene=    scene.vray
	VRayMaterial= ma.vray

	VRayExporter= VRayScene.exporter

	mapped_params= PLUGINS['BRDF'][VRayMaterial.type].get_defaults(bus)

	# Mapped parameters
	bus['textures']= {}

	# Displace settings pointer
	bus['node']['displace']= None

	# Normal mapping settings pointer and uvwgen
	bus['normal']=        None
	bus['normal_uvwgen']= None

	for i,slot in enumerate(ma.texture_slots):
		if ma.use_textures[i] and slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot= slot.texture.vray_slot

			for key in mapped_params:
				if getattr(VRaySlot, 'map_'+key):
					factor= getattr(VRaySlot, key+'_mult')
					
					if key not in bus['textures']: # If texture is first in stack
						bus['textures'][key]= []
						# If this texture will be blended over some value
						# we need to add this value
						# (for example, texture blended over diffuse color)
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
							bus['textures'][key].append(mapped_params[key])

					if key == 'displacement':
						bus['node']['displacement']['slot']= slot

					elif key == 'normal':
						bus['normal']['slot']= slot

					bus['mtex']= {}
					bus['mtex']['mapto']=   key
					bus['mtex']['slot']=    slot
					bus['mtex']['texture']= slot.texture
					bus['mtex']['factor']=  factor
					bus['mtex']['name']=    clean_string("MT%.2iSL%sTE%s" % (i,
																			 slot.name,
																			 slot.texture.name))
					# Write texture
					write_texture(bus)

					# Append texture to stack and write texture with factor
					bus['textures'][key].append( (write_factor(bus),
												  slot.use_stencil,
												  VRaySlot.blend_mode) )

	if VRayExporter.debug:
		if len(bus['textures']):
			print_dict(scene, "Material \"%s\" texture stack" % ma.name, bus['textures'])
	
	for key in bus['textures']:
		if len(bus['textures'][key]):
			bus['textures'][key]= write_TexOutput(bus, stack_write_textures(bus, stack_collapse_layers(bus['textures'][key])), key)

	if 'displacement' in bus['textures']:
		bus['node']['displacement']['texture']= bus['textures']['displacement']


	return bus['textures']


def	write_material(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']
	ob=    bus['node']['object']

	ma=    bus['material']

	VRayMaterial= ma.vray

	ma_name= get_name(ma, prefix='MA')

	# TODO: don't cache when Object mapping is used in any texture
	if ma_name in bus['cache']['materials']:
		return ma_name
	bus['cache']['materials'].append(ma_name)
	
	# Write material textures
	write_material_textures(bus)

	# Write material BRDF
	PLUGINS['BRDF'][VRayMaterial.type].write(bus)

	# Add BRDFBump if needed
	PLUGINS['BRDF']['BRDFBump'].write(bus)

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
	ofile.write("\n\tbrdf= %s;" % a(scene, bus['brdf']))
	ofile.write("\n}\n")

	if VRayMaterial.Mtl2Sided.use:
		base_material= complex_material.pop()
		ofile.write("\nMtl2Sided %s {"%(complex_material[-1]))
		ofile.write("\n\tfront= %s;"%(base_material))
		back= base_material
		if VRayMaterial.Mtl2Sided.back:
			if VRayMaterial.Mtl2Sided.back in bpy.data.materials:
				back= get_name(bpy.data.materials[VRayMaterial.Mtl2Sided.back],"Material")
		ofile.write("\n\tback= %s;"%(back))

		if VRayMaterial.Mtl2Sided.control == 'SLIDER':
			ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))
		elif VRayMaterial.Mtl2Sided.control == 'COLOR':
			ofile.write("\n\ttranslucency= %s;" % a(scene, VRayMaterial.Mtl2Sided.translucency_color))
		else:
			if VRayMaterial.Mtl2Sided.translucency_tex:
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

	# Multi-material name
	mtl_name= get_name(ob, prefix='MA')

	# Collecting and exporting object materials
	mtls_list= []
	ids_list=  []
	ma_id= 0 # For cases with empty slots
	if len(ob.material_slots):
		for slot in ob.material_slots:
			ma= slot.material
			if ma:
				bus['material']= ma

				# Node material
				if scene.vray.exporter.use_material_nodes and ma.use_nodes:
					debug(scene,"Node materials temporarily disabled...")
					#mtls_list.append(write_node_material(params))
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

	textures= write_lamp_textures(bus)['mapto']

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
			ofile.write("\n\t%s= \"%s\";"%(param,get_full_filepath(scene,lamp,VRayLamp.ies_file)))
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

	node_name= bus['node']['name']
	matrix=    bus['node']['matrix']
	base_mtl=  bus['node']['material']

	if SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
		material= get_name(bpy.data.materials[SettingsOptions.mtl_override], prefix='MA')

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

	# Write object materials
	write_materials(bus)

	# VRayProxy
	PLUGINS['GEOMETRY']['GeomMeshFile'].write(bus)

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

	write_node(bus)


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

	for key in bus['files']:
		bus['files'][key].write("// V-Ray/Blender %s" % VERSION)

	bus['files']['scene'].write("\n// Settings\n")
	bus['files']['nodes'].write("\n// Nodes\n")
	bus['files']['lights'].write("\n// Lights\n")
	bus['files']['camera'].write("\n// Camera\n")
	bus['files']['environment'].write("\n// Environment\n")
	bus['files']['materials'].write("\n// Materials\n")
	bus['files']['textures'].write("\n// Textures\n")

	bus['files']['materials'].write("\n// Useful defaults")
	bus['files']['materials'].write("\nUVWGenChannel DEFAULTUVWC {")
	bus['files']['materials'].write("\n\tuvw_channel= 1;")
	bus['files']['materials'].write("\n\tuvw_transform= Transform(Matrix(Vector(1.0,0.0,0.0),Vector(0.0,1.0,0.0),Vector(0.0,0.0,1.0)),Vector(0.0,0.0,0.0));")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nTexChecker %s {" % bus['defaults']['texture'])
	bus['files']['materials'].write("\n\tuvwgen= DEFAULTUVWC;")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nBRDFDiffuse %s {" % bus['defaults']['brdf'])
	bus['files']['materials'].write("\n\tcolor=Color(0.5,0.5,0.5);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nMtlSingleBRDF %s {" % bus['defaults']['material'])
	bus['files']['materials'].write("\n\tbrdf= BRDFNOBRDFISSET;")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nTexAColor TEDefaultBlend {")
	bus['files']['materials'].write("\n\tuvwgen= DEFAULTUVWC;")
	bus['files']['materials'].write("\n\ttexture= AColor(1.0,1.0,1.0,1.0);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\n// Scene materials")

	if bus['preview']:
		bus['files']['lights'].write("\nLightDirectMax LALamp_008 {")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tunits= 0;")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.001000;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tdiffuse_contribution= 1.000000;")
		bus['files']['lights'].write("\n\tspecular_contribution= 1.000000;")
		bus['files']['lights'].write("\n\tintensity= 3.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tfallsize= 100.000000;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\tMatrix(")
		bus['files']['lights'].write("\n\tVector(1.000000, 0.000000, -0.000000),")
		bus['files']['lights'].write("\n\tVector(0.000000, 0.000000, 1.000000),")
		bus['files']['lights'].write("\n\tVector(0.000000, -1.000000, 0.000000)")
		bus['files']['lights'].write("\n\t),")
		bus['files']['lights'].write("\n\tVector(1.471056, -14.735638, 3.274598));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp {")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tunits= 0;")
		bus['files']['lights'].write("\n\tenabled= 1;")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.001000;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tspecular_contribution= 0.000000;")
		bus['files']['lights'].write("\n\tintensity= 150.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 4;")
		bus['files']['lights'].write("\n\tdecay= 2.000000;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\tMatrix(")
		bus['files']['lights'].write("\n\tVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\n\tVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\n\tVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n\t),")
		bus['files']['lights'].write("\n\tVector(15.685226, -7.460007, 2.990525));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightSpot LALamp_002 {")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tunits= 0;")
		bus['files']['lights'].write("\n\tconeAngle= 0.872665;")
		bus['files']['lights'].write("\n\tpenumbraAngle= -0.465689;")
		bus['files']['lights'].write("\n\tenabled= 1;")
		bus['files']['lights'].write("\n\tshadows= 1;")
		bus['files']['lights'].write("\n\tshadowColor= Color(0.000,0.000,0.000);")
		bus['files']['lights'].write("\n\tshadowBias= 0.000000;")
		bus['files']['lights'].write("\n\tcausticSubdivs= 1000;")
		bus['files']['lights'].write("\n\tcausticMult= 1.000000;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.001000;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 1;")
		bus['files']['lights'].write("\n\tbumped_below_surface_check= 0;")
		bus['files']['lights'].write("\n\tnsamples= 0;")
		bus['files']['lights'].write("\n\tdiffuse_contribution= 1.000000;")
		bus['files']['lights'].write("\n\tspecular_contribution= 1.000000;")
		bus['files']['lights'].write("\n\tintensity= 30.000000;")
		bus['files']['lights'].write("\n\tshadowRadius= 0.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 8;")
		bus['files']['lights'].write("\n\tdecay= 2.000000;")
		bus['files']['lights'].write("\ntransform= Transform(")
		bus['files']['lights'].write("\nMatrix(")
		bus['files']['lights'].write("\nVector(-0.549843, 0.655945, 0.517116),")
		bus['files']['lights'].write("\nVector(-0.733248, -0.082559, -0.674931),")
		bus['files']['lights'].write("\nVector(-0.400025, -0.750280, 0.526365)")
		bus['files']['lights'].write("\n),")
		bus['files']['lights'].write("\nVector(-5.725639, -13.646054, 8.475835));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp_001 {")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tunits= 0;")
		bus['files']['lights'].write("\n\tenabled= 1;")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.001000;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 1;")
		bus['files']['lights'].write("\n\tbumped_below_surface_check= 0;")
		bus['files']['lights'].write("\n\tnsamples= 0;")
		bus['files']['lights'].write("\n\tspecular_contribution= 1.000000;")
		bus['files']['lights'].write("\n\tintensity= 300.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 8;")
		bus['files']['lights'].write("\n\tdecay= 2.000000;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\nMatrix(")
		bus['files']['lights'].write("\nVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\nVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\nVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n),")
		bus['files']['lights'].write("\nVector(-10.500286, -12.464991, 3.075305));")
		bus['files']['lights'].write("\n}\n")

	# Processed objects
	bus['objects']= []

	bus['effects']= {}
	bus['effects']['fog']= []
	bus['effects']['toon']= []

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

		VRayScene=       scene.vray

		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		# Cache stores already exported data
		bus['cache']= {}
		bus['cache']['textures']= []
		bus['cache']['materials']= []

		bus['filter']= {} # TODO: Rename!
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

		for ob in bus['objects']:
			if not object_visible(bus, ob):
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

	debug(scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))


def run(engine, bus):
	scene= bus['scene']

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
	params.append(bus['filenames']['scene'])

	params.append('-numThreads=')
	params.append(str(scene.render.threads))

	if bus['preview']:
		preview_file= os.path.join(tempfile.gettempdir(), "preview.jpg")

		params.append('-imgFile=')
		params.append(preview_file)
		params.append('-display=')
		params.append('0')
		params.append('-autoclose=')
		params.append('1')
		params.append('-showProgress=')
		params.append('0')

	else:
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
			image_file= os.path.join(bus['filenames']['output'],
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

			if bus['preview'] or (VRayExporter.image_to_blender and VRayExporter.use_render_operator):
				load_file= preview_file if bus['preview'] else os.path.join(bus['filenames']['output'],
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

	if preview:
		write_geometry_python(bus)
	else:
		if VRayExporter.auto_meshes:
			write_geometry(bus)

	write_scene(bus)

	for key in bus['files']:
		bus['files'][key].write("\n// vim: set syntax=on syntax=c:\n\n")
		bus['files'][key].close()

	run(engine, bus)

	del bus

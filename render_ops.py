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
from vb25.plugins import *
from vb25.shaders import *
from vb25.proxy import *
from vb25.render import *


VERSION= '2.5.10'


class VRAY_OT_create_proxy(bpy.types.Operator):
	bl_idname      = "vray.create_proxy"
	bl_label       = "Create proxy"
	bl_description = "Creates proxy from selection."

	def execute(self, context):
		sce= context.scene

		def _create_proxy(ob):
			if ob.type in ('LAMP','CAMERA','ARMATURE','LATTICE','EMPTY'):
				return

			timer= time.clock()

			GeomMeshFile= ob.data.vray.GeomMeshFile

			vrmesh_filename= GeomMeshFile.filename if GeomMeshFile.filename else clean_string(ob.name)
			vrmesh_filename+= ".vrmesh"

			vrmesh_dirpath= bpy.path.abspath(GeomMeshFile.dirpath)
			if not os.path.exists(vrmesh_dirpath):
				os.mkdir(vrmesh_dirpath)
			vrmesh_filepath= os.path.join(vrmesh_dirpath,vrmesh_filename)

			if GeomMeshFile.animation:
				selected_frame= sce.frame_current

				frame_start= sce.frame_start
				frame_end= sce.frame_end
				if GeomMeshFile.animation_range == 'MANUAL':
					frame_start= GeomMeshFile.frame_start
					frame_end= GeomMeshFile.frame_end

				# Export first frame to create file
				frame= frame_start
				sce.frame_set(frame)
				generate_proxy(sce,ob,vrmesh_filepath)
				frame+= 1
				# Export all other frames
				while(frame <= frame_end):
					sce.frame_set(frame)
					generate_proxy(sce,ob,vrmesh_filepath,append=True)
					frame+= 1
				sce.frame_set(selected_frame)
			else:
				generate_proxy(sce,ob,vrmesh_filepath)

			ob_name= ob.name
			ob_data_name= ob.data.name

			if GeomMeshFile.mode != 'NONE':
				if GeomMeshFile.mode in ('THIS','REPLACE'):
					if GeomMeshFile.add_suffix:
						ob.name+= '_proxy'
						ob.data.name+= '_proxy'

				if GeomMeshFile.mode == 'THIS':
					GeomMeshFile.use= True
					GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)

				bbox_faces= ((0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7))
				bbox_mesh= bpy.data.meshes.new(ob_data_name+'_proxy')
				bbox_mesh.from_pydata(ob.bound_box, [], bbox_faces)
				bbox_mesh.update()

				if GeomMeshFile.mode in ('NEW','REPLACE'):
					for slot in ob.material_slots:
						if slot and slot.material:
							bbox_mesh.materials.append(slot.material)

				if GeomMeshFile.mode == 'NEW':
					new_ob= bpy.data.objects.new(ob_name+'_proxy', bbox_mesh)
					sce.objects.link(new_ob)
					new_ob.matrix_world= ob.matrix_world
					new_ob.draw_type= 'WIRE'
					bpy.ops.object.select_all(action='DESELECT')
					new_ob.select= True
					sce.objects.active= new_ob

					if GeomMeshFile.apply_transforms:
						ob.select= True
						sce.objects.active= ob
						bpy.ops.object.scale_apply()
						bpy.ops.object.rotation_apply()
						bpy.ops.object.location_apply()

					GeomMeshFile= new_ob.data.vray.GeomMeshFile
					GeomMeshFile.use= True
					GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)

				elif GeomMeshFile.mode == 'REPLACE':
					original_mesh= ob.data

					ob.data= bbox_mesh
					ob.draw_type= 'WIRE'
					for md in ob.modifiers: ob.modifiers.remove(md)

					if GeomMeshFile.apply_transforms:
						ob.select= True
						sce.objects.active= ob
						bpy.ops.object.scale_apply()
						bpy.ops.object.rotation_apply()
						bpy.ops.object.location_apply()

					GeomMeshFile= ob.data.vray.GeomMeshFile
					GeomMeshFile.use= True
					GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)

					bpy.data.meshes.remove(original_mesh)
			debug(context.scene, "Proxy generation total time: %.2f\n" % (time.clock() - timer))

		if len(bpy.context.selected_objects):
			for ob in bpy.context.selected_objects:
				_create_proxy(ob)
		else:
			_create_proxy(context.object)

		return{'FINISHED'}


class VRAY_OT_write_scene(bpy.types.Operator):
	bl_idname      = "vray.write_scene"
	bl_label       = "Export scene"
	bl_description = "Export scene to \"vrscene\" file."

	preview= bpy.props.BoolProperty(
		name= "Preview",
		description= "Write material preview scene.",
		default= False
	)

	scene=  None
	camera= None

	EnvironmentFog= []
	VolumeVRayToon= []

	def write_settings(self):
		VRayScene=    self.scene.vray
		VRayExporter= VRayScene.exporter
		VRayDR=       VRayScene.VRayDR

		ofile= open(get_filenames(self.scene,'scene'), 'w')
		
		ofile.write("// V-Ray/Blender %s\n" % VERSION)
		ofile.write("// Settings\n\n")

		for f in ('materials', 'lights', 'nodes', 'camera'):
			if VRayDR.on:
				if VRayDR.type == 'UU':
					ofile.write("#include \"%s\"\n" % get_filenames(self.scene,f))
				elif VRayDR.type == 'WU':
					ofile.write("#include \"%s\"\n" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),os.path.split(bpy.data.filepath)[1][:-6],os.path.basename(get_filenames(self.scene,f)))))
				else:
					ofile.write("#include \"%s\"\n" % (os.path.join(os.path.normpath(bpy.path.abspath(VRayDR.shared_dir)),os.path.split(bpy.data.filepath)[1][:-6],os.path.basename(get_filenames(self.scene,f)))))
			else:
				ofile.write("#include \"%s\"\n"%(os.path.basename(get_filenames(self.scene,f))))

		for t in range(self.scene.render.threads):
			ofile.write("#include \"%s_%.2i.vrscene\"\n" % (os.path.basename(get_filenames(self.scene,'geometry'))[:-11], t))

		wx= int(self.scene.render.resolution_x * self.scene.render.resolution_percentage / 100)
		wy= int(self.scene.render.resolution_y * self.scene.render.resolution_percentage / 100)

		ofile.write("\nSettingsOutput {")
		ofile.write("\n\timg_separateAlpha= %d;"%(0))
		ofile.write("\n\timg_width= %s;" % wx)
		if VRayScene.VRayBake.use:
			ofile.write("\n\timg_height= %s;" % wx)
		else:
			ofile.write("\n\timg_height= %s;" % wy)
		if VRayExporter.animation:
			ofile.write("\n\timg_file= \"render_%s.%s\";" % (clean_string(self.scene.camera.name),get_render_file_format(VRayExporter,self.scene.render.file_format)))
			ofile.write("\n\timg_dir= \"%s\";"%(get_filenames(self.scene,'output')))
			ofile.write("\n\timg_file_needFrameNumber= 1;")
			ofile.write("\n\tanim_start= %d;"%(self.scene.frame_start))
			ofile.write("\n\tanim_end= %d;"%(self.scene.frame_end))
			ofile.write("\n\tframe_start= %d;"%(self.scene.frame_start))
			ofile.write("\n\tframes_per_second= %d;"%(1.0) )
			ofile.write("\n\tframes= %d-%d;"%(self.scene.frame_start, self.scene.frame_end))
		ofile.write("\n\tframe_stamp_enabled= %d;"%(0))
		ofile.write("\n\tframe_stamp_text= \"%s\";"%("vb25 (git) | V-Ray Standalone %%vraycore | %%rendertime"))
		ofile.write("\n}\n")

		SettingsImageSamplerFilter= VRayScene.SettingsImageSampler
		if SettingsImageSamplerFilter.filter_type != 'NONE':
			ofile.write(AA_FILTER_TYPE[SettingsImageSamplerFilter.filter_type])
			ofile.write("\n\tsize= %.3f;" % SettingsImageSamplerFilter.filter_size)
			ofile.write("\n}\n")

		for module in MODULES:
			vmodule= getattr(VRayScene, module)

			ofile.write("\n%s {"%(module))
			if module == 'SettingsImageSampler':
				ofile.write("\n\ttype= %d;"%(IMAGE_SAMPLER_TYPE[vmodule.type]))
			elif module == 'SettingsColorMapping':
				ofile.write("\n\ttype= %d;"%(COLOR_MAPPING_TYPE[vmodule.type]))

			for param in MODULES[module]:
				ofile.write("\n\t%s= %s;"%(param, p(getattr(vmodule, param))))
			ofile.write("\n}\n")

		ofile.write("\nSettingsEXR SettingsEXR {")
		ofile.write("\n\tcompression= 0;") # 0 - default, 1 - no compression, 2 - RLE, 3 - ZIPS, 4 - ZIP, 5 - PIZ, 6 - pxr24
		ofile.write("\n\tbits_per_channel= %d;" % (16 if self.scene.render.use_exr_half else 32))
		ofile.write("\n}\n")

		ofile.write("\nSettingsJPEG SettingsJPEG {")
		ofile.write("\n\tquality= %d;" % self.scene.render.file_quality)
		ofile.write("\n}\n")

		ofile.write("\nSettingsPNG SettingsPNG {")
		ofile.write("\n\tcompression= %d;" % (int(self.scene.render.file_quality / 10) if self.scene.render.file_quality < 90 else 90))
		ofile.write("\n\tbits_per_channel= 16;")
		ofile.write("\n}\n")

		for plugin in SETTINGS_PLUGINS:
			if hasattr(plugin, 'write'):
				if hasattr(plugin, 'PLUG'):
					rna_pointer= getattr(VRayScene, plugin.PLUG)
					plugin.write(ofile, self.scene, rna_pointer)
				else:
					plugin.write(ofile, self.scene, {})

		for render_channel in VRayScene.render_channels:
			plugin= get_plugin_by_id(CHANNEL_PLUGINS, render_channel.type)
			if plugin:
				plugin.write(ofile, getattr(render_channel,plugin.PLUG), self.scene, render_channel.name)

		# plug= get_plugin_by_name('TexSky')
		# if plug:
		# 	print(plug.NAME)

		# print('ID', get_plugin_property(SettingsIrradianceMap,'detail_scale'))

		ofile.write("\n")

	
	def write_frame(self):
		timer= time.clock()

		debug(self.scene, "Writing frame (%i)..."%(self.scene.frame_current), False)

		VRayScene=       self.scene.vray
		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		for ob in self.scene.objects:
			if ob.type in ('CAMERA','ARMATURE','LATTICE'):
				continue

			if VRayExporter.active_layers:
				if not object_on_visible_layers(self.scene,ob):
					if ob.type == 'LAMP':
						if not VRayScene.use_hidden_lights:
							continue
					elif not SettingsOptions.geom_doHidden:
						continue
					else:
						continue

			if ob.hide_render:
				if ob.type == 'LAMP':
					if not VRayScene.use_hidden_lights:
						continue
				else:
					if not SettingsOptions.geom_doHidden:
						continue

			if PLATFORM == "linux2":
				debug(self.scene, "{0}: \033[0;32m{1:<32}\033[0m".format(ob.type, ob.name), True if VRayExporter.debug else False)
			else:
				debug(self.scene, "{0}: {1:<32}".format(ob.type, ob.name), True if VRayExporter.debug else False)

		debug(self.scene, "Writing frame {0}... done {1:<64}".format(self.scene.frame_current, "[%.2f]"%(time.clock() - timer)))

	def execute(self, context):
		self.scene= context.scene

		VRayScene= self.scene.vray
		VRayExporter= VRayScene.exporter

		debug(self.scene, "Writing scene...")

		timer= time.clock()

		if VRayExporter.animation:
			selected_frame= self.scene.frame_current
			f= self.scene.frame_start
			while(f <= self.scene.frame_end):
				self.scene.frame_set(f)
				self.write_frame()
				f+= self.scene.frame_step
			self.scene.frame_set(selected_frame)
		else:
			self.write_frame()

		self.write_settings()

		debug(self.scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))
		
		return {'FINISHED'}


class VRAY_OT_write_geometry(bpy.types.Operator):
	bl_idname      = "vray.write_geometry"
	bl_label       = "Export meshes"
	bl_description = "Export meshes into vrscene file."

	def execute(self, context):
		sce= context.scene

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

		return {'FINISHED'}


class VRAY_OT_run(bpy.types.Operator):
	bl_idname      = "vray.run"
	bl_label       = "Run V-Ray"
	bl_description = "Run V-Ray renderer."

	def execute(self, context):
		scene= context.scene
		
		VRayScene= scene.vray
		VRayExporter= VRayScene.exporter
		VRayDR=       VRayScene.VRayDR

		vray_exporter=   get_vray_exporter_path()
		vray_standalone= get_vray_standalone_path(scene)

		params= []
		params.append(vray_standalone)

		wx= scene.render.resolution_x * scene.render.resolution_percentage / 100
		wy= scene.render.resolution_y * scene.render.resolution_percentage / 100

		if scene.render.use_border:
			x0= wx * scene.render.border_min_x
			y0= wy * (1.0 - scene.render.border_max_y)
			x1= wx * scene.render.border_max_x
			y1= wy * (1.0 - scene.render.border_min_y)

			if scene.render.use_crop_to_border:
				params.append('-crop=')
			else:
				params.append('-region=')
			params.append("%i;%i;%i;%i"%(x0,y0,x1,y1))

		params.append('-sceneFile=')
		params.append(get_filenames(scene,'scene'))

		params.append('-display=')
		params.append('1')

		if VRayExporter.image_to_blender:
			params.append('-autoclose=')
			params.append('1')

		params.append('-frames=')
		if VRayExporter.animation:
			params.append("%d-%d,%d"%(scene.frame_start, scene.frame_end,int(scene.frame_step)))
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
				
		if VRayExporter.auto_save_render:
			params.append('-imgFile=')
			params.append(image_file)

		if VRayExporter.autorun:
			if VRayExporter.detach:
				command= "(%s)&" % (' '.join(params))
				if PLATFORM == "win32":
					command= "start \"VRAYSTANDALONE\" /B /BELOWNORMAL \"%s\" %s" % (params[0], ' '.join(params[1:]))
				os.system(command)
			else:
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
								result= self.begin_result(0, 0, int(wx), int(wy))
								result.layers[0].load_from_file(load_file)
								self.end_result(result)
						except:
							pass
						break

					time.sleep(0.1)

		else:
			debug(scene, "Enable \"Autorun\" option to start V-Ray automatically after export.")
			debug(scene, "Command: %s" % ' '.join(params))

				
		return {'FINISHED'}


class VRAY_OT_render(bpy.types.Operator):
	bl_idname      = "vray.render"
	bl_label       = "V-Ray Renderer"
	bl_description = "Render operator."

	def execute(self, context):
		scene= context.scene
		
		VRayScene= scene.vray
		VRayExporter= VRayScene.exporter

		if VRayExporter.auto_meshes:
			bpy.ops.vray.write_geometry()

		bpy.ops.vray.write_scene()

		bpy.ops.vray.run()

		return {'FINISHED'}


class VRayRenderer(bpy.types.RenderEngine):
	bl_idname      = 'VRAY_RENDER'
	bl_label       = "V-Ray (git)"
	bl_use_preview =  False
	
	def render(self, scene):
		bpy.ops.vray.render()
		
		# global sce

		# sce= scene
		# rd=  scene.render
		# wo=  scene.world

		# vsce= sce.vray
		# ve= vsce.exporter
		# dr= vsce.VRayDR

		# VRayBake= vsce.VRayBake

		# if ve.auto_meshes:
		# 	bpy.ops.vray.write_geometry()

		# write_scene(sce, bake= VRayBake.use)

		# vb_path= get_vray_exporter_path()

		# params= []
		# params.append(get_vray_standalone_path(sce))

		# image_file= os.path.join(get_filenames(sce,'output'),"render_%s.%s" % (clean_string(sce.camera.name),get_render_file_format(ve,rd.file_format)))
		# load_file= os.path.join(get_filenames(sce,'output'),"render_%s.%.4i.%s" % (clean_string(sce.camera.name),sce.frame_current,get_render_file_format(ve,rd.file_format)))

		# wx= rd.resolution_x * rd.resolution_percentage / 100
		# wy= rd.resolution_y * rd.resolution_percentage / 100

		# if rd.use_border:
		# 	x0= wx * rd.border_min_x
		# 	y0= wy * (1.0 - rd.border_max_y)
		# 	x1= wx * rd.border_max_x
		# 	y1= wy * (1.0 - rd.border_min_y)

		# 	if rd.use_crop_to_border:
		# 		params.append('-crop=')
		# 	else:
		# 		params.append('-region=')
		# 	params.append("%i;%i;%i;%i"%(x0,y0,x1,y1))

		# params.append('-sceneFile=')
		# params.append(get_filenames(sce,'scene'))

		# params.append('-display=')
		# params.append('1')

		# if ve.image_to_blender:
		# 	params.append('-autoclose=')
		# 	params.append('1')

		# params.append('-frames=')
		# if ve.animation:
		# 	params.append("%d-%d,%d"%(sce.frame_start, sce.frame_end,int(sce.frame_step)))
		# else:
		# 	params.append("%d" % sce.frame_current)

		# if dr.on:
		# 	if len(dr.nodes):
		# 		params.append('-distributed=')
		# 		params.append('1')
		# 		params.append('-portNumber=')
		# 		params.append(str(dr.port))
		# 		params.append('-renderhost=')
		# 		params.append("\"%s\"" % ';'.join([n.address for n in dr.nodes]))
				
		# params.append('-imgFile=')
		# params.append(image_file)

		# if ve.autorun:
		# 	process= subprocess.Popen(params)

		# 	while True:
		# 		if self.test_break():
		# 			try:
		# 				process.kill()
		# 			except:
		# 				pass
		# 			break

		# 		if process.poll() is not None:
		# 			try:
		# 				if not ve.animation and ve.image_to_blender:
		# 					result= self.begin_result(0, 0, int(wx), int(wy))
		# 					result.layers[0].load_from_file(load_file)
		# 					self.end_result(result)
		# 			except:
		# 				pass
		# 			break

		# 		time.sleep(0.05)
		# else:
		# 	print("V-Ray/Blender: Enable \"Autorun\" option to start V-Ray automatically after export.")
		# 	print("V-Ray/Blender: Command: %s" % ' '.join(params))


class VRayRendererPreview(bpy.types.RenderEngine):
	bl_idname      = 'VRAY_RENDER_PREVIEW'
	bl_label       = "V-Ray (git) [material preview]"
	bl_use_preview = True
	
	def render(self, scene):
		global sce
		
		sce= scene
		rd=  scene.render
		wo=  scene.world

		vsce= sce.vray
		ve= vsce.exporter

		wx= int(rd.resolution_x * rd.resolution_percentage / 100)
		wy= int(rd.resolution_y * rd.resolution_percentage / 100)

		vb_path=   get_vray_exporter_path()
		vray_path= get_vray_standalone_path(sce)

		params= []
		params.append(vray_path)

		if sce.name == "preview":
			if wx < 100:
				return

			image_file= os.path.join(get_filenames(sce,'output'),"preview.exr")
			load_file= image_file

			filters= {
				'exported_bitmaps':   [],
				'exported_materials': [],
				'exported_proxy':     []
			}

			temp_params= {
				'uv_ids': get_uv_layers(sce),
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
				'volume':       None,
			}

			ofile= open(os.path.join(vb_path,"preview","preview_materials.vrscene"), 'w')
			ofile.write("\nSettingsOutput {")
			ofile.write("\n\timg_separateAlpha= 0;")
			ofile.write("\n\timg_width= %s;" % wx)
			ofile.write("\n\timg_height= %s;" % wy)
			ofile.write("\n}\n")
			for ob in sce.objects:
				if ob.type == 'CAMERA':
					if ob.name == "Camera":
						write_camera(sce, ofile, camera= ob)
					continue
				if ob.type in ('CAMERA','LAMP','EMPTY','ARMATURE','LATTICE'):
					continue
				if object_on_visible_layers(sce,ob):
					continue
				for ms in ob.material_slots:
					if ms.material:
						if ob.name.find("preview") != -1:
							write_material(ms.material, filters, object_params, ofile, name="PREVIEW", ob= ob, params= temp_params)
						elif ms.material.name in ("checkerlight","checkerdark"):
							write_material(ms.material, filters, object_params, ofile, ob= ob, params= temp_params)
			ofile.close()

			params.append('-sceneFile=')
			params.append(os.path.join(vb_path,"preview","preview.vrscene"))
			params.append('-display=')
			params.append("0")
			params.append('-showProgress=')
			params.append("0")
			params.append('-imgFile=')
			params.append(image_file)

		else:
			image_file= os.path.join(get_filenames(sce,'output'),"render_%s.%s" % (clean_string(sce.camera.name),get_render_file_format(ve,rd.file_format)))
			load_file= os.path.join(get_filenames(sce,'output'),"render_%s.%.4i.%s" % (clean_string(sce.camera.name),sce.frame_current,get_render_file_format(ve,rd.file_format)))

			if ve.auto_meshes:
				bpy.ops.vray.write_geometry()
			write_scene(sce)

			if rd.use_border:
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

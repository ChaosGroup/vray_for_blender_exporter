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
import os
import subprocess
import tempfile
import time

''' Blender modules '''
import bpy

''' vb modules '''
import vb25.render
import vb25.proxy

from vb25.utils import *


class VRAY_OT_effect_add(bpy.types.Operator):
	bl_idname=      'vray.effect_add'
	bl_label=       "Add Effect"
	bl_description= "Add effect."

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		VRayEffects.effects.add()
		VRayEffects.effects[-1].name= "Effect"

		return {'FINISHED'}


class VRAY_OT_effect_remove(bpy.types.Operator):
	bl_idname=      'vray.effect_remove'
	bl_label=       "Remove Effect"
	bl_description= "Remove effect."

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects
				
		if VRayEffects.effects_selected >= 0:
			VRayEffects.effects.remove(VRayEffects.effects_selected)
			VRayEffects.effects_selected-= 1

		return {'FINISHED'}


# class VRAY_OT_effect_up(bpy.types.Operator):
# 	bl_idname=      'vray.effect_up'
# 	bl_label=       "Move Effect Up"
# 	bl_description= "Move effect up."

# 	def execute(self, context):
# 		VRayScene= context.scene.vray

# 		VRayEffects= VRayScene.VRayEffects

# 		if VRayEffects.effects_selected >= 0:
# 			if VRayEffects.effects_selected == 0:
# 				return {'FINISHED'}

# 			sel= VRayEffects.effects_selected
			
# 			VRayEffects.effects[sel], VRayEffects.effects[sel - 1] = VRayEffects.effects[sel - 1], VRayEffects.effects[sel]

# 			VRayEffects.effects_selected-= 1

# 		return {'FINISHED'}


# class VRAY_OT_effect_down(bpy.types.Operator):
# 	bl_idname=      'vray.effect_down'
# 	bl_label=       "Move Effect Down"
# 	bl_description= "Move effect down."

# 	def execute(self, context):
# 		VRayScene= context.scene.vray

# 		VRayEffects= VRayScene.VRayEffects

# 		if VRayEffects.effects_selected >= 0:
# 			if VRayEffects.effects_selected == len(VRayEffects.effects) - 1:
# 				return {'FINISHED'}

# 			sel= VRayEffects.effects_selected
			
# 			VRayEffects.effects[sel], VRayEffects.effects[sel + 1] = VRayEffects.effects[sel + 1], VRayEffects.effects[sel]

# 			VRayEffects.effects_selected+= 1

# 		return {'FINISHED'}


class VRAY_OT_channel_add(bpy.types.Operator):
	bl_idname=      'vray.render_channels_add'
	bl_label=       "Add Render Channel"
	bl_description= "Add render channel."

	def execute(self, context):
		sce= context.scene
		vsce= sce.vray

		render_channels= vsce.render_channels

		render_channels.add()
		render_channels[-1].name= "RenderChannel"

		return{'FINISHED'}


class VRAY_OT_channel_del(bpy.types.Operator):
	bl_idname=      'vray.render_channels_remove'
	bl_label=       "Remove Render Channel"
	bl_description= "Remove render channel."

	def execute(self, context):
		sce= context.scene
		vsce= sce.vray
		
		render_channels= vsce.render_channels
		
		if vsce.render_channels_index >= 0:
		   render_channels.remove(vsce.render_channels_index)
		   vsce.render_channels_index-= 1

		return{'FINISHED'}


class VRAY_OT_node_add(bpy.types.Operator):
	bl_idname=      'vray.render_nodes_add'
	bl_label=       "Add Render Node"
	bl_description= "Add render node."

	def execute(self, context):
		vs= context.scene.vray
		module= vs.VRayDR

		module.nodes.add()
		module.nodes[-1].name= "Render Node"

		return{'FINISHED'}


class VRAY_OT_node_del(bpy.types.Operator):
	bl_idname=      'vray.render_nodes_remove'
	bl_label=       "Remove Render Node"
	bl_description= "Remove render node"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.VRayDR

		if module.nodes_selected >= 0:
		   module.nodes.remove(module.nodes_selected)
		   module.nodes_selected-= 1

		return{'FINISHED'}


class VRAY_OT_convert_scene(bpy.types.Operator):
	bl_idname      = "vray.convert_materials"
	bl_label       = "Convert materials"
	bl_description = "Convert scene materials from Blender Internal to V-Ray."

	CONVERT_BLEND_TYPE= {
		'MIX':          'OVER',
		'SCREEN':       'OVER',
		'DIVIDE':       'OVER',
		'HUE':          'OVER',
		'VALUE':        'OVER',
		'COLOR':        'OVER',
		'SOFT LIGHT':   'OVER',
		'LINEAR LIGHT': 'OVER',
		'OVERLAY':      'OVER',
		'ADD':          'ADD',
		'SUBTRACT':     'SUBTRACT',
		'MULTIPLY':     'MULTIPLY',
		'DIFFERENCE':   'DIFFERENCE',
		'DARKEN':       'DARKEN',
		'LIGHTEN':      'LIGHTEN',
		'SATURATION':   'SATURATE',
	}

	def execute(self, context):
		for ma in bpy.data.materials:
			debug(context.scene, "Converting material: %s" % ma.name)
			
			rm= ma.raytrace_mirror
			rt= ma.raytrace_transparency
			
			VRayMaterial= ma.vray
			BRDFVRayMtl=  VRayMaterial.BRDFVRayMtl

			if ma.emit > 0.0:
				VRayMaterial.type= 'EMIT'

			if rm.use:
				BRDFVRayMtl.reflect_color= tuple([rm.reflect_factor]*3)
				BRDFVRayMtl.reflect_glossiness= rm.gloss_factor
				BRDFVRayMtl.reflect_subdivs= rm.gloss_samples
				BRDFVRayMtl.reflect_depth= rm.depth
				BRDFVRayMtl.option_cutoff= rm.gloss_threshold
				BRDFVRayMtl.anisotropy= 1.0 - rm.gloss_anisotropic

				if rm.fresnel > 0.0:
					BRDFVRayMtl.fresnel= True
					BRDFVRayMtl.fresnel_ior= rm.fresnel
			
			for slot in ma.texture_slots:
				if slot and slot.texture and slot.texture.type in TEX_TYPES:
					VRaySlot=    slot.texture.vray_slot
					VRayTexture= slot.texture.vray

					VRaySlot.blend_mode= self.CONVERT_BLEND_TYPE[slot.blend_type]
					
					if slot.use_map_emit:
						VRayMaterial.type= 'EMIT'

			# if ma.type == 'VOLUME':
			# 	VRayMaterial.type= 'VOL'
				
		return{'FINISHED'}


class VRAY_OT_flip_resolution(bpy.types.Operator):
	bl_idname      = "vray.flip_resolution"
	bl_label       = "Flip resolution"
	bl_description = "Flip render resolution."

	def execute(self, context):
		scene= context.scene
		rd=    scene.render

		VRayScene= scene.vray

		if VRayScene.image_aspect_lock:
			VRayScene.image_aspect= 1.0 / VRayScene.image_aspect

		rd.resolution_x, rd.resolution_y = rd.resolution_y, rd.resolution_x
		rd.pixel_aspect_x, rd.pixel_aspect_y = rd.pixel_aspect_y, rd.pixel_aspect_x
		
		return{'FINISHED'}


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
					vb25.proxy.generate_proxy(sce,ob,vrmesh_filepath,append=True)
					frame+= 1
				sce.frame_set(selected_frame)
			else:
				vb25.proxy.generate_proxy(sce,ob,vrmesh_filepath)

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


class VRAY_OT_preview(bpy.types.Operator):
	bl_idname      = "vray.write_scene"
	bl_label       = "Export scene"
	bl_description = "Export scene to \"vrscene\" file."

	type= bpy.props.EnumProperty(
		name= "Type",
		description= "Preview type.",
		items= (
			('TEXTURE',  "Texture",  ""),
			('MATERIAL', "Material", ""),
		),
		default= 'MATERIAL'
	)

	def execute(self, context):

		vb25.render.preview(context.scene, self.type)
		
		return {'FINISHED'}


class VRAY_OT_write_scene(bpy.types.Operator):
	bl_idname      = "vray.write_scene"
	bl_label       = "Export scene"
	bl_description = "Export scene to \"vrscene\" file."

	def execute(self, context):

		vb25.render.write_scene(context.scene)
		
		return {'FINISHED'}


class VRAY_OT_write_geometry(bpy.types.Operator):
	bl_idname      = "vray.write_geometry"
	bl_label       = "Export meshes"
	bl_description = "Export meshes into vrscene file."

	def execute(self, context):

		vb25.render.write_geometry(context.scene)

		return {'FINISHED'}


class VRAY_OT_run(bpy.types.Operator):
	bl_idname      = "vray.run"
	bl_label       = "Run V-Ray"
	bl_description = "Run V-Ray renderer."

	def execute(self, context):

		vb25.render.run(None, context.scene)
				
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



'''
  RENDER ENGINE
'''
class VRayRenderer(bpy.types.RenderEngine):
	bl_idname      = 'VRAY_RENDER'
	bl_label       = "V-Ray (git)"
	bl_use_preview =  False
	
	def render(self, scene):
		VRayScene= scene.vray
		VRayExporter= VRayScene.exporter

		if VRayExporter.use_render_operator:
			vb25.render.render(self, scene)
		else:
			#bpy.ops.vray.render()
			vb25.render.render(self, scene)


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

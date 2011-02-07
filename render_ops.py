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
from bpy.props import *

''' vb modules '''
import vb25.render
import vb25.proxy

from vb25.utils import *


VRAYBLENDER_MENU_ITEM= "V-Ray 2.0"


'''
  Effects operators
'''
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


'''
  Material operators
'''
def active_node_mat(mat):
    if mat:
        mat_node= mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat
    return None


def find_brdf_pointer(rna_pointer):
	if rna_pointer.brdf_selected >= 0 and rna_pointer.brdfs[rna_pointer.brdf_selected].type == 'BRDFLayered':
		return find_brdf_pointer(getattr(rna_pointer.brdfs[rna_pointer.brdf_selected], 'BRDFLayered'))
	return rna_pointer


class VRAY_OT_brdf_add(bpy.types.Operator):
	bl_idname=      'vray.brdf_add'
	bl_label=       "Add BRDF"
	bl_description= "Add BRDF."

	def execute(self, context):
		ma= active_node_mat(context.material)
		if ma:
			rna_pointer= ma.vray.BRDFLayered
			# rna_pointer= find_brdf_pointer(VRayMaterial)

			rna_pointer.brdfs.add()
			rna_pointer.brdfs[-1].name= "BRDF"
			
			return {'FINISHED'}

		return {'CHANCELED'}


class VRAY_OT_brdf_remove(bpy.types.Operator):
	bl_idname=      'vray.brdf_remove'
	bl_label=       "Remove BRDF"
	bl_description= "Remove BRDF."

	def execute(self, context):
		ma= active_node_mat(context.material)
		if ma:
			rna_pointer= ma.vray.BRDFLayered
			# rna_pointer= find_brdf_pointer(VRayMaterial)
				
			if rna_pointer.brdf_selected >= 0:
				rna_pointer.brdfs.remove(rna_pointer.brdf_selected)
				rna_pointer.brdf_selected-= 1

			return {'FINISHED'}

		return {'CHANCELED'}


class VRAY_OT_brdf_up(bpy.types.Operator):
	bl_idname=      'vray.brdf_up'
	bl_label=       "Move BRDF up"
	bl_description= "Move BRDF up."

	def execute(self, context):
		ma= active_node_mat(context.material)
		if ma:
			rna_pointer= ma.vray.BRDFLayered
			# rna_pointer= find_brdf_pointer(VRayMaterial)

			if rna_pointer.brdf_selected <= 0:
				return {'FINISHED'}

			rna_pointer.brdfs.move(rna_pointer.brdf_selected,
								   rna_pointer.brdf_selected - 1)
			rna_pointer.brdf_selected-= 1

			return {'FINISHED'}

		return {'CHANCELED'}


class VRAY_OT_brdf_down(bpy.types.Operator):
	bl_idname=      'vray.brdf_down'
	bl_label=       "Move BRDF down"
	bl_description= "Move BRDF down."

	def execute(self, context):
		ma= active_node_mat(context.material)
		if ma:
			rna_pointer= ma.vray.BRDFLayered
			# rna_pointer= find_brdf_pointer(VRayMaterial)

			if rna_pointer.brdf_selected == len(rna_pointer.brdfs) - 1:
				return {'FINISHED'}

			rna_pointer.brdfs.move(rna_pointer.brdf_selected,
								   rna_pointer.brdf_selected + 1)
			rna_pointer.brdf_selected+= 1

			return {'FINISHED'}

		return {'CHANCELED'}


'''
  Render channel operators
'''
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


'''
  DR node operators
'''
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


'''
  Some usefull utils
'''
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


class VRAY_OT_settings_to_text(bpy.types.Operator):
	bl_idname=      'vray.settings_to_text'
	bl_label=       "Settings to Text"
	bl_description= "Export settings to Text."

	bb_code= BoolProperty(
		name= "Use BB-code",
		description= "Use BB-code formatting.",
		default= True
	)

	def execute(self, context):
		# TODO:
		return {'FINISHED'}


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
	bl_label       = "%s" % VRAYBLENDER_MENU_ITEM
	bl_use_preview =  False
	
	def render(self, scene):
		VRayScene= scene.vray
		VRayExporter= VRayScene.exporter

		# if VRayExporter.use_render_operator:
		# 	vb25.render.render(self, scene)
		# else:
		# 	bpy.ops.vray.render()
		vb25.render.render(self, scene)


class VRayRendererPreview(bpy.types.RenderEngine):
	bl_idname      = 'VRAY_RENDER_PREVIEW'
	bl_label       = "%s (material preview)" % VRAYBLENDER_MENU_ITEM
	bl_use_preview = True
	
	def render(self, scene):
		VRayScene= scene.vray
		VRayExporter= VRayScene.exporter

		if scene.name == "preview":
			if scene.render.resolution_x < 64:
				return
			vb25.render.render(self, scene, preview=True)
		else:
			vb25.render.render(self, scene)


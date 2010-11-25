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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


''' Python modules '''
import os

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class VRayData(bpy.types.IDPropertyGroup):
    pass

bpy.types.Mesh.vray= PointerProperty(
	name= "V-Ray Object Data Settings",
	type=  VRayData,
	description= "V-Ray object data settings."
)

bpy.types.Curve.vray= PointerProperty(
	name= "V-Ray Object Data Settings",
	type=  VRayData,
	description= "V-Ray object data settings."
)


'''
  Plugin: GeomMeshFile
'''
class GeomMeshFile(bpy.types.IDPropertyGroup):
    pass

VRayData.GeomMeshFile= PointerProperty(
	name= "V-Ray Proxy",
	type=  GeomMeshFile,
	description= "V-Ray proxy settings."
)

GeomMeshFile.use= BoolProperty(
	name= "Use Proxy",
	description= "Use proxy mesh.",
	default= False
)

GeomMeshFile.file= StringProperty(
	name= "File",
	subtype= 'FILE_PATH',
	description= "Proxy file."
)

GeomMeshFile.anim_type= EnumProperty(
	name= "Animation type",
	description= "Proxy animation type.",
	items= (
		('LOOP',     "Loop",      "."),
		('ONCE',     "Once",      "."),
		('PINGPONG', "Ping-pong", "."),
		('STILL',    "Still",     ".")
	),
	default= 'LOOP'
)

GeomMeshFile.mode= EnumProperty(
	name= "Mode",
	description= "Proxy creation mode.",
	items= (
		('NONE',    "None",        "Don\'t attach proxy."),
		('NEW',     "New object",  "Attach proxy to new object."),
		('THIS',    "This object", "Attach proxy to this object."),
		('REPLACE', "Replace",     "Replace this object with proxy."),
	),
	default= 'NONE'
)

GeomMeshFile.anim_speed= FloatProperty(
	name= "Speed",
	description= "Animated proxy playback speed.",
	min= 0.0,
	max= 1000.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

GeomMeshFile.anim_offset= FloatProperty(
	name= "Offset",
	description= "Animated proxy initial frame offset.",
	min= 0.0,
	max= 1000.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.0
)

GeomMeshFile.scale= FloatProperty(
	name= "Scale",
	description= "Size scaling factor.",
	min= 0.0,
	max= 1000.0,
	soft_min= 0.0,
	soft_max= 2.0,
	default= 1.0
)

GeomMeshFile.apply_transforms= BoolProperty(
	name= "Apply transform",
	description= "Apply rotation, location and scale.",
	default= False
)

GeomMeshFile.add_suffix= BoolProperty(
	name= "Add suffix",
	description= "Add \"_proxy\" suffix to object and mesh names.",
	default= True
)

GeomMeshFile.dirpath= StringProperty(
	name= "Path",
	subtype= 'DIR_PATH',
	description= "Proxy generation directory.",
	default= "//proxy"
)

GeomMeshFile.filename= StringProperty(
	name= "Name",
	subtype= 'NONE',
	description= "Proxy file name. If empty object's name is used.",
	default= ""
)

GeomMeshFile.animation= BoolProperty(
	name= "Animation",
	description= "Animated proxy.",
	default= False
)

GeomMeshFile.animation_range= EnumProperty(
	name= "Animation range",
	description= "Animation range type.",
	items= (
		('MANUAL', "Manual", "."),
		('SCENE',  "Scene",     ".")
	),
	default= 'SCENE'
)

GeomMeshFile.frame_start= IntProperty(
	name= "Start frame",
	description= "Proxy generation start frame.",
	min= 1,
	max= 1000,
	soft_min= 1,
	soft_max= 250,
	default= 1
)

GeomMeshFile.frame_end= IntProperty(
	name= "End frame",
	description= "Proxy generation end frame.",
	min= 1,
	max= 1000,
	soft_min= 1,
	soft_max= 250,
	default= 250
)



'''
  GUI
'''
import properties_data_mesh
properties_data_mesh.DATA_PT_context_mesh.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_normals.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_settings.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_shape_keys.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_texface.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_uv_texture.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_vertex_colors.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_vertex_groups.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.MESH_MT_shape_key_specials.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.MESH_MT_vertex_group_specials.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_context_mesh.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_normals.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_settings.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_shape_keys.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_texface.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_uv_texture.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_vertex_colors.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.DATA_PT_vertex_groups.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.MESH_MT_shape_key_specials.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_mesh.MESH_MT_vertex_group_specials.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
del properties_data_mesh


narrowui= 200


def base_poll(cls, context):
	rd= context.scene.render
	return (context.mesh) and (rd.engine in cls.COMPAT_ENGINES)


class DataButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'


class DATA_PT_vray_proxy(DataButtonsPanel, bpy.types.Panel):
	bl_label = "Proxy"
	bl_default_closed = True
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		ob= context.mesh.vray.GeomMeshFile
		self.layout.prop(ob, 'use', text="")

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		GeomMeshFile= context.mesh.vray.GeomMeshFile

		split= layout.split()
		split.active= GeomMeshFile.use
		col= split.column()
		col.prop(GeomMeshFile, 'file')
		col.prop(GeomMeshFile, 'anim_type')

		split= layout.split()
		split.active= GeomMeshFile.use
		col= split.column(align=True)
		col.prop(GeomMeshFile, 'anim_speed')
		if wide_ui:
			col= split.column()
		col.prop(GeomMeshFile, 'anim_offset')

		layout.separator()
		
		split= layout.split()
		col= split.column()
		col.label(text="Proxy generation:")

		split= layout.split()
		col= split.column()
		col.prop(GeomMeshFile, 'dirpath')
		col.prop(GeomMeshFile, 'filename')
		col.separator()
		col.prop(GeomMeshFile, 'mode', text="Attach mode")

		split= layout.split()
		col= split.column()
		col.prop(GeomMeshFile, 'animation')
		sub= col.column()
		sub.active= GeomMeshFile.animation
		sub.prop(GeomMeshFile, 'animation_range', text="Range")
		if GeomMeshFile.animation_range == 'MANUAL':
			sub= sub.column(align=True)
			sub.prop(GeomMeshFile, 'frame_start')
			sub.prop(GeomMeshFile, 'frame_end')
		if wide_ui:
			col= split.column()
		col.prop(GeomMeshFile, 'add_suffix')
		col.prop(GeomMeshFile, 'apply_transforms')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.operator('vray_create_proxy', icon='OUTLINER_OB_MESH')

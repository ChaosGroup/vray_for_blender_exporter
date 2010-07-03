'''

 V-Ray/Blender 2.5.8

 http://vray.cgdo.ru

 Started:       29 Aug 2009
 Last Modified: 29 Aug 2009

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


import bpy


FloatProperty= bpy.types.Mesh.FloatProperty
IntProperty= bpy.types.Mesh.IntProperty
BoolProperty= bpy.types.Mesh.BoolProperty


FloatProperty(
	attr= "vray_node_generate_gi",
	name= "Generate GI",
	description= "",
	min= 0.0,
	max= 1000.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.0
)


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
del properties_data_mesh


class DataButtonsPanel(bpy.types.Panel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'

	def poll(self, context):
		engine= context.scene.render.engine
		return (context.mesh) and (engine in self.COMPAT_ENGINES)


class DATA_PT_vray_node(DataButtonsPanel):
	bl_label = "Properties"

	COMPAT_ENGINES = {'VRAY_RENDER'}

	def draw(self, context):
		layout = self.layout
		
		ob= context.object
		me= context.mesh

		split= layout.split()
		col= split.column()
		col.prop(me, "vray_node_generate_gi")


bpy.types.register(DATA_PT_vray_node)


#
# V-Ray For Blender
#
# http://vray.cgdo.ru
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import bpy

from pynodes_framework import idref

from vb25.ui import classes


class VRAY_OBP_context_node(classes.VRayObjectPanel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	def draw(self, context):
		VRayObject = context.object.vray

		split = self.layout.split()
		row = split.row(align=True)
		idref.draw_idref(row, VRayObject, 'ntree', text="Node Tree")
		row.operator("vray.add_nodetree_object", icon='ZOOMIN', text="")


class VRAY_OBP_render(classes.VRayObjectPanel):
	bl_label = "Render"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls, context):
		return classes.VRayObjectPanel.poll(context) and not context.object.vray.LightMesh.use

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		layout = self.layout
		wide_ui = context.region.width > classes.narrowui

		VRayObject     = context.object.vray
		MtlRenderStats = VRayObject.MtlRenderStats

		layout.prop(VRayObject, 'fade_radius')


class VRAY_OBP_lightmesh(classes.VRayObjectPanel):
	bl_label = "Light"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		ob= context.object
		VRayObject= ob.vray
		LightMesh= VRayObject.LightMesh
		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(LightMesh, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		ob= context.object
		VRayObject= ob.vray
		LightMesh= VRayObject.LightMesh

		layout= self.layout
		layout.active= LightMesh.use

		split= layout.split()
		col= split.column()
		col.row().prop(LightMesh, 'color_type', expand=True)
		if wide_ui:
			col= split.column()
		if LightMesh.color_type == 'RGB':
			sub= col.row(align= True)
			sub.prop(LightMesh, 'color', text="")
			sub.operator('vray.set_kelvin_color', text="", icon= 'COLOR', emboss= False).data_path="object.vray.LightMesh.color"
		else:
			col.prop(LightMesh, 'temperature', text="K")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(LightMesh, 'lightPortal', text="Mode")
		if LightMesh.lightPortal == 'NORMAL':
			col.prop(LightMesh, 'units', text="Units")
			col.prop(LightMesh, 'intensity', text="Intensity")
		col.prop(LightMesh, 'subdivs')
		col.prop(LightMesh, 'causticSubdivs', text="Caustics")
		if wide_ui:
			col= split.column()
		col.prop(LightMesh, 'enabled', text="On")
		col.prop(LightMesh, 'invisible')
		col.prop(LightMesh, 'affectDiffuse')
		col.prop(LightMesh, 'affectSpecular')
		col.prop(LightMesh, 'affectReflections')
		col.prop(LightMesh, 'noDecay')
		col.prop(LightMesh, 'doubleSided')
		col.prop(LightMesh, 'storeWithIrradianceMap')

		layout.separator()
		layout.prop(LightMesh, 'use_include_exclude')

		if LightMesh.use_include_exclude:
			split= layout.split()
			col= split.column()
			col.prop(LightMesh, 'include_exclude')
			col.prop_search(LightMesh,     'include_objects',
							context.scene, 'objects',
							text="Objects")
			col.prop_search(LightMesh, 'include_groups',
							bpy.data,  'groups',
							text="Groups")


class VRAY_OBP_subdivision(classes.VRayObjectPanel):
	bl_label   = "Subdivision"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		ob= context.object
		VRayObject= ob.vray
		GeomStaticSmoothedMesh= VRayObject.GeomStaticSmoothedMesh
		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(GeomStaticSmoothedMesh, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		ob= context.object
		VRayObject= ob.vray
		GeomStaticSmoothedMesh= VRayObject.GeomStaticSmoothedMesh

		layout= self.layout
		layout.active= GeomStaticSmoothedMesh.use

		split= layout.split()
		col= split.column()
		col.prop(GeomStaticSmoothedMesh, 'static_subdiv')
		if wide_ui:
			col= split.column()
		col.prop(GeomStaticSmoothedMesh, 'use_globals')

		if not GeomStaticSmoothedMesh.use_globals:
			layout.separator()
			split= layout.split()
			col= split.column()
			col.prop(GeomStaticSmoothedMesh, 'edge_length')
			col.prop(GeomStaticSmoothedMesh, 'max_subdivs')
			if wide_ui:
				col= split.column()
			col.prop(GeomStaticSmoothedMesh, 'view_dep')



class VRAY_OBP_VRayPattern(classes.VRayObjectPanel):
	bl_label   = "VRayPattern"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls, context):
		return classes.VRayObjectPanel.poll(context) and context.scene.vray.exporter.experimental

	def draw_header(self, context):
		ob = context.object
		VRayObject = ob.vray
		GeomVRayPattern = VRayObject.GeomVRayPattern
		self.layout.prop(GeomVRayPattern, 'use', text="")

	def draw(self, context):
		wide_ui = context.region.width > classes.narrowui

		ob = context.object
		VRayObject = ob.vray
		GeomVRayPattern = VRayObject.GeomVRayPattern

		layout = self.layout
		layout.active = GeomVRayPattern.use

		split = layout.split()
		split.label(text="Pattern Object:")
		split.prop_search(GeomVRayPattern, 'pattern_object',
						  context.scene,   'objects',
						  text="")

		layout.separator()

		layout.prop(GeomVRayPattern, 'crop_size')
		layout.operator('vray.pattern_fit', icon='MOD_MESHDEFORM')
		# layout.prop(GeomVRayPattern, 'geometry_bias')
		layout.separator()

		split = layout.split()
		col = split.column()
		col.prop(GeomVRayPattern, 'height')
		if wide_ui:
			col = split.column()
		col.prop(GeomVRayPattern, 'shift')

		layout.separator()

		layout.prop(GeomVRayPattern, 'use_real_world')
		split = layout.split()
		col = split.column()
		col.prop(GeomVRayPattern, 'tiling_u', text="U")
		if wide_ui:
			col = split.column()
		col.prop(GeomVRayPattern, 'tiling_v', text="V")

		layout.label(text="Polygon ID:")
		split = layout.split()
		col = split.column()
		col.prop(GeomVRayPattern, 'polygon_id_from', text="From")
		if wide_ui:
			col = split.column()
		col.prop(GeomVRayPattern, 'polygon_id_to', text="To")

		layout.label(text="Random Segment Count:")
		split = layout.split()
		col = split.column()
		col.prop(GeomVRayPattern, 'random_segment_u', text="U")
		if wide_ui:
			col = split.column()
		col.prop(GeomVRayPattern, 'random_segment_v', text="V")

		layout.prop(GeomVRayPattern, 'random_segment_seed')

		layout.separator()

		split = layout.split()
		col = split.column()
		col.prop(GeomVRayPattern, 'render_base_object')
		if wide_ui:
			col = split.column()
		col.prop(GeomVRayPattern, 'render_pattern_object')


def GetRegClasses():
	return (
		VRAY_OBP_context_node,
		VRAY_OBP_render,
		VRAY_OBP_lightmesh,
		VRAY_OBP_subdivision,
		VRAY_OBP_VRayPattern,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

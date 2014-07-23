#
# V-Ray For Blender
#
# http://chaosgroup.com
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

from vb30.ui import classes
from vb30.plugins import PLUGINS_ID


class VRAY_OBP_context_node(classes.VRayObjectPanel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	def draw(self, context):
		VRayObject = context.object.vray

		split = self.layout.split()
		row = split.row(align=True)
		row.prop_search(VRayObject, 'ntree', bpy.data, 'node_groups', text="Object Tree")
		if not VRayObject.ntree:
			row.operator("vray.add_nodetree_object", icon='ZOOMIN', text="")


class VRAY_OBP_VRayPattern(classes.VRayObjectPanel):
	bl_label   = "VRayPattern"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls, context):
		return classes.VRayObjectPanel.poll(context) and context.scene.vray.Exporter.experimental

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


class VRayObjectPanelWrapper(classes.VRayObjectPanel, bpy.types.Panel):
	bl_label = "Wrapper"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		ob= context.object
		plugin= ob.vray.MtlWrapper
		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(plugin, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		ob= context.object
		plugin= ob.vray.MtlWrapper

		layout= self.layout
		layout.active= plugin.use

		split= layout.split()
		col= split.column()
		col.prop(plugin, 'generate_gi')
		col.prop(plugin, 'receive_gi')
		if wide_ui:
			col= split.column()
		col.prop(plugin, 'generate_caustics')
		col.prop(plugin, 'receive_caustics')

		split= layout.split()
		col= split.column()
		col.prop(plugin, 'gi_quality_multiplier')

		split= layout.split()
		col= split.column()
		col.label(text="Matte properties")

		split= layout.split()
		colL= split.column()
		colL.prop(plugin, 'matte_surface')
		if wide_ui:
			colR= split.column()
		else:
			colR= colL
		colR.prop(plugin, 'alpha_contribution')
		if plugin.matte_surface:
			colR.prop(plugin, 'reflection_amount')
			colR.prop(plugin, 'refraction_amount')
			colR.prop(plugin, 'gi_amount')
			colR.prop(plugin, 'no_gi_on_other_mattes')

			colL.prop(plugin, 'affect_alpha')
			colL.prop(plugin, 'shadows')
			if plugin.shadows:
				colL.prop(plugin, 'shadow_tint_color')
				colL.prop(plugin, 'shadow_brightness')

		split= layout.split()
		col= split.column()
		col.label(text="Miscellaneous")

		split= layout.split()
		col= split.column()
		col.prop(plugin, 'gi_surface_id')
		col.prop(plugin, 'trace_depth')
		if wide_ui:
			col= split.column()
		col.prop(plugin, 'matte_for_secondary_rays')

		layout.prop(plugin, 'generate_render_elements')


class VRayObjectPanelRenderStats(classes.VRayObjectPanel, bpy.types.Panel):
	bl_label = "Render"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		ob= context.object
		plugin= ob.vray.MtlRenderStats
		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(plugin, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		ob= context.object
		VRayObject= ob.vray
		plugin= VRayObject.MtlRenderStats

		layout= self.layout
		layout.active= plugin.use

		split= layout.split()
		col= split.column()
		col.prop(plugin, 'visibility', text="Visible")

		split= layout.split()
		col= split.column()
		col.label(text="Visible to:")

		split= layout.split()
		sub= split.column()
		sub.active= plugin.visibility
		sub.prop(plugin, 'camera_visibility', text="Camera")
		sub.prop(plugin, 'gi_visibility', text="GI")
		sub.prop(plugin, 'shadows_visibility', text="Shadows")
		if wide_ui:
			sub= split.column()
			sub.active= plugin.visibility
		sub.prop(plugin, 'reflections_visibility', text="Reflections")
		sub.prop(plugin, 'refractions_visibility', text="Refractions")


class VRayObjectPanelUserAttributes(classes.VRayObjectPanel, bpy.types.Panel):
	bl_label = "User Attributes"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		layout = self.layout
		ob = context.object

		Node = ob.vray.Node

		row = layout.row()
		row.template_list('VRayListUserAttributes',
			"",
			Node, 'user_attributes',
			Node, 'user_attributes_selected',
			rows = 4)

		col = row.column()
		sub = col.row()
		subsub = sub.column(align=True)
		subsub.operator('vray.user_attribute_add', text="", icon='ZOOMIN')
		subsub.operator('vray.user_attribute_del', text="", icon='ZOOMOUT')

		if Node.user_attributes_selected >= 0 and len(Node.user_attributes):
			user_attribute = Node.user_attributes[Node.user_attributes_selected]

			layout.separator()
			layout.prop(user_attribute, 'name')
			layout.prop(user_attribute, 'value_type')
			layout.prop(user_attribute, PLUGINS_ID['Node'].gUserAttributeTypeToValue[user_attribute.value_type], text="Value")


class VRayObjectPanelAdvanced(classes.VRayObjectPanel):
	bl_label   = "Advanced"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		VRayObject = context.object.vray

		self.layout.prop(VRayObject, 'use_instancer')


def GetRegClasses():
	return (
		VRAY_OBP_context_node,
		VRAY_OBP_VRayPattern,

		VRayObjectPanelWrapper,
		VRayObjectPanelRenderStats,

		VRayObjectPanelUserAttributes,
		VRayObjectPanelAdvanced,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

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
from vb30.lib import BlenderUtils


class VRAY_OBP_context_node(classes.VRayObjectPanel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	@classmethod
	def poll_custom(cls, context):
		return context.object.type not in BlenderUtils.NonGeometryTypes

	def draw(self, context):
		VRayObject = context.object.vray

		classes.NtreeWidget(self.layout, VRayObject, "Object Tree", "vray.add_nodetree_object", 'OBJECT')


class VRAY_OBP_VRayPattern(classes.VRayObjectPanel):
	bl_label   = "VRayPattern"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll_custom(cls, context):
		return context.scene.vray.Exporter.experimental

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


class VRayObjectPanelVRayClipper(classes.VRayObjectPanel):
	bl_label = "Clipper"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		VRayClipper = context.object.vray.VRayClipper

		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(VRayClipper, 'enabled', text="")

	def draw(self, context):
		layout  = self.layout
		wide_ui = context.region.width > classes.narrowui

		VRayClipper = context.object.vray.VRayClipper

		layout.active = VRayClipper.enabled

		split = layout.split()
		col = split.column()
		col.prop(VRayClipper, 'affect_light')
		col.prop(VRayClipper, 'clip_lights')
		col.prop(VRayClipper, 'use_obj_mesh')

		col.prop(VRayClipper, 'only_camera_rays')
		col.prop(VRayClipper, 'use_obj_mtl')
		col.prop(VRayClipper, 'use_obj_mesh')
		col.prop(VRayClipper, 'invert_inside')

		row = layout.row(align=True)
		row.prop(VRayClipper, 'exclusion_mode', text="")
		row.prop_search(VRayClipper, 'exclusion_nodes', bpy.data, 'groups', text="")

		layout.prop(VRayClipper, 'set_material_id')
		col = layout.column()
		col.active = VRayClipper.set_material_id
		col.prop(VRayClipper, 'material_id')


class VRayObjectPanelVRayScene(classes.VRayObjectPanel):
	bl_label   = "Scene Asset"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		VRayObject = context.object.vray

		self.layout.label(text="", icon='VRAY_LOGO_MONO')
		self.layout.prop(VRayObject, 'overrideWithScene', text="")

	def draw(self, context):
		wide_ui = context.region.width > classes.narrowui
		layout  = self.layout

		VRayObject = context.object.vray
		VRayAsset  = VRayObject.VRayAsset

		layout.active = VRayObject.overrideWithScene

		layout.label("Filepath:")
		layout.prop(VRayAsset, 'sceneFilepath', text="")
		layout.separator()

		split = layout.split()
		col = split.column()
		col.prop(VRayAsset, 'sceneUseTransform')
		# col.prop(VRayAsset, 'flipAxis')
		if wide_ui:
			col = split.column()
		col.prop(VRayAsset, 'sceneAddNodes')
		col.prop(VRayAsset, 'sceneAddLights')

		# col.prop(VRayAsset, 'sceneAddMaterials')
		# col.prop(VRayAsset, 'sceneAddCameras')
		# col.prop(VRayAsset, 'sceneAddEnvironment')

		layout.separator()
		layout.prop(VRayAsset, 'anim_type')
		split = layout.split()
		col = split.column(align=True)
		col.prop(VRayAsset, 'anim_speed')
		col.prop(VRayAsset, 'anim_offset')
		if wide_ui:
			col = split.column(align=True)
		col.prop(VRayAsset, 'anim_start')
		col.prop(VRayAsset, 'anim_length')

		layout.separator()
		layout.prop(VRayAsset, 'use_hide_objects')
		col = layout.column()
		col.active = VRayAsset.use_hide_objects
		col.prop(VRayAsset, 'hidden_objects')

		layout.separator()
		layout.label("Preview Mesh:")
		layout.prop(VRayAsset, 'maxPreviewFaces')
		row = layout.row(align=True)
		row.operator('vray.vrayscene_generate_preview', icon='OUTLINER_OB_MESH', text="Generate")
		row.operator('vray.vrayscene_load_preview',     icon='EDITMODE_HLT',     text="Load")
		row.operator('vray.rotate_to_flip',             icon='FILE_REFRESH',     text="Rotate")


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

		selectedItem     = Node.user_attributes_selected
		haveSelectedItem = selectedItem >= 0 and len(Node.user_attributes)
		if haveSelectedItem:
			user_attribute = Node.user_attributes[selectedItem]

			layout.separator()
			layout.prop(user_attribute, 'name')
			layout.prop(user_attribute, 'value_type')
			layout.prop(user_attribute, PLUGINS_ID['Node'].gUserAttributeTypeToValue[user_attribute.value_type], text="Value")

			box = layout.box()
			box.label("Promote Attribute To Selection")
			box.prop(Node, 'user_attributes_rnd_use')
			box_split = box.split()
			box_split.active = Node.user_attributes_rnd_use
			if user_attribute.value_type == '0':
				sub = box_split.row(align=True)
				sub.prop(Node, 'user_attributes_int_rnd_min')
				sub.prop(Node, 'user_attributes_int_rnd_max')
			elif user_attribute.value_type == '1':
				sub = box_split.row(align=True)
				sub.prop(Node, 'user_attributes_float_rnd_min')
				sub.prop(Node, 'user_attributes_float_rnd_max')
			box.operator('vray.user_attribute_promote')


class VRayObjectPanelAdvanced(classes.VRayObjectPanel):
	bl_label   = "Advanced"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		VRayObject = context.object.vray

		self.layout.label("Duplication:")
		self.layout.prop(VRayObject, 'dupliShowEmitter')

		self.layout.label("Duplication / Particles:")
		self.layout.prop(VRayObject, 'use_instancer')

		split = self.layout.split()
		row = split.row()
		row.active = not VRayObject.use_instancer
		row.prop(VRayObject, 'dupliGroupIDOverride', text="Dupli / Part Object ID Override")

		self.layout.label("Animation:")
		self.layout.prop(VRayObject, 'subframes')


def GetRegClasses():
	return (
		VRAY_OBP_context_node,
		VRAY_OBP_VRayPattern,

		VRayObjectPanelVRayScene,
		VRayObjectPanelVRayClipper,

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

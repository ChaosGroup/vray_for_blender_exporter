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
from vb30.lib import LibUtils
from vb30.plugins import PLUGINS


class VRayPanelMiscTools(classes.VRayRenderLayersPanel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout = self.layout
		VRayScene = context.scene.vray
		VRayQuickSettings = VRayScene.VRayQuickSettings

		box = layout.box()
		box.label("Quick Settings:")
		box.row().prop(VRayQuickSettings, 'presets', expand=True)
		box.separator()
		column = box.column()
		column.active = VRayQuickSettings.presets != 'NONE'
		col = column.column(align=True)
		col.prop(VRayQuickSettings, 'gi_quality',      slider=True)
		col.prop(VRayQuickSettings, 'shading_quality', slider=True)
		col.prop(VRayQuickSettings, 'aa_quality',      slider=True)
		col = column.column(align=True)
		col.prop(VRayQuickSettings, 'max_aa_subdivs')

		VRayConverter = VRayScene.VRayConverter

		box = layout.box()
		box.label("Migration:")
		box.prop(VRayConverter, 'convert_from')
		brow = box.row()
		brow.prop(VRayConverter, 'convert_objects', text="Object Properties")
		brow.prop(VRayConverter, 'convert_materials', text="Materials")
		box.operator("vray.convert_scene", icon='NODETREE')

		box = layout.box()
		box.label("Render Channels:")
		box_row = box.column()
		box_row.operator("vray.gen_random_mtl_ids")


class VRayPanelNodeTrees(classes.VRayRenderLayersPanel):
	bl_label   = "Node Tools"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		VRayExporter = context.scene.vray.Exporter

		self.layout.template_list("VRayListNodeTrees", "", bpy.data, 'node_groups', VRayExporter, 'ntreeListIndex', rows=10)
		self.layout.operator("vray.del_nodetree", text="Delete Selected Nodetree", icon="ZOOMOUT")

		box = self.layout.box()
		box.prop(VRayExporter, 'ntreeExportDirectory', text="Path")
		box.separator()
		box.operator("vray.export_nodetree", text="Export Selected Nodetree", icon='NODETREE')

		box = self.layout.box()
		box.label("Tools")

		box_row = box.row(align=True)
		box_row.operator("vray.switch_material_slot", text="Switch Slots To", icon='MATERIAL')
		box_row.prop(VRayExporter, 'op_switch_slots_switch_to', text="")

		box.separator()
		box_row = box.column()
		box_row.operator("vray.restore_ntree_textures", text="Restore Textures", icon='FILE_REFRESH')
		box_row.operator("vray.remove_fake_textures", text="Remove Unused Data", icon='ERROR')


class VRayPanelMaterials(classes.VRayRenderLayersPanel):
	bl_label   = "Scene Materials"
	bl_options = {'DEFAULT_CLOSED'}

	def getMaterial(self, context):
		VRayExporter = context.scene.vray.Exporter

		listIndex = VRayExporter.materialListIndex if VRayExporter.materialListIndex >= 0 else 0
		numMaterials = len(bpy.data.materials)

		if numMaterials:
			if listIndex >= numMaterials:
				listIndex = 0

			return bpy.data.materials[listIndex]

	def draw(self, context):
		VRayExporter = context.scene.vray.Exporter

		if context.scene.render.engine in {'VRAY_RENDER_PREVIEW', 'VRAY_RENDER_RT'}:
			expandIcon = 'TRIA_DOWN' if VRayExporter.materialListShowPreview else 'TRIA_RIGHT'

			box = self.layout.box()
			row = box.row(align=True)
			row.prop(VRayExporter, 'materialListShowPreview', text="",  icon=expandIcon, emboss=False)
			row.label(text="Show Preview")

			if VRayExporter.materialListShowPreview:
					material = self.getMaterial(context)
					if material:
						box.template_preview(material, show_buttons=True)

		self.layout.operator('vray.new_material', text="New Material", icon='MATERIAL')

		self.layout.template_list("VRayListMaterials", "", bpy.data, 'materials', VRayExporter, 'materialListIndex', rows=15)
		self.layout.separator()

		material = self.getMaterial(context)
		if material:
			split = self.layout.split()

			col = split.column()
			col.prop(material, 'name')

			row = col.row(align=True)
			row.label("Node Tree:")

			op = row.operator("vray.sync_ntree_name", icon='SYNTAX_OFF', text="")
			op.material = material

			row.prop(material.vray, 'ntree', text="", icon='NODETREE')


class VRayPanelLightLister(classes.VRayRenderLayersPanel):
	bl_label   = "Lights"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()

		if bpy.data.lamps:
			for lamp in bpy.data.lamps:
				VRayLight = lamp.vray
				VRayScene = context.scene.vray

				lightPluginName = LibUtils.GetLightPluginName(lamp)

				lightPropGroup = getattr(VRayLight, lightPluginName)

				sub_t = col.row()
				sub_t.label(text=" %s" % lamp.name, icon='LAMP_%s' % lamp.type)

				if lightPluginName == 'SunLight':
					sub = col.row()

					sub.prop(lightPropGroup, 'enabled', text="")

					r = sub.row()
					r.scale_x = 0.4
					r.prop(lightPropGroup, 'filter_color',   text="")

					sub.prop(lightPropGroup, 'intensity_multiplier', text="")
					sub.prop(lightPropGroup, 'shadow_subdivs',       text="")
				else:
					sub = col.row()
					sub.prop(lightPropGroup, 'enabled', text="")
					sub.prop(lightPropGroup, 'color',   text="")
					sub.prop(lightPropGroup, 'intensity', text="")
					if hasattr(lightPropGroup, 'subdivs'):
						sub.prop(lightPropGroup, 'subdivs', text="")
					if hasattr(lightPropGroup, 'shadowSubdivs'):
						sub.prop(lightPropGroup, 'shadowSubdivs', text="")
		else:
			col.label(text="Nothing in bpy.data.lamps...")


class VRayPanelIncluder(classes.VRayRenderLayersPanel):
	bl_label   = "Include *.vrscene"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		VRayScene = context.scene.vray
		Includer  = VRayScene.Includer
		self.layout.prop(Includer, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		layout= self.layout

		row= layout.row()

		vs= context.scene.vray
		module= vs.Includer

		layout.active= module.use

		row.template_list("VRayListUse", "", module, 'nodes', module, 'nodes_selected', rows=5)

		col= row.column()
		sub= col.row()
		subsub= sub.column(align=True)
		subsub.operator('vray.includer_add',    text="", icon="ZOOMIN")
		subsub.operator('vray.includer_remove', text="", icon="ZOOMOUT")
		sub= col.row()
		subsub= sub.column(align=True)
		subsub.operator("vray.includer_up",   icon='MOVE_UP_VEC',   text="")
		subsub.operator("vray.includer_down", icon='MOVE_DOWN_VEC', text="")

		if module.nodes_selected >= 0 and len(module.nodes) > 0:
			render_node= module.nodes[module.nodes_selected]

			layout.separator()

			layout.prop(render_node, 'name')
			layout.prop(render_node, 'scene')


class VRayPanelExportSets(classes.VRayRenderLayersPanel):
	bl_label   = "Export Sets"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout = self.layout

		VRayScene = context.scene.vray
		VRayExporter  = VRayScene.Exporter
		ExportSets    = VRayScene.ExportSets

		def renderExportSetItem(layout, item):
			layout.prop(item, 'name')
			layout.separator()
			layout.prop(item, 'dirpath')
			layout.prop(item, 'filename')
			layout.prop_search(item,     'group',
							   bpy.data, 'groups',
							   text="Group")
			layout.prop(item, 'use_animation')
			if item.use_animation == 'MANUAL':
				row = layout.row()
				row.prop(item, 'frame_start')
				row.prop(item, 'frame_end')
			layout.separator()

		classes.DrawListWidget(layout, context.scene, 'vray.ExportSets', 'VRayListUse',
			"Export Set", itemRenderFunc=renderExportSetItem)

		layout.separator()
		expLayout = layout.box().column()
		expLayout.label("Export:")
		expLayout.active = len(ExportSets.list_items) and ExportSets.list_item_selected >= 0
		expLayout.prop(ExportSets, 'generate_preview')
		expLayout.prop(ExportSets, 'max_preview_faces')
		expLayout.separator()
		row = expLayout.row(align=True)
		row.operator("vray.expset_export_selected", text="Selected")
		row.operator("vray.expset_export_all",      text="All")


def GetRegClasses():
	return (
		VRayPanelMaterials,
		VRayPanelMiscTools,
		VRayPanelNodeTrees,
		VRayPanelLightLister,
		VRayPanelIncluder,
		VRayPanelExportSets,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

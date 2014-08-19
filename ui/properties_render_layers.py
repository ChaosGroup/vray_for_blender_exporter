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
		box.label("Migration")
		box.operator("vray.convert_scene", icon='NODETREE')
		box.prop(VRayConverter, 'convert_from')


class VRayPanelNodeTrees(classes.VRayRenderLayersPanel):
	bl_label   = "Node Trees"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		VRayExporter = context.scene.vray.Exporter

		self.layout.template_list("VRayListNodeTrees", "", bpy.data, 'node_groups', VRayExporter, 'ntreeListIndex', rows = 4)
		self.layout.operator("vray.del_nodetree", text="Delete Selected Nodetree", icon="ZOOMOUT")

		box = self.layout.box()
		box.prop(VRayExporter, 'ntreeExportDirectory', text="Path")
		box.separator()
		box.operator("vray.export_nodetree", text="Export Selected Nodetree", icon='NODETREE')

		box = self.layout.box()
		box.label("Tools")
		box.operator("vray.restore_ntree_textures", text="Restore Textures")


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

		row.template_list("VRayListUse", "", module, 'nodes', module, 'nodes_selected', rows = 4)

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


def GetRegClasses():
	return (
		VRayPanelMiscTools,
		VRayPanelNodeTrees,
		VRayPanelLightLister,
		VRayPanelIncluder,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

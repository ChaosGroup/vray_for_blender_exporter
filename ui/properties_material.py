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

from vb25.ui import classes
from vb25.lib     import DrawUtils
from vb25.plugins import PLUGINS


class VRAY_MP_preview(classes.VRayMaterialPanel):
	bl_label = "Preview"
	
	COMPAT_ENGINES = {'VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		self.layout.template_preview(context.material, show_buttons=False)


class VRAY_MP_context_material(classes.VRayMaterialPanel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	@classmethod
	def poll(cls, context):
		engine = context.scene.render.engine
		return (context.material or context.object) and classes.PollEngine(cls, context)

	def draw(self, context):
		layout = self.layout

		mat = context.material

		ob = context.object
		slot = context.material_slot
		space = context.space_data

		if ob:
			row = layout.row()

			row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=2)

			col = row.column(align=True)
			col.operator("object.material_slot_add", icon='ZOOMIN', text="")
			col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

			col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

			if ob.mode == 'EDIT':
				row = layout.row(align=True)
				row.operator("object.material_slot_assign", text="Assign")
				row.operator("object.material_slot_select", text="Select")
				row.operator("object.material_slot_deselect", text="Deselect")

		split = layout.split(percentage=0.65)

		if ob:
			split.template_ID(ob, "active_material", new="material.new")
			row = split.row()

			if slot:
				row.prop(slot, "link", text="")
			else:
				row.label()

			if mat:
				VRayMaterial = mat.vray
				if VRayMaterial.nodetree == "":
					layout.separator()
					layout.operator("vray.add_material_nodetree", icon='NODETREE', text="Add Node Tree")
		elif mat:
			split.template_ID(space, "pin_id")

		if mat:
			layout.separator()
			layout.prop(mat, "diffuse_color", text="Viewport Color")

			VRayMaterial = mat.vray
			if VRayMaterial.nodetree:
				layout.separator()
				layout.prop_search(VRayMaterial, "nodetree", bpy.data, "node_groups")
			

class VRAY_MP_node(classes.VRayMaterialPanel):
	bl_label = "Node"

	@classmethod
	def poll(cls, context):
		material = context.material
		if not material:
			return False
		ntreeName = material.vray.nodetree
		if not ntreeName:
			return False
		if not ntreeName in bpy.data.node_groups:
			return False
		ntree = bpy.data.node_groups[ntreeName]
		if not len(ntree.nodes):
			return False
		return classes.VRayMaterialPanel.poll(context)

	def draw(self, context):
		ntree      = bpy.data.node_groups[context.material.vray.nodetree]
		activeNode = ntree.nodes[-1]

		vrayPlugin = None
		toShow     = True

		if not hasattr(activeNode, 'vray_type'):
			toShow = False
		else:
			if activeNode.vray_type == 'NONE' or activeNode.vray_plugin == 'NONE':
				toShow = False
			else:
				if not hasattr(activeNode, activeNode.vray_plugin):
					toShow = False
				pluginTypes = PLUGINS[activeNode.vray_type]

				if activeNode.vray_plugin in pluginTypes:
					vrayPlugin = pluginTypes[activeNode.vray_plugin]

		if not toShow or not vrayPlugin:
			self.layout.label(text="Selected node has no attibutes to show...")
		else:
			self.layout.label(text="Node: %s" % activeNode.name)
			self.layout.separator()
			
			dataPointer = getattr(activeNode, activeNode.vray_plugin)

			if hasattr(vrayPlugin, 'gui'):
				vrayPlugin.gui(context, self.layout, dataPointer)
			else:
				DrawUtils.Draw(context, self.layout, dataPointer, vrayPlugin.PluginParams)		


# class VRAY_MP_outline(classes.VRayMaterialPanel):
# 	bl_label   = "Outline"
# 	bl_options = {'DEFAULT_CLOSED'}

# 	@classmethod
# 	def poll(cls, context):
# 		material = context.material
# 		if material is None:
# 			return False
# 		VRayMaterial = material.vray
# 		if VRayMaterial.nodetree:
# 			return False
# 		return engine_poll(__class__, context)

# 	def draw_header(self, context):
# 		ma= context.material
# 		VRayMaterial= ma.vray
# 		VolumeVRayToon= VRayMaterial.VolumeVRayToon
# 		self.layout.prop(VolumeVRayToon, 'use', text="")

# 	def draw(self, context):
# 		wide_ui= context.region.width > classes.narrowui
# 		layout= self.layout

# 		ob= context.object
# 		ma= context.material

# 		VRayMaterial= ma.vray
# 		VolumeVRayToon= VRayMaterial.VolumeVRayToon

# 		layout.active= VolumeVRayToon.use

# 		PLUGINS['SETTINGS']['SettingsEnvironment'].draw_VolumeVRayToon(context, layout, VRayMaterial)


def GetRegClasses():
	return (
		VRAY_MP_preview,
		VRAY_MP_context_material,
		VRAY_MP_node,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

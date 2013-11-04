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

from vb25.ui      import classes
from vb25.plugins import PLUGINS


class VRAY_SP_includer(classes.VRayScenePanel):
	bl_label   = "Includes"
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

		# layout.separator()
		# box= layout.box()
		# box.label(text="Enable options export in curent scene:")
		# split = box.split()
		# col= split.column()
		# col.prop(module, 'setting', text="Use export scene setting")
		# col.prop(module, 'camera', text="Use export camera")
		# col.prop(module, 'materials', text="Use export materials")
		
		# col.prop(module, 'environment', text="Use export environment")
		# col.prop(module, 'lights', text="Use export lights")
		# col.prop(module, 'colorMapping_standalone', text="Use Color Mapping")
		# col.prop(module, 'geometry', text="Use export geometry")
		# col.prop(module, 'scene_nodes', text="Use Vray Nodes")


class VRAY_SP_tools(classes.VRayScenePanel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		VRayExporter = context.scene.vray.Exporter

		layout= self.layout

		box = layout.box()
		box.label(text="Scene:")
		split = box.split()
		col = split.column()
		col.operator("vray.settings_to_text", icon='TEXT')

		layout.separator()

		box = layout.box()
		box.label(text="Object:")
		split = box.split()
		col=  split.column()
		col.operator("vray.copy_linked_materials", icon='MATERIAL')

		layout.separator()
		layout.label(text="Scene Node Trees:")
		layout.template_list("VRayListNodeTrees", "", bpy.data, 'node_groups', VRayExporter, 'ntreeListIndex', rows = 4)


class VRAY_SP_lights_tweaker(classes.VRayScenePanel):
	bl_label   = "Lights"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()

		if bpy.data.lamps:
			for lamp in bpy.data.lamps:
				VRayLamp= lamp.vray
				sub_t= col.row()
				sub_t.label(text= " %s" % lamp.name, icon='LAMP_%s' % lamp.type)

				sub= col.row(align= True)
				sub_c= sub.row()
				sub_c.prop(VRayLamp, 'enabled', text="")
				sub_c.prop(lamp,     'color',     text="")
				sub_v= sub.row()
				sub_v.prop(VRayLamp, 'intensity', text="")
				sub_v.prop(VRayLamp, 'subdivs',   text="")
		else:
			col.label(text="Nothing in bpy.data.lamps...")


def GetRegClasses():
	return (
		VRAY_SP_tools,
		VRAY_SP_includer,
		VRAY_SP_lights_tweaker,
	)


def register():
	from bl_ui import properties_scene
	for member in dir(properties_scene):
		subclass = getattr(properties_scene, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.add(compatEngine)
		except:
			pass
	del properties_scene

	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	from bl_ui import properties_scene
	for member in dir(properties_scene):
		subclass = getattr(properties_scene, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.remove(compatEngine)
		except:
			pass
	del properties_scene

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

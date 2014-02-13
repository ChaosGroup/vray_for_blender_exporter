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

from pynodes_framework import idref

from vb30.ui import classes


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

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		layout = self.layout

		VRayObject = context.object.vray

		layout.prop(VRayObject, 'fade_radius')


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


def GetRegClasses():
	return (
		VRAY_OBP_context_node,
		VRAY_OBP_render,
		VRAY_OBP_VRayPattern,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

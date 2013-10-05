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

from bpy.types import Brush, Lamp, Material, Object, ParticleSettings, Texture, World

from vb25.ui import classes

from bl_ui.properties_texture import context_tex_datablock

from bl_ui import properties_texture
for compatEngine in classes.VRayEngines:
	properties_texture.TEXTURE_PT_image.COMPAT_ENGINES.add(compatEngine)
	properties_texture.TEXTURE_PT_voxeldata.COMPAT_ENGINES.add(compatEngine)
del properties_texture


class VRAY_TP_context(classes.VRayTexturePanel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}
	
	@classmethod
	def poll(cls, context):
		if not hasattr(context, "texture_slot"):
			return False

		return ((context.material or context.world or context.lamp or context.brush or context.texture or context.particle_system or isinstance(context.space_data.pin_id, bpy.types.ParticleSettings))
				and classes.PollEngine(cls, context))

	def draw(self, context):
		layout = self.layout
		slot = context.texture_slot
		node = context.texture_node
		space = context.space_data
		tex = context.texture
		idblock = context_tex_datablock(context)
		pin_id = space.pin_id

		if space.use_pin_id and not isinstance(pin_id, bpy.types.Texture):
			idblock = id_tex_datablock(pin_id)
			pin_id = None

		if not space.use_pin_id:
			layout.prop(space, "texture_context", expand=True)

		tex_collection = (pin_id is None) and (node is None) and (not isinstance(idblock, bpy.types.Brush))

		if tex_collection:
			row = layout.row()

			row.template_list("TEXTURE_UL_texslots", "", idblock, "texture_slots", idblock, "active_texture_index", rows=2)

			col = row.column(align=True)
			col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
			col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
			col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

		if tex_collection:
			layout.template_ID(idblock, "active_texture", new="texture.new")
		elif node:
			layout.template_ID(node, "texture", new="texture.new")
		elif idblock:
			layout.template_ID(idblock, "texture", new="texture.new")

		if pin_id:
			layout.template_ID(space, "pin_id")

		if tex:
			split = layout.split(percentage=0.2)

			if slot and tex.use_nodes:
				split.label(text="Output:")
				split.prop(slot, "output_node", text="")

			if not tex.use_nodes:
				layout.prop(tex, 'type', text="Texture")
				if tex.type == 'VRAY':
					layout.prop(tex.vray, 'type', text="Type")


class VRAY_TP_preview(classes.VRayTexturePanel):
	bl_label = "Preview"
	
	@classmethod
	def poll(cls, context):
		tex= context.texture

		if not tex:
			return False

		if tex.type == 'VRAY' and context.scene.render.engine == 'VRAY_RENDER':
			return False

		return classes.VRayTexturePanel.poll(context)

	def draw(self, context):
		layout= self.layout

		tex= context.texture
		slot= getattr(context, "texture_slot", None)
		idblock= context_tex_datablock(context)

		if idblock:
			layout.template_preview(tex, parent= idblock, slot= slot)
		else:
			layout.template_preview(tex, slot= slot)


# class VRAY_TP_displacement(classes.VRayTexturePanel):
# 	bl_label = "Displacement"
	
# 	@classmethod
# 	def poll(cls, context):
# 		idblock= context_tex_datablock(context)
# 		if not type(idblock) == bpy.types.Material:
# 			return False

# 		texture_slot= getattr(context,'texture_slot',None)
# 		if not texture_slot:
# 			return False

# 		texture= texture_slot.texture
# 		if not texture:
# 			return False

# 		VRaySlot= texture.vray_slot
# 		return VRaySlot.map_displacement and engine_poll(cls, context)

# 	def draw(self, context):
# 		layout= self.layout
# 		wide_ui= context.region.width > classes.narrowui

# 		texture_slot= getattr(context,'texture_slot',None)
# 		texture= texture_slot.texture if texture_slot else context.texture

# 		if texture:
# 			VRaySlot= texture.vray_slot

# 			if VRaySlot:
# 				GeomDisplacedMesh= VRaySlot.GeomDisplacedMesh

# 				split= layout.split()
# 				col= split.column()
# 				col.prop(GeomDisplacedMesh, 'displacement_shift', slider=True)
# 				col.prop(GeomDisplacedMesh, 'water_level', slider=True)
# 				col.prop(GeomDisplacedMesh, 'resolution')
# 				col.prop(GeomDisplacedMesh, 'precision')
# 				if wide_ui:
# 					col= split.column()
# 				col.prop(GeomDisplacedMesh, 'keep_continuity')
# 				col.prop(GeomDisplacedMesh, 'filter_texture')
# 				if GeomDisplacedMesh.filter_texture:
# 					col.prop(GeomDisplacedMesh, 'filter_blur')
# 				col.prop(GeomDisplacedMesh, 'use_bounds')
# 				if GeomDisplacedMesh.use_bounds:
# 					sub= col.column(align= True)
# 					sub.prop(GeomDisplacedMesh, 'min_bound', text="Min", slider= True)
# 					sub.prop(GeomDisplacedMesh, 'max_bound', text="Max", slider= True)

# 				split= layout.split()
# 				col= split.column()
# 				col.prop(GeomDisplacedMesh, 'use_globals')
# 				if not GeomDisplacedMesh.use_globals:
# 					split= layout.split()
# 					col= split.column()
# 					col.prop(GeomDisplacedMesh, 'edge_length')
# 					col.prop(GeomDisplacedMesh, 'max_subdivs')
# 					if wide_ui:
# 						col= split.column()
# 					col.prop(GeomDisplacedMesh, 'view_dep')
# 					col.prop(GeomDisplacedMesh, 'tight_bounds')


class VRAY_TP_bitmap(classes.VRayTexturePanel):
	bl_label = "Bitmap"

	@classmethod
	def poll(cls, context):
		if not classes.PollEngine(cls, context):
			return False

		tex= context.texture
		if not tex:
			return False

		return (tex.type == 'IMAGE' and tex.image)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		slot= getattr(context,'texture_slot',None)
		tex= slot.texture if slot else context.texture

		BitmapBuffer= tex.image.vray.BitmapBuffer

		split= layout.split()
		col= split.column()
		col.prop(BitmapBuffer, 'color_space')

		split= layout.split()
		col= split.column()
		col.prop(BitmapBuffer, 'filter_type', text="Filter")
		if BitmapBuffer.filter_type != 'NONE':
			col.prop(BitmapBuffer, 'filter_blur')
		if BitmapBuffer.filter_type == 'MIPMAP':
			col.prop(BitmapBuffer, 'interpolation', text="Interp.")
		if wide_ui:
			col= split.column()
		col.prop(BitmapBuffer, 'use_input_gamma')
		if not BitmapBuffer.use_input_gamma:
			col.prop(BitmapBuffer, 'gamma')
			#col.prop(BitmapBuffer, 'gamma_correct')
		col.prop(BitmapBuffer, 'allow_negative_colors')
		col.prop(BitmapBuffer, 'use_data_window')


def GetRegClasses():
	return (
		VRAY_TP_context,
		VRAY_TP_preview,
		VRAY_TP_bitmap,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

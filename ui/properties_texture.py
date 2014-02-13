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

from bpy.types import Brush, Lamp, Material, Object, ParticleSettings, Texture, World

from vb30.ui import classes

from bl_ui.properties_texture import context_tex_datablock


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


def GetRegClasses():
	return (
		# VRAY_TP_context,
	)


def register():
	from bl_ui import properties_texture
	for member in dir(properties_texture):
		subclass = getattr(properties_texture, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.add(compatEngine)
		except:
			pass
	del properties_texture

	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	from bl_ui import properties_texture
	for member in dir(properties_texture):
		subclass = getattr(properties_texture, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.remove(compatEngine)
		except:
			pass
	del properties_texture

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

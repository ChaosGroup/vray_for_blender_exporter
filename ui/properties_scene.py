'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Blender modules '''
import bpy

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *
from vb25.plugins import *


class VRAY_SP_effects(VRayScenePanel, bpy.types.Panel):
	bl_label   = "Effects"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		VRayScene= context.scene.vray
		self.layout.prop(VRayScene.VRayEffects, 'use', text="")

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray
		VRayEffects= VRayScene.VRayEffects

		layout.active= VRayEffects.use

		split= layout.split()
		row= split.row()
		row.template_list(VRayEffects, 'effects',
						  VRayEffects, 'effects_selected',
						  rows= 4)
		col= row.column()
		sub= col.row()
		subsub= sub.column(align=True)
		subsub.operator('vray.effect_add',    text="", icon="ZOOMIN")
		subsub.operator('vray.effect_remove', text="", icon="ZOOMOUT")

		if VRayEffects.effects_selected >= 0:
			layout.separator()

			effect= VRayEffects.effects[VRayEffects.effects_selected]

			if wide_ui:
				split= layout.split(percentage=0.2)
			else:
				split= layout.split()
			col= split.column()
			col.label(text="Name:")
			if wide_ui:
				col= split.column()
			row= col.row(align=True)
			row.prop(effect, 'name', text="")
			row.prop(effect, 'use', text="")

			if wide_ui:
				split= layout.split(percentage=0.2)
			else:
				split= layout.split()
			col= split.column()
			col.label(text="Type:")
			if wide_ui:
				col= split.column()
			col.prop(effect, 'type', text="")

			layout.separator()

			# Box border
			layout= layout.box()

			if effect.type == 'FOG':
				PLUGINS['SETTINGS']['SettingsEnvironment'].draw_EnvironmentFog(context, layout, effect)

			elif effect.type == 'TOON':
				PLUGINS['SETTINGS']['SettingsEnvironment'].draw_VolumeVRayToon(context, layout, effect)


class VRAY_SP_tools(VRayScenePanel, bpy.types.Panel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray

		split= layout.split()
		col= split.column()
		col.operator("vray.convert_materials", icon="MATERIAL")
		col.operator("vray.settings_to_text", icon="RENDER_STILL")

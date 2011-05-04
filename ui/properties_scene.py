'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Wednesday, 04 May 2011 [15:07]"

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


class VRAY_SP_tools(VRayScenePanel, bpy.types.Panel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		layout= self.layout

		box= layout.box()
		box.label(text="Scene:")
		split= box.split()
		col= split.column()
		col.operator("vray.convert_materials", icon='MATERIAL')
		if wide_ui:
			col= split.column()
		col.operator("vray.settings_to_text", icon='TEXT')

		layout.separator()

		box= layout.box()
		box.label(text="Object:")
		split= box.split()
		col= split.column()
		col.operator("vray.copy_linked_materials", icon='MATERIAL')

		# layout.separator()

		# layout.operator("vray.update", icon='SCENE_DATA')


class VRAY_SP_lights_tweaker(VRayScenePanel, bpy.types.Panel):
	bl_label   = "Lights"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		wide_ui= context.region.width > narrowui

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
			col.label(text= "Nothing in bpy.data.lamps...")

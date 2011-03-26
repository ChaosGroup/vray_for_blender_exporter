'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Saturday, 26 March 2011 [21:45]"

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

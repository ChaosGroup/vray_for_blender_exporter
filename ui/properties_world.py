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
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


class VRAY_WP_environment(VRayWorldPanel, bpy.types.Panel):
	bl_label = "Environment"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout

		VRayWorld= context.world.vray

		split= layout.split()
		col= split.column()
		col.label(text="Background:")
		
		row= layout.row(align=True)
		row.prop(VRayWorld, 'bg_color_mult', text="Mult", slider=True)
		row.prop(VRayWorld, 'bg_color', text="")

		split= layout.split()
		col= split.column()
		col.label(text="Override:")

		split= layout.split()
		col= split.column()
		factor_but(col, VRayWorld, 'gi_override',         'gi_color_mult',         color= 'gi_color',         label= "GI")
		factor_but(col, VRayWorld, 'reflection_override', 'reflection_color_mult', color= 'reflection_color', label= "Reflection")
		factor_but(col, VRayWorld, 'refraction_override', 'refraction_color_mult', color= 'refraction_color', label= "Refraction")

		layout.separator()
		layout.prop(VRayWorld, 'global_light_level')


bpy.utils.register_class(VRAY_WP_environment)

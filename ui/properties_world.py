'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class VRayWorld(bpy.types.PropertyGroup):
	pass

bpy.types.World.vray= PointerProperty(
	name= "V-Ray World Settings",
	type=  VRayWorld,
	description= "V-Ray world settings."
)


'''
  SettingsEnvironment
'''

VRayWorld.bg_color= FloatVectorProperty(
	name= "Background color",
	description= "Background color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayWorld.bg_color_mult= FloatProperty(
	name= "Background color multiplier",
	description= "Background color multiplier.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 2,
	default= 1.0
)

VRayWorld.gi_override= BoolProperty(
	name= "Override color for GI",
	description= "Override color for GI.",
	default= False
)

VRayWorld.gi_color= FloatVectorProperty(
	name= "GI color",
	description= "GI (skylight) color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayWorld.gi_color_mult= FloatProperty(
	name= "GI color multiplier",
	description= "GI color multiplier.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 2,
	default= 1.0
)

VRayWorld.reflection_override= BoolProperty(
	name= "Override color for reflection",
	description= "Override color for reflection.",
	default= False
)

VRayWorld.reflection_color= FloatVectorProperty(
	name= "Reflection color",
	description= "Reflection (skylight) color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayWorld.reflection_color_mult= FloatProperty(
	name= "Reflection color multiplier",
	description= "Reflection color multiplier.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 2,
	default= 1.0
)

VRayWorld.refraction_override= BoolProperty(
	name= "Override color for refraction",
	description= "Override color for refraction.",
	default= False
)

VRayWorld.refraction_color= FloatVectorProperty(
	name= "Refraction color",
	description= "Refraction (skylight) color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayWorld.refraction_color_mult= FloatProperty(
	name= "Refraction color multiplier",
	description= "Refraction color multiplier.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 2,
	default= 1.0
)



'''
  GUI
'''
narrowui= 200


def base_poll(cls, context):
	rd= context.scene.render
	return (context.world) and (rd.engine in cls.COMPAT_ENGINES)


class WorldButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'world'


class WORLD_PT_vray_environment(WorldButtonsPanel, bpy.types.Panel):
	bl_label = "Environment"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		wo= context.world.vray

		def factor_but(layout, active, toggle, factor, color, label= None):
			row= layout.row(align=False)
			row.prop(wo, toggle, text="")
			sub= row.row()
			sub.active= active
			if(label):
				sub.prop(wo, factor, slider=True, text=label)
			else:
				sub.prop(wo, factor, slider=True)
			sub.prop(wo, color, text="")

		split= layout.split()
		col= split.column()
		col.label(text="Background:")
		
		split= layout.split()
		col= split.column()
		col.prop(wo, 'bg_color_mult', text="Mult", slider=True)
		col= split.column()
		col.prop(wo, 'bg_color', text="")

		split= layout.split()
		col= split.column()
		col.label(text="Override:")

		split= layout.split()
		col= split.column()
		factor_but(col, wo.gi_override,         'gi_override',         'gi_color_mult',         'gi_color',         "GI")
		factor_but(col, wo.reflection_override, 'reflection_override', 'reflection_color_mult', 'reflection_color', "Reflection")
		factor_but(col, wo.refraction_override, 'refraction_override', 'refraction_color_mult', 'refraction_color', "Refraction")

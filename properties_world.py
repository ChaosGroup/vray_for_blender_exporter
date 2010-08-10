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


import bpy


FloatProperty= bpy.types.World.FloatProperty
IntProperty= bpy.types.World.IntProperty
BoolProperty= bpy.types.World.BoolProperty
VectorProperty= bpy.types.World.FloatVectorProperty


'''
  SettingsEnvironment
'''
VectorProperty(
	attr="vray_env_bg_color",
	name="Background color",
	description="Background color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

FloatProperty(
	attr= "vray_env_bg_color_mult", 
	name= "Background color multiplier", 
	description= 'Background color multiplier.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 2.0, 
	precision= 2, 
	default= 1.0
)

BoolProperty( 
	attr= "vray_env_gi_override", 
	name= "Override color for GI", 
	description= 'Override color for GI.', 
	default= False
)

VectorProperty(
	attr="vray_env_gi_color",
	name="GI color",
	description="GI (skylight) color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

FloatProperty(
	attr= "vray_env_gi_color_mult", 
	name= "GI color multiplier", 
	description= 'GI color multiplier.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 2.0, 
	precision= 2, 
	default= 1.0
)

BoolProperty(
	attr= "vray_env_reflection_override",
	name= "Override color for reflection",
	description= 'Override color for reflection.',
	default= False
)

VectorProperty(
	attr="vray_env_reflection_color",
	name="REFLECTION color",
	description="REFLECTION (skylight) color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

FloatProperty(
	attr= "vray_env_reflection_color_mult", 
	name= "Reflection color multiplier", 
	description= 'Reflection color multiplier.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 2.0, 
	precision= 2, 
	default= 1.0
)

BoolProperty(
	attr= "vray_env_refraction_override",
	name= "Override color for refraction",
	description= 'Override color for refraction.',
	default= False
)

VectorProperty(
	attr="vray_env_refraction_color",
	name="REFRACTION color",
	description="REFRACTION (skylight) color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

FloatProperty(
	attr= "vray_env_refraction_color_mult", 
	name= "Refraction color multiplier", 
	description= 'Refraction color multiplier.', 
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
		
		wo= context.world

		split= layout.split()
		col= split.column()
		col.label(text="Background:")
		
		split= layout.split()
		col= split.column()
		col.prop(wo, "vray_env_bg_color_mult", text="Mult", slider=True)
		col= split.column()
		col.prop(wo, "vray_env_bg_color", text="")

		split= layout.split()
		col= split.column()
		col.label(text="Override:")

		split= layout.split()
		col= split.column()
		factor_but(col, wo.vray_env_gi_override,         'vray_env_gi_override',         'vray_env_gi_color_mult',         'vray_env_gi_color',         "GI")
		factor_but(col, wo.vray_env_reflection_override, 'vray_env_reflection_override', 'vray_env_reflection_color_mult', 'vray_env_reflection_color', "Reflection")
		factor_but(col, wo.vray_env_refraction_override, 'vray_env_refraction_override', 'vray_env_refraction_color_mult', 'vray_env_refraction_color', "Refraction")


# bpy.types.register(WORLD_PT_vray_environment)

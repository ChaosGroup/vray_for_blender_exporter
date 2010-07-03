'''

 V-Ray/Blender 2.5.8

 http://vray.cgdo.ru

 Started:       29 Aug 2009
 Last Modified: 21 Mar 2010

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


narrowui = 180


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
	soft_max= 10.0, 
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
	soft_max= 10.0, 
	precision= 2, 
	default= 1.0
)



class WorldButtonsPanel(bpy.types.Panel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'world'

	def poll(self, context):
		engine= context.scene.render.engine
		return (context.world) and (engine in self.COMPAT_ENGINES)


class WORLD_PT_vray_environment(WorldButtonsPanel):
	bl_label = "Environment"

	COMPAT_ENGINES = set(['VRAY_RENDER'])

	def draw(self, context):
		layout= self.layout
		
		wo= context.world

		split= layout.split()
		colL= split.column()
		colL.label(text="Background")
		
		split= layout.split()
		colL= split.column()
		colL.prop(wo, "vray_env_bg_color_mult", text="Mult")

		colR= split.column()
		colR.prop(wo, "vray_env_bg_color", text="")

		split= layout.split()
		colL= split.column()
		colL.prop(wo, "vray_env_gi_override")

		split= layout.split()
		sub= split.row()
		sub.active= wo.vray_env_gi_override
		colL= sub.column()
		colL.prop(wo, "vray_env_gi_color_mult", text="Mult")
		colR= sub.column()
		colR.prop(wo, "vray_env_gi_color", text="")



bpy.types.register(WORLD_PT_vray_environment)

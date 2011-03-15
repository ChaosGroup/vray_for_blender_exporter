'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 15 March 2011 [21:22]"

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
from vb25.ui.ui import *


class VRayFur(bpy.types.PropertyGroup):
	width= bpy.props.FloatProperty(
		name= "Width",
		description= "Hair thin.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 0.01,
		precision= 5,
		default= 0.02
	)

class VRayParticleSettings(bpy.types.PropertyGroup):
	pass

bpy.utils.register_class(VRayFur)
bpy.utils.register_class(VRayParticleSettings)

bpy.types.ParticleSettings.vray= bpy.props.PointerProperty(
	name= "V-Ray Particle Settings",
	type=  VRayParticleSettings,
	description= "V-Ray Particle settings."
)

VRayParticleSettings.VRayFur= bpy.props.PointerProperty(
	name= "V-Ray Fur Settings",
	type=  VRayFur,
	description= "V-Ray Fur settings."
)


import properties_particle
for member in dir(properties_particle):
	subclass= getattr(properties_particle, member)
	try:
		subclass.COMPAT_ENGINES.add('VRAY_RENDER')
		subclass.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
	except:
		pass
del properties_particle


class VRAY_PP_hair(VRayParticlePanel, bpy.types.Panel):
	bl_label       = "Fur"
	bl_options     = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return super().poll(context) and context.particle_system.settings.type == 'HAIR'

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		particle_settings= context.particle_system.settings
		
		VRayFur= particle_settings.vray.VRayFur

		layout.prop(VRayFur, 'width')

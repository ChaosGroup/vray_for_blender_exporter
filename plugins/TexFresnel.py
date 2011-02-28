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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''

TYPE= 'TEXTURE'
ID=   'TEXFRESNEL'
NAME= 'Fresnel'
PLUG= 'TexFresnel'
DESC= "TODO."
PID=  2

PARAMS= (
	'fresnel_ior',
	'refract_ior',
	'white_color',
	'black_color'
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class TexFresnel(bpy.types.PropertyGroup):
    pass

def add_properties(VRayTexture):
	VRayTexture.TexFresnel= PointerProperty(
		name= "TexFresnel",
		type=  TexFresnel,
		description= "V-Ray TexFresnel settings"
	)

	TexFresnel.fresnel_ior= FloatProperty(
		name= "Fresnel IOR",
		description= "Fresnel ior.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.55
	)

	TexFresnel.refract_ior= FloatProperty(
		name= "Refract IOR",
		description= "Refraction ior of the underlying surface; this is ignored if the surface has a volume shader (the volume IOR is used).",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.55
	)

	TexFresnel.white_color= FloatVectorProperty(
		name= "Front color",
		description= "Refraction (front) color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	TexFresnel.black_color= FloatVectorProperty(
		name= "Side color",
		description= "Reflection (side) color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)


def write(ofile, sce, params):
	slot= params.get('slot')
	tex= params.get('texture')

	tex_name= params['name'] if 'name' in params else get_name(tex, "Texture")

	vtex= tex.vray.TexFresnel

	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'sky_model':
			ofile.write("\n\t%s= %s;"%(param, SKY_MODEL[vtex.sky_model]))
		elif param == 'sun':
			if(sun_light):
				ofile.write("\n\t%s= %s;"%(param, sun_light))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vtex, param))))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
narrowui= 200


class TexFresnelPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_TexFresnel(TexFresnelPanel, bpy.types.Panel):
	bl_label = NAME

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		if not tex:
			return False
		vtex= tex.vray
		engine= context.scene.render.engine
		return ((tex and tex.type == 'VRAY' and vtex.type == ID) and (engine in __class__.COMPAT_ENGINES))
	
	def draw(self, context):
		tex= context.texture
		vtex= tex.vray.TexFresnel
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop(vtex, 'white_color')
		if wide_ui:
			col= split.column()
		col.prop(vtex, 'black_color')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(vtex, 'fresnel_ior')
		if wide_ui:
			col= split.column()
		col.prop(vtex, 'refract_ior')
	

bpy.utils.register_class(TEXTURE_PT_TexFresnel)

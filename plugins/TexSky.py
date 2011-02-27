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

ID=   'TEXSKY'
NAME= 'Sky'
PLUG= 'TexSky'
DESC= "TODO."
PID=  3

PARAMS= (
	'auto',
	#'transform',
	#'target_transform',
	'turbidity',
	'ozone',
	'water_vapour',
	'intensity_multiplier',
	'size_multiplier',
	#'up_vector',
	'invisible',
	'horiz_illum',
	'sky_model',
	'sun'
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


def add_properties(VRayTexture):
	class TexSky(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(TexSky)

	VRayTexture.TexSky= PointerProperty(
		name= "TexSky",
		type=  TexSky,
		description= "V-Ray TexSky settings"
	)

	TexSky.auto= BoolProperty(
		name= "Take settings from Sun",
		description= "Take settings from Sun automatically.",
		default= True
	)

	TexSky.turbidity= FloatProperty(
		name= "Turbidity",
		description= "TODO.",
		min= 2.0,
		max= 100.0,
		soft_min= 2.0,
		soft_max= 10.0,
		precision= 3,
		default= 3.0
	)

	TexSky.ozone= FloatProperty(
		name= "Ozone",
		description= "TODO.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.35
	)

	TexSky.water_vapour= FloatProperty(
		name= "Water vapour",
		description= "TODO.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 2
	)

	TexSky.intensity_multiplier= FloatProperty(
		name= "Intensity mult.",
		description= "TODO.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	TexSky.size_multiplier= FloatProperty(
		name= "Size mult.",
		description= "TODO.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	TexSky.invisible= BoolProperty(
		name= "Invisible",
		description= "TODO.",
		default= False
	)

	TexSky.sun= StringProperty(
		name= "Sun",
		description= "Sun lamp.",
		default= ""
	)

	TexSky.horiz_illum= FloatProperty(
		name= "Horiz illumination",
		description= "TODO.",
		min= 0.0,
		max= 100000.0,
		soft_min= 0.0,
		soft_max= 10000.0,
		precision= 0,
		default= 25000
	)

	TexSky.sky_model= EnumProperty(
		name= "Sky model",
		description= "Sky model.",
		items= (
			('CIEOVER',"CIE Overcast",""),
			('CIECLEAR',"CIE Clear",""),
			('PREETH',"Preetham et al.","")
		),
		default= 'PREETH'
	)


def write(ofile, sce, params):
	SKY_MODEL= {
		'CIEOVER'  : 2,
		'CIECLEAR' : 1,
		'PREETH'   : 0
	}

	slot= params.get('slot')
	tex= params.get('texture')

	tex_name= params['name'] if 'name' in params else get_name(tex, "Texture")

	vtex= getattr(tex.vray, PLUG)

	# Find Sun lamp
	sun_light= None
	if vtex.auto:
		for ob in sce.objects:
			if ob.type == 'LAMP':
				if ob.data.type == 'SUN' and ob.data.vray.direct_type == 'SUN':
					sun_light= get_name(ob,"Light")
					break
	else:
		if vtex.sun:
			if vtex.sun in bpy.data.objects:
				sun_light= get_name(bpy.data.objects[vtex.sun],"Light")

	# Write output
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'sky_model':
			ofile.write("\n\t%s= %s;"%(param, SKY_MODEL[vtex.sky_model]))
		elif param == 'sun':
			if sun_light:
				ofile.write("\n\t%s= %s;"%(param, sun_light))
			else:
				continue
		elif param == 'auto':
			pass
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vtex, param))))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
narrowui= 200


class TexSkyTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_TexSky(TexSkyTexturePanel, bpy.types.Panel):
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
		vtex= getattr(tex.vray, PLUG)
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop(vtex, 'auto')

		split= layout.split()
		split.active= not vtex.auto
		col= split.column()
		col.prop(vtex, 'sky_model')
		if not vtex.auto:
			col.prop_search(vtex, 'sun', context.scene, 'objects')

		split= layout.split()
		split.active= not vtex.auto
		col= split.column()
		col.prop(vtex, 'turbidity')
		col.prop(vtex, 'ozone')
		col.prop(vtex, 'intensity_multiplier')
		col.prop(vtex, 'size_multiplier')
		if wide_ui:
			col= split.column()
		col.prop(vtex, 'invisible')
		col.prop(vtex, 'horiz_illum')
		col.prop(vtex, 'water_vapour')
		

bpy.utils.register_class(TEXTURE_PT_TexSky)

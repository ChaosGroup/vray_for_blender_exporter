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

ID=   'TEXFALLOFF'
PLUG= 'TexFalloff'
NAME= 'Falloff'
DESC= "TODO."
PID=  1

PARAMS= (
	'alpha_from_intensity',
	'invert',
	'invert_alpha',
	'color_mult',
	'color_offset',
	'alpha_mult',
	'alpha_offset',
	'nouvw_color',
	'color1',
	'color2',
	'type',
	'direction_type',
	'fresnel_ior',
	'dist_extrapolate',
	'dist_near',
	'dist_far',
	'explicit_dir',
	'use_blend_input'
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class TexFalloff(bpy.types.IDPropertyGroup):
    pass

def add_properties(VRayTexture):
	VRayTexture.TexFalloff= PointerProperty(
		name= "TexFalloff",
		type=  TexFalloff,
		description= "V-Ray TexFalloff settings"
	)

	TexFalloff.alpha_from_intensity= BoolProperty(
		name= "Alpha from intensity",
		description= "If true, the resulting alpha is the color intensity; otherwise the alpha is taken from the bitmap alpha",
		default= False
	)

	TexFalloff.invert= BoolProperty(
		name= "Invert",
		description= "If true, the resulting texture color will be inverted",
		default= False
	)

	TexFalloff.invert_alpha= BoolProperty(
		name= "Invert alpha",
		description= "If true and invert is on, the resulting texture alpha will be inverted too. If false, just the color will be inverted",
		default= True
	)

	TexFalloff.color_mult= FloatVectorProperty(
		name= "Color multiplier",
		description= "A multiplier for the texture color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	TexFalloff.color_offset= FloatVectorProperty(
		name= "Color offset",
		description= "An additional offset for the texture color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	TexFalloff.alpha_mult= FloatProperty(
		name= "Alpha multiplier",
		description= "A multiplier for the texture alpha",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	TexFalloff.alpha_offset= FloatProperty(
		name= "Alpha offset",
		description= "An additional offset for the texture alpha",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexFalloff.nouvw_color= FloatVectorProperty(
		name= "NoUV color",
		description= "The color when there are no valid uvw coordinates",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.5,0.5,0.5)
	)

	TexFalloff.color1= FloatVectorProperty(
		name= "Front color",
		description= "First color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	TexFalloff.color2= FloatVectorProperty(
		name= "Side color",
		description= "Second color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	TexFalloff.type= EnumProperty(
		name= "Type",
		description= "Falloff type",
		items= (
			('TA',"Towards / Away",""),
			('PP',"Perpendicular / Parallel",""),
			('FRES',"Fresnel",""),
			('SHAD',"Shadow / Light",""),
			('DIST',"Distance blend","")
		),
		default= 'TA'
	)

	TexFalloff.direction_type= EnumProperty(
		name= "Direction type",
		description= "Direction type",
		items= (
			('VIEWZ',   "View Z",           ""),
			('VIEWX',   "View X",           ""),
			('VIEWY',   "View Y",           ""),
			('EXPL',    "Explicit",         ""),
			('LX',      "Local X",          ""),
			('LY',      "Local Y",          ""),
			('LZ',      "Local Z",          ""),
			('WX',      "World X",          ""),
			('WY',      "World Y",          ""),
			('WZ',      "World Z",          ""),
		),
		default= 'VIEWZ'
	)

	TexFalloff.fresnel_ior= FloatProperty(
		name= "Fresnel IOR",
		description= "IOR for the Fresnel falloff type",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.6
	)

	TexFalloff.dist_extrapolate= BoolProperty(
		name= "Extrapolate distance",
		description= "Extrapolate for the distance blend falloff type",
		default= False
	)

	TexFalloff.dist_near= FloatProperty(
		name= "Near distance",
		description= "Near distance for the distance blend falloff type",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexFalloff.dist_far= FloatProperty(
		name= "Far distance",
		description= "Far distance for the distance blend falloff type",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 100
	)

	TexFalloff.explicit_dir= FloatVectorProperty(
		name= "Explicit direction",
		description= "Direction for the explicit direction type",
		subtype= 'DIRECTION',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,1)
	)

	TexFalloff.use_blend_input= BoolProperty(
		name= "Use \"blend\" input",
		description= "TODO",
		default= False
	)


def write(ofile, sce, tex, name= None):
	TYPE= {
		'TA':   0,
		'PP':   1,
		'FRES': 2,
		'SHAD': 3,
		'DIST': 4
	}

	DIRECTION_TYPE= {
		'VIEWZ': 0,
		'VIEWX': 1,
		'VIEWY': 2,
		'EXPL':  3,
		'LX':    4,
		'LY':    5,
		'LZ':    6,
		'WX':    7,
		'WY':    8,
		'WZ':    9
	}

	tex_name= "%s"%(get_name(tex, "Texture"))
	if name is not None:
		tex_name= name

	vtex= getattr(tex.vray, PLUG)

	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'direction_type':
			ofile.write("\n\t%s= %s;"%(param, DIRECTION_TYPE[vtex.direction_type]))
		elif param == 'type':
			ofile.write("\n\t%s= %s;"%(param, TYPE[vtex.type]))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vtex, param))))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
narrowui= 200


class TexFalloffTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_TexFalloff(TexFalloffTexturePanel, bpy.types.Panel):
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
		col.prop(vtex,'color1')
		if wide_ui:
			col= split.column()
		col.prop(vtex,'color2')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(vtex,'type')
		col.prop(vtex,'direction_type')

		split= layout.split()
		col= split.column()
		if vtex.type == 'FRES':
			col.prop(vtex,'fresnel_ior')
		elif vtex.type == 'DIST':
			col.prop(vtex,'dist_near')
			if wide_ui:
				col= split.column()
			col.prop(vtex,'dist_far')
			col.prop(vtex,'dist_extrapolate')

		layout.separator()
		
		split= layout.split()
		col= split.column()
		col.prop(vtex,'invert')
		col.prop(vtex,'invert_alpha')
		col.prop(vtex,'alpha_from_intensity')
		# col.prop(vtex,'nouvw_color')
		# col.prop(vtex,'color_mult')
		# col.prop(vtex,'color_offset')
		if wide_ui:
			col= split.column()
		col.prop(vtex,'alpha_offset')
		col.prop(vtex,'alpha_mult')
		# col.prop(vtex,'blend_output')
		# col.prop(vtex,'use_blend_input')
		# col.prop(vtex,'blend_input')
	

bpy.types.register(TEXTURE_PT_TexFalloff)



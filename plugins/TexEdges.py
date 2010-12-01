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

ID=   'TEXEDGES'
NAME= 'Edge'
PLUG= 'TexEdges'
DESC= "It is a very simple texture map that allows you to render out the wire frame of a mesh."
PID=   4

PARAMS= (
	'edges_tex',         # acolor texture = AColor(1, 1, 1, 1)
	'bg_tex',            # acolor texture = AColor(0, 0, 0, 1)
	'show_hidden_edges', # bool = false
	'width_type',        # integer = 0, 0: World units, 1: Pixels
	# 'world_width',     # float = 1
	# 'pixel_width',     # float = 1
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class TexEdges(bpy.types.IDPropertyGroup):
    pass

def add_properties(VRayTexture):
	VRayTexture.TexEdges= PointerProperty(
		name= "TexEdges",
		type=  TexEdges,
		description= "V-Ray TexEdges settings."
	)

	TexEdges.edges_tex= FloatVectorProperty(
		name= "Edges color",
		description= "Edges color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	TexEdges.bg_tex= FloatVectorProperty(
		name= "Background color",
		description= "Background color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	TexEdges.show_hidden_edges= BoolProperty(
		name= "Show hidden edges",
		description= "Show hidden edges.",
		default= False
	)
	
	TexEdges.width_type= EnumProperty(
		name= "Width type",
		description= "Width type: world units or pixels.",
		items= (
			('WORLD', "World", ""),
			('PIXEL', "Pixel", "")
		),
		default= 'PIXEL'
	)

	TexEdges.width= FloatProperty(
		name= "Width",
		description= "Edge width.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)


def write(ofile, sce, params):
	WIDTH_TYPE= {
		'PIXEL' : 1,
		'WORLD' : 0
	}

	slot= params.get('slot')
	tex= params.get('texture')

	tex_name= params['name'] if 'name' in params else get_name(tex, "Texture")

	vtex= getattr(tex.vray, PLUG)

	# Write output
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'width_type':
			ofile.write("\n\t%s= %s;"%(param, WIDTH_TYPE[vtex.width_type]))
			if vtex.width_type == 'PIXEL':
				_param= 'pixel_width'
			else:
				_param= 'world_width'
			ofile.write("\n\t%s= %s;"%(_param, a(sce,getattr(vtex, 'width'))))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vtex, param))))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
narrowui= 200


class TexEdgesTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_TexEdges(TexEdgesTexturePanel, bpy.types.Panel):
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
		col.prop(vtex, 'edges_tex')
		if wide_ui:
			col= split.column()
		col.prop(vtex, 'bg_tex')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(vtex, 'show_hidden_edges')
		if wide_ui:
			col= split.column()
		col.prop(vtex, 'width_type', text="Type")
		col.prop(vtex, 'width')


bpy.types.register(TEXTURE_PT_TexEdges)

'''

  V-Ray/Blender

  http://vray.cgdo.ru

  Time-stamp: " "

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


TYPE= 'BRDF'
ID=   'BRDFDiffuse'
PID=   5

NAME= 'BRDFDiffuse'
UI=   "Diffuse"
DESC= "BRDFDiffuse."

PARAMS= (
	'color',
	'color_tex',
	'color_tex_mult',
	'transparency',
	'transparency_tex',
	'transparency_tex_mult',
	'roughness',
	'use_irradiance_map',
)


def add_properties(rna_pointer):
	class BRDFDiffuse(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(BRDFDiffuse)
	rna_pointer.BRDFDiffuse= PointerProperty(
		name= "BRDFDiffuse",
		type=  BRDFDiffuse,
		description= "V-Ray BRDFDiffuse settings"
	)

	# color
	BRDFDiffuse.color= FloatVectorProperty(
		name= "Color",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	# color_tex
	BRDFDiffuse.color_tex= StringProperty(
		name= "Color texture",
		description= "TODO: Tooltip",
		default= ""
	)

	BRDFDiffuse.map_color_tex= BoolProperty(
		name= "color tex",
		description= "TODO: Tooltip",
		default= False
	)

	# color_tex_mult
	BRDFDiffuse.color_tex_mult= FloatProperty(
		name= "color tex mult",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# transparency
	BRDFDiffuse.transparency= FloatVectorProperty(
		name= "Transparency",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	# transparency_tex
	BRDFDiffuse.transparency_tex= StringProperty(
		name= "Transparency",
		description= "TODO: Tooltip",
		default= ""
	)

	BRDFDiffuse.map_transparency_tex= BoolProperty(
		name= "transparency tex",
		description= "TODO: Tooltip",
		default= False
	)

	# transparency_tex_mult
	BRDFDiffuse.transparency_tex_mult= FloatProperty(
		name= "transparency tex mult",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# roughness
	BRDFDiffuse.roughness= FloatProperty(
		name= "Roughness",
		description= "Roughness.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	BRDFDiffuse.roughness_tex= StringProperty(
		name= "Roughness texture",
		description= "Roughness texture.",
		default= ""
	)

	BRDFDiffuse.map_roughness= BoolProperty(
		name= "Roughness texture",
		description= "Roughness texture.",
		default= False
	)

	BRDFDiffuse.roughness_mult= FloatProperty(
		name= "Roughness texture multiplier",
		description= "Roughness texture multiplier.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# use_irradiance_map
	BRDFDiffuse.use_irradiance_map= BoolProperty(
		name= "Use Irradiance map",
		description= "Use irradiance map.",
		default= True
	)



def write(ofile, scene, params):
	BRDFDiffuse= getattr(scene.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		value= getattr(BRDFDiffuse, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
def gui(context, layout, BRDFDiffuse):
	wide_ui= context.region.width > narrowui

	split= layout.split()
	col= split.column(align=True)
	col.prop(BRDFDiffuse, 'color')
	col.prop_search(BRDFDiffuse, 'color_tex',
					bpy.data, 'textures',
					text= "")
	if BRDFDiffuse.color_tex:
		col.prop(BRDFDiffuse, 'color_tex_mult', text="Mult")
	if wide_ui:
		col= split.column(align=True)
	col.prop(BRDFDiffuse, 'transparency', text="Opacity")
	col.prop_search(BRDFDiffuse, 'transparency_tex',
					bpy.data, 'textures',
					text= "")
	if BRDFDiffuse.transparency_tex:
		col.prop(BRDFDiffuse, 'transparency_tex_mult', text="Mult")

	layout.separator()

	split= layout.split()
	col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFDiffuse, 'roughness')
	# sub.prop_search(BRDFDiffuse, 'roughness_tex',
	# 				bpy.data, 'textures',
	# 				text= "")
	if wide_ui:
		col= split.column()
	col.prop(BRDFDiffuse, 'use_irradiance_map')

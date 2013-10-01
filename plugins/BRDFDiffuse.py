'''

  V-Ray/Blender

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
import vb25.texture

from vb25.utils import *
from vb25.ui.ui import *

from vb25.lib import ExportUtils


TYPE= 'BRDF'
ID=   'BRDFDiffuse'
PID=   5

NAME= 'Diffuse'
UI=   "Diffuse"
DESC= "BRDFDiffuse."

MAPPED_PARAMS = {
	'color_tex'        : 'TEXTURE',
	'transparency_tex' : 'FLOAT_TEXTURE',
	'roughness'        : 'FLOAT_TEXTURE',
}

PARAMS= (
	'color_tex',
	'transparency_tex',
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

	BRDFDiffuse.color_tex = FloatVectorProperty(
		name= "Color",
		description= "",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	BRDFDiffuse.transparency_tex = FloatProperty(
		name= "Transparency",
		description= "Transparency",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	BRDFDiffuse.roughness= FloatProperty(
		name= "Roughness",
		description= "Roughness",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	BRDFDiffuse.use_irradiance_map= BoolProperty(
		name= "Use Irradiance map",
		description= "Use irradiance map",
		default= True
	)


def writeDatablock(bus, BRDFDiffuse, pluginName, mappedParams):
	ofile = bus['files']['materials']
	scene = bus['scene']

	ofile.write("\nBRDFDiffuse %s {" % pluginName)
	ofile.write("\n\tcolor=Color(0.0,0.0,0.0);")
	ofile.write("\n\tcolor_tex_mult=1.0;")
	ofile.write("\n\ttransparency=Color(0.0,0.0,0.0);")
	ofile.write("\n\ttransparency_tex_mult=1.0;")

	ExportUtils.writeParamsBlock(bus, ofile, BRDFDiffuse, mappedParams, PARAMS, MAPPED_PARAMS)

	ofile.write("\n}\n")

	return pluginName


def write(bus, baseName=None):
	print("This shouldn't happen!")


def gui(context, layout, BRDFDiffuse):
	contextType = GetContextType(context)
	regionWidth = GetRegionWidthFromContext(context)

	wide_ui = regionWidth > narrowui

	split= layout.split()
	col= split.column(align=True)
	col.prop(BRDFDiffuse, 'color_tex', text="")
	if wide_ui:
		col= split.column(align=True)
	col.prop(BRDFDiffuse, 'transparency_tex', text="Opacity")

	layout.separator()

	split= layout.split()
	col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFDiffuse, 'roughness')
	if wide_ui:
		col= split.column()
	col.prop(BRDFDiffuse, 'use_irradiance_map')

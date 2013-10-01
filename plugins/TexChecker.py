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
from vb25.utils   import *
from vb25.ui.ui   import *
from vb25.plugins import *
from vb25.texture import *
from vb25.uvwgen  import *


TYPE= 'TEXTURE'
ID=   'TexChecker'
PLUG= 'TexChecker'

NAME= 'Checker'
DESC= "TexChecker."

PID=   14

PARAMS= (
	'uvwgen',
	'white_color',
	'black_color',
	'contrast',
)


def add_properties(rna_pointer):
	class TexChecker(bpy.types.PropertyGroup):
		white_color= FloatVectorProperty(
			name= "White color",
			description= "The white checker color",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (1,1,1)
		)

		black_color= FloatVectorProperty(
			name= "Black color",
			description= "The black checker color",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0,0,0)
		)

		contrast= FloatProperty(
			name= "Contrast",
			description= "Contrast value",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

	bpy.utils.register_class(TexChecker)

	rna_pointer.TexChecker= PointerProperty(
		name= "TexChecker",
		type=  TexChecker,
		description= "V-Ray TexChecker settings"
	)


def writeDatablock(bus, TexChecker, pluginName, mappedParams=None):
	ofile = bus['files']['textures']
	scene = bus['scene']
	
	uvwgen = write_uvwgen(bus)

	ofile.write("\n%s %s {"%(PLUG, pluginName))

	PLUGINS['TEXTURE']['TexCommon'].write(bus)

	for param in PARAMS:
		if param == 'uvwgen':
			if mappedParams and 'uvwgen' in mappedParams:
				uvwgenValue = mappedParams['uvwgen']
			elif 'uvwgen' in bus:
				uvwgenValue = bus['uvwgen']
			else:
				uvwgenValue = uvwgen
			if not uvwgenValue:
				continue
			ofile.write("\n\tuvwgen=%s;" % (uvwgenValue))
			continue
		elif mappedParams and param in mappedParams:
			value = mappedParams[param]
		else:
			value = getattr(TexChecker, param)
		ofile.write("\n\t%s=%s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return pluginName


def write(bus):
	scene = bus['scene']
	ofile = bus['files']['textures']

	slot     = bus['mtex']['slot']
	texture  = bus['mtex']['texture']
	tex_name = bus['mtex']['name']

	TexChecker = getattr(texture.vray, PLUG)

	return writeDatablock(bus, TexChecker, tex_name)


def gui(context, layout, TexChecker):
	contextType = GetContextType(context)
	regionWidth = GetRegionWidthFromContext(context)

	wide_ui = regionWidth > narrowui

	split = layout.split()
	col = split.column()
	col.prop(TexChecker, 'white_color', text="")
	if wide_ui:
		col = split.column()
	col.prop(TexChecker, 'black_color', text="")

	split = layout.split()
	col = split.column()
	col.prop(TexChecker, 'contrast', slider= True)


class VRAY_TP_TexChecker(VRayTexturePanel, bpy.types.Panel):
	bl_label       = NAME
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDERER','VRAYBLENDER_REALTIME','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		return tex and tex.type == 'VRAY' and tex.vray.type == ID and engine_poll(cls, context)

	def draw(self, context):
		TexChecker = getattr(context.texture.vray, PLUG)

		gui(context, self.layout, TexChecker)


bpy.utils.register_class(VRAY_TP_TexChecker)

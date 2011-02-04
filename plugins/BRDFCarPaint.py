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
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'BRDF'
ID=   'BRDFCarPaint'
PID=   7

NAME= 'BRDFCarPaint'
UI=   "Car"
DESC= "BRDFCarPaint."


PARAMS= (
	'base_color',
	'base_reflection',
	'base_glossiness',
	'flake_color',
	'flake_glossiness',
	'flake_orientation',
	'flake_density',
	'flake_scale',
	'flake_size',
	'flake_map_size',
	'flake_filtering_mode',
	'flake_seed',
	'flake_uvwgen',
	'coat_color',
	'coat_strength',
	'coat_glossiness',
	'coat_bump_float',
	'coat_bump_color',
	'coat_bump_amount',
	'coat_bump_type',
	'traceReflections',
	'doubleSided',
	'subdivs',
	'cutoff_threshold',
	'mapping_type',
	'mapping_channel',
)

def add_properties(rna_pointer):
	class BRDFCarPaint(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.BRDFCarPaint= PointerProperty(
		name= "BRDFCarPaint",
		type=  BRDFCarPaint,
		description= "V-Ray BRDFCarPaint settings"
	)

	# base_color
	BRDFCarPaint.base_color= FloatVectorProperty(
		name= "base color",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.3,0.4,0.5)
	)

	BRDFCarPaint.map_base_color= BoolProperty(
		name= "base color",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.base_color_mult= FloatProperty(
		name= "base color",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# base_reflection
	BRDFCarPaint.base_reflection= FloatProperty(
		name= "base reflection",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.5
	)

	BRDFCarPaint.map_base_reflection= BoolProperty(
		name= "base reflection",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.base_reflection_mult= FloatProperty(
		name= "base reflection",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# base_glossiness
	BRDFCarPaint.base_glossiness= FloatProperty(
		name= "base glossiness",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.6
	)

	BRDFCarPaint.map_base_glossiness= BoolProperty(
		name= "base glossiness",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.base_glossiness_mult= FloatProperty(
		name= "base glossiness",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# flake_color
	BRDFCarPaint.flake_color= FloatVectorProperty(
		name= "flake color",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.3,0.4,0.8)
	)

	BRDFCarPaint.map_flake_color= BoolProperty(
		name= "flake color",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.flake_color_mult= FloatProperty(
		name= "flake color",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# flake_glossiness
	BRDFCarPaint.flake_glossiness= FloatProperty(
		name= "flake glossiness",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.8
	)

	BRDFCarPaint.map_flake_glossiness= BoolProperty(
		name= "flake glossiness",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.flake_glossiness_mult= FloatProperty(
		name= "flake glossiness",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# flake_orientation
	BRDFCarPaint.flake_orientation= FloatProperty(
		name= "flake orientation",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.3
	)

	BRDFCarPaint.map_flake_orientation= BoolProperty(
		name= "flake orientation",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.flake_orientation_mult= FloatProperty(
		name= "flake orientation",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# flake_density
	BRDFCarPaint.flake_density= FloatProperty(
		name= "flake density",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.5
	)

	# flake_scale
	BRDFCarPaint.flake_scale= FloatProperty(
		name= "flake scale",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.01
	)

	# flake_size
	BRDFCarPaint.flake_size= FloatProperty(
		name= "flake size",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.5
	)

	# flake_map_size
	BRDFCarPaint.flake_map_size= IntProperty(
		name= "flake map size",
		description= "The size of the internal flakes map.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1024
	)

	# flake_filtering_mode
	BRDFCarPaint.flake_filtering_mode= IntProperty(
		name= "flake filtering mode",
		description= "Flake filtering mode (0 - simple; 1 - directional).",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	# flake_seed
	BRDFCarPaint.flake_seed= IntProperty(
		name= "flake seed",
		description= "The random seed for the flakes.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	# flake_uvwgen
	# coat_color
	BRDFCarPaint.coat_color= FloatVectorProperty(
		name= "coat color",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	BRDFCarPaint.map_coat_color= BoolProperty(
		name= "coat color",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.coat_color_mult= FloatProperty(
		name= "coat color",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_strength
	BRDFCarPaint.coat_strength= FloatProperty(
		name= "coat strength",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.05
	)

	BRDFCarPaint.map_coat_strength= BoolProperty(
		name= "coat strength",
		description= "TODO: Tooltip",
		default= False
	)

	BRDFCarPaint.coat_strength_mult= FloatProperty(
		name= "coat strength",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_glossiness
	BRDFCarPaint.coat_glossiness= FloatProperty(
		name= "coat glossiness",
		description= "The glossiness of the coat layer.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	BRDFCarPaint.map_coat_glossiness= BoolProperty(
		name= "coat glossiness",
		description= "The glossiness of the coat layer",
		default= False
	)

	BRDFCarPaint.coat_glossiness_mult= FloatProperty(
		name= "coat glossiness",
		description= "The glossiness of the coat layer.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_bump_float
	BRDFCarPaint.map_coat_bump_float= BoolProperty(
		name= "coat bump float",
		description= "Bump texture for the coat layer",
		default= False
	)

	BRDFCarPaint.coat_bump_float_mult= FloatProperty(
		name= "coat bump float",
		description= "Bump texture for the coat layer.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_bump_color
	BRDFCarPaint.map_coat_bump_color= BoolProperty(
		name= "coat bump color",
		description= "Bump texture for the coat layer (color version)",
		default= False
	)

	BRDFCarPaint.coat_bump_color_mult= FloatProperty(
		name= "coat bump color",
		description= "Bump texture for the coat layer (color version).",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_bump_amount
	BRDFCarPaint.map_coat_bump_amount= BoolProperty(
		name= "coat bump amount",
		description= "Bump amount for the coat layer",
		default= False
	)

	BRDFCarPaint.coat_bump_amount_mult= FloatProperty(
		name= "coat bump amount",
		description= "Bump amount for the coat layer.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# coat_bump_type
	BRDFCarPaint.coat_bump_type= IntProperty(
		name= "coat bump type",
		description= "The type of bump mapping (see BRDFBump for more details).",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# traceReflections
	BRDFCarPaint.traceReflections= IntProperty(
		name= "traceReflections",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	# doubleSided
	BRDFCarPaint.doubleSided= IntProperty(
		name= "doubleSided",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	# subdivs
	BRDFCarPaint.subdivs= IntProperty(
		name= "subdivs",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	# cutoff_threshold
	BRDFCarPaint.cutoff_threshold= FloatProperty(
		name= "cutoff threshold",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.001
	)

	# mapping_type
	BRDFCarPaint.mapping_type= IntProperty(
		name= "mapping type",
		description= "The mapping method for the flakes (0 - explicit mapping channel, 1 - triplanar projection in object space).",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# mapping_channel
	BRDFCarPaint.mapping_channel= IntProperty(
		name= "mapping channel",
		description= "The mapping channel when the mapping_type is 0.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)


def write(ofile, scene, params):
	BRDFCarPaint= getattr(scene.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		value= getattr(BRDFCarPaint, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
def gui(context, layout, BRDFCarPaint):
	wide_ui= context.region.width > narrowui

	split= layout.split()
	col= split.column()
	col.prop(BRDFCarPaint, 'base_color')
	col.prop(BRDFCarPaint, 'base_reflection')
	col.prop(BRDFCarPaint, 'base_glossiness')
	col.prop(BRDFCarPaint, 'coat_color')
	col.prop(BRDFCarPaint, 'coat_strength')
	col.prop(BRDFCarPaint, 'coat_glossiness')
	# col.prop(BRDFCarPaint, 'coat_bump_float')
	# col.prop(BRDFCarPaint, 'coat_bump_color')
	# col.prop(BRDFCarPaint, 'coat_bump_amount')
	col.prop(BRDFCarPaint, 'coat_bump_type')
	if wide_ui:
		col= split.column()
	col.prop(BRDFCarPaint, 'flake_color')
	col.prop(BRDFCarPaint, 'flake_glossiness')
	col.prop(BRDFCarPaint, 'flake_orientation')
	col.prop(BRDFCarPaint, 'flake_density')
	col.prop(BRDFCarPaint, 'flake_scale')
	col.prop(BRDFCarPaint, 'flake_size')
	col.prop(BRDFCarPaint, 'flake_map_size')
	col.prop(BRDFCarPaint, 'flake_filtering_mode')
	col.prop(BRDFCarPaint, 'flake_seed')
	# col.prop(BRDFCarPaint, 'flake_uvwgen')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(BRDFCarPaint, 'traceReflections')
	col.prop(BRDFCarPaint, 'doubleSided')
	col.prop(BRDFCarPaint, 'subdivs')
	if wide_ui:
		col= split.column()
	col.prop(BRDFCarPaint, 'cutoff_threshold')
	col.prop(BRDFCarPaint, 'mapping_type')
	col.prop(BRDFCarPaint, 'mapping_channel')

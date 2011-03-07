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
from vb25.uvwgen  import *

TYPE= 'TEXTURE'
ID=   'TexTiles'
PLUG= 'TexTiles'
NAME= 'Tiles'
DESC= "TexTiles."
PID=   8

PARAMS= (
	'alpha_from_intensity',
	'invert',
	'invert_alpha',
	'color_mult',
	'color_offset',
	'alpha_mult',
	'alpha_offset',
	'nouvw_color',
	'placement_type',
	'u',
	'v',
	'w',
	'h',
	'jitter',
	'tile_u',
	'tile_v',
	'uv_noise_on',
	'uv_noise_animate',
	'uv_noise_amount',
	'uv_noise_levels',
	'uv_noise_size',
	'un_noise_phase',
	'color_mortar',
	'color_tiles',
	'horizontal_count',
	'vertical_count',
	'color_variance',
	'horizontal_gap',
	'vertical_gap',
	'pattern_type',
	'line_shift',
	'random_shift',
	'edge_roughness',
	'holes',
	'random_seed',
	'fade_variance',
	'row_modify',
	'column_modify',
	'per_row',
	'row_change',
	'per_column',
	'column_change',
	'uvwgen',
)

def add_properties(rna_pointer):
	class TexTiles(bpy.types.PropertyGroup):
		# alpha_from_intensity
		alpha_from_intensity= BoolProperty(
			name= "alpha from intensity",
			description= "If true, the resulting alpha is the color intensity; otherwise the alpha is taken from the bitmap alpha.",
			default= False
		)

		# invert
		invert= BoolProperty(
			name= "invert",
			description= "If true, the resulting texture color will be inverted.",
			default= False
		)

		# invert_alpha
		invert_alpha= BoolProperty(
			name= "invert alpha",
			description= "If true and invert is on, the resulting texture alpha will be inverted too. If false, just the color will be inverted.",
			default= True
		)

		# color_mult
		color_mult= FloatVectorProperty(
			name= "color mult",
			description= "A multiplier for the texture color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (1,1,1)
		)

		map_color_mult= BoolProperty(
			name= "color mult",
			description= "A multiplier for the texture color",
			default= False
		)

		color_mult_mult= FloatProperty(
			name= "color mult",
			description= "A multiplier for the texture color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# color_offset
		color_offset= FloatVectorProperty(
			name= "color offset",
			description= "An additional offset for the texture color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0,0,0)
		)

		map_color_offset= BoolProperty(
			name= "color offset",
			description= "An additional offset for the texture color",
			default= False
		)

		color_offset_mult= FloatProperty(
			name= "color offset",
			description= "An additional offset for the texture color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# alpha_mult
		alpha_mult= FloatProperty(
			name= "alpha mult",
			description= "A multiplier for the texture alpha.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		map_alpha_mult= BoolProperty(
			name= "alpha mult",
			description= "A multiplier for the texture alpha",
			default= False
		)

		alpha_mult_mult= FloatProperty(
			name= "alpha mult",
			description= "A multiplier for the texture alpha.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# alpha_offset
		alpha_offset= FloatProperty(
			name= "alpha offset",
			description= "An additional offset for the texture alpha.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		map_alpha_offset= BoolProperty(
			name= "alpha offset",
			description= "An additional offset for the texture alpha",
			default= False
		)

		alpha_offset_mult= FloatProperty(
			name= "alpha offset",
			description= "An additional offset for the texture alpha.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# nouvw_color
		nouvw_color= FloatVectorProperty(
			name= "nouvw color",
			description= "The color when there are no valid uvw coordinates.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.5,0.5,0.5)
		)

		map_nouvw_color= BoolProperty(
			name= "nouvw color",
			description= "The color when there are no valid uvw coordinates",
			default= False
		)

		nouvw_color_mult= FloatProperty(
			name= "nouvw color",
			description= "The color when there are no valid uvw coordinates.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# uvwgen
		# placement_type
		placement_type= IntProperty(
			name= "placement type",
			description= "The way the valid portion of the texture is applied: 0 - the whole texture is valid, 1 - crop, 2 -place.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# u
		u= FloatProperty(
			name= "u",
			description= "U coordinate of the valid texture sector.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# v
		v= FloatProperty(
			name= "v",
			description= "V coordinate of the valid texture sector.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# w
		w= FloatProperty(
			name= "w",
			description= "Width of the valid texture sector.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# h
		h= FloatProperty(
			name= "h",
			description= "Height of the valid texture sector.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# jitter
		jitter= FloatProperty(
			name= "jitter",
			description= "Amount of random placement variation.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# tile_u
		tile_u= IntProperty(
			name= "tile u",
			description= "If true there is horizontal tiling.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# tile_v
		tile_v= IntProperty(
			name= "tile v",
			description= "If true there is vertical tiling.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# uv_noise_on
		uv_noise_on= IntProperty(
			name= "uv noise on",
			description= "If true the noise is enabled.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# uv_noise_animate
		uv_noise_animate= IntProperty(
			name= "uv noise animate",
			description= "If true the noise is animated.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# uv_noise_amount
		uv_noise_amount= FloatProperty(
			name= "uv noise amount",
			description= "UV noise amount.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# uv_noise_levels
		uv_noise_levels= FloatProperty(
			name= "uv noise levels",
			description= "UV noise iterations.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# uv_noise_size
		uv_noise_size= FloatProperty(
			name= "uv noise size",
			description= "UV noise size.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# un_noise_phase
		un_noise_phase= FloatProperty(
			name= "un noise phase",
			description= "UV noise phase.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# color_mortar
		color_mortar= FloatVectorProperty(
			name= "Mortar",
			description= "Mortar color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.7,0.7,0.7)
		)

		color_mortar_tex= StringProperty(
			name= "Mortar texture ",
			description= "Mortar color texture.",
			default= ""
		)

		map_color_mortar= BoolProperty(
			name= "color mortar",
			description= "Mortar color",
			default= False
		)

		color_mortar_mult= FloatProperty(
			name= "Mortar color multiplier",
			description= "Mortar color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# color_tiles
		color_tiles= FloatVectorProperty(
			name= "Tiles",
			description= "Tiles color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.6,0.5,0.4)
		)

		color_tiles_tex= StringProperty(
			name= "Tiles texture ",
			description= "Tiles color texture.",
			default= ""
		)

		map_color_tiles= BoolProperty(
			name= "color tiles",
			description= "Tiles color",
			default= False
		)

		color_tiles_mult= FloatProperty(
			name= "color tiles",
			description= "Tiles color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# horizontal_count
		horizontal_count= FloatProperty(
			name= "Horizontal count",
			description= "Tiles horizontal count.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 4
		)

		# vertical_count
		vertical_count= FloatProperty(
			name= "Vertical count",
			description= "Tiles vertical count.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 4
		)

		# color_variance
		color_variance= FloatProperty(
			name= "Color variance",
			description= "Color variance.",
			subtype= 'PERCENTAGE',
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 100.0,
			precision= 1,
			default= 0
		)

		# horizontal_gap
		horizontal_gap= FloatProperty(
			name= "Horizontal gap",
			description= "Horizontal gap between tiles.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.5
		)

		# vertical_gap
		vertical_gap= FloatProperty(
			name= "Vertical gap",
			description= "Vertical gap between tiles.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.5
		)

		# pattern_type
		pattern_type= EnumProperty(
			name= "Pattern type",
			description= "Tiles pattern.",
			items= (
				('CUSTOM_TILES',    "Custom Tiles",        "Custom Tiles."), # 0
				('RUNNING_BOND',    "Running Bond",        "Running Bond."),
				('FLEMISH_BOND',    "Common Flemish Bond", "Common Flemish Bond."),
				('ENGLISH_BOND',    "English Bond",        "English Bond."),
				('RUNNING BOND',    "1/2 Running Bond",    "1/2 Running Bond."),
				('STACK_BOND',      "Stack Bond",          "Stack Bond."),
				('FINE_BOND',       "Fine Running Bond",   "Fine Running Bond."),
				('FINE_STACK_BOND', "Fine Stack Bond",     "Fine Stack Bond."),
			),
			default= 'STACK_BOND'
		)

		# line_shift
		line_shift= FloatProperty(
			name= "Line shift",
			description= "Line shift.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.5
		)

		# random_shift
		random_shift= FloatProperty(
			name= "Random shift",
			description= "Random shift.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# edge_roughness
		edge_roughness= FloatProperty(
			name= "Edge roughness",
			description= "Edge roughness.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# holes
		holes= IntProperty(
			name= "Holes",
			description= "Holes.",
			subtype= 'PERCENTAGE',
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 100,
			default= 0
		)

		# random_seed
		random_seed= IntProperty(
			name= "Random seed",
			description= "Random seed.",
			min= 0,
			max= 100000,
			soft_min= 0,
			soft_max= 10000,
			default= 0
		)

		# fade_variance
		fade_variance= FloatProperty(
			name= "Fade variance",
			description= "Fade variance.",
			subtype= 'PERCENTAGE',
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 100.0,
			precision= 1,
			default= 0.0
		)

		# row_modify
		row_modify= BoolProperty(
			name= "Row modify",
			description= "Custom row parameters.",
			default= 0
		)

		# column_modify
		column_modify= BoolProperty(
			name= "Column modify",
			description= "Custom column parameters.",
			default= 0
		)

		# per_row
		per_row= IntProperty(
			name= "Per row",
			description= "every per_row row is modified by corresponding change value.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 2
		)

		# row_change
		row_change= FloatProperty(
			name= "Row change",
			description= "row change value modifying the number of tiles in affected rows.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# per_column
		per_column= IntProperty(
			name= "Per column",
			description= "every per_column column is modified by corresponding change value.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 2
		)

		# column_change
		column_change= FloatProperty(
			name= "Col change",
			description= "column change value modifying the number of tiles in affected columns.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

	bpy.utils.register_class(TexTiles)

	rna_pointer.TexTiles= PointerProperty(
		name= "TexTiles",
		type=  TexTiles,
		description= "V-Ray TexTiles settings"
	)


def write(bus):
	PATTERN_TYPE= {
		'CUSTOM_TILES':    0,
		'RUNNING_BOND':    1,
		'FLEMISH_BOND':    2,
		'ENGLISH_BOND':    3,
		'RUNNING BOND':    4,
		'STACK_BOND':      5,
		'FINE_BOND':       6,
		'FINE_STACK_BOND': 7,
	}

	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	uvwgen= write_uvwgen(bus)

	TexTiles= getattr(texture.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'uvwgen':
			value= uvwgen
		elif param =='pattern_type':
			value= PATTERN_TYPE[TexTiles.pattern_type]
		else:
			value= getattr(TexTiles, param)
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
class VRAY_TP_TexTiles(VRayTexturePanel, bpy.types.Panel):
	bl_label       = NAME
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		return tex and tex.type == 'VRAY' and tex.vray.type == ID and engine_poll(cls, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		tex= context.texture
		TexTiles= getattr(tex.vray, PLUG)

		split= layout.split()
		col= split.column(align= True)
		col.prop(TexTiles, 'color_mortar')
		col.prop_search(TexTiles, 'color_mortar_tex',
						bpy.data, 'textures',
						text= "")
		if wide_ui:
			col= split.column(align= True)
		col.prop(TexTiles, 'color_tiles')
		col.prop_search(TexTiles, 'color_tiles_tex',
						bpy.data, 'textures',
						text= "")

		layout.separator()

		layout.prop(TexTiles, 'pattern_type')

		layout.separator()

		box= layout.box()
		box.label(text="Tiles setup:")
		split= box.split()
		col= split.column()
		col.prop(TexTiles, 'horizontal_count', text= "H. count")
		col.prop(TexTiles, 'vertical_count', text= "V. count")
		if wide_ui:
			col= split.column()
		col.prop(TexTiles, 'color_variance', text= "Color var.")
		col.prop(TexTiles, 'fade_variance', text= "Fade var.")

		layout.separator()

		box= layout.box()
		box.label(text="Grout setup:")
		split= box.split()
		col= split.column()
		col.prop(TexTiles, 'horizontal_gap', text= "H. gap")
		col.prop(TexTiles, 'vertical_gap', text= "V. gap")
		if wide_ui:
			col= split.column()
		col.prop(TexTiles, 'holes')
		col.prop(TexTiles, 'edge_roughness', text= "Edge rough.")

		layout.separator()

		box= layout.box()
		box.active= TexTiles.pattern_type == 'CUSTOM_TILES'
		box.label(text="Custom setup:")
		split= box.split()
		col= split.column()
		col.prop(TexTiles, 'column_modify')
		if TexTiles.column_modify:
			col.prop(TexTiles, 'per_column')
			col.prop(TexTiles, 'column_change')
		if wide_ui:
			col= split.column()
		col.prop(TexTiles, 'row_modify')
		if TexTiles.row_modify:
			col.prop(TexTiles, 'per_row')
			col.prop(TexTiles, 'row_change')

		box.separator()

		split= box.split()
		col= split.column()
		col.prop(TexTiles, 'line_shift')
		if wide_ui:
			col= split.column()
		col.prop(TexTiles, 'random_shift')

		box.separator()

		box.prop(TexTiles, 'random_seed')

		# # Common params - move to "Common" panel
		# split= layout.split()
		# col= split.column()
		# col.prop(TexNoiseMax, 'alpha_from_intensity')
		# col.prop(TexNoiseMax, 'invert')
		# col.prop(TexNoiseMax, 'invert_alpha')
		# col.prop(TexNoiseMax, 'color_mult')
		# col.prop(TexNoiseMax, 'color_offset')
		# col.prop(TexNoiseMax, 'alpha_mult')
		# col.prop(TexNoiseMax, 'alpha_offset')
		# col.prop(TexNoiseMax, 'nouvw_color')
		# col.prop(TexNoiseMax, 'placement_type')
		# col.prop(TexNoiseMax, 'u')
		# col.prop(TexNoiseMax, 'v')
		# col.prop(TexNoiseMax, 'w')
		# col.prop(TexNoiseMax, 'h')
		# col.prop(TexNoiseMax, 'jitter')
		# col.prop(TexNoiseMax, 'tile_u')
		# col.prop(TexNoiseMax, 'tile_v')
		# col.prop(TexNoiseMax, 'uv_noise_on')
		# col.prop(TexNoiseMax, 'uv_noise_animate')
		# col.prop(TexNoiseMax, 'uv_noise_amount')
		# col.prop(TexNoiseMax, 'uv_noise_levels')
		# col.prop(TexNoiseMax, 'uv_noise_size')
		# col.prop(TexNoiseMax, 'un_noise_phase')

bpy.utils.register_class(VRAY_TP_TexTiles)


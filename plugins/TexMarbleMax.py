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
ID=   'TexMarbleMax'
PLUG= 'TexMarbleMax'
NAME= 'Marble'
DESC= "TexMarbleMax."
PID=   9

PARAMS= (
	'alpha_from_intensity',
	'invert',
	'invert_alpha',
	'color_mult',
	'color_offset',
	'alpha_mult',
	'alpha_offset',
	'nouvw_color',
	'use_3d_mapping',
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
	'color1',
	'color2',
	'size',
	'vein_width',
	'uvwgen',
)

def add_properties(rna_pointer):
	class TexMarbleMax(bpy.types.PropertyGroup):
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

		# use_3d_mapping
		use_3d_mapping= BoolProperty(
			name= "use 3d mapping",
			description= "TODO: Tooltip.",
			default= True
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

		# color1
		color1= FloatVectorProperty(
			name= "color1",
			description= "First color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (1,1,1)
		)

		map_color1= BoolProperty(
			name= "color1",
			description= "First color",
			default= False
		)

		color1_mult= FloatProperty(
			name= "color1",
			description= "First color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# color2
		color2= FloatVectorProperty(
			name= "color2",
			description= "Second color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0,0,0)
		)

		map_color2= BoolProperty(
			name= "color2",
			description= "Second color",
			default= False
		)

		color2_mult= FloatProperty(
			name= "color2",
			description= "Second color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# size
		size= FloatProperty(
			name= "size",
			description= "Size.",
			min= 0.0,
			max= 1000.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# vein_width
		vein_width= FloatProperty(
			name= "vein width",
			description= "Vein width.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.02
		)

	bpy.utils.register_class(TexMarbleMax)

	rna_pointer.TexMarbleMax= PointerProperty(
		name= "TexMarbleMax",
		type=  TexMarbleMax,
		description= "V-Ray TexMarbleMax settings"
	)


def write(bus):
	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	uvwgen= write_uvwgen(bus)

	TexMarbleMax= getattr(texture.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'uvwgen':
			value= uvwgen
		else:
			value= getattr(TexMarbleMax, param)
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
class VRAY_TP_TexMarbleMax(VRayTexturePanel, bpy.types.Panel):
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
		TexMarbleMax= getattr(tex.vray, PLUG)

		layout.label(text="Colors:")
		
		split= layout.split()
		row= split.row()
		row.prop(TexMarbleMax, 'color1', text="")
		row.prop(TexMarbleMax, 'color2', text="")

		layout.separator()
		
		split= layout.split()
		col= split.column()
		col.prop(TexMarbleMax, 'size')
		col.prop(TexMarbleMax, 'vein_width')

		# # Common params - move to "Common" panel
		# split= layout.split()
		# col= split.column()
		# col.prop(TexMarbleMax, 'alpha_from_intensity')
		# col.prop(TexMarbleMax, 'invert')
		# col.prop(TexMarbleMax, 'invert_alpha')
		# col.prop(TexMarbleMax, 'color_mult')
		# col.prop(TexMarbleMax, 'color_offset')
		# col.prop(TexMarbleMax, 'alpha_mult')
		# col.prop(TexMarbleMax, 'alpha_offset')
		# col.prop(TexMarbleMax, 'nouvw_color')
		# col.prop(TexMarbleMax, 'use_3d_mapping')
		# col.prop(TexMarbleMax, 'placement_type')
		# col.prop(TexMarbleMax, 'u')
		# col.prop(TexMarbleMax, 'v')
		# col.prop(TexMarbleMax, 'w')
		# col.prop(TexMarbleMax, 'h')
		# col.prop(TexMarbleMax, 'jitter')
		# col.prop(TexMarbleMax, 'tile_u')
		# col.prop(TexMarbleMax, 'tile_v')
		# col.prop(TexMarbleMax, 'uv_noise_on')
		# col.prop(TexMarbleMax, 'uv_noise_animate')
		# col.prop(TexMarbleMax, 'uv_noise_amount')
		# col.prop(TexMarbleMax, 'uv_noise_levels')
		# col.prop(TexMarbleMax, 'uv_noise_size')
		# col.prop(TexMarbleMax, 'un_noise_phase')

bpy.utils.register_class(VRAY_TP_TexMarbleMax)


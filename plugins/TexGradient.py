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
ID=   'TexGradient'
PLUG= 'TexGradient'
NAME= 'Gradient'
DESC= "TexGradient."
PID=   7

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
	'color1',
	'color2',
	'color3',
	'has_textures',
	'middle',
	'type',
	'noise_amount',
	'noise_size',
	'noise_type',
	'noise_iterations',
	'noise_phase',
	'noise_low',
	'noise_high',
	'noise_smooth',
	'uvwgen',
)

def add_properties(rna_pointer):
	class TexGradient(bpy.types.PropertyGroup):
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
			default= (0,0,0)
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
			description= "Middle color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.5,0.5,0.5)
		)

		map_color2= BoolProperty(
			name= "color2",
			description= "Middle color",
			default= False
		)

		color2_mult= FloatProperty(
			name= "color2",
			description= "Middle color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# color3
		color3= FloatVectorProperty(
			name= "color3",
			description= "End color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (1,1,1)
		)

		map_color3= BoolProperty(
			name= "color3",
			description= "End color",
			default= False
		)

		color3_mult= FloatProperty(
			name= "color3",
			description= "End color.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# has_textures
		has_textures= BoolProperty(
			name= "has textures",
			description= "This affects bump mapping, following a peculiarity in the 3ds Max implementation.",
			default= False
		)

		# middle
		middle= FloatProperty(
			name= "Middle position",
			description= "Middle color position.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.5
		)

		# type
		type= EnumProperty(
			name= "Type",
			description= "Gradient type.",
			items= (
				('LINEAR', "Linear", "Linear."),
				('RADIAL', "Radial", "Radial."),
			),
			default= 'LINEAR'
		)

		# noise_amount
		noise_amount= FloatProperty(
			name= "noise amount",
			description= "Noise amount.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_size
		noise_size= FloatProperty(
			name= "noise size",
			description= "Noise size.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# noise_type
		noise_type= IntProperty(
			name= "noise type",
			description= "Noise type (0 - regular, 1 - fractal, 2 - turbulence).",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# noise_iterations
		noise_iterations= FloatProperty(
			name= "noise iterations",
			description= "Noise iterations.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 4
		)

		# noise_phase
		noise_phase= FloatProperty(
			name= "noise phase",
			description= "Noise phase.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_low
		noise_low= FloatProperty(
			name= "noise low",
			description= "Noise low threshold.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_high
		noise_high= FloatProperty(
			name= "noise high",
			description= "Noise high threshold.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# noise_smooth
		noise_smooth= FloatProperty(
			name= "noise smooth",
			description= "Threshold smoothing.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

	bpy.utils.register_class(TexGradient)

	rna_pointer.TexGradient= PointerProperty(
		name= "TexGradient",
		type=  TexGradient,
		description= "V-Ray TexGradient settings"
	)


def write(bus):
	TYPE= {
		'LINEAR': 0,
		'RADIAL': 1,
	}

	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	uvwgen= write_uvwgen(bus)

	TexGradient= getattr(texture.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'uvwgen':
			value= uvwgen
		elif param == 'type':
			value= TYPE[TexGradient.type]
		else:
			value= getattr(TexGradient, param)
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
class VRAY_TP_TexGradient(VRayTexturePanel, bpy.types.Panel):
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
		TexGradient= getattr(tex.vray, PLUG)

		layout.prop(TexGradient, 'type', expand= True)

		layout.label(text="Colors:")

		split= layout.split()
		row= split.row(align= True)
		row.prop(TexGradient, 'color1', text="")
		row.prop(TexGradient, 'color2', text="")
		row.prop(TexGradient, 'color3', text="")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(TexGradient, 'middle')

		# layout.separator()

		# split= layout.split()
		# col= split.column()
		# col.prop(TexGradient, 'alpha_from_intensity')
		# col.prop(TexGradient, 'invert')
		# col.prop(TexGradient, 'invert_alpha')
		# col.prop(TexGradient, 'color_mult')
		# col.prop(TexGradient, 'color_offset')
		# col.prop(TexGradient, 'alpha_mult')
		# col.prop(TexGradient, 'alpha_offset')
		# col.prop(TexGradient, 'nouvw_color')
		# col.prop(TexGradient, 'placement_type')
		# col.prop(TexGradient, 'u')
		# col.prop(TexGradient, 'v')
		# col.prop(TexGradient, 'w')
		# col.prop(TexGradient, 'h')
		# col.prop(TexGradient, 'jitter')
		# col.prop(TexGradient, 'tile_u')
		# col.prop(TexGradient, 'tile_v')
		# if wide_ui:
		# 	col= split.column()
		# col.prop(TexGradient, 'uv_noise_on')
		# col.prop(TexGradient, 'uv_noise_animate')
		# col.prop(TexGradient, 'uv_noise_amount')
		# col.prop(TexGradient, 'uv_noise_levels')
		# col.prop(TexGradient, 'uv_noise_size')
		# col.prop(TexGradient, 'un_noise_phase')
		# col.prop(TexGradient, 'has_textures')
		# col.prop(TexGradient, 'noise_amount')
		# col.prop(TexGradient, 'noise_size')
		# col.prop(TexGradient, 'noise_type')
		# col.prop(TexGradient, 'noise_iterations')
		# col.prop(TexGradient, 'noise_phase')
		# col.prop(TexGradient, 'noise_low')
		# col.prop(TexGradient, 'noise_high')
		# col.prop(TexGradient, 'noise_smooth')

bpy.utils.register_class(VRAY_TP_TexGradient)


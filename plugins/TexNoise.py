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
from vb25.shaders import *
from vb25.ui.ui import *

TYPE= 'TEXTURE'

ID=   'TEXNOISEMAX'
NAME= 'Noise'
PLUG= 'TexNoiseMax'
DESC= "3ds max like noise texture."
PID=  5

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
	'phase',
	'iterations',
	'low',
	'high',
	'type',
	'uvwgen',
)


def add_properties(rna_pointer):
	class TexNoiseMax(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(TexNoiseMax)

	rna_pointer.TexNoiseMax= PointerProperty(
		name= "TexNoiseMax",
		type=  TexNoiseMax,
		description= "V-Ray TexNoiseMax settings"
	)

	# alpha_from_intensity
	TexNoiseMax.alpha_from_intensity= BoolProperty(
		name= "alpha from intensity",
		description= "If true, the resulting alpha is the color intensity; otherwise the alpha is taken from the bitmap alpha.",
		default= False
	)

	# invert
	TexNoiseMax.invert= BoolProperty(
		name= "invert",
		description= "If true, the resulting texture color will be inverted.",
		default= False
	)

	# invert_alpha
	TexNoiseMax.invert_alpha= BoolProperty(
		name= "invert alpha",
		description= "If true and invert is on, the resulting texture alpha will be inverted too. If false, just the color will be inverted.",
		default= True
	)

	# color_mult
	TexNoiseMax.color_mult= FloatVectorProperty(
		name= "color mult",
		description= "A multiplier for the texture color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	TexNoiseMax.map_color_mult= BoolProperty(
		name= "color mult",
		description= "A multiplier for the texture color",
		default= False
	)

	TexNoiseMax.color_mult_mult= FloatProperty(
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
	TexNoiseMax.color_offset= FloatVectorProperty(
		name= "color offset",
		description= "An additional offset for the texture color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	TexNoiseMax.map_color_offset= BoolProperty(
		name= "color offset",
		description= "An additional offset for the texture color",
		default= False
	)

	TexNoiseMax.color_offset_mult= FloatProperty(
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
	TexNoiseMax.alpha_mult= FloatProperty(
		name= "alpha mult",
		description= "A multiplier for the texture alpha.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	TexNoiseMax.map_alpha_mult= BoolProperty(
		name= "alpha mult",
		description= "A multiplier for the texture alpha",
		default= False
	)

	TexNoiseMax.alpha_mult_mult= FloatProperty(
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
	TexNoiseMax.alpha_offset= FloatProperty(
		name= "alpha offset",
		description= "An additional offset for the texture alpha.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexNoiseMax.map_alpha_offset= BoolProperty(
		name= "alpha offset",
		description= "An additional offset for the texture alpha",
		default= False
	)

	TexNoiseMax.alpha_offset_mult= FloatProperty(
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
	TexNoiseMax.nouvw_color= FloatVectorProperty(
		name= "nouvw color",
		description= "The color when there are no valid uvw coordinates.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.5,0.5,0.5)
	)

	TexNoiseMax.map_nouvw_color= BoolProperty(
		name= "nouvw color",
		description= "The color when there are no valid uvw coordinates",
		default= False
	)

	TexNoiseMax.nouvw_color_mult= FloatProperty(
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
	TexNoiseMax.use_3d_mapping= BoolProperty(
		name= "use 3d mapping",
		description= "TODO: Tooltip.",
		default= True
	)

	# placement_type
	TexNoiseMax.placement_type= EnumProperty(
		name= "Placement type",
		description= "Image texure placement type.",
		items= (
			('FULL', "Full",  "The whole texture is valid."),
			('CROP', "Crop",  "Crop texture."),
			('PLACE',"Place", "Place texture."),
		),
		default= 'FULL'
	)

	# u
	TexNoiseMax.u= FloatProperty(
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
	TexNoiseMax.v= FloatProperty(
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
	TexNoiseMax.w= FloatProperty(
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
	TexNoiseMax.h= FloatProperty(
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
	TexNoiseMax.jitter= FloatProperty(
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
	TexNoiseMax.tile_u= IntProperty(
		name= "tile u",
		description= "If true there is horizontal tiling.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# tile_v
	TexNoiseMax.tile_v= IntProperty(
		name= "tile v",
		description= "If true there is vertical tiling.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# uv_noise_on
	TexNoiseMax.uv_noise_on= IntProperty(
		name= "uv noise on",
		description= "If true the noise is enabled.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# uv_noise_animate
	TexNoiseMax.uv_noise_animate= IntProperty(
		name= "uv noise animate",
		description= "If true the noise is animated.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# uv_noise_amount
	TexNoiseMax.uv_noise_amount= FloatProperty(
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
	TexNoiseMax.uv_noise_levels= FloatProperty(
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
	TexNoiseMax.uv_noise_size= FloatProperty(
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
	TexNoiseMax.un_noise_phase= FloatProperty(
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
	TexNoiseMax.color1= FloatVectorProperty(
		name= "Color 1",
		description= "First color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	TexNoiseMax.color1_tex= StringProperty(
		name= "Color 1 texture",
		description= "Color 1 texture.",
		default= ""
	)

	# color2
	TexNoiseMax.color2= FloatVectorProperty(
		name= "Color 2",
		description= "Second color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	TexNoiseMax.color2_tex= StringProperty(
		name= "Color 2 texture",
		description= "Color 2 texture.",
		default= ""
	)


	# size
	TexNoiseMax.size= FloatProperty(
		name= "Size",
		description= "Size.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# phase
	TexNoiseMax.phase= FloatProperty(
		name= "Phase",
		description= "Phase.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# iterations
	TexNoiseMax.iterations= FloatProperty(
		name= "Iterations",
		description= "Number of iterations for the fractal generator.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 3
	)

	# low
	TexNoiseMax.low= FloatProperty(
		name= "Low",
		description= "Low threshold.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# high
	TexNoiseMax.high= FloatProperty(
		name= "High",
		description= "High threshold.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# type
	TexNoiseMax.type= EnumProperty(
		name= "Type",
		description= "Noise type.",
		items= (
			('REGULAR',    "Regular",    ""), # 0
			('FRACTAL',    "Fractal",    ""),
			('TRUBULENCE', "Turbulence", ""),
		),
		default= 'REGULAR'
	)


def write(ofile, sce, params):
	_TYPE= {
		'REGULAR':    0,
		'FRACTAL':    1,
		'TRUBULENCE': 2,
	}
	_PLACEMENT_TYPE= {
		'FULL':  0,
		'CROP':  1,
		'PLACE': 2,
	}

	#ofile= params.get('file')
	#sce= params.get('scene')
	slot= params.get('slot')
	texture= params.get('texture')

	uvwgen= write_UVWGenChannel(ofile, sce, params)

	tex_name= params['name'] if 'name' in params else get_random_string()

	TexNoiseMax= getattr(texture.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'type':
			value= _TYPE[TexNoiseMax.type]
		elif param == 'placement_type':
			value= _PLACEMENT_TYPE[TexNoiseMax.placement_type]
		elif param == 'uvwgen':
			value= uvwgen
		else:
			value= getattr(TexNoiseMax, param)
		ofile.write("\n\t%s= %s;"%(param, a(sce,value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
class VRAY_TP_TexNoiseMax(VRayTexturePanel, bpy.types.Panel):
	bl_label       = NAME
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		if not tex:
			return False
		engine= context.scene.render.engine
		return ((tex and tex.type == 'VRAY' and tex.vray.type == ID) and (base_poll(__class__, context)))

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		tex= context.texture
		TexNoiseMax= getattr(tex.vray, PLUG)

		split= layout.split()
		col= split.column()
		col.prop(TexNoiseMax, 'color1')
		col.prop_search(TexNoiseMax, 'color1_tex', bpy.data, 'textures', text= "")
		if wide_ui:
			col= split.column()
		col.prop(TexNoiseMax, 'color2')
		col.prop_search(TexNoiseMax, 'color2_tex', bpy.data, 'textures', text= "")

		split= layout.split()
		col= split.column()
		col.prop(TexNoiseMax, 'type')
		col.prop(TexNoiseMax, 'size')
		col.prop(TexNoiseMax, 'iterations')
		if wide_ui:
			col= split.column()
		col.prop(TexNoiseMax, 'low')
		col.prop(TexNoiseMax, 'high')
		col.prop(TexNoiseMax, 'phase')

		# layout.separator()

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
		# col.prop(TexNoiseMax, 'use_3d_mapping')
		# col.prop(TexNoiseMax, 'placement_type')
		# if wide_ui:
		# 	col= split.column()
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

bpy.utils.register_class(VRAY_TP_TexNoiseMax)

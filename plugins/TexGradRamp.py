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
from vb25.shaders import *

TYPE= 'TEXTURE'
ID=   'TexGradRamp'
NAME= 'Gradient Ramp'
PLUG= 'TexGradRamp'
DESC= "TexGradRamp."
PID=   6

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
	'positions',
	# 'colors',
	# 'texture_map',
	'gradient_type',
	'interpolation',
	'noise_amount',
	'noise_type',
	'noise_size',
	'noise_phase',
	'noise_levels',
	'noise_treshold_low',
	'noise_treshold_high',
	'noise_smooth',
)

def add_properties(rna_pointer):
	class TexGradRamp(bpy.types.PropertyGroup):
		class GradRampElement(bpy.types.PropertyGroup):
			position= IntProperty()
			color= FloatVectorProperty()

		bpy.utils.register_class(GradRampElement)
	
		ramp_elements= CollectionProperty(
			type= GradRampElement,
		)
		
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

		# positions
		positions= FloatProperty(
			name= "positions",
			description= "positions of the given colors.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.5
		)

		# colors
		# texture_map
		map_texture_map= BoolProperty(
			name= "texture map",
			description= "the texture used for mapped gradient ramp",
			default= False
		)

		texture_map_mult= FloatProperty(
			name= "texture map",
			description= "the texture used for mapped gradient ramp.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0
		)

		# gradient_type
		gradient_type= IntProperty(
			name= "gradient type",
			description= "0:four corner, 1:box, 2:diagonal, 3:lighting, 4:linear, 5:mapped, 6:normal, 7:pong, 8:radial, 9:spiral, 10:sweep, 11:tartan.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# interpolation
		interpolation= IntProperty(
			name= "interpolation",
			description= "0:none, 1:linear, 2:expUp, 3:expDown, 4:smooth, 5:bump, 6:spike.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 1
		)

		# noise_amount
		noise_amount= FloatProperty(
			name= "noise amount",
			description= "Distortion noise amount.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_type
		noise_type= IntProperty(
			name= "noise type",
			description= "0:regular, 1:fractal, 2:turbulence.",
			min= 0,
			max= 100,
			soft_min= 0,
			soft_max= 10,
			default= 0
		)

		# noise_size
		noise_size= FloatProperty(
			name= "noise size",
			description= "default = 1.0.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1
		)

		# noise_phase
		noise_phase= FloatProperty(
			name= "noise phase",
			description= "default = 0.0.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_levels
		noise_levels= FloatProperty(
			name= "noise levels",
			description= "default = 4.0.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 4
		)

		# noise_treshold_low
		noise_treshold_low= FloatProperty(
			name= "noise treshold low",
			description= "default = 0.0f.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_treshold_high
		noise_treshold_high= FloatProperty(
			name= "noise treshold high",
			description= "default = 1.0f.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

		# noise_smooth
		noise_smooth= FloatProperty(
			name= "noise smooth",
			description= "default = 0.0f.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0
		)

	bpy.utils.register_class(TexGradRamp)

	rna_pointer.TexGradRamp= PointerProperty(
		name= "TexGradRamp",
		type=  TexGradRamp,
		description= "V-Ray TexGradRamp settings"
	)


def write(bus):
	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	TexGradRamp= getattr(texture.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		value= getattr(TexGradRamp, param)
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return tex_name


'''
  GUI
'''
class VRAY_TP_TexGradRamp(VRayTexturePanel, bpy.types.Panel):
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
		TexGradRamp= getattr(tex.vray, PLUG)

		layout.template_color_ramp(TexGradRamp, 'ramp_elements')

		split= layout.split()
		col= split.column()
		col.prop(TexGradRamp, 'positions')
		col.prop(TexGradRamp, 'gradient_type')
		col.prop(TexGradRamp, 'interpolation')

		split= layout.split()
		col= split.column()
		col.prop(TexGradRamp, 'alpha_from_intensity')
		col.prop(TexGradRamp, 'invert')
		col.prop(TexGradRamp, 'invert_alpha')
		col.prop(TexGradRamp, 'color_mult')
		col.prop(TexGradRamp, 'color_offset')
		col.prop(TexGradRamp, 'alpha_mult')
		col.prop(TexGradRamp, 'alpha_offset')
		col.prop(TexGradRamp, 'nouvw_color')
		col.prop(TexGradRamp, 'placement_type')
		col.prop(TexGradRamp, 'u')
		col.prop(TexGradRamp, 'v')
		col.prop(TexGradRamp, 'w')
		col.prop(TexGradRamp, 'h')
		col.prop(TexGradRamp, 'jitter')
		col.prop(TexGradRamp, 'tile_u')
		col.prop(TexGradRamp, 'tile_v')
		if wide_ui:
			col= split.column()
		col.prop(TexGradRamp, 'uv_noise_on')
		col.prop(TexGradRamp, 'uv_noise_animate')
		col.prop(TexGradRamp, 'uv_noise_amount')
		col.prop(TexGradRamp, 'uv_noise_levels')
		col.prop(TexGradRamp, 'uv_noise_size')
		col.prop(TexGradRamp, 'un_noise_phase')
		# col.prop(TexGradRamp, 'colors')
		# col.prop(TexGradRamp, 'texture_map')
		col.prop(TexGradRamp, 'noise_amount')
		col.prop(TexGradRamp, 'noise_type')
		col.prop(TexGradRamp, 'noise_size')
		col.prop(TexGradRamp, 'noise_phase')
		col.prop(TexGradRamp, 'noise_levels')
		col.prop(TexGradRamp, 'noise_treshold_low')
		col.prop(TexGradRamp, 'noise_treshold_high')
		col.prop(TexGradRamp, 'noise_smooth')

bpy.utils.register_class(VRAY_TP_TexGradRamp)


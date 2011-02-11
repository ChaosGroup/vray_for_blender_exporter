'''

  V-Ray/Blender 2.5

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

''' vb modules '''
from vb25.utils   import *
from vb25.plugins import *


def write_TexAColorOp(ofile, sce, color_a, mult):
	tex_name= get_random_string()
	ofile.write("\nTexAColorOp %s {" % tex_name)
	ofile.write("\n\tcolor_a= %s;" % color_a)
	ofile.write("\n\tmult_a= %s;" % a(sce,mult))
	ofile.write("\n}\n")
	return tex_name


def write_TexInvert(ofile, tex):
	tex_name= get_random_string()
	ofile.write("\nTexInvert %s {" % tex_name)
	ofile.write("\n\ttexture= %s;" % tex)
	ofile.write("\n}\n")
	return tex_name


def write_TexCompMax(ofile, sce, params):
	OPERATOR= {
		'Add':        0,
		'Substract':  1,
		'Difference': 2,
		'Multiply':   3,
		'Divide':     4,
		'Minimum':    5,
		'Maximum':    6
	}

	tex_name= "TexCompMax_%s"%(params['name'])

	ofile.write("\nTexCompMax %s {" % tex_name)
	ofile.write("\n\tsourceA= %s;" % params['sourceA'])
	ofile.write("\n\tsourceB= %s;" % params['sourceB'])
	ofile.write("\n\toperator= %d;" % OPERATOR[params['operator']])
	ofile.write("\n}\n")

	return tex_name


def write_TexFresnel(ofile, sce, ma, ma_name, textures):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {" % tex_name)
	if 'reflect' in textures:
		ofile.write("\n\tblack_color= %s;" % textures['reflect'])
	else:
		ofile.write("\n\tblack_color= %s;" % a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color]))))
	ofile.write("\n\tfresnel_ior= %s;" % a(sce,ma.vray.BRDFVRayMtl.fresnel_ior))
	ofile.write("\n}\n")

	return tex_name


def write_texture(bus):
	scene=   bus['scene']
	texture= bus['texture']

	if texture.type == 'IMAGE':
		return PLUGINS['TEXTURE']['TexBitmap'].write(bus)

	elif texture.type == 'VRAY':
		VRayTexture= texture.vray
		return PLUGINS['TEXTURE'][VRayTexture.type].write(bus)

	else:
		debug(sce, "Texture %s: type \'%s\' is not supported." % (texture.name, texture.type), error= True)
		return None



'''
  TEXTURE STACK
  
  Stack naming:
    BAbase_name+TEtexture_name+IDtexture_id_in_stack+PLplugin
  like:
    MAmaterial+TEtexture+IDtexture_id_in_stack
  or:
    LAlamp+TEtexture+IDtexture_id_in_stack
'''
def write_factor(ofile, sce, input_texture_name, mult_value):
	if mult_value == 1.0:
		return input_texture_name

	tex_name= get_random_string()

	if mult_value > 1.0:
		ofile.write("\nTexOutput %s {" % tex_name)
		ofile.write("\n\ttexmap= %s;" % input_texture_name)
		ofile.write("\n\tcolor_mult= %s;" % a(sce, "AColor(%s,%s,%s,1.0)" % ([mult_value]*3)))
		ofile.write("\n}\n")
		# ofile.write("\nTexAColorOp %s {" % tex_name)
		# ofile.write("\n\tcolor_a= %s;" % input_texture_name)
		# ofile.write("\n\tmult_a= %s;" % a(sce, mult_value))
		# ofile.write("\n\tresult_alpha= 1.0;")
		# ofile.write("\n}\n")
	else:
		ofile.write("\nTexAColorOp %s {" % tex_name)
		ofile.write("\n\tcolor_a= %s;" % input_texture_name)
		ofile.write("\n\tmult_a= 1.0;")
		ofile.write("\n\tresult_alpha= %s;" % a(sce, mult_value))
		ofile.write("\n}\n")
				
	return tex_name


def write_stack_factor(ofile, sce, params):
	tex_name= write_texture(ofile, sce, params)
	tex_name= write_factor(ofile, sce, tex_name, params['factor'])
	return tex_name


def stack_write_TexLayered(ofile, layers):
	BLEND_MODES= {
		'NONE':         '0',
		'STENCIL':      '1',
		'OVER':         '1',
		'IN':           '2',
		'OUT':          '3',
		'ADD':          '4',
		'SUBTRACT':     '5',
		'MULTIPLY':     '6',
		'DIFFERENCE':   '7',
		'LIGHTEN':      '8',
		'DARKEN':       '9',
		'SATURATE':    '10',
		'DESATUREATE': '11',
		'ILLUMINATE':  '12',
	}

	tex_name= 'TL' + get_random_string()
	if len(layers) == 1: return layers[0][0]
	ofile.write("\nTexLayered %s {"%(tex_name))
	ofile.write("\n\ttextures= List(%s);"%(','.join([l[0] for l in layers])))
	ofile.write("\n\tblend_modes= List(%s);"%(','.join([BLEND_MODES[l[1]] for l in layers])))
	ofile.write("\n}\n")
	return tex_name


def stack_write_TexMix(ofile, color1, color2, blend_amount):
	tex_name= 'TM' + get_random_string()
	ofile.write("\nTexMix %s {" % tex_name)
	ofile.write("\n\tcolor1= %s;" % color1)
	ofile.write("\n\tcolor2= %s;" % color2)
	ofile.write("\n\tmix_amount= 1.0;")
	ofile.write("\n\tmix_map= %s;" % blend_amount)
	ofile.write("\n}\n")
	return tex_name


def stack_write_textures(ofile, layer):
	if type(layer) == dict:
		color_a= stack_write_textures(ofile, layer['color_a'])
		color_b= stack_write_textures(ofile, layer['color_b'])
		layer_name= stack_write_TexMix(ofile, color_a, color_b, layer['blend_amount'])
	elif type(layer) == list:
		layer_name= stack_write_TexLayered(ofile, layer)
	return layer_name


def stack_collapse_layers(slots):
	layers= []
	for i,slot in enumerate(slots):
		(texture,stencil,blend_mode)= slot
		if stencil:
			color_a= layers
			color_b= stack_collapse_layers(slots[i+1:])
			if len(color_a) and len(color_b):
				return {'color_a': color_a,
						'color_b': color_b,
						'blend_amount': texture}
		layers.append((texture,blend_mode))
	return layers


def write_TexOutput(ofile, texmap, params):
	tex_name= 'TO' + get_random_string()
	ofile.write("\nTexOutput %s {" % tex_name)
	ofile.write("\n\ttexmap= %s;" % texmap)
	ofile.write("\n}\n")
	return tex_name

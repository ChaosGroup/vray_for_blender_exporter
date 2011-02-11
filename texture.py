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
from vb25.uvwgen  import *


'''
  Image texture
'''
def write_BitmapBuffer(bus):
	FILTER_TYPE= {
		'NONE':   0,
		'MIPMAP': 1,
		'AREA':   2,
	}
	COLOR_SPACE= {
		'LINEAR': 0,
		'GAMMA':  1,
		'SRGB':   2,
	}
	INTERPOLATION= {
		'BILINEAR': 0,
		'BICUBIC':  1,
	}

	ofile= bus['files']['texture']
	scene= bus['scene']

	slot=    bus['slot']
	texture= bus['texture']

	VRayScene=    scene.vray
	SettingsColorMapping= VRayScene.SettingsColorMapping
	
	VRaySlot=     texture.vray_slot
	VRayTexture=  texture.vray
	BitmapBuffer= texture.image.vray.BitmapBuffer

	filename= get_full_filepath(sce, texture.image, texture.image.filepath)

	bitmap_name= 'IM' + clean_string(texture.image.name)
	if texture.image.source == 'SEQUENCE':
		bitmap_name= 'IM' + texture.image_user.as_pointer()

	# Check if already exported
	if bitmap_name in bus['filter']['bitmap']:
		return bitmap_name
	bus['filter']['bitmap'].append(bitmap_name)

	ofile.write("\nBitmapBuffer %s {" % bitmap_name)
	ofile.write("\n\tfile= \"%s\";" % filename)
	ofile.write("\n\tcolor_space= %i;" % COLOR_SPACE[BitmapBuffer.color_space])
	ofile.write("\n\tinterpolation= %i;" % INTERPOLATION[BitmapBuffer.interpolation])
	ofile.write("\n\tallow_negative_colors= %i;" % BitmapBuffer.allow_negative_colors)
	ofile.write("\n\tfilter_type= %d;" % FILTER_TYPE[BitmapBuffer.filter_type])
	ofile.write("\n\tfilter_blur= %.3f;" % BitmapBuffer.filter_blur)
	ofile.write("\n\tuse_data_window= %i;" % BitmapBuffer.use_data_window)
	ofile.write("\n}\n")
	if BitmapBuffer.use_input_gamma:
		ofile.write("\n\tgamma= %s;" % p(SettingsColorMapping.input_gamma))
	else:
		ofile.write("\n\tgamma= %s;" % a(sce, BitmapBuffer.gamma))
	if texture.image.source == 'SEQUENCE':
		ofile.write("\n\tframe_sequence= 1;")
		ofile.write("\n\tframe_number= %s;" % a(sce,sce.frame_current))
		ofile.write("\n\tframe_offset= %i;" % texture.image_user.frame_offset)

	return bitmap_name


def write_TexBitmap(bus):
	PLACEMENT_TYPE= {
		'FULL':  0,
		'CROP':  1,
		'PLACE': 2,
	}
	TILE= {
		'NOTILE': 0,
		'TILEUV': 1,
		'TILEU':  2,
		'TILEV':  3,
	}

	ofile= bus['files']['texture']
	scene= bus['scene']

	slot=    bus['slot']
	texture= bus['texture']

	VRayTexture= texture.vray
	VRaySlot=    texture.vray_slot

	if not texture.image:
		print("V-Ray/Blender: %s Image is not set! (%s)"%(color("Error!",'red'),texture.name))
		return "Texture_no_texture"

	tex_name= 'TE' + clean_string(texture.name)

	if VRayTexture.texture_coords == 'ORCO':
		if 'object' in params:
			tex_name= 'OB' + clean_string(params['object'].name) + tex_name

	if 'filters' in params and 'exported_textures' in params['filters']:
		if tex_name in params['filters']['exported_textures']:
			debug(sce, "Filters: %s" % params['filters'])
			return tex_name
		params['filters']['exported_textures'].append(tex_name)

	bitmap= write_BitmapBuffer(ofile, sce, params)

	if bitmap is None:
		return None
	
	if 'environment' in params:
		uvwgen= write_UVWGenEnvironment(ofile, sce, params)
	else:
		uvwgen= write_UVWGenChannel(ofile, sce, params)

	ofile.write("\nTexBitmap %s {" % tex_name)
	ofile.write("\n\tbitmap= %s;" % bitmap)
	ofile.write("\n\tuvwgen= %s;" % uvwgen)
	if 'material' in params:
		ofile.write("\n\tnouvw_color= AColor(%.3f,%.3f,%.3f,1.0);" % tuple(params['material'].diffuse_color))
	ofile.write("\n\ttile= %d;" % TILE[VRayTexture.tile])
	ofile.write("\n\tu= %s;" % texture.crop_min_x)
	ofile.write("\n\tv= %s;" % texture.crop_min_y)
	ofile.write("\n\tw= %s;" % texture.crop_max_x)
	ofile.write("\n\th= %s;" % texture.crop_max_y)
	ofile.write("\n\tplacement_type= %i;" % PLACEMENT_TYPE[texture.vray.placement_type])
	if slot:
		ofile.write("\n\tinvert= %d;"%(slot.invert))
	ofile.write("\n}\n")

	return tex_name


'''
  Procedural textures
'''
def write_TexPlugin(ofile, sce, bus):
	texture= bus.get('texture')
	if texture:
		VRayTexture= texture.vray
		plugin= PLUGINS['TEXTURE'].get(VRayTexture.type)
		if plugin:
			return plugin.write(ofile, sce, bus)


'''
  TEXTURES
'''
def write_texture(ofile, sce, params):
	texture= params['texture']

	texture_name= 'TE' + clean_string(texture.name)
	if 'material' in params:
		texture_name= 'MA' + clean_string(params['material'].name) + texture_name
	if 'mapto' in params:
		texture_name+= 'TS' + params['mapto']

	params['name']= texture_name

	if texture.type == 'IMAGE':
		texture_name= write_TexBitmap(ofile, sce, params)

	elif texture.type == 'VRAY':
		tex_name= write_TexPlugin(ofile, sce, params)
		texture_name= "TO%s" % texture_name
		ofile.write("\nTexOutput %s {" % tex_name)
		ofile.write("\n\ttexmap= %s;" % tex_name)
		ofile.write("\n\tinvert= %s;" % a(sce, params['slot'].invert))
		ofile.write("\n}\n")

	else:
		texture_name= None
		debug(sce, "Texture type [%s] is currently unsupported." % texture.type, error= True)


	if texture_name is None:
		return "Texture_no_texture"

	return texture_name



'''
  Useful textures
'''
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


'''
  Texture multiply and factor
'''
def write_multiply_texture(ofile, sce, input_texture_name, mult_value):
	if mult_value == 1.0:
		return input_texture_name

	tex_name= get_random_string()
		
	ofile.write("\nTexAColorOp %s {" % tex_name)
	ofile.write("\n\tcolor_a= %s;" % input_texture_name)
	if mult_value > 1.0:
		ofile.write("\n\tmult_a= %s;" % a(sce, mult_value))
		ofile.write("\n\tresult_alpha= %s;" % a(sce, 1.0))
	else:
		ofile.write("\n\tmult_a= %s;" % a(sce, 1.0))
		ofile.write("\n\tresult_alpha= %s;" % a(sce, mult_value))
	ofile.write("\n}\n")
				
	return tex_name

def write_texture_factor(ofile, sce, params):
	tex_name= write_texture(ofile, sce, params)
	tex_name= write_multiply_texture(ofile, sce, tex_name, params['factor'])
	return tex_name


'''
  TEXTURE STACK
  
  Stack naming:
    BAbase_name+TEtexture_name+IDtexture_id_in_stack+PLplugin
  like:
    MAmaterial+TEtexture+IDtexture_id_in_stack
  or:
    LAlamp+TEtexture+IDtexture_id_in_stack
'''
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

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

ID=   'TexBitmap'
NAME= 'Bitmap'

DESC= "Image texture."


def add_properties(rna_pointer):
	class VRayImage(bpy.types.IDPropertyGroup):
		pass

	bpy.types.Image.vray= PointerProperty(
		name= "V-Ray Image Settings",
		type=  VRayImage,
		description= "V-Ray image settings."
	)
	
	class BitmapBuffer(bpy.types.IDPropertyGroup):
		pass

	VRayImage.BitmapBuffer= PointerProperty(
		name= "BitmapBuffer",
		type=  BitmapBuffer,
		description= "BitmapBuffer settings."
	)

	BitmapBuffer.filter_type= EnumProperty(
		name= "Filter type",
		description= "Filter type.",
		items= (
			('NONE',   "None",        ""),
			('MIPMAP', "Mip-Map",     "Mip-map filtering."),
			('AREA',   "Area",        "Summed area filtering.")
		),
		default= 'AREA'
	)

	BitmapBuffer.color_space= EnumProperty(
		name= "Color space",
		description= "Color space.",
		items= (
			('LINEAR', "Linear",          ""), # 0
			('GAMMA',  "Gamma corrected", ""),
			('SRGB',   "sRGB",            "")
		),
		default= 'LINEAR'
	)

	BitmapBuffer.interpolation= EnumProperty(
		name= "Interpolation",
		description= "Interpolation.",
		items= (
			('BILINEAR', "Bilinear", ""), # 0
			('BICUBIC',  "Bicubic",  ""),
		),
		default= 'BILINEAR'
	)

	BitmapBuffer.filter_blur= FloatProperty(
		name= "Blur",
		description= "Filter blur.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BitmapBuffer.gamma= FloatProperty(
		name= "Gamma",
		description= "Gamma.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 4,
		default= 1.0
	)

	BitmapBuffer.use_input_gamma= BoolProperty(
		name= "Use \"Input gamma\"",
		description= "Use \"Input gamma\" from \"Color mapping\" settings.",
		default= True
	)

	BitmapBuffer.gamma_correct= BoolProperty(
		name= "Invert gamma",
		description= "Correct \"Color mapping\" gamma (set image gamma = 1 / cm_gamma).",
		default= False
	)

	BitmapBuffer.allow_negative_colors= BoolProperty(
		name= "Allow negative colors",
		description= "If false negative colors will be clamped.",
		default= False
	)

	BitmapBuffer.use_data_window= BoolProperty(
		name= "Use data window",
		description= "Use the data window information in OpenEXR files.",
		default= True
	)

	rna_pointer.TexNoiseMax= PointerProperty(
		name= "TexNoiseMax",
		type=  TexNoiseMax,
		description= "V-Ray TexNoiseMax settings"
	)



'''
  OUTPUT
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


def write(bus):
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
		debug(scene, "Texture: %s Image file is not set!" % texture.name, error= True)
		return bus['defaults']['texture']

	tex_name= 'TE' + clean_string(texture.name)

	# Object mapping - so texture is object dependent
	if VRayTexture.texture_coords == 'ORCO':
		ob= None
		if VRayTexture.object:
			ob= get_data_by_name(scene, 'objects', VRayTexture.object)
		else:
			if 'object' in bus:
				ob= bus['object']
		if ob:
			tex_name= 'OB' + clean_string(params['object'].name) + tex_name

	# Check if already exported
	if tex_name in bus['filter']['texture']:
		return tex_name
	bus['filter']['texture'].append(tex_name)

	bitmap= write_BitmapBuffer(bus)

	if 'environment' in bus:
		uvwgen= write_UVWGenEnvironment(ofile, sce, params)
	else:
		uvwgen= write_UVWGenChannel(ofile, sce, params)

	ofile.write("\nTexBitmap %s {" % tex_name)
	ofile.write("\n\tbitmap= %s;" % bitmap)
	ofile.write("\n\tuvwgen= %s;" % uvwgen)
	ofile.write("\n\tplacement_type= %i;" % PLACEMENT_TYPE[texture.vray.placement_type])
	ofile.write("\n\ttile= %d;" % TILE[VRayTexture.tile])
	ofile.write("\n\tu= %s;" % texture.crop_min_x)
	ofile.write("\n\tv= %s;" % texture.crop_min_y)
	ofile.write("\n\tw= %s;" % texture.crop_max_x)
	ofile.write("\n\th= %s;" % texture.crop_max_y)
	if slot:
		ofile.write("\n\tinvert= %d;" % slot.invert)
	ofile.write("\n\tnouvw_color= AColor(1.0,1.0,1.0,1.0);")
	ofile.write("\n}\n")

	return tex_name

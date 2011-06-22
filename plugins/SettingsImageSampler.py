'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Wednesday, 22 June 2011 [20:34]"

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


TYPE= 'SETTINGS'
ID=   'SettingsImageSampler'

NAME= 'Image sampler'
DESC= "Image sampler options."

PARAMS= (
	'type',
	'fixed_subdivs',
	'dmc_minSubdivs',
	'dmc_maxSubdivs',
	'dmc_threshold',
	'dmc_show_samples',
	'subdivision_minRate',
	'subdivision_maxRate',
	'subdivision_threshold',
	'subdivision_edges',
	'subdivision_normals',
	'subdivision_normals_threshold',
	'subdivision_jitter',
	'subdivision_show_samples',
)


def add_properties(rna_pointer):
	class SettingsImageSampler(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(SettingsImageSampler)

	rna_pointer.SettingsImageSampler= PointerProperty(
		name= "Image Sampler",
		type=  SettingsImageSampler,
		description= "Image Sampler settings."
	)

	SettingsImageSampler.filter_type= EnumProperty(
		name= "Filter type",
		description= "Antialiasing filter.",
		items= (
			('NONE',"None",""),
			('GAUSS',"Gaussian",""),
			('SINC',"Sinc",""),
			('CATMULL',"CatmullRom",""),
			('LANC',"Lanczos",""),
			('TRIANGLE',"Triangle",""),
			('BOX',"Box",""),
			('AREA',"Area","")
		),
		default= "NONE"
	)

	SettingsImageSampler.filter_size= FloatProperty(
		name= "Filter size",
		description= "Filter size.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		default= 1.5
	)

	SettingsImageSampler.type= EnumProperty(
		name= "Type",
		description= "Image sampler type.",
		items= (
			('FXD',"Fixed",""),
			('DMC',"Adaptive DMC",""),
			('SBD',"Adaptive subdivision","")
		),
		default= "DMC"
	)

	SettingsImageSampler.dmc_minSubdivs= IntProperty(
		name= "Min subdivs",
		description= "The initial (minimum) number of samples taken for each pixel.",
		min= 1,
		max= 100,
		default= 1
	)

	SettingsImageSampler.dmc_maxSubdivs= IntProperty(
		name= "Max subdivs",
		description= "The maximum number of samples for a pixel.",
		min= 1,
		max= 100,
		default= 4
	)

	SettingsImageSampler.dmc_treshhold_use_dmc= BoolProperty(
		name= "Use DMC sampler threshold",
		description= "Use threshold specified in the \"DMC sampler\"",
		default= 1
	)

	SettingsImageSampler.dmc_threshold= FloatProperty(
		name= "Color threshold",
		description= "The threshold that will be used to determine if a pixel needs more samples.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.01
	)

	SettingsImageSampler.dmc_show_samples= BoolProperty(
		name= "Show samples",
		description= "Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
		default= 0
	)

	SettingsImageSampler.fixed_subdivs= IntProperty(
		name= "Subdivs",
		description= "The number of samples per pixel.",
		min= 1,
		max= 100,
		default= 1
	)

	SettingsImageSampler.subdivision_show_samples= BoolProperty(
		name= "Show samples",
		description= "Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
		default= 0
	)

	SettingsImageSampler.subdivision_normals= BoolProperty(
		name= "Normals",
		description= "This will supersample areas with sharply varying normals.",
		default= 0
	)

	SettingsImageSampler.subdivision_normals_threshold= FloatProperty(
		name= "Normals threshold",
		description= "Normals threshold.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.05
	)

	SettingsImageSampler.subdivision_jitter= BoolProperty(
		name= "Randomize samples",
		description= "Displaces the samples slightly to produce better antialiasing of nearly horizontal or vertical lines.",
		default= 1
	)

	SettingsImageSampler.subdivision_threshold= FloatProperty(
		name= "Color threshold",
		description= "Determines the sensitivity of the sampler to changes in pixel intensity.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.1
	)

	SettingsImageSampler.subdivision_edges= BoolProperty(
		name= "Object outline",
		description= "This will cause the image sampler to always supersample object edges.",
		default= 0
	)

	SettingsImageSampler.subdivision_minRate= IntProperty(
		name= "Min rate",
		description= "Minimum number of samples per pixel.",
		min= -10,
		max= 50,
		default= -1
	)

	SettingsImageSampler.subdivision_maxRate= IntProperty(
		name= "Max rate",
		description= "Maximum number of samples per pixel.",
		min= -10,
		max= 50,
		default= 2
	)


def write(bus):
	FILTER_TYPE= {
		'AREA'     : "\nFilterArea {",
		'BOX'      : "\nFilterBox {",
		'TRIANGLE' : "\nFilterTriangle {",
		'LANC'     : "\nFilterLanczos {",
		'SINC'     : "\nFilterSinc {",
		'GAUSS'    : "\nFilterGaussian {",
		'CATMULL'  : "\nFilterCatmullRom {"
	}

	TYPE= {
		'FXD': 0,
		'DMC': 1,
		'SBD': 2,
	}

	ofile= bus['files']['scene']
	scene= bus['scene']

	VRayScene= scene.vray
	SettingsImageSampler=       VRayScene.SettingsImageSampler
	SettingsImageSamplerFilter= VRayScene.SettingsImageSampler

	ofile.write("\n%s %s {" % (ID, ID))
	for param in PARAMS:
		if param == 'type':
			value= TYPE[SettingsImageSampler.type]
		else:
			value= getattr(SettingsImageSampler, param)
		ofile.write("\n\t%s= %s;" % (param, p(value)))
	ofile.write("\n}\n")

	if SettingsImageSamplerFilter.filter_type != 'NONE':
		ofile.write(FILTER_TYPE[SettingsImageSamplerFilter.filter_type])
		ofile.write("\n\tsize= %.3f;" % SettingsImageSamplerFilter.filter_size)
		ofile.write("\n}\n")

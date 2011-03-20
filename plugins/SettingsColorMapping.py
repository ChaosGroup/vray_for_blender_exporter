'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: " "

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
ID=   'SettingsColorMapping'

NAME= 'Color mapping'
DESC= "Color mapping options."

PARAMS= (
	'type',
	'affect_background',
	'dark_mult',
	'bright_mult',
	'gamma',
	'subpixel_mapping',
	'clamp_output',
	'clamp_level',
	'adaptation_only',
	'linearWorkflow',
)


def add_properties(rna_pointer):
	class SettingsColorMapping(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(SettingsColorMapping)

	rna_pointer.SettingsColorMapping= PointerProperty(
		name= "Color Mapping",
		type=  SettingsColorMapping,
		description= "Color mapping settings."
	)

	SettingsColorMapping.type= EnumProperty(
		name= "Type",
		description= "Color mapping type.",
		items= (
			('LNR',"Linear",""),
			('EXP',"Exponential",""),
			('HSV',"HSV exponential",""),
			('INT',"Intensity exponential",""),
			('GCOR',"Gamma correction",""),
			('GINT',"Intensity gamma",""),
			('REIN',"Reinhard","")
		),
		default= "LNR"
	)

	SettingsColorMapping.affect_background= BoolProperty(
		name= "Affect background",
		description= "Affect colors belonging to the background.",
		default= True
	)

	SettingsColorMapping.dark_mult= FloatProperty(
		name= "Dark multiplier",
		description= "Multiplier for dark colors.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsColorMapping.bright_mult= FloatProperty(
		name= "Bright multiplier",
		description= "Multiplier for bright colors.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	SettingsColorMapping.gamma= FloatProperty(
		name= "Gamma",
		description= "Gamma correction for the output image regardless of the color mapping mode.",
		min= 0.0,
		max= 10.0,
		soft_min= 1.0,
		soft_max= 2.2,
		default= 1.0
	)

	SettingsColorMapping.input_gamma= FloatProperty(
		name= "Input gamma",
		description= "Input gamma for textures.",
		min= 0.0,
		max= 10.0,
		soft_min= 1.0,
		soft_max= 2.2,
		default= 1.0
	)

	SettingsColorMapping.clamp_output= BoolProperty(
		name= "Clamp output",
		description= "Clamp colors after color mapping.",
		default= True
	)

	SettingsColorMapping.clamp_level= FloatProperty(
		name= "Clamp level",
		description= "The level at which colors will be clamped.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 100.0,
		default= 1.0
	)

	SettingsColorMapping.subpixel_mapping= BoolProperty(
		name= "Sub-pixel mapping",
		description= "This option controls whether color mapping will be applied to the final image pixels, or to the individual sub-pixel samples.",
		default= False
	)

	SettingsColorMapping.adaptation_only= BoolProperty(
		name= "Adaptation only",
		description= "When this parameter is on, the color mapping will not be applied to the final image, however V-Ray will proceed with all its calculations as though color mapping is applied (e.g. the noise levels will be corrected accordingly).",
		default= False
	)

	SettingsColorMapping.linearWorkflow= BoolProperty(
		name= "Linear workflow",
		description= "When this option is checked V-Ray will automatically apply the inverse of the Gamma correction that you have set in the Gamma field to all materials in scene.",
		default= False
	)


def write(bus):
	TYPE= {
		'LNR':  0,
		'EXP':  1,
		'HSV':  2,
		'INT':  3,
		'GCOR': 4,
		'GINT': 5,
		'REIN': 6,
	}

	ofile=  bus['files']['scene']
	scene=  bus['scene']

	VRayScene=            scene.vray
	SettingsColorMapping= VRayScene.SettingsColorMapping

	ofile.write("\n%s %s {" % (ID, ID))
	for param in PARAMS:
		if param == 'type':
			value= TYPE[SettingsColorMapping.type]
		else:
			value= getattr(SettingsColorMapping, param)
		ofile.write("\n\t%s= %s;" % (param, p(value)))
	ofile.write("\n}\n")

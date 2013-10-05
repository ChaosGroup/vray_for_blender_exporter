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
from vb25.ui    import classes


TYPE= 'SETTINGS'
ID=   'SettingsCaustics'

NAME= 'Caustics'
DESC= "Caustics settings"

PARAMS= (
	'on',
	'max_photons',
	'search_distance',
	'max_density',
	'multiplier',
	'mode',
	'file',
	# 'dont_delete',
	'auto_save',
	'auto_save_file',
	'show_calc_phase'
)


def add_properties(parent_struct):
	class SettingsCaustics(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(SettingsCaustics)
	
	parent_struct.SettingsCaustics= PointerProperty(
		name= "Caustics",
		type=  SettingsCaustics,
		description= "Caustics settings"
	)

	SettingsCaustics.on= BoolProperty(
		name= "On",
		description= "Enable caustics computation",
		default= False
	)

	SettingsCaustics.max_photons= IntProperty(
		name= "Max photons",
		description= "TODO",
		min= 0,
		max= 10000,
		soft_min= 0,
		soft_max= 1000,
		default= 30
	)

	SettingsCaustics.search_distance= FloatProperty(
		name= "Search distance",
		description= "TODO",
		subtype= 'DISTANCE',
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.1
	)
	
	SettingsCaustics.max_density= FloatProperty(
		name= "Max density",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	SettingsCaustics.multiplier= FloatProperty(
		name= "Multiplier",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	SettingsCaustics.mode= EnumProperty(
		name= "Mode",
		description= "Caustics computaion mode",
		items= (
			('FILE', "From file", ""),
			('NEW',  "New",       ""),
		),
		default= 'NEW'
	)

	SettingsCaustics.file= StringProperty(
		name= "File",
		subtype= 'FILE_PATH',
		description= "TODO"
	)
	
	SettingsCaustics.auto_save= BoolProperty(
		name= "Auto save",
		description= "TODO",
		default= False
	)

	SettingsCaustics.auto_save_file= StringProperty(
		name= "Auto save file",
		subtype= 'FILE_PATH',
		description= "TODO"
	)

	SettingsCaustics.show_calc_phase= BoolProperty(
		name= "Show calc phase",
		description= "TODO",
		default= False
	)

	# SettingsCaustics.dont_delete= BoolProperty(
	# 	name= "Don\'t delete",
	# 	description= "TODO",
	# 	default= False
	# )



'''
  OUTPUT
'''
def write(bus):
	MODE= {
		'FILE': 1,
		'NEW':  0
	}

	ofile=  bus['files']['scene']
	scene=  bus['scene']

	VRayScene=        scene.vray
	SettingsCaustics= VRayScene.SettingsCaustics

	ofile.write("\n%s %s {" % (ID,ID))
	for param in PARAMS:
		if param in ('file','auto_save_file'):
			value= "\"%s\"" % path_sep_to_unix(bpy.path.abspath(getattr(SettingsCaustics, param)))
		elif param == 'mode':
			value= MODE[SettingsCaustics.mode]
		else:
			value= getattr(SettingsCaustics, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")

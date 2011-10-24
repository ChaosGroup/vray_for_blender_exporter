'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Saturday, 12 March 2011 [02:14]"

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

ID=   'SettingsRaycaster'

NAME= 'Raycaster'
DESC= "Raycaster options"

PARAMS= (
	'maxLevels',
	'minLeafSize',
	'faceLevelCoef',
	'dynMemLimit',
)


def add_properties(rna_pointer):
	class SettingsRaycaster(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(SettingsRaycaster)

	rna_pointer.SettingsRaycaster= PointerProperty(
		name= "Raycaster",
		type=  SettingsRaycaster,
		description= "Raycaster settings"
	)

	SettingsRaycaster.maxLevels= IntProperty(
		name= "Max. tree depth",
		description= "Maximum BSP tree depth",
		min= 50,
		max= 100,
		default= 80
	)

	SettingsRaycaster.minLeafSize= FloatProperty(
		name= "Min. leaf size",
		description= "Minimum size of a leaf node",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	SettingsRaycaster.faceLevelCoef= FloatProperty(
		name= "Face/level",
		description= "Maximum amount of triangles in a leaf node",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 10.0,
		default= 1.0
	)

	SettingsRaycaster.dynMemLimit= IntProperty(
		name= "Dynamic memory limit",
		description= "RAM limit for the dynamic raycasters (0 = auto)",
		min= 0,
		max= 100000,
		default= 0
	)


def write(bus):
	ofile=  bus['files']['scene']
	scene=  bus['scene']

	rna_pointer= getattr(scene.vray, ID)
	ofile.write("\n%s %s {" % (ID,ID))
	for param in PARAMS:
		value= getattr(rna_pointer, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")

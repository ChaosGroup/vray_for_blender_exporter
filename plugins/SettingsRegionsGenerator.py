'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''

TYPE= 'SETTINGS'

ID=   'SETTINGSRG'
NAME= 'Regions Generator'
PLUG= 'SettingsRegionsGenerator'
DESC= "Regions generator settings."

PARAMS= (
	'xc',
	'yc',
	'xymeans',
	'seqtype',
	'reverse'
)


import bpy

from vb25.utils import *


class SettingsRegionsGenerator(bpy.types.IDPropertyGroup):
	pass

def add_properties(parent_struct):
	parent_struct.PointerProperty(
		attr= 'SettingsRegionsGenerator',
		type= SettingsRegionsGenerator,
		name= NAME,
		description= DESC
	)

	SettingsRegionsGenerator.EnumProperty(
		attr= 'seqtype',
		name= "Type",
		description= "Determines the order in which the regions are rendered.",
		items=(
			('HILBERT',   "Hilbert",          ""),
			('TRIANGLE',  "Triangulation",    ""),
			('IOSPIRAL',  "(TODO) IOSPIRAL",  ""),
			('TBCHECKER', "(TODO) TBCHECKER", ""),
			('LRWIPE',    "(TODO) LRWIPE",    ""),
			('TBWIPE',    "(TODO) TBWIPE",    "") # 0
		),
		default= 'TRIANGLE'
	)

	SettingsRegionsGenerator.BoolProperty(
		attr= 'reverse',
		name= "Reverse",
		description= "Reverses the region sequence order. ",
		default= False
	)

	SettingsRegionsGenerator.EnumProperty(
		attr= "xymeans",
		name= "XY means",
		description="XY means region width/height or region count.",
		items=(
			('BUCKETS',  "Region count",  ""),
			('SIZE',     "Region W/H",    "") # 0
		),
		default= 'SIZE'
	)

	SettingsRegionsGenerator.IntProperty(
		attr= 'xc',
		name= "X",
		description= "Determines the maximum region width in pixels (Region W/H is selected) or the number of regions in the horizontal direction (when Region Count is selected)",
		min=1, max=100,
		default=32
	)

	SettingsRegionsGenerator.IntProperty(
		attr= 'yc',
		name= "Y",
		description= "Determines the maximum region height in pixels (Region W/H is selected) or the number of regions in the vertical direction (when Region Count is selected)",
		min=1, max=100,
		default=32
	)

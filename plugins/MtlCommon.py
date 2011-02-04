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


TYPE= 'MATERIAL'
ID=   'Material'

NAME= 'General material setings'
DESC= "General V-Ray material settings."

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	rna_pointer.type= EnumProperty(
		name= "Type",
		description= "Material type.",
		items= (
			('MTL',  "Standard", "Standard V-Ray material."),
			('SSS',  "SSS",      "Fast SSS material."),
			('EMIT', "Light",    "Light emitting material / mesh light ."),
			('CAR',  "Car",      "Car paint material."),
			('BRDF', "Layered",  "Custom material from BRDFs."),
		),
		default= 'MTL'
	)

	rna_pointer.emitter_type= EnumProperty(
		name= "Emitter type",
		description= "This determines the type of BRDF (the shape of the hilight).",
		items= (
			('MTL',  "Material",   "Light material."),
			('MESH', "Mesh light", "Mesh light.")
		),
		default= 'MTL'
	)

	rna_pointer.material_id_number= IntProperty(
		name= "Material ID",
		description= "Material ID.",
		min= 0,
		max= 1024,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	rna_pointer.material_id_color= FloatVectorProperty(
		name= "Color",
		description= "Material ID color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)
	

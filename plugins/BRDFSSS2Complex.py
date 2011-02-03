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

ID=   'BRDFSSS2Complex'

NAME= 'BRDFSSS2Complex'
UI=   "SSS"
DESC= "BRDFSSS2Complex settings."

PID=   2

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	class BRDFSSS2Complex(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.BRDFSSS2Complex= PointerProperty(
		name= "BRDFSSS2Complex",
		type=  BRDFSSS2Complex,
		description= "V-Ray BRDFSSS2Complex settings"
	)

	BRDFSSS2Complex.prepass_rate= IntProperty(
		name= "Prepass rate",
		description= "Sampling density for the illumination map.",
		min= -10,
		max= 10,
		default= -1
	)

	BRDFSSS2Complex.interpolation_accuracy= FloatProperty(
		name= "Interpolation accuracy",
		description= "Interpolation accuracy for the illumination map; normally 1.0 is fine.",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	BRDFSSS2Complex.scale= FloatProperty(
		name= "Scale",
		description= "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smalle.",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 1000.0,
		precision= 4,
		default= 1
	)

	BRDFSSS2Complex.ior= FloatProperty(
		name= "IOR",
		description= 'TODO.',
		min= 0.0,
		max= 30.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.5
	)

	BRDFSSS2Complex.diffuse_amount= FloatProperty(
		name= "Diffuse amount",
		description= 'TODO.',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	BRDFSSS2Complex.scatter_radius= FloatVectorProperty(
		name= "Scatter radius",
		description= 'TODO.',
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.92,0.52,0.175)
	)

	BRDFSSS2Complex.scatter_radius_mult= FloatProperty(
		name= "Scatter radius",
		description= 'TODO.',
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	BRDFSSS2Complex.overall_color= FloatVectorProperty(
		name= "Overall color",
		description= 'TODO.',
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFSSS2Complex.diffuse_color= FloatVectorProperty(
		name= "Diffuse color",
		description= 'TODO.',
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.5,0.5,0.5)
	)

	BRDFSSS2Complex.sub_surface_color= FloatVectorProperty(
		name= "Sub surface color",
		description= 'TODO.',
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.5,0.5,0.5)
	)

	BRDFSSS2Complex.phase_function= FloatProperty(
		name= "Phase function",
		description= 'TODO.',
		min= -1.0,
		max= 1.0,
		soft_min= -1.0,
		soft_max= 1.0,
		precision= 3,
		default= 0
	)

	BRDFSSS2Complex.specular_color= FloatVectorProperty(
		name= "Specular color",
		description= "Specular color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFSSS2Complex.specular_subdivs= IntProperty(
		name= "Specular subdivs",
		description= "Specular subdivs.",
		min= 0,
		max= 10,
		default= 8
	)

	BRDFSSS2Complex.specular_amount= FloatProperty(
		name= "Specular amount",
		description= "Specular amount.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	BRDFSSS2Complex.specular_glossiness= FloatProperty(
		name= "Specular glossiness",
		description= 'TODO.',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.6
	)

	BRDFSSS2Complex.cutoff_threshold= FloatProperty(
		name= "Cutoff threshold",
		description= 'TODO.',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.01
	)

	BRDFSSS2Complex.trace_reflections= BoolProperty(
		name= "Trace reflections",
		description= "TODO.",
		default= True
	)

	BRDFSSS2Complex.reflection_depth= IntProperty(
		name= "Reflection depth",
		description= 'TODO.',
		min= 0,
		max= 10,
		default= 5
	)

	BRDFSSS2Complex.single_scatter= EnumProperty(
		name= "Single scatter",
		description= 'TODO.',
		items= (
			('NONE',"None",""),
			('SIMPLE',"Simple",""),
			('SOLID',"Raytraced (solid)",""),
			('REFR',"Raytraced (refractive)","")
		),
		default= "SIMPLE"
	)

	BRDFSSS2Complex.subdivs= IntProperty(
		name= "Subdivs",
		description= 'TODO.',
		min= 0,
		max= 10,
		default= 8
	)

	BRDFSSS2Complex.refraction_depth= IntProperty(
		name= "Refraction depth",
		description= 'TODO.',
		min= 0,
		max= 10,
		default= 5
	)

	BRDFSSS2Complex.front_scatter= BoolProperty(
		name= "Front scatter",
		description= 'TODO.',
		default= True
	)

	BRDFSSS2Complex.back_scatter= BoolProperty(
		name= "Back scatter",
		description= 'TODO.',
		default= True
	)

	BRDFSSS2Complex.scatter_gi= BoolProperty(
		name= "Scatter GI",
		description= 'TODO.',
		default= False
	)

	BRDFSSS2Complex.prepass_blur= FloatProperty(
		name= "Prepass blur",
		description= 'TODO.',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1.2
	)


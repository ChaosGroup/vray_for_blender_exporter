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
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'BRDF'
ID=   'BRDFBump'

NAME= 'Bump'
DESC= "V-Ray bump shader."

PARAMS= (
)

def add_properties(rna_pointer):
	class BRDFBump(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(BRDFBump)

	rna_pointer.BRDFBump= PointerProperty(
		name= "BRDFBump",
		type=  BRDFBump,
		description= "BRDFBump texture slot settings."
	)

	BRDFBump.bump_tex_mult= FloatProperty(
		name= "Amount",
		description= "Bump amount.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.02
	)

	BRDFBump.map_type= EnumProperty(
		name= "Map type",
		description= "Normal map type.",
		items= (
			('EXPLICIT', "Normal (explicit)", "."),
			('WORLD',    "Normal (world)",    "."),
			('CAMERA',   "Normal (camera)",   "."),
			('OBJECT',   "Normal (object)",   "."),
			('TANGENT',  "Normal (tangent)" , "."),
			('BUMP',     "Bump",              ".")
		),
		default= 'BUMP'
	)

	BRDFBump.bump_shadows= BoolProperty(
		name= "Bump shadows",
		description= "Offset the surface shading point, in addition to the normal.",
		default= False
	)

	BRDFBump.compute_bump_for_shadows= BoolProperty(
		name= "Transparent bump shadows",
		description= "True to compute bump mapping for shadow rays in case the material is transparent; false to skip the bump map for shadow rays (faster rendering).",
		default= True
	)


def write(bus):
	MAP_TYPE= {
		'EXPLICIT': 6,
		'WORLD':    4,
		'CAMERA':   3,
		'OBJECT':   2,
		'TANGENT':  1,
		'BUMP'   :  0,
	}

	ofile=     bus['files']['materials']
	scene=     bus['scene']
	textures=  bus['textures']['mapto']
	slot=      bus['textures']['values']['normal_slot']
	base_brdf= bus['brdf']

	VRayTexture= slot.texture.vray
	VRaySlot=    slot.texture.vray_slot
	BRDFBump=    VRaySlot.BRDFBump

	brdf_name= "BRDFBump_%s" % base_brdf

	ofile.write("\nBRDFBump %s {" % brdf_name)
	ofile.write("\n\tbase_brdf= %s;" % base_brdf)
	ofile.write("\n\tmap_type= %d;" % MAP_TYPE[BRDFBump.map_type])
	ofile.write("\n\tbump_tex_color= %s;" % textures['normal'])
	ofile.write("\n\tbump_tex_float= %s;" % textures['normal'])
	ofile.write("\n\tbump_tex_mult= %s;" % a(scene,BRDFBump.bump_tex_mult))
	ofile.write("\n\tnormal_uvwgen= %s;" % VRaySlot.uvwgen)
	ofile.write("\n\tbump_shadows= %d;" % BRDFBump.bump_shadows)
	ofile.write("\n\tcompute_bump_for_shadows= %d;" % BRDFBump.compute_bump_for_shadows)
	ofile.write("\n}\n")

	bus['brdf']= brdf_name
	
	return brdf_name


def draw():
	pass

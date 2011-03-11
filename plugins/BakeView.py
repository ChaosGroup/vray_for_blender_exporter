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


TYPE= 'SETTINGS'
ID=   'BakeView'

NAME= 'Bake'
DESC= "Bake settings."

PARAMS= (
)


def add_properties(rna_pointer):
	class VRayBake(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(VRayBake)
	
	rna_pointer.VRayBake= PointerProperty(
		name= "Bake",
		type=  VRayBake,
		description= "Texture baking settings."
	)

	VRayBake.use= BoolProperty(
		name= "Bake",
		description= "Bake to texture.",
		default= False
	)

	VRayBake.bake_node= StringProperty(
		name= "Object",
		subtype= 'NONE',
		description= "Object to bake."
	)

	VRayBake.dilation= IntProperty(
		name= "Dilation",
		description= "Number of pixels to expand around geometry.",
		min= 0,
		max= 1000,
		soft_min= 0,
		soft_max= 100,
		default= 2,
	)

	VRayBake.flip_derivs= BoolProperty(
		name= "Flip derivatives",
		description= "Flip the texture direction derivatives (reverses bump mapping).",
		default= False
	)


def write(bus):
	ofile=  bus['files']['camera']
	scene=  bus['scene']
	camera= bus['camera']

	VRayScene= scene.vray
	VRayBake=  VRayScene.VRayBake

	if VRayBake.use and VRayBake.bake_node:
		bake_node= get_data_by_name(scene, 'objects', VRayBake.bake_node)
		if bake_node:
			ofile.write("\nUVWGenChannel BakeViewUVW {")
			ofile.write("\n\tuvw_transform=Transform(")
			ofile.write("\n\t\tMatrix(")
			ofile.write("\n\t\tVector(1.0,0.0,0.0),")
			ofile.write("\n\t\tVector(0.0,1.0,0.0),")
			ofile.write("\n\t\tVector(0.0,0.0,1.0)")
			ofile.write("\n\t\t),")
			ofile.write("\n\t\tVector(0.0,0.0,0.0)")
			ofile.write("\n\t);")
			ofile.write("\n\tuvw_channel=1;")
			ofile.write("\n}\n")
			ofile.write("\nBakeView BakeView {")
			ofile.write("\n\tbake_node= %s;" % get_name(bake_node, pefix="OB"))
			ofile.write("\n\tbake_uvwgen= BakeViewUVW;")
			ofile.write("\n\tdilation= %i;" % VRayBake.dilation)
			ofile.write("\n\tflip_derivs= %i;" % VRayBake.flip_derivs)
			ofile.write("\n}\n")
		else:
			debug(scene, "Bake object not found.", error=True)

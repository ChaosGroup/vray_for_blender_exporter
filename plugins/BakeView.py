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


TYPE= 'SETTINGS'

ID=   'BAKEVIEW'
NAME= 'VRayBake'
UI=   "Bake"
PLUG= 'BakeView'
DESC= "Bake settings."

PID=   140

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	class VRayBake(bpy.types.IDPropertyGroup):
		pass

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


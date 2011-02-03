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

ID=   'MTLRENDERSTATS'
NAME= 'MtlRenderStats'
UI=   "Render"
PLUG= 'MtlRenderStats'
DESC= "MtlRenderStats settings."

PID=   130

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	class MtlRenderStats(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.MtlRenderStats= PointerProperty(
		name= "MtlRenderStats",
		type=  MtlRenderStats,
		description= "V-Ray MtlRenderStats settings"
	)

	MtlRenderStats.use= BoolProperty(
		name= "Use material render options",
		description= "Use material render options.",
		default= False
	)

	MtlRenderStats.camera_visibility= BoolProperty(
		name= "Camera visibility",
		description= "TODO.",
		default= True
	)

	MtlRenderStats.reflections_visibility= BoolProperty(
		name= "Reflections visibility",
		description= "TODO.",
		default= True
	)

	MtlRenderStats.refractions_visibility= BoolProperty(
		name= "Refractions visibility",
		description= "TODO.",
		default= True
	)

	MtlRenderStats.gi_visibility= BoolProperty(
		name= "GI visibility",
		description= "TODO.",
		default= True
	)

	MtlRenderStats.shadows_visibility= BoolProperty(
		name= "Shadows visibility",
		description= "TODO.",
		default= True
	)

	MtlRenderStats.visibility= BoolProperty(
		name= "Overall visibility",
		description= "TODO.",
		default= True
	)


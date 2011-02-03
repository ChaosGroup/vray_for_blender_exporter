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

ID=   'LIGHTMESH'
NAME= 'LightMesh'
UI=   "Mesh light"
PLUG= 'LightMesh'
DESC= "LightMesh settings."

PID=   140

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	class LightMesh(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.LightMesh= PointerProperty(
		name= "LightMesh",
		type=  LightMesh,
		description= "Mesh light settings"
	)

	LightMesh.enabled= BoolProperty(
		name= "Enabled",
		description= "Light\'s on/off state.",
		default= True
	)

	LightMesh.lightPortal= EnumProperty(
		name= "Light portal mode",
		description= "Specifies if the light is a portal light.",
		items= (
			('NORMAL',"Normal light",""),
			('PORTAL',"Portal",""),
			('SPORTAL',"Simple portal","")
		),
		default= 'NORMAL'
	)

	LightMesh.units= EnumProperty(
		name= "Intensity units",
		description= "Units for the intensity.",
		items= (
			('DEFAULT',"Default",""),
			('LUMENS',"Lumens",""),
			('LUMM',"Lm/m/m/sr",""),
			('WATTSM',"Watts",""),
			('WATM',"W/m/m/sr","")
		),
		default= 'DEFAULT'
	)

	LightMesh.intensity= FloatProperty(
		name= "Intensity",
		description= "Light intensity.",
		min= 0.0,
		max= 10000000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 2,
		default= 30
	)

	LightMesh.causticSubdivs= IntProperty(
		name= "Caustic subdivs",
		description= "Caustic subdivs.",
		min= 1,
		max= 10000,
		default= 1000
	)

	LightMesh.subdivs= IntProperty(
		name= "Subdivs",
		description= "The number of samples V-Ray takes to compute lighting.",
		min= 0,
		max= 256,
		default= 8
	)

	LightMesh.noDecay= BoolProperty(
		name= "No decay",
		description= "TODO.",
		default= False
	)

	LightMesh.affectReflections= BoolProperty(
		name= "Affect reflections",
		description= "true if the light appears in reflections and false otherwise",
		default= True
	)

	LightMesh.invisible= BoolProperty(
		name= "Invisible",
		description= "TODO.",
		default= False
	)

	LightMesh.storeWithIrradianceMap= BoolProperty(
		name= "Store with Irradiance Map",
		description= "TODO.",
		default= False
	)

	LightMesh.affectDiffuse= BoolProperty(
		name= "Affect diffuse",
		description= "true if the light produces diffuse lighting and false otherwise",
		default= True
	)

	LightMesh.affectSpecular= BoolProperty(
		name= "Affect dpecular",
		description= "true if the light produces specular hilights and false otherwise",
		default= True
	)

	LightMesh.doubleSided= BoolProperty(
		name= "Double-sided",
		description= "TODO.",
		default= False
	)


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


TYPE= 'GEOMETRY'
ID=   'LightMesh'

NAME= 'LightMesh'
UI=   "Mesh light"
DESC= "LightMesh settings."

PARAMS= (
)


def add_properties(rna_pointer):
	class LightMesh(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.LightMesh= PointerProperty(
		name= "LightMesh",
		type=  LightMesh,
		description= "Mesh light settings"
	)

	LightMesh.use= BoolProperty(
		name= "Use mesh light",
		description= "Use mesh light.",
		default= False
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
		name= "Affect specular",
		description= "true if the light produces specular hilights and false otherwise",
		default= True
	)

	LightMesh.doubleSided= BoolProperty(
		name= "Double-sided",
		description= "TODO.",
		default= False
	)


def write(bus):
	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']

	plugin= 'LightMesh'

	VRayObject= ob.vray
	LightMesh=  VRayObject.LightMesh
	
	ma=  bus['texture']['material']
	tex= bus['texture']

	light= getattr(ma.vray,plugin)

	ofile.write("\n%s %s {" % (plugin,name))
	ofile.write("\n\ttransform= %s;"%(a(scene,transform(matrix))))
	for param in OBJECT_PARAMS[plugin]:
		if param == 'color':
			if tex:
				ofile.write("\n\tcolor= %s;" % a(scene,ma.diffuse_color))
				ofile.write("\n\ttex= %s;" % tex)
				ofile.write("\n\tuse_tex= 1;")
			else:
				ofile.write("\n\tcolor= %s;"%(a(scene,ma.diffuse_color)))
		elif param == 'geometry':
			ofile.write("\n\t%s= %s;"%(param, geometry))
		elif param == 'units':
			ofile.write("\n\t%s= %i;"%(param, UNITS[light.units]))
		elif param == 'lightPortal':
			ofile.write("\n\t%s= %i;"%(param, LIGHT_PORTAL[light.lightPortal]))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(light,param))))
	ofile.write("\n}\n")

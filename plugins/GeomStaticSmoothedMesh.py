'''
  V-Ray/Blender

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 19 July 2011 [10:25]"

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
  along with this program.	If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
'''


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'GEOMETRY'
ID=	  'GeomStaticSmoothedMesh'

NAME= 'Subdivision'
DESC= "Subdivision surface settings."

PARAMS= (
	'displacement_amount',
	'displacement_shift',
	'keep_continuity',
	'water_level',
	'use_globals',
	'view_dep',
	'edge_length',
	'max_subdivs',
	'use_bounds',
	'min_bound',
	'max_bound',
	'static_subdiv',
)

def add_properties(rna_pointer):
	class GeomStaticSmoothedMesh(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(GeomStaticSmoothedMesh)

	rna_pointer.GeomStaticSmoothedMesh= PointerProperty(
		name= "GeomStaticSmoothedMesh",
		type=  GeomStaticSmoothedMesh,
		description= "GeomStaticSmoothedMesh texture slot settings."
	)

	GeomStaticSmoothedMesh.use= BoolProperty(
		name= "Override displacement settings",
		description= "Override material displacement settings.",
		default= False
	)

	GeomStaticSmoothedMesh.displacement_amount= FloatProperty(
		name= "Amount",
		description= "Displacement amount.",
		min= -100.0,
		max= 100.0,
		soft_min= -0.1,
		soft_max= 0.1,
		precision= 5,
		default= 0.02
	)

	GeomStaticSmoothedMesh.displacement_shift= FloatProperty(
		name="Shift",
		description="",
		min=-100.0,
		max=100.0,
		soft_min=-1.0,
		soft_max=1.0,
		precision=4,
		default=0.0
	)

	GeomStaticSmoothedMesh.water_level= FloatProperty(
		name="Water level",
		description="",
		min=-100.0, max=100.0, soft_min=-1.0, soft_max=1.0,
		default=0.0
	)

	GeomStaticSmoothedMesh.use_globals= BoolProperty(
		name= "Use globals",
		description= "If true, the global displacement quality settings will be used.",
		default= True
	)

	GeomStaticSmoothedMesh.view_dep= BoolProperty(
		name= "View dependent",
		description= "Determines if view-dependent tesselation is used",
		default= True
	)

	GeomStaticSmoothedMesh.edge_length= FloatProperty(
		name= "Edge length",
		description= "Determines the approximate edge length for the sub-triangles",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 4
	)

	GeomStaticSmoothedMesh.max_subdivs= IntProperty(
		name= "Max subdivs",
		description= "Determines the maximum subdivisions for a triangle of the original mesh",
		min= 0,
		max= 2048,
		soft_min= 0,
		soft_max= 1024,
		default= 256
	)

	GeomStaticSmoothedMesh.keep_continuity= BoolProperty(
		name= "Keep continuity",
		description= "If true, the plugin will attempt to keep the continuity of the displaced surface",
		default= False
	)

	GeomStaticSmoothedMesh.use_bounds= BoolProperty(
		name= "Use bounds",
		description= "If true, the min/max values for the displacement texture are specified by the min_bound and max_bound parameters; if false, these are calculated automatically.",
		default= False
	)

	GeomStaticSmoothedMesh.min_bound= FloatProperty(
		name= "Min bound",
		description= "The lowest value for the displacement texture",
		min= -1.0,
		max=  1.0,
		soft_min= -1.0,
		soft_max=  1.0,
		default= 0.0
	)

	GeomStaticSmoothedMesh.max_bound= FloatProperty(
		name= "Max bound",
		description= "The biggest value for the displacement texture",
		min= -1.0,
		max=  1.0,
		soft_min= -1.0,
		soft_max=  1.0,
		default= 1.0
	)

	GeomStaticSmoothedMesh.static_subdiv= BoolProperty(
		name= "Static subdivision",
		description= "True if the resulting triangles of the subdivision algorithm will be inserted into the rayserver as static geometry.",
		default= False
	)



def write(bus):
	ofile= bus['files']['nodes']
	scene= bus['scene']

	ob=	   bus['node']['object']
	me=	   bus['node']['geometry']
	
	VRayScene= scene.vray
	VRayExporter= VRayScene.exporter

	if not VRayExporter.use_displace:
		return
		
		slot= bus['node']['displacement_slot']

	VRayObject= ob.vray
	GeomStaticSmoothedMesh= VRayObject.GeomStaticSmoothedMesh
	
	VRaySlot=			 slot.texture.vray_slot
	GeomDisplacedMesh=	 VRaySlot.GeomDisplacedMesh
	displacement_amount= GeomDisplacedMesh.displacement_amount

	if GeomStaticSmoothedMesh.use:
		subdiv_name= 'SBDV'+me
		if not append_unique(bus['cache']['displace'], subdiv_name):
			return subdiv_name

		ofile.write("\nGeomStaticSmoothedMesh %s {" % subdiv_name)
		ofile.write("\n\tmesh= %s;" % me)
		for param in PARAMS:
			if param == 'displacement_amount':
				if ob.vray.GeomStaticSmoothedMesh.use:
					if GeomDisplacedMesh.amount_type == 'OVER':
						value= GeomDisplacedMesh.displacement_amount
					else:
						value= GeomDisplacedMesh.amount_mult * displacement_amount
				else:
					value= displacement_amount
			else:		
				value= getattr(GeomStaticSmoothedMesh, param)
			ofile.write("\n\t%s= %s;" % (param, a(scene,value)))
		ofile.write("\n}\n")

		bus['node']['geometry']= subdiv_name


def influence(context, layout, slot):
	pass

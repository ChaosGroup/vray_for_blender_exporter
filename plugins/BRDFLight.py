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
ID=   'BRDFLight'
PID=   3
MAIN_BRDF= True

NAME= 'BRDFLight'
UI=   "Light"
DESC= "V-Ray light shader."

PARAMS= (
)

def add_properties(rna_pointer):
	class BRDFLight(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(BRDFLight)

	rna_pointer.BRDFLight= PointerProperty(
		name= "BRDFLight",
		type=  BRDFLight,
		description= "V-Ray BRDFLight settings"
	)

	BRDFLight.color= FloatVectorProperty(
		name= "Color",
		description= "Color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFLight.colorMultiplier= FloatProperty(
		name= "Multiplier",
		description= "Color multiplier.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFLight.doubleSided= BoolProperty(
		name= "Double-sided",
		description= "If false, the light color is black for back-facing surfaces.",
		default= False
	)

	BRDFLight.emitOnBackSide= BoolProperty(
		name= "Emit on back side",
		description= 'TODO.',
		default= False
	)

	BRDFLight.compensateExposure= BoolProperty(
		name= "Compensate camera exposure",
		description= 'TODO.',
		default= False
	)

	BRDFLight.transparency= FloatProperty(
		name= "Transparency",
		description= "Transparency of the BRDF.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)



def get_defaults(bus, BRDFLayered= None):
	scene= bus['scene']
	ma=    bus['material']

	defaults= {}

	VRayMaterial= ma.vray
	BRDFLight=    VRayMaterial.BRDFLight

	if BRDFLayered:
		defaults['diffuse']= (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFLight.color)),       0, 'NONE')
		defaults['opacity']= (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFLight.opacity]*3)), 0, 'NONE')
	else:
		defaults['diffuse']= (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)), 0, 'NONE')
		defaults['opacity']= (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([ma.alpha]*3)),     0, 'NONE')

	return defaults


def write(bus):
	material= bus['material']
	
	brdf_name= "%s_%s" % (ID, clean_string(material.name))

	bus['brdf']= brdf_name

	return brdf_name



def influence(context, layout, slot):
	wide_ui= context.region.width > narrowui

	VRaySlot= slot.texture.vray_slot

	split= layout.split()
	col= split.column()
	col.label(text="Diffuse:")
	split= layout.split()
	col= split.column()
	factor_but(col, slot, 'use_map_color_diffuse', 'diffuse_color_factor', "Diffuse")
	if wide_ui:
		col= split.column()
	factor_but(col, slot, 'use_map_alpha', 'alpha_factor', "Alpha")


def gui(context, layout, BRDFLight, material= None):
	wide_ui= context.region.width > narrowui

	if material:
		layout.label(text="Color")

		split= layout.split()
		col= split.column()
		col.prop(material, 'diffuse_color', text="")
		if wide_ui:
			col= split.column()
		col.prop(material, 'alpha')
	else:
		layout.prop(BRDFLight, 'transparency')

	layout.separator()

	split= layout.split()
	col= split.column()
	if material:
		col.prop(material, 'emit', text="Intensity")
	else:
		col.prop(BRDFLight, 'color', text="")
		col.prop(BRDFLight, 'colorMultiplier', text="Intensity")
	if wide_ui:
		col= split.column()
	col.prop(BRDFLight, 'emitOnBackSide')
	col.prop(BRDFLight, 'compensateExposure', text="Compensate exposure")
	col.prop(BRDFLight, 'doubleSided')



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
ID=   'BRDFSSS2Complex'
PID=   2
MAIN_BRDF= True

NAME= 'BRDFSSS2Complex'
UI=   "Fast SSS"
DESC= "BRDFSSS2Complex settings."

PARAMS= (
	'prepass_rate',
	'interpolation_accuracy',
	'scale',
	'ior',
	#'overall_color',
	#'diffuse_color',
	#'diffuse_amount',
	#'sub_surface_color',
	#'scatter_radius',
	'scatter_radius_mult',
	'phase_function',
	#'specular_color',
	#'specular_amount',
	#'specular_glossiness',
	'specular_subdivs',
	'cutoff_threshold',
	'trace_reflections',
	'reflection_depth',
	#'single_scatter',
	'subdivs',
	'refraction_depth',
	'front_scatter',
	'back_scatter',
	'scatter_gi',
	'prepass_blur'
	#'channels'
)


def add_properties(rna_pointer):
	class BRDFSSS2Complex(bpy.types.PropertyGroup):
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


def get_defaults(bus, BRDFLayered= None):
	scene= bus['scene']
	ma=    bus['material']

	defaults= {}

	VRayMaterial=    ma.vray
	BRDFSSS2Complex= BRDFLayered.BRDFSSS2Complex if BRDFLayered else VRayMaterial.BRDFSSS2Complex

	if BRDFLayered:
		defaults['overall_color']=   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.diffuse_color)), 0, 'NONE')
	else:
		defaults['overall_color']=   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(ma.diffuse_color)), 0, 'NONE')

	defaults['sub_surface_color']=   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.sub_surface_color)),  0, 'NONE')
	defaults['scatter_radius']=      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.scatter_radius)),     0, 'NONE')
	defaults['diffuse_color']=       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.diffuse_color)),      0, 'NONE')
	defaults['diffuse_amount']=      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([BRDFSSS2Complex.diffuse_amount]*3)), 0, 'NONE')
	defaults['specular_color']=      (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(BRDFSSS2Complex.specular_color)),     0, 'NONE')
	defaults['specular_amount']=     (a(scene,"AColor(0.0,0.0,0.0,1.0)"), 0, 'NONE')
	defaults['specular_glossiness']= (a(scene,"AColor(0.0,0.0,0.0,1.0)"), 0, 'NONE')

	return defaults


def write(bus, rna_pointer= None):
	SINGLE_SCATTER= {
		'NONE':   0,
		'SIMPLE': 1,
		'SOLID':  2,
		'REFR':   3,
	}

	BRDFSSS2Complex= ma.vray.BRDFSSS2Complex

	brdf_name= "BRDFSSS2Complex_%s"%(ma_name)

	ofile.write("\nBRDFSSS2Complex %s {" % brdf_name)

	for key in ('overall_color','diffuse_color','sub_surface_color','scatter_radius','specular_color'):
		ofile.write("\n\t%s= %s;" % (key, a(scene,textures[key]) if key in textures else a(scene,getattr(BRDFSSS2Complex,key))))

	for key in ('specular_amount','specular_glossiness','diffuse_amount'):
		ofile.write("\n\t%s= %s;" % (key, "%s::out_intensity" % textures[key] if key in textures else a(scene,getattr(BRDFSSS2Complex,key))))

	for param in OBJECT_PARAMS['BRDFSSS2Complex']:
		if param == 'single_scatter':
			value= SINGLE_SCATTER[BRDFSSS2Complex.single_scatter]
		else:
			value= getattr(BRDFSSS2Complex,param)
		ofile.write("\n\t%s= %s;"%(param, a(scene,value)))

	ofile.write("\n}\n")

	return brdf_name



def gui(context, layout, BRDFSSS2Complex, material= None):
	wide_ui= context.region.width > narrowui

	split= layout.split()
	col= split.column()
	col.label(text="General:")

	split= layout.split()
	col= split.column()
	col.menu('MATERIAL_MT_VRAY_presets', text="Presets")

	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'prepass_rate')
	col.prop(BRDFSSS2Complex, 'scale')
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'ior')
	col.prop(BRDFSSS2Complex, 'interpolation_accuracy', text='Accuracy')

	layout.separator()

	split= layout.split()
	col= split.column()
	if material:
		col.prop(material, 'diffuse_color', text="Overall color")
	else:
		col.prop(BRDFSSS2Complex, 'overall_color')
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'diffuse_color')
	split= layout.split()
	col= split.column()
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'diffuse_amount', text="Amount")

	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'sub_surface_color')
	col.prop(BRDFSSS2Complex, 'phase_function')
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'scatter_radius', text="Scatter color")
	col.prop(BRDFSSS2Complex, 'scatter_radius_mult', text="Radius")

	split= layout.split()
	col= split.column()
	col.label(text='Specular layer:')
	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'specular_color', text='')
	col.prop(BRDFSSS2Complex, 'specular_subdivs', text='Subdivs')
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'specular_amount', text='Amount')
	col.prop(BRDFSSS2Complex, 'specular_glossiness', text='Glossiness')

	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'trace_reflections')
	if BRDFSSS2Complex.trace_reflections:
		if wide_ui:
			col= split.column()
		col.prop(BRDFSSS2Complex, 'reflection_depth')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'single_scatter')

	split= layout.split()
	col= split.column()
	col.prop(BRDFSSS2Complex, 'subdivs')
	col.prop(BRDFSSS2Complex, 'refraction_depth')
	col.prop(BRDFSSS2Complex, 'cutoff_threshold')
	if wide_ui:
		col= split.column()
	col.prop(BRDFSSS2Complex, 'front_scatter')
	col.prop(BRDFSSS2Complex, 'back_scatter')
	col.prop(BRDFSSS2Complex, 'scatter_gi')
	col.prop(BRDFSSS2Complex, 'prepass_blur')

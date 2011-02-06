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
ID=   'BRDFVRayMtl'
PID=   1
MAIN_BRDF= True

NAME= "VRayMtl"
UI=   "VRayMtl"
DESC= "BRDFVRayMtl settings."


PARAMS= (
)


def add_properties(rna_pointer):
	class BRDFVRayMtl(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.BRDFVRayMtl= PointerProperty(
		name= "BRDFVRayMtl",
		type=  BRDFVRayMtl,
		description= "V-Ray BRDFVRayMtl settings."
	)

	BRDFVRayMtl.diffuse= FloatVectorProperty(
		name= "Diffuse",
		description= "Diffuse color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.75,0.75,0.75)
	)

	BRDFVRayMtl.opacity= FloatProperty(
		name= "Opacity",
		description= "Opacity.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.fog_color= FloatVectorProperty(
		name= "Fog color",
		description= "Fog color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFVRayMtl.refract_color= FloatVectorProperty(
		name= "Refraction color",
		description= "Refraction color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.reflect_color= FloatVectorProperty(
		name= "Reflection color",
		description= "Reflection color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.reflect_exit_color= FloatVectorProperty(
		name= "Reflection exit color",
		description= "Reflection exit color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.fresnel= BoolProperty(
		name= "Frensnel reflections",
		description= "Enable frensnel reflections.",
		default= False
	)

	BRDFVRayMtl.fresnel_ior_lock= BoolProperty(
		name= "Frensnel reflections lock",
		description= "",
		default= False
	)

	BRDFVRayMtl.dispersion_on= BoolProperty(
		name= "Dispersion",
		description= "Enable dispersion.",
		default= False
	)

	BRDFVRayMtl.dispersion= IntProperty(
		name= "Abbe",
		description= "Abbe value.",
		min= 1,
		max= 1024,
		soft_min= 1,
		soft_max= 100,
		default= 50
	)

	BRDFVRayMtl.fresnel_ior= FloatProperty(
		name= "Fresnel IOR",
		description= "",
		min= 0.0,
		max= 30.0,
		soft_min= 0.0,
		soft_max= 10.0,
		default= 1.6
	)

	BRDFVRayMtl.refract_ior= FloatProperty(
		name= "Refractions IOR",
		description= "The IOR for refractions.",
		min= 0.0,
		max= 30.0,
		soft_min= 0.0,
		soft_max= 10.0,
		default= 1.6
	)

	BRDFVRayMtl.reflect_subdivs= IntProperty(
		name= "Reflection subdivs",
		description= "Subdivs for glossy reflections",
		min= 1,
		max= 256,
		default= 8
	)

	BRDFVRayMtl.reflect_depth= IntProperty(
		name= "Reflections depth",
		description= "The maximum depth for reflections.",
		min= 1,
		max= 256,
		default= 5
	)

	BRDFVRayMtl.refract_depth= IntProperty(
		name= "Refractions depth",
		description= "The maximum depth for refractions.",
		min= 1,
		max= 256,
		default= 5
	)

	BRDFVRayMtl.refract_subdivs= IntProperty(
		name= "Refraction subdivs",
		description= "Subdivs for glossy refractions",
		min= 1,
		max= 256,
		default= 8
	)

	BRDFVRayMtl.roughness= FloatProperty(
		name= "Roughness",
		description= "",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFVRayMtl.hilight_glossiness= FloatProperty(
		name= "Hilight glossiness",
		description= "The glossiness of the hilights.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.reflect_glossiness= FloatProperty(
		name= "Reflection glossiness",
		description= "The glossiness of the reflections.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.refract_glossiness= FloatProperty(
		name= "Refraction glossiness",
		description= "The glossiness of the refractions.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.hilight_glossiness_lock= BoolProperty(
		name= "Hilight glossiness lock",
		description= "",
		default= True
	)

	BRDFVRayMtl.hilight_soften= FloatProperty(
		name= "Hilight soften",
		description= "How much to soften hilights and reflections at grazing light angles",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFVRayMtl.reflect_dim_distance_on= BoolProperty(
		name= "reflect dim distance on",
		description= "True to enable dim distance",
		default= False
	)

	BRDFVRayMtl.reflect_dim_distance_falloff= FloatProperty(
		name= "reflect dim distance falloff",
		description= "Fall off for the dim distance",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	BRDFVRayMtl.anisotropy_derivation= IntProperty(
		name= "anisotropy derivation",
		description= "What method to use for deriving anisotropy axes (0 - local object axis; 1 - a specified uvw generator)",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	BRDFVRayMtl.anisotropy_axis= IntProperty(
		name= "anisotropy axis",
		description= "Which local object axis to use when anisotropy_derivation is 0",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 2
	)

	BRDFVRayMtl.refract_affect_shadows= BoolProperty(
		name= "Affect shadows",
		description= "",
		default= False
	)

	BRDFVRayMtl.refract_affect_alpha= BoolProperty(
		name= "Affect alpha",
		description= "",
		default= False
	)

	BRDFVRayMtl.fog_mult= FloatProperty(
		name= "Fog multiplier",
		description= "Multiplier for the absorption.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 4,
		default= 0.1
	)

	BRDFVRayMtl.fog_unit_scale_on= BoolProperty(
		name= "Fog unit scale",
		description= "Enable unit scale multiplication, when calculating absorption",
		default= True
	)

	BRDFVRayMtl.fog_bias= FloatProperty(
		name= "Fog bias",
		description= "Bias for the absorption.",
		min= -100.0,
		max= 100.0,
		soft_min= -1.0,
		soft_max= 1.0,
		precision= 4,
		default= 0.0
	)

	BRDFVRayMtl.anisotropy= FloatProperty(
		name= "Anisotropy",
		description= "The anisotropy for glossy reflections.",
		min= -1.0,
		max= 1.0,
		soft_min= -1.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFVRayMtl.anisotropy_rotation= FloatProperty(
		name= "Rotation",
		description= "The rotation of the anisotropy axes.",
		min= 0.0,
		max= 360.0,
		soft_min= 0.0,
		soft_max= 360.0,
		default= 0.0
	)

	BRDFVRayMtl.brdf_type= EnumProperty(
		name= "BRDF type",
		description= "This determines the type of BRDF (the shape of the hilight).",
		items= (
			('PHONG',"Phong","Phong hilight/reflections."),
			('BLINN',"Blinn","Blinn hilight/reflections."),
			('WARD',"Ward","Ward hilight/reflections.")
		),
		default= 'BLINN'
	)

	BRDFVRayMtl.refract_trace= BoolProperty(
		name= "Trace refractions",
		description= "",
		default= True
	)

	BRDFVRayMtl.refract_exit_color= FloatVectorProperty(
		name= "Refraction exit color",
		description= "The color to use when maximum depth is reached when refract_exit_color_on is true",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	BRDFVRayMtl.refract_exit_color_on= BoolProperty(
		name= "Use refraction exit color",
		description= "If false, when the maximum refraction depth is reached, the material is assumed transparent, instead of terminating the ray",
		default= False
	)

	BRDFVRayMtl.reflect_trace= BoolProperty(
		name= "Trace reflections",
		description= 'TODO.',
		default= True
	)

	BRDFVRayMtl.option_reflect_on_back= BoolProperty(
		name= "Reflect on back side",
		description= "",
		default= False
	)

	BRDFVRayMtl.option_double_sided= BoolProperty(
		name= "Double-sided",
		description= "",
		default= True
	)

	BRDFVRayMtl.option_glossy_rays_as_gi= EnumProperty(
		name= "Glossy rays as GI",
		description= "Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always",
		items= (
			('ALWAYS',"Always",""),
			('GI',"Only for GI rays",""),
			('NEVER',"Never","")
		),
		default= 'GI'
	)

	BRDFVRayMtl.option_cutoff= FloatProperty(
		name= "Cutoff",
		description= "Specifies a cutoff threshold for tracing reflections/refractions",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.001
	)

	BRDFVRayMtl.option_use_irradiance_map= BoolProperty(
		name= "Use irradiance map",
		description= "false to perform local brute-force GI calculatons and true to use the current GI engine",
		default= True
	)

	BRDFVRayMtl.option_energy_mode= EnumProperty(
		name= "Energy mode",
		description= "Energy preservation mode for reflections and refractions.",
		items= (
			('MONO',"Monochrome",""),
			('COLOR',"Color","")
		),
		default= 'COLOR'
	)

	BRDFVRayMtl.environment_priority= IntProperty(
		name= "Environment priority",
		description= "Environment override priority (used when several materials override it along a ray path)",
		min= 0,
		max= 100,
		default= 0
	)

	BRDFVRayMtl.translucency= EnumProperty(
		name= "Translucency",
		description= "Translucency mode",
		items= (
			('HYBRID',"Hybrid model",""),
			('SOFT',"Soft (water) model",""),
			('HARD',"Hard (wax) model",""),
			('NONE',"None","")
		),
		default= 'NONE'
	)

	BRDFVRayMtl.translucency_color= FloatVectorProperty(
		name= "Translucency_color",
		description= "Filter color for the translucency effect.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFVRayMtl.translucency_light_mult= FloatProperty(
		name= "Translucency light mult",
		description= "A multiplier for the calculated lighting for the translucency effect",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	BRDFVRayMtl.translucency_thickness= FloatProperty(
		name= "Translucency thickness",
		description= "Maximum distance to trace inside the object.",
		min= 0.0,
		max= 100000.0,
		soft_min= 0.0,
		soft_max= 10000.0,
		precision= 3,
		default= 1000.0
	)

	BRDFVRayMtl.translucency_scatter_dir= FloatProperty(
		name= "Translucency scatter dir",
		description= "Scatter direction (0.0 is backward, 1.0 is forward)",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.5
	)

	BRDFVRayMtl.translucency_scatter_coeff= FloatProperty(
		name= "Translucency scatter coeff",
		description= "Scattering cone (0.0 - no scattering, 1.0 - full scattering",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0
	)


def write(bus):
	pass


def gui(context, layout, BRDFVRayMtl, material= None):
	wide_ui= context.region.width > narrowui

	row= layout.row()
	colL= row.column()
	colL.label(text="Diffuse")

	split= layout.split()
	col= split.column()
	if material:
		col.prop(material, "diffuse_color", text="")
	else:
		col.prop(BRDFVRayMtl, 'diffuse', text="")
	col.prop(BRDFVRayMtl, 'roughness')
	if wide_ui:
		col= split.column()
	if material:
		col.prop(material, 'alpha')
	else:
		col.prop(BRDFVRayMtl, 'opacity')

	split= layout.split()
	col= split.column()
	col.label(text="Reflections")

	split= layout.split()
	col= split.column(align=True)
	col.prop(BRDFVRayMtl, 'reflect_color', text="")
	if not BRDFVRayMtl.hilight_glossiness_lock:
		col.prop(BRDFVRayMtl, 'hilight_glossiness', slider=True)
	col.prop(BRDFVRayMtl, "reflect_glossiness", text="Glossiness", slider=True)
	col.prop(BRDFVRayMtl, 'reflect_subdivs', text="Subdivs")
	col.prop(BRDFVRayMtl, 'reflect_depth', text="Depth")
	if wide_ui:
		col= split.column()
	col.prop(BRDFVRayMtl, 'brdf_type', text="")
	col.prop(BRDFVRayMtl, "hilight_glossiness_lock")

	if not BRDFVRayMtl.brdf_type == 'PHONG':
		col.prop(BRDFVRayMtl, "anisotropy")
		col.prop(BRDFVRayMtl, "anisotropy_rotation")
	col.prop(BRDFVRayMtl, "fresnel")
	if BRDFVRayMtl.fresnel:
		col.prop(BRDFVRayMtl, "fresnel_ior")

	split= layout.split()
	col= split.column()
	col.label(text="Refractions")
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'refract_color', text="")
	sub.prop(BRDFVRayMtl, 'refract_ior', text="IOR")
	sub.prop(BRDFVRayMtl, 'refract_glossiness', text="Glossiness", slider=True)
	sub.prop(BRDFVRayMtl, 'refract_subdivs', text="Subdivs")
	sub.prop(BRDFVRayMtl, 'refract_depth', text="Depth")
	if wide_ui:
		col= split.column()
	col.label(text="Fog")
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'fog_color', text="")
	sub.prop(BRDFVRayMtl, 'fog_mult')
	sub.prop(BRDFVRayMtl, 'fog_bias')
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'refract_affect_alpha')
	sub.prop(BRDFVRayMtl, 'refract_affect_shadows')

	split= layout.split()
	col= split.column()
	col.prop(BRDFVRayMtl, 'dispersion_on')
	if wide_ui:
		col= split.column()
	if BRDFVRayMtl.dispersion_on:
		col.prop(BRDFVRayMtl, 'dispersion')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(BRDFVRayMtl, 'translucency')
	if BRDFVRayMtl.translucency != 'NONE':
		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'translucency_color', text="")
		col.prop(BRDFVRayMtl, 'translucency_thickness', text="Thickness")
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'translucency_scatter_coeff', text="Scatter coeff")
		col.prop(BRDFVRayMtl, 'translucency_scatter_dir', text="Fwd/Bck coeff")
		col.prop(BRDFVRayMtl, 'translucency_light_mult', text="Light multiplier")

	if not material:
		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'reflect_trace')
		col.prop(BRDFVRayMtl, 'refract_trace')
		col.prop(BRDFVRayMtl, 'option_cutoff')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'option_double_sided')
		col.prop(BRDFVRayMtl, 'option_reflect_on_back')
		col.prop(BRDFVRayMtl, 'option_use_irradiance_map')

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'reflect_exit_color')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'refract_exit_color')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'option_glossy_rays_as_gi')
		col.prop(BRDFVRayMtl, 'option_energy_mode')

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'environment_priority')

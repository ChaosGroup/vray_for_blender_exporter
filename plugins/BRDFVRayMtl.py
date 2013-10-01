#
# V-Ray For Blender
#
# http://vray.cgdo.ru
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import bpy
from bpy.props import *

from vb25.utils import *
from vb25.ui.ui import *
from vb25.lib   import VRaySocket
from vb25.lib   import AttributeUtils


TYPE = 'BRDF'
ID   = 'BRDFVRayMtl'
PID  =  1

MAIN_BRDF = True # To show in "Material Type" menu

NAME = "VRayMtl"
UI   = "VRayMtl"
DESC = "BRDFVRayMtl settings."

MAPPED_PARAMS = {
	'diffuse' : 'TEXTURE',

	'opacity'   : 'FLOAT_TEXTURE',
	'roughness' : 'FLOAT_TEXTURE',

	'reflect_glossiness' : 'FLOAT_TEXTURE',
	'hilight_glossiness' : 'FLOAT_TEXTURE',
	'refract_glossiness' : 'FLOAT_TEXTURE',
	
	'reflect' : 'TEXTURE',
	'refract' : 'TEXTURE',

	'fresnel_ior' : 'FLOAT_TEXTURE',
	'refract_ior' : 'FLOAT_TEXTURE',

	'anisotropy'          : 'FLOAT_TEXTURE',
	'anisotropy_rotation' : 'FLOAT_TEXTURE',

	'translucency_color' : 'TEXTURE',
}

PARAMS = (
	'opacity',
	'diffuse',
	'roughness',
	## 'brdf_type',
	'reflect',
	'reflect_glossiness',
	'hilight_glossiness',
	'hilight_glossiness_lock',
	'fresnel',
	'fresnel_ior',
	'fresnel_ior_lock',
	'reflect_subdivs',
	'reflect_trace',
	'reflect_depth',
	'reflect_exit_color',
	'hilight_soften',
	'reflect_dim_distance',
	'reflect_dim_distance_on',
	'reflect_dim_distance_falloff',
	'reflect_affect_alpha',
	'anisotropy',
	'anisotropy_rotation',
	'anisotropy_derivation',
	'anisotropy_axis',
	## 'anisotropy_uvwgen',
	'refract',
	'refract_ior',
	'dispersion_on',
	'dispersion',
	'refract_glossiness',
	'refract_subdivs',
	'refract_trace',
	'refract_depth',
	'refract_exit_color',
	'refract_exit_color_on',
	'refract_affect_alpha',
	'refract_affect_shadows',
	'fog_color',
	'fog_mult',
	'fog_bias',
	'fog_unit_scale_on',
	'translucency',
	'translucency_color',
	'translucency_light_mult',
	'translucency_scatter_dir',
	'translucency_scatter_coeff',
	'translucency_thickness',
	'option_double_sided',
	'option_reflect_on_back',
	'option_glossy_rays_as_gi',
	'option_cutoff',
	'option_use_irradiance_map',
	'option_energy_mode',
	## 'environment_override',
	'environment_priority',
)

BRDF_TYPE= {
	'PHONG': 0,
	'BLINN': 1,
	'WARD':  2,
}

TRANSLUCENSY= {
	'NONE':   0,
	'HARD':   1,
	'SOFT':   2,
	'HYBRID': 3,
}

GLOSSY_RAYS= {
	'NEVER':  0,
	'GI':     1,
	'ALWAYS': 2,
}

ENERGY_MODE= {
	'COLOR': 0,
	'MONO':  1,
}

AFFECT_ALPHA= {
	'COL':  0,
	'RERF': 1,
	'ALL':  2
}


def add_properties(rna_pointer):
	class BRDFVRayMtl(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(BRDFVRayMtl)

	rna_pointer.BRDFVRayMtl= PointerProperty(
		name= "BRDFVRayMtl",
		type=  BRDFVRayMtl,
		description= "V-Ray BRDFVRayMtl settings"
	)

	BRDFVRayMtl.diffuse= FloatVectorProperty(
		name        = "Diffuse",
		description = "Diffuse color",
		subtype     = 'COLOR',
		min         = 0.0,
		max         = 1.0,
		soft_min    = 0.0,
		soft_max    = 1.0,
		default     = (0.75,0.75,0.75),
		update      = AttributeUtils.callback_match_BI_diffuse
	)

	BRDFVRayMtl.as_viewport_color = BoolProperty(
		name        = "Use As Viewport Color",
		description = "Use BRDF diffuse color as viewport color",
		default     = True,
		update      = AttributeUtils.callback_match_BI_diffuse
	)

	BRDFVRayMtl.opacity= FloatProperty(
		name= "Opacity",
		description= "Opacity",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.fog_color= FloatVectorProperty(
		name= "Fog color",
		description= "Fog color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	BRDFVRayMtl.refract= FloatVectorProperty(
		name= "Refraction color",
		description= "Refraction color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.reflect= FloatVectorProperty(
		name= "Reflection color",
		description= "Reflection color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.reflect_exit_color= FloatVectorProperty(
		name= "Reflection exit color",
		description= "Reflection exit color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	BRDFVRayMtl.fresnel= BoolProperty(
		name= "Fresnel reflections",
		description= "Enable fresnel reflections",
		default= False
	)

	BRDFVRayMtl.fresnel_ior_lock= BoolProperty(
		name= "Fresnel reflections lock",
		description= "",
		default= False
	)

	BRDFVRayMtl.dispersion_on= BoolProperty(
		name= "Dispersion",
		description= "Enable dispersion",
		default= False
	)

	BRDFVRayMtl.dispersion= IntProperty(
		name= "Abbe",
		description= "Dispersion Abbe value",
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
		name        = "Refractions IOR",
		description = "The IOR for refractions",
		min         = 0.0,
		max         = 30.0,
		soft_min    = 0.0,
		soft_max    = 10.0,
		precision   = 4,
		default     = 1.6
	)

	BRDFVRayMtl.reflect_subdivs= IntProperty(
		name= "Reflection subdivs",
		description= "Subdivs for glossy reflections",
		min= 1,
		max= 1000,
		default= 8
	)

	BRDFVRayMtl.reflect_depth= IntProperty(
		name= "Reflections depth",
		description= "The maximum depth for reflections",
		min= 1,
		max= 1000,
		default= 5
	)

	BRDFVRayMtl.refract_depth= IntProperty(
		name= "Refractions depth",
		description= "The maximum depth for refractions",
		min= 1,
		max= 1000,
		default= 5
	)

	BRDFVRayMtl.refract_subdivs= IntProperty(
		name= "Refraction subdivs",
		description= "Subdivs for glossy refractions",
		min= 1,
		max= 1000,
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
		description= "The glossiness of the hilights",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.reflect_glossiness= FloatProperty(
		name= "Reflection glossiness",
		description= "The glossiness of the reflections",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 1.0
	)

	BRDFVRayMtl.refract_glossiness= FloatProperty(
		name= "Refraction glossiness",
		description= "The glossiness of the refractions",
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
		name= "Dim distance",
		description= "Dim distance",
		default= False
	)

	BRDFVRayMtl.reflect_dim_distance= FloatProperty(
		name= "Dim distance",
		description= "How much to dim reflection as length of rays increases",
		min= 0.0,
		max= 100000000.0,
		soft_min= 0.0,
		soft_max= 10000.0,
		default= 100.0
	)

	BRDFVRayMtl.reflect_dim_distance_falloff= FloatProperty(
		name= "Dim distance falloff",
		description= "Falloff for the dim distance",
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

	BRDFVRayMtl.refract_affect_alpha= EnumProperty(
		name= "Affect Channels",
		description= "Which channels refractions affect",
		items= (
			('COL',  "Color Only",   "The transperency will affect only the RGB channel of the final render."),
			('RERF', "Color+Alpha",  "This will cause the material to transmit the alpha of the refracted objects, instead of displaying an opaque alpha.."),
			('ALL',  "All Channels", "All channels and render elements will be affected by the transperency of the material.")
		),
		default= 'COL'
	)

	BRDFVRayMtl.reflect_affect_alpha= EnumProperty(
		name= "Affect Channels",
		description= "Which channels reflections affect",
		items= (
			('COL',  "Color Only",   "The transperency will affect only the RGB channel of the final render."),
			('RERF', "Color+Alpha",  "This will cause the material to transmit the alpha of the refracted objects, instead of displaying an opaque alpha.."),
			('ALL',  "All Channels", "All channels and render elements will be affected by the transperency of the material.")
		),
		default= 'COL'
	)

	BRDFVRayMtl.fog_mult= FloatProperty(
		name= "Fog multiplier",
		description= "Multiplier for the absorption",
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
		description= "Bias for the absorption",
		min= -100.0,
		max= 100.0,
		soft_min= -1.0,
		soft_max= 1.0,
		precision= 4,
		default= 0.0
	)

	BRDFVRayMtl.anisotropy= FloatProperty(
		name= "Anisotropy",
		description= "The anisotropy for glossy reflections",
		min= -1.0,
		max= 1.0,
		soft_min= -1.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFVRayMtl.anisotropy_rotation= FloatProperty(
		name= "Rotation",
		description= "The rotation of the anisotropy axes",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFVRayMtl.brdf_type= EnumProperty(
		name= "BRDF type",
		description= "This determines the type of BRDF (the shape of the hilight)",
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
		description= "Trace reflections",
		default= True
	)

	BRDFVRayMtl.option_reflect_on_back= BoolProperty(
		name= "Reflect on back side",
		description= "Reflect on back side",
		default= False
	)

	BRDFVRayMtl.option_double_sided= BoolProperty(
		name= "Double-sided",
		description= "Double-sided",
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
		name= "Use Irradiance Map",
		description= "false to perform local brute-force GI calculatons and true to use the current GI engine",
		default= True
	)

	BRDFVRayMtl.option_energy_mode= EnumProperty(
		name= "Energy mode",
		description= "Energy preservation mode for reflections and refractions",
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
		description= "Filter color for the translucency effect",
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
		description= "Maximum distance to trace inside the object",
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


def writeDatablock(bus, BRDFVRayMtl, pluginName, mappedParams):
	ofile = bus['files']['materials']
	scene = bus['scene']

	ofile.write("\nBRDFVRayMtl %s {" % pluginName)
	ofile.write("\n\tbrdf_type=%s;" % (a(scene, BRDF_TYPE[BRDFVRayMtl.brdf_type])))

	for param in PARAMS:
		value = getattr(BRDFVRayMtl, param)

		if param in MAPPED_PARAMS:
			if param in mappedParams:
				value = mappedParams[param]

			if MAPPED_PARAMS[param] == 'FLOAT_TEXTURE':
				if type(value) is str:
					value = "%s::out_intensity" % value
		else:
			if param == 'translucency':
				value = TRANSLUCENSY[BRDFVRayMtl.translucency]
			elif param == 'refract_affect_alpha':
				value = AFFECT_ALPHA[BRDFVRayMtl.refract_affect_alpha]
			elif param == 'reflect_affect_alpha':
				value = AFFECT_ALPHA[BRDFVRayMtl.reflect_affect_alpha]
			elif param == 'option_glossy_rays_as_gi':
				value = GLOSSY_RAYS[BRDFVRayMtl.option_glossy_rays_as_gi]
			elif param == 'option_energy_mode':
				value = ENERGY_MODE[BRDFVRayMtl.option_energy_mode]	
			elif param == 'translucency_thickness':
				value = BRDFVRayMtl.translucency_thickness * 1000000000000

		ofile.write("\n\t%s=%s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return pluginName


def write(bus, baseName=None):
	ma       = bus['material']['material']
	textures = bus['textures']

	BRDFVRayMtl = ma.vray.BRDFVRayMtl

	brdf_name = "%s%s%s" % (ID, get_name(ma, prefix='MA'), bus['material']['orco_suffix'])
	if baseName:
		brdf_name = "%s%s%s" % (baseName, ID, bus['material']['orco_suffix'])

	mappedParams = {}
	for key in MAPPED_PARAMS:
		if key in textures:
			mappedParams[key] = textures[key]
		else:
			mappedParams[key] = getattr(BRDFVRayMtl, key)

	writeDatablock(bus, BRDFVRayMtl, brdf_name, mappedParams)

	return brdf_name


def influence(context, layout, slot):
	wide_ui= context.region.width > narrowui

	VRaySlot= slot.texture.vray_slot

	split= layout.split()
	col= split.column()
	col.label(text="Diffuse:")
	split= layout.split()
	col= split.column()
	factor_but(col, VRaySlot, 'map_diffuse',             'diffuse_mult',             "Diffuse")
	factor_but(col, VRaySlot, 'map_roughness',           'roughness_mult',           "Roughness")
	if wide_ui:
		col= split.column()
	factor_but(col, VRaySlot, 'map_opacity',             'opacity_mult',             "Opacity")

	split= layout.split()
	col= split.column()
	col.label(text="Reflection:")
	split= layout.split()
	col= split.column()
	factor_but(col, VRaySlot, 'map_reflect',             'reflect_mult',             "Reflect")
	factor_but(col, VRaySlot, 'map_reflect_glossiness',  'reflect_glossiness_mult',  "Glossiness")
	factor_but(col, VRaySlot, 'map_hilight_glossiness',  'hilight_glossiness_mult',  "Hilight")
	if wide_ui:
		col= split.column()
	factor_but(col, VRaySlot, 'map_anisotropy',          'anisotropy_mult',          "Anisotropy")
	factor_but(col, VRaySlot, 'map_anisotropy_rotation', 'anisotropy_rotation_mult', "Rotation")
	factor_but(col, VRaySlot, 'map_fresnel_ior',         'fresnel_ior_mult',         "Fresnel")

	split= layout.split()
	col= split.column()
	col.label(text="Refraction:")
	split= layout.split()
	col= split.column()
	factor_but(col, VRaySlot, 'map_refract',            'refract_mult',            "Refract")
	factor_but(col, VRaySlot, 'map_refract_glossiness', 'refract_glossiness_mult', "Glossiness")
	if wide_ui:
		col= split.column()
	factor_but(col, VRaySlot, 'map_refract_ior',        'refract_ior_mult',        "IOR")
	factor_but(col, VRaySlot, 'map_translucency_color', 'translucency_color_mult', "Translucency")


def gui_options(context, layout, BRDFVRayMtl):
	contextType = GetContextType(context)
	regionWidth = GetRegionWidthFromContext(context)

	wide_ui = regionWidth > narrowui

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
	if wide_ui:
		sub= split.column(align=True)
		sub.prop(BRDFVRayMtl, 'reflect_dim_distance_on', text="Dim reflect ray distance")
		sub_r= sub.row()
		sub_r.active= BRDFVRayMtl.reflect_dim_distance_on
		sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance', text="Distance")
		sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance_falloff', text="Falloff")
	else:
		sub= split.column(align=True)
		sub.prop(BRDFVRayMtl, 'reflect_dim_distance_on')
		sub_r= sub.column()
		sub_r.active= BRDFVRayMtl.reflect_dim_distance_on
		sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance', text="Distance")
		sub_r.prop(BRDFVRayMtl, 'reflect_dim_distance_falloff', text="Falloff")

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


def gui(context, layout, BRDFVRayMtl, node=None):
	contextType = GetContextType(context)
	regionWidth = GetRegionWidthFromContext(context)

	wide_ui = regionWidth > narrowui

	row= layout.row()
	colL= row.column()
	colL.label(text="Diffuse:")

	split= layout.split()
	col= split.column(align= True)
	col.prop(BRDFVRayMtl, 'diffuse', text="")
	col.prop(BRDFVRayMtl, 'opacity', slider=True)
	if wide_ui:
		col= split.column()
	col.prop(BRDFVRayMtl, 'roughness', slider=True)
	col.prop(BRDFVRayMtl, 'as_viewport_color')

	split= layout.split()
	col= split.column()
	col.label(text="Reflections:")

	split= layout.split()
	col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'reflect', text="")
	if not BRDFVRayMtl.hilight_glossiness_lock:
		sub.prop(BRDFVRayMtl, 'hilight_glossiness', slider=True)
	sub.prop(BRDFVRayMtl, 'reflect_glossiness', text="Glossiness", slider=True)
	sub.prop(BRDFVRayMtl, 'reflect_subdivs', text="Subdivs")
	sub.prop(BRDFVRayMtl, 'reflect_depth', text="Depth")
	col.prop(BRDFVRayMtl, 'reflect_affect_alpha', text="Affect")
	if wide_ui:
		col= split.column()
	col.prop(BRDFVRayMtl, 'brdf_type', text="")
	col.prop(BRDFVRayMtl, "hilight_glossiness_lock")
	if not BRDFVRayMtl.brdf_type == 'PHONG':
		sub= col.column(align= True)
		sub.prop(BRDFVRayMtl, 'anisotropy', slider= True)
		sub.prop(BRDFVRayMtl, 'anisotropy_rotation', slider= True)
	col.prop(BRDFVRayMtl, 'fresnel')
	if BRDFVRayMtl.fresnel:
		col.prop(BRDFVRayMtl, 'fresnel_ior')

	split= layout.split()
	col= split.column()
	col.label(text="Refractions:")
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'refract', text="")
	sub.prop(BRDFVRayMtl, 'refract_ior', text="IOR")
	sub.prop(BRDFVRayMtl, 'refract_glossiness', text="Glossiness", slider=True)
	sub.prop(BRDFVRayMtl, 'refract_subdivs', text="Subdivs")
	sub.prop(BRDFVRayMtl, 'refract_depth', text="Depth")
	if wide_ui:
		col= split.column()
	col.label(text="Fog:")
	sub= col.column(align=True)
	sub.prop(BRDFVRayMtl, 'fog_color', text="")
	sub.prop(BRDFVRayMtl, 'fog_mult', text="Mult")
	sub.prop(BRDFVRayMtl, 'fog_bias', slider=True, text="Bias")
	sub.prop(BRDFVRayMtl, 'dispersion_on')
	if BRDFVRayMtl.dispersion_on:
		sub.prop(BRDFVRayMtl, 'dispersion')

	split= layout.split()
	col= split.column()
	col.prop(BRDFVRayMtl, 'refract_affect_alpha', text="Affect")
	if wide_ui:
		col= split.column()
	col.prop(BRDFVRayMtl, 'refract_affect_shadows')

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

	# Material will draw advanced BRDFVRayMtl
	# options in a separate panel
	#
	if contextType not in ['MATERIAL'] or context.material.vray.nodetree:
		layout.separator()

		gui_options(context, layout, BRDFVRayMtl)

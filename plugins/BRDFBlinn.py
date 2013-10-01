'''

  V-Ray/Blender

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

from vb25.lib import ExportUtils


TYPE= 'BRDF'
ID=   'BRDFBlinn'
PID=   7

NAME= 'Glossy'
UI=   "Glossy"
DESC= "BRDFBlinn."


MAPPED_PARAMS = {
	'color_tex'                : 'TEXTURE',
	'hilightGlossiness_tex'    : 'FLOAT_TEXTURE',
	'reflectionGlossiness_tex' : 'FLOAT_TEXTURE',
	'transparency_tex'         : 'FLOAT_TEXTURE',
	'anisotropy'               : 'FLOAT_TEXTURE',
	'anisotropy_rotation'      : 'FLOAT_TEXTURE',
}

PARAMS= (
	# 'anisotropy_uvwgen',
	'anisotropy',
	'anisotropy_rotation',
	'back_side',
	'color_tex',
	'cutoff',
	'fix_dark_edges',
	'hilightGlossiness_tex',
	'imap_color_thresh',
	'imap_max_rate',
	'imap_min_rate',
	'imap_norm_thresh',
	'imap_samples',
	'interpolation_on',
	'reflect_dim_distance',
	'reflect_dim_distance_falloff',
	'reflect_dim_distance_on',
	'reflect_exit_color',
	'reflectionGlossiness_tex',
	'soften_edge',
	'subdivs',
	'trace_depth',
	'trace_reflections',
	'transparency_tex',
)

BRDF_TYPE = {
	'PHONG': 'BRDFPhong',
	'BLINN': 'BRDFBlinn',
	'WARD':  'BRDFWard',
}

GLOSSY_RAYS = {
	'NEVER':  0,
	'GI':     1,
	'ALWAYS': 2,
}


def add_properties(rna_pointer):
	class BRDFBlinn(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(BRDFBlinn)
	
	rna_pointer.BRDFBlinn= PointerProperty(
		name= "BRDFBlinn",
		type=  BRDFBlinn,
		description= "V-Ray BRDFBlinn settings"
	)

	BRDFBlinn.brdf_type= EnumProperty(
		name= "BRDF type",
		description= "This determines the type of BRDF (the shape of the hilight)",
		items= (
			('PHONG',"Phong","Phong hilight/reflections."),
			('BLINN',"Blinn","Blinn hilight/reflections."),
			('WARD',"Ward","Ward hilight/reflections.")
		),
		default= 'BLINN'
	)

	BRDFBlinn.color_tex = FloatVectorProperty(
		name= "Color",
		description= "Reflection color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	BRDFBlinn.transparency_tex = FloatProperty(
		name= "Transparency",
		description= "BRDF transparency",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= 0.0
	)

	BRDFBlinn.cutoff= FloatProperty(
		name= "Cutoff",
		description= "",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.01
	)

	BRDFBlinn.back_side= BoolProperty(
		name= "Back side",
		description= "",
		default= False
	)

	BRDFBlinn.trace_reflections= BoolProperty(
		name= "Trace reflections",
		description= "",
		default= True
	)

	BRDFBlinn.trace_depth= IntProperty(
		name= "Depth",
		description= "The maximum reflection depth (-1 is controlled by the global options)",
		min= -1,
		max= 100,
		soft_min= -1,
		soft_max= 10,
		default= -1
	)

	BRDFBlinn.reflect_exit_color= FloatVectorProperty(
		name= "Exit color",
		description= "The color to use when the maximum depth is reached",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	BRDFBlinn.map_reflect_exit_color= BoolProperty(
		name= "reflect exit color",
		description= "The color to use when the maximum depth is reached",
		default= False
	)

	BRDFBlinn.reflect_exit_color_mult= FloatProperty(
		name= "reflect exit color",
		description= "The color to use when the maximum depth is reached",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# reflect_dim_distance
	BRDFBlinn.reflect_dim_distance= FloatProperty(
		name= "Distance",
		description= "How much to dim reflection as length of rays increases",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1e+18
	)

	# reflect_dim_distance_on
	BRDFBlinn.reflect_dim_distance_on= BoolProperty(
		name= "Dim distance",
		description= "True to enable dim distance",
		default= False
	)

	# reflect_dim_distance_falloff
	BRDFBlinn.reflect_dim_distance_falloff= FloatProperty(
		name= "Falloff",
		description= "Fall off for the dim distance",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	BRDFBlinn.hilightGlossiness_tex= FloatProperty(
		name= "Hilight",
		description= "",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1.0
	)

	BRDFBlinn.reflectionGlossiness_tex= FloatProperty(
		name= "Glossiness",
		description= "",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1.0
	)

	BRDFBlinn.subdivs= IntProperty(
		name= "Subdivs",
		description= "",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	BRDFBlinn.glossyAsGI= EnumProperty(
		name= "Glossy rays as GI",
		description= "Specifies when to treat GI rays as glossy rays (0 - never; 1 - only for rays that are already GI rays; 2 - always",
		items= (
			('ALWAYS',"Always",""),
			('GI',"Only for GI rays",""),
			('NEVER',"Never","")
		),
		default= 'GI'
	)

	BRDFBlinn.soften_edge= FloatProperty(
		name= "Soften edge",
		description= "Soften edge of the BRDF at light/shadow transition",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	BRDFBlinn.interpolation_on= BoolProperty(
		name= "Interpolation",
		description= "",
		default= False
	)

	BRDFBlinn.imap_min_rate= IntProperty(
		name= "Min rate",
		description= "",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= -1
	)

	BRDFBlinn.imap_max_rate= IntProperty(
		name= "Max rate",
		description= "",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	BRDFBlinn.imap_color_thresh= FloatProperty(
		name= "Color thresh",
		description= "",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.25
	)

	BRDFBlinn.imap_norm_thresh= FloatProperty(
		name= "Normal thresh",
		description= "",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.4
	)

	BRDFBlinn.imap_samples= IntProperty(
		name= "Samples",
		description= "",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 20
	)

	BRDFBlinn.anisotropy= FloatProperty(
		name= "Anisotropy",
		description= "Reflection anisotropy in the range (-1, 1)",
		min= -1.0,
		max=  1.0,
		soft_min= -1.0,
		soft_max=  1.0,
		precision= 3,
		default= 0.0
	)

	# anisotropy_uvwgen
	
	BRDFBlinn.anisotropy_rotation= FloatProperty(
		name= "Rotation",
		description= "Anisotropy rotation in the range [0, 1]",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	BRDFBlinn.fix_dark_edges= BoolProperty(
		name= "Fix dark edges",
		description= "true to fix dark edges with glossy reflections; only set this to false for compatibility with older versions",
		default= True
	)


def writeDatablock(bus, dataPointer, pluginName, mappedParams):
	ofile = bus['files']['materials']
	scene = bus['scene']

	brdf_type = BRDF_TYPE[dataPointer.brdf_type]

	ofile.write("\n%s %s {" % (brdf_type, pluginName))
	ofile.write("\n\tcolor=Color(0.0,0.0,0.0);")
	ofile.write("\n\tcolor_tex_mult=1.0;")
	ofile.write("\n\ttransparency=Color(0.0,0.0,0.0);")
	ofile.write("\n\ttransparency_tex_mult=1.0;")
	ofile.write("\n\thilightGlossiness=Color(0.0,0.0,0.0);")
	ofile.write("\n\thilightGlossiness_tex_mult=1.0;")
	ofile.write("\n\treflectionGlossiness=Color(0.0,0.0,0.0);")
	ofile.write("\n\treflectionGlossiness_tex_mult=1.0;")
	ofile.write("\n\tglossyAsGI=%i;" % GLOSSY_RAYS[dataPointer.glossyAsGI])

	ExportUtils.writeParamsBlock(bus, ofile, dataPointer, mappedParams, PARAMS, MAPPED_PARAMS)

	ofile.write("\n}\n")

	return pluginName


def write(bus, VRayBRDF= None, base_name= None):
	print("This shouldn't happen!")
	

def gui(context, layout, BRDFBlinn):
	contextType = GetContextType(context)
	regionWidth = GetRegionWidthFromContext(context)

	wide_ui = regionWidth > narrowui

	split= layout.split()
	col= split.column(align=True)
	col.prop(BRDFBlinn, 'color_tex', text="")
	if wide_ui:
		col= split.column(align=True)
	col.prop(BRDFBlinn, 'transparency_tex', text= "Reflection", slider= True)

	layout.separator()

	split= layout.split()
	col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFBlinn, 'hilightGlossiness_tex', slider= True)
	sub.prop(BRDFBlinn, 'reflectionGlossiness_tex', slider= True)
	sub.prop(BRDFBlinn, 'subdivs')
	sub.prop(BRDFBlinn, 'trace_depth')
	if wide_ui:
		col= split.column()
	col.prop(BRDFBlinn, 'brdf_type', text="")
	if not BRDFBlinn.brdf_type == 'PHONG':
		sub= col.column(align=True)
		sub.prop(BRDFBlinn, 'anisotropy', slider= True)
		# sub.prop(BRDFBlinn, 'anisotropy_uvwgen')
		sub.prop(BRDFBlinn, 'anisotropy_rotation', slider= True)

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'cutoff')
	col.prop(BRDFBlinn, 'back_side')
	col.prop(BRDFBlinn, 'trace_reflections')
	if wide_ui:
		col= split.column()
	col.prop(BRDFBlinn, 'reflect_dim_distance_on')
	if BRDFBlinn.reflect_dim_distance_on:
		col.prop(BRDFBlinn, 'reflect_dim_distance')
		col.prop(BRDFBlinn, 'reflect_dim_distance_falloff')

	layout.separator()

	layout.prop(BRDFBlinn, 'glossyAsGI')
	layout.prop(BRDFBlinn, 'reflect_exit_color', text="Exit Color")

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'soften_edge')
	if wide_ui:
		col= split.column()
	col.prop(BRDFBlinn, 'fix_dark_edges')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'interpolation_on')
	if BRDFBlinn.interpolation_on:
		split= layout.split()
		col= split.column()
		col.prop(BRDFBlinn, 'imap_min_rate')
		col.prop(BRDFBlinn, 'imap_max_rate')
		col.prop(BRDFBlinn, 'imap_samples')
		if wide_ui:
			col= split.column()
		col.prop(BRDFBlinn, 'imap_color_thresh')
		col.prop(BRDFBlinn, 'imap_norm_thresh')

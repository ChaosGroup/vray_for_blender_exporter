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


TYPE= 'BRDF'
ID=   'BRDFBlinn'
PID=   4

NAME= 'BRDFBlinn'
UI=   "Blinn"
DESC= "BRDFBlinn."

PARAMS= (
	'color',
	'color_tex',
	'color_tex_mult',
	'transparency',
	'transparency_tex',
	'transparency_tex_mult',
	'cutoff',
	'back_side',
	'trace_reflections',
	'trace_depth',
	'reflect_exit_color',
	'reflect_dim_distance',
	'reflect_dim_distance_on',
	'reflect_dim_distance_falloff',
	'hilightGlossiness',
	'hilightGlossiness_tex',
	'hilightGlossiness_tex_mult',
	'reflectionGlossiness',
	'reflectionGlossiness_tex',
	'reflectionGlossiness_tex_mult',
	'subdivs',
	'glossyAsGI',
	'soften_edge',
	'interpolation_on',
	'imap_min_rate',
	'imap_max_rate',
	'imap_color_thresh',
	'imap_norm_thresh',
	'imap_samples',
	'anisotropy',
	'anisotropy_uvwgen',
	'anisotropy_rotation',
	'fix_dark_edges',
)


def add_properties(rna_pointer):
	class BRDFBlinn(bpy.types.IDPropertyGroup):
		pass
	
	rna_pointer.BRDFBlinn= PointerProperty(
		name= "BRDFBlinn",
		type=  BRDFBlinn,
		description= "V-Ray BRDFBlinn settings"
	)

	# color
	BRDFBlinn.color= FloatVectorProperty(
		name= "Color",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	# color_tex
	BRDFBlinn.color_tex= StringProperty(
		name= "Color texture",
		description= "TODO: Tooltip",
		default= ""
	)

	BRDFBlinn.map_color_tex= BoolProperty(
		name= "Color texture",
		description= "TODO: Tooltip",
		default= False
	)

	# color_tex_mult
	BRDFBlinn.color_tex_mult= FloatProperty(
		name= "Color texture multiplier",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# transparency
	BRDFBlinn.transparency= FloatVectorProperty(
		name= "Transparency",
		description= "TODO: Tooltip.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	# transparency_tex
	BRDFBlinn.transparency_tex= StringProperty(
		name= "Transparency",
		description= "TODO: Tooltip",
		default= ""
	)

	BRDFBlinn.map_transparency_tex= BoolProperty(
		name= "transparency tex",
		description= "TODO: Tooltip",
		default= False
	)

	# transparency_tex_mult
	BRDFBlinn.transparency_tex_mult= FloatProperty(
		name= "transparency tex",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# cutoff
	BRDFBlinn.cutoff= FloatProperty(
		name= "Cut-off",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.01
	)

	# back_side
	BRDFBlinn.back_side= BoolProperty(
		name= "Back side",
		description= "TODO: Tooltip.",
		default= False
	)

	# trace_reflections
	BRDFBlinn.trace_reflections= BoolProperty(
		name= "Trace reflections",
		description= "TODO: Tooltip.",
		default= True
	)

	# trace_depth
	BRDFBlinn.trace_depth= IntProperty(
		name= "Depth",
		description= "The maximum reflection depth (-1 is controlled by the global options).",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= -1
	)

	# reflect_exit_color
	BRDFBlinn.reflect_exit_color= FloatVectorProperty(
		name= "Exit color",
		description= "The color to use when the maximum depth is reached.",
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
		description= "The color to use when the maximum depth is reached.",
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
		description= "How much to dim reflection as length of rays increases.",
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
		description= "True to enable dim distance.",
		default= False
	)

	# reflect_dim_distance_falloff
	BRDFBlinn.reflect_dim_distance_falloff= FloatProperty(
		name= "Falloff",
		description= "Fall off for the dim distance.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# hilightGlossiness
	BRDFBlinn.hilightGlossiness= FloatProperty(
		name= "Hilight",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# hilightGlossiness_tex
	BRDFBlinn.map_hilightGlossiness_tex= BoolProperty(
		name= "hilightGlossiness tex",
		description= "TODO: Tooltip",
		default= False
	)

	# hilightGlossiness_tex_mult
	BRDFBlinn.hilightGlossiness_tex_mult= FloatProperty(
		name= "hilightGlossiness tex mult",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# reflectionGlossiness
	BRDFBlinn.reflectionGlossiness= FloatProperty(
		name= "Glossiness",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# reflectionGlossiness_tex
	BRDFBlinn.map_reflectionGlossiness_tex= BoolProperty(
		name= "reflectionGlossiness tex",
		description= "TODO: Tooltip",
		default= False
	)

	# reflectionGlossiness_tex_mult
	BRDFBlinn.reflectionGlossiness_tex_mult= FloatProperty(
		name= "reflectionGlossiness tex mult",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# subdivs
	BRDFBlinn.subdivs= IntProperty(
		name= "Subdivs",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	# glossyAsGI
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

	# soften_edge
	BRDFBlinn.soften_edge= FloatProperty(
		name= "soften edge",
		description= "Soften edge of the BRDF at light/shadow transition.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# interpolation_on
	BRDFBlinn.interpolation_on= BoolProperty(
		name= "interpolation on",
		description= "TODO: Tooltip.",
		default= False
	)

	# imap_min_rate
	BRDFBlinn.imap_min_rate= IntProperty(
		name= "imap min rate",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= -1
	)

	# imap_max_rate
	BRDFBlinn.imap_max_rate= IntProperty(
		name= "imap max rate",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1
	)

	# imap_color_thresh
	BRDFBlinn.imap_color_thresh= FloatProperty(
		name= "imap color thresh",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.25
	)

	# imap_norm_thresh
	BRDFBlinn.imap_norm_thresh= FloatProperty(
		name= "imap norm thresh",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.4
	)

	# imap_samples
	BRDFBlinn.imap_samples= IntProperty(
		name= "imap samples",
		description= "TODO: Tooltip.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 20
	)

	# anisotropy
	BRDFBlinn.anisotropy= FloatProperty(
		name= "Anisotropy",
		description= "Reflection anisotropy in the range (-1, 1).",
		min= -1.0,
		max=  1.0,
		soft_min= -1.0,
		soft_max=  1.0,
		precision= 3,
		default= 0.0
	)

	BRDFBlinn.map_anisotropy= BoolProperty(
		name= "Anisotropy",
		description= "Reflection anisotropy in the range (-1, 1)",
		default= False
	)

	BRDFBlinn.anisotropy_mult= FloatProperty(
		name= "anisotropy",
		description= "Reflection anisotropy in the range (-1, 1).",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# anisotropy_uvwgen
	
	# anisotropy_rotation
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

	BRDFBlinn.map_anisotropy_rotation= BoolProperty(
		name= "anisotropy rotation",
		description= "Anisotropy rotation in the range [0, 1]",
		default= False
	)

	BRDFBlinn.anisotropy_rotation_mult= FloatProperty(
		name= "anisotropy rotation",
		description= "Anisotropy rotation in the range [0, 1].",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# fix_dark_edges
	BRDFBlinn.fix_dark_edges= BoolProperty(
		name= "fix dark edges",
		description= "true to fix dark edges with glossy reflections; only set this to false for compatibility with older versions.",
		default= True
	)


def write(bus):
	brdf_name= "BRDFBlinn"

	# BRDFBlinn= getattr(scene.vray, PLUG)
	# ofile.write("\n%s %s {"%(PLUG, tex_name))
	# for param in PARAMS:
	# 	value= getattr(BRDFBlinn, param)
	# 	ofile.write("\n\t%s= %s;"%(param, p(value)))
	# ofile.write("\n}\n")

	return brdf_name


'''
  GUI
'''
def gui(context, layout, BRDFBlinn):
	wide_ui= context.region.width > narrowui

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'color')
	col.prop_search(BRDFBlinn, 'color_tex',
					bpy.data, 'textures',
					text= "")
	if BRDFBlinn.color_tex:
		col.prop(BRDFBlinn, 'color_tex_mult')
	if wide_ui:
		col= split.column()
	col.prop(BRDFBlinn, 'transparency', text="Reflection")
	col.prop_search(BRDFBlinn, 'transparency_tex',
					bpy.data, 'textures',
					text= "")
	if BRDFBlinn.transparency_tex:
		col.prop(BRDFBlinn, 'transparency_tex_mult')

	split= layout.split()
	col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFBlinn, 'hilightGlossiness')
	# sub.prop(BRDFBlinn, 'hilightGlossiness_tex')
	# sub.prop(BRDFBlinn, 'hilightGlossiness_tex_mult')
	sub.prop(BRDFBlinn, 'reflectionGlossiness')
	# sub.prop(BRDFBlinn, 'reflectionGlossiness_tex')
	# sub.prop(BRDFBlinn, 'reflectionGlossiness_tex_mult')
	sub.prop(BRDFBlinn, 'subdivs')
	sub.prop(BRDFBlinn, 'trace_depth')
	if wide_ui:
		col= split.column()
	sub= col.column(align=True)
	sub.prop(BRDFBlinn, 'anisotropy')
	# sub.prop(BRDFBlinn, 'anisotropy_uvwgen')
	sub.prop(BRDFBlinn, 'anisotropy_rotation')

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'cutoff')
	col.prop(BRDFBlinn, 'back_side')
	col.prop(BRDFBlinn, 'trace_reflections')
	col.prop(BRDFBlinn, 'reflect_exit_color')
	if wide_ui:
		col= split.column()
	col.prop(BRDFBlinn, 'reflect_dim_distance_on')
	if BRDFBlinn.reflect_dim_distance_on:
		col.prop(BRDFBlinn, 'reflect_dim_distance')
		col.prop(BRDFBlinn, 'reflect_dim_distance_falloff')

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'glossyAsGI')
	col.prop(BRDFBlinn, 'soften_edge')
	# col.prop(BRDFBlinn, 'fix_dark_edges')

	split= layout.split()
	col= split.column()
	col.prop(BRDFBlinn, 'interpolation_on')
	if BRDFBlinn.interpolation_on:
		split= layout.split()
		col= split.column()
		col.prop(BRDFBlinn, 'imap_min_rate')
		col.prop(BRDFBlinn, 'imap_max_rate')
		if wide_ui:
			col= split.column()
		col.prop(BRDFBlinn, 'imap_color_thresh')
		col.prop(BRDFBlinn, 'imap_norm_thresh')
		col.prop(BRDFBlinn, 'imap_samples')



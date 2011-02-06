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
from vb25.plugins import *


TYPE= 'BRDF'
ID=   'BRDFLayered'
PID=   200 # BRDFLayered must be last
MAIN_BRDF= True

NAME= "BRDFLayered"
UI=   "Layered"
DESC= "BRDFLayered."

PARAMS= (
	'brdfs',
	'weights',
	'transparency',
	'transparency_tex',
	'transparency_tex_mult',
	'additive_mode',
	'channels',
)


def add_properties(rna_pointer):
	class VRayBRDF(bpy.types.IDPropertyGroup):
		pass

	class BRDFLayered(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.BRDFLayered= PointerProperty(
		name= "BRDFLayered",
		type=  BRDFLayered,
		description= "V-Ray BRDFLayered settings"
	)

	# brdfs
	BRDFLayered.brdfs= CollectionProperty(
		name= "BRDFs",
		type=  VRayBRDF,
		description= "Material shaders collection."
	)

	BRDFLayered.brdf_selected= IntProperty(
		name= "Selected BRDF",
		description= "Selected BRDF.",
		default= -1,
		min= -1,
		max= 100
	)

	brdfs= gen_menu_items(PLUGINS['BRDF'], none_item= False)
	
	VRayBRDF.type= EnumProperty(
		name= "BRDF Type",
		description= "BRDF type.",
		items= (tuple(brdfs)),
		default= brdfs[4][0] # BRDFDiffuse
	)

	VRayBRDF.use= BoolProperty(
		name= "Use BRDF",
		description= "Use BRDF.",
		default= True
	)

	# weights List()
	VRayBRDF.weight= FloatVectorProperty(
		name= "Weight",
		description= "Weight.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	VRayBRDF.weight_tex= StringProperty(
		name= "Weight texture",
		description= "Weight texture.",
		default= ""
	)

	
	# transparency
	BRDFLayered.transparency= FloatVectorProperty(
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
	BRDFLayered.transparency_tex= StringProperty(
		name= "Transparency",
		description= "TODO: Tooltip",
		default= ""
	)

	BRDFLayered.map_transparency_tex= BoolProperty(
		name= "transparency tex",
		description= "TODO: Tooltip",
		default= False
	)

	# transparency_tex_mult
	BRDFLayered.transparency_tex_mult= FloatProperty(
		name= "transparency tex mult",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# additive_mode
	BRDFLayered.additive_mode= BoolProperty(
		name= "Additive \"shellac\" mode",
		description= "Additive \"shellac\" blending mode.",
		default= False
	)

	# channels List()

	return VRayBRDF
	

def write(ofile, scene, params):
	BRDFLayered= getattr(scene.vray, PLUG)
	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		value= getattr(BRDFLayered, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
def gui(context, layout, BRDFLayered):
	wide_ui= context.region.width > narrowui

	row= layout.row()
	row.template_list(BRDFLayered, 'brdfs',
					  BRDFLayered, 'brdf_selected',
					  rows= 3)

	col= row.column()
	sub= col.row()
	subsub= sub.column(align=True)
	subsub.operator('vray.brdf_add',    text="", icon="ZOOMIN")
	subsub.operator('vray.brdf_remove', text="", icon="ZOOMOUT")
	sub= col.row()
	subsub= sub.column(align=True)
	subsub.operator("vray.brdf_up",   icon='MOVE_UP_VEC',   text="")
	subsub.operator("vray.brdf_down", icon='MOVE_DOWN_VEC', text="")

	split= layout.split()
	col= split.column()
	col.prop(BRDFLayered, 'additive_mode')

	layout.label(text="Transparency:")
	split= layout.split()
	row= split.row(align=True)
	row.prop(BRDFLayered, 'transparency', text="")
	if not wide_ui:
		row= split.column()
	row.prop_search(BRDFLayered, 'transparency_tex',
					bpy.data, 'textures',
					text= "")
	if BRDFLayered.transparency_tex:
		row.prop(BRDFLayered, 'transparency_tex_mult', text="Mult")

	# col.prop(BRDFLayered, 'channels')

	if BRDFLayered.brdf_selected >= 0:
		layout.separator()
		
		brdf= BRDFLayered.brdfs[BRDFLayered.brdf_selected]
		
		if wide_ui:
			split= layout.split(percentage=0.2)
		else:
			split= layout.split()
		col= split.column()
		col.label(text="Name:")
		if wide_ui:
			col= split.column()
		row= col.row(align=True)
		row.prop(brdf, 'name', text="")
		row.prop(brdf, 'use', text="")

		if wide_ui:
			split= layout.split(percentage=0.2)
		else:
			split= layout.split()
		col= split.column()
		col.label(text="Type:")
		if wide_ui:
			col= split.column()
		col.prop(brdf, 'type', text="")

		if wide_ui:
			split= layout.split(percentage=0.2)
		else:
			split= layout.split()
		col= split.column()
		col.label(text="Weight:")
		if wide_ui:
			col= split.row(align=True)
		else:
			col= col.column(align=True)
		col.prop(brdf, 'weight', text="")
		col.prop_search(brdf, 'weight_tex',
						bpy.data, 'textures',
						text= "")
					
		layout.separator()
		
		rna_pointer= getattr(brdf, brdf.type)
		if rna_pointer:
			plugin= PLUGINS['BRDF'].get(brdf.type)
			if plugin:
				plugin.gui(context, layout, rna_pointer)

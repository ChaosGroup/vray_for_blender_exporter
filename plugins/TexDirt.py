'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 22 March 2011 [16:41]"

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
from vb25.shaders import *
from vb25.ui.ui import *


TYPE= 'TEXTURE'

ID=   'TexDirt'
NAME= 'Dirt'
PLUG= 'TexDirt'
DESC= "TODO."
PID=  0

PARAMS= (
	'white_color',
	'black_color',
	'radius',
	'distribution',
	'falloff',
	'subdivs',
	'bias_x',
	'bias_y',
	'bias_z',
	'ignore_for_gi',
	'consider_same_object_only',
	'invert_normal',
	'work_with_transparency',
	'ignore_self_occlusion',
	# 'render_nodes',
	# 'affect_result_nodes',
	'mode',
	'environment_occlusion',
	'affect_reflection_elements',
	# 'glossiness'
)


def add_properties(VRayTexture):
	class TexDirt(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(TexDirt)
	
	VRayTexture.TexDirt= PointerProperty(
		name= "TexDirt",
		type=  TexDirt,
		description= "V-Ray TexDirt settings"
	)

	TexDirt.white_color= FloatVectorProperty(
		name= "Unoccluded color",
		description= "Unoccluded color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	TexDirt.white_color_tex= StringProperty(
		name= "Unoccluded color texture",
		description= "Unoccluded color texture.",
		default= ""
	)

	TexDirt.black_color= FloatVectorProperty(
		name= "Occluded color",
		description= "Occluded color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	TexDirt.black_color_tex= StringProperty(
		name= "Occluded color texture",
		description= "Occluded color texture.",
		default= ""
	)

	TexDirt.radius= FloatProperty(
		name= "Radius",
		description= "Radius.",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 0.1
	)

	TexDirt.distribution= FloatProperty(
		name= "Distribution",
		description= "Distribution.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.falloff= FloatProperty(
		name= "Falloff",
		description= "Falloff.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.subdivs= IntProperty(
		name= "Subdivs",
		description= "Subdivs.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	TexDirt.bias_x= FloatProperty(
		name= "Bias X",
		description= "Bias Z.",
		min= -100.0,
		max= 100.0,
		soft_min= -10.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.bias_y= FloatProperty(
		name= "Bias Y",
		description= "Bias Y.",
		min= -100.0,
		max= 100.0,
		soft_min= -10.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.bias_z= FloatProperty(
		name= "Bias Z",
		description= "Bias Z.",
		min= -100.0,
		max= 100.0,
		soft_min= -10.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.ignore_for_gi= BoolProperty(
		name= "Ignore for GI",
		description= "Ignore for GI.",
		default= True
	)

	TexDirt.consider_same_object_only= BoolProperty(
		name= "Consider same object only",
		description= "Consider same object only.",
		default= False
	)

	TexDirt.invert_normal= BoolProperty(
		name= "Invert normal",
		description= "Invert normal.",
		default= False
	)

	TexDirt.work_with_transparency= BoolProperty(
		name= "Work with transparency",
		description= "Work with transparency.",
		default= False
	)

	TexDirt.ignore_self_occlusion= BoolProperty(
		name= "Ignore self occlusion",
		description= "Ignore self occlusion.",
		default= False
	)

	TexDirt.mode= EnumProperty(
		name= "Mode",
		description= "Mode",
		items= (
			('AO',"Ambient occlusion",""),
			('PHONG',"Phong reflection occlusion",""),
			('BLINN',"Blinn reflection occlusion",""),
			('WARD',"Ward reflection occlusion","")
		),
		default= 'AO'
	)

	TexDirt.environment_occlusion= BoolProperty(
		name= "Environment occlusion",
		description= "Compute the environment for unoccluded samples",
		default= False
	)

	TexDirt.affect_reflection_elements= BoolProperty(
		name= "Affect reflection elements",
		description= "Add the occlusion to relection render elements when mode>0",
		default= False
	)

	TexDirt.glossiness= FloatProperty(
		name= "Glossiness",
		description= "The spread of the rays traced for reflection occlusion.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)


def write(bus):
	MODE= {
		'AO':    0,
		'PHONG': 1,
		'BLINN': 2,
		'WARD':  3
	}

	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	TexDirt= getattr(texture.vray, PLUG)

	mapped_params= {}
	# TODO:
	# for key in ('white_color_tex','black_color_tex'):
	# 	key_tex= getattr(TexDirt, key)
	# 	if key_tex:
	# 		if key_tex in bpy.data.textures:
	# 			bus['mtex']['texture']= bpy.data.textures[key_tex]
	# 			mapped_params[key]= write_texture(bus)

	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		value= getattr(TexDirt, param)
		if param == 'mode':
			value= MODE[TexDirt.mode]

		elif param in ('white_color','black_color'):
			key= param+'_tex'
			if key in mapped_params:
				value= mapped_params[key]
			else:
				pass
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
class TEXTURE_PT_TexDirt(VRayTexturePanel, bpy.types.Panel):
	bl_label = NAME

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		if not tex:
			return False
		vtex= tex.vray
		engine= context.scene.render.engine
		return ((tex and tex.type == 'VRAY' and vtex.type == ID) and (engine_poll(__class__, context)))
	
	def draw(self, context):
		tex= context.texture
		vtex= getattr(tex.vray, PLUG)
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		layout.prop(vtex,'mode')

		split= layout.split()
		col= split.column(align= True)
		col.prop(vtex,'white_color')
		col.prop_search(vtex, 'white_color_tex',
						bpy.data, 'textures',
						text= "")
		if wide_ui:
			col= split.column(align= True)
		col.prop(vtex,'black_color')
		col.prop_search(vtex, 'black_color_tex',
						bpy.data, 'textures',
						text= "")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(vtex,'radius')
		col.prop(vtex,'distribution')
		if vtex.mode != 'AO':
			col.prop(vtex,'glossiness')
		if wide_ui:
			col= split.column()
		col.prop(vtex,'falloff')
		col.prop(vtex,'subdivs')
		if vtex.mode != 'AO':
			col.prop(vtex,'affect_reflection_elements')

		layout.separator()

		split= layout.split()
		row= split.row(align=True)
		row.prop(vtex,'bias_x')
		row.prop(vtex,'bias_y')
		row.prop(vtex,'bias_z')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(vtex,'invert_normal')
		col.prop(vtex,'ignore_for_gi')
		col.prop(vtex,'ignore_self_occlusion')
		col.prop(vtex,'consider_same_object_only')
		if wide_ui:
			col= split.column()
		col.prop(vtex,'work_with_transparency')
		col.prop(vtex,'environment_occlusion')
		
		
bpy.utils.register_class(TEXTURE_PT_TexDirt)

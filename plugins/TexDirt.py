'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''

TYPE= 'TEXTURE'

ID=   'TEXDIRT'
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


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class TexDirt(bpy.types.IDPropertyGroup):
    pass

def add_properties(VRayTexture):
	VRayTexture.TexDirt= PointerProperty(
		name= "TexDirt",
		type=  TexDirt,
		description= "V-Ray TexDirt settings"
	)

	TexDirt.white_color= FloatVectorProperty(
		name= "White color",
		description= "TODO",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	TexDirt.black_color= FloatVectorProperty(
		name= "Black color",
		description= "TODO",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	TexDirt.radius= FloatProperty(
		name= "Radius",
		description= "TODO",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 0.1
	)

	TexDirt.distribution= FloatProperty(
		name= "Distribution",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.falloff= FloatProperty(
		name= "Falloff",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.subdivs= IntProperty(
		name= "Subdivs",
		description= "TODO",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	TexDirt.bias_x= FloatProperty(
		name= "Bias X",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.bias_y= FloatProperty(
		name= "Bias Y",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.bias_z= FloatProperty(
		name= "Bias Z",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	TexDirt.ignore_for_gi= BoolProperty(
		name= "Ignore for GI",
		description= "TODO",
		default= True
	)

	TexDirt.consider_same_object_only= BoolProperty(
		name= "Consider same object only",
		description= "TODO",
		default= False
	)

	TexDirt.invert_normal= BoolProperty(
		name= "Invert normal",
		description= "TODO",
		default= False
	)

	TexDirt.work_with_transparency= BoolProperty(
		name= "Work with transparency",
		description= "TODO",
		default= False
	)

	TexDirt.ignore_self_occlusion= BoolProperty(
		name= "Ignore self occlusion",
		description= "TODO",
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
		description= "true to compute the environment for unoccluded samples",
		default= False
	)

	TexDirt.affect_reflection_elements= BoolProperty(
		name= "Affect reflection elements",
		description= "true to add the occlusion to relection render elements when mode>0",
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


def write(ofile, sce, tex, name= None):
	MODE= {
		'AO':    0,
		'PHONG': 1,
		'BLINN': 2,
		'WARD':  3
	}
	
	tex_name= "%s"%(get_name(tex, "Texture"))
	if name is not None:
		tex_name= name

	vtex= getattr(tex.vray, PLUG)

	ofile.write("\n%s %s {"%(PLUG, tex_name))
	for param in PARAMS:
		if param == 'mode':
			ofile.write("\n\t%s= %s;"%(param, MODE[vtex.mode]))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(sce,getattr(vtex, param))))
	ofile.write("\n}\n")

	return tex_name



'''
  GUI
'''
narrowui= 200


class TexDirtTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_TexDirt(TexDirtTexturePanel, bpy.types.Panel):
	bl_label = NAME

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		if not tex:
			return False
		vtex= tex.vray
		engine= context.scene.render.engine
		return ((tex and tex.type == 'VRAY' and vtex.type == ID) and (engine in __class__.COMPAT_ENGINES))
	
	def draw(self, context):
		tex= context.texture
		vtex= getattr(tex.vray, PLUG)
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		layout.prop(vtex,'mode')

		split= layout.split()
		col= split.column()
		col.prop(vtex,'white_color',text="Unoccluded color")
		if wide_ui:
			col= split.column()
		col.prop(vtex,'black_color',text="Occluded color")

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
		
		
bpy.types.register(TEXTURE_PT_TexDirt)




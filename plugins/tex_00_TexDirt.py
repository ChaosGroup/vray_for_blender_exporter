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


import bpy

from vb25.utils import *


class TexDirt(bpy.types.IDPropertyGroup):
    pass

def add_properties(VRayTexture):
	VRayTexture.PointerProperty(
		attr= 'TexDirt',
		type= TexDirt,
		name= "TexDirt",
		description= "V-Ray TexDirt settings"
	)

	FloatProperty= TexDirt.FloatProperty
	IntProperty= TexDirt.IntProperty
	BoolProperty= TexDirt.BoolProperty
	EnumProperty= TexDirt.EnumProperty
	FloatVectorProperty= TexDirt.FloatVectorProperty
	CollectionProperty= TexDirt.CollectionProperty

	# white_color: acolor texture
	FloatVectorProperty(
		attr= 'white_color',
		name= "White color",
		description= "TODO",
		subtype= "COLOR",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	# black_color: acolor texture
	FloatVectorProperty(
		attr= 'black_color',
		name= "Black color",
		description= "TODO",
		subtype= "COLOR",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	# radius: float texture = 10
	FloatProperty(
		attr= 'radius',
		name= "Radius",
		description= "TODO",
		min= 0.0,
		max= 1000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 0.1
	)

	# distribution: float
	FloatProperty(
		attr= 'distribution',
		name= "distribution",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	# falloff: float
	FloatProperty(
		attr= 'falloff',
		name= "falloff",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	# subdivs: integer
	IntProperty(
		attr= 'subdivs',
		name= "subdivs",
		description= "TODO",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)
	
	# bias_x: float
	FloatProperty(
		attr= 'bias_x',
		name= "bias x",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	# bias_y: float
	FloatProperty(
		attr= 'bias_y',
		name= "bias y",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	# bias_z: float
	FloatProperty(
		attr= 'bias_z',
		name= "bias z",
		description= "TODO",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	# ignore_for_gi: bool
	BoolProperty(
		attr= 'ignore_for_gi',
		name= "ignore for gi",
		description= "TODO",
		default= True
	)
	
	# consider_same_object_only: bool
	BoolProperty(
		attr= 'consider_same_object_only',
		name= "consider same object only",
		description= "TODO",
		default= False
	)
	
	# invert_normal: bool
	BoolProperty(
		attr= 'invert_normal',
		name= "invert normal",
		description= "TODO",
		default= False
	)
	
	# work_with_transparency: bool
	BoolProperty(
		attr= 'work_with_transparency',
		name= "work with transparency",
		description= "TODO",
		default= False
	)
	
	# ignore_self_occlusion: bool
	BoolProperty(
		attr= 'ignore_self_occlusion',
		name= "ignore self occlusion",
		description= "TODO",
		default= False
	)
	
	# render_nodes: plugin, unlimited list
	# affect_result_nodes: plugin, unlimited list

	# mode: integer (Mode (0 - ambient occlusion; 1 - Phong reflection occlusion; 2 - Blinn reflection occlusion; 3 - Ward reflection occlusion))
	EnumProperty(
		attr= 'mode',
		name= "Mode",
		description= "Mode",
		items=(
			('AO',    "Ambient occlusion",          ""),
			('PHONG', "Phong reflection occlusion", ""),
			('BLINN', "Blinn reflection occlusion", ""),
			('WARD',  "Ward reflection occlusion",  "")
		),
		default= 'AO'
	)
	
	# environment_occlusion: bool (true to compute the environment for unoccluded samples)
	BoolProperty(
		attr= 'environment_occlusion',
		name= "environment occlusion",
		description= "true to compute the environment for unoccluded samples",
		default= False
	)
	
	# affect_reflection_elements: bool (true to add the occlusion to relection render elements when mode>0)
	BoolProperty(
		attr= 'affect_reflection_elements',
		name= "affect reflection elements",
		description= "true to add the occlusion to relection render elements when mode>0",
		default= False
	)
	
	# glossiness: float texture (A texture for the glossiness when mode>0)


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

	vtex= getattr(tex.vray_texture, PLUG)

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
		vtex= tex.vray_texture
		engine= context.scene.render.engine
		return ((tex and tex.type == 'PLUGIN' and vtex.type == ID) and (engine in __class__.COMPAT_ENGINES))
	
	def draw(self, context):
		tex= context.texture
		vtex= getattr(tex.vray_texture, PLUG)
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()

		for param in PARAMS:
			col.prop(vtex, param)
		
		
bpy.types.register(TEXTURE_PT_TexDirt)




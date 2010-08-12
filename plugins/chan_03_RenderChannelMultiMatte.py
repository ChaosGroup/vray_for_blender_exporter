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

TYPE= 'RENDERCHANNEL'

ID=   'MULTIMATTE'
NAME= 'MultiMatte'
PLUG= 'RenderChannelMultiMatte'
DESC= "TODO."

PARAMS= (
	'name',
	'red_id',
	'green_id',
	'blue_id',
	'use_mtl_id',
	'affect_matte_objects'
)


import bpy

from vb25.utils import *


class RenderChannelMultiMatte(bpy.types.IDPropertyGroup):
    pass

def add_properties(parent_struct):
	parent_struct.PointerProperty(
		attr= 'RenderChannelMultiMatte',
		type= RenderChannelMultiMatte,
		name= "MultiMatte",
		description= "V-Ray render channel \"MultiMatte\" settings."
	)

	FloatProperty= RenderChannelMultiMatte.FloatProperty
	IntProperty= RenderChannelMultiMatte.IntProperty
	BoolProperty= RenderChannelMultiMatte.BoolProperty
	EnumProperty= RenderChannelMultiMatte.EnumProperty
	FloatVectorProperty= RenderChannelMultiMatte.FloatVectorProperty
	StringProperty= RenderChannelMultiMatte.StringProperty

	# name: string
	StringProperty(
		attr= 'name',
		name= "Name",
		description= "Render channel name",
		maxlen= 64,
		default= "MultiMatte"
	)

	# red_id: integer (The object ID that will be written as the red channel (0 to disable the red channel))
	RenderChannelMultiMatte.IntProperty(
		attr= 'red_id',
		name= "Red ID",
		description= "The object ID that will be written as the red channel (0 to disable the red channel)",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# green_id: integer (The object ID that will be written as the green channel (0 to disable the green channel))
	RenderChannelMultiMatte.IntProperty(
		attr= 'green_id',
		name= "Green ID",
		description= "The object ID that will be written as the green channel (0 to disable the green channel)",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# blue_id: integer (The object ID that will be written as the blue channel (0 to disable the blue channel))
	RenderChannelMultiMatte.IntProperty(
		attr= 'blue_id',
		name= "Blue ID",
		description= "The object ID that will be written as the blue channel (0 to disable the blue channel)",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# use_mtl_id: bool (true to use the material IDs instead of the object IDs)
	RenderChannelMultiMatte.BoolProperty(
		attr= 'use_mtl_id',
		name= "Use material ID",
		description= "true to use the material IDs instead of the object IDs",
		default= False
	)

	# affect_matte_objects: bool (false to not affect Matte Objects)
	RenderChannelMultiMatte.BoolProperty(
		attr= 'affect_matte_objects',
		name= "Affect matte objects",
		description= "false to not affect Matte Objects",
		default= True
	)



'''
  OUTPUT
'''
def write(ofile, render_channel, sce= None, name= None):
	channel_name= render_channel.name
	if name is not None:
		channel_name= name

	ofile.write("\n%s %s {"%(PLUG, clean_string(channel_name)))
	for param in PARAMS:
		if param == 'name':
			value= "\"%s\"" % channel_name
		else:
			value= getattr(render_channel, param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")



'''
  GUI
'''
def draw(rna_pointer, layout, wide_ui):
	split= layout.split()
	col= split.column()
	col.prop(rna_pointer, 'red_id')
	col.prop(rna_pointer, 'green_id')
	col.prop(rna_pointer, 'blue_id')
	if wide_ui:
		col = split.column()
	col.prop(rna_pointer, 'use_mtl_id')
	col.prop(rna_pointer, 'affect_matte_objects')

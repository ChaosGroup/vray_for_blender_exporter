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
ID=   'COLOR'
NAME= 'Color'
PLUG= 'RenderChannelColor'
DESC= "TODO."

PARAMS= (
	'name',
	'alias',
	'color_mapping',
	'consider_for_aa',
	'filtering'
)

import bpy

from vb25.utils import *


class RenderChannelColor(bpy.types.IDPropertyGroup):
	pass

def add_properties(parent_struct):
	parent_struct.PointerProperty(
		attr= 'RenderChannelColor',
		type=  RenderChannelColor,
		name= "Color",
		description= "V-Ray render channel \"Color\" settings."
	)

	# name: string
	RenderChannelColor.StringProperty(
		attr= 'name',
		name= "name",
		description= "TODO.",
		default= "ColorChannel"
	)

	# alias: integer
	RenderChannelColor.IntProperty(
		attr= 'alias',
		name= "Alias",
		description= "TODO.",
		min= 0,
		max= 2000,
		soft_min= 0,
		soft_max= 2000,
		default= 1000
	)
	
	# color_mapping: bool (true to apply color mapping to the channel; false otherwise)
	RenderChannelColor.BoolProperty(
		attr= 'color_mapping',
		name= "Color mapping",
		description= "true to apply color mapping to the channel; false otherwise",
		default= False
	)
	
	# consider_for_aa: bool
	RenderChannelColor.BoolProperty(
		attr= 'consider_for_aa',
		name= "Consider for AA",
		description= "TODO.",
		default= False
	)
	
	# filtering: bool
	RenderChannelColor.BoolProperty(
		attr= 'filtering',
		name= "Filtering",
		description= "TODO.",
		default= True
	)
	


'''
  OUTPUT
'''
def write(ofile, render_channel, sce= None, name= None):
	channel_name= "%s"%(clean_string(render_channel.name))
	if name is not None:
		channel_name= name

	ofile.write("\n%s %s {"%(PLUG, channel_name))
	for param in PARAMS:
		if param == 'name':
			value= "\"%s\"" % getattr(render_channel, param)
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
	col.prop(rna_pointer, 'alias')
	col.prop(rna_pointer, 'filtering')
	if wide_ui:
		col = split.column()
	col.prop(rna_pointer, 'color_mapping')
	col.prop(rna_pointer, 'consider_for_aa')


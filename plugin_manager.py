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


import bpy

import sys
import os
import imp

from vb25.utils import *


TEX_PLUGINS= []
TEX_PLUGINS_TYPES= []

CHANNEL_PLUGINS= []
CHANNEL_PLUGINS_TYPES= []

SETTINGS_PLUGINS= []

base_dir= vb_script_path()
if base_dir is not None:
	plugins_dir= os.path.join(base_dir,"plugins")
	
	if not plugins_dir in sys.path:
		sys.path.append(plugins_dir)

	plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname.endswith(".py")]
	plugins= [__import__(fname) for fname in plugins_files]

	for plugin in plugins:
		sys.stdout.write("V-Ray/Blender: Loading module: %s                    \r"%(plugin.__name__))
		if plugin.TYPE == 'TEXTURE':
			TEX_PLUGINS.append(plugin)
			TEX_PLUGINS_TYPES.append(plugin.ID)
		elif plugin.TYPE == 'RENDERCHANNEL':
			CHANNEL_PLUGINS.append(plugin)
			CHANNEL_PLUGINS_TYPES.append(plugin.ID)
		elif plugin.TYPE == 'SETTINGS':
			SETTINGS_PLUGINS.append(plugin)
		sys.stdout.flush()
	sys.stdout.write("V-Ray/Blender: Loading modules... done.                    \n")


# class VRay(bpy.types.IDPropertyGroup):
# 	pass

class VRayTexture(bpy.types.IDPropertyGroup):
	pass

class VRayScene(bpy.types.IDPropertyGroup):
	pass

class VRayRenderChannel(bpy.types.IDPropertyGroup):
	pass


def add_properties():
	def load_plugins(plugins, parent_struct, items= False):
		if items:
			enum_items= []
			enum_items.append(('NONE',"None",""))
		for plugin in plugins:
			plugin.add_properties(parent_struct)
			if items:
				plugin_desc= []
				plugin_desc.append(plugin.ID)
				plugin_desc.append(plugin.NAME)
				plugin_desc.append(plugin.DESC)
				enum_items.append(tuple(plugin_desc))
		if items:
			return enum_items

	'''
	  Base types
	'''
	bpy.types.Texture.PointerProperty(
		attr= 'vray_texture',
		type= VRayTexture,
		name= "V-Ray Texture Settings",
		description= "V-Ray texture settings."
	)

	# bpy.types.Main.PointerProperty(
	# 	attr= 'vray',
	# 	type= VRay,
	# 	name= "V-Ray Settings",
	# 	description= "V-Ray settings."
	# )

	bpy.types.Scene.PointerProperty(
		attr= 'vray_scene',
		type= VRayScene,
		name= "V-Ray Settings",
		description= "V-Ray settings."
	)


	'''
	  Scene
	'''
	VRayScene.CollectionProperty(
		attr= 'render_channels',
		type= VRayRenderChannel,
		name= "Render Channels",
		description= "V-Ray render channels."
	)

	VRayScene.IntProperty(
		attr= 'render_channels_index',
		name= "Render Channel Index",
		default= -1,
		min= -1,
		max= 100
	)

	'''
	  Texture
	'''
	VRayTexture.EnumProperty(
		attr= 'type',
		name= "Texture Type",
		description= "V-Ray texture type.",
		items= (tuple(load_plugins(TEX_PLUGINS,VRayTexture,items= True))),
		default= 'NONE'
	)

	'''
	  V-Ray: RenderChannel
	'''
	VRayRenderChannel.EnumProperty(
		attr= 'type',
		name= "Channel Type",
		description= "Render channel type.",
		items= (tuple(load_plugins(CHANNEL_PLUGINS,VRayRenderChannel,items= True))),
		default= 'NONE'
	)

	load_plugins(SETTINGS_PLUGINS,VRayScene)
	



def remove_properties():
	bpy.types.Texture.RemoveProperty('vray_texture')
	bpy.types.Scene.RemoveProperty('vray_scene')

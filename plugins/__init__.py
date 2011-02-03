'''

  V-Ray/Blender 2.5

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


''' Python modules '''
import os
import sys

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


PLUGINS= {
	'CAMERA':        {},
	'MATERIAL':      {},
	'GEOMETRY':      {},
	'OBJECT':        {},
	'BRDF':          {},
	'TEXTURE':       {},
	'SETTINGS':      {},
	'RENDERCHANNEL': {},
}


def get_plugin_by_id(plugins, plugin_id):
	for plugin in plugins:
		if plugin.ID == plugin_id:
			return plugin
	return None

def get_plugin_by_name(plugins, plugin_name):
	for plugin in plugins:
		if plugin.PLUG == plugin_name:
			return plugin
	return None

def load_plugins(plugins, parent_struct, items= False):
	if items:
		enum_items= []
		enum_items.append(('NONE',"None",""))
		for plugin in plugins:
			if hasattr(plugin,'ID'):
				enum_items.append((plugin.ID, plugin.NAME, plugin.DESC))
		return enum_items
	else:
		for plugin in plugins:
			plugin.add_properties(parent_struct)


base_dir= get_vray_exporter_path()
if base_dir is not None:
	plugins_dir= os.path.join(base_dir,"plugins")
	
	if not plugins_dir in sys.path:
		sys.path.append(plugins_dir)

	plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname.endswith(".py") and not fname == "__init__.py"]
	plugins= [__import__(fname) for fname in plugins_files]

	for plugin in plugins:
		sys.stdout.write("V-Ray/Blender: Loading module: {0:<64}\r".format(plugin.__name__))
		sys.stdout.flush()
		PLUGINS[plugin.TYPE][plugin.ID]= plugin

	# PLUGINS['TEXTURE']=       sorted(PLUGINS['TEXTURE'],       key=lambda plug: plug.PID)
	# PLUGINS['RENDERCHANNEL']= sorted(PLUGINS['RENDERCHANNEL'], key=lambda plug: plug.PID)
	
	sys.stdout.write("V-Ray/Blender: Loading modules... {0:<64}\n".format("done."))
	sys.stdout.flush()

	for plugin_type in PLUGINS:
		print("Type: %s" % plugin_type)
		for plugin in PLUGINS[plugin_type]:
			print("  %s" % PLUGINS[plugin_type][plugin].NAME)


def add_properties():
	class VRayCamera(bpy.types.IDPropertyGroup):
		pass

	class VRayMesh(bpy.types.IDPropertyGroup):
		pass

	class VRayMaterial(bpy.types.IDPropertyGroup):
		pass

	class VRayTexture(bpy.types.IDPropertyGroup):
		pass

	class VRayScene(bpy.types.IDPropertyGroup):
		pass

	class VRayRenderChannel(bpy.types.IDPropertyGroup):
		pass

	bpy.types.Texture.vray= PointerProperty(
		name= "V-Ray Texture Settings",
		type=  VRayTexture,
		description= "V-Ray texture settings."
	)

	bpy.types.Scene.vray= PointerProperty(
		name= "V-Ray Settings",
		type=  VRayScene,
		description= "V-Ray Renderer settings."
	)

	bpy.types.Material.vray= PointerProperty(
		name= "V-Ray Material Settings",
		type=  VRayMaterial,
		description= "V-Ray material settings"
		)
	bpy.types.Mesh.vray= PointerProperty(
		name= "V-Ray Mesh Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings."
	)

	bpy.types.Curve.vray= PointerProperty(
		name= "V-Ray Curve Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings."
	)

	bpy.types.Camera.vray= PointerProperty(
		name= "V-Ray Camera Settings",
		type=  VRayCamera,
		description= "V-Ray Camera / DoF / Motion Blur settings."
	)

	'''
	  Scene
	'''
	VRayScene.render_channels= CollectionProperty(
		name= "Render Channels",
		type=  VRayRenderChannel,
		description= "V-Ray render channels."
	)

	VRayScene.render_channels_index= IntProperty(
		name= "Render Channel Index",
		default= -1,
		min= -1,
		max= 100
	)

	VRayRenderChannel.type= EnumProperty(
		name= "Channel Type",
		description= "Render channel type.",
		items= (tuple(load_plugins(PLUGINS['RENDERCHANNEL'],VRayRenderChannel,items= True))),
		default= 'NONE'
	)

	'''
	  Texture
	'''
	VRayTexture.type= EnumProperty(
		name= "Texture Type",
		description= "V-Ray texture type.",
		items= (tuple(load_plugins(PLUGINS['TEXTURE'], VRayTexture, items= True))),
		default= 'NONE'
	)

	'''
	  Add plugin properties
	'''
	# load_plugins(PLUGINS['SETTINGS'], VRayScene)
	# load_plugins(PLUGINS['TEXTURE'],  VRayTexture)
	# load_plugins(PLUGINS['GEOMETRY'], VRayMesh)
	# load_plugins(PLUGINS['CAMERA'],   VRayCamera)
	# load_plugins(PLUGINS['MATERIAL'], VRayMaterial)


def remove_properties():
	pass

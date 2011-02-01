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
import imp

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *

PLUGINS= []

TEX_PLUGINS= []
TEX_PLUGINS_TYPES= []

CHANNEL_PLUGINS= []
CHANNEL_PLUGINS_TYPES= []

SETTINGS_PLUGINS= []

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
		PLUGINS.append(plugin)
		if plugin.TYPE == 'TEXTURE':
			TEX_PLUGINS.append(plugin)
			TEX_PLUGINS_TYPES.append(plugin.ID)
		elif plugin.TYPE == 'RENDERCHANNEL':
			CHANNEL_PLUGINS.append(plugin)
			CHANNEL_PLUGINS_TYPES.append(plugin.ID)
		elif plugin.TYPE == 'SETTINGS':
			SETTINGS_PLUGINS.append(plugin)

	TEX_PLUGINS= sorted(TEX_PLUGINS, key=lambda plug: plug.PID)
	CHANNEL_PLUGINS= sorted(CHANNEL_PLUGINS, key=lambda plug: plug.PID)
	
	sys.stdout.write("V-Ray/Blender: Loading modules... {0:<64}\r".format("done."))


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
				enum_items.append((plugin.ID, plugin.NAME, plugin.DESC))
			return enum_items
		else:
			for plugin in plugins:
				plugin.add_properties(parent_struct)

	'''
	  Blender GUI as is
	'''
	import properties_particle
	for member in dir(properties_particle):
		subclass= getattr(properties_particle, member)
		try:
			subclass.COMPAT_ENGINES.add('VRAY_RENDER')
			subclass.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
		except:
			pass
	del properties_particle

	'''
	  RNA pointers
	'''
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
		items= (tuple(load_plugins(CHANNEL_PLUGINS,VRayRenderChannel,items= True))),
		default= 'NONE'
	)

	'''
	  Texture
	'''
	VRayTexture.name= StringProperty(
		name= "V-Ray Texture name",
		description= "V-Ray texture name for internal usage.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

	VRayTexture.type= EnumProperty(
		name= "Texture Type",
		description= "V-Ray texture type.",
		items= (tuple(load_plugins(TEX_PLUGINS, VRayTexture, items= True))),
		default= 'NONE'
	)

	VRayTexture.placement_type= EnumProperty(
		name= "Placement type",
		description= "Image texure placement type.",
		items= (
			('FULL', "Full",  "The whole texture is valid."),
			('CROP', "Crop",  "Crop texture."),
			('PLACE',"Place", "Place texture."),
		),
		default= 'FULL'
	)

	VRayTexture.texture_coords= EnumProperty(
		name= "Coords",
		description= "Image texure placement type.",
		items= (
			('ORCO', "Object", "Generated coordinates."),
			('UV',   "UV",     "Mesh UV coordinates."),
		),
		default= 'UV'
	)

	VRayTexture.tile= EnumProperty(
		name= "Tile",
		description= "Tile type.",
		items= (
			('NOTILE', "No tile", "No tiling."),
			('TILEUV', "Tile UV", "Tile in UV."),
			('TILEU',  "Tile U",  "Tile in U."),
			('TILEV',  "Tile V",  "Tile in V."),
		),
		default= 'TILEUV'
	)

	VRayTexture.mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('FLAT',   "Flat",        "Planar projection."),
			('CUBE',   "Cube",        "Cubic projection."),
			('SPHERE', "Sphere",      "Spherical projection."),
			('TUBE',   "Tube",        "Cylindrical projection."),
			('BALL',   "Ball",        "Ball projection."),
			('TRI',    "Triplanar",   "Triplanar projection."),
			('PERS',   "Perspective", "Perspective projection."),
		),
		default= 'FLAT'
	)

	VRayTexture.environment_mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('SCREEN',  "Screen",      "Planar projection."),
			('CUBIC',   "Cube",        "Cubic projection."),
			('SPHERE',  "Sphere",      "Spherical projection."),
			('TUBE',    "Tube",        "Cylindrical projection."),
			('ANGULAR', "Angular",     "Angular projection."),
			('MBALL',   "Mirror ball", "Mirror ball projection."),
		),
		default= 'SPHERE'
	)

	VRayTexture.object= StringProperty(
		name= "Mapping Object",
		description= "Object to use for mapping generation.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

	'''
	  Add plugin properties
	'''
	load_plugins(SETTINGS_PLUGINS,VRayScene)
	load_plugins(TEX_PLUGINS,VRayTexture)


def remove_properties():
	pass

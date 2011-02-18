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


def load_plugins(plugins, rna_pointer):
	for key in plugins:
		plugins[key].add_properties(rna_pointer)


# Generate menu items from plugins
def gen_menu_items(plugins, none_item= True):
	plugs= [plugins[plug] for plug in plugins if hasattr(plugins[plug], 'PID')]

	# We need to sort plugins by PID so that adding new plugins
	# won't mess enum indexes in existing scenes
	plugs= sorted(plugs, key=lambda plug: plug.PID)
	
	enum_items= []
	if none_item:
		enum_items.append(('NONE', "None", ""))
	for plugin in plugs:
		if hasattr(plugin,'ID'):
			ui_label= plugin.UI if hasattr(plugin,'UI') else plugin.NAME
			enum_items.append((plugin.ID, ui_label, plugin.DESC))

	print("<Debug information. Remove this from release!>")
	for item in enum_items:
		print(" ", item)
	
	return enum_items


base_dir= get_vray_exporter_path()
if base_dir is not None:
	plugins_dir= os.path.join(base_dir,"plugins")
	
	if not plugins_dir in sys.path:
		sys.path.append(plugins_dir)

	plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname.endswith(".py") and not fname == "__init__.py"]
	plugins= [__import__(fname) for fname in plugins_files]

	for plugin in plugins:
		debug(None, "Loading plugin: {0:<32}".format(plugin.__name__), newline= False)
		PLUGINS[plugin.TYPE][plugin.ID]= plugin

	debug(None, "Loading plugins... {0:<32}".format("done."))

	# print("Debug information. Remove this from release!")
	# for plugin_type in PLUGINS:
	# 	print(plugin_type)
	# 	for plugin in PLUGINS[plugin_type]:
	# 		print("  %s" % PLUGINS[plugin_type][plugin].ID)

else:
	debug(None, "Plugins not found!", error= True)


def add_properties():
	class VRayCamera(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayCamera)

	class VRayObject(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayObject)

	class VRayMesh(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayMesh)

	class VRayMaterial(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayMaterial)

	class VRayTexture(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayTexture)

	class VRayScene(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayScene)

	class VRayRenderChannel(bpy.types.PropertyGroup):
		pass

	bpy.utils.register_class(VRayRenderChannel)

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

	bpy.types.Object.vray= PointerProperty(
		name= "V-Ray Object Settings",
		type=  VRayObject,
		description= "V-Ray Object Settings."
	)

	'''
	  Scene
	'''
	VRayScene.render_channels= CollectionProperty(
		name= "Render Channels",
		type=  VRayRenderChannel,
		description= "V-Ray render channels."
	)

	VRayScene.render_channels_use= BoolProperty(
		name= "Use render channels",
		description= "Use render channels.",
		default= False
	)

	VRayScene.render_channels_index= IntProperty(
		name= "Render Channel Index",
		default= -1,
		min= -1,
		max= 100
	)

	'''
	  Passes types
	'''
	VRayRenderChannel.type= EnumProperty(
		name= "Channel Type",
		description= "Render channel type.",
		items= (tuple(gen_menu_items(PLUGINS['RENDERCHANNEL']))),
		default= 'NONE'
	)

	VRayRenderChannel.use= BoolProperty(
		name= "Use channel",
		description= "Use render channel.",
		default= True
	)

	'''
	  Texture types
	'''
	VRayTexture.type= EnumProperty(
		name= "Texture Type",
		description= "V-Ray texture type.",
		items= (tuple(gen_menu_items(PLUGINS['TEXTURE']))),
		default= 'NONE'
	)

	'''
	  Loading plugin properties
	'''
	load_plugins(PLUGINS['SETTINGS'],      VRayScene)
	load_plugins(PLUGINS['TEXTURE'],       VRayTexture)
	load_plugins(PLUGINS['GEOMETRY'],      VRayMesh)
	load_plugins(PLUGINS['CAMERA'],        VRayCamera)
	load_plugins(PLUGINS['MATERIAL'],      VRayMaterial)
	load_plugins(PLUGINS['RENDERCHANNEL'], VRayRenderChannel)

	PLUGINS['SETTINGS']['SettingsEnvironment'].add_properties(VRayMaterial)
	PLUGINS['SETTINGS']['SettingsEnvironment'].add_properties(VRayObject)

	PLUGINS['MATERIAL']['MtlOverride'].add_properties(VRayObject)
	PLUGINS['MATERIAL']['MtlWrapper'].add_properties(VRayObject)
	PLUGINS['MATERIAL']['MtlRenderStats'].add_properties(VRayObject)

	PLUGINS['GEOMETRY']['LightMesh'].add_properties(VRayObject)
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].add_properties(VRayObject)

	PLUGINS['BRDF']['BRDFBump'].add_properties(VRayTexture)

	for key in PLUGINS['BRDF']:
		if key != 'BRDFBump':
			if key == 'BRDFLayered':
				load_plugins(PLUGINS['BRDF'], PLUGINS['BRDF']['BRDFLayered'].add_properties(VRayMaterial))
			else:
				PLUGINS['BRDF'][key].add_properties(VRayMaterial)


def remove_properties():
	del bpy.types.Camera.vray
	del bpy.types.Material.vray
	del bpy.types.Mesh.vray
	del bpy.types.Object.vray
	del bpy.types.Scene.vray
	del bpy.types.Texture.vray

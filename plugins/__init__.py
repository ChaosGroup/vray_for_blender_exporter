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
			enum_items.append((plugin.ID, plugin.NAME, plugin.DESC))

	print("Debug information. Remove this from release!")
	for item in enum_items:
		print(item)
	
	return enum_items


base_dir= get_vray_exporter_path()
if base_dir is not None:
	plugins_dir= os.path.join(base_dir,"plugins")
	
	if not plugins_dir in sys.path:
		sys.path.append(plugins_dir)

	plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname.endswith(".py") and not fname == "__init__.py"]
	plugins= [__import__(fname) for fname in plugins_files]

	for plugin in plugins:
		sys.stdout.write("V-Ray/Blender: Loading plugin: {0:<64}\r".format(plugin.__name__))
		sys.stdout.flush()
		PLUGINS[plugin.TYPE][plugin.ID]= plugin

	sys.stdout.write("V-Ray/Blender: Loading plugins... {0:<64}\n".format("done."))

	print("Debug information. Remove this from release!")
	for plugin_type in PLUGINS:
		print(plugin_type)
		for plugin in PLUGINS[plugin_type]:
			print("  %s" % PLUGINS[plugin_type][plugin].ID)
else:
	sys.stdout.write("V-Ray/Blender: Plugins not found!\n")
sys.stdout.flush()


def add_properties():
	class VRayCamera(bpy.types.IDPropertyGroup):
		pass

	class VRayObject(bpy.types.IDPropertyGroup):
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

	class VRayBRDF(bpy.types.IDPropertyGroup):
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
		description= "Channel.",
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
	  BRDF types
	'''
	VRayMaterial.brdfs= CollectionProperty(
		name= "BRDFs",
		type=  VRayBRDF,
		description= "Material shaders collection."
	)

	VRayMaterial.brdf_selected= IntProperty(
		name= "Selected BRDF",
		description= "Selected BRDF.",
		default= -1,
		min= -1,
		max= 100
	)

	VRayMaterial.additive_mode= BoolProperty(
		name= "Additive \"Shellac\" mode",
		description= "Additive \"Shellac\" blending mode.",
		default= False
	)

	brdfs= gen_menu_items(PLUGINS['BRDF'], none_item= False)
	
	VRayBRDF.type= EnumProperty(
		name= "BRDF Type",
		description= "BRDF type.",
		items= (tuple(brdfs)),
		default= brdfs[0][0]
	)

	'''
	  Loading plugin properties
	'''
	load_plugins(PLUGINS['SETTINGS'],      VRayScene)
	load_plugins(PLUGINS['TEXTURE'],       VRayTexture)
	load_plugins(PLUGINS['GEOMETRY'],      VRayMesh)
	load_plugins(PLUGINS['CAMERA'],        VRayCamera)
	load_plugins(PLUGINS['MATERIAL'],      VRayMaterial)
	load_plugins(PLUGINS['BRDF'],          VRayMaterial)
	load_plugins(PLUGINS['BRDF'],          VRayBRDF)
	load_plugins(PLUGINS['RENDERCHANNEL'], VRayRenderChannel)

	PLUGINS['BRDF']['BRDFBump'].add_properties(VRayTexture)

	PLUGINS['SETTINGS']['SettingsEnvironmet'].add_properties(VRayMaterial)

	PLUGINS['MATERIAL']['MtlOverride'].add_properties(VRayObject)
	PLUGINS['MATERIAL']['MtlWrapper'].add_properties(VRayObject)
	PLUGINS['MATERIAL']['MtlRenderStats'].add_properties(VRayObject)
	PLUGINS['MATERIAL']['LightMesh'].add_properties(VRayObject)
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].add_properties(VRayObject)


def remove_properties():
	pass

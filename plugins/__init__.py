#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import os
import sys
import math
import imp

import bpy

from pynodes_framework import idref

from vb30       import utils
from vb30.debug import Debug
from vb30.lib   import ClassUtils


PLUGINS_DIRS = []
PLUGINS_ID = {}
PLUGINS = {
	'BRDF':          {},
	'CAMERA':        {},
	'GEOMETRY':      {},
	'LIGHT':         {},
	'MATERIAL':      {},
	'OBJECT':        {},
	'RENDERCHANNEL': {},
	'SETTINGS':      {},
	'SLOT':          {},
	'TEXTURE':       {},
	'WORLD':         {},
	'UVWGEN':        {},
	'SYSTEM':        {},
	'EFFECT':        {},
}


##        #######     ###    ########  #### ##    ##  ######
##       ##     ##   ## ##   ##     ##  ##  ###   ## ##    ##
##       ##     ##  ##   ##  ##     ##  ##  ####  ## ##
##       ##     ## ##     ## ##     ##  ##  ## ## ## ##   ####
##       ##     ## ######### ##     ##  ##  ##  #### ##    ##
##       ##     ## ##     ## ##     ##  ##  ##   ### ##    ##
########  #######  ##     ## ########  #### ##    ##  ######

def gen_menu_items(plugins, none_item=True):
	plugs = [plugins[plug] for plug in plugins if hasattr(plugins[plug], 'ID')]

	# We need to sort plugins by PID so that adding new plugins
	# won't mess enum indexes in existing scenes
	plugs = sorted(plugs, key=lambda plug: plug.ID)

	enum_items = []
	if none_item:
		enum_items.append(('NONE', "None", ""))
	for plugin in plugs:
		if not hasattr(plugin, 'ID'):
			continue
		enum_items.append((plugin.ID, plugin.NAME, plugin.DESC))

	return enum_items


# Load settings to the bpy.props.PointerProperty
def AddAttributes(plugin, pointerProp):
	if hasattr(plugin, 'add_properties'):
		plugin.add_properties(pointerProp)
	if hasattr(plugin, 'PluginParams'):
		ClassUtils.RegisterPluginPropertyGroup(pointerProp, plugin)


def LoadPluginAttributes(plugins, pointerProp):
	for plugin in plugins:
		AddAttributes(plugins[plugin], pointerProp)


def GetPluginsDir():
	return os.path.join(utils.get_vray_exporter_path(), "plugins")

def LoadPlugins(PluginDict, PluginIDDict):
	pluginsDir = GetPluginsDir()

	if not pluginsDir or not os.path.exists(pluginsDir):
		Debug("Plugin directory not found!", msgType='ERROR')
		return

	plugins = []
	for dirName, subdirList, fileList in os.walk(pluginsDir):
		if dirName.endswith("__pycache__"):
			continue

		if not dirName in sys.path:
			PLUGINS_DIRS.append(dirName)
			sys.path.append(dirName)

		for fname in fileList:
			if fname == "__init__.py":
				continue
			if not fname.endswith(".py"):
				continue

			module_name, module_ext = os.path.splitext(fname)

			plugins.append(__import__(module_name))

	for plugin in plugins:
		if not hasattr(plugin, 'ID'):
			continue
		PluginDict[plugin.TYPE][plugin.ID] = plugin
		PluginIDDict[plugin.ID] = plugin


def GenerateJsonDescription(pluginModule):
	import json

	if not hasattr(pluginModule, 'PluginParams'):
		Debug("Plugin '%s' has 'PluginParams'!" % p, msgType='ERROR')
		return None

	pluginWidgetTmpl = """{ "widgets": []}"""

	if hasattr(pluginModule, 'PluginWidget'):
		pluginWidget = pluginModule.PluginWidget
	else:
		pluginWidget = pluginWidgetTmpl

	plugWdgDict = None
	try:
		plugWdgDict = json.loads(pluginWidget)
	except ValueError as e:
		print(p, e)

	jsonPlugin = {
		'Type'       : pluginModule.TYPE,
		'ID'         : pluginModule.ID,
		'Name'       : pluginModule.NAME,
		'Desciption' : pluginModule.DESC,
		'Parameters' : pluginModule.PluginParams,
		'Widget'     : plugWdgDict,
	}

	return jsonPlugin


def GetJsonPluginDesc(pluginName):
	import json

	pluginDesc = GenerateJsonDescription(PLUGINS_ID[pluginName])
	return json.dumps(pluginDesc, indent=4, sort_keys=True)


def UpdateJsonDescription():
	pluginsDir = GetPluginsDir()

	if not pluginsDir or not os.path.exists(pluginsDir):
		Debug("Plugin directory not found!", msgType='ERROR')
		return

	jsonDirpath = os.path.expanduser("~/devel/vray/vray_json")

	for p in PLUGINS_ID:
		pluginModule = PLUGINS_ID[p]

		jsonFilepath = os.path.join(jsonDirpath, "%s.json" % p)

		with open(jsonFilepath, 'w') as f:
			jsonPlugin = GenerateJsonDescription(pluginID, outputFile)
			if jsonPlugin is not None:
				json.dump(jsonPlugin, f, indent=4, sort_keys=True)


def GetPluginByName(pluginID):
	for pluginName in PLUGINS_ID:
		plugin = PLUGINS_ID[pluginName]
		if pluginID == plugin.ID:
			return plugin
	return None


 ######     ###    ##     ## ######## ########     ###
##    ##   ## ##   ###   ### ##       ##     ##   ## ##
##        ##   ##  #### #### ##       ##     ##  ##   ##
##       ##     ## ## ### ## ######   ########  ##     ##
##       ######### ##     ## ##       ##   ##   #########
##    ## ##     ## ##     ## ##       ##    ##  ##     ##
 ######  ##     ## ##     ## ######## ##     ## ##     ##

class VRayCamera(bpy.types.PropertyGroup):
	use_camera_loop = bpy.props.BoolProperty(
		name= "Use In \"Camera loop\"",
		description= "Use camera in \"Camera loop\"",
		default= False
	)

	override_fov = bpy.props.BoolProperty(
		name= "Override FOV",
		description= "Override FOV (if you need FOV > 180)",
		default= False
	)

	fov = bpy.props.FloatProperty(
		name= "FOV",
		description= "Field of vision",
		min= 0.0,
		max= math.pi * 2,
		soft_min= 0.0,
		soft_max= math.pi * 2,
		subtype= 'ANGLE',
		precision= 2,
		default= math.pi / 4
	)

	#
	# Hide From View
	#
	hide_from_view= bpy.props.BoolProperty(
		name= "Hide From View",
		description= "Hide objects from current view",
		default= False
	)

	hf_all= bpy.props.BoolProperty(
		name= "Hide from everything",
		description= "Hide objects completely",
		default= False
	)

	hf_all_auto= bpy.props.BoolProperty(
		name= "Hide from everything (automatic)",
		description= "Create group with name \"hf_<camera-name>\"",
		default= False
	)

	hf_all_objects= bpy.props.StringProperty(
		name= "Objects",
		description= "Objects to hide completely: name{;name;etc}",
		default= ""
	)

	hf_all_groups= bpy.props.StringProperty(
		name= "Groups",
		description= "Groups to hide completely: name{;name;etc}",
		default= ""
	)

for key in {'camera', 'gi', 'reflect', 'refract', 'shadows'}:
	setattr(VRayCamera, 'hf_%s' % key, bpy.props.BoolProperty(
		name= "Hide from %s" % key,
		description= "Hide objects from %s" % key,
		default= False)
	)

	setattr(VRayCamera, 'hf_%s_auto' % key, bpy.props.BoolProperty(
		name= "Auto",
		description= "Hide objects automaically from %s" % key,
		default= False)
	)

	setattr(VRayCamera, 'hf_%s_objects' % key, bpy.props.StringProperty(
		name= "Objects",
		description= "Objects to hide from %s" % key,
		default= "")
	)

	setattr(VRayCamera, 'hf_%s_groups' % key, bpy.props.StringProperty(
		name= "Groups",
		description= "Groups to hide from %s" % key,
		default= "")
	)


 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##
class VRayAsset(bpy.types.PropertyGroup):
	scenePrefix = bpy.props.StringProperty(
		name        = "Prefix",
		description = "Scene object name prefix"
	)

	sceneFilepath = bpy.props.StringProperty(
		name        = "File Path",
		subtype     = 'FILE_PATH',
		description = "Path to a *.vrscene file"
	)

	sceneDirpath = bpy.props.StringProperty(
		name        = "Directory Path",
		subtype     = 'DIR_PATH',
		description = "Path to a directory with *.vrscene files"
	)

	sceneReplace = bpy.props.BoolProperty(
		name        = "Override Current Scene Objects",
		description = "Replace objects in the root scene",
		default     = False
	)

	sceneUseTransform = bpy.props.BoolProperty(
		name        = "Use Transform",
		description = "Use Empty transform as scene transform",
		default     = True
	)

	sceneAddNodes = bpy.props.BoolProperty(
		name        = "Add Nodes",
		description = "Add nodes from the included files",
		default     = True
	)

	sceneAddMaterials = bpy.props.BoolProperty(
		name        = "Add Materials",
		description = "Add materials from the included files",
		default     = True
	)

	sceneAddLights = bpy.props.BoolProperty(
		name        = "Add Lights",
		description = "Add lights from the included files",
		default     = True
	)

	sceneAddCameras = bpy.props.BoolProperty(
		name        = "Add Cameras",
		description = "Add cameras from the included files",
		default     = False
	)

	sceneAddEnvironment = bpy.props.BoolProperty(
		name        = "Add Environment",
		description = "Add environment from the included files",
		default     = False
	)


class VRayObject(bpy.types.PropertyGroup):
	overrideWithScene = bpy.props.BoolProperty(
		name        = "Override With VRScene Asset",
		description = "Override with *.vrscene asset",
		default     = False
	)

	is_animated = bpy.props.BoolProperty(
		name        = "Animated",
		description = "Defines object as animated",
		default     =  True
	)

	fade_radius = bpy.props.FloatProperty(
		name = "Sphere Fade Radius",
		description = "Sphere fade gizmo radius",
		min = 0.0,
		max = 10000.0,
		soft_min = 0.0,
		soft_max = 100.0,
		precision = 3,
		default = 1.0
	)


##     ## ########  ######  ##     ##
###   ### ##       ##    ## ##     ##
#### #### ##       ##       ##     ##
## ### ## ######    ######  #########
##     ## ##             ## ##     ##
##     ## ##       ##    ## ##     ##
##     ## ########  ######  ##     ##

class VRayMesh(bpy.types.PropertyGroup):
	pass


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

class VRayMaterial(bpy.types.PropertyGroup):
	pass


##       ####  ######   ##     ## ########
##        ##  ##    ##  ##     ##    ##
##        ##  ##        ##     ##    ##
##        ##  ##   #### #########    ##
##        ##  ##    ##  ##     ##    ##
##        ##  ##    ##  ##     ##    ##
######## ####  ######   ##     ##    ##

class VRayLight(bpy.types.PropertyGroup):
	color_type= bpy.props.EnumProperty(
		name= "Color type",
		description= "Color type",
		items= (
			('RGB',    "RGB", ""),
			('KELVIN', "K",   ""),
		),
		default= 'RGB'
	)

	temperature= bpy.props.IntProperty(
		name= "Temperature",
		description= "Kelvin temperature",
		min= 1000,
		max= 40000,
		step= 100,
		default= 5000
	)

	use_include_exclude= bpy.props.BoolProperty(
		name= "Use Include / Exclude",
		description= "Use Include / Exclude",
		default= False
	)

	include_exclude = bpy.props.EnumProperty(
		name = "Type",
		description = "Include or exclude object from lightning",
		items = (
			('EXCLUDE', "Exclude", ""),
			('INCLUDE', "Include", ""),
		),
		default = 'EXCLUDE'
	)

	include_objects = bpy.props.StringProperty(
		name = "Include objects",
		description = "Include objects: name{;name;etc}"
	)

	include_groups = bpy.props.StringProperty(
		name = "Include groups",
		description = "Include groups: name{;name;etc}"
	)

	omni_type = bpy.props.EnumProperty(
		name = "Omni type",
		description = "Omni light type",
		items = (
			('OMNI',    "Omni",    ""),
			('AMBIENT', "Ambient", ""),
			('SPHERE',  "Sphere",  ""),
		),
		default = 'OMNI'
	)

	direct_type = bpy.props.EnumProperty(
		name = "Direct type",
		description = "Direct light type",
		items = (
			('DIRECT', "Direct", ""),
			('SUN',    "Sun",    ""),
		),
		default = 'DIRECT'
	)

	spot_type = bpy.props.EnumProperty(
		name = "Spot type",
		description = "Spot light subtype",
		items = (
			('SPOT', "Spot", ""),
			('IES',  "IES",  ""),
		),
		default = 'SPOT'
	)


##      ##  #######  ########  ##       ########
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ##     ## ##       ##     ##
##  ##  ## ##     ## ########  ##       ##     ##
##  ##  ## ##     ## ##   ##   ##       ##     ##
##  ##  ## ##     ## ##    ##  ##       ##     ##
 ###  ###   #######  ##     ## ######## ########

class VRayWorld(bpy.types.PropertyGroup):
	global_light_level = bpy.props.FloatProperty(
		name = "Global Light Level",
		description = "A global light level multiplier for all lights",
		min = 0.0,
		soft_max = 2.0,
		precision = 3,
		default = 1.0,
	)


######## ######## ##     ## ######## ##     ## ########  ########
   ##    ##        ##   ##     ##    ##     ## ##     ## ##
   ##    ##         ## ##      ##    ##     ## ##     ## ##
   ##    ######      ###       ##    ##     ## ########  ######
   ##    ##         ## ##      ##    ##     ## ##   ##   ##
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##
   ##    ######## ##     ##    ##     #######  ##     ## ########

class VRayTexture(bpy.types.PropertyGroup):
	pass


########  ######## ##    ## ########  ######## ########     ######## ##       ######## ##     ## ######## ##    ## ########
##     ## ##       ###   ## ##     ## ##       ##     ##    ##       ##       ##       ###   ### ##       ###   ##    ##
##     ## ##       ####  ## ##     ## ##       ##     ##    ##       ##       ##       #### #### ##       ####  ##    ##
########  ######   ## ## ## ##     ## ######   ########     ######   ##       ######   ## ### ## ######   ## ## ##    ##
##   ##   ##       ##  #### ##     ## ##       ##   ##      ##       ##       ##       ##     ## ##       ##  ####    ##
##    ##  ##       ##   ### ##     ## ##       ##    ##     ##       ##       ##       ##     ## ##       ##   ###    ##
##     ## ######## ##    ## ########  ######## ##     ##    ######## ######## ######## ##     ## ######## ##    ##    ##

class VRayRenderChannel(bpy.types.PropertyGroup):
	type= bpy.props.EnumProperty(
		name= "Channel Type",
		description= "Render channel type",
		items= (tuple(gen_menu_items(PLUGINS['RENDERCHANNEL']))),
		default= 'NONE'
	)

	use= bpy.props.BoolProperty(
		name= "",
		description= "Use render channel",
		default= True
	)


 ######   ######  ######## ##    ## ########
##    ## ##    ## ##       ###   ## ##
##       ##       ##       ####  ## ##
 ######  ##       ######   ## ## ## ######
	  ## ##       ##       ##  #### ##
##    ## ##    ## ##       ##   ### ##
 ######   ######  ######## ##    ## ########

class VRayScene(bpy.types.PropertyGroup):
	render_channels= bpy.props.CollectionProperty(
		name= "Render Channels",
		type=  VRayRenderChannel,
		description= "V-Ray render channels"
	)

	render_channels_use= bpy.props.BoolProperty(
		name= "Use render channels",
		description= "Use render channels",
		default= False
	)

	render_channels_index= bpy.props.IntProperty(
		name= "Render Channel Index",
		default= -1,
		min= -1,
		max= 100
	)


class IncluderList(bpy.types.PropertyGroup):
	scene= bpy.props.StringProperty(
		name= "Filepath",
		subtype= 'FILE_PATH',
		description= "Path to a *.vrscene file"
	)

	use= bpy.props.BoolProperty(
		name= "",
		description= "Use scene",
		default= True
	)


class Includer(bpy.types.PropertyGroup):
	use = bpy.props.BoolProperty(
		name        = "Use Includer",
		description = "Add additional *.vrscene files",
		default     = False
	)

	setting= bpy.props.BoolProperty(
		name= "",
		description= "Use scene Settings",
		default= True
	)

	camera= bpy.props.BoolProperty(
		name= "",
		description= "Use camera",
		default= True
	)

	materials= bpy.props.BoolProperty(
		name= "",
		description= "Use materials",
		default= True
	)

	environment= bpy.props.BoolProperty(
		name= "",
		description= "Use environment",
		default= True
	)

	lights= bpy.props.BoolProperty(
		name= "",
		description= "Use lights",
		default= True
	)

	textures= bpy.props.BoolProperty(
		name= "",
		description= "Use textures",
		default= True
	)

	colorMapping_standalone= bpy.props.BoolProperty(
		name= "",
		description= "Use Color Mapping standalone",
		default= True
	)

	geometry= bpy.props.BoolProperty(
		name= "",
		description= "Use scene geometry",
		default= True
	)

	scene_nodes= bpy.props.BoolProperty(
		name= "",
		description= "Use Vray nodes",
		default= True
	)
	
	nodes= bpy.props.CollectionProperty(
		name= "Scene Name",
		type=  IncluderList,
		description= "Custom name scene"
	)

	nodes_selected= bpy.props.IntProperty(
		name= "Scene Index",
		default= -1,
		min= -1,
		max= 100
	)


######## ##     ## ########
##       ##     ## ##     ##
##       ##     ## ##     ##
######   ##     ## ########
##       ##     ## ##   ##
##       ##     ## ##    ##
##        #######  ##     ##

class VRayFur(bpy.types.PropertyGroup):
	width= bpy.props.FloatProperty(
		name= "Width",
		description= "Hair thin",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 0.01,
		precision= 5,
		default= 0.0001
	)

	make_thinner= bpy.props.BoolProperty(
		name= "Make thinner",
		description= "Make hair thiner to the end [experimental]",
		default= False
	)

	thin_start= bpy.props.IntProperty(
		name= "Thin start segment",
		description= "Make hair thiner to the end",
		subtype= 'PERCENTAGE',
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 100,
		default= 70
	)


########     ###    ########  ######## ####  ######  ##       ########  ######
##     ##   ## ##   ##     ##    ##     ##  ##    ## ##       ##       ##    ##
##     ##  ##   ##  ##     ##    ##     ##  ##       ##       ##       ##
########  ##     ## ########     ##     ##  ##       ##       ######    ######
##        ######### ##   ##      ##     ##  ##       ##       ##             ##
##        ##     ## ##    ##     ##     ##  ##    ## ##       ##       ##    ##
##        ##     ## ##     ##    ##    ####  ######  ######## ########  ######

class VRayParticleSettings(bpy.types.PropertyGroup):
	pass


########  ####  ######  ######## ########  #### ########  ##     ## ######## ######## ########  
##     ##  ##  ##    ##    ##    ##     ##  ##  ##     ## ##     ##    ##    ##       ##     ## 
##     ##  ##  ##          ##    ##     ##  ##  ##     ## ##     ##    ##    ##       ##     ## 
##     ##  ##   ######     ##    ########   ##  ########  ##     ##    ##    ######   ##     ## 
##     ##  ##        ##    ##    ##   ##    ##  ##     ## ##     ##    ##    ##       ##     ## 
##     ##  ##  ##    ##    ##    ##    ##   ##  ##     ## ##     ##    ##    ##       ##     ## 
########  ####  ######     ##    ##     ## #### ########   #######     ##    ######## ########  

class VRayRenderNode(bpy.types.PropertyGroup):
	address= bpy.props.StringProperty(
		name= "IP/Hostname",
		description= "Render node IP or hostname"
	)

	use = bpy.props.BoolProperty(
		name = "Use Node",
		description = "Use render node",
		default = True
	)


class VRayDR(bpy.types.PropertyGroup):
	on = bpy.props.BoolProperty(
		name= "Distributed Rendering",
		description= "Distributed rendering",
		default= False
	)

	port = bpy.props.IntProperty(
		name= "Distributed Rendering Port",
		description= "Distributed rendering port",
		min= 0,
		max= 65535,
		default= 20204
	)

	shared_dir = bpy.props.StringProperty(
		name= "Shared Directory",
		subtype= 'DIR_PATH',
		description= "Distributed rendering shader directory"
	)

	share_name = bpy.props.StringProperty(
		name= "Share Name",
		default= "VRAYDR",
		description= "Share name"
	)

	type = bpy.props.EnumProperty(
		name= "Type",
		description= "Distributed rendering network type",
		items= (
			('WW', "Windows - Windows", "Window master & Windows nodes"),
			# ('WU', "Windows - Unix",    "Window master & Unix nodes"),
			('UU', "Unix - Unix",       "Unix master & Unix nodes"),
			# ('UW', "Unix - Windows",    "Unix master & Windows nodes"),
		),
		default= 'WW'
	)

	nodes= bpy.props.CollectionProperty(
		name= "Render Nodes",
		type=  VRayRenderNode,
		description= "V-Ray render nodes"
	)

	nodes_selected= bpy.props.IntProperty(
		name= "Render Node Index",
		default= -1,
		min= -1,
		max= 100
	)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
	return (
		IncluderList,
		Includer,

		VRayRenderNode,
		VRayDR,

		VRayCamera,
		VRayFur,
		VRayLight,
		VRayMaterial,
		VRayMesh,
		VRayObject,
		VRayParticleSettings,
		VRayRenderChannel,
		VRayScene,
		VRayTexture,
		VRayWorld,
	)


def register():
	global PLUGINS
	global PLUGINS_ID

	LoadPlugins(PLUGINS, PLUGINS_ID)

	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)

	idref.bpy_register_idref(VRayScene, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray scene node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeScene',
		options = {'FAKE_USER'},
	))
	
	idref.bpy_register_idref(VRayWorld, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray environment node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeWorld',
		options = {'FAKE_USER'},
	))
	
	idref.bpy_register_idref(VRayMaterial, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray material node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeMaterial',
		options = {'FAKE_USER'},
	))

	idref.bpy_register_idref(VRayObject, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray object node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeObject',
		options = {'FAKE_USER'},
	))

	idref.bpy_register_idref(VRayLight, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray light node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeLight',
		options = {'FAKE_USER'},
	))

	bpy.types.ParticleSettings.vray= bpy.props.PointerProperty(
		name= "V-Ray Particle Settings",
		type=  VRayParticleSettings,
		description= "V-Ray Particle settings"
	)

	VRayParticleSettings.VRayFur = bpy.props.PointerProperty(
		name= "V-Ray Fur Settings",
		type=  VRayFur,
		description= "V-Ray Fur settings"
	)

	bpy.types.Texture.vray= bpy.props.PointerProperty(
		name= "V-Ray Texture Settings",
		type=  VRayTexture,
		description= "V-Ray texture settings"
	)

	bpy.types.Scene.vray= bpy.props.PointerProperty(
		name= "V-Ray Settings",
		type=  VRayScene,
		description= "V-Ray Renderer settings"
	)

	bpy.types.Material.vray= bpy.props.PointerProperty(
		name= "V-Ray Material Settings",
		type=  VRayMaterial,
		description= "V-Ray material settings"
	)

	bpy.types.Mesh.vray= bpy.props.PointerProperty(
		name= "V-Ray Mesh Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings"
	)

	bpy.types.Lamp.vray= bpy.props.PointerProperty(
		name= "V-Ray Lamp Settings",
		type=  VRayLight,
		description= "V-Ray lamp settings"
	)

	bpy.types.Curve.vray= bpy.props.PointerProperty(
		name= "V-Ray Curve Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings"
	)

	bpy.types.Camera.vray= bpy.props.PointerProperty(
		name= "V-Ray Camera Settings",
		type=  VRayCamera,
		description= "V-Ray Camera / DoF / Motion Blur settings"
	)

	bpy.types.Object.vray= bpy.props.PointerProperty(
		name= "V-Ray Object Settings",
		type=  VRayObject,
		description= "V-Ray Object Settings"
	)

	bpy.types.World.vray= bpy.props.PointerProperty(
		name= "V-Ray World Settings",
		type=  VRayWorld,
		description= "V-Ray world settings"
	)

	VRayScene.VRayDR = bpy.props.PointerProperty(
		name = "Distributed rendering",
		type =  VRayDR,
		description = "Distributed rendering settings"
	)

	VRayScene.Includer = bpy.props.PointerProperty(
		name = "Includes",
		type =  Includer,
		description = "Include additional *.vrscene files"
	)

	for pluginName in PLUGINS_ID:
		plugin = PLUGINS_ID[pluginName]
		if hasattr(plugin, 'register'):
			plugin.register()

	LoadPluginAttributes(PLUGINS['BRDF'],          VRayMaterial)
	LoadPluginAttributes(PLUGINS['CAMERA'],        VRayCamera)
	LoadPluginAttributes(PLUGINS['EFFECT'],        VRayScene)
	LoadPluginAttributes(PLUGINS['GEOMETRY'],      VRayMesh)
	LoadPluginAttributes(PLUGINS['LIGHT'],         VRayLight)
	LoadPluginAttributes(PLUGINS['MATERIAL'],      VRayMaterial)
	LoadPluginAttributes(PLUGINS['OBJECT'],        VRayObject)
	LoadPluginAttributes(PLUGINS['RENDERCHANNEL'], VRayRenderChannel)
	LoadPluginAttributes(PLUGINS['SETTINGS'],      VRayScene)
	LoadPluginAttributes(PLUGINS['TEXTURE'],       VRayTexture)
	LoadPluginAttributes(PLUGINS['UVWGEN'],        VRayTexture)

	LoadPluginAttributes(PLUGINS['SYSTEM'],        VRayScene)

	AddAttributes(PLUGINS['SETTINGS']['SettingsEnvironment'], VRayMaterial)
	AddAttributes(PLUGINS['SETTINGS']['SettingsEnvironment'], VRayObject)

	AddAttributes(PLUGINS['SETTINGS']['SettingsCamera'],      VRayCamera)
	AddAttributes(PLUGINS['SETTINGS']['SettingsCameraDof'],   VRayCamera)
	AddAttributes(PLUGINS['SETTINGS']['SettingsMotionBlur'],  VRayCamera)

	VRayScene.Exporter = bpy.props.PointerProperty(
		name = "Exporter",
		type =  bpy.types.VRayExporter,
		description = "Global exporting settings"
	)


def unregister():
	global PLUGINS_ID
	global PLUGINS_DIRS

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

	idref.bpy_unregister_idref(VRayLight,    'ntree')
	idref.bpy_unregister_idref(VRayMaterial, 'ntree')
	idref.bpy_unregister_idref(VRayObject,   'ntree')
	idref.bpy_unregister_idref(VRayScene,    'ntree')
	idref.bpy_unregister_idref(VRayWorld,    'ntree')

	del VRayScene.Exporter

	for pluginName in PLUGINS_ID:
		plugin = PLUGINS_ID[pluginName]
		if hasattr(plugin, 'unregister'):
			plugin.unregister()

	del bpy.types.Camera.vray
	del bpy.types.Lamp.vray
	del bpy.types.Material.vray
	del bpy.types.Mesh.vray
	del bpy.types.Object.vray
	del bpy.types.Scene.vray
	del bpy.types.Texture.vray
	del bpy.types.World.vray

	for plugDir in PLUGINS_DIRS:
		if plugDir in sys.path:
			sys.path.remove(plugDir)
	PLUGINS_DIRS = []

	for plug in PLUGINS_ID:
		del plug

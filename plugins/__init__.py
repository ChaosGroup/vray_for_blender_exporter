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

from vb30.debug import Debug
from vb30.lib   import ClassUtils
from vb30.lib   import SysUtils
from vb30.lib   import PluginUtils


PLUGINS_DIRS = []
PLUGINS_ID = {}
PLUGINS = {
	'BRDF':            {},
	'CAMERA':          {},
	'GEOMETRY':        {},
	'LIGHT':           {},
	'MATERIAL':        {},
	'OBJECT':          {},
	'RENDERCHANNEL':   {},
	'SETTINGS':        {},
	'SETTINGS_GLOBAL': {},
	'SLOT':            {},
	'TEXTURE':         {},
	'WORLD':           {},
	'UVWGEN':          {},
	'SYSTEM':          {},
	'EFFECT':          {},
	'UTILITIES':       {},
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
	return os.path.join(SysUtils.GetExporterPath(), "plugins")


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

	maxPreviewFaces = bpy.props.IntProperty(
		name    = "Max. Preview Faces",
		min     = 100,
		max     = 1000000,
		default = 200
	)


class VRayObject(bpy.types.PropertyGroup):
	data_updated = bpy.props.IntProperty(
		options = {'HIDDEN', 'SKIP_SAVE'},
		default = False
	)

	overrideWithScene = bpy.props.BoolProperty(
		name        = "Override With VRScene Asset",
		description = "Override with *.vrscene asset",
		default     = False
	)

	ntree = bpy.props.PointerProperty(
		name = "Node Tree",
		type = bpy.types.NodeTree,
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeObject',
		description = "V-Ray node tree",
	)

	dupliGroupIDOverride = bpy.props.IntProperty(
		name        = "Dupli Group ID Override",
		description = "Override \"Object ID\" for the whole Dupli Group. -1 - means no override",
		min         = -1,
		default     = -1
	)

	use_instancer = bpy.props.BoolProperty(
		name = "Use Instancer For Dupli / Particles",
		default = True
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
	ntree = bpy.props.PointerProperty(
		name = "Node Tree",
		type = bpy.types.NodeTree,
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeMaterial',
		description = "V-Ray material node tree",
	)



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

	include_exclude= bpy.props.EnumProperty(
		name= "Use Include / Exclude",
		items = (
			('0', "None", ""),
			('1', "Exclude", ""),
			('2', "Include", ""),
		),
		default= '0'
	)

	illumination_shadow= bpy.props.EnumProperty(
		name= "Include / Exclude Type",
		items = (
			('0', "Illumination", ""),
			('1', "Shadow Casting", ""),
			('2', "Illumination / Shadow", ""),
		),
		default = '2'
	)

	exclude_objects= bpy.props.StringProperty(
		name= "Exclude objects",
		description= "Exclude objects"
	)

	exclude_groups= bpy.props.StringProperty(
		name= "Exclude groups",
		description= "Exclude groups"
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

	ntree = bpy.props.PointerProperty(
		name = "Node Tree",
		type = bpy.types.NodeTree,
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeLight',
		description = "V-Ray node tree",
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

	ntree = bpy.props.PointerProperty(
		name = "Node Tree",
		type = bpy.types.NodeTree,
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeWorld',
		description = "V-Ray environment node tree",
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
	pass


 ######   ######  ######## ##    ## ########
##    ## ##    ## ##       ###   ## ##
##       ##       ##       ####  ## ##
 ######  ##       ######   ## ## ## ######
	  ## ##       ##       ##  #### ##
##    ## ##    ## ##       ##   ### ##
 ######   ######  ######## ##    ## ########

class VRayScene(bpy.types.PropertyGroup):
	ntree = bpy.props.PointerProperty(
		name = "Node Tree",
		type = bpy.types.NodeTree,
		poll = lambda s, p: p.bl_idname == 'VRayNodeTreeScene',
		description = "V-Ray scene node tree",
	)


######## ##     ## ########
##       ##     ## ##     ##
##       ##     ## ##     ##
######   ##     ## ########
##       ##     ## ##   ##
##       ##     ## ##    ##
##        #######  ##     ##

class VRayFur(bpy.types.PropertyGroup):
	width = bpy.props.FloatProperty(
		name        = "Width",
		description = "Hair thickness",
		min         = 0.0,
		max         = 100.0,
		soft_min    = 0.0001,
		soft_max    = 0.01,
		precision   = 5,
		default     = 0.001
	)

	widths_in_pixels = bpy.props.BoolProperty(
		name        = "Width In Pixels",
		description = "If true, the widths parameter is in pixels, otherwise it is in world units",
		default     = False
	)

	make_thinner = bpy.props.BoolProperty(
		name        = "Make Thinner",
		description = "Make hair thiner to the end",
		default     = False
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

	assetSharing = bpy.props.EnumProperty(
		name        = "Asset Sharing",
		description = "Asset sharing for distributed rendering",
		items = (
			('TRANSFER', "V-Ray Transfer",   "V-Ray will transfer assets itself"),
			('SHARE',    "Shared Directory", "Share assets via shared directory"),
			('ABSOLUTE', "Absolute Paths",   "Use paths as is"),
		),
		default = 'TRANSFER'
	)

	networkType = bpy.props.EnumProperty(
		name= "Network Type",
		description= "Distributed rendering network type",
		items= (
			('WW', "Windows", "Window master & Windows nodes"),
			('UU', "Unix",    "Unix master & Unix nodes"),
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

	renderOnlyOnNodes = bpy.props.BoolProperty(
		name        = "Render Only On Nodes",
		description = "Use distributed rendering excluding the local machine",
		default     = False
	)

	checkAssets = bpy.props.BoolProperty(
		name        = "Check Asset Cache",
		description = "Check for assets in the asset cache folder before transferring them",
		default     = False
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
		VRayRenderNode,
		VRayDR,

		VRayAsset,
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

	PluginUtils.LoadPluginDesc()
	LoadPlugins(PLUGINS, PLUGINS_ID)

	for jsonPluginName in PluginUtils.PLUGINS_DESC:
		if jsonPluginName not in PLUGINS_ID:
			jsonPlugin = PluginUtils.PLUGINS_DESC[jsonPluginName]

			print("JSON plugin: %s" % jsonPluginName)

			DynPluginType = type(
				# Name
				"JSON%s" % jsonPluginName,
				# Inheritance
				(object,),
				# Attributes
				jsonPlugin
			)

			PLUGINS[jsonPlugin['TYPE']][jsonPlugin['ID']] = DynPluginType
			PLUGINS_ID[jsonPlugin['ID']] = DynPluginType

	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)

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

	VRayObject.VRayAsset = bpy.props.PointerProperty(
		name = "VRayAsset",
		type =  VRayAsset,
		description = "VRayAsset settings"
	)

	# Add global settings to 'VRayExporterPreferences'
	# BEFORE registration
	#
	for pluginName in PLUGINS['SETTINGS_GLOBAL']:
		AddAttributes(
			PLUGINS['SETTINGS_GLOBAL'][pluginName],
			PLUGINS['SYSTEM']['VRayExporter'].VRayExporterPreferences
		)

	# Register properties
	#
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

	LoadPluginAttributes(PLUGINS['UTILITIES'],       VRayScene)
	LoadPluginAttributes(PLUGINS['SYSTEM'],          VRayScene)
	LoadPluginAttributes(PLUGINS['SETTINGS_GLOBAL'], VRayScene)

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

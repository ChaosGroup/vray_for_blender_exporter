#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

import bpy
from bpy.props import *

from pynodes_framework import idref

from vb25.utils import *
from vb25.debug import Debug
from vb25.lib   import ClassUtils


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
}


# Load settings to the RNA Pointer
#
def AddProperties(plugin, rna_pointer):
	if hasattr(plugin, 'add_properties'):
		plugin.add_properties(rna_pointer)
	else:
		ClassUtils.RegisterPluginPropertyGroup(rna_pointer, plugin)


def LoadPlugins(plugins, rna_pointer):
	for plugin in plugins:
		AddProperties(plugins[plugin], rna_pointer)


def gen_menu_items(plugins, none_item= True):
	plugs = [plugins[plug] for plug in plugins if hasattr(plugins[plug], 'ID')]

	# We need to sort plugins by PID so that adding new plugins
	# won't mess enum indexes in existing scenes
	plugs = sorted(plugs, key=lambda plug: plug.PID)

	enum_items = []
	if none_item:
		enum_items.append(('NONE', "None", ""))
	for plugin in plugs:
		if not hasattr(plugin, 'ID'):
			continue
		enum_items.append((plugin.ID, plugin.NAME, plugin.DESC))

	return enum_items


##        #######     ###    ########  #### ##    ##  ######   
##       ##     ##   ## ##   ##     ##  ##  ###   ## ##    ##  
##       ##     ##  ##   ##  ##     ##  ##  ####  ## ##        
##       ##     ## ##     ## ##     ##  ##  ## ## ## ##   #### 
##       ##     ## ######### ##     ##  ##  ##  #### ##    ##  
##       ##     ## ##     ## ##     ##  ##  ##   ### ##    ##  
########  #######  ##     ## ########  #### ##    ##  ######   

base_dir = os.path.join(get_vray_exporter_path(), "plugins")

if not base_dir or not os.path.exists(base_dir):
	Debug("Plugin directory not found!", msgType='ERROR')
else:
	for subdir in ("", "brdf", "texture", "material", "uvwgen", "geometry", "settings", "renderchannel"):
		plugins_dir = os.path.join(base_dir, subdir)

		if not plugins_dir in sys.path:
			sys.path.append(plugins_dir)

		plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname and fname.endswith(".py") and not fname == "__init__.py"]
		plugins= [__import__(fname) for fname in plugins_files]

		for plugin in plugins:
			if not hasattr(plugin, 'ID'):
				continue
			PLUGINS[plugin.TYPE][plugin.ID]= plugin


 ######     ###    ##     ## ######## ########     ###    
##    ##   ## ##   ###   ### ##       ##     ##   ## ##   
##        ##   ##  #### #### ##       ##     ##  ##   ##  
##       ##     ## ## ### ## ######   ########  ##     ## 
##       ######### ##     ## ##       ##   ##   ######### 
##    ## ##     ## ##     ## ##       ##    ##  ##     ## 
 ######  ##     ## ##     ## ######## ##     ## ##     ## 

class VRayCamera(bpy.types.PropertyGroup):
	pass


 #######  ########        ## ########  ######  ######## 
##     ## ##     ##       ## ##       ##    ##    ##    
##     ## ##     ##       ## ##       ##          ##    
##     ## ########        ## ######   ##          ##    
##     ## ##     ## ##    ## ##       ##          ##    
##     ## ##     ## ##    ## ##       ##    ##    ##    
 #######  ########   ######  ########  ######     ##    

class VRayObject(bpy.types.PropertyGroup):
	overrideWithScene = BoolProperty(
		name        = "Override With VRScene Asset",
		description = "Override with *.vrscene asset",
		default     = False
	)

	scenePrefix = StringProperty(
		name        = "Prefix",
		description = "Scene object name prefix"
	)

	sceneFilepath = StringProperty(
		name        = "File Path",
		subtype     = 'FILE_PATH',
		description = "Path to a *.vrscene file"
	)

	sceneDirpath = StringProperty(
		name        = "Directory Path",
		subtype     = 'DIR_PATH',
		description = "Path to a directory with *.vrscene files"
	)

	sceneReplace = BoolProperty(
		name        = "Override Current Scene Objects",
		description = "Replace objects in the root scene",
		default     = False
	)

	sceneUseTransform = BoolProperty(
		name        = "Use Transform",
		description = "Use Empty transform as scene transform",
		default     = True
	)

	sceneAddNodes = BoolProperty(
		name        = "Add Nodes",
		description = "Add nodes from the included files",
		default     = True
	)

	sceneAddMaterials = BoolProperty(
		name        = "Add Materials",
		description = "Add materials from the included files",
		default     = True
	)

	sceneAddLights = BoolProperty(
		name        = "Add Lights",
		description = "Add lights from the included files",
		default     = True
	)

	sceneAddCameras = BoolProperty(
		name        = "Add Cameras",
		description = "Add cameras from the included files",
		default     = False
	)

	sceneAddEnvironment = BoolProperty(
		name        = "Add Environment",
		description = "Add environment from the included files",
		default     = False
	)

	fade_radius= FloatProperty(
		name= "Sphere fade radius",
		description= "Sphere fade gizmo radiusBeam radius",
		min= 0.0,
		max= 10000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 1.0
	)


##     ## ########  ######  ##     ## 
###   ### ##       ##    ## ##     ## 
#### #### ##       ##       ##     ## 
## ### ## ######    ######  ######### 
##     ## ##             ## ##     ## 
##     ## ##       ##    ## ##     ## 
##     ## ########  ######  ##     ## 

class VRayMesh(bpy.types.PropertyGroup):
	override = BoolProperty(
		name        = "Override",
		description = "Override mesh",
		default     = False
	)

	override_type = EnumProperty(
		name        = "Override",
		description = "Override geometry type",
		items = (
			('VRAYPROXY', "VRayProxy", ""),
			('VRAYPLANE', "VRayPlane", ""),
		),
		default = 'VRAYPROXY'
	)


##     ##    ###    ######## ######## ########  ####    ###    ##       
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##       
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##       
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##       
##     ## #########    ##    ##       ##   ##    ##  ######### ##       
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##       
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ######## 

class VRayMaterial(bpy.types.PropertyGroup):
	dontOverride = BoolProperty(
		name        = "Don't Override",
		description = "Don't override material",
		default     = False
	)


##       ####  ######   ##     ## ######## 
##        ##  ##    ##  ##     ##    ##    
##        ##  ##        ##     ##    ##    
##        ##  ##   #### #########    ##    
##        ##  ##    ##  ##     ##    ##    
##        ##  ##    ##  ##     ##    ##    
######## ####  ######   ##     ##    ##    

class VRayLight(bpy.types.PropertyGroup):
	dome_targetRadius= FloatProperty(
		name= "Target Radius",
		description= "Target Radius",
		min= 0.0,
		max= 10000.0,
		soft_min= 0.0,
		soft_max= 200.0,
		precision= 3,
		default= 100
	)

	dome_emitRadius= FloatProperty(
		name= "Emit Radius",
		description= "Emit Radius",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 150
	)

	dome_spherical= BoolProperty(
		name= "Spherical",
		description= "Use sphere instead of half-sphere",
		default= False
	)

	dome_rayDistanceMode= BoolProperty(
		name= "Use Ray Distance",
		description= "When enabled the distance at which shadow rays are traced will be limited to the value of \"Ray Distance\" parameter",
		default= False
	)

	dome_rayDistance= FloatProperty(
		name= "Ray Distance",
		description= "specifies the maximum distance to which shadow rays are going to be traced",
		min= 0.0,
		max= 10000000.0,
		soft_min= 50000.0,
		soft_max= 200000.0,
		precision= 2,
		default= 100000.0
	)

	# Move to Light plugin
	enabled= BoolProperty(
		name= "Enabled",
		description= "Turns the light on and off",
		default= True
	)

	units= EnumProperty(
		name= "Intensity units",
		description= "Units for the intensity",
		items= (
			('DEFAULT',"Default",""),
			('LUMENS',"Lumens",""),
			('LUMM',"Lm/m/m/sr",""),
			('WATTSM',"Watts",""),
			('WATM',"W/m/m/sr","")
		),
		default= 'DEFAULT'
	)

	color_type= EnumProperty(
		name= "Color type",
		description= "Color type",
		items= (
			('RGB',    "RGB", ""),
			('KELVIN', "K",   ""),
		),
		default= 'RGB'
	)

	temperature= IntProperty(
		name= "Temperature",
		description= "Kelvin temperature",
		min= 1000,
		max= 40000,
		step= 100,
		default= 5000
	)

	use_include_exclude= BoolProperty(
		name= "Use Include / Exclude",
		description= "Use Include / Exclude",
		default= False
	)

	include_exclude= EnumProperty(
		name= "Type",
		description= "Include or exclude object from lightning",
		items= (
			('EXCLUDE',"Exclude",""),
			('INCLUDE',"Include",""),
		),
		default= 'EXCLUDE'
	)

	include_objects= StringProperty(
		name= "Include objects",
		description= "Include objects: name{;name;etc}"
	)

	include_groups= StringProperty(
		name= "Include groups",
		description= "Include groups: name{;name;etc}"
	)

	fallsize= FloatProperty(
		name= "Beam radius",
		description= "Beam radius, 0.0 if the light has no beam radius",
		min= 0.0,
		max= 10000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 1.0
	)

	omni_type= EnumProperty(
		name= "Omni type",
		description= "Omni light type",
		items= (
			('OMNI',    "Omni",    ""),
			('AMBIENT', "Ambient", ""),
		),
		default= 'OMNI'
	)

	ambientShade= FloatProperty(
		name= "Ambient Shade",
		description= "Ambient Shade",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 1.0
	)

	direct_type= EnumProperty(
		name= "Direct type",
		description= "Direct light type",
		items= (
			('DIRECT', "Direct", ""),
			('SUN',    "Sun",    ""),
		),
		default= 'DIRECT'
	)

	spot_type= EnumProperty(
		name= "Spot type",
		description= "Spot light subtype",
		items= (
			('SPOT', "Spot", ""),
			('IES',  "IES",  ""),
		),
		default= 'SPOT'
	)

	shadows= BoolProperty(
		name= "Shadows",
		description= "Produce shadows",
		default= True
	)

	affectDiffuse= BoolProperty(
		name= "Affect diffuse",
		description= "Produces diffuse lighting",
		default= True
	)

	affectSpecular= BoolProperty(
		name= "Affect specular",
		description= "Produces specular hilights",
		default= True
	)

	affectReflections= BoolProperty(
		name= "Affect reflections",
		description= "Appear in reflections",
		default= False
	)

	shadowColor= FloatVectorProperty(
		name= "Shadow color",
		description= "The shadow color. Anything but black is not physically accurate",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	shadowBias= FloatProperty(
		name= "Shadow bias",
		description= "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	shadowSubdivs= IntProperty(
		name= "Shadow subdivs",
		description= "This value controls the number of samples V-Ray takes to compute area shadows. Lower values mean more noisy results, but will render faster. Higher values produce smoother results but take more time",
		min= 0,
		max= 256,
		default= 8
	)

	shadowRadius= FloatProperty(
		name= "Shadow radius",
		description= "Shadow radius",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0
	)

	decay= FloatProperty(
		name= "Decay",
		description= "Light decay",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 4.0,
		precision= 3,
		default= 2
	)

	cutoffThreshold= FloatProperty(
		name= "Cutoff threshold",
		description= "Light cut-off threshold (speed optimization). If the light intensity for a point is below this threshold, the light will not be computed",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 0.1,
		precision= 3,
		default= 0.001
	)

	intensity= FloatProperty(
		name= "Intensity",
		description= "Light intensity",
		min= 0.0,
		max= 10000000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 4,
		default= 30
	)

	subdivs= IntProperty(
		name= "Subdivs",
		description= "This controls the number of samples for the area shadow. More subdivs produce area shadows with better quality but render slower",
		min= 0,
		max= 256,
		default= 8
	)

	storeWithIrradianceMap= BoolProperty(
		name= "Store with irradiance map",
		description= "When this option is on and GI calculation is set to Irradiance map V-Ray will calculate the effects of the VRayLightRect and store them in the irradiance map",
		default= False
	)

	invisible= BoolProperty(
		name= "Invisible",
		description= "This setting controls whether the shape of the light source is visible in the render result",
		default= False
	)

	noDecay= BoolProperty(
		name= "No decay",
		description= "When this option is on the intensity will not decay with distance",
		default= False
	)

	doubleSided= BoolProperty(
		name= "Double-sided",
		description= "This option controls whether light is beamed from both sides of the plane",
		default= False
	)

	lightPortal= EnumProperty(
		name= "Light portal mode",
		description= "Specifies if the light is a portal light",
		items= (
			('NORMAL',"Normal light",""),
			('PORTAL',"Portal",""),
			('SPORTAL',"Simple portal","")
		),
		default= 'NORMAL'
	)

	radius= FloatProperty(
		name= "Radius",
		description= "Sphere light radius",
		min= 0.0,
		max= 10000.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.0
	)

	sphere_segments= IntProperty(
		name= "Sphere segments",
		description= "Controls the quality of the light object when it is visible either directly or in reflections",
		min= 0,
		max= 100,
		default= 20
	)

	bumped_below_surface_check= BoolProperty(
		name= "Bumped below surface check",
		description= "If the bumped normal should be used to check if the light dir is below the surface",
		default= False
	)

	nsamples= IntProperty(
		name= "Motion blur samples",
		description= "Motion blur samples",
		min= 0,
		max= 10,
		default= 0
	)

	diffuse_contribution= FloatProperty(
		name= "Diffuse contribution",
		description= "A multiplier for the effect of the light on the diffuse",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	specular_contribution= FloatProperty(
		name= "Specular contribution",
		description= "A multiplier for the effect of the light on the specular",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	areaSpeculars= BoolProperty(
		name= "Area speculars",
		description= "When this parameter is enabled, the specular highlights will be computed with the real light shape as defined in the .ies files",
		default= False
	)

	ignoreLightNormals= BoolProperty(
		name= "Ignore light normals",
		description= "When this option is off, more light is emitted in the direction of the source surface normal",
		default= True
	)

	tex_resolution= IntProperty(
		name= "Tex resolution",
		description= "Specifies the resolution at which the texture is sampled when the \"Tex Adaptive\" option is checked",
		min= 1,
		max= 20000,
		soft_max = 1024,
		default= 512
	)

	tex_adaptive= BoolProperty(
		name= "Tex adaptive",
		description= "When this option is checked V-Ray will use impotance sampling on the texture in order to produce better shadows",
		default= True
	)

	causticSubdivs= IntProperty(
		name= "Caustic subdivs",
		description= "Caustic subdivisions. Lower values mean more noisy results, but will render faster. Higher values produce smoother results but take more time",
		min= 1,
		max= 100000,
		default= 1000
	)

	causticMult= FloatProperty(
		name= "Caustics multiplier",
		description= "Caustics multiplier",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	ies_file= StringProperty(
		name= "IES file",
		subtype= 'FILE_PATH',
		description= "IES file"
	)

	soft_shadows= BoolProperty(
		name= "Soft shadows",
		description= "Use the shape of the light as described in the IES profile",
		default= True
	)

	turbidity= FloatProperty(
		name= "Turbidity",
		description= "This parameter determines the amount of dust in the air and affects the color of the sun and sky",
		min= 2.0,
		max= 100.0,
		soft_min= 2.0,
		soft_max= 6.0,
		precision= 3,
		default= 3.0
	)

	intensity_multiplier= FloatProperty(
		name= "Intensity multiplier",
		description= "This is an intensity multiplier for the Sun",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 4,
		default= 1.0
	)

	ozone= FloatProperty(
		name= "Ozone",
		description= "This parameter affects the color of the sun light",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.35
	)

	water_vapour= FloatProperty(
		name= "Water vapour",
		description= "Water vapour",
		min= 0.0,
		max= 10.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 2
	)

	size_multiplier= FloatProperty(
		name= "Size",
		description= "This parameter controls the visible size of the sun",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	horiz_illum= FloatProperty(
		name= "Horiz illumination",
		description= "Specifies the intensity (in lx) of the illumination on horizontal surfaces coming from the Sky",
		min= 0.0,
		max= 100000.0,
		soft_min= 0.0,
		soft_max= 100000.0,
		precision= 0,
		default= 25000
	)

	sky_model= EnumProperty(
		name= "Sky model",
		description= "Allows you to specify the procedural model that will be used to generate the VRaySky texture",
		items= (
			('CIEOVER',"CIE Overcast",""),
			('CIECLEAR',"CIE Clear",""),
			('PREETH',"Preetham et al","")
		),
		default= 'PREETH'
	)

	ies_light_shape = BoolProperty (
		name        = "Define shape",
		description = "IES light shape; if False the default light shape from IES profile is used",
		default     = False
	)

	ies_light_shape_lock = BoolProperty (
		name        = "Shape controls lock",
		description = "Change width, height and length simultaneously",
		default     = True
	)

	ies_light_width= FloatProperty(
		name        = "Width",
		description = "Light shape width",
		min         = 0,
		max         = 100,
		default     = 0
	)

	ies_light_length= FloatProperty(
		name        = "Length",
		description = "Light shape length",
		min         = 0,
		max         = 100,
		default     = 0
	)

	ies_light_height= FloatProperty(
		name        = "Height",
		description = "Light shape height",
		min         = 0,
		max         = 100,
		default     = 0
	)

	ies_light_diameter= FloatProperty(
		name        = "Diameter",
		description = "Light shape diameter",
		min         = 0,
		max         = 100,
		default     = 0
	)


##      ##  #######  ########  ##       ########  
##  ##  ## ##     ## ##     ## ##       ##     ## 
##  ##  ## ##     ## ##     ## ##       ##     ## 
##  ##  ## ##     ## ########  ##       ##     ## 
##  ##  ## ##     ## ##   ##   ##       ##     ## 
##  ##  ## ##     ## ##    ##  ##       ##     ## 
 ###  ###   #######  ##     ## ######## ########  

class VRayWorld(bpy.types.PropertyGroup):
	bg_color= FloatVectorProperty(
		name= "Background color",
		description= "Background color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	bg_color_mult= FloatProperty(
		name= "Background color multiplier",
		description= "Background color multiplier",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 1.0
	)

	gi_override= BoolProperty(
		name= "Override color for GI",
		description= "Override color for GI",
		default= False
	)

	gi_color= FloatVectorProperty(
		name= "GI color",
		description= "GI (skylight) color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	gi_color_mult= FloatProperty(
		name= "GI color multiplier",
		description= "GI color multiplier",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 1.0
	)

	reflection_override= BoolProperty(
		name= "Override color for reflection",
		description= "Override color for reflection",
		default= False
	)

	reflection_color= FloatVectorProperty(
		name= "Reflection color",
		description= "Reflection (skylight) color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	reflection_color_mult= FloatProperty(
		name= "Reflection color multiplier",
		description= "Reflection color multiplier",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 1.0
	)

	refraction_override= BoolProperty(
		name= "Override color for refraction",
		description= "Override color for refraction",
		default= False
	)

	refraction_color= FloatVectorProperty(
		name= "Refraction color",
		description= "Refraction (skylight) color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.0,0.0,0.0)
	)

	refraction_color_mult= FloatProperty(
		name= "Refraction color multiplier",
		description= "Refraction color multiplier",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 2.0,
		precision= 3,
		default= 1.0
	)

	global_light_level= FloatProperty(
		name= "Global Light Level",
		description= "A global light level multiplier for all lights",
		min= 0.001,
		max= 1000.0,
		soft_min= 0.001,
		soft_max= 2.0,
		precision= 3,
		default= 1.0,
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
	type= EnumProperty(
		name= "Channel Type",
		description= "Render channel type",
		items= (tuple(gen_menu_items(PLUGINS['RENDERCHANNEL']))),
		default= 'NONE'
	)

	use= BoolProperty(
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
	render_channels= CollectionProperty(
		name= "Render Channels",
		type=  VRayRenderChannel,
		description= "V-Ray render channels"
	)

	render_channels_use= BoolProperty(
		name= "Use render channels",
		description= "Use render channels",
		default= False
	)

	render_channels_index= IntProperty(
		name= "Render Channel Index",
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


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

def GetRegClasses():
	return (
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
		VRayCamera,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)

	idref.bpy_register_idref(VRayMaterial, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray material node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayShaderTreeType',
		options = {'FAKE_USER'},
	))

	idref.bpy_register_idref(VRayWorld, 'ntree', idref.IDRefProperty(
		"Node Tree",
		"V-Ray environment node tree",
		idtype = 'NODETREE',
		poll = lambda s, p: p.bl_idname == 'VRayWorldNodeTree',
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

	bpy.types.Texture.vray= PointerProperty(
		name= "V-Ray Texture Settings",
		type=  VRayTexture,
		description= "V-Ray texture settings"
	)

	bpy.types.Scene.vray= PointerProperty(
		name= "V-Ray Settings",
		type=  VRayScene,
		description= "V-Ray Renderer settings"
	)

	bpy.types.Material.vray= PointerProperty(
		name= "V-Ray Material Settings",
		type=  VRayMaterial,
		description= "V-Ray material settings"
	)

	bpy.types.Mesh.vray= PointerProperty(
		name= "V-Ray Mesh Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings"
	)

	bpy.types.Lamp.vray= PointerProperty(
		name= "V-Ray Lamp Settings",
		type=  VRayLight,
		description= "V-Ray lamp settings"
	)

	bpy.types.Curve.vray= PointerProperty(
		name= "V-Ray Curve Settings",
		type=  VRayMesh,
		description= "V-Ray geometry settings"
	)

	bpy.types.Camera.vray= PointerProperty(
		name= "V-Ray Camera Settings",
		type=  VRayCamera,
		description= "V-Ray Camera / DoF / Motion Blur settings"
	)

	bpy.types.Object.vray= PointerProperty(
		name= "V-Ray Object Settings",
		type=  VRayObject,
		description= "V-Ray Object Settings"
	)

	bpy.types.World.vray= PointerProperty(
		name= "V-Ray World Settings",
		type=  VRayWorld,
		description= "V-Ray world settings"
	)

	for pluginType in PLUGINS:
		for plugin in PLUGINS[pluginType]:
			if 'register' in dir(PLUGINS[pluginType][plugin]):
				PLUGINS[pluginType][plugin].register()

	'''
	  Loading plugin properties
	'''
	LoadPlugins(PLUGINS['SETTINGS'],      VRayScene)
	LoadPlugins(PLUGINS['GEOMETRY'],      VRayMesh)
	LoadPlugins(PLUGINS['CAMERA'],        VRayCamera)
	LoadPlugins(PLUGINS['RENDERCHANNEL'], VRayRenderChannel)
	LoadPlugins(PLUGINS['OBJECT'],        VRayObject)

	LoadPlugins(PLUGINS['TEXTURE'],       VRayTexture)
	LoadPlugins(PLUGINS['UVWGEN'],        VRayTexture)

	LoadPlugins(PLUGINS['MATERIAL'],      VRayMaterial)
	LoadPlugins(PLUGINS['BRDF'],          VRayMaterial)

	AddProperties(PLUGINS['SETTINGS']['SettingsEnvironment'], VRayMaterial)
	AddProperties(PLUGINS['SETTINGS']['SettingsEnvironment'], VRayObject)

	AddProperties(PLUGINS['MATERIAL']['MtlOverride'], VRayObject)
	AddProperties(PLUGINS['MATERIAL']['MtlWrapper'], VRayObject)
	AddProperties(PLUGINS['MATERIAL']['MtlRenderStats'], VRayObject)

	AddProperties(PLUGINS['GEOMETRY']['LightMesh'], VRayObject)
	AddProperties(PLUGINS['GEOMETRY']['LightMesh'], VRayMaterial)
	AddProperties(PLUGINS['GEOMETRY']['GeomDisplacedMesh'], VRayObject)
	AddProperties(PLUGINS['GEOMETRY']['GeomStaticSmoothedMesh'], VRayObject)

	# AddProperties(PLUGINS['BRDF']['BRDFBump'], VRaySlot)
	# AddProperties(PLUGINS['GEOMETRY']['GeomDisplacedMesh'], VRaySlot)

	# for key in PLUGINS['BRDF']:
	# 	if key != 'BRDFBump':
	# 		AddProperties(PLUGINS['BRDF'][key], VRayMaterial)


def unregister():
	del bpy.types.Camera.vray
	del bpy.types.Lamp.vray
	del bpy.types.Material.vray
	del bpy.types.Mesh.vray
	del bpy.types.Object.vray
	del bpy.types.Scene.vray
	del bpy.types.Texture.vray
	del bpy.types.World.vray

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

	idref.bpy_unregister_idref(VRayMaterial, 'ntree')
	idref.bpy_unregister_idref(VRayWorld, 'ntree')
	idref.bpy_unregister_idref(VRayObject, 'ntree')
	idref.bpy_unregister_idref(VRayLight, 'ntree')

	for pluginType in PLUGINS:
		for plugin in PLUGINS[pluginType]:
			if 'unregister' in dir(PLUGINS[pluginType][plugin]):
				PLUGINS[pluginType][plugin].unregister()

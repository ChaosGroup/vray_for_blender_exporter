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
	'BRDF':          {},
	'CAMERA':        {},
	'GEOMETRY':      {},
	'MATERIAL':      {},
	'OBJECT':        {},
	'RENDERCHANNEL': {},
	'SETTINGS':      {},
	'SLOT':          {},
	'TEXTURE':       {},
	'WORLD':         {},
}


# Load settings to the RNA Pointer
def load_plugins(plugins, rna_pointer):
	for key in plugins:
		plugins[key].add_properties(rna_pointer)

def gen_material_menu_items(plugins):
	plugs= [plugins[plug] for plug in plugins if hasattr(plugins[plug], 'PID') and hasattr(plugins[plug], 'MAIN_BRDF')]

	# We need to sort plugins by PID so that adding new plugins
	# won't mess enum indexes in existing scenes
	plugs= sorted(plugs, key=lambda plug: plug.PID)
	
	enum_items= []
	for plugin in plugs:
		if hasattr(plugin,'ID'):
			ui_label= plugin.UI if hasattr(plugin,'UI') else plugin.NAME
			enum_items.append((plugin.ID, ui_label, plugin.DESC))

	return enum_items

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

	# print("<Debug information. Remove this from release!>")
	# for item in enum_items:
	# 	print(" ", item)
	
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

	# Move to World plugin
	class VRayWorld(bpy.types.PropertyGroup):
		bg_color= FloatVectorProperty(
			name= "Background color",
			description= "Background color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.0,0.0,0.0)
		)

		bg_color_mult= FloatProperty(
			name= "Background color multiplier",
			description= "Background color multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		gi_override= BoolProperty(
			name= "Override color for GI",
			description= "Override color for GI.",
			default= False
		)

		gi_color= FloatVectorProperty(
			name= "GI color",
			description= "GI (skylight) color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.0,0.0,0.0)
		)

		gi_color_mult= FloatProperty(
			name= "GI color multiplier",
			description= "GI color multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		reflection_override= BoolProperty(
			name= "Override color for reflection",
			description= "Override color for reflection.",
			default= False
		)

		reflection_color= FloatVectorProperty(
			name= "Reflection color",
			description= "Reflection (skylight) color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.0,0.0,0.0)
		)

		reflection_color_mult= FloatProperty(
			name= "Reflection color multiplier",
			description= "Reflection color multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		refraction_override= BoolProperty(
			name= "Override color for refraction",
			description= "Override color for refraction.",
			default= False
		)

		refraction_color= FloatVectorProperty(
			name= "Refraction color",
			description= "Refraction (skylight) color.",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.0,0.0,0.0)
		)

		refraction_color_mult= FloatProperty(
			name= "Refraction color multiplier",
			description= "Refraction color multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		global_light_level= FloatProperty(
			name= "Global light level",
			description= "A global light level multiplier for all lights.",
			min= 0.0,
			max= 1000.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 1.0,
		)

	bpy.utils.register_class(VRayWorld)

	# Move to Slot plugin
	class BRDFLight(bpy.types.PropertyGroup):
		map_color= BoolProperty(
			name= "Color",
			description= "A color texture that if present will override the \"Color\" parameter.",
			default= True
		)

		color_mult= FloatProperty(
			name= "Color texture multiplier",
			description= "Color texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_shadowColor= BoolProperty(
			name= "Shadow",
			description= "A color texture that if present will override the \"Shadow color\" parameter.",
			default= False
		)

		shadowColor_mult= FloatProperty(
			name= "Shadow color texture multiplier",
			description= "Shadow color texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_intensity= BoolProperty(
			name= "Intensity",
			description= "A color texture that if present will override the \"Intensity\" parameter.",
			default= False
		)

		intensity_mult= FloatProperty(
			name= "Intensity texture multiplier",
			description= "Intensity texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)
	bpy.utils.register_class(BRDFLight)

	# Move to Slot plugin
	class VRaySlot(bpy.types.PropertyGroup):
		uvwgen= StringProperty(
			name= "UVW Generator",
			subtype= 'NONE',
			options= {'HIDDEN'},
			description= "UVW generator name.",
			default= "UVWGenChannel_default"
		)

		blend_mode= EnumProperty(
			name= "Blend mode",
			description= "Blend mode.",
			items= (
				('NONE',        "None",       ""),
				('OVER',        "Over",       ""),
				('IN',          "In",         ""),
				('OUT',         "Out",        ""),
				('ADD',         "Add",        ""),
				('SUBTRACT',    "Subtract",   ""),
				('MULTIPLY',    "Multiply",   ""),
				('DIFFERENCE',  "Difference", ""),
				('LIGHTEN',     "Lighten",    ""),
				('DARKEN',      "Darken",     ""),
				('SATURATE',    "Saturate",   ""),
				('DESATUREATE', "Desaturate", ""),
				('ILLUMINATE',  "Illuminate", ""),
			),
			default= 'NONE'
		)

		texture_rotation_h= FloatProperty(
			name= "Horiz. rotation",
			description= "Horizontal rotation.",
			min= -360.0,
			max= 360.0,
			soft_min= -180.0,
			soft_max= 180.0,
			default= 0.0
		)

		texture_rotation_v= FloatProperty(
			name= "Vert. rotation",
			description= "TODO.",
			min= -360.0,
			max= 360.0,
			soft_min= -180.0,
			soft_max= 180.0,
			default= 0.0
		)

		map_displacement= BoolProperty(
			name= "Displacement",
			description= "Displacement texture.",
			default= False
		)

		displacement_mult= FloatProperty(
			name= "Displacement texture multiplier",
			description= "Displacement texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_normal= BoolProperty(
			name= "Normal",
			description= "Normal texture.",
			default= False
		)

		normal_mult= FloatProperty(
			name= "Normal texture multiplier",
			description= "Normal texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_opacity= BoolProperty(
			name= "Opacity",
			description= "Opacity texture.",
			default= False
		)

		opacity_mult= FloatProperty(
			name= "Opacity texture multiplier",
			description= "Opacity texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_roughness= BoolProperty(
			name= "Roughness",
			description= "Roughness texture.",
			default= False
		)

		roughness_mult= FloatProperty(
			name= "Roughness texture multiplier",
			description= "Roughness texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_reflect= BoolProperty(
			name= "Reflection",
			description= "Reflection texture.",
			default= False
		)

		reflect_mult= FloatProperty(
			name= "Reflection texture multiplier",
			description= "Reflection texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_reflect_glossiness= BoolProperty(
			name= "Reflection glossiness",
			description= "Reflection glossiness texture.",
			default= False
		)

		reflect_glossiness_mult= FloatProperty(
			name= "Reflection glossiness texture multiplier",
			description= "Reflection glossiness texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_hilight_glossiness= BoolProperty(
			name= "Hilight glossiness",
			description= "Hilight glossiness texture.",
			default= False
		)

		hilight_glossiness_mult= FloatProperty(
			name= "Hilight glossiness texture multiplier",
			description= "Hilight glossiness texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_anisotropy= BoolProperty(
			name= "Anisotropy",
			description= "Anisotropy texture.",
			default= False
		)

		anisotropy_mult= FloatProperty(
			name= "Anisotropy texture multiplier",
			description= "Anisotropy texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_anisotropy_rotation= BoolProperty(
			name= "Anisotropy rotation",
			description= "Anisotropy rotation texture.",
			default= False
		)

		anisotropy_rotation_mult= FloatProperty(
			name= "Anisotropy rotation texture multiplier",
			description= "Anisotropy rotation texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_fresnel_ior= BoolProperty(
			name= "Fresnel IOR",
			description= "Fresnel IOR texture.",
			default= False
		)

		fresnel_ior_mult= FloatProperty(
			name= "Fresnel IOR texture multiplier",
			description= "Fresnel IOR texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_refract= BoolProperty(
			name= "Refraction",
			description= "Refraction texture.",
			default= False
		)

		refract_mult= FloatProperty(
			name= "Refraction texture multiplier",
			description= "Refraction texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_refract_ior= BoolProperty(
			name= "Refraction IOR",
			description= "Refraction IOR texture.",
			default= False
		)

		refract_ior_mult= FloatProperty(
			name= "Refraction IOR texture multiplier",
			description= "Refraction IOR texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_refract_glossiness= BoolProperty(
			name= "Refraction glossiness",
			description= "Refraction glossiness texture.",
			default= False
		)

		refract_glossiness_mult= FloatProperty(
			name= "Refraction glossiness texture multiplier",
			description= "Refraction glossiness texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_translucency_color= BoolProperty(
			name= "Translucency",
			description= "Translucency texture.",
			default= False
		)

		translucency_color_mult= FloatProperty(
			name= "Translucency texture multiplier",
			description= "Translucency texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)


		'''
		  BRDFSSS2Complex
		'''
		map_overall_color= BoolProperty(
			name= "Overall color",
			description= "Overall color.",
			default= False
		)

		overall_color_mult= FloatProperty(
			name= "Overall color multiplier",
			description= "Overall color multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_diffuse_color= BoolProperty(
			name= "Diffuse color",
			description= "Diffuse color.",
			default= False
		)

		diffuse_color_mult= FloatProperty(
			name= "Diffuse color multiplier",
			description= "Diffuse color multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_diffuse_amount= BoolProperty(
			name= "Diffuse amount",
			description= "Diffuse amount.",
			default= False
		)

		diffuse_amount_mult= FloatProperty(
			name= "Diffuse amount multiplier",
			description= "Diffuse amount multiplie.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_sub_surface_color= BoolProperty(
			name= "Sub-surface color",
			description= "Sub-surface color.",
			default= False
		)

		sub_surface_color_mult= FloatProperty(
			name= "Sub-surface color multiplier",
			description= "Sub-surface color multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_scatter_radius= BoolProperty(
			name= "Scatter radius",
			description= "Scatter radius.",
			default= False
		)

		scatter_radius_mult= FloatProperty(
			name= "Scatter radius multiplier",
			description= "Scatter radius multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_specular_color= BoolProperty(
			name= "Specular color",
			description= "Specular color.",
			default= False
		)

		specular_color_mult= FloatProperty(
			name= "Specular color multiplier",
			description= "Specular color multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_specular_amount= BoolProperty(
			name= "Specular amount",
			description= "Specular amoun.",
			default= False
		)

		specular_amount_mult= FloatProperty(
			name= "Specular amount multiplier.",
			description= "Specular amount multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)

		map_specular_glossiness= BoolProperty(
			name= "Specular glossiness",
			description= "Specular glossiness.",
			default= False
		)

		specular_glossiness_mult= FloatProperty(
			name= "Specular glossiness multiplier.",
			description= "Specular glossiness multiplier.",
			min=0.0,
			max=100.0,
			soft_min=0.0,
			soft_max=1.0,
			default=1.0
		)


		'''
		  EnvironmentFog
		'''
		map_emission_tex= BoolProperty(
			name= "Emission",
			description= "Emission texture.",
			default= False
		)

		emission_tex_mult= FloatProperty(
			name= "Emission texture multiplier",
			description= "Emission texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_color_tex= BoolProperty(
			name= "Color",
			description= "Color texture.",
			default= False
		)

		color_tex_mult= FloatProperty(
			name= "Color texture multiplier",
			description= "Color texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_density_tex= BoolProperty(
			name= "Density",
			description= "Density texture.",
			default= False
		)

		density_tex_mult= FloatProperty(
			name= "Density texture multiplier",
			description= "Density texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		map_fade_out_tex= BoolProperty(
			name= "Fade out",
			description= "Fade out texture.",
			default= False
		)

		fade_out_tex_mult= FloatProperty(
			name= "Fade out texture multiplier",
			description= "Fade out texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= 1.0
		)

		use_map_env_bg= BoolProperty(
			name= "Background",
			description= "Background.",
			default= True
		)

		env_bg_factor= FloatProperty(
			name= "Background texture multiplier",
			description= "Background texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		use_map_env_gi= BoolProperty(
			name= "GI",
			description= "Override for GI.",
			default= False
		)

		env_gi_factor= FloatProperty(
			name= "GI texture multiplier",
			description= "GI texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		use_map_env_reflection= BoolProperty(
			name= "Reflection",
			description= "Override for Reflection.",
			default= False
		)

		env_reflection_factor= FloatProperty(
			name= "Reflection texture multiplier",
			description= "Reflection texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)

		use_map_env_refraction= BoolProperty(
			name= "Refraction",
			description= "Override for Refraction.",
			default= False
		)

		env_refraction_factor= FloatProperty(
			name= "Refraction texture multiplier",
			description= "Refraction texture multiplier.",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 2.0,
			precision= 3,
			default= 1.0
		)
	bpy.utils.register_class(VRaySlot)

	VRaySlot.BRDFLight= PointerProperty(
		name= "BRDFLight",
		type=  BRDFLight,
		description= "VRay lights texture slot settings."
	)

	class VRayTexture(bpy.types.PropertyGroup):
		type= EnumProperty(
			name= "Texture Type",
			description= "V-Ray texture type.",
			items= (tuple(gen_menu_items(PLUGINS['TEXTURE']))),
			default= 'NONE'
		)
	bpy.utils.register_class(VRayTexture)

	class VRayRenderChannel(bpy.types.PropertyGroup):
		type= EnumProperty(
			name= "Channel Type",
			description= "Render channel type.",
			items= (tuple(gen_menu_items(PLUGINS['RENDERCHANNEL']))),
			default= 'NONE'
		)

		use= BoolProperty(
			name= "Use channel",
			description= "Use render channel.",
			default= True
		)
	bpy.utils.register_class(VRayRenderChannel)

	class VRayScene(bpy.types.PropertyGroup):
		render_channels= CollectionProperty(
			name= "Render Channels",
			type=  VRayRenderChannel,
			description= "V-Ray render channels."
		)

		render_channels_use= BoolProperty(
			name= "Use render channels",
			description= "Use render channels.",
			default= False
		)

		render_channels_index= IntProperty(
			name= "Render Channel Index",
			default= -1,
			min= -1,
			max= 100
		)
	bpy.utils.register_class(VRayScene)

	bpy.types.Texture.vray= PointerProperty(
		name= "V-Ray Texture Settings",
		type=  VRayTexture,
		description= "V-Ray texture settings."
	)

	bpy.types.Texture.vray_slot= PointerProperty(
		name= "V-Ray Material Texture Slot",
		type=  VRaySlot,
		description= "V-Ray material texture slot settings."
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

	bpy.types.World.vray= PointerProperty(
		name= "V-Ray World Settings",
		type=  VRayWorld,
		description= "V-Ray world settings."
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
	PLUGINS['GEOMETRY']['LightMesh'].add_properties(VRayMaterial)
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].add_properties(VRayObject)

	PLUGINS['BRDF']['BRDFBump'].add_properties(VRaySlot)
	PLUGINS['GEOMETRY']['GeomDisplacedMesh'].add_properties(VRaySlot)

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

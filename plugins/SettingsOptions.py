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

TYPE= 'SETTINGS'

ID=   'SETTINGSOPTIONS'
NAME= 'Render Options'
PLUG= 'SettingsOptions'
DESC= "Render options."

PARAMS= (
	'geom_displacement',
	'geom_doHidden',
	'geom_backfaceCull',
	'ray_bias',
	'gi_dontRenderImage',
	'light_doLights',
	'light_doDefaultLights',
	'light_doHiddenLights',
	'light_doShadows',
	'light_onlyGI',
	'mtl_reflectionRefraction',
	'mtl_limitDepth',
	'mtl_maxDepth',
	'mtl_doMaps',
	'mtl_filterMaps',
	'mtl_filterMapsForSecondaryRays',
	'mtl_transpMaxLevels',
	'mtl_transpCutoff',
	'mtl_override_on',
	'mtl_override',
	'mtl_glossy',
	'misc_lowThreadPriority',
)


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class SettingsOptions(bpy.types.PropertyGroup):
	pass

bpy.utils.register_class(SettingsOptions)

def add_properties(parent_struct):
	setattr(parent_struct, PLUG, PointerProperty(type= SettingsOptions,
												 name= NAME,
												 description= DESC))
	
	SettingsOptions.geom_displacement= BoolProperty(
		name= "Displacement",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.geom_doHidden= BoolProperty(
		name= "Render hidden",
		description= "TODO.",
		default= False
	)
	
	SettingsOptions.light_doLights= BoolProperty(
		name= "Lights",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.light_doDefaultLights= BoolProperty(
		name= "Default lights",
		description= "TODO.",
		default= False
	)
	
	SettingsOptions.light_doHiddenLights= BoolProperty(
		name= "Hidden lights",
		description= "TODO.",
		default= False
	)
	
	SettingsOptions.light_doShadows= BoolProperty(
		name= "Shadows",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.light_onlyGI= BoolProperty(
		name= "Show GI only",
		description= "TODO.",
		default= False
	)
	
	SettingsOptions.gi_dontRenderImage= BoolProperty(
		name= "Calculate GI only",
		description= "Don't render final image",
		default= False
	)
	
	SettingsOptions.mtl_reflectionRefraction= BoolProperty(
		name= "Reflection/refraction",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.mtl_limitDepth= BoolProperty(
		name= "Limit depth",
		description= "Limit max depth",
		default= False
	)
	
	SettingsOptions.mtl_maxDepth= IntProperty(
		name= "Max depth",
		description= "Max. ray depth for reflections and refractions",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 5
	)
	
	SettingsOptions.mtl_doMaps= BoolProperty(
		name= "Textures",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.mtl_filterMaps= BoolProperty(
		name= "Filter textures",
		description= "TODO.",
		default= True
	)
	
	SettingsOptions.mtl_filterMapsForSecondaryRays= BoolProperty(
		name= "Filter textures for GI",
		description= "False to turn off filtering for glossy and GI rays",
		default= False
	)
	
	SettingsOptions.mtl_transpMaxLevels= IntProperty(
		name= "Max transp. levels",
		description= "Max. transparency levels",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 50
	)
	
	SettingsOptions.mtl_transpCutoff= FloatProperty(
		name= "Transp. cutoff",
		description= "Transparency cutoff",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.001
	)
	
	SettingsOptions.mtl_override_on= BoolProperty(
		name= "Override",
		description= "Override material",
		default= False
	)

	SettingsOptions.mtl_override= StringProperty(
		name= "Override material",
		description= "Override material",
		default= ""
	)
	
	SettingsOptions.mtl_glossy= BoolProperty(
		name= "Glossy effects",
		description= "Glossy effects",
		default= True
	)
	
	SettingsOptions.geom_backfaceCull= BoolProperty(
		name= "Force back face culling",
		description= "If true, back faces will be invisible to camera and shadow rays",
		default= False
	)
	
	SettingsOptions.ray_bias= FloatProperty(
		name= "Secondary rays bias",
		description= "Secondary ray bias",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)
	
	SettingsOptions.misc_lowThreadPriority= BoolProperty(
		name= "Low thread priority",
		description= "TODO.",
		default= True
	)


def write(ofile, sce, rna_pointer):
	VRayScene= sce.vray
	SettingsOptions= VRayScene.SettingsOptions

	ofile.write("\n%s {" % PLUG)
	for param in PARAMS:
		if param == 'mtl_override':
			continue
		else:
			value= getattr(SettingsOptions, param)
		ofile.write("\n\t%s= %s;" % (param, p(value)))
	ofile.write("\n}\n")

	

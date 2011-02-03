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


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'SETTINGS'

ID=   'SettingsOptions'

NAME= 'Render Options'
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


def add_properties(rna_pointer):
	class SettingsOptions(bpy.types.IDPropertyGroup):
		pass
	
	setattr(rna_pointer, PLUG, PointerProperty(type= SettingsOptions,
											   name= NAME,
											   description= DESC))
	
	SettingsOptions.geom_displacement= BoolProperty(
		name= "Displacement",
		description= "No tooltip yet :(",
		default= True
	)
	
	SettingsOptions.geom_doHidden= BoolProperty(
		name= "Render hidden",
		description= "No tooltip yet :(",
		default= False
	)
	
	SettingsOptions.light_doLights= BoolProperty(
		name= "Lights",
		description= "No tooltip yet :(",
		default= True
	)
	
	SettingsOptions.light_doDefaultLights= BoolProperty(
		name= "Default lights",
		description= "No tooltip yet :(",
		default= False
	)
	
	SettingsOptions.light_doHiddenLights= BoolProperty(
		name= "Hidden lights",
		description= "No tooltip yet :(",
		default= False
	)
	
	SettingsOptions.light_doShadows= BoolProperty(
		name= "Shadows",
		description= "No tooltip yet :(",
		default= True
	)
	
	SettingsOptions.light_onlyGI= BoolProperty(
		name= "Show GI only",
		description= "No tooltip yet :(",
		default= False
	)
	
	SettingsOptions.gi_dontRenderImage= BoolProperty(
		name= "Calculate GI only",
		description= "Don't render final image",
		default= False
	)
	
	SettingsOptions.mtl_reflectionRefraction= BoolProperty(
		name= "Reflection/refraction",
		description= "No tooltip yet :(",
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
		description= "No tooltip yet :(",
		default= True
	)
	
	SettingsOptions.mtl_filterMaps= BoolProperty(
		name= "Filter textures",
		description= "No tooltip yet :(",
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
		description= "No tooltip yet :(",
		default= True
	)


def write(ofile, scene, rna_pointer):
	VRayScene=       scene.vray
	SettingsOptions= VRayScene.SettingsOptions

	ofile.write("\n%s %s {" % (PLUG, PLUG))
	for param in PARAMS:
		if param == 'mtl_override':
			# Not implemented in V-Ray plugin:
			# override is done in "Node" export function
			continue
		else:
			value= getattr(SettingsOptions, param)
		ofile.write("\n\t%s= %s;" % (param, p(value)))
	ofile.write("\n}\n")

	

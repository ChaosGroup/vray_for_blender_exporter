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
from vb25.utils   import *
from vb25.shaders import *
from vb25.ui.ui   import *


TYPE= 'SETTINGS'
ID=   'SettingsEnvironment'

NAME= 'Environment Effects'
DESC= "Environment effects."

PARAMS= {
	'EnvironmentFog' : (
		'gizmos',
		'emission',
		'emission_tex',
		'emission_mult',
		'emission_mult_tex',
		'color',
		'color_tex',
		'distance',
		'density',
		'density_tex',
		'use_height',
		'height',
		'subdivs',
		'yup',
		'fade_out_mode',
		'fade_out_radius',
		'per_object_fade_out_radius',
		'use_fade_out_tex',
		'fade_out_tex',
		'edge_fade_out',
		'fade_out_type',
		'scatter_gi',
		'scatter_bounces',
		'simplify_gi',
		'step_size',
		'max_steps',
		'tex_samples',
		'cutoff_threshold',
		'light_mode',
		'lights',
		'use_shade_instance',
		'affect_background',
		'affect_reflections',
		'affect_refractions',
		'affect_shadows',
		'affect_gi',
		'affect_camera',
	),

	'VolumeVRayToon': (
	),
}


def add_properties(rna_pointer):
	class VolumeVRayToon(bpy.types.IDPropertyGroup):
		pass

	class EnvironmentFog(bpy.types.IDPropertyGroup):
		pass

	class EnvironmentEffect(bpy.types.IDPropertyGroup):
		pass

	class VRayEffects(bpy.types.IDPropertyGroup):
		pass

	rna_pointer.EnvironmentFog= PointerProperty(
		name= "EnvironmentFog",
		type=  EnvironmentFog,
		description= "EnvironmentFog settings."
	)

	rna_pointer.VolumeVRayToon= PointerProperty(
		name= "VolumeVRayToon",
		type=  VolumeVRayToon,
		description= "VolumeVRayToon settings."
	)

	rna_pointer.VRayEffects= PointerProperty(
		name= "Environment Effects",
		type=  VRayEffects,
		description= "V-Ray environment effects settings."
	)

	VRayEffects.effects= CollectionProperty(
		name= "Environment Effect",
		type=  EnvironmentEffect,
		description= "V-Ray environment effect."
	)

	VRayEffects.use= BoolProperty(
		name= "Use effects",
		description= "Use effects.",
		default= False
	)

	VRayEffects.effects_selected= IntProperty(
		name= "Selected Environment Effect",
		description= "Selected environment effect.",
		default= -1,
		min= -1,
		max= 100
	)

	EnvironmentEffect.type= EnumProperty(
		name= "Type",
		description= "Distributed rendering network type.",
		items= (
			('TOON', "Toon", "Object outline (toon style)."),
			('FOG',  "Fog",  "Environment / object fog.")
		),
		default= 'FOG'
	)

	EnvironmentEffect.use= BoolProperty(
		name= "Use effect",
		description= "Use effect.",
		default= True
	)

	EnvironmentEffect.EnvironmentFog= PointerProperty(
		name= "EnvironmentFog",
		type=  EnvironmentFog,
		description= "V-Ray EnvironmentFog settings."
	)

	EnvironmentEffect.VolumeVRayToon= PointerProperty(
		name= "VolumeVRayToon",
		type=  VolumeVRayToon,
		description= "V-Ray VolumeVRayToon settings."
	)

	EnvironmentFog.emission= FloatVectorProperty(
		name= "Emission",
		description= "Fog emission color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	EnvironmentFog.color= FloatVectorProperty(
		name= "Color",
		description= "Fog color",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1.0,1.0,1.0)
	)

	EnvironmentFog.distance= FloatProperty(
		name= "Distance",
		description= "Distance between fog particles",
		min= 0.0,
		max= 10000.0,
		soft_min= 0.0,
		soft_max= 100.0,
		precision= 3,
		default= 0.2
	)
	
	EnvironmentFog.density= FloatProperty(
		name= "Density",
		description= "A multiplier for the Fog distance parameter that allows a texture to be used for the density of the fog.",
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 1
	)

	EnvironmentFog.use_height= BoolProperty(
		name= "Use height",
		description= "Whether or not the height should be taken into account.",
		default= False
	)

	EnvironmentFog.height= FloatProperty(
		name= "Height",
		description= "Fog starting point along the Z-axis.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 100
	)
	
	EnvironmentFog.subdivs= IntProperty(
		name= "Subdivs",
		description= "Fog subdivision",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	EnvironmentFog.affect_background= BoolProperty(
		name= "Affect background",
		description= "Affect background",
		default= True
	)

	EnvironmentFog.yup= BoolProperty(
		name= "Y-up",
		description= "If true, y is the up axis, not z.",
		default= False
	)

	EnvironmentFog.fade_out_mode= EnumProperty(
		name= "Fade out mode",
		description= "Fade out mode.",
		items= (
			('SUBSTRACT',"Substract",""),
			('MULT',"Multiply","")
		),
		default= 'MULT'
	)
	
	EnvironmentFog.fade_out_radius= FloatProperty(
		name= "Fade out radius",
		description= "Fade out effect for the edges",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	EnvironmentFog.per_object_fade_out_radius= BoolProperty(
		name= "Per object fade out radius",
		description= "Fade out effect for the edges per object",
		default= False
	)

	EnvironmentFog.use_fade_out_tex= BoolProperty(
		name= "Use fade out tex",
		description= "True if the fade_out_tex should be used for fade out computation.",
		default= False
	)

	EnvironmentFog.edge_fade_out= FloatProperty(
		name= "Edge fade out",
		description= "Used with the fade_out_tex, mimics Maya fluid's edge dropoff attribute",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	EnvironmentFog.fade_out_type= IntProperty(
		name= "Fade out type",
		description= "0 - used for the gradients and the grid falloff(fadeout);1 - used for the sphere, cone and double cone types;2 - used for the cube type, the computations are done in the TexMayaFluidProcedural plug-in;",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)
	
	EnvironmentFog.scatter_gi= BoolProperty(
		name= "Scatter GI",
		description= "Scatter global illumination",
		default= True
	)
	
	EnvironmentFog.scatter_bounces= IntProperty(
		name= "Scatter bounces",
		description= "Number of GI bounces calculated inside the fog",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 8
	)

	EnvironmentFog.simplify_gi= BoolProperty(
		name= "Simplify GI",
		description= "Simplify global illumination",
		default= False
	)

	EnvironmentFog.step_size= FloatProperty(
		name= "Step size",
		description= "Size of one step through the volume",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	EnvironmentFog.max_steps= IntProperty(
		name= "Max steps",
		description= "Maximum number of steps through the volume",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 1000
	)

	EnvironmentFog.tex_samples= IntProperty(
		name= "Texture samples",
		description= "Number of texture samples for each step through the volume",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 4
	)

	EnvironmentFog.cutoff_threshold= FloatProperty(
		name= "Cutoff",
		description= "Controls when the raymarcher will stop traversing the volume.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.001
	)

	EnvironmentFog.light_mode= EnumProperty(
		name= "Light mode",
		description= "Light mode.",
		items= (
			('ADDGIZMO',"Add to per-gizmo lights",""),
			('INTERGIZMO',"Intersect with per-gizmo lights",""),
			('OVERGIZMO',"Override per-gizmo lights",""),
			('PERGIZMO',"Use per-gizmo lights",""),
			('NO',"No lights","")
		),
		default= 'PERGIZMO'
	)

	EnvironmentFog.use_shade_instance= BoolProperty(
		name= "Use shade instance",
		description= "True if the shade instance should be used when sampling textures.",
		default= False
	)

	EnvironmentFog.objects= StringProperty(
		name= "Objects",
		description= "TODO: Tooltip",
		default= ""
	)

	EnvironmentFog.groups= StringProperty(
		name= "Groups",
		description= "TODO: Tooltip",
		default= ""
	)

	VolumeVRayToon.use= BoolProperty(
		name= "Use",
		description= "Render outline.",
		default= False
	)

	# lineColor
	VolumeVRayToon.lineColor= FloatVectorProperty(
		name= "Color",
		description= "The color of cartoon line.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	# widthType
	VolumeVRayToon.widthType= EnumProperty(
		name= "Type",
		description= "TODO: Tooltip.",
		items= (
			('WORLD', "World",  "World units."),
			('PIXEL', "Pixels", "Pixels.")
		),
		default= 'PIXEL'
	)

	# lineWidth
	VolumeVRayToon.lineWidth= FloatProperty(
		name= "Width",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.5
	)

	# opacity
	VolumeVRayToon.opacity= FloatProperty(
		name= "Opacity",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# hideInnerEdges
	VolumeVRayToon.hideInnerEdges= BoolProperty(
		name= "Hide inner edges",
		description= "TODO: Tooltip.",
		default= True
	)

	# normalThreshold
	VolumeVRayToon.normalThreshold= FloatProperty(
		name= "Normal thresh",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.7
	)

	# overlapThreshold
	VolumeVRayToon.overlapThreshold= FloatProperty(
		name= "Overlap thresh",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.95
	)

	# traceBias
	VolumeVRayToon.traceBias= FloatProperty(
		name= "Bias",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0.2
	)

	# doSecondaryRays
	VolumeVRayToon.doSecondaryRays= BoolProperty(
		name= "Do reflections / refractons",
		description= "TODO: Tooltip.",
		default= False
	)

	# excludeType
	VolumeVRayToon.excludeType= EnumProperty(
		name= "Include / exclude",
		description= "TODO: Tooltip.",
		items= (
			('INCLUDE', "Include", "Include objects."),
			('EXCLUDE', "Exclude", "Exclude objects.")
		),
		default= 'EXCLUDE'
	)

	# excludeList
	VolumeVRayToon.excludeList_objects= StringProperty(
		name= "excludeList",
		description= "TODO: Tooltip",
		default= ""
	)

	VolumeVRayToon.excludeList_groups= StringProperty(
		name= "excludeList",
		description= "TODO: Tooltip",
		default= ""
	)

	# lineColor_tex
	VolumeVRayToon.map_lineColor_tex= BoolProperty(
		name= "lineColor tex",
		description= "TODO: Tooltip",
		default= False
	)

	VolumeVRayToon.lineColor_tex_mult= FloatProperty(
		name= "lineColor tex",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# lineWidth_tex
	VolumeVRayToon.map_lineWidth_tex= BoolProperty(
		name= "lineWidth tex",
		description= "TODO: Tooltip",
		default= False
	)

	VolumeVRayToon.lineWidth_tex_mult= FloatProperty(
		name= "lineWidth tex",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# opacity_tex
	VolumeVRayToon.map_opacity_tex= BoolProperty(
		name= "opacity tex",
		description= "TODO: Tooltip",
		default= False
	)

	VolumeVRayToon.opacity_tex_mult= FloatProperty(
		name= "opacity tex",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)

	# distortion_tex
	VolumeVRayToon.map_distortion_tex= BoolProperty(
		name= "distortion tex",
		description= "TODO: Tooltip",
		default= False
	)

	VolumeVRayToon.distortion_tex_mult= FloatProperty(
		name= "distortion tex",
		description= "TODO: Tooltip.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.0
	)



'''
  Write plugins settings to file
'''
def write(params):
	ofile= params['files']['environment']
	scene= params['scene']

	def write_EnvFogMeshGizmo(ofile, node_name, node_geometry, node_matrix):
		plugin= 'EnvFogMeshGizmo'
		name= "%s_%s" % (plugin,node_name)

		ofile.write("\n%s %s {"%(plugin,name))
		ofile.write("\n\ttransform= %s;" % a(scene,transform(node_matrix)))
		ofile.write("\n\tgeometry= %s;" % node_geometry)
		#ofile.write("\n\tlights= List(%s);" % )
		#ofile.write("\n\tfade_out_radius= %s;" % )
		ofile.write("\n}\n")

		return name

	def write_EnvironmentFog(ofile,volume,material):
		LIGHT_MODE= {
			'ADDGIZMO':    4,
			'INTERGIZMO':  3,
			'OVERGIZMO':   2,
			'PERGIZMO':    1,
			'NO':          0
		}

		plugin= 'EnvironmentFog'
		name= "%s_%s" % (plugin,material)

		ofile.write("\n%s %s {"%(plugin,name))
		ofile.write("\n\tgizmos= List(%s);" % ','.join(volume[material]['gizmos']))
		for param in volume[material]['params']:
			if param == 'light_mode':
				value= LIGHT_MODE[volume[material]['params'][param]]
			elif param in ('density_tex','fade_out_tex','emission_mult_tex'):
				value= "%s::out_intensity" % volume[material]['params'][param]
			else:
				value= volume[material]['params'][param]
			ofile.write("\n\t%s= %s;"%(param, a(scene,value)))
		ofile.write("\n}\n")

		return name

	# TODO:
	#volumes= [write_EnvironmentFog(files['nodes'],types['volume'],vol) for vol in types['volume']]
	volumes= []

	world=     scene.world
	VRayWorld= world.vray

	bg_tex=      None
	gi_tex=      None
	reflect_tex= None
	refract_tex= None

	bg_tex_mult=      1.0
	gi_tex_mult=      1.0
	reflect_tex_mult= 1.0
	refract_tex_mult= 1.0

	for slot in world.texture_slots:
		if slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot= slot.texture.vray_slot

			params= {'slot': slot,
					 'texture': slot.texture,
					 'environment': True,
					 'rotate': {'angle': VRaySlot.texture_rotation_h,
								'axis': 'Z'},
					 'transform': ({'rotate': {'angle': VRaySlot.texture_rotation_h, 'axis': 'Z'}},
								   {'rotate': {'angle': VRaySlot.texture_rotation_v, 'axis': 'Y'}}),
			}

			if slot.use_map_blend:
				bg_tex= write_texture(ofile, scene, params)
				bg_tex_mult= slot.blend_factor
			if slot.use_map_horizon:
				gi_tex= write_texture(ofile, scene, params)
				gi_tex_mult= slot.horizon_factor
			if slot.use_map_zenith_up:
				reflect_tex= write_texture(ofile, scene, params)
				reflect_tex_mult= slot.zenith_up_factor
			if slot.use_map_zenith_down:
				refract_tex=  write_texture(ofile, scene, params)
				refract_tex_mult= slot.zenith_down_factor

	ofile.write("\nSettingsEnvironment {")

	ofile.write("\n\tbg_color= %s;"%(a(scene,VRayWorld.bg_color)))
	if bg_tex:
		ofile.write("\n\tbg_tex= %s;"%(bg_tex))
		ofile.write("\n\tbg_tex_mult= %s;"%(a(scene,bg_tex_mult)))

	if VRayWorld.gi_override:
		ofile.write("\n\tgi_color= %s;"%(a(scene,VRayWorld.gi_color)))
	if gi_tex:
		ofile.write("\n\tgi_tex= %s;"%(gi_tex))
		ofile.write("\n\tgi_tex_mult= %s;"%(a(scene,gi_tex_mult)))

	if VRayWorld.reflection_override:
		ofile.write("\n\treflect_color= %s;"%(a(scene,VRayWorld.reflection_color)))
	if reflect_tex:
		ofile.write("\n\treflect_tex= %s;"%(reflect_tex))
		ofile.write("\n\treflect_tex_mult= %s;"%(a(scene,reflect_tex_mult)))

	if VRayWorld.refraction_override:
		ofile.write("\n\trefract_color= %s;"%(a(scene,VRayWorld.refraction_color)))
	if refract_tex:
		ofile.write("\n\trefract_tex= %s;"%(refract_tex))
		ofile.write("\n\trefract_tex_mult= %s;"%(a(scene,refract_tex_mult)))

	if volumes:
		ofile.write("\n\tenvironment_volume= List(%s);"%(','.join(volumes)))

	ofile.write("\n}\n")



'''
  Main GUI function
'''
def draw_EnvironmentFog(context, layout, rna_pointer):
	wide_ui= context.region.width > narrowui

	EnvironmentFog= rna_pointer.EnvironmentFog

	split= layout.split()
	col= split.column()
	col.prop(EnvironmentFog, 'color')
	if wide_ui:
		col= split.column()
	col.prop(EnvironmentFog, 'emission')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(EnvironmentFog, 'distance')
	col.prop(EnvironmentFog, 'density')
	col.prop(EnvironmentFog, 'subdivs')
	col.prop(EnvironmentFog, 'scatter_gi')
	if EnvironmentFog.scatter_gi:
		col.prop(EnvironmentFog, 'scatter_bounces')
	col.prop(EnvironmentFog, 'use_height')
	if EnvironmentFog.use_height:
		col.prop(EnvironmentFog, 'height')
	if wide_ui:
		col= split.column()
	#col.prop(EnvironmentFog, 'fade_out_type')
	col.prop(EnvironmentFog, 'fade_out_radius')
	col.prop(EnvironmentFog, 'affect_background')
	col.prop(EnvironmentFog, 'use_shade_instance')
	col.prop(EnvironmentFog, 'simplify_gi')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(EnvironmentFog, 'light_mode')
	col.prop(EnvironmentFog, 'fade_out_mode')

	layout.separator()

	split= layout.split()
	col= split.column()
	col.prop(EnvironmentFog, 'step_size')
	col.prop(EnvironmentFog, 'max_steps')
	if wide_ui:
		col= split.column()
	col.prop(EnvironmentFog, 'tex_samples')
	col.prop(EnvironmentFog, 'cutoff_threshold')

	#col.prop(EnvironmentFog, 'per_object_fade_out_radius')
	#col.prop(EnvironmentFog, 'yup')

	layout.separator()
	
	split= layout.split()
	col= split.column()
	col.prop_search(EnvironmentFog, 'objects',
					context.scene, 'objects', text="Objects")
	col.prop_search(EnvironmentFog, 'groups',
					bpy.data, 'groups', text="Groups")


def draw_VolumeVRayToon(context, layout, rna_pointer):
	wide_ui= context.region.width > narrowui

	VolumeVRayToon= rna_pointer.VolumeVRayToon

	split= layout.split()
	col= split.column()
	col.prop(VolumeVRayToon, 'lineColor', text="")
	col.prop(VolumeVRayToon, 'widthType')
	col.prop(VolumeVRayToon, 'lineWidth')
	col.prop(VolumeVRayToon, 'opacity')
	if wide_ui:
		col= split.column()
	col.prop(VolumeVRayToon, 'normalThreshold')
	col.prop(VolumeVRayToon, 'overlapThreshold')
	col.prop(VolumeVRayToon, 'hideInnerEdges')
	col.prop(VolumeVRayToon, 'doSecondaryRays')
	col.prop(VolumeVRayToon, 'traceBias')

	# col.prop(VolumeVRayToon, 'lineColor_tex')
	# col.prop(VolumeVRayToon, 'lineWidth_tex')
	# col.prop(VolumeVRayToon, 'opacity_tex')
	# col.prop(VolumeVRayToon, 'distortion_tex')

	if not str(type(rna_pointer)) == '<class \'vb25.plugins.VRayMaterial\'>': # Ugly =)
		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VolumeVRayToon, 'excludeType', text="")
		col.prop_search(VolumeVRayToon, 'excludeList_objects',
						context.scene, 'objects', text="Objects")
		col.prop_search(VolumeVRayToon, 'excludeList_groups',
						bpy.data, 'groups', text="Groups")
	

def gui(context, layout, VRayEffects):
	wide_ui= context.region.width > narrowui

	split= layout.split()
	row= split.row()
	row.template_list(VRayEffects, 'effects',
					  VRayEffects, 'effects_selected',
					  rows= 3)
	col= row.column(align=True)
	col.operator('vray.effect_add',	   text="", icon="ZOOMIN")
	col.operator('vray.effect_remove', text="", icon="ZOOMOUT")

	if VRayEffects.effects_selected >= 0:
		layout.separator()

		effect= VRayEffects.effects[VRayEffects.effects_selected]

		split= layout.split()
		col= split.column()
		col.prop(effect, 'name')
		col.prop(effect, 'type')

		layout.separator()

		if effect.type == 'FOG':
			draw_EnvironmentFog(context, layout, effect)

		elif effect.type == 'TOON':
			draw_VolumeVRayToon(context, layout, rna_pointer)

		else:
			split= layout.split()
			col= split.column()
			col.label(text="Strange, but this effect type doesn\'t exist...")

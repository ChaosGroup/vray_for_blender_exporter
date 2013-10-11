'''

  V-Ray/Blender

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
from vb25.ui   import classes
from vb25.plugins import *
from vb25.utils   import *

from vb25 import nodes


TYPE= 'SETTINGS'
ID=   'SettingsEnvironment'

NAME= 'Environment Effects'
DESC= "Environment effects"

PARAMS= {
	'SettingsEnvironment': (
		'num_environment_objects', # integer = 0, Used for implementing image planes
	),

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
		'lineColor',
		'widthType',
		'lineWidth',
		'opacity',
		'hideInnerEdges',
		'normalThreshold',
		'overlapThreshold',
		'traceBias',
		'doSecondaryRays',
		'excludeType',
		'excludeList',
		# 'lineColor_tex',
		# 'lineWidth_tex',
		# 'opacity_tex',
		# 'distortion_tex',
	),

	'SphereFade': (
		#'gizmos',
		'empty_color',
		'affect_alpha',
		'falloff'
	),
}


def add_properties(rna_pointer):
	class SphereFade(bpy.types.PropertyGroup):
		use = BoolProperty(
			name        = "",
			description = "",
			default     = False
		)

		affect_alpha = BoolProperty(
			name        = "Affect Alpha",
			description = "Affect Alpha",
			default     = False
		)

		empty_color= FloatVectorProperty(
			name= "Empty Color",
			description= "",
			subtype= 'COLOR',
			min= 0.0,
			max= 1.0,
			soft_min= 0.0,
			soft_max= 1.0,
			default= (0.5,0.5,0.5)
		)

		falloff= FloatProperty(
			name= "Falloff",
			description= "",
			min= 0.0,
			max= 100.0,
			soft_min= 0.0,
			soft_max= 10.0,
			precision= 3,
			default= 0.2
		)

		gizmos_objects= StringProperty(
			name= "Gizmo",
			description= "",
			default= ""
		)

		gizmos_groups= StringProperty(
			name= "Gizmo group",
			description= "",
			default= ""
		)
	bpy.utils.register_class(SphereFade)

	class EnvironmentEffect(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(EnvironmentEffect)

	class VRayEffects(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(VRayEffects)

	rna_pointer.SphereFade= PointerProperty(
		name= "SphereFade",
		type=  SphereFade,
		description= "SphereFade settings"
	)

	rna_pointer.VRayEffects= PointerProperty(
		name= "Environment Effects",
		type=  VRayEffects,
		description= "V-Ray environment effects settings"
	)

	VRayEffects.effects= CollectionProperty(
		name= "Environment Effect",
		type=  EnvironmentEffect,
		description= "V-Ray environment effect"
	)

	VRayEffects.use= BoolProperty(
		name= "Use effects",
		description= "Use effects",
		default= False
	)

	VRayEffects.effects_selected= IntProperty(
		name= "Selected Environment Effect",
		description= "Selected environment effect",
		default= -1,
		min= -1,
		max= 100
	)

	EnvironmentEffect.type= EnumProperty(
		name= "Type",
		description= "Distributed rendering network type",
		items= (
			('TOON', "Toon", "Object outline (toon style)"),
			('FOG',  "Fog",  "Environment / object fog"),
			('SFADE',  "SphereFade",  "Sphere Fade")
		),
		default= 'FOG'
	)

	EnvironmentEffect.use= BoolProperty(
		name= "",
		description= "Use effect",
		default= True
	)

	EnvironmentEffect.SphereFade= PointerProperty(
		name= "SphereFade",
		type=  SphereFade,
		description= "SphereFade settings"
	)



'''
  Write plugins settings to file
'''
def write_VolumeVRayToon_from_material(bus):
	WIDTHTYPE= {
		'PIXEL': 0,
		'WORLD': 1,
	}

	ofile= bus['files']['environment']
	scene= bus['scene']

	ob= bus['node']['object']
	ma= bus['material']['material']

	VRayMaterial= ma.vray

	VolumeVRayToon= VRayMaterial.VolumeVRayToon

	toon_name= clean_string("MT%s%s" % (ob.name, ma.name))

	ofile.write("\nVolumeVRayToon %s {" % toon_name)
	ofile.write("\n\tcompensateExposure= 1;")
	for param in PARAMS['VolumeVRayToon']:
		if param == 'excludeType':
			value= 1
		elif param == 'excludeList':
			value= "List(%s)" % get_name(ob, prefix='OB')
		elif param == 'widthType':
			value= WIDTHTYPE[VolumeVRayToon.widthType]
		else:
			value= getattr(VolumeVRayToon, param)
		ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return toon_name

def write(bus):
	ofile= bus['files']['environment']
	scene= bus['scene']

	VRayScene= scene.vray
	VRayExporter= VRayScene.exporter

	def write_EnvFogMeshGizmo(bus, ob):
		name= "MG%s" % get_name(ob, prefix='OB')

		ofile.write("\nEnvFogMeshGizmo %s {" % name)
		ofile.write("\n\tgeometry= %s;" % get_name(ob.data if VRayExporter.use_instances else ob, prefix='ME'))
		ofile.write("\n\ttransform= %s;" % a(scene, transform(ob.matrix_world)))
		#ofile.write("\n\tlights= List(%s);" % )
		#ofile.write("\n\tfade_out_radius= %s;" % )
		ofile.write("\n}\n")

		return name

	def write_SphereFadeGizmo(bus, ob):
		vray = ob.vray
		name= "MG%s" % get_name(ob, prefix='EMPTY')
		ofile.write("\nSphereFadeGizmo %s {" % name)
		ofile.write("\n\ttransform= %s;" % a(scene, transform(ob.matrix_world)))
		if ob.type == 'EMPTY':
			ofile.write("\n\tradius=%s;" % ob.empty_draw_size)
		elif vray.MtlRenderStats.use:
			ofile.write("\n\tradius=%s;" % vray.fade_radius)
		ofile.write("\n\tinvert=0;")
		ofile.write("\n}\n")
		return name

	def write_SphereFade(bus, effect, gizmos):
		scene= bus['scene']
		name= "ESF%s" % clean_string(effect.name)

		ofile.write("\nSphereFade %s {" % name)
		print(gizmos)
		ofile.write("\n\tgizmos= List(%s);" % ','.join(gizmos))
		for param in PARAMS['SphereFade']:
			value= getattr(effect.SphereFade, param)
			ofile.write("\n\t%s= %s;"%(param, a(scene,value)))

		ofile.write("\n}\n")

	def write_EnvironmentFog_from_material(ofile,volume,material):
		LIGHT_MODE = {
			'ADDGIZMO':    4,
			'INTERGIZMO':  3,
			'OVERGIZMO':   2,
			'PERGIZMO':    1,
			'NO':          0
		}

		plugin = 'EnvironmentFog'
		name   = "%s_%s" % (plugin, material)

		ofile.write("\n%s %s {" % (plugin, name))
		ofile.write("\n\tgizmos=List(%s);" % ','.join(volume[material]['gizmos']))
		for param in volume[material]['params']:
			if param == 'light_mode':
				value = LIGHT_MODE[volume[material]['params'][param]]
			elif param in ('density_tex','fade_out_tex','emission_mult_tex'):
				value = "%s::out_intensity" % volume[material]['params'][param]
			else:
				value = volume[material]['params'][param]
			ofile.write("\n\t%s=%s;" % (param, a(scene,value)))
		ofile.write("\n}\n")

		return name

	def write_EnvironmentFog(bus, effect, gizmos):
		LIGHT_MODE= {
			'ADDGIZMO':    4,
			'INTERGIZMO':  3,
			'OVERGIZMO':   2,
			'PERGIZMO':    1,
			'NO':          0
		}
		FADE_OUT_MODE= {
			'MULT':      0,
			'SUBSTRACT': 1,
		}

		EnvironmentFog= effect.EnvironmentFog

		density_tex_voxel = False

		density_tex  = None
		emission_tex = None
		color_tex    = None

		if EnvironmentFog.density_tex:
			if EnvironmentFog.density_tex in bpy.data.textures:
				density_tex = write_subtexture(bus, EnvironmentFog.density_tex)

		if EnvironmentFog.emission_tex:
			if EnvironmentFog.emission_tex in bpy.data.textures:
				emission_tex = write_subtexture(bus, EnvironmentFog.emission_tex)

		if not emission_tex or not density_tex:
			if EnvironmentFog.objects:
				ob = get_data_by_name(scene, 'objects', EnvironmentFog.objects)
				if ob and len(ob.modifiers):
					for md in ob.modifiers:
						if md.type == 'SMOKE' and md.smoke_type == 'DOMAIN':
							density_tex_voxel = True
							density_tex  = clean_string("OB%sSMD%s" % (ob.name, md.name))
							emission_tex = density_tex
							color_tex    = density_tex

		if emission_tex:
			emission_tex_mult_name = "%sMult" % emission_tex
			ofile.write("\nTexAColorOp %s {" % emission_tex_mult_name)
			ofile.write("\n\tcolor_a=%s::out_color;" % emission_tex)
			ofile.write("\n\tmult_a=%.3f;" % EnvironmentFog.emission_mult)
			ofile.write("\n}\n")
			emission_tex = emission_tex_mult_name

		name= "EEF%s" % clean_string(effect.name)

		ofile.write("\nEnvironmentFog %s {" % name)
		for param in PARAMS['EnvironmentFog']:
			value = None

			if param.endswith('_tex') or param.endswith('_mult'):
				if param == 'density_tex' and density_tex:
					value = density_tex + "::out_density"
				elif param == 'emission_tex' and emission_tex:
					value = emission_tex
				elif param == 'color_tex' and color_tex:
					value = color_tex + "::out_color"
				# elif param == 'emission_mult_tex':
				# 	value = density_tex + "::out_flame"					
				else:
					continue
			elif param == 'emission':
				value = "%s * %.3f" % (p(EnvironmentFog.emission), EnvironmentFog.emission_mult)
			elif param == 'fade_out_mode':
				value= FADE_OUT_MODE[EnvironmentFog.fade_out_mode]
			elif param == 'light_mode':
				value= LIGHT_MODE[EnvironmentFog.light_mode]
			elif param == 'gizmos':
				value= "List(%s)" % ','.join(gizmos)
			elif param == 'lights':
				light_object_list= [get_name(ob, prefix='LA') for ob in generate_object_list(EnvironmentFog.lights) if object_visible(bus,ob)]
				if not len(light_object_list):
					continue
				value= "List(%s)" % ','.join(light_object_list)
			else:
				value= getattr(EnvironmentFog, param)

			if value is not None:
				ofile.write("\n\t%s=%s;"%(param, a(scene, value)))
		ofile.write("\n}\n")

		return name

	def write_VolumeVRayToon(bus, effect, objects):
		EXCLUDETYPE= {
			'EXCLUDE': 0,
			'INCLUDE': 1,
		}
		WIDTHTYPE= {
			'PIXEL': 0,
			'WORLD': 1,
		}

		VolumeVRayToon= effect.VolumeVRayToon

		name= "EVT%s" % clean_string(effect.name)

		ofile.write("\nVolumeVRayToon %s {" % name)
		ofile.write("\n\tcompensateExposure= 1;")
		for param in PARAMS['VolumeVRayToon']:
			if param == 'excludeType':
				value= EXCLUDETYPE[VolumeVRayToon.excludeType]
			elif param == 'widthType':
				value= WIDTHTYPE[VolumeVRayToon.widthType]
			elif param == 'excludeList':
				value= "List(%s)" % ','.join(objects)
			else:
				value= getattr(VolumeVRayToon, param)
			ofile.write("\n\t%s= %s;"%(param, a(scene, value)))
		ofile.write("\n}\n")

		return name

	VRayScene=   scene.vray
	VRayEffects= VRayScene.VRayEffects

	# Processing Effects
	volumes= []
	if VRayEffects.use:
		for effect in VRayEffects.effects:
			if effect.use:
				if effect.type == 'FOG':
					EnvironmentFog= effect.EnvironmentFog
					gizmos= [write_EnvFogMeshGizmo(bus, ob) for ob in generate_object_list(EnvironmentFog.objects, EnvironmentFog.groups) if object_visible(bus,ob)]
					# if gizmos:
					# 	volumes.append(write_EnvironmentFog(bus, effect, gizmos))
					volumes.append(write_EnvironmentFog(bus, effect, gizmos))

				elif effect.type == 'TOON':
					VolumeVRayToon= effect.VolumeVRayToon

					excludeList= generate_object_list(VolumeVRayToon.excludeList_objects, VolumeVRayToon.excludeList_groups)
					toon_objects= [get_name(ob, prefix='OB') for ob in excludeList]

					if not VolumeVRayToon.override_material:
						if VolumeVRayToon.excludeType == 'EXCLUDE':
							toon_objects.extend( [ get_name(ob, prefix='OB') for ob in bus['effects']['toon']['objects'] ] )

					volumes.append(write_VolumeVRayToon(bus, effect, toon_objects))

				elif effect.type == 'SFADE':
					SphereFade= effect.SphereFade
					gizmos= [write_SphereFadeGizmo(bus, ob) for ob in generate_object_list(gizmos_objects, gizmos_groups) if object_visible(bus,ob)]
					write_SphereFade(bus, effect, gizmos)

	volumes.reverse()
	volumes.extend(bus['effects']['toon']['effects'])

	VRayWorld = scene.world.vray

	socketParams = {}
	outputNode = None

	if VRayWorld.ntree:
		outputNode = nodes.export.GetNodeByType(VRayWorld.ntree, 'VRayNodeWorldOutput')

		for nodeSocket in outputNode.inputs:
			vrayAttr = nodeSocket.vray_attr
			socketParams[vrayAttr] = nodes.export.WriteConnectedNode(bus, VRayWorld.ntree, nodeSocket)

	ofile.write("\nSettingsEnvironment settingsEnvironment {")
	ofile.write("\n\tglobal_light_level=%s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayWorld.global_light_level))
	ofile.write("\n\tenvironment_volume=List(%s);" % (','.join(volumes)))
	ofile.write("\n\tbg_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\tbg_tex_mult=1.0;")
	ofile.write("\n\tgi_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\tgi_tex_mult=1.0;")
	ofile.write("\n\treflect_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\treflect_tex_mult=1.0;")
	ofile.write("\n\trefract_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\trefract_tex_mult=1.0;")

	ofile.write("\n\tbg_tex=%s;" % a(scene, socketParams.get('bg_tex', "Color(0.0,0.0,0.0)")))

	for override in ('gi_tex', 'reflect_tex', 'refract_tex'):
		value = None

		if override in socketParams and getattr(outputNode, override):
			value = socketParams[override]
		else:
			value = socketParams.get('bg_tex', None)

		if value:
			ofile.write("\n\t%s=%s;" % (override, a(scene, value)))

	ofile.write("\n}\n")


def draw_VolumeVRayToon(context, layout, rna_pointer):
	wide_ui= context.region.width > classes.narrowui

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

	if not str(type(rna_pointer)) == "<class 'vb25.plugins.VRayMaterial'>": # Very ugly :(
		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VolumeVRayToon, 'override_material')

		split= layout.split()
		col= split.column()
		col.prop(VolumeVRayToon, 'excludeType', text="")
		col.prop_search(VolumeVRayToon, 'excludeList_objects',
						context.scene,  'objects',
						text="Objects")
		col.prop_search(VolumeVRayToon, 'excludeList_groups',
						bpy.data,       'groups',
						text="Groups")


def draw_SphereFade(context, layout, rna_pointer):
	wide_ui= context.region.width > classes.narrowui

	SphereFade= rna_pointer.SphereFade

	split= layout.split()
	col= split.column()
	col.prop(SphereFade, 'empty_color')
	col.prop(SphereFade, 'affect_alpha')
	col.prop(SphereFade, 'falloff')

	#col= split.column()
	col.prop_search(SphereFade, 'gizmos_objects',
					context.scene,  'objects',
					text="Objects")
	col.prop_search(SphereFade, 'gizmos_groups',
					bpy.data,       'groups',
					text="Groups")


def gui(context, layout, VRayEffects):
	wide_ui= context.region.width > classes.narrowui

	split= layout.split()
	row= split.row()
	row.template_list("VRayListUse", "",
					  VRayEffects, 'effects',
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
			col.label(text="Strange, but this effect type doesn\'t exist..")

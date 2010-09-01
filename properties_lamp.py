'''

 V-Ray/Blender

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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


import os
import bpy

from vb25.utils import *

# class MyTest(bpy.types.IDPropertyGroup):
#     pass
# bpy.types.Lamp.PointerProperty(
# 	attr= 'mytest',
# 	type=  MyTest,
# 	name= "MyTest Settings",
# 	description= "MyTest settings"
# )

class VRayLamp(bpy.types.IDPropertyGroup):
    pass

bpy.types.Lamp.PointerProperty(
	attr= 'vray',
	type=  VRayLamp,
	name= "V-Ray Lamp Settings",
	description= "V-Ray lamp settings"
)

VRayLamp.BoolProperty(
	attr="enabled",
	name="Enabled",
	description="Turns the light on and off",
	default= True
)

VRayLamp.EnumProperty(
	attr= 'units',
	name= "Intensity units",
	description= "Units for the intensity.",
	items=(
		('DEFUALT',  "Default",   ""),
		('LUMENS',   "Lumens",    ""),
		('LUMM',     "Lm/m/m/sr", ""),
		('WATTSM',   "Watts",     ""),
		('WATM',     "W/m/m/sr",  "")
	),
	default= 'DEFAULT'
)

VRayLamp.FloatProperty(
	attr= 'beamRadius',
	name= "Beam radius",
	description= "Beam radius, 0.0 if the light has no beam radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 3,
	default= 0.0
)

VRayLamp.EnumProperty(
	attr= 'direct_type',
	name= "Direct type",
	description= "Direct light type.",
	items=(
		('DIRECT',  "Direct",  ""),
		('SUN',     "Sun",     "")
	),
	default= 'DIRECT'
)


VRayLamp.EnumProperty(
	attr="spot_type",
	name="Spot type",
	description="Spot light subtype.",
	items=(
		('SPOT',  "Spot",  ""),
		('IES',   "IES",   "")
	),
	default= 'DIRECT'
)

VRayLamp.BoolProperty(
	attr= "shadows",
	name= "Shadows",
	description= "TODO.",
	default= True
)

VRayLamp.BoolProperty(
	attr= "affectDiffuse",
	name= "Affect diffuse",
	description= "Produces diffuse lighting.",
	default= True
)

VRayLamp.BoolProperty(
	attr= "affectSpecular",
	name= "Affect specular",
	description= "Produces specular hilights.",
	default= True
)

VRayLamp.BoolProperty(
	attr= "affectReflections",
	name= "Affect reflections",
	description= "Appear in reflections.",
	default= False
)

VRayLamp.FloatVectorProperty(
	attr= "shadowColor",
	name= "Shadow color",
	description= "The shadow color. Anything but black is not physically accurate.",
	subtype= "COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayLamp.FloatProperty(
	attr= "shadowBias",
	name= "Shadow bias",
	description= "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

VRayLamp.IntProperty(
	attr= "shadowSubdivs",
	name= "Shadow subdivs",
	description= "TODO.",
	min= 0,
	max= 256,
	default= 8
)

VRayLamp.FloatProperty(
	attr= "shadowRadius",
	name= "Shadow radius",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

VRayLamp.FloatProperty(
	attr= "decay",
	name= "Decay",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 2
)

VRayLamp.FloatProperty(
	attr= "cutoffThreshold",
	name= "Cut-off threshold",
	description= "Light cut-off threshold (speed optimization). If the light intensity for a point is below this threshold, the light will not be computed..",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 0.1,
	precision= 3,
	default= 0.001
)

VRayLamp.FloatProperty(
	attr= "intensity",
	name= "Intensity",
	description= "Light intensity.",
	min= 0.0,
	max= 10000000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 2,
	default= 30
)

VRayLamp.IntProperty(
	attr= "subdivs",
	name= "Subdivs",
	description= "TODO.",
	min= 0,
	max= 256,
	default= 8
)

VRayLamp.BoolProperty(
	attr= "storeWithIrradianceMap",
	name= "Store with irradiance map",
	description= "TODO.",
	default= False
)

VRayLamp.BoolProperty(
	attr= "invisible",
	name= "Invisible",
	description= "TODO.",
	default= False
)

VRayLamp.BoolProperty(
	attr= "noDecay",
	name= "No decay",
	description= "TODO.",
	default= False
)

VRayLamp.BoolProperty(
	attr= "doubleSided",
	name= "Double-sided",
	description= "TODO.",
	default= False
)

VRayLamp.EnumProperty(
	attr="lightPortal",
	name="Light portal mode",
	description="Specifies if the light is a portal light.",
	items=(
		('NORMAL',  "Normal light",   ""),
		('PORTAL',  "Portal",         ""),
		('SPORTAL', "Simple portal",  "")
	),
	default= 'NORMAL'
)

VRayLamp.FloatProperty(
	attr= "radius",
	name= "Radius",
	description= "Sphere light radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

VRayLamp.IntProperty(
	attr= "sphere_segments",
	name= "Sphere segments",
	description= "TODO.",
	min= 0,
	max= 100,
	default= 20
)

VRayLamp.BoolProperty(
	attr= "bumped_below_surface_check",
	name= "Bumped below surface check",
	description= "If the bumped normal should be used to check if the light dir is below the surface.",
	default= False
)

VRayLamp.IntProperty(
	attr= "nsamples",
	name= "Motion blur samples",
	description= "Motion blur samples.",
	min= 0,
	max= 10,
	default= 0
)

VRayLamp.FloatProperty(
	attr= "diffuse_contribution",
	name= "Diffuse contribution",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.FloatProperty(
	attr= "specular_contribution",
	name= "Specular contribution",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.BoolProperty(
	attr= "areaSpeculars",
	name= "Area speculars",
	description= "TODO.",
	default= False
)

VRayLamp.BoolProperty(
	attr= "ignoreLightNormals",
	name= "Ignore light normals",
	description= "TODO.",
	default= True
)

VRayLamp.BoolProperty(
	attr= "use_rect_tex",
	name= "Use rect tex",
	description= "TODO.",
	default= False
)

VRayLamp.IntProperty(
	attr= "tex_resolution",
	name= "Tex resolution",
	description= "TODO.",
	min= 0,
	max= 10,
	default= 512
)

VRayLamp.FloatProperty(
	attr= "tex_adaptive",
	name= "Tex adaptive",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.IntProperty(
	attr= "causticSubdivs",
	name= "Caustic subdivs",
	description= "Caustic subdivs.",
	min= 1,
	max= 100000,
	default= 1000
)

VRayLamp.FloatProperty(
	attr= "causticMult",
	name= "Causticmult",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.StringProperty(
	attr= 'ies_file',
	name= "IES file",
	subtype= 'FILE_PATH',
	description= "IES file."
)

VRayLamp.BoolProperty(
	attr= 'soft_shadows',
	name= "Soft shadows",
	description= "Use the shape of the light as described in the IES profile.",
	default= True
)

VRayLamp.FloatProperty(
	attr= 'turbidity',
	name= 'Turbidity',
	description= "TODO.",
	min= 2.0,
	max= 100.0,
	soft_min= 2.0,
	soft_max= 6.0,
	precision= 3,
	default= 3.0
)

VRayLamp.FloatProperty(
	attr= 'intensity_multiplier',
	name= 'Intensity multiplier',
	description= "TODO.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 2,
	default= 1.0
)

VRayLamp.FloatProperty(
	attr= 'ozone',
	name= 'Ozone',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.35
)

VRayLamp.FloatProperty(
	attr= 'water_vapour',
	name= 'Water vapour',
	description= "TODO.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 3,
	default= 2
)

VRayLamp.FloatProperty(
	attr= 'size_multiplier',
	name= 'Size',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.BoolProperty(
	attr= 'invisible',
	name= 'Invisible',
	description= "TODO.",
	default= False
)

VRayLamp.FloatProperty(
	attr= 'horiz_illum',
	name= 'Horiz illumination',
	description= "TODO.",
	min= 0.0,
	max= 100000.0,
	soft_min= 0.0,
	soft_max= 100000.0,
	precision= 0,
	default= 25000
)

VRayLamp.EnumProperty(
	attr= 'sky_model',
	name= 'Sky model',
	description= "Sky model.",
	items=(
		('CIEOVER',  "CIE Overcast",       ""),
		('CIECLEAR', "CIE Clear",          ""),
		('PREETH',   "Preetham et al.",    "")
	),
	default= 'PREETH'
)



'''
	GUI
'''
narrowui= 200


def base_poll(cls, context):
	rd= context.scene.render
	return (context.lamp) and (rd.engine in cls.COMPAT_ENGINES)


class DataButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'


class DATA_PT_context_lamp(DataButtonsPanel, bpy.types.Panel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		space= context.space_data
		wide_ui= context.region.width > narrowui

		if wide_ui:
			split= layout.split(percentage=0.65)
			if ob:
				split.template_ID(ob, 'data')
				split.separator()
			elif lamp:
				split.template_ID(space, 'pin_id')
				split.separator()
		else:
			if ob:
				layout.template_ID(ob, 'data')
			elif lamp:
				layout.template_ID(space, 'pin_id')

		if wide_ui:
			layout.prop(lamp, 'type', expand=True)
		else:
			layout.prop(lamp, 'type')


class DATA_PT_vray_light(DataButtonsPanel, bpy.types.Panel):
	bl_label       = "Lamp"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		split= layout.split()
		col= split.column()
		col.prop(vl,'enabled', text="On")

		if(lamp.type == 'AREA'):
			pass
		elif(lamp.type == 'POINT'):
			pass
		elif(lamp.type == 'SUN'):
			pass
		elif(lamp.type == 'SPOT'):
			pass
		elif(lamp.type == 'HEMI'):
			pass
		else:
			pass

		split= layout.split()
		col= split.column()
		col.prop(lamp,'color', text="")
		if lamp.type == 'AREA':
			col.prop(vl,'lightPortal', text="Mode")
		col.prop(vl,'units', text="Units")
		if not ((lamp.type == 'SUN' and vl.direct_type == 'SUN') or (lamp.type == 'AREA' and vl.lightPortal != 'NORMAL')):
			col.prop(vl,'intensity', text="Intensity")
		col.prop(vl,'subdivs')
		col.prop(vl,'causticSubdivs', text="Caustics")
		
		if wide_ui:
			col= split.column()
		col.prop(vl,'invisible')
		col.prop(vl,'affectDiffuse')
		col.prop(vl,'affectSpecular')
		col.prop(vl,'affectReflections')
		col.prop(vl,'noDecay')

		if(lamp.type == 'AREA'):
			col.prop(vl,'doubleSided')

		if((lamp.type == 'AREA') or (lamp.type == 'POINT' and vl.radius > 0)):
			col.prop(vl,'storeWithIrradianceMap')


class DATA_PT_vray_light_shape(DataButtonsPanel, bpy.types.Panel):
	bl_label       = "Shape"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		lamp= context.lamp
		return (lamp and lamp.type not in ('HEMI')) and base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		if(lamp.type == 'AREA'):
			layout.prop(lamp,'shape', expand=True)
		elif(lamp.type == 'SUN'):
			layout.prop(vl,'direct_type', expand=True)
		elif(lamp.type == 'SPOT'):
			layout.prop(vl,'spot_type', expand=True)

		split= layout.split()
		col= split.column()
		if lamp.type == 'AREA':
			if lamp.shape == 'SQUARE':
				col.prop(lamp,'size')
			else:
				col.prop(lamp,'size', text="Size X")
				col.prop(lamp,'size_y')

		elif lamp.type == 'POINT':
			col.prop(vl,'radius')
			if vl.radius > 0:
				col.prop(vl,'sphere_segments')

		elif lamp.type == 'SUN':
			if vl.direct_type == 'DIRECT':
				col.prop(vl,'beamRadius')
			else:
				split= layout.split()
				col= split.column()
				col.prop(vl,'sky_model')
				
				split= layout.split()
				col= split.column()
				col.prop(vl,'turbidity')
				col.prop(vl,'ozone')
				col.prop(vl,'intensity_multiplier', text= "Intensity")
				col.prop(vl,'size_multiplier', text= "Size")
				if wide_ui:
					col= split.column()
				col.prop(vl,'invisible')
				col.prop(vl,'horiz_illum')
				col.prop(vl,'water_vapour')

		elif lamp.type == 'SPOT':
			if vl.spot_type == 'SPOT':
				col.prop(lamp,'distance')
				if wide_ui:
					col= split.column()
				col.prop(lamp,'spot_size', text="Size")
			else:
				col.prop(vl,'ies_file', text="File")
				col.prop(vl,'soft_shadows')

		elif(lamp.type == 'HEMI'):
			pass

		else:
			pass


class DATA_PT_vray_light_shadows(DataButtonsPanel, bpy.types.Panel):
	bl_label   = "Shadows"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		vl= context.lamp.vray
		self.layout.prop(vl,'shadows', text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		layout.active = vl.shadows

		split= layout.split()
		col= split.column()
		col.prop(vl,'shadowColor', text="")
		if wide_ui:
			col= split.column()
		col.prop(vl,'shadowBias', text="Bias")
		if(lamp.type in ('SPOT','POINT','SUN')):
			col.prop(vl,'shadowRadius', text="Radius")

		split= layout.split()
		col= split.column()
		if(lamp.type == 'AREA'):
			pass
		elif(lamp.type == 'POINT'):
			pass
		elif(lamp.type == 'SUN'):
			pass
		elif(lamp.type == 'SPOT'):
			pass
		elif(lamp.type == 'HEMI'):
			pass
		else:
			pass


class DATA_PT_vray_light_advanced(DataButtonsPanel, bpy.types.Panel):
	bl_label   = "Advanced"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		split= layout.split()
		col= split.column()
		col.prop(vl,'diffuse_contribution', text="Diffuse cont.")
		col.prop(vl,'specular_contribution', text="Specular cont.")
		col.prop(vl,'cutoffThreshold', text="Cut-off")
		
		if wide_ui:
			col= split.column()
		col.prop(vl,'nsamples')
		col.prop(vl,'bumped_below_surface_check', text="Bumped surface check")
		col.prop(vl,'ignoreLightNormals')
		col.prop(vl,'areaSpeculars')
		
		if(lamp.type == 'AREA'):
			pass
		elif(lamp.type == 'POINT'):
			pass
		elif(lamp.type == 'SUN'):
			pass
		elif(lamp.type == 'SPOT'):
			pass
		elif(lamp.type == 'HEMI'):
			pass
		else:
			pass


# bpy.types.register(DATA_PT_context_lamp)
# bpy.types.register(DATA_PT_vray_light)
# bpy.types.register(DATA_PT_vray_light_shape)
# bpy.types.register(DATA_PT_vray_light_shadows)
# bpy.types.register(DATA_PT_vray_light_advanced)


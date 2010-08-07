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

import bpy


FloatProperty= bpy.types.Lamp.FloatProperty
IntProperty= bpy.types.Lamp.IntProperty
BoolProperty= bpy.types.Lamp.BoolProperty
VectorProperty= bpy.types.Lamp.FloatVectorProperty
EnumProperty= bpy.types.Lamp.EnumProperty
StringProperty= bpy.types.Lamp.StringProperty


EnumProperty(
	attr="vr_la_units",
	name="Intensity units",
	description="Units for the intensity.",
	items=(
		('DEFUALT',  "Default",   ""),
		('LUMENS',   "Lumens",    ""),
		('LUMM',     "Lm/m/m/sr", ""),
		('WATTSM',   "Watts",     ""),
		('WATM',     "W/m/m/sr", "")
	),
	default= 'DEFAULT'
)

EnumProperty(
	attr="vr_la_direct_type",
	name="Direct light subtype",
	description="Direct light subtype.",
	items=(
		('DIRECT',  "Direct",  ""),
		('SUN',     "Sun",     "")
	),
	default= 'DIRECT'
)

EnumProperty(
	attr="vr_la_spot_type",
	name="Spot light subtype",
	description="Spot light subtype.",
	items=(
		('SPOT',  "Spot",  ""),
		('IES',   "IES",   "")
	),
	default= 'DIRECT'
)

BoolProperty(
	attr="vr_la_enabled",
	name="Enabled",
	description="Turns the light on and off",
	default= True
)

BoolProperty(
	attr= "vr_la_shadows",
	name= "Shadows",
	description= "TODO.",
	default= True
)

BoolProperty(
	attr= "vr_la_affectDiffuse",
	name= "Affect diffuse",
	description= "Produces diffuse lighting.",
	default= True
)

BoolProperty(
	attr= "vr_la_affectSpecular",
	name= "Affect specular",
	description= "Produces specular hilights.",
	default= True
)

BoolProperty(
	attr= "vr_la_affectReflections",
	name= "Affect reflections",
	description= "Appear in reflections.",
	default= False
)

VectorProperty(
	attr= "vr_la_shadowColor",
	name= "Shadow color",
	description= "The shadow color. Anything but black is not physically accurate.",
	subtype= "COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

FloatProperty(
	attr= "vr_la_shadowBias",
	name= "Shadow bias",
	description= "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

IntProperty(
	attr= "vr_la_shadowSubdivs",
	name= "Shadow subdivs",
	description= "TODO.",
	min= 0,
	max= 256,
	default= 8
)

FloatProperty(
	attr= "vr_la_shadowRadius",
	name= "Shadow radius",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

FloatProperty(
	attr= "vr_la_decay",
	name= "Decay",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 2
)

FloatProperty(
	attr= "vr_la_cutoffThreshold",
	name= "Cut-off threshold",
	description= "Light cut-off threshold (speed optimization). If the light intensity for a point is below this threshold, the light will not be computed..",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 0.1,
	precision= 3,
	default= 0.001
)

FloatProperty(
	attr= "vr_la_intensity",
	name= "Intensity",
	description= "Light intensity.",
	min= 0.0,
	max= 10000000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 2,
	default= 30
)

IntProperty(
	attr= "vr_la_subdivs",
	name= "Subdivs",
	description= "TODO.",
	min= 0,
	max= 256,
	default= 8
)

BoolProperty(
	attr= "vr_la_storeWithIrradianceMap",
	name= "Store with irradiance map",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vr_la_invisible",
	name= "Invisible",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vr_la_noDecay",
	name= "No decay",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vr_la_doubleSided",
	name= "Double-sided",
	description= "TODO.",
	default= False
)

EnumProperty(
	attr="vr_la_portal_mode",
	name="Light portal mode",
	description="Specifies if the light is a portal light.",
	items=(
		('NORMAL',  "Normal light",   ""),
		('PORTAL',  "Portal",         ""),
		('SPORTAL', "Simple portal",  "")
	),
	default= 'NORMAL'
)

FloatProperty(
	attr= "vr_la_radius",
	name= "Radius",
	description= "Sphere light radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

FloatProperty(
	attr= "vr_la_beamRadius",
	name= "Beam radius",
	description= "Direct light beam radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 3,
	default= 1.0
)

IntProperty(
	attr= "vr_la_sphere_segments",
	name= "Sphere segments",
	description= "TODO.",
	min= 0,
	max= 100,
	default= 20
)

BoolProperty(
	attr= "vr_la_bumped_below_surface_check",
	name= "Bumped below surface check",
	description= "If the bumped normal should be used to check if the light dir is below the surface.",
	default= False
)

IntProperty(
	attr= "vr_la_nsamples",
	name= "Motion blur samples",
	description= "Motion blur samples.",
	min= 0,
	max= 10,
	default= 0
)

FloatProperty(
	attr= "vr_la_diffuse_contribution",
	name= "Diffuse contribution",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

FloatProperty(
	attr= "vr_la_specular_contribution",
	name= "Specular contribution",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

BoolProperty(
	attr= "vr_la_areaSpeculars",
	name= "Area speculars",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vr_la_ignoreLightNormals",
	name= "Ignore light normals",
	description= "TODO.",
	default= True
)

BoolProperty(
	attr= "vr_la_use_rect_tex",
	name= "Use rect tex",
	description= "TODO.",
	default= False
)

IntProperty(
	attr= "vr_la_tex_resolution",
	name= "Tex resolution",
	description= "TODO.",
	min= 0,
	max= 10,
	default= 512
)

FloatProperty(
	attr= "vr_la_tex_adaptive",
	name= "Tex adaptive",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

IntProperty(
	attr= "vr_la_causticSubdivs",
	name= "Causticsubdivs",
	description= "TODO.",
	min= 1,
	max= 10000,
	default= 1000
)

FloatProperty(
	attr= "vr_la_causticMult",
	name= "Causticmult",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)



'''
  Plugin: LightIES
'''
StringProperty(
	attr="vr_la_ies_file",
	name="IES file",
	subtype= 'FILE_PATH',
	description="IES file."
)

# FloatProperty(
# 	attr= "vr_la_power",
# 	name= "IES power",
# 	description= "Limuous power (in lm); if zero, the default lumious power from the IES profile is used.",
# 	min= 0.0,
# 	max= 1.0,
# 	soft_min= 0.0,
# 	soft_max= 1.0,
# 	precision= 3,
# 	default= 1
# )

BoolProperty(
	attr= "vr_la_soft_shadows",
	name= "Soft shadows",
	description= "Use the shape of the light as described in the IES profile.",
	default= True
)



'''
  Plugin: SunLight
'''
# turbidity: float
FloatProperty(
	attr= 'vr_la_turbidity',
	name= 'Turbidity',
	description= "TODO.",
	min= 2.0,
	max= 100.0,
	soft_min= 2.0,
	soft_max= 6.0,
	precision= 3,
	default= 3.0
)

# intensity_multiplier: float
FloatProperty(
	attr= 'vr_la_intensity_multiplier',
	name= 'Intensity multiplier',
	description= "TODO.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 2,
	default= 1.0
)

# ozone: float
FloatProperty(
	attr= 'vr_la_ozone',
	name= 'Ozone',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.35
)

# water_vapour: float
FloatProperty(
	attr= 'vr_la_water_vapour',
	name= 'Water vapour',
	description= "TODO.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 3,
	default= 2
)

# size_multiplier: float
FloatProperty(
	attr= 'vr_la_size_multiplier',
	name= 'Size',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# up_vector: vector = Color(0, 0, 0)
# invisible: bool
BoolProperty(
	attr= 'vr_la_invisible',
	name= 'Invisible',
	description= "TODO.",
	default= False
)

# horiz_illum: float
FloatProperty(
	attr= 'vr_la_horiz_illum',
	name= 'Horiz illumination',
	description= "TODO.",
	min= 0.0,
	max= 100000.0,
	soft_min= 0.0,
	soft_max= 100000.0,
	precision= 0,
	default= 25000
)

# sky_model: integer
EnumProperty(
	attr= 'vr_la_sky_model',
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
	bl_show_header = False

	COMPAT_ENGINES= {'VRAY_RENDER'}

	@staticmethod
	def poll(context):
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
	bl_show_header = True

	COMPAT_ENGINES= {'VRAY_RENDER'}

	@staticmethod
	def poll(context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		wide_ui= context.region.width > narrowui

		split= layout.split()
		col= split.column()
		col.prop(lamp, 'vr_la_enabled', text="On")

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
		col.prop(lamp, 'color', text="")
		if(lamp.type == 'AREA'):
			col.prop(lamp, 'vr_la_portal_mode', text="Mode")
		col.prop(lamp, 'vr_la_units', text="Units")

		if not ((lamp.type == 'SUN' and lamp.vr_la_direct_type == 'SUN') or (lamp.type == 'AREA' and lamp.vr_la_portal_mode != 'NORMAL')):
			col.prop(lamp, 'vr_la_intensity', text="Intensity")
		col.prop(lamp, 'vr_la_subdivs')

		if wide_ui:
			col= split.column()
		col.prop(lamp, 'vr_la_invisible')
		col.prop(lamp, 'vr_la_affectDiffuse')
		col.prop(lamp, 'vr_la_affectSpecular')
		col.prop(lamp, 'vr_la_affectReflections')
		col.prop(lamp, 'vr_la_noDecay')

		if(lamp.type == 'AREA'):
			col.prop(lamp, 'vr_la_doubleSided')

		if((lamp.type == 'AREA') or (lamp.type == 'POINT' and lamp.vr_la_radius > 0)):
			col.prop(lamp, 'vr_la_storeWithIrradianceMap')


class DATA_PT_vray_light_shape(DataButtonsPanel, bpy.types.Panel):
	bl_label       = "Shape"
	bl_show_header = True

	COMPAT_ENGINES= {'VRAY_RENDER'}

	@staticmethod
	def poll(context):
		lamp= context.lamp
		return (lamp and lamp.type not in ('HEMI')) and base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		wide_ui= context.region.width > narrowui

		if(lamp.type == 'AREA'):
			layout.prop(lamp, 'shape', expand=True)
		elif(lamp.type == 'SUN'):
			layout.prop(lamp, 'vr_la_direct_type', expand=True)
		elif(lamp.type == 'SPOT'):
			layout.prop(lamp, 'vr_la_spot_type', expand=True)

		split= layout.split()
		col= split.column()
		if(lamp.type == 'AREA'):
			if(lamp.shape == 'SQUARE'):
				col.prop(lamp, 'size')
			else:
				col.prop(lamp, 'size', text="Size X")
				col.prop(lamp, 'size_y')

		elif(lamp.type == 'POINT'):
			col.prop(lamp, 'vr_la_radius')
			if(lamp.vr_la_radius > 0):
				col.prop(lamp, 'vr_la_sphere_segments')

		elif(lamp.type == 'SUN'):
			if(lamp.vr_la_direct_type == 'DIRECT'):
				col.prop(lamp, 'vr_la_beamRadius')
			else:
				split= layout.split()
				col= split.column()
				col.prop(lamp, 'vr_la_sky_model')
				
				split= layout.split()
				col= split.column()
				col.prop(lamp, 'vr_la_turbidity')
				col.prop(lamp, 'vr_la_ozone')
				col.prop(lamp, 'vr_la_intensity_multiplier', text= "Intensity")
				col.prop(lamp, 'vr_la_size_multiplier', text= "Size")
				if(wide_ui):
					col= split.column()
				col.prop(lamp, 'vr_la_invisible')
				col.prop(lamp, 'vr_la_horiz_illum')
				col.prop(lamp, 'vr_la_water_vapour')

		elif(lamp.type == 'SPOT'):
			if(lamp.vr_la_spot_type == 'SPOT'):
				col.prop(lamp, 'distance')
				if wide_ui:
					col= split.column()
				col.prop(lamp, 'spot_size', text="Size")
			else:
				col.prop(lamp, 'vr_la_ies_file', text="File")
				col.prop(lamp, 'vr_la_soft_shadows')

		elif(lamp.type == 'HEMI'):
			pass

		else:
			pass


class DATA_PT_vray_light_shadows(DataButtonsPanel, bpy.types.Panel):
	bl_label          = "Shadows"
	bl_show_header    = True
	bl_default_closed = True

	COMPAT_ENGINES= {'VRAY_RENDER'}

	@staticmethod
	def poll(context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		lamp= context.lamp
		self.layout.prop(lamp, 'vr_la_shadows', text="")

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		wide_ui= context.region.width > narrowui

		layout.active = lamp.vr_la_shadows

		split= layout.split()
		col= split.column()
		col.prop(lamp, 'vr_la_shadowColor', text="")
		if wide_ui:
			col= split.column()
		col.prop(lamp, 'vr_la_shadowBias', text="Bias")
		if(lamp.type in ('SPOT','POINT','SUN')):
			col.prop(lamp, 'vr_la_shadowRadius', text="Radius")

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
	bl_label          = "Advanced"
	bl_show_header    = True
	bl_default_closed = True

	COMPAT_ENGINES= {'VRAY_RENDER'}

	@staticmethod
	def poll(context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		wide_ui= context.region.width > narrowui

		split= layout.split()
		col= split.column()
		col.prop(lamp, 'vr_la_diffuse_contribution', text="Diffuse cont.")
		col.prop(lamp, 'vr_la_specular_contribution', text="Specular cont.")
		col.prop(lamp, 'vr_la_cutoffThreshold', text="Cut-off")
		
		if wide_ui:
			col= split.column()
		col.prop(lamp, 'vr_la_nsamples')
		col.prop(lamp, 'vr_la_bumped_below_surface_check', text="Bumped surface check")
		col.prop(lamp, 'vr_la_ignoreLightNormals')
		col.prop(lamp, 'vr_la_areaSpeculars')
		
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


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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


import bpy


FloatProperty= bpy.types.Mesh.FloatProperty
IntProperty= bpy.types.Mesh.IntProperty
BoolProperty= bpy.types.Mesh.BoolProperty
EnumProperty= bpy.types.Mesh.EnumProperty
VectorProperty= bpy.types.Mesh.FloatVectorProperty
StringProperty= bpy.types.Mesh.StringProperty


'''
  Plugin: LightMesh
'''
BoolProperty(
	attr= "vray_node_meshlight",
	name= "Mesh-light",
	description= "Mesh is mesh-light.",
	options={'HIDDEN'},
	default= False
)

EnumProperty(
	attr="vray_lamp_units",
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

BoolProperty(
	attr="vray_lamp_enabled",
	name="Enabled",
	description="Turns the light on and off",
	default= True
)

BoolProperty(
	attr= "vray_lamp_shadows",
	name= "Shadows",
	description= "TODO.",
	default= True
)

BoolProperty(
	attr= "vray_lamp_affectDiffuse",
	name= "Affect diffuse",
	description= "Produces diffuse lighting.",
	default= True
)

BoolProperty(
	attr= "vray_lamp_affectSpecular",
	name= "Affect specular",
	description= "Produces specular hilights.",
	default= True
)

BoolProperty(
	attr= "vray_lamp_affectReflections",
	name= "Affect reflections",
	description= "Appear in reflections.",
	default= False
)

VectorProperty(
	attr= "vray_lamp_shadowColor",
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
	attr= "vray_lamp_shadowBias",
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
	attr= "vray_lamp_shadowSubdivs",
	name= "Shadow subdivs",
	description= "TODO.",
	min= 0,
	max= 10,
	default= 8
)

FloatProperty(
	attr= "vray_lamp_shadowRadius",
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
	attr= "vray_lamp_decay",
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
	attr= "vray_lamp_cutoffThreshold",
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
	attr= "vray_lamp_intensity",
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
	attr= "vray_lamp_subdivs",
	name= "Subdivs",
	description= "TODO.",
	min= 0,
	max= 10,
	default= 8
)

BoolProperty(
	attr= "vray_lamp_storeWithIrradianceMap",
	name= "Store with irradiance map",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vray_lamp_invisible",
	name= "Invisible",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vray_lamp_noDecay",
	name= "No decay",
	description= "TODO.",
	default= False
)

BoolProperty(
	attr= "vray_lamp_doubleSided",
	name= "Double-sided",
	description= "TODO.",
	default= False
)

EnumProperty(
	attr="vray_lamp_portal_mode",
	name="Light portal mode",
	description="Specifies if the light is a portal light.",
	items=(
		('NORMAL',  "Normal light",   ""),
		('PORTAL',  "Portal",         ""),
		('SPORTAL', "Simple portal",  "")
	),
	default= 'NORMAL'
)

BoolProperty(
	attr= "vray_lamp_bumped_below_surface_check",
	name= "Bumped below surface check",
	description= "If the bumped normal should be used to check if the light dir is below the surface.",
	default= False
)

IntProperty(
	attr= "vray_lamp_nsamples",
	name= "Motion blur samples",
	description= "Motion blur samples.",
	min= 0,
	max= 10,
	default= 0
)

FloatProperty(
	attr= "vray_lamp_diffuse_contribution",
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
	attr= "vray_lamp_specular_contribution",
	name= "Specular contribution",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

IntProperty(
	attr= "vray_lamp_causticSubdivs",
	name= "Causticsubdivs",
	description= "TODO.",
	min= 0,
	max= 10,
	default= 1000
)

FloatProperty(
	attr= "vray_lamp_causticMult",
	name= "Causticmult",
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)


# shadowColor: color (The shadow color. Anything but black is not physically accurate.) = Color(0, 0, 0)
# shadowColor_tex: acolor texture (A color texture that if present will override the shadowColor parameter)
# channels: plugin (Render channels the result of this light will be written to), unlimited list
# channels_raw: plugin (Render channels the raw diffuse result of this light will be written to), unlimited list
# channels_diffuse: plugin (Render channels the diffuse result of this light will be written to), unlimited list
# channels_specular: plugin (Render channels the specular result of this light will be written to), unlimited list

# tex: acolor texture (The light texture)

# use_tex: bool (true if the texture should be used)
BoolProperty(
	attr= 'vray_lamp_use_tex',
	name= 'use_tex',
	description= "TODO.",
	default= False
)

# tex_resolution: integer (The internal texture resolution)
IntProperty(
	attr= 'vray_lamp_tex_resolution',
	name= 'tex_resolution',
	description= "TODO.",
	min= 0,
	max= 10,
	default= 256
)

# cache_tex: bool (When this is true the texture will be cached at tex_resolution x tex_resolution and this cached texture will be used to determine the texture color for shadows rays(speeding up light evaluation, especially for complex procedural textures))
BoolProperty(
	attr= 'vray_lamp_cache_tex',
	name= 'cache_tex',
	description= "TODO.",
	default= True
)



'''
  Plugin: GeomMeshFile
'''
BoolProperty(
	attr="vray_proxy",
	name="Proxy",
	description="",
	default= False
)

StringProperty(
	attr="vray_proxy_file",
	name="File",
	subtype= 'FILE_PATH',
	description="Proxy file."
)

EnumProperty(
	attr="vray_proxy_anim_type",
	name="Animation type",
	description="Proxy animation type.",
	items=(("LOOP",     "Loop",      "TODO."),
		   ("ONCE",     "Once",      "TODO."),
		   ("PINGPONG", "Ping-pong", "TODO."),
		   ("STILL",    "Still",     "TODO.")),
	default= "LOOP"
)

FloatProperty(
	attr="vray_proxy_anim_speed",
	name="Speed",
	description="Animated proxy playback speed.",
	min=0.0, max=1000.0,
	soft_min=0.0, soft_max=1.0,
	default= 1.0
)

FloatProperty(
	attr="vray_proxy_anim_offset",
	name="Offset",
	description="Animated proxy initial frame offset.",
	min=0.0, max=1000.0, soft_min=0.0, soft_max=1.0, default= 0.0
)

BoolProperty(
	attr="vray_proxy_apply_transforms",
	name="Apply transform",
	description="Apply rotation and location.",
	default= False
)

BoolProperty(
	attr="vray_proxy_apply_scale",
	name="Apply scale",
	description="Apply scale.",
	default= True
)



'''
  GUI
'''
import properties_data_mesh
properties_data_mesh.DATA_PT_context_mesh.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_normals.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_settings.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_shape_keys.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_texface.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_uv_texture.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_vertex_colors.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.DATA_PT_vertex_groups.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.MESH_MT_shape_key_specials.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_mesh.MESH_MT_vertex_group_specials.COMPAT_ENGINES.add('VRAY_RENDER')
del properties_data_mesh


narrowui= 200



def base_poll(cls, context):
	rd= context.scene.render
	return (context.mesh) and (rd.engine in cls.COMPAT_ENGINES)


class DataButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'


class DATA_PT_vray_proxy(DataButtonsPanel, bpy.types.Panel):
	bl_label = "Proxy"
	bl_default_closed = True
	
	COMPAT_ENGINES = {'VRAY_RENDER'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		ob= context.mesh
		self.layout.prop(ob, "vray_proxy", text="")

	def draw(self, context):
		ob= context.mesh

		layout= self.layout

		wide_ui= context.region.width > narrowui

		layout.active= ob.vray_proxy

		split= layout.split()
		col= split.column()
		col.prop(ob, "vray_proxy_file")

		split= layout.split()
		col= split.column()
		col.prop(ob, "vray_proxy_anim_type")

		split= layout.split()
		col= split.column()
		col.prop(ob, "vray_proxy_anim_speed")
		if(wide_ui):
			col= split.column()
		col.prop(ob, "vray_proxy_anim_offset")

		split= layout.split()
		col= split.column()
		col.label(text="Proxy generation:")
		split= layout.split()
		split.active= 0
		col= split.column()
		col.operator("vray_create_proxy")
		if(wide_ui):
			col= split.column()
		col.operator("vray_replace_with_proxy", text= "Replace with proxy")

		split= layout.split()
		split.active= 0
		col= split.column()
		col.prop(ob, "vray_proxy_apply_transforms")
		if(wide_ui):
			col= split.column()
		col.prop(ob, "vray_proxy_apply_scale")


# bpy.types.register(DATA_PT_vray_proxy)

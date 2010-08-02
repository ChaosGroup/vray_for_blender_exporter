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


BoolProperty= bpy.types.MaterialTextureSlot.BoolProperty
FloatProperty= bpy.types.MaterialTextureSlot.FloatProperty


'''
  BRDFSSS2Complex
'''
BoolProperty(	attr="vray_fsss_overall_on",
				name="Overall Color",
				description="",
				default = False)

FloatProperty(  attr="vray_fsss_overall_factor",
				name="Overall color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_fsss_diffuse_on",
				name="Diffuse Color",
				description="",
				default = False)

FloatProperty(  attr="vray_fsss_diffuse_factor",
				name="Diffuse Color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_fsss_subsurface_on",
				name="Subsurface Color",
				description="",
				default = False)

FloatProperty(  attr="vray_fsss_subsurface_factor",
				name="Subsurface Color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_fsss_scatter_on",
				name="Scatter Color",
				description="",
				default = False)

FloatProperty(  attr="vray_fsss_scatter_factor",
				name="Scatter Color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)



'''
  BRDFVRayMtl
'''
BoolProperty(
	attr="map_vray_hilight",
	name="Hilight",
	description="TODO.",
	default= False
)

BoolProperty(
	attr="map_myslot",
	name="My Slot",
	description="TODO.",
	default= False
)

FloatProperty(
	attr="vray_hilight_mult",
	name="Hilight multiplier",
	description="TODO.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default= 1.0
)

BoolProperty(	attr="vray_reflect_gloss_on",
				name="Reflect gloss",
				description="",
				default = False)

FloatProperty(  attr="vray_reflect_gloss_factor",
				name="Reflect Gloss multiplier",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_reglect_ior_on",
				name="reflect ior",
				description="",
				default = False)

FloatProperty(  attr="vray_reflect_ior_factor",
				name="reflect factor",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_refract_ior_on",
				name="refract ior",
				description="",
				default = False)

FloatProperty(  attr="vray_refract_ior_factor",
				name="Scatter Color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

BoolProperty(	attr="vray_refract_gloss_on",
				name="refract ior",
				description="",
				default = False)

FloatProperty(  attr="vray_refract_gloss_factor",
				name="Scatter Color",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0)

FloatProperty(
	attr="vray_disp_amount",
	name="Displacement Amount",
	description="",
	min=0.0, max=100.0,
	soft_min=0.0, soft_max=1.0,
	precision= 4,
	default= 1.0
)

FloatProperty(
	attr="vray_disp_shift",
	name="Displacement Shift",
	description="",
	min=-1.0, max=1.0,
	soft_min=-1.0, soft_max=1.0,
	precision= 4,
	default= 0.0
)

FloatProperty(
	attr="vray_disp_water",
	name="Displacement Water",
	description="",
	min=-100.0, max=100.0, soft_min=-1.0, soft_max=1.0,
	default= 0.0
)




FloatProperty= bpy.types.Texture.FloatProperty
IntProperty= bpy.types.Texture.IntProperty
BoolProperty= bpy.types.Texture.BoolProperty
EnumProperty= bpy.types.Texture.EnumProperty
VectorProperty= bpy.types.Texture.FloatVectorProperty

'''
  WORLD
'''
BoolProperty(
	attr= 'map_vray_env_gi',
	name= "Override GI",
	description= "Use texture for GI.",
	default= False
)

BoolProperty(
	attr= 'map_vray_env_refl',
	name= "Override reflections",
	description= "Use texture for reflections.",
	default= False
)

BoolProperty(
	attr= 'map_vray_env_refr',
	name= "Override refractions",
	description= "Use texture for refractions.",
	default= False
)



'''
  TEXTURES
'''
EnumProperty(
	attr= 'vb_tex_type',
	name= "Texture type",
	description= "V-Ray texture type.",
	items=(
		('TEXFRESNEL', "TexFresnel", ""),
		('TEXSKY',     "VRaySky",    "Procedural Sky texture. Depends on Sun position."),
		('NONE',       "None",       "")
	),
	default= 'NONE'
)



'''
  Plugin: TexSky
'''
BoolProperty(
	attr= 'vb_tsky_auto',
	name= 'Take settings from Sun',
	description= "Take settings from Sun automatically.",
	default= True
)

# transform: transform

# target_transform: transform

# turbidity: float
FloatProperty(
	attr= 'vb_tsky_turbidity',
	name= 'Turbidity',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 3
)

# ozone: float
FloatProperty(
	attr= 'vb_tsky_ozone',
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
	attr= 'vb_tsky_water_vapour',
	name= 'Water vapour',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 2
)

# intensity_multiplier: float
FloatProperty(
	attr= 'vb_tsky_intensity_multiplier',
	name= 'Intensity mult.',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

# size_multiplier: float
FloatProperty(
	attr= 'vb_tsky_size_multiplier',
	name= 'Size mult.',
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
	attr= 'vb_tsky_invisible',
	name= 'Invisible',
	description= "TODO.",
	default= False
)

# horiz_illum: float
FloatProperty(
	attr= 'vb_tsky_horiz_illum',
	name= 'Horiz illumination',
	description= "TODO.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 25000
)

# sky_model: integer
EnumProperty(
	attr= 'vb_tsky_sky_model',
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
  Plugin: TexFresnel
'''
# fresnel_ior: float (Fresnel ior.)
FloatProperty(
	attr= 'vb_TexFresnel_fresnel_ior',
	name= 'Fresnel IOR',
	description= "Fresnel ior.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1.55
)

# refract_ior: float (Refraction ior of the underlying surface; this is ignored if the surface has a volume shader (the volume IOR is used).)
FloatProperty(
	attr= 'vb_TexFresnel_refract_ior',
	name= 'Refract IOR',
	description= "Refraction ior of the underlying surface; this is ignored if the surface has a volume shader (the volume IOR is used).",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1.55
)

# white_color: acolor texture (Refraction (front) color)
VectorProperty(
	attr= 'vb_TexFresnel_white_color',
	name= "Front color",
	description= "Refraction (front) color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0, 0.0, 0.0)
)

# black_color: acolor texture (Reflection (side) color)
VectorProperty(
	attr= 'vb_TexFresnel_black_color',
	name= "Side color",
	description= "Reflection (side) color.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1.0, 1.0, 1.0)
)



'''
  GUI
'''


narrowui= bpy.context.user_preferences.view.properties_width_check


import properties_texture
properties_texture.TEXTURE_PT_context_texture.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_mapping.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_image.COMPAT_ENGINES.add('VRAY_RENDER')
del properties_texture


def context_tex_datablock(context):
    idblock= context.material
    if idblock:
        return idblock

    idblock= context.lamp
    if idblock:
        return idblock

    idblock= context.world
    if idblock:
        return idblock

    idblock= context.brush
    return idblock


class TextureButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'

	def poll(self, context):
		tex= context.texture
		if not tex or tex == None:
			return False
		engine= context.scene.render.engine
		return (tex.type != 'NONE' or tex.use_nodes) and (engine in self.COMPAT_ENGINES)


class TEXTURE_PT_vray_influence(TextureButtonsPanel, bpy.types.Panel):
	bl_label = "Influence"
	
	COMPAT_ENGINES = {'VRAY_RENDER'}

	def poll(self, context):
		if hasattr(context, "texture_slot"):
			if context.texture_slot:
				return True
		return False

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		idblock= context_tex_datablock(context)

		tex= context.texture_slot
		mat= context.material
		
		def factor_but(layout, active, toggle, factor, label= None):
			row= layout.row(align=True)
			row.prop(tex, toggle, text="")
			sub= row.row()
			sub.active= active
			if(label):
				sub.prop(tex, factor, slider=True, text=label)
			else:
				sub.prop(tex, factor, slider=True)

		if type(idblock) == bpy.types.Material:
			layout.split().row().label(text= "This doesn't work as it should...")
			layout.split().row().label(text= "We need to wait for some additions from BF.")

			split= layout.split()
			col= split.column()
			col.label(text = "Shading:")
			factor_but(col, tex.map_colordiff,   "map_colordiff",    "colordiff_factor",  "Color")
			factor_but(col, tex.map_colorspec,   "map_colorspec",    "colorspec_factor",  "Hilight")
			factor_but(col, tex.map_specular,    "map_specular",     "specular_factor",   "Glossy")
			factor_but(col, tex.map_raymir,      "map_raymir",       "raymir_factor",     "Reflection")
			factor_but(col, tex.map_emit,        "map_emit",         "emit_factor",       "Emit")
			factor_but(col, tex.map_alpha,       "map_alpha",        "alpha_factor",      "Alpha")

			col= split.column()
			col.label(text = "SSS:")
			factor_but(col, tex.vray_fsss_overall_on,    "vray_fsss_overall_on",    "vray_fsss_overall_factor")
			factor_but(col, tex.vray_fsss_diffuse_on,    "vray_fsss_diffuse_on",    "vray_fsss_diffuse_factor")
			factor_but(col, tex.vray_fsss_subsurface_on, "vray_fsss_subsurface_on", "vray_fsss_subsurface_factor")
			factor_but(col, tex.vray_fsss_scatter_on,    "vray_fsss_scatter_on",    "vray_fsss_scatter_factor")

			split= layout.split()
			col= split.column()
			col.label(text="Geometry:")
			factor_but(col, tex.map_normal,       "map_normal",       "normal_factor",       "Bump/Normal")
			factor_but(col, tex.map_displacement, "map_displacement", "displacement_factor", "Displace")

			col= split.column()
			col.active= tex.map_displacement
			col.label(text = "Displacement settings:")
			col.prop(tex,"vray_disp_amount",text="Amount",slider=True)
			col.prop(tex,"vray_disp_shift",text="Shift",slider=True)
			col.prop(tex,"vray_disp_water",text="Water",slider=True)

		elif type(idblock) == bpy.types.Lamp:
			# vray_lamp_intensity_tex
			# vray_lamp_shadowColor_tex
			# vray_lamp_rect_tex
			pass

		elif type(idblock) == bpy.types.World:
			# factor_but(col, tex.map_vray_env_gi,   "map_vray_env_gi",   "", "")
			# factor_but(col, tex.map_vray_env_refl, "map_vray_env_refl", "", "")
			# factor_but(col, tex.map_vray_env_refr, "map_vray_env_refr", "", "")

			split= layout.split()
			col= split.column()
			col.label(text="Environment:")
			factor_but(col, tex.map_blend,   "map_blend", "blend_factor",   "Background")

			if(wide_ui):
				col= split.column()
			col.label(text="Override:")
			factor_but(col, tex.map_horizon, "map_horizon",         "horizon_factor",     "GI")
			factor_but(col, tex.map_zenith_up,   "map_zenith_up",   "zenith_up_factor",   "Reflections")
			factor_but(col, tex.map_zenith_down, "map_zenith_down", "zenith_down_factor", "Refractions")
		else:
			pass


class TEXTURE_PT_plugin(TextureButtonsPanel, bpy.types.Panel):
	bl_label = "V-Ray Textures"

	COMPAT_ENGINES = {'VRAY_RENDER'}

	def poll(self, context):
		tex= context.texture
		engine= context.scene.render.engine
		return (tex and tex.type == 'PLUGIN' and (engine in self.COMPAT_ENGINES))

	def draw(self, context):
		tex= context.texture
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop(tex,'vb_tex_type')

		if(tex.vb_tex_type == 'NONE'):
			split= layout.split()
			col= split.column()
			col.label(text="Please, select texture type.")

		elif(tex.vb_tex_type == 'TEXSKY'):
			split= layout.split()
			col= split.column()
			col.label(text="VRaySky:")

			split= layout.split()
			col= split.column()
			col.prop(tex, 'vb_tsky_auto')

			split= layout.split()
			split.active= not tex.vb_tsky_auto
			col= split.column()
			col.prop(tex, 'vb_tsky_sky_model')
			
			split= layout.split()
			split.active= not tex.vb_tsky_auto
			col= split.column()
			col.prop(tex, 'vb_tsky_turbidity')
			col.prop(tex, 'vb_tsky_ozone')
			col.prop(tex, 'vb_tsky_intensity_multiplier')
			col.prop(tex, 'vb_tsky_size_multiplier')
			if(wide_ui):
				col= split.column()
			col.prop(tex, 'vb_tsky_invisible')
			col.prop(tex, 'vb_tsky_horiz_illum')
			col.prop(tex, 'vb_tsky_water_vapour')

		elif(tex.vb_tex_type == 'TEXFRESNEL'):
			split= layout.split()
			col= split.column()
			col.label(text="Fresnel texture:")

			split= layout.split()
			col= split.column()
			col.prop(tex, 'vb_TexFresnel_white_color')
			col.prop(tex, 'vb_TexFresnel_fresnel_ior')
			if(wide_ui):
				col= split.column()
			col.prop(tex, 'vb_TexFresnel_black_color')
			col.prop(tex, 'vb_TexFresnel_refract_ior')

			split= layout.split()
			col= split.column()
			col.label(text="Use \"Nodes\" for advanced control.")

		else:
			pass

 
bpy.types.register(TEXTURE_PT_vray_influence)

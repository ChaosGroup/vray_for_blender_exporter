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


# class VRaySlot(bpy.types.IDPropertyGroup):
# 	pass

# bpy.types.MaterialTextureSlot.PointerProperty(
# 	attr= 'vray_slot',
# 	type= VRaySlot,
# 	name= "Slot",
# 	description= "V-Ray texture slot"
# )

# VRaySlot.BoolProperty(
# 	attr='overall',
# 	name="Overall Color",
# 	description="TODO.",
# 	default=False
# )

# VRaySlot.FloatProperty(
# 	attr="overall_factor",
# 	name="Overall multiplier",
# 	description="TODO.",
# 	min=0.0, max=10.0,
# 	soft_min=0.0, soft_max=1.0,
# 	default=1.0
# )


'''
  SLOT
'''

'''
  Plugin: BRDFSSS2Complex
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
  Plugin: BRDFVRayMtl
'''
BoolProperty(
	attr="map_vray_hilight",
	name="Hilight",
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

BoolProperty(
	attr="vray_reflect_gloss_on",
	name="Reflect gloss",
	description="",
	default = False
)

FloatProperty(
	attr="vray_reflect_gloss_factor",
	name="Reflect Gloss multiplier",
	description="",
	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
)

BoolProperty(
	attr="vray_reglect_ior_on",
	name="reflect ior",
	description="",
	default = False
)

FloatProperty(
	attr="vray_reflect_ior_factor",
	name="reflect factor",
	description="",
	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
)

BoolProperty(
	attr="vray_refract_ior_on",
	name="refract ior",
	description="",
	default = False
)

FloatProperty(
	attr="vray_refract_ior_factor",
	name="Scatter Color",
	description="",
	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
)

BoolProperty(
	attr="vray_refract_gloss_on",
	name="refract ior",
	description="",
	default = False
)

FloatProperty(
	attr="vray_refract_gloss_factor",
	name="Scatter Color",
	description="",
	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
)

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
  GUI
'''

narrowui= 200

import properties_texture
properties_texture.TEXTURE_PT_context_texture.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_mapping.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_image.COMPAT_ENGINES.add('VRAY_RENDER')

properties_texture.TEXTURE_PT_context_texture.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_texture.TEXTURE_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_texture.TEXTURE_PT_mapping.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_texture.TEXTURE_PT_image.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
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


def base_poll(cls, context):
	rd= context.scene.render
	tex= context.texture
	if not tex or tex == None:
		return False
	return (tex.type != 'NONE' or tex.use_nodes) and (rd.engine in cls.COMPAT_ENGINES)


class TextureButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_vray_influence(TextureButtonsPanel, bpy.types.Panel):
	bl_label = "Influence"
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		if hasattr(context, "texture_slot"):
			if context.texture_slot:
				return True
		return False

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		idblock= context_tex_datablock(context)

		tex= context.texture_slot
		# vslot= context.texture_slot.vray_slot
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
			split= layout.split()
			col= split.column()
			col.label(text = "Shading:")
			factor_but(col, tex.map_colordiff,   "map_colordiff",    "colordiff_factor",   "Color")
			factor_but(col, tex.map_colorspec,   "map_colorspec",    "colorspec_factor",   "Hilight")
			factor_but(col, tex.map_specular,    "map_specular",     "specular_factor",    "Glossy")
			factor_but(col, tex.map_raymir,      "map_raymir",       "raymir_factor",      "Reflection")
			factor_but(col, tex.map_emit,        "map_emit",         "emit_factor",        "Emit")
			factor_but(col, tex.map_alpha,       "map_alpha",        "alpha_factor",       "Alpha")
			factor_but(col, tex.map_translucency,"map_translucency", "translucency_factor","Refraction")

			if(wide_ui):
				col= split.column()
			col.label(text = "(TODO) SSS:")
			# factor_but(col, vslot.overall_on, 'overall_on', 'overall_factor')
			factor_but(col, tex.vray_fsss_overall_on,    "vray_fsss_overall_on",    "vray_fsss_overall_factor")
			factor_but(col, tex.vray_fsss_diffuse_on,    "vray_fsss_diffuse_on",    "vray_fsss_diffuse_factor")
			factor_but(col, tex.vray_fsss_subsurface_on, "vray_fsss_subsurface_on", "vray_fsss_subsurface_factor")
			factor_but(col, tex.vray_fsss_scatter_on,    "vray_fsss_scatter_on",    "vray_fsss_scatter_factor")

			split= layout.split()
			col= split.column()
			col.label(text="Geometry:")
			factor_but(col, tex.map_normal,       "map_normal",       "normal_factor",       "Bump/Normal")
			factor_but(col, tex.map_displacement, "map_displacement", "displacement_factor", "Displace")

			if(wide_ui):
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
			factor_but(col, tex.map_horizon,     "map_horizon",     "horizon_factor",     "GI")
			factor_but(col, tex.map_zenith_up,   "map_zenith_up",   "zenith_up_factor",   "Reflections")
			factor_but(col, tex.map_zenith_down, "map_zenith_down", "zenith_down_factor", "Refractions")
		else:
			pass


class TEXTURE_PT_plugin(TextureButtonsPanel, bpy.types.Panel):
	bl_label = "V-Ray Textures"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		engine= context.scene.render.engine
		return (tex and tex.type == 'PLUGIN' and (engine in __class__.COMPAT_ENGINES))

	def draw(self, context):
		tex= context.texture
		vtex= tex.vray_texture
		
		wide_ui= context.region.width > narrowui

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop(vtex,'type')

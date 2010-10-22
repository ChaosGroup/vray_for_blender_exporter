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


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


Slot= bpy.types.Texture

class VRaySlot(bpy.types.IDPropertyGroup):
	pass

Slot.vray_slot= PointerProperty(
	name= "V-Ray Material Texture Slot",
	type=  VRaySlot,
	description= "V-Ray material texture slot settings."
)


class BRDFSSS2Complex(bpy.types.IDPropertyGroup):
	pass

VRaySlot.BRDFSSS2Complex= PointerProperty(
	name= "BRDFSSS2Complex",
	type=  BRDFSSS2Complex,
	description= "BRDFSSS2Complex texture slot settings."
)

BRDFSSS2Complex.map_overall_color= BoolProperty(
	name= "Overall Color",
	description= "TODO.",
	default= False
)

BRDFSSS2Complex.overall_color_factor= FloatProperty(
	name= "Overall Color Multiplier",
	description= "TODO.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=1.0
)

BRDFSSS2Complex.map_diffuse_color= BoolProperty(
	name= "Diffuse Color",
	description= "TODO.",
	default= False
)

BRDFSSS2Complex.diffuse_color_factor= FloatProperty(
	name= "Diffuse Color Multiplier",
	description= "TODO.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=1.0
)

BRDFSSS2Complex.map_sub_surface_color= BoolProperty(
	name= "Subsurface Color",
	description= "TODO.",
	default= False
)

BRDFSSS2Complex.sub_surface_color_factor= FloatProperty(
	name= "Subsurface Color Multiplier",
	description= "TODO.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=1.0
)

BRDFSSS2Complex.map_scatter_radius= BoolProperty(
	name= "Scatter Radius",
	description= "TODO.",
	default= False
)

BRDFSSS2Complex.scatter_radius_factor= FloatProperty(
	name= "Scatter Color Multiplier",
	description= "TODO.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=1.0
)


class GeomDisplacedMesh(bpy.types.IDPropertyGroup):
	pass

VRaySlot.GeomDisplacedMesh= PointerProperty(
	name= "GeomDisplacedMesh",
	type=  GeomDisplacedMesh,
	description= "GeomDisplacedMesh texture slot settings."
)

GeomDisplacedMesh.displacement_amount= FloatProperty(
	name= "Amount",
	description= "",
	min=-100.0,
	max=100.0,
	soft_min=-1.0,
	soft_max=1.0,
	precision=4,
	default=1.0
)

GeomDisplacedMesh.displacement_shift= FloatProperty(
	name="Shift",
	description="",
	min=-100.0,
	max=100.0,
	soft_min=-1.0,
	soft_max=1.0,
	precision=4,
	default=0.0
)

GeomDisplacedMesh.water_level= FloatProperty(
	name="Water level",
	description="",
	min=-100.0, max=100.0, soft_min=-1.0, soft_max=1.0,
	default=0.0
)


# '''
#   Plugin: BRDFVRayMtl
# '''
# BoolProperty(
# 	attr="map_vray_hilight",
# 	name="Hilight",
# 	description="TODO.",
# 	default= False
# )

# FloatProperty(
# 	attr="vray_hilight_mult",
# 	name="Hilight multiplier",
# 	description="TODO.",
# 	min=0.0,
# 	max=1.0,
# 	soft_min=0.0,
# 	soft_max=1.0,
# 	default= 1.0
# )

# BoolProperty(
# 	attr="vray_reflect_gloss_on",
# 	name="Reflect gloss",
# 	description="",
# 	default = False
# )

# FloatProperty(
# 	attr="vray_reflect_gloss_factor",
# 	name="Reflect Gloss multiplier",
# 	description="",
# 	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
# )

# BoolProperty(
# 	attr="vray_reglect_ior_on",
# 	name="reflect ior",
# 	description="",
# 	default = False
# )

# FloatProperty(
# 	attr="vray_reflect_ior_factor",
# 	name="reflect factor",
# 	description="",
# 	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
# )

# BoolProperty(
# 	attr="vray_refract_ior_on",
# 	name="refract ior",
# 	description="",
# 	default = False
# )

# FloatProperty(
# 	attr="vray_refract_ior_factor",
# 	name="Scatter Color",
# 	description="",
# 	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
# )

# BoolProperty(
# 	attr="vray_refract_gloss_on",
# 	name="refract ior",
# 	description="",
# 	default = False
# )

# FloatProperty(
# 	attr="vray_refract_gloss_factor",
# 	name="Scatter Color",
# 	description="",
# 	min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default = 1.0
# )


# '''
#   WORLD
# '''
# BoolProperty(
# 	attr= 'map_vray_env_gi',
# 	name= "Override GI",
# 	description= "Use texture for GI.",
# 	default= False
# )

# BoolProperty(
# 	attr= 'map_vray_env_refl',
# 	name= "Override reflections",
# 	description= "Use texture for reflections.",
# 	default= False
# )

# BoolProperty(
# 	attr= 'map_vray_env_refr',
# 	name= "Override refractions",
# 	description= "Use texture for refractions.",
# 	default= False
# )



'''
  GUI
'''

narrowui= 200

import properties_texture
properties_texture.TEXTURE_PT_mapping.COMPAT_ENGINES.add('VRAY_RENDER')
properties_texture.TEXTURE_PT_image.COMPAT_ENGINES.add('VRAY_RENDER')

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
	try:
		tex= context.texture_slot.texture
	except:
		return False
	if tex is None:
		return False
	return (tex.type != 'NONE' or tex.use_nodes) and (rd.engine in cls.COMPAT_ENGINES)


class TextureButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class TEXTURE_PT_context_texture(TextureButtonsPanel, bpy.types.Panel):
	bl_label   = ""
	bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		engine = context.scene.render.engine
		if not hasattr(context, "texture_slot"):
			return False
		return ((context.material or context.world or context.lamp or context.brush or context.texture)
				and (engine in cls.COMPAT_ENGINES))

	def draw(self, context):
		layout = self.layout
		slot = context.texture_slot
		node = context.texture_node
		space = context.space_data
		tex = context.texture
		idblock = context_tex_datablock(context)
		tex_collection = space.pin_id == None and type(idblock) != bpy.types.Brush and not node

		if tex_collection:
			row = layout.row()
			row.template_list(idblock, "texture_slots", idblock, "active_texture_index", rows=2)
			col = row.column(align=True)
			col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
			col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
			col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

		split = layout.split(percentage=0.65)
		col = split.column()

		if tex_collection:
			col.template_ID(idblock, "active_texture", new="texture.new")
		elif node:
			col.template_ID(node, "texture", new="texture.new")
		elif idblock:
			col.template_ID(idblock, "texture", new="texture.new")

		if space.pin_id:
			col.template_ID(space, "pin_id")

		col = split.column()

		if not space.pin_id:
			col.prop(space, "show_brush_texture", text="Brush", toggle=True)

		if tex:
			split = layout.split(percentage=0.2)
			if tex.use_nodes:
				if slot:
					split.label(text="Output:")
					split.prop(slot, "output_node", text="")
			else:
				split.label(text="Texture:")
				split.prop(tex, "type", text="")
				if tex.type == 'VRAY':
					split= layout.split()
					col= split.column()
					col.prop(tex.vray, 'type', text="Type")


class TEXTURE_PT_vray_influence(TextureButtonsPanel, bpy.types.Panel):
	bl_label = "Influence"
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		idblock= context_tex_datablock(context)
		return (base_poll(__class__, context) and (type(idblock) in (bpy.types.Material,bpy.types.Lamp,bpy.types.World)))

	def draw(self, context):
		def factor_but(layout, slot, toggle, factor, label= None):
			row= layout.row(align=True)
			row.prop(slot, toggle, text="")
			sub= row.row()
			sub.active= getattr(slot,toggle)
			if label:
				sub.prop(slot, factor, slider=True, text=label)
			else:
				sub.prop(slot, factor, slider=True)

		layout= self.layout
		wide_ui= context.region.width > narrowui

		idblock= context_tex_datablock(context)

		texture_slot= context.texture_slot
		texture= texture_slot.texture

		# TEMP! Replace after BF fixes
		#VRaySlot= texture_slot.vray
		if texture is not None:
			VRaySlot= texture.vray_slot
		
		mat= context.material
		
		if type(idblock) == bpy.types.Material:
			split= layout.split()
			col= split.column()
			col.label(text="Shading:")
			factor_but(col, texture_slot, 'use_map_color_diffuse', 'diffuse_color_factor',   "Color")
			factor_but(col, texture_slot, 'use_map_alpha',         'alpha_factor',           "Alpha")
			factor_but(col, texture_slot, 'use_map_raymir',        'raymir_factor',          "Reflection")
			factor_but(col, texture_slot, 'use_map_specular',      'specular_factor',        "Glossy")
			factor_but(col, texture_slot, 'use_map_color_spec',    'specular_color_factor',  "Hilight")
			factor_but(col, texture_slot, 'use_map_translucency',  'translucency_factor',    "Refraction")
			factor_but(col, texture_slot, 'use_map_emit',          'emit_factor',            "Emit")

			if wide_ui:
				col= split.column()

			if VRaySlot is not None:
				BRDFSSS2Complex= VRaySlot.BRDFSSS2Complex

				col.label(text="SSS:")
				factor_but(col, BRDFSSS2Complex, 'map_overall_color',     'overall_color_factor',     "Overall")
				factor_but(col, BRDFSSS2Complex, 'map_diffuse_color',     'diffuse_color_factor',     "Diffuse")
				factor_but(col, BRDFSSS2Complex, 'map_sub_surface_color', 'sub_surface_color_factor', "Sub-surface")
				factor_but(col, BRDFSSS2Complex, 'map_scatter_radius',    'scatter_radius_factor',    "Scatter Radius")

			split= layout.split()
			col= split.column()
			col.label(text="Geometry:")
			factor_but(col, texture_slot, 'use_map_normal',       'normal_factor',       "Bump/Normal")
			factor_but(col, texture_slot, 'use_map_displacement', 'displacement_factor', "Displace")

			if wide_ui:
				col= split.column()

			if VRaySlot is not None:
				GeomDisplacedMesh= VRaySlot.GeomDisplacedMesh

				col.active= texture_slot.use_map_displacement
				col.label(text="Displacement")
				col.prop(GeomDisplacedMesh,'displacement_amount',text="Amount",slider=True)
				col.prop(GeomDisplacedMesh,'displacement_shift',text="Shift",slider=True)
				col.prop(GeomDisplacedMesh,'water_level',text="Water",slider=True)

		elif type(idblock) == bpy.types.Lamp:
			# intensity_tex
			# shadowColor_tex
			# rect_tex
			pass

		elif type(idblock) == bpy.types.World:
			split= layout.split()
			col= split.column()
			col.label(text="Environment:")
			factor_but(col, texture_slot, 'use_map_blend',       'blend_factor',       "Background")

			if wide_ui:
				col= split.column()
			
			col.label(text="Override:")
			factor_but(col, texture_slot, 'use_map_horizon',     'horizon_factor',     "GI")
			factor_but(col, texture_slot, 'use_map_zenith_up',   'zenith_up_factor',   "Reflections")
			factor_but(col, texture_slot, 'use_map_zenith_down', 'zenith_down_factor', "Refractions")

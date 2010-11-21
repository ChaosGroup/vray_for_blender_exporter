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


class VRayImage(bpy.types.IDPropertyGroup):
	pass

bpy.types.Image.vray= PointerProperty(
	name= "V-Ray Image Settings",
	type=  VRayImage,
	description= "V-Ray image settings."
)

class BitmapBuffer(bpy.types.IDPropertyGroup):
	pass

VRayImage.BitmapBuffer= PointerProperty(
	name= "BitmapBuffer",
	type=  BitmapBuffer,
	description= "BitmapBuffer settings."
)

BitmapBuffer.filter_type= EnumProperty(
	name= "Filter type",
	description= "Filter type.",
	items= (
		('NONE',   "None",        "."),
		('MIPMAP', "Mip-Map",     "."),
		('AREA',   "Summed Area", ".")
	),
	default= 'AREA'
)

BitmapBuffer.filter_blur= FloatProperty(
	name= "Blur",
	description= "Filter blur.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.0
)

BitmapBuffer.gamma= FloatProperty(
	name= "Gamma",
	description= "Gamma.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.0
)

BitmapBuffer.allow_negative_colors= BoolProperty(
	name= "Allow negative colors",
	description= "If false negative colors will be clamped.",
	default= False
)

BitmapBuffer.use_data_window= BoolProperty(
	name= "Use data window",
	description= "True to use the data window information in e.g. OpenEXR files.",
	default= True
)


Slot= bpy.types.Texture

class VRaySlot(bpy.types.IDPropertyGroup):
	pass

Slot.vray_slot= PointerProperty(
	name= "V-Ray Material Texture Slot",
	type=  VRaySlot,
	description= "V-Ray material texture slot settings."
)

VRaySlot.uvwgen= StringProperty(
	name= "UVW Generator",
	subtype= 'NONE',
	options= {'HIDDEN'},
	description= "TEMP VARIABLE.",
	default= "UVWGenChannel_default"
)

VRaySlot.blend_modes= EnumProperty(
	name= "Blend mode",
	description= "Blend mode.",
	items= (
		('OVER', "Over", "."),
		('IN', "In", "."),
		('OUT', "Out", "."),
		('ADD', "Add", "."),
		('SUBSTRACT', "Substract", "."),
		('MULTIPLY', "Multiply", "."),
		('DIFFERENCE', "Difference", "."),
		('LIGHTEN', "Lighten", "."),
		('DARKEN', "Darken", "."),
		('SATURATE', "Saturate", "."),
		('DESATUREATE', "Desaturate", "."),
		('ILLUMINATE', "Illuminate", ".")
	),
	default= 'OVER'
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

GeomDisplacedMesh.type= EnumProperty(
	name= "Type",
	description= "Displacement type.",
	items= (
		('2D',  "2D",     "2D displacement."),
		('NOR', "Normal", "Normal displacement."),
		('3D',  "Vector", "Vector displacement.")
	),
	default= 'NOR'
)

# GeomDisplacedMesh.displacement_amount= FloatProperty()
# This is 'displacement_factor' actually.

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

	
GeomDisplacedMesh.use_globals= BoolProperty(
	name= "Use globals",
	description= "If true, the global displacement quality settings will be used.",
	default= True
)

GeomDisplacedMesh.view_dep= BoolProperty(
	name= "View dependent",
	description= "Determines if view-dependent tesselation is used",
	default= True
)

GeomDisplacedMesh.edge_length= FloatProperty(
	name= "Edge length",
	description= "Determines the approximate edge length for the sub-triangles",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 4
)

GeomDisplacedMesh.max_subdivs= IntProperty(
	name= "Max subdivs",
	description= "Determines the maximum subdivisions for a triangle of the original mesh",
	min= 0,
	max= 2048,
	soft_min= 0,
	soft_max= 1024,
	default= 256
)

GeomDisplacedMesh.keep_continuity= BoolProperty(
	name= "Keep continuity",
	description= "If true, the plugin will attempt to keep the continuity of the displaced surface",
	default= False
)

GeomDisplacedMesh.map_channel= IntProperty(
	name= "Map channel",
	description= "The mapping channel to use for vector and 2d displacement.",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 0
)

GeomDisplacedMesh.use_bounds= BoolProperty(
	name= "Use bounds",
	description= "If true, the min/max values for the displacement texture are specified by the min_bound and max_bound parameters; if false, these are calculated automatically.",
	default= False
)

GeomDisplacedMesh.min_bound= FloatVectorProperty(
	name= "Min bound",
	description= "The lowest value for the displacement texture",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0,0,0)
)

GeomDisplacedMesh.max_bound= FloatVectorProperty(
	name= "Max bound",
	description= "The biggest value for the displacement texture",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (1,1,1)
)

GeomDisplacedMesh.resolution= IntProperty(
	name= "Resolution",
	description= "Resolution at which to sample the displacement map for 2d displacement.",
	min= 0,
	max= 2048,
	soft_min= 0,
	soft_max= 512,
	default= 256
)

GeomDisplacedMesh.precision= IntProperty(
	name= "Precision",
	description= "Increase for curved surfaces to avoid artifacts.",
	min= 0,
	max= 100,
	soft_min= 0,
	soft_max= 10,
	default= 8
)

GeomDisplacedMesh.tight_bounds= BoolProperty(
	name= "Tight bounds",
	description= "When this is on, initialization will be slower, but tighter bounds will be computed for the displaced triangles making rendering faster.",
	default= False
)

GeomDisplacedMesh.filter_texture= BoolProperty(
	name= "Filter texture",
	description= "Filter the texture for 2d displacement.",
	default= False
)

GeomDisplacedMesh.filter_blur= FloatProperty(
	name= "Blur",
	description= "The amount of UV space to average for filtering purposes. A value of 1.0 will average the whole texture.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 0.001
)
	




class BRDFBump(bpy.types.IDPropertyGroup):
	pass

VRaySlot.BRDFBump= PointerProperty(
	name= "BRDFBump",
	type=  BRDFBump,
	description= "BRDFBump texture slot settings."
)

BRDFBump.map_type= EnumProperty(
	name= "Map type",
	description= "Normal map type.",
	items= (
		('EXPLICIT', "Normal (explicit)", "."),
		('WORLD',    "Normal (world)",    "."),
		('CAMERA',   "Normal (camera)",   "."),
		('OBJECT',   "Normal (object)",   "."),
		('TANGENT',  "Normal (tangent)" , "."),
		('BUMP',     "Bump",              ".")
	),
	default= 'BUMP'
)

BRDFBump.bump_shadows= BoolProperty(
	name= "Bump shadows",
	description= "Offset the surface shading point, in addition to the normal.",
	default= False
)

BRDFBump.compute_bump_for_shadows= BoolProperty(
	name= "Transparent bump shadows",
	description= "True to compute bump mapping for shadow rays in case the material is transparent; false to skip the bump map for shadow rays (faster rendering).",
	default= True
)



'''
  GUI
'''

narrowui= 200

import properties_texture
properties_texture.TEXTURE_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER')
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


class VRayTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'


class VRAY_TEX_context(VRayTexturePanel, bpy.types.Panel):
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


class VRAY_TEX_influence(VRayTexturePanel, bpy.types.Panel):
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
		if texture:
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
			#factor_but(col, texture_slot, 'use_map_emit',          'emit_factor',            "Emit")

			if wide_ui:
				col= split.column()

			if VRaySlot:
				BRDFSSS2Complex= VRaySlot.BRDFSSS2Complex

				col.label(text="SSS:")
				factor_but(col, BRDFSSS2Complex, 'map_overall_color',     'overall_color_factor',     "Overall")
				factor_but(col, BRDFSSS2Complex, 'map_diffuse_color',     'diffuse_color_factor',     "Diffuse")
				factor_but(col, BRDFSSS2Complex, 'map_sub_surface_color', 'sub_surface_color_factor', "Sub-surface")
				factor_but(col, BRDFSSS2Complex, 'map_scatter_radius',    'scatter_radius_factor',    "Scatter Radius")

			layout.separator()

			split= layout.split()
			col= split.column()
			factor_but(col, texture_slot, 'use_map_normal',       'normal_factor',       "Normal")

			if wide_ui:
				col= split.column()

			if VRaySlot is not None:
				BRDFBump= VRaySlot.BRDFBump

				col.active= texture_slot.use_map_normal
				col.prop(BRDFBump,'map_type',text="Type")
				col.prop(BRDFBump,'bump_shadows')
				col.prop(BRDFBump,'compute_bump_for_shadows')

			split= layout.split()
			col= split.column()
			col.label(text="Geometry:")

			split= layout.split()
			col= split.column()
			factor_but(col, texture_slot, 'use_map_displacement', 'displacement_factor', "Displace")

			if wide_ui:
				col= split.column()

			if VRaySlot is not None:
				GeomDisplacedMesh= VRaySlot.GeomDisplacedMesh

				col.active= texture_slot.use_map_displacement
				col.prop(GeomDisplacedMesh, 'type')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(VRaySlot,'blend_modes',text="Blend")
			if wide_ui:
				col= split.column()
			col.prop(texture_slot,'invert',text="Invert")

			layout.separator()

			split= layout.split()
			col= split.column()
			col.label(text="NOTE: cause of API limitations some parameters are")
			col.label(text="texture dependend not slot.")

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


class VRAY_TEX_displacement(VRayTexturePanel, bpy.types.Panel):
	bl_label = "Displacement"
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		idblock= context_tex_datablock(context)
		if not type(idblock) == bpy.types.Material:
			return False

		texture_slot= context.texture_slot
		if not texture_slot:
			return False

		texture= texture_slot.texture
		if not texture:
			return False
		
		return (base_poll(__class__, context) and (texture_slot.use_map_displacement))

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		texture_slot= context.texture_slot
		texture= texture_slot.texture

		if texture:
			VRaySlot= texture.vray_slot

			if VRaySlot:
				GeomDisplacedMesh= VRaySlot.GeomDisplacedMesh

				split= layout.split()
				col= split.column()

				col.prop(GeomDisplacedMesh, 'displacement_shift', slider=True)
				col.prop(GeomDisplacedMesh, 'water_level', slider=True)
				col.prop(GeomDisplacedMesh, 'resolution')
				col.prop(GeomDisplacedMesh, 'precision')
				if wide_ui:
					col= split.column()
				col.prop(GeomDisplacedMesh, 'keep_continuity')
				col.prop(GeomDisplacedMesh, 'use_bounds')
				if GeomDisplacedMesh.use_bounds:
					sub= col.row()
					sub.prop(GeomDisplacedMesh, 'min_bound', text="Min")
					sub.prop(GeomDisplacedMesh, 'max_bound', text="Max")
				col.prop(GeomDisplacedMesh, 'filter_texture')
				if GeomDisplacedMesh.filter_texture:
					col.prop(GeomDisplacedMesh, 'filter_blur')

				split= layout.split()
				col= split.column()
				col.prop(GeomDisplacedMesh, 'use_globals')
				if not GeomDisplacedMesh.use_globals:
					split= layout.split()
					col= split.column()
					col.prop(GeomDisplacedMesh, 'edge_length')
					col.prop(GeomDisplacedMesh, 'max_subdivs')
					if wide_ui:
						col= split.column()
					col.prop(GeomDisplacedMesh, 'view_dep')
					col.prop(GeomDisplacedMesh, 'tight_bounds')


class VRAY_TEX_image(VRayTexturePanel, bpy.types.Panel):
	bl_label = "Image Settings"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		engine= context.scene.render.engine
		return tex and ((tex.type == 'IMAGE' and tex.image) and (engine in cls.COMPAT_ENGINES))

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		texture_slot= context.texture_slot
		tex= texture_slot.texture

		BitmapBuffer= tex.image.vray.BitmapBuffer

		split= layout.split()
		col= split.column()
		col.prop(BitmapBuffer, 'filter_type', text="Filter")
		if BitmapBuffer.filter_type != 'NONE':
			col.prop(BitmapBuffer, 'filter_blur')
		if wide_ui:
			col= split.column()
		col.prop(BitmapBuffer, 'gamma')
		col.prop(BitmapBuffer, 'allow_negative_colors')
		col.prop(BitmapBuffer, 'use_data_window')
		


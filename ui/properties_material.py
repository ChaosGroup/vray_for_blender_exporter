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

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *
from vb25.plugins import *


import properties_material
#properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER')
properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
del properties_material


def active_node_mat(mat):
    if mat:
        mat_node= mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat
    return None


class MATERIAL_MT_VRAY_presets(bpy.types.Menu):
	bl_label= "SSS Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "sss")
	preset_operator = "script.execute_preset"
	draw = bpy.types.Menu.draw_preset


class VRAY_MP_context_material(VRayMaterialPanel, bpy.types.Panel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		rd= context.scene.render
		return (context.material or context.object) and base_poll(__class__, context)
	
	def draw(self, context):
		layout= self.layout

		mat= active_node_mat(context.material)
		
		ob= context.object
		slot= context.material_slot
		space= context.space_data

		wide_ui= context.region.width > narrowui

		if ob:
			row = layout.row()
			row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
			col = row.column(align=True)
			col.operator("object.material_slot_add", icon='ZOOMIN', text="")
			col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")
			col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")
			if ob.mode == 'EDIT':
				row = layout.row(align=True)
				row.operator("object.material_slot_assign", text="Assign")
				row.operator("object.material_slot_select", text="Select")
				row.operator("object.material_slot_deselect", text="Deselect")

		if wide_ui:
			split = layout.split(percentage=0.65)

			if ob:
				split.template_ID(ob, "active_material", new="material.new")
				row = split.row()
				if mat:
					row.prop(mat, "use_nodes", icon="NODETREE", text="")

				if slot:
					row.prop(slot, "link", text="")
				else:
					row.label()
			elif mat:
				split.template_ID(space, "pin_id")
				split.separator()
		else:
			if ob:
				layout.template_ID(ob, "active_material", new="material.new")
			elif mat:
				layout.template_ID(space, "pin_id")

		if mat:
			VRayMaterial= mat.vray
			if wide_ui:
				layout.prop(VRayMaterial, 'type', expand=True)
			else:
				layout.prop(VRayMaterial, 'type')


class VRAY_MP_basic(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Parameters"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		material= active_node_mat(context.material)
		if material is None:
			return False
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		material= active_node_mat(context.material)

		VRayMaterial= material.vray

		PLUGINS['BRDF'][VRayMaterial.type].gui(context, layout,
											   getattr(VRayMaterial, VRayMaterial.type),
											   material)


class VRAY_MP_options(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Options"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		material= active_node_mat(context.material)
		if material is None:
			return False
		VRayMaterial= material.vray
		return VRayMaterial.type == 'BRDFVRayMtl' and base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > 200
		
		ve= context.scene.vray.exporter
		ob= context.object
		material= active_node_mat(context.material)
		
		VRayMaterial= material.vray
		BRDFVRayMtl= VRayMaterial.BRDFVRayMtl

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'reflect_trace')
		col.prop(BRDFVRayMtl, 'refract_trace')
		col.prop(BRDFVRayMtl, 'option_cutoff')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'option_double_sided')
		col.prop(BRDFVRayMtl, 'option_reflect_on_back')
		col.prop(BRDFVRayMtl, 'option_use_irradiance_map')

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'reflect_exit_color')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'refract_exit_color')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'option_glossy_rays_as_gi')
		col.prop(BRDFVRayMtl, 'option_energy_mode')

		split= layout.split()
		col= split.column()
		col.prop(BRDFVRayMtl, 'option_cutoff')
		if wide_ui:
			col= split.column()
		col.prop(BRDFVRayMtl, 'environment_priority')


class VRAY_MAT_two_sided(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Two-Sided"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return active_node_mat(context.material) and base_poll(__class__, context)

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		Mtl2Sided= ma.vray.Mtl2Sided
		self.layout.prop(Mtl2Sided, 'use', text="")

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > 200

		ma= active_node_mat(context.material)

		Mtl2Sided= ma.vray.Mtl2Sided
		
		layout.active= Mtl2Sided.use

		split= layout.split()
		col= split.column()
		col.prop_search(Mtl2Sided, 'back', bpy.data, 'materials', text= "Back material")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(Mtl2Sided, 'control')

		if Mtl2Sided.control == 'SLIDER':
			split= layout.split()
			col= split.column()
			col.prop(Mtl2Sided, 'translucency_slider', slider=True)
		elif Mtl2Sided.control == 'COLOR':
			split= layout.split()
			col= split.column()
			col.prop(Mtl2Sided, 'translucency_color', text="")
		else:
			split= layout.split(percentage=0.3)
			col= split.row()
			col.prop(Mtl2Sided, 'translucency_tex_mult', text="Mult")
			col= split.row()
			col.prop_search(Mtl2Sided, 'translucency_tex', bpy.data, 'textures', text= "")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(Mtl2Sided, 'force_1sided')


class VRAY_MP_override(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Override"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return active_node_mat(context.material) and base_poll(__class__, context)

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		MtlOverride= ma.vray.MtlOverride
		self.layout.prop(MtlOverride, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		MtlOverride= ma.vray.MtlOverride
		
		layout= self.layout
		layout.active= MtlOverride.use

		split= layout.split()
		col= split.column()
		col.prop_search(MtlOverride, 'gi_mtl',      bpy.data, 'materials', text= "GI")
		col.prop_search(MtlOverride, 'reflect_mtl', bpy.data, 'materials', text= "Reflection")
		col.prop_search(MtlOverride, 'refract_mtl', bpy.data, 'materials', text= "Refraction")
		col.prop_search(MtlOverride, 'shadow_mtl',  bpy.data, 'materials', text= "Shadow")

		layout.separator()
		split= layout.split()
		col= split.column()
		col.prop_search(MtlOverride, 'environment_override',  bpy.data, 'textures', text= "Environment")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(MtlOverride, 'environment_priority')


class VRAY_MP_wrapper(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Wrapper"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return active_node_mat(context.material) and base_poll(__class__, context)

	def draw_header(self, context):
		mat= active_node_mat(context.material)
		MtlWrapper= mat.vray.MtlWrapper
		self.layout.prop(MtlWrapper, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		MtlWrapper= ma.vray.MtlWrapper
		
		layout= self.layout
		layout.active= MtlWrapper.use

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'generate_gi')
		col.prop(MtlWrapper, 'receive_gi')
		if wide_ui:
			col= split.column()
		col.prop(MtlWrapper, 'generate_caustics')
		col.prop(MtlWrapper, 'receive_caustics')

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'gi_quality_multiplier')

		split= layout.split()
		col= split.column()
		col.label(text="Matte properties")

		split= layout.split()
		colL= split.column()
		colL.prop(MtlWrapper, 'matte_surface')
		if wide_ui:
			colR= split.column()
		else:
			colR= colL
		colR.prop(MtlWrapper, 'alpha_contribution')
		if MtlWrapper.matte_surface:
			colL.prop(MtlWrapper, 'affect_alpha')
			colL.prop(MtlWrapper, 'shadows')
			if MtlWrapper.shadows:
				colL.prop(MtlWrapper, 'shadow_tint_color')
				colL.prop(MtlWrapper, 'shadow_brightness')

			colR.prop(MtlWrapper, 'reflection_amount')
			colR.prop(MtlWrapper, 'refraction_amount')
			colR.prop(MtlWrapper, 'gi_amount')
			colR.prop(MtlWrapper, 'no_gi_on_other_mattes')

		split= layout.split()
		col= split.column()
		col.label(text="Miscellaneous")

		split= layout.split()
		col= split.column()
		col.prop(MtlWrapper, 'gi_surface_id')
		col.prop(MtlWrapper, 'trace_depth')
		if wide_ui:
			col= split.column()
		col.prop(MtlWrapper, 'matte_for_secondary_rays')


class VRAY_MP_render(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Render"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		vma= active_ma.vray
		return base_poll(__class__, context) and not (vma.type == 'EMIT' and vma.emitter_type == 'MESH') and not vma.type == 'VOL'

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		MtlRenderStats= ma.vray.MtlRenderStats
		self.layout.prop(MtlRenderStats, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		ob= context.object
		ma= active_node_mat(context.material)

		VRayMaterial= ma.vray
		MtlRenderStats= VRayMaterial.MtlRenderStats

		layout= self.layout
		
		split= layout.split()
		col= split.column()
		col.prop(VRayMaterial, 'material_id_number')
		if wide_ui:
			col= split.column()
		else:
			col= col.column()
		col.active= VRayMaterial.material_id_number
		col.prop(VRayMaterial, 'material_id_color', text="")

		split= layout.split()
		split.active= MtlRenderStats.use
		col= split.column()
		col.prop(MtlRenderStats, 'visibility', text="Visible")

		split= layout.split()
		split.active= MtlRenderStats.use
		col= split.column()
		col.label(text="Visible to:")

		split= layout.split()
		split.active= MtlRenderStats.use
		sub= split.column()
		sub.active= MtlRenderStats.visibility
		sub.prop(MtlRenderStats, 'camera_visibility', text="Camera")
		sub.prop(MtlRenderStats, 'gi_visibility', text="GI")
		sub.prop(MtlRenderStats, 'shadows_visibility', text="Shadows")
		if wide_ui:
			sub= split.column()
			sub.active= MtlRenderStats.visibility
		sub.prop(MtlRenderStats, 'reflections_visibility', text="Reflections")
		sub.prop(MtlRenderStats, 'refractions_visibility', text="Refractions")


class VRAY_MP_outline(VRayMaterialPanel, bpy.types.Panel):
	bl_label   = "Outline"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		active_ma= active_node_mat(context.material)
		if active_ma is None:
			return False
		return base_poll(__class__, context)

	def draw_header(self, context):
		ma= active_node_mat(context.material)
		VRayMaterial= ma.vray
		VolumeVRayToon= VRayMaterial.VolumeVRayToon
		self.layout.prop(VolumeVRayToon, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200
		layout= self.layout

		ob= context.object
		ma= active_node_mat(context.material)

		VRayMaterial= ma.vray
		VolumeVRayToon= VRayMaterial.VolumeVRayToon

		layout.active= VolumeVRayToon.use

		PLUGINS['SETTINGS']['SettingsEnvironment'].draw_VolumeVRayToon(context, layout, VRayMaterial)

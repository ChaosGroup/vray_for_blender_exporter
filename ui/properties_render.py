'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Monday, 14 March 2011 [14:35]"

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
from vb25.utils import *
from vb25.ui.ui import *
from vb25.plugins import *
	

class VRAY_MT_preset_IM(bpy.types.Menu):
	bl_label= "Irradiance Map Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "im")
	preset_operator= "script.execute_preset"
	draw= bpy.types.Menu.draw_preset


class VRAY_MT_preset_global(bpy.types.Menu):
	bl_label= "V-Ray Global Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "render")
	preset_operator= "script.execute_preset"
	draw= bpy.types.Menu.draw_preset


class VRAY_RP_dimensions(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Dimensions"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		scene= context.scene
		rd=    scene.render
		VRayScene= scene.vray
		
		if VRayScene.image_aspect_lock:
			rd.resolution_y= rd.resolution_x / VRayScene.image_aspect

		row = layout.row(align=True)
		row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
		row.operator("render.preset_add", text="", icon="ZOOMIN")
		row.operator("render.preset_add", text="", icon="ZOOMOUT").remove_active = True

		layout.label(text="Resolution:")
		
		split= layout.split()
		col= split.column()
		sub= col.column(align=True)
		sub.prop(rd, "resolution_x", text="X")
		sub_aspect= sub.column()
		sub_aspect.active= not VRayScene.image_aspect_lock
		sub_aspect.prop(rd, "resolution_y", text="Y")
		sub.operator("vray.flip_resolution", text="", icon="FILE_REFRESH")
		sub.prop(rd, "resolution_percentage", text="")

		row= col.row()
		row.prop(rd, "use_border", text="Border")
		sub= row.row()
		sub.active = rd.use_border
		sub.prop(rd, "use_crop_to_border", text="Crop")

		if wide_ui:
			col= split.column()

		sub = col.column(align=True)
		sub.prop(VRayScene, "image_aspect_lock", text="Image aspect")
		if VRayScene.image_aspect_lock:
			sub.prop(VRayScene, "image_aspect")
		sub.label(text="Pixel aspect:")
		sub.prop(rd, "pixel_aspect_x", text="X")
		sub.prop(rd, "pixel_aspect_y", text="Y")

		split= layout.split()
		col = split.column()
		sub = col.column(align=True)
		sub.label(text="Frame Range:")
		sub.prop(scene, "frame_start", text="Start")
		sub.prop(scene, "frame_end", text="End")
		sub.prop(scene, "frame_step", text="Step")

		if wide_ui:
			col= split.column()

		sub = col.column(align=True)
		sub.label(text="Frame Rate:")
		sub.prop(rd, "fps")
		sub.prop(rd, "fps_base", text="/")
		subrow = sub.row(align=True)
		subrow.prop(rd, "frame_map_old", text="Old")
		subrow.prop(rd, "frame_map_new", text="New")


class VRAY_RP_output(VRayRenderPanel, bpy.types.Panel):
	bl_label	   = "Output"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw_header(self, context):
		VRayExporter= context.scene.vray.exporter
		self.layout.prop(VRayExporter, 'auto_save_render', text="")

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		scene= context.scene
		rd=    scene.render

		file_format = rd.file_format

		VRayScene= scene.vray
		VRayExporter=   VRayScene.exporter
		SettingsOutput= VRayScene.SettingsOutput

		layout.active= VRayExporter.auto_save_render

		if wide_ui:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.label(text="Path:")
			col.label(text="Filename:")
			col= split.column()
			col.prop(SettingsOutput, 'img_dir',  text="")
			col.prop(SettingsOutput, 'img_file', text="")
		else:
			layout.prop(SettingsOutput, 'img_dir',  text="")
			layout.prop(SettingsOutput, 'img_file', text="")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(rd, 'file_format', text= "Format")

		split= layout.split()
		col= split.column()

		if file_format == 'JPEG':
			col.prop(rd, 'file_quality', slider= True)

		elif file_format == 'PNG':
			col.prop(rd, 'file_quality', slider= True, text= "Compression")

		elif file_format == 'TIFF':
			col.prop(rd, 'use_tiff_16bit')

		elif file_format in {'OPEN_EXR', 'MULTILAYER'}:
			row= col.row()
			row.prop(rd, 'exr_codec')

			if file_format == 'OPEN_EXR':
				row.prop(rd, 'use_exr_half', text= "16 bit")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(SettingsOutput, 'img_noAlpha')
		col.prop(SettingsOutput, 'img_separateAlpha')
		col.prop(SettingsOutput, 'relements_separateFolders')
		if wide_ui:
			col = split.column()
		col.prop(SettingsOutput, 'img_file_needFrameNumber')
		col.prop(VRayExporter, 'image_to_blender')
		sub= col.column()
		sub.active= False
		sub.prop(rd, "use_overwrite")


class VRAY_RP_render(VRayRenderPanel, bpy.types.Panel):
	bl_label       = "Render"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		rd= context.scene.render
		vs= context.scene.vray
		ve= vs.exporter
		SettingsOptions= vs.SettingsOptions

		split= layout.split()
		col= split.column()
		if ve.animation:
			render_label= "Animation"
			render_icon= 'RENDER_ANIMATION'
		elif ve.camera_loop:
			render_label= "Cameras"
			render_icon= 'RENDER_ANIMATION'
		else:
			render_label= "Image"
			render_icon= 'RENDER_STILL'

		if ve.use_render_operator:
			col.operator('render.render', text= render_label, icon= render_icon)
		else:
			col.operator('vray.render', text= render_label, icon= render_icon)

		if not ve.auto_meshes:
			if wide_ui:
				col= split.column()
			col.operator('vray.write_geometry', icon='OUTLINER_OB_MESH')

		split= layout.split()
		col= split.column()
		col.label(text="Modules:")
		col.prop(vs.SettingsGI, 'on', text="Global Illumination")
		col.prop(vs.SettingsCaustics, 'on', text="Caustics")
		col.prop(ve, 'use_displace', text= "Displace")
		col.prop(vs.VRayDR, 'on')
		col.prop(vs.VRayBake, 'use')
		col.prop(vs.RTEngine, 'enabled')
		if wide_ui:
			col= split.column()
		col.label(text="Pipeline:")
		col.prop(ve, 'animation')
		if not ve.animation:
			col.prop(ve, 'camera_loop')
		col.prop(ve, 'active_layers')
		if vs.SettingsGI.on:
			col.prop(SettingsOptions, 'gi_dontRenderImage')
		col.label(text="Options:")
		col.prop(ve, 'use_material_nodes')


class VRAY_RP_SettingsOptions(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "Globals"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray
		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		split= layout.split()
		col= split.column()
		col.label(text="Geometry:")
		col.prop(SettingsOptions, 'geom_doHidden')
		col.prop(SettingsOptions, 'geom_backfaceCull')
		col.prop(SettingsOptions, 'ray_bias', text="Secondary bias")
		if wide_ui:
			col= split.column()
		col.label(text="Lights:")
		col.prop(SettingsOptions, 'light_doLights')
		# col.prop(SettingsOptions, 'light_doDefaultLights')
		col.prop(SettingsOptions, 'light_doHiddenLights')
		col.prop(SettingsOptions, 'light_doShadows')
		col.prop(SettingsOptions, 'light_onlyGI')

		layout.label(text="Materials:")
		split= layout.split()
		col= split.column()
		col.prop(SettingsOptions, 'mtl_override_on')
		if SettingsOptions.mtl_override_on:
			col.prop_search(SettingsOptions, 'mtl_override', bpy.data, 'materials', text="")
		col.prop(SettingsOptions, 'mtl_doMaps')
		if SettingsOptions.mtl_doMaps:
			col.prop(SettingsOptions, 'mtl_filterMaps')
			col.prop(SettingsOptions, 'mtl_filterMapsForSecondaryRays')
		if wide_ui:
			col= split.column()
		col.prop(SettingsOptions, 'mtl_reflectionRefraction')
		if SettingsOptions.mtl_reflectionRefraction:
			col.prop(SettingsOptions, 'mtl_limitDepth')
			if SettingsOptions.mtl_limitDepth:
				col.prop(SettingsOptions, 'mtl_maxDepth')
		col.prop(SettingsOptions, 'mtl_glossy')

		split= layout.split()
		col= split.column()
		col.prop(SettingsOptions, 'mtl_transpMaxLevels')
		if wide_ui:
			col= split.column()
		col.prop(SettingsOptions, 'mtl_transpCutoff')


class VRAY_RP_exporter(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "Exporter"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		rd= context.scene.render
		ve= context.scene.vray.exporter

		row= layout.row(align=True)
		row.menu("VRAY_MT_preset_global", text=bpy.types.VRAY_MT_preset_global.bl_label)
		row.operator("vray.preset_add", text="", icon="ZOOMIN")
		row.operator("vray.preset_add", text="", icon="ZOOMOUT").remove_active = True

		layout.separator()

		split= layout.split()
		col= split.column()
		col.label(text="Options:")
		col.prop(ve, 'autorun')
		col.prop(ve, 'auto_meshes')
		col.prop(ve, 'use_render_operator')
		col.prop(ve, 'display')
		col.prop(ve, 'debug')
		if wide_ui:
			col= split.column()
		col.label(text="Mesh export:")
		col.prop(ve, 'mesh_active_layers', text= "Active layers")
		# col.prop(ve, 'check_animated')
		col.prop(ve, 'use_instances')
		# col.prop(SettingsOptions, 'geom_displacement')
		col.prop(ve, 'use_hair')
		col.prop(ve, 'mesh_debug')
		
		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(ve, 'detect_vray')
		if not ve.detect_vray:
			split= layout.split()
			col= split.column()
			col.prop(ve, 'vray_binary')
		split= layout.split()
		col= split.column()
		# col.prop(ve, 'detach', text="Detach process")
		if PLATFORM == "linux2":
			col.prop(ve, 'log_window')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(ve, 'output', text="Export to")
		if ve.output == 'USER':
			col.prop(ve, 'output_dir')
		col.prop(ve, 'output_unique')


class VRAY_RP_cm(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Color mapping"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		cm= vs.SettingsColorMapping

		split= layout.split()
		col= split.column()
		col.prop(cm, 'type')
		if cm.type == 'REIN':
			col.prop(cm, "dark_mult", text="Multiplier")
			col.prop(cm, "bright_mult",  text="Burn")
		elif cm.type in ('GCOR', 'GINT'):
			col.prop(cm, "bright_mult", text="Multiplier")
			col.prop(cm, "dark_mult", text="Inverse gamma")
		else:
			col.prop(cm, "bright_mult")
			col.prop(cm, "dark_mult")
		col.prop(cm, "gamma")
		col.prop(cm, "input_gamma")
		if wide_ui:
			col= split.column()
		col.prop(cm, "affect_background")
		col.prop(cm, "subpixel_mapping")
		col.prop(cm, "adaptation_only")
		col.prop(cm, "linearWorkflow")
		col.prop(cm, "clamp_output")
		if cm.clamp_output:
			col.prop(cm, "clamp_level")


class VRAY_RP_aa(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Image sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		module= vs.SettingsImageSampler

		split= layout.split()
		col= split.column()
		col.prop(module, "type")

		split= layout.split()
		col= split.column()
		col.label(text="Parameters:")

		split= layout.split()
		col= split.column()
		if module.type == 'FXD':
			col.prop(module, "fixed_subdivs")
		elif module.type == 'DMC':
			col.prop(module, "dmc_minSubdivs")
			col.prop(module, "dmc_maxSubdivs")

			if wide_ui:
				col= split.column()
			col.prop(module, "dmc_treshhold_use_dmc", text= "Use DMC sampler thresh.")
			if not module.dmc_treshhold_use_dmc:
				col.prop(module, "dmc_threshold")
			col.prop(module, "dmc_show_samples")
		else:
			col.prop(module, "subdivision_minRate")
			col.prop(module, "subdivision_maxRate")
			col.prop(module, "subdivision_threshold")

			if wide_ui:
				col= split.column()
			col= split.column()
			col.prop(module, "subdivision_edges")
			col.prop(module, "subdivision_normals")
			if module.subdivision_normals:
				col.prop(module, "subdivision_normals_threshold")
			col.prop(module, "subdivision_jitter")
			col.prop(module, "subdivision_show_samples")

		split= layout.split()
		col= split.column()
		col.label(text="Filter type:")
		if wide_ui:
			col= split.column()
		col.prop(module, "filter_type", text="")
		if not module.filter_type == 'NONE':
			col.prop(module, "filter_size")


class VRAY_RP_dmc(VRayRenderPanel, bpy.types.Panel):
	bl_label = "DMC sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		module= vs.SettingsDMCSampler

		split= layout.split()
		col= split.column()
		col.prop(module, "adaptive_threshold")
		col.prop(module, "subdivs_mult")
		col.prop(module, "time_dependent")

		if wide_ui:
			col= split.column()
		col.prop(module, "adaptive_amount")
		col.prop(module, "adaptive_min_samples")


class VRAY_RP_gi(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Global Illumination"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		SettingsGI= context.scene.vray.SettingsGI
		return super().poll(context) and SettingsGI.on

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		module= vs.SettingsGI

		# split= layout.split()
		# col= split.column()
		# col.prop(module,'preset')
		
		# layout.separator()

		split= layout.split()
		col= split.column()
		col.label(text="GI caustics:")
		sub= col.column()
		sub.prop(module, "reflect_caustics", text="Reflect")
		sub.prop(module, "refract_caustics", text="Refract")
		if wide_ui:
			col= split.column()
		col.label(text="Post-processing:")
		sub= col.column()
		sub.prop(module, "saturation")
		sub.prop(module, "contrast")
		sub.prop(module, "contrast_base")

		layout.label(text="Primary engine:")
		if wide_ui:
			split= layout.split(percentage=0.35)
		else:
			split= layout.split()
		col= split.column()
		col.prop(module, "primary_multiplier", text="Mult")
		if wide_ui:
			col= split.column()
		col.prop(module, "primary_engine", text="")

		layout.label(text="Secondary engine:")
		if wide_ui:
			split= layout.split(percentage=0.35)
		else:
			split= layout.split()
		col= split.column()
		col.prop(module, "secondary_multiplier", text="Mult")
		if wide_ui:
			col= split.column()
		col.prop(module, "secondary_engine", text="")


class VRAY_RP_GI_im(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Irradiance Map"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return engine_poll(__class__, context) and module.on and module.primary_engine == 'IM'

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		gi= vs.SettingsGI
		module= gi.SettingsIrradianceMap

		split= layout.split()
		colR= split.column()
		colR.prop(module, "mode", text="Mode")

		if module.mode not in ('FILE', 'ANIM_REND'):
			split= layout.split()
			col= split.column()
			col.label(text="Preset:")
			if wide_ui:
				col= split.column()
			col.menu('VRAY_MT_preset_IM', text="Preset")

			split= layout.split()
			split.label(text="Basic parameters:")

			split= layout.split()
			col= split.column(align=True)
			col.prop(module,"min_rate")
			col.prop(module,"max_rate")
			col.prop(module,"subdivs", text= "HSph. subdivs")
			if wide_ui:
				col= split.column(align=True)
			else:
				split= layout.split()
				col= split.column(align=True)
			col.prop(module,"color_threshold", text="Clr thresh", slider=True)
			col.prop(module,"normal_threshold", text="Nrm thresh", slider=True)
			col.prop(module,"distance_threshold", text="Dist thresh", slider=True)

			split= layout.split()
			split.column().prop(module,"interp_samples", text= "Interp. samples")
			if wide_ui:
				split.column()

			split= layout.split()
			split.label(text="Advanced parameters:")

			if wide_ui:
				split= layout.split(percentage=0.7)
			else:
				split= layout.split()
			col= split.column()
			col.prop(module,"interpolation_mode", text="Interp. type")
			col.prop(module,"lookup_mode")
			col.prop(module,"calc_interp_samples")
			if wide_ui:
				col= split.column()
			col.prop(module,"multipass")
			col.prop(module,"randomize_samples", text="Randomize")
			col.prop(module,"check_sample_visibility", text="Check sample")

		elif module.mode == 'ANIM_REND':
			split= layout.split()
			split.label(text="Basic parameters:")

			split= layout.split()
			colL= split.column()
			colL.prop(module,"interp_frames")

		split= layout.split()
		split.label(text="Detail enhancement:")

		split= layout.split(percentage=0.12)
		split.column().prop(module, "detail_enhancement", text="On")
		sub= split.column().row()
		sub.active= module.detail_enhancement
		sub.prop(module, "detail_radius", text="R")
		sub.prop(module, "detail_subdivs_mult", text="Subdivs", slider=True)
		sub.prop(module, "detail_scale", text="")

		if module.mode not in ('FILE', 'ANIM_REND'):
			split= layout.split()
			split.label(text="Options:")
			row= layout.split().row()
			row.prop(module,"show_calc_phase")
			sub= row.column().row()
			sub.active= module.show_calc_phase
			sub.prop(module,"show_direct_light")
			sub.prop(module,"show_samples")
			sub.prop(module,"multiple_views", text="Camera path")

		split= layout.split()
		split.label(text="Files:")
		split= layout.split(percentage=0.25)
		colL= split.column()
		colR= split.column()
		if module.mode in ('FILE', 'ANIM_REND'):
			colL.label(text="Map file name:")
			colR.prop(module,"file", text="")
		else:
			colL.prop(module,"auto_save", text="Auto save")
			colR.active= module.auto_save
			colR.prop(module,"auto_save_file", text="")


class VRAY_RP_GI_bf(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Brute Force"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return engine_poll(__class__, context) and module.on and (module.primary_engine == 'BF' or module.secondary_engine == 'BF')

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vsce= context.scene.vray
		gi= vsce.SettingsGI
		module= gi.SettingsDMCGI

		split= layout.split()
		col= split.column()
		col.prop(module, "subdivs")
		if gi.secondary_engine == 'BF':
			if wide_ui:
				col= split.column()
			col.prop(module, "depth")


class VRAY_RP_GI_lc(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Light Cache"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return (engine_poll(__class__, context) and module.on and (module.primary_engine == 'LC' or module.secondary_engine == 'LC'))

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		module= vs.SettingsGI.SettingsLightCache

		split= layout.split()
		col= split.column()
		col.prop(module, "mode", text="Mode")

		if not module.mode == 'FILE':
			layout.label(text="Calculation parameters:")
			if wide_ui:
				split= layout.split(percentage=0.6)
			else:
				split= layout.split()
			col= split.column()
			col.prop(module, "subdivs")
			col.prop(module, "sample_size")
			col.prop(module, "world_scale", text="Sample scale")
			if not module.num_passes_auto:
				col.prop(module, "num_passes")
			col.prop(module, "depth", slider= True)
			
			if wide_ui:
				col= split.column()
			col.prop(module, "store_direct_light")
			col.prop(module, "adaptive_sampling")
			col.prop(module, "show_calc_phase")
			col.prop(module, "num_passes_auto")

		layout.label(text="Reconstruction parameters:")
		if not module.mode == 'FILE':
			split= layout.split(percentage=0.2)
			split.column().prop(module, "filter")
			sub= split.column().row()
			sub.active= module.filter
			sub.prop(module, "filter_type", text="Type")
			if module.filter_type != 'NONE':
				if module.filter_type == 'NEAREST':
					sub.prop(module, "filter_samples")
				else:
					sub.prop(module, "filter_size")
			else:
				sub.label(text="")

		split= layout.split(percentage=0.2)
		split.column().prop(module, "prefilter")
		colR= split.column()
		colR.active= module.prefilter
		colR.prop(module, "prefilter_samples")

		split= layout.split()
		split= layout.split()
		col= split.column()
		col.prop(module, "use_for_glossy_rays")
		col.prop(module, "multiple_views")
		if wide_ui:
			col= split.column()
		col.prop(module, "retrace_enabled")
		sub= col.column()
		sub.active= module.retrace_enabled
		sub.prop(module, "retrace_threshold", text="Retrace thresh.")

		split= layout.split()
		split.label(text="Files:")
		split= layout.split(percentage=0.25)
		colL= split.column()
		colR= split.column()
		if module.mode == 'FILE':
			colL.label(text="Map file name:")
			colR.prop(module,"file", text="")
		else:
			colL.prop(module,"auto_save", text="Auto save")
			colR.active= module.auto_save
			colR.prop(module,"auto_save_file", text="")


class VRAY_RP_Layers(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "Channels"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return engine_poll(__class__, context)

	def draw_header(self, context):
		VRayScene= context.scene.vray
		self.layout.prop(VRayScene, 'render_channels_use', text="")

	def draw(self, context):
		wide_ui = context.region.width > narrowui
		layout= self.layout
		
		sce= context.scene
		vsce= sce.vray
		render_channels= vsce.render_channels

		layout.active= vsce.render_channels_use

		row= layout.row()
		row.template_list(vsce, 'render_channels',
						  vsce, 'render_channels_index',
						  rows= 4)
		col= row.column()
		sub= col.row()
		subsub= sub.column(align=True)
		subsub.operator('vray.render_channels_add',	   text="", icon="ZOOMIN")
		subsub.operator('vray.render_channels_remove', text="", icon="ZOOMOUT")

		if vsce.render_channels_index >= 0 and len(render_channels) > 0:
			render_channel= render_channels[vsce.render_channels_index]
		
			layout.separator()

			if wide_ui:
				split= layout.split(percentage=0.2)
			else:
				split= layout.split()
			col= split.column()
			col.label(text="Name:")
			if wide_ui:
				col= split.column()
			row= col.row(align=True)
			row.prop(render_channel, 'name', text="")
			row.prop(render_channel, 'use', text="")

			if wide_ui:
				split= layout.split(percentage=0.2)
			else:
				split= layout.split()
			col= split.column()
			col.label(text="Type:")
			if wide_ui:
				col= split.column()
			col.prop(render_channel, 'type', text="")

			layout.separator()

			if render_channel.type != 'NONE':
				# Box border
				layout= layout.box()
				
				plugin= PLUGINS['RENDERCHANNEL'].get(render_channel.type)
				if plugin is not None:
					render_channel_data= getattr(render_channel,plugin.PLUG)

					if render_channel.name == "" or render_channel.name == "RenderChannel":
						def get_unique_name():
							for chan in render_channels:
								if render_channel_data.name == chan.name:
									return render_channel_data.name + " (enter unique name)"
							return render_channel_data.name
						render_channel.name= get_unique_name()
					
					plugin.draw(getattr(render_channel,plugin.PLUG), layout, wide_ui)


class VRAY_RP_displace(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Displacement"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		VRayExporter= context.scene.vray.exporter
		return engine_poll(__class__, context) and VRayExporter.use_displace

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray
		SettingsDefaultDisplacement= VRayScene.SettingsDefaultDisplacement

		split= layout.split()
		col= split.column()
		col.prop(SettingsDefaultDisplacement, 'override_on')

		split= layout.split()
		split.active= SettingsDefaultDisplacement.override_on
		col= split.column()
		col.prop(SettingsDefaultDisplacement, 'amount')
		col.prop(SettingsDefaultDisplacement, 'edgeLength')
		col.prop(SettingsDefaultDisplacement, 'maxSubdivs')
		if wide_ui:
			col= split.column()
		col.prop(SettingsDefaultDisplacement, 'viewDependent')
		col.prop(SettingsDefaultDisplacement, 'tightBounds')
		col.prop(SettingsDefaultDisplacement, 'relative')


class VRAY_RP_dr(VRayRenderPanel, bpy.types.Panel):
	bl_label = "Distributed rendering"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		vs= context.scene.vray
		module= vs.VRayDR
		return engine_poll(__class__, context) and module.on

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		module= vs.VRayDR

		split= layout.split()
		col= split.column()
		col.prop(module, 'shared_dir')

		split= layout.split()
		col= split.column()
		col.prop(module, 'type', text="Network type")

		layout.separator()

		split= layout.split()
		col= split.column()
		col.label(text="Port:")
		if wide_ui:
			col= split.column()
		col.prop(module, 'port', text="")
		
		layout.separator()

		split= layout.split()
		row= split.row()
		row.template_list(module, 'nodes', module, 'nodes_selected', rows= 3)
		col= row.column(align=True)
		col.operator('vray.render_nodes_add',    text="", icon="ZOOMIN")
		col.operator('vray.render_nodes_remove', text="", icon="ZOOMOUT")

		if module.nodes_selected >= 0 and len(module.nodes) > 0:
			render_node= module.nodes[module.nodes_selected]
		
			layout.separator()

			layout.prop(render_node, 'name')
			layout.prop(render_node, 'address')


class VRAY_RP_bake(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "Bake"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		VRayScene= context.scene.vray
		VRayBake= VRayScene.VRayBake
		return (engine_poll(__class__, context) and VRayBake.use)

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray
		VRayBake= VRayScene.VRayBake

		layout= self.layout

		split= layout.split()
		col= split.column()
		col.prop_search(VRayBake, 'bake_node',  context.scene, 'objects')
		if wide_ui:
			col= split.column()
		col.prop(VRayBake, 'dilation')
		col.prop(VRayBake, 'flip_derivs')


class VRAY_RP_SettingsSystem(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "System"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return engine_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		rd= context.scene.render

		VRayScene= context.scene.vray
		SettingsRaycaster=        VRayScene.SettingsRaycaster
		SettingsUnitsInfo=        VRayScene.SettingsUnitsInfo
		SettingsRegionsGenerator= VRayScene.SettingsRegionsGenerator
		SettingsOptions=          VRayScene.SettingsOptions

		layout.label(text="Threads:")
		split= layout.split()
		col= split.column()
		col.row().prop(rd, "threads_mode", expand=True)
		if wide_ui:
			col= split.column(align=True)
		sub= col.column()
		sub.enabled= rd.threads_mode == 'FIXED'
		sub.prop(rd, 'threads', text="Count")

		layout.separator()

		layout.label(text="Raycaster parameters:")
		split= layout.split()
		col= split.column()
		col.prop(SettingsRaycaster, 'maxLevels')
		col.prop(SettingsRaycaster, 'minLeafSize')
		if wide_ui:
			col= split.column()
		col.prop(SettingsRaycaster, 'faceLevelCoef')
		col.prop(SettingsOptions, 'misc_lowThreadPriority')
		split= layout.split()
		col= split.column()
		col.prop(SettingsRaycaster, 'dynMemLimit')

		# layout.separator()

		# layout.label(text="Units scale:")
		# split= layout.split()
		# col= split.column()
		# col.prop(SettingsUnitsInfo, 'meters_scale', text="Metric")
		# if wide_ui:
		# 	col= split.column()
		# col.prop(SettingsUnitsInfo, 'photometric_scale', text="Photometric")

		layout.separator()

		layout.label(text="Render region division:")
		split= layout.split()
		col= split.column()
		col.prop(SettingsRegionsGenerator, 'xymeans', text="XY")
		col.prop(SettingsRegionsGenerator, 'seqtype')
		col.prop(SettingsRegionsGenerator, 'reverse')
		if wide_ui:
			col= split.column()
		sub= col.row(align=True)
		sub.prop(SettingsRegionsGenerator, 'xc')
		sub= sub.column()
		sub.active= not SettingsRegionsGenerator.lock_size
		sub.prop(SettingsRegionsGenerator, 'yc')
		col.prop(SettingsRegionsGenerator, 'lock_size')


class VRAY_RP_about(VRayRenderPanel, bpy.types.Panel):
	bl_label   = "About"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return engine_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		split= layout.split()
		col= split.column()
		col.label(text="V-Ray/Blender 2.5 (git)")
		col.separator()
		col.label(text="Author: Andrey M. Izrantsev")
		col.label(text="URL: http://vray.cgdo.ru")
		col.label(text="Email: izrantsev@cgdo.ru")
		col.label(text="Jabber: izrantsev@gmail.com")
		col.separator()
		col.label(text="IRC: irc.freenode.net #vrayblender")
		col.separator()
		col.label(text="V-Ray(R) is a registered trademark of Chaos Group Ltd.")

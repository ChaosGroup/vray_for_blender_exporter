#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import os
import sys

import bpy

from vb30.lib import LibUtils
from vb30.ui  import classes
from vb30     import plugins, preset


########  #### ##     ## ######## ##    ##  ######  ####  #######  ##    ##  ######
##     ##  ##  ###   ### ##       ###   ## ##    ##  ##  ##     ## ###   ## ##    ##
##     ##  ##  #### #### ##       ####  ## ##        ##  ##     ## ####  ## ##
##     ##  ##  ## ### ## ######   ## ## ##  ######   ##  ##     ## ## ## ##  ######
##     ##  ##  ##     ## ##       ##  ####       ##  ##  ##     ## ##  ####       ##
##     ##  ##  ##     ## ##       ##   ### ##    ##  ##  ##     ## ##   ### ##    ##
########  #### ##     ## ######## ##    ##  ######  ####  #######  ##    ##  ######

class VRAY_RP_dimensions(classes.VRayRenderPanel):
	bl_label = "Dimensions"

	def draw(self, context):
		layout = self.layout
		wide_ui = context.region.width > classes.narrowui

		scene = context.scene
		rd    = scene.render

		VRayScene = scene.vray
		VRayExporter = VRayScene.Exporter

		row = layout.row(align=True)
		row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
		row.operator("render.preset_add", text="", icon="ZOOMIN")
		row.operator("render.preset_add", text="", icon="ZOOMOUT").remove_active= True

		split = layout.split()
		col = split.column(align=True)
		col.label(text="Resolution:")
		col.prop(rd, "resolution_x", text="X")
		col.prop(rd, "resolution_y", text="Y")
		col.operator("vray.flip_resolution", text="", icon="FILE_REFRESH")
		col.prop(rd, "resolution_percentage", text="")

		row = col.row()
		row.prop(rd, "use_border", text="Border")
		row.prop(rd, "use_crop_to_border", text="Crop")

		col = split.column(align=True)
		col.label(text="Pixel aspect:")
		col.prop(rd, "pixel_aspect_x", text="X")
		col.prop(rd, "pixel_aspect_y", text="Y")

		split = layout.split()
		sub = split.column(align=True)
		sub.label(text="Frame Range:")
		sub.prop(scene, "frame_start", text="Start")
		sub.prop(scene, "frame_end", text="End")
		sub.prop(scene, "frame_step", text="Step")
		sub = split.column(align=True)
		sub.label(text="Frame Rate:")
		sub.prop(rd, "fps")
		sub.prop(rd, "fps_base", text="/")
		subrow = sub.row(align=True)
		subrow.prop(rd, "frame_map_old", text="Old")
		subrow.prop(rd, "frame_map_new", text="New")


 #######  ##     ## ######## ########  ##     ## ########
##     ## ##     ##    ##    ##     ## ##     ##    ##
##     ## ##     ##    ##    ##     ## ##     ##    ##
##     ## ##     ##    ##    ########  ##     ##    ##
##     ## ##     ##    ##    ##        ##     ##    ##
##     ## ##     ##    ##    ##        ##     ##    ##
 #######   #######     ##    ##         #######     ##

class VRAY_RP_output(classes.VRayRenderPanel):
	bl_label = "Output"

	def draw_header(self, context):
		VRayExporter= context.scene.vray.Exporter
		self.layout.prop(VRayExporter, 'auto_save_render', text="")

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		scene = context.scene
		rd    = scene.render.image_settings

		VRayScene      = scene.vray
		VRayExporter   = VRayScene.Exporter
		SettingsOutput = VRayScene.SettingsOutput

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
		col.prop(SettingsOutput, 'img_format', text="Format")

		formatPropGroupName = LibUtils.FormatToSettings[SettingsOutput.img_format]

		imgFormatPropGroup = getattr(VRayScene, formatPropGroupName)

		classes.DrawPluginUIAuto(context, layout, imgFormatPropGroup, formatPropGroupName)

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(SettingsOutput, 'img_noAlpha')
		col.prop(SettingsOutput, 'img_separateAlpha')
		col.prop(SettingsOutput, 'relements_separateFolders')
		if wide_ui:
			col = split.column()
		col.prop(SettingsOutput, 'img_file_needFrameNumber')
		if VRayExporter.animation_mode == 'NONE':
			col.prop(VRayExporter, 'image_to_blender')


########  ######## ##    ## ########  ######## ########
##     ## ##       ###   ## ##     ## ##       ##     ##
##     ## ##       ####  ## ##     ## ##       ##     ##
########  ######   ## ## ## ##     ## ######   ########
##   ##   ##       ##  #### ##     ## ##       ##   ##
##    ##  ##       ##   ### ##     ## ##       ##    ##
##     ## ######## ##    ## ########  ######## ##     ##

class VRAY_RP_render(classes.VRayRenderPanel):
	bl_label = "Render"

	def draw(self, context):
		layout = self.layout
		wide_ui = context.region.width > classes.narrowui

		rd = context.scene.render

		VRayScene = context.scene.vray
		VRayExporter    = VRayScene.Exporter
		SettingsOptions = VRayScene.SettingsOptions

		render_icon = 'RENDER_ANIMATION'
		if VRayExporter.animation_mode == 'NONE':
			render_icon = 'RENDER_STILL'
		elif VRayExporter.animation_mode == 'CAMERA_LOOP':
			render_icon = 'CAMERA_DATA'

		split = layout.split()
		row = split.row(align=True)
		row.operator('render.render', text="Render", icon=render_icon)
		row.prop(rd, "use_lock_interface", text="")

		layout.prop(VRayExporter, 'animation_mode', text="Animation")
		layout.separator()

		if VRayExporter.useSeparateFiles:
			layout.prop(VRayExporter, 'auto_meshes', text="Re-Export Meshes")

		split= layout.split()
		col= split.column()
		col.label(text="Modules:")
		col.prop(VRayScene.SettingsGI, 'on', text="Global Illumination")
		col.prop(VRayScene.SettingsCaustics, 'on', text="Caustics")
		col.prop(VRayExporter, 'use_displace')
		col.prop(VRayScene.VRayDR, 'on')
		col.prop(VRayScene.BakeView, 'use', text="Bake")
		col.prop(VRayScene.RTEngine, 'enabled', text="Realtime Engine")
		col.prop(VRayScene.VRayStereoscopicSettings, 'use')
		if wide_ui:
			col= split.column()
		col.label(text="Pipeline:")
		col.prop(VRayExporter, 'activeLayers', text="")
		if VRayExporter.activeLayers == 'CUSTOM':
			col.prop(VRayExporter, 'customRenderLayers', text="")
		col.prop(SettingsOptions, 'gi_dontRenderImage')
		col.prop(VRayExporter, 'draft')

		layout.separator()
		layout.prop(rd, "display_mode")


########  ########    ###    ##       ######## #### ##     ## ########
##     ## ##         ## ##   ##          ##     ##  ###   ### ##
##     ## ##        ##   ##  ##          ##     ##  #### #### ##
########  ######   ##     ## ##          ##     ##  ## ### ## ######
##   ##   ##       ######### ##          ##     ##  ##     ## ##
##    ##  ##       ##     ## ##          ##     ##  ##     ## ##
##     ## ######## ##     ## ########    ##    #### ##     ## ########

class VRAY_RP_RTEngine(classes.VRayRenderPanel):
	bl_label = "Realtime Engine"

	@classmethod
	def poll(cls, context):
		rtengineOn     = context.scene.vray.RTEngine.enabled
		rtengineChosen = context.scene.render.engine == 'VRAY_RENDER_RT'

		useRTEgine = rtengineOn or rtengineChosen

		return useRTEgine and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		VRayScene = context.scene.vray

		classes.DrawPluginUIAuto(context, self.layout, VRayScene.RTEngine, 'RTEngine')

		self.layout.separator()

		classes.DrawPluginUIAuto(context, self.layout, VRayScene.SettingsRTEngine, 'SettingsRTEngine')


 ######  ######## ######## ########  ########  #######   ######   ######   #######  ########  ####  ######
##    ##    ##    ##       ##     ## ##       ##     ## ##    ## ##    ## ##     ## ##     ##  ##  ##    ##
##          ##    ##       ##     ## ##       ##     ## ##       ##       ##     ## ##     ##  ##  ##
 ######     ##    ######   ########  ######   ##     ##  ######  ##       ##     ## ########   ##  ##
      ##    ##    ##       ##   ##   ##       ##     ##       ## ##       ##     ## ##         ##  ##
##    ##    ##    ##       ##    ##  ##       ##     ## ##    ## ##    ## ##     ## ##         ##  ##    ##
 ######     ##    ######## ##     ## ########  #######   ######   ######   #######  ##        ####  ######

class VRAY_RP_VRayStereoscopicSettings(classes.VRayRenderPanel):
	bl_label = "Stereoscopic"

	@classmethod
	def poll(cls, context):
		VRayStereoscopicSettings = context.scene.vray.VRayStereoscopicSettings
		return VRayStereoscopicSettings.use and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui
		layout= self.layout

		VRayScene= context.scene.vray
		VRayStereoscopicSettings= VRayScene.VRayStereoscopicSettings

		split = layout.split()
		col   = split.column()
		col.prop(VRayStereoscopicSettings, 'eye_distance')

		sub = col.row(align=True)
		sub_f = sub.column()
		sub_f.active = VRayStereoscopicSettings.specify_focus
		sub_f.prop(VRayStereoscopicSettings, 'focus_distance')
		sub.prop(VRayStereoscopicSettings, 'specify_focus', text="")

		split = layout.split()
		col   = split.column()
		col.prop(VRayStereoscopicSettings, 'focus_method', text="Focus")
		col.prop(VRayStereoscopicSettings, 'interocular_method', text="Interocular")
		col.prop(VRayStereoscopicSettings, 'view')
		col.prop(VRayStereoscopicSettings, 'adjust_resolution')

		# NOTE: Shademap is currently broken
		# layout.separator()
		# layout.prop(VRayStereoscopicSettings, 'sm_mode', text="Mode")
		# sub = layout.row()
		# sub.active = VRayStereoscopicSettings.sm_mode != '0'
		# sub.prop(VRayStereoscopicSettings, 'shademap_file', text="Shademap")
		# layout.prop(VRayStereoscopicSettings, 'reuse_threshold')

		#layout.separator()
		#layout.prop(VRayStereoscopicSettings, 'exclude_list')


 ######   ##        #######  ########     ###    ##        ######
##    ##  ##       ##     ## ##     ##   ## ##   ##       ##    ##
##        ##       ##     ## ##     ##  ##   ##  ##       ##
##   #### ##       ##     ## ########  ##     ## ##        ######
##    ##  ##       ##     ## ##     ## ######### ##             ##
##    ##  ##       ##     ## ##     ## ##     ## ##       ##    ##
 ######   ########  #######  ########  ##     ## ########  ######

class VRAY_RP_Globals(classes.VRayRenderPanel):
	bl_label   = "Globals"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		VRayScene= context.scene.vray
		VRayExporter=    VRayScene.Exporter
		SettingsOptions= VRayScene.SettingsOptions

		split= layout.split()
		col= split.column()
		col.label(text="Geometry:")
		# col.prop(SettingsOptions, 'geom_doHidden')
		col.prop(SettingsOptions, 'geom_backfaceCull')
		col.prop(SettingsOptions, 'ray_bias')
		if wide_ui:
			col= split.column()
		col.label(text="Lighting:")
		col.prop(SettingsOptions, 'light_doLights')
		col.prop(SettingsOptions, 'light_doDefaultLights')
		col.prop(SettingsOptions, 'light_disableSelfIllumination')
		col.prop(SettingsOptions, 'light_doHiddenLights')
		col.prop(SettingsOptions, 'light_doShadows')
		col.prop(SettingsOptions, 'light_onlyGI')

		layout.label(text="GI:")
		split= layout.split()
		col= split.column()
		col.prop(SettingsOptions, 'ray_max_intensity_on')
		if wide_ui:
			col= split.column()
		sub = col.column()
		sub.active = SettingsOptions.ray_max_intensity_on
		sub.prop(SettingsOptions, 'ray_max_intensity', text="")
		layout.prop(SettingsOptions, 'gi_texFilteringMultiplier')

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
		col.prop(SettingsOptions, 'mtl_uninvertedNormalBump')

		split= layout.split()
		col= split.column()
		col.prop(SettingsOptions, 'mtl_transpMaxLevels')
		if wide_ui:
			col= split.column()
		col.prop(SettingsOptions, 'mtl_transpCutoff')


######## ##     ## ########   #######  ########  ######## ######## ########
##        ##   ##  ##     ## ##     ## ##     ##    ##    ##       ##     ##
##         ## ##   ##     ## ##     ## ##     ##    ##    ##       ##     ##
######      ###    ########  ##     ## ########     ##    ######   ########
##         ## ##   ##        ##     ## ##   ##      ##    ##       ##   ##
##        ##   ##  ##        ##     ## ##    ##     ##    ##       ##    ##
######## ##     ## ##         #######  ##     ##    ##    ######## ##     ##

class VRAY_RP_exporter(classes.VRayRenderPanel):
	bl_label   = "Exporter"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		VRayScene      = context.scene.vray
		VRayExporter   = VRayScene.Exporter
		SettingsOutput = VRayScene.SettingsOutput

		preset.GlobalPreset(layout)

		layout.label(text="Options:")
		split = layout.split()
		col = split.column()
		col.prop(VRayExporter, 'autorun')
		if wide_ui:
			col = split.column()
		col.prop(VRayExporter, 'use_smoke')
		col.prop(VRayExporter, 'use_hair')

		split = layout.split()
		col = split.column()
		sub = col.row()
		sub.active = VRayExporter.animation_mode in {'FRAMEBYFRAME', 'NONE'}
		sub.prop(VRayExporter, 'frames_to_export')

		layout.separator()
		layout.label(text="V-Ray Frame Buffer:")
		split = layout.split()
		col = split.column()
		col.prop(VRayExporter, 'display', text="Display")
		col.prop(VRayExporter, 'display_srgb', text="sRGB")
		if wide_ui:
			col = split.column()
		col.prop(VRayExporter, 'autoclose')

		layout.prop(SettingsOutput, 'frame_stamp_enabled', text="Frame Stamp")
		if SettingsOutput.frame_stamp_enabled:
			layout.prop(SettingsOutput, 'frame_stamp_text', text="")

		layout.separator()
		layout.label(text="Export:")
		split = layout.split()
		col = split.column()
		col.prop(VRayExporter, 'output', text="Directory")
		if VRayExporter.output == 'USER':
			col.prop(VRayExporter, 'output_dir')

		split = layout.split()
		col = split.column()
		col.prop(VRayExporter, 'useSeparateFiles')
		if wide_ui:
			col = split.column()
		col.prop(VRayExporter, 'output_unique', text="Unique Filename")

		layout.separator()
		layout.label(text="Advanced:")
		split = layout.split()
		col = split.column()
		col.prop(VRayExporter, 'debug')

		if sys.platform == "linux":
			split = layout.split()
			col = split.column()
			col.prop(VRayExporter, 'log_window')
			if VRayExporter.log_window:
				col.prop(VRayExporter, 'log_window_type', text="Terminal")
				if VRayExporter.log_window_type == 'CUSTOM':
					col.prop(VRayExporter, 'log_window_term')

		layout.separator()
		layout.operator('vray.update', icon='FILE_REFRESH')


 ######   #######  ##        #######  ########     ##     ##    ###    ########  ########  #### ##    ##  ######
##    ## ##     ## ##       ##     ## ##     ##    ###   ###   ## ##   ##     ## ##     ##  ##  ###   ## ##    ##
##       ##     ## ##       ##     ## ##     ##    #### ####  ##   ##  ##     ## ##     ##  ##  ####  ## ##
##       ##     ## ##       ##     ## ########     ## ### ## ##     ## ########  ########   ##  ## ## ## ##   ####
##       ##     ## ##       ##     ## ##   ##      ##     ## ######### ##        ##         ##  ##  #### ##    ##
##    ## ##     ## ##       ##     ## ##    ##     ##     ## ##     ## ##        ##         ##  ##   ### ##    ##
 ######   #######  ########  #######  ##     ##    ##     ## ##     ## ##        ##        #### ##    ##  ######

class VRAY_RP_cm(classes.VRayRenderPanel):
	bl_label = "Color Mapping"

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		cm= context.scene.vray.SettingsColorMapping

		split= layout.split()
		col= split.column()
		col.prop(cm, 'type')
		if cm.type == '6':
			col.prop(cm, "dark_mult",   text="Multiplier")
			col.prop(cm, "bright_mult", text="Burn")
		elif cm.type in {'4', '5'}:
			col.prop(cm, "bright_mult", text="Multiplier")
			col.prop(cm, "dark_mult",   text="Inverse Gamma")
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


#### ##     ##    ###     ######   ########     ######     ###    ##     ## ########  ##       ######## ########
 ##  ###   ###   ## ##   ##    ##  ##          ##    ##   ## ##   ###   ### ##     ## ##       ##       ##     ##
 ##  #### ####  ##   ##  ##        ##          ##        ##   ##  #### #### ##     ## ##       ##       ##     ##
 ##  ## ### ## ##     ## ##   #### ######       ######  ##     ## ## ### ## ########  ##       ######   ########
 ##  ##     ## ######### ##    ##  ##                ## ######### ##     ## ##        ##       ##       ##   ##
 ##  ##     ## ##     ## ##    ##  ##          ##    ## ##     ## ##     ## ##        ##       ##       ##    ##
#### ##     ## ##     ##  ######   ########     ######  ##     ## ##     ## ##        ######## ######## ##     ##

class VRAY_RP_aa(classes.VRayRenderPanel):
	bl_label = "Image Sampler"

	def draw(self, context):
		VRayScene = context.scene.vray
		SettingsImageSampler = VRayScene.SettingsImageSampler

		classes.DrawPluginUIAuto(context, self.layout, SettingsImageSampler, 'SettingsImageSampler')

		if SettingsImageSampler.type not in {'3'}:
			self.layout.separator()
			self.layout.prop(SettingsImageSampler, "filter_type")

			if SettingsImageSampler.filter_type not in {'NONE'}:
				filterPluginName = SettingsImageSampler.filter_type
				filterPropGroup  = getattr(VRayScene, filterPluginName)

				classes.DrawPluginUIAuto(context, self.layout, filterPropGroup, filterPluginName)


########  ##     ##  ######
##     ## ###   ### ##    ##
##     ## #### #### ##
##     ## ## ### ## ##
##     ## ##     ## ##
##     ## ##     ## ##    ##
########  ##     ##  ######

class VRAY_RP_dmc(classes.VRayRenderPanel):
	bl_label = "DMC Sampler"

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

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


 ######   ####
##    ##   ##
##         ##
##   ####  ##
##    ##   ##
##    ##   ##
 ######   ####

class VRAY_RP_gi(classes.VRayRenderPanel):
	bl_label = "Global Illumination"

	@classmethod
	def poll(cls, context):
		SettingsGI = context.scene.vray.SettingsGI
		return SettingsGI.on and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		VRayScene=  context.scene.vray
		SettingsGI= VRayScene.SettingsGI

		# row= layout.row(align=True)
		# row.menu("VRAY_MT_preset_gi", text=bpy.types.VRAY_MT_preset_gi.bl_label)
		# row.operator("vray.preset_gi_add", text="", icon="ZOOMIN")
		# row.operator("vray.preset_gi_add", text="", icon="ZOOMOUT").remove_active = True

		# layout.separator()

		split= layout.split()
		col= split.column()
		col.label(text="GI caustics:")
		sub= col.column()
		sub.prop(SettingsGI, "reflect_caustics", text="Reflect")
		sub.prop(SettingsGI, "refract_caustics", text="Refract")
		if wide_ui:
			col= split.column()
		col.label(text="Post-processing:")
		sub= col.column()
		sub.prop(SettingsGI, "saturation")
		sub.prop(SettingsGI, "contrast")
		sub.prop(SettingsGI, "contrast_base")

		layout.label(text="Primary engine:")
		if wide_ui:
			split= layout.split(percentage=0.35)
		else:
			split= layout.split()
		col= split.column()
		col.prop(SettingsGI, "primary_multiplier", text="Mult")
		if wide_ui:
			col= split.column()
		col.prop(SettingsGI, "primary_engine", text="")

		if SettingsGI.primary_engine != '4':
			layout.label(text="Secondary engine:")
			if wide_ui:
				split= layout.split(percentage=0.35)
			else:
				split= layout.split()
			col= split.column()
			col.prop(SettingsGI, "secondary_multiplier", text="Mult")
			if wide_ui:
				col= split.column()
			col.prop(SettingsGI, "secondary_engine", text="")


		layout.separator()

		layout.prop(SettingsGI, 'ao_on', text="Ambient occlusion")
		if SettingsGI.ao_on:
			split= layout.split()
			col= split.column()
			col.prop(SettingsGI, 'ao_amount', slider= True)
			if wide_ui:
				col= split.column()
			col.prop(SettingsGI, 'ao_radius')
			col.prop(SettingsGI, 'ao_subdivs')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(SettingsGI, 'ray_distance_on')
		if wide_ui:
			col= split.column()
		sub= col.column()
		sub.active= SettingsGI.ray_distance_on
		sub.prop(SettingsGI, 'ray_distance')


 ######  ########  ##     ##        ##     ##    ###    ########  ##     ##  #######  ##    ## ####  ######   ######
##    ## ##     ## ##     ##        ##     ##   ## ##   ##     ## ###   ### ##     ## ###   ##  ##  ##    ## ##    ##
##       ##     ## ##     ##        ##     ##  ##   ##  ##     ## #### #### ##     ## ####  ##  ##  ##       ##
 ######  ########  #########        ######### ##     ## ########  ## ### ## ##     ## ## ## ##  ##  ##        ######
      ## ##        ##     ##        ##     ## ######### ##   ##   ##     ## ##     ## ##  ####  ##  ##             ##
##    ## ##        ##     ## ###    ##     ## ##     ## ##    ##  ##     ## ##     ## ##   ###  ##  ##    ## ##    ##
 ######  ##        ##     ## ###    ##     ## ##     ## ##     ## ##     ##  #######  ##    ## ####  ######   ######

class VRAY_RP_GI_sh(classes.VRayRenderPanel):
	bl_label = "Spherical Harmonics"

	@classmethod
	def poll(cls, context):
		SettingsGI = context.scene.vray.SettingsGI
		return SettingsGI.on and SettingsGI.primary_engine == '4' and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		VRayScene=                  context.scene.vray
		SettingsGI=                 VRayScene.SettingsGI

		layout.prop(SettingsGI, 'spherical_harmonics', expand= True)

		layout.separator()

		if SettingsGI.spherical_harmonics == 'RENDER':
			SphericalHarmonicsRenderer= SettingsGI.SphericalHarmonicsRenderer

			split= layout.split()
			col= split.column()
			col.prop(SphericalHarmonicsRenderer, 'file_name')
			col.prop(SphericalHarmonicsRenderer, 'precalc_light_per_frame')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(SphericalHarmonicsRenderer, 'sample_environment')
			if SphericalHarmonicsRenderer.sample_environment:
				col.prop(SphericalHarmonicsRenderer, 'is_hemispherical')
				col.prop(SphericalHarmonicsRenderer, 'subdivs', slider= True)

			if wide_ui:
				col= split.column()

			col.prop(SphericalHarmonicsRenderer, 'apply_filtering')
			if SphericalHarmonicsRenderer.apply_filtering:
				col.prop(SphericalHarmonicsRenderer, 'filter_strength', slider= True)

		else:
			SphericalHarmonicsExporter= SettingsGI.SphericalHarmonicsExporter

			layout.prop(SphericalHarmonicsExporter, 'file_name')
			layout.prop(SphericalHarmonicsExporter, 'file_format')

			layout.separator()

			split= layout.split()
			col= split.column()
			col.prop(SphericalHarmonicsExporter, 'mode')

			if str(SphericalHarmonicsExporter.mode).endswith('_SEL'):
				col.prop_search(SphericalHarmonicsExporter, 'node',
								   context.scene,              'objects')

			col.prop(SphericalHarmonicsExporter, 'object_space')
			col.prop(SphericalHarmonicsExporter, 'per_normal')

			split= layout.split()
			col= split.column()
			col.prop(SphericalHarmonicsExporter, 'bands', slider= True)
			col.prop(SphericalHarmonicsExporter, 'subdivs', slider= True)
			if wide_ui:
				col= split.column()
			col.prop(SphericalHarmonicsExporter, 'ray_bias')

			if SphericalHarmonicsExporter.mode in ('INT_SEL', 'INT_ALL'):
				col.prop(SphericalHarmonicsExporter, 'bounces')
				col.prop(SphericalHarmonicsExporter, 'hit_recording')


#### ########  ########         ##     ##    ###    ########
 ##  ##     ## ##     ##        ###   ###   ## ##   ##     ##
 ##  ##     ## ##     ##        #### ####  ##   ##  ##     ##
 ##  ########  ########         ## ### ## ##     ## ########
 ##  ##   ##   ##   ##          ##     ## ######### ##
 ##  ##    ##  ##    ##  ###    ##     ## ##     ## ##
#### ##     ## ##     ## ###    ##     ## ##     ## ##

class VRAY_RP_GI_im(classes.VRayRenderPanel):
	bl_label = "Irradiance Map"

	@classmethod
	def poll(cls, context):
		SettingsGI = context.scene.vray.SettingsGI
		return SettingsGI.on and SettingsGI.primary_engine == '0' and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		vs= context.scene.vray
		gi= vs.SettingsGI
		module= vs.SettingsIrradianceMap

		split= layout.split()
		colR= split.column()
		colR.prop(module, "mode", text="Mode")

		if module.mode not in {'2', '7'}:
			# split= layout.split()
			# col= split.column()
			# col.label(text="Preset:")
			# if wide_ui:
			# 	col= split.column()
			# col.menu('VRAY_MT_preset_IM', text="Preset")

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

		if module.mode == '2':
			layout.label(text="Basic parameters:")
			layout.prop(module,"interp_samples", text= "Interp. samples")

			layout.label(text="Advanced parameters:")
			split= layout.split()
			col= split.column()
			col.prop(module,"interpolation_mode", text="Interp. type")
			col.prop(module,"lookup_mode")
			col.prop(module,"calc_interp_samples")

		if module.mode == '7':
			split= layout.split()
			split.label(text="Basic parameters:")

			split= layout.split()
			colL= split.column()
			colL.prop(module,"interp_frames")

		split= layout.split()
		split.label(text="Detail enhancement:")
		if wide_ui:
			split= layout.split(percentage=0.07)
			split.column().prop(module, "detail_enhancement", text="")
			sub= split.column().row(align=True)
			sub.active= module.detail_enhancement
			sub.prop(module, "detail_radius", text="R")
			sub.prop(module, "detail_subdivs_mult", text="Subdivs", slider=True)
			sub.prop(module, "detail_scale", text="")
		else:
			split= layout.split()
			col= split.column()
			col.prop(module, "detail_enhancement", text="Use")
			sub= col.column(align=True)
			sub.active= module.detail_enhancement
			sub.prop(module, "detail_radius", text="R")
			sub.prop(module, "detail_subdivs_mult", text="Subdivs", slider=True)
			sub.prop(module, "detail_scale", text="")

		layout.label(text="Show:")
		split = layout.split()
		if wide_ui:
			col = split.row()
		else:
			col = split.column()
		col.prop(module,"show_calc_phase", text="Calc phase")
		sub = col.column()
		sub.active = module.show_calc_phase
		sub.prop(module,"show_direct_light", text="Direct light")
		col.prop(module,"show_samples", text="Samples")

		layout.label(text="Options:")
		split= layout.split()
		col= split.column()
		col.prop(module,"multiple_views", text="Use camera path")

		split= layout.split()
		split.label(text="Files:")
		split= layout.split(percentage=0.3)
		colL= split.column()
		colR= split.column()
		if module.mode in {'2', '7'}:
			colL.label(text="Map file name:")
			colR.prop(module,"file", text="")
		else:
			colL.prop(module,"auto_save", text="Auto save")
			colR.active= module.auto_save
			colR.prop(module,"auto_save_file", text="")


########  ########  ##     ## ######## ########    ########  #######  ########   ######  ########
##     ## ##     ## ##     ##    ##    ##          ##       ##     ## ##     ## ##    ## ##
##     ## ##     ## ##     ##    ##    ##          ##       ##     ## ##     ## ##       ##
########  ########  ##     ##    ##    ######      ######   ##     ## ########  ##       ######
##     ## ##   ##   ##     ##    ##    ##          ##       ##     ## ##   ##   ##       ##
##     ## ##    ##  ##     ##    ##    ##          ##       ##     ## ##    ##  ##    ## ##
########  ##     ##  #######     ##    ########    ##        #######  ##     ##  ######  ########

class VRAY_RP_GI_bf(classes.VRayRenderPanel):
	bl_label = "Brute Force"

	@classmethod
	def poll(cls, context):
		SettingsGI = context.scene.vray.SettingsGI
		showPanel = (SettingsGI.primary_engine == '2' or SettingsGI.secondary_engine == '2') and SettingsGI.primary_engine != '4'
		return SettingsGI.on and showPanel and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		vsce= context.scene.vray
		gi= vsce.SettingsGI
		module= vsce.SettingsDMCGI

		split= layout.split()
		col= split.column()
		col.prop(module, "subdivs")
		if gi.secondary_engine == '2':
			if wide_ui:
				col= split.column()
			col.prop(module, "depth")


##       ####  ######   ##     ## ########     ######     ###     ######  ##     ## ########
##        ##  ##    ##  ##     ##    ##       ##    ##   ## ##   ##    ## ##     ## ##
##        ##  ##        ##     ##    ##       ##        ##   ##  ##       ##     ## ##
##        ##  ##   #### #########    ##       ##       ##     ## ##       ######### ######
##        ##  ##    ##  ##     ##    ##       ##       ######### ##       ##     ## ##
##        ##  ##    ##  ##     ##    ##       ##    ## ##     ## ##    ## ##     ## ##
######## ####  ######   ##     ##    ##        ######  ##     ##  ######  ##     ## ########

class VRAY_RP_GI_lc(classes.VRayRenderPanel):
	bl_label = "Light Cache"

	@classmethod
	def poll(cls, context):
		SettingsGI = context.scene.vray.SettingsGI
		showPanel = (SettingsGI.primary_engine == '3' or SettingsGI.secondary_engine == '3') and SettingsGI.primary_engine != '4'
		return SettingsGI.on and showPanel and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		vs= context.scene.vray
		module= vs.SettingsLightCache

		split= layout.split()
		col= split.column()
		col.prop(module, "mode", text="Mode")

		if not module.mode == '1':
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
		split= layout.split(percentage=0.2)
		split.column().prop(module, "filter")
		sub= split.column().row()
		sub.active= module.filter
		sub.prop(module, "filter_type", text="Type")
		if module.filter_type != '0':
			if module.filter_type == '1':
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
		split= layout.split(percentage=0.3)
		colL= split.column()
		colR= split.column()
		if module.mode == '1':
			colL.label(text="Map file name:")
			colR.prop(module,"file", text="")
		else:
			colL.prop(module,"auto_save", text="Auto save")
			colR.active= module.auto_save
			colR.prop(module,"auto_save_file", text="")


########  ####  ######  ########  ##          ###     ######  ########
##     ##  ##  ##    ## ##     ## ##         ## ##   ##    ## ##
##     ##  ##  ##       ##     ## ##        ##   ##  ##       ##
##     ##  ##   ######  ########  ##       ##     ## ##       ######
##     ##  ##        ## ##        ##       ######### ##       ##
##     ##  ##  ##    ## ##        ##       ##     ## ##    ## ##
########  ####  ######  ##        ######## ##     ##  ######  ########

class VRAY_RP_displace(classes.VRayRenderPanel):
	bl_label = "Displace / Subdivision"

	@classmethod
	def poll(cls, context):
		VRayExporter = context.scene.vray.Exporter
		return VRayExporter.use_displace and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		VRayScene= context.scene.vray
		SettingsDefaultDisplacement= VRayScene.SettingsDefaultDisplacement

		split= layout.split()
		col= split.column()
		col.prop(SettingsDefaultDisplacement, 'amount')
		col.prop(SettingsDefaultDisplacement, 'edgeLength')
		col.prop(SettingsDefaultDisplacement, 'maxSubdivs')
		if wide_ui:
			col= split.column()
		col.prop(SettingsDefaultDisplacement, 'viewDependent')
		col.prop(SettingsDefaultDisplacement, 'tightBounds')
		col.prop(SettingsDefaultDisplacement, 'relative')
		col.prop(SettingsDefaultDisplacement, 'override_on')


########  ########
##     ## ##     ##
##     ## ##     ##
##     ## ########
##     ## ##   ##
##     ## ##    ##
########  ##     ##

class VRAY_RP_dr(classes.VRayRenderPanel):
	bl_label = "Distributed Rendering"

	@classmethod
	def poll(cls, context):
		VRayDR = context.scene.vray.VRayDR
		return VRayDR.on and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		layout = self.layout

		VRayScene = context.scene.vray
		VRayDR          = VRayScene.VRayDR
		SettingsOptions = VRayScene.SettingsOptions

		layout.prop(VRayDR, 'assetSharing')
		layout.separator()

		if VRayDR.assetSharing == 'SHARE':
			layout.prop(VRayDR, 'networkType')
			layout.prop(VRayDR, 'shared_dir')
			if VRayDR.networkType == 'WW':
				layout.prop(VRayDR, 'share_name')
			layout.separator()

		elif VRayDR.assetSharing == 'TRANSFER':
			split = layout.split()
			col = split.column()
			col.prop(VRayDR, 'checkAssets')
			col.prop(VRayDR, 'renderOnlyOnNodes')
			col = split.column()
			col.prop(SettingsOptions, 'misc_useCachedAssets')
			col.prop(SettingsOptions, 'misc_abortOnMissingAsset')
			col.prop(SettingsOptions, 'dr_overwriteLocalCacheSettings')

			split= layout.split()
			split.active = SettingsOptions.dr_overwriteLocalCacheSettings
			col= split.column()
			col.prop(SettingsOptions, 'dr_assetsCacheLimitType', text="Cache Limit")
			sub = col.row()
			sub.active = SettingsOptions.dr_assetsCacheLimitType != '0'
			sub.prop(SettingsOptions, 'dr_assetsCacheLimitValue', text="Limit")
			layout.separator()

		layout.prop(VRayDR, 'port', text="Port")
		layout.separator()

		split= layout.split()
		row= split.row()
		row.template_list("VRayListDR", "", VRayDR, 'nodes', VRayDR, 'nodes_selected', rows= 3)
		col= row.column(align=True)
		col.operator('vray.render_nodes_add',    text="", icon="ZOOMIN")
		col.operator('vray.render_nodes_remove', text="", icon="ZOOMOUT")

		col = col.row().column(align=True)
		col.operator('vray.dr_nodes_load',       text="", icon="FILE_FOLDER")
		col.operator('vray.dr_nodes_save',       text="", icon="SAVE_PREFS")

		if VRayDR.nodes_selected >= 0 and len(VRayDR.nodes) > 0:
			render_node= VRayDR.nodes[VRayDR.nodes_selected]

			layout.separator()

			layout.prop(render_node, 'name')
			layout.prop(render_node, 'address')


########     ###    ##    ## ########
##     ##   ## ##   ##   ##  ##
##     ##  ##   ##  ##  ##   ##
########  ##     ## #####    ######
##     ## ######### ##  ##   ##
##     ## ##     ## ##   ##  ##
########  ##     ## ##    ## ########

class VRAY_RP_bake(classes.VRayRenderPanel):
	bl_label   = "Bake"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls, context):
		VRayBake = context.scene.vray.BakeView
		return VRayBake.use and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		wide_ui = context.region.width > classes.narrowui

		VRayScene = context.scene.vray
		VRayBake  = VRayScene.BakeView

		layout = self.layout
		layout.prop_search(VRayBake, 'bake_node', context.scene, 'objects')

		layout.separator()
		layout.prop(VRayBake, 'uv_channel')

		split = layout.split()
		col = split.column()
		col.prop(VRayBake, 'dilation')
		if wide_ui:
			col = split.column()
		col.prop(VRayBake, 'flip_derivs')


 ######     ###    ##     ##  ######  ######## ####  ######   ######
##    ##   ## ##   ##     ## ##    ##    ##     ##  ##    ## ##    ##
##        ##   ##  ##     ## ##          ##     ##  ##       ##
##       ##     ## ##     ##  ######     ##     ##  ##        ######
##       ######### ##     ##       ##    ##     ##  ##             ##
##    ## ##     ## ##     ## ##    ##    ##     ##  ##    ## ##    ##
 ######  ##     ##  #######   ######     ##    ####  ######   ######

class VRAY_RP_SettingsCaustics(classes.VRayRenderPanel):
	bl_label = "Caustics"

	@classmethod
	def poll(cls, context):
		SettingsCaustics = context.scene.vray.SettingsCaustics
		return SettingsCaustics.on and classes.VRayRenderPanel.poll(context)

	def draw(self, context):
		VRayScene = context.scene.vray
		SettingsCaustics = VRayScene.SettingsCaustics

		classes.DrawPluginUIAuto(context, self.layout, SettingsCaustics, 'SettingsCaustics')


 ######  ##    ##  ######  ######## ######## ##     ##
##    ##  ##  ##  ##    ##    ##    ##       ###   ###
##         ####   ##          ##    ##       #### ####
 ######     ##     ######     ##    ######   ## ### ##
      ##    ##          ##    ##    ##       ##     ##
##    ##    ##    ##    ##    ##    ##       ##     ##
 ######     ##     ######     ##    ######## ##     ##

class VRAY_RP_SettingsSystem(classes.VRayRenderPanel):
	bl_label   = "System"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > classes.narrowui

		rd= context.scene.render

		VRayScene= context.scene.vray
		SettingsRaycaster=        VRayScene.SettingsRaycaster
		SettingsUnitsInfo=        VRayScene.SettingsUnitsInfo
		SettingsRegionsGenerator= VRayScene.SettingsRegionsGenerator
		SettingsOptions=          VRayScene.SettingsOptions
		VRayExporter=             VRayScene.Exporter

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

		layout.separator()
		layout.prop(SettingsRaycaster, 'embreeUse', text="Use Embree")

		split = layout.split()
		split.active = SettingsRaycaster.embreeUse
		col = split.column()
		col.prop(SettingsRaycaster, 'embreeUseMB', text="Use For Motion Blur")
		col.prop(SettingsRaycaster, 'embreeHighPrec', text="High Precision")
		if wide_ui:
			col = split.column()
		col.prop(SettingsRaycaster, 'embreeLowMemory', text="Low Memory")
		col.prop(SettingsRaycaster, 'embreeRayPackets', text="Ray Packets")

		layout.separator()
		layout.label(text="Render Region Division:")
		layout.prop(SettingsRegionsGenerator, 'seqtype', text="Sequence")
		layout.prop(SettingsRegionsGenerator, 'xymeans', text="Buckets")

		bucketLabel = "Size" if SettingsRegionsGenerator.xymeans == '0' else "Count"

		split = layout.split()
		col = split.column()
		col.prop(SettingsRegionsGenerator, 'lock_size', text="Lock %s" % bucketLabel)
		col.prop(SettingsRegionsGenerator, 'reverse')
		if wide_ui:
			col = split.column()
		if SettingsRegionsGenerator.lock_size:
			col.prop(SettingsRegionsGenerator, 'xc', text=bucketLabel)
		else:
			sub = col.column(align=True)
			sub.prop(SettingsRegionsGenerator, 'xc', text="X %s" % bucketLabel)
			sub.prop(SettingsRegionsGenerator, 'yc', text="Y %s" % bucketLabel)

		layout.separator()
		layout.label("Console Log:")
		layout.prop(VRayExporter, 'verboseLevel')
		layout.prop(VRayExporter, 'showProgress')


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
	return (
		VRAY_RP_dimensions,
		VRAY_RP_output,
		VRAY_RP_render,
		VRAY_RP_Globals,
		VRAY_RP_RTEngine,
		VRAY_RP_SettingsCaustics,
		VRAY_RP_exporter,
		VRAY_RP_cm,
		VRAY_RP_aa,
		VRAY_RP_dmc,
		VRAY_RP_gi,
		VRAY_RP_GI_sh,
		VRAY_RP_GI_im,
		VRAY_RP_GI_bf,
		VRAY_RP_GI_lc,
		VRAY_RP_displace,
		VRAY_RP_dr,
		VRAY_RP_bake,
		VRAY_RP_SettingsSystem,
		VRAY_RP_VRayStereoscopicSettings,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

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
from vb25.plugin_manager import *


VRayScene.use_hidden_lights= BoolProperty(
	name= "Hidden lights",
	description= "Render hidden lights.",
	default= False
)


class VRayBake(bpy.types.IDPropertyGroup):
	pass

VRayScene.VRayBake= PointerProperty(
	name= "VRayBake",
	type=  VRayBake,
	description= "Texture baking settings."
)

VRayBake.use= BoolProperty(
	name= "Bake texture",
	description= "Bake texture.",
	default= False
)

VRayBake.object= StringProperty(
	name= "Object",
	subtype= 'NONE',
	description= "Object to bake."
)

VRayBake.dilation= IntProperty(
	name= "Dilation",
	description= "Number of pixels to expand around geometry.",
	min= 0,
	max= 1000,
	soft_min= 0,
	soft_max= 100,
	default= 2,
)

VRayBake.flip_derivs= BoolProperty(
	name= "Flip derivatives",
	description= "Flip the texture direction derivatives (reverses bump mapping).",
	default= False
)


class SettingsDefaultDisplacement(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsDefaultDisplacement= PointerProperty(
	name= "SettingsDefaultDisplacement",
	type=  SettingsDefaultDisplacement,
	description= "Default displacement settings."
)

SettingsDefaultDisplacement.override_on= BoolProperty(
	name= "Override",
	description= "Override settings globally.",
	default= False
)

SettingsDefaultDisplacement.edgeLength= FloatProperty(
	name= "Edge length",
	description= "Max. height",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 4
)

SettingsDefaultDisplacement.viewDependent= BoolProperty(
	name= "View dependent",
	description= "Determines if view-dependent tesselation is used.",
	default= True
)

SettingsDefaultDisplacement.maxSubdivs= IntProperty(
	name= "Max subdivs",
	description= "Determines the maximum subdivisions for a triangle of the original mesh.",
	min= 0,
	max= 2048,
	soft_min= 0,
	soft_max= 1024,
	default= 256
)

SettingsDefaultDisplacement.tightBounds= BoolProperty(
	name= "Tight bounds",
	description= "When this is on, initialization will be slower, but tighter bounds will be computed for the displaced triangles making rendering faster.",
	default= True
)

SettingsDefaultDisplacement.amount= FloatProperty(
	name= "Amount",
	description= "Determines the displacement amount for white areas in the displacement map.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1
)

SettingsDefaultDisplacement.relative= BoolProperty(
	name= "Relative",
	description= "TODO.",
	default= False
)


class SettingsDMCSampler(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsDMCSampler= PointerProperty(
	name= "DMC Sampler",
	type=  SettingsDMCSampler,
	description= "DMC Sampler settings."
)

SettingsDMCSampler.adaptive_threshold= FloatProperty(
	name= "Noise threshold",
	description= "Controls V-Ray's judgement of when a blurry value is \"good enough\" to be used.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.001,
	soft_max= 0.1,
	default= 0.01,
	precision= 3
)

SettingsDMCSampler.adaptive_min_samples= IntProperty(
	name= "Min samples",
	description= "The minimum number of samples that must be made before the early termination algorithm is used.",
	min= 1,
	max= 100,
	default= 8
)

SettingsDMCSampler.adaptive_amount= FloatProperty(
	name= "Adaptive amount",
	description= "A value of 1.0 means full adaptation; a value of 0.0 means no adaptation.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.85,
	precision= 2
)

SettingsDMCSampler.time_dependent= BoolProperty(
	name= "Time dependent",
	description= "This make the samping pattern change with time.",
	default= 0
)

SettingsDMCSampler.subdivs_mult= FloatProperty(
	name= "Subdivs mult",
	description= "This will multiply all subdivs values everywhere during rendering.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.0
)


class SettingsColorMapping(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsColorMapping= PointerProperty(
	name= "Color Mapping",
	type=  SettingsColorMapping,
	description= "Color mapping settings."
)

SettingsColorMapping.type= EnumProperty(
	name= "Type",
	description= "Color mapping type.",
	items= (
		('LNR',"Linear",""),
		('EXP',"Exponential",""),
		('HSV',"HSV exponential",""),
		('INT',"Intensity exponential",""),
		('GCOR',"Gamma correction",""),
		('GINT',"Intensity gamma",""),
		('REIN',"Reinhard","")
	),
	default= "LNR"
)

SettingsColorMapping.affect_background= BoolProperty(
	name= "Affect background",
	description= "Affect colors belonging to the background.",
	default= True
)

SettingsColorMapping.dark_mult= FloatProperty(
	name= "Dark multiplier",
	description= "Multiplier for dark colors.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

SettingsColorMapping.bright_mult= FloatProperty(
	name= "Bright multiplier",
	description= "Multiplier for bright colors.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 1.0
)

SettingsColorMapping.gamma= FloatProperty(
	name= "Gamma",
	description= "Gamma correction for the output image regardless of the color mapping mode.",
	min= 0.0,
	max= 10.0,
	soft_min= 1.0,
	soft_max= 2.2,
	default= 1.0
)

SettingsColorMapping.input_gamma= FloatProperty(
	name= "Input gamma",
	description= "Input gamma for textures.",
	min= 0.0,
	max= 10.0,
	soft_min= 1.0,
	soft_max= 2.2,
	default= 1.0
)

SettingsColorMapping.clamp_output= BoolProperty(
	name= "Clamp output",
	description= "Clamp colors after color mapping.",
	default= True
)

SettingsColorMapping.clamp_level= FloatProperty(
	name= "Clamp level",
	description= "The level at which colors will be clamped.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 100.0,
	default= 1.0
)

SettingsColorMapping.subpixel_mapping= BoolProperty(
	name= "Sub-pixel mapping",
	description= "This option controls whether color mapping will be applied to the final image pixels, or to the individual sub-pixel samples.",
	default= False
)

SettingsColorMapping.adaptation_only= BoolProperty(
	name= "Adaptation only",
	description= "When this parameter is on, the color mapping will not be applied to the final image, however V-Ray will proceed with all its calculations as though color mapping is applied (e.g. the noise levels will be corrected accordingly).",
	default= False
)

SettingsColorMapping.linearWorkflow= BoolProperty(
	name= "Linear workflow",
	description= "When this option is checked V-Ray will automatically apply the inverse of the Gamma correction that you have set in the Gamma field to all materials in scene.",
	default= False
)


class SettingsImageSampler(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsImageSampler= PointerProperty(
	name= "Image Sampler",
	type=  SettingsImageSampler,
	description= "Image Sampler settings."
)

SettingsImageSampler.filter_type= EnumProperty(
	name= "Filter type",
	description= "Antialiasing filter.",
	items= (
		('NONE',"None",""),
		('GAUSS',"Gaussian",""),
		('SINC',"Sinc",""),
		('CATMULL',"CatmullRom",""),
		('LANC',"Lanczos",""),
		('TRIANGLE',"Triangle",""),
		('BOX',"Box",""),
		('AREA',"Area","")
	),
	default= "NONE"
)

SettingsImageSampler.filter_size= FloatProperty(
	name= "Filter size",
	description= "Filter size.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.5
)

SettingsImageSampler.type= EnumProperty(
	name= "Type",
	description= "Image sampler type.",
	items= (
		('FXD',"Fixed",""),
		('DMC',"Adaptive DMC",""),
		('SBD',"Adaptive subdivision","")
	),
	default= "DMC"
)

SettingsImageSampler.dmc_minSubdivs= IntProperty(
	name= "Min subdivs",
	description= "The initial (minimum) number of samples taken for each pixel.",
	min= 1,
	max= 100,
	default= 1
)

SettingsImageSampler.dmc_maxSubdivs= IntProperty(
	name= "Max subdivs",
	description= "The maximum number of samples for a pixel.",
	min= 1,
	max= 100,
	default= 4
)

SettingsImageSampler.dmc_treshhold_use_dmc= BoolProperty(
	name= "Use DMC sampler threshold",
	description= "Use threshold specified in the \"DMC sampler\"",
	default= 1
)

SettingsImageSampler.dmc_threshold= FloatProperty(
	name= "Color threshold",
	description= "The threshold that will be used to determine if a pixel needs more samples.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.01
)

SettingsImageSampler.dmc_show_samples= BoolProperty(
	name= "Show samples",
	description= "Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
	default= 0
)

SettingsImageSampler.fixed_subdivs= IntProperty(
	name= "Subdivs",
	description= "The number of samples per pixel.",
	min= 1,
	max= 100,
	default= 1
)

SettingsImageSampler.subdivision_show_samples= BoolProperty(
	name= "Show samples",
	description= "Show an image where the pixel brightness is directly proportional to the number of samples taken at this pixel.",
	default= 0
)

SettingsImageSampler.subdivision_normals= BoolProperty(
	name= "Normals",
	description= "This will supersample areas with sharply varying normals.",
	default= 0
)

SettingsImageSampler.subdivision_normals_threshold= FloatProperty(
	name= "Normals threshold",
	description= "Normals threshold.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.05
)

SettingsImageSampler.subdivision_jitter= BoolProperty(
	name= "Randomize samples",
	description= "Displaces the samples slightly to produce better antialiasing of nearly horizontal or vertical lines.",
	default= 1
)

SettingsImageSampler.subdivision_threshold= FloatProperty(
	name= "Color threshold",
	description= "Determines the sensitivity of the sampler to changes in pixel intensity.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.1
)

SettingsImageSampler.subdivision_edges= BoolProperty(
	name= "Object outline",
	description= "This will cause the image sampler to always supersample object edges.",
	default= 0
)

SettingsImageSampler.subdivision_minRate= IntProperty(
	name= "Min rate",
	description= "Minimum number of samples per pixel.",
	min= -10,
	max= 50,
	default= -1
)

SettingsImageSampler.subdivision_maxRate= IntProperty(
	name= "Max rate",
	description= "Maximum number of samples per pixel.",
	min= -10,
	max= 50,
	default= 2
)


class SettingsRaycaster(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsRaycaster= PointerProperty(
	name= "Raycaster",
	type=  SettingsRaycaster,
	description= "Raycaster settings."
)

SettingsRaycaster.maxLevels= IntProperty(
	name= "Max. tree depth",
	description= "Maximum BSP tree depth.",
	min= 50,
	max= 100,
	default= 80
)

SettingsRaycaster.minLeafSize= FloatProperty(
	name= "Min. leaf size",
	description= "Minimum size of a leaf node.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= 0.0
)

SettingsRaycaster.faceLevelCoef= FloatProperty(
	name= "Face/level",
	description= "Maximum amount of triangles in a leaf node.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 10.0,
	default= 1.0
)

SettingsRaycaster.dynMemLimit= IntProperty(
	name= "Dynamic memory limit",
	description= "RAM limit for the dynamic raycasters.",
	min= 100,
	max= 100000,
	default= 400
)


class SettingsUnitsInfo(bpy.types.IDPropertyGroup):
	pass

VRayScene.SettingsUnitsInfo= PointerProperty(
	name= "Units",
	type=  SettingsUnitsInfo,
	description="Units settings."
)

SettingsUnitsInfo.photometric_scale= FloatProperty(
	name= "Photometric scale",
	description= "Photometric scale.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 4,
	default= 0.002
)

SettingsUnitsInfo.meters_scale= FloatProperty(
	name= "Meters scale",
	description= "Meters scale.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1.0
)


class VRayExporter(bpy.types.IDPropertyGroup):
	pass

VRayScene.exporter= PointerProperty(
	name= "Exporter",
	type=  VRayExporter,
	description= "Exporter settings."
)

VRayExporter.use_material_nodes= BoolProperty(
	name= "Use material nodes",
	description= "Use material nodes.",
	default= False
)

VRayExporter.mesh_active_layers= BoolProperty(
	name= "Export meshes from active layers",
	description= "Export meshes from active layers only.",
	default= True
)

VRayExporter.use_displace= BoolProperty(
	name= "Use displace",
	description= "Use displace.",
	default= True
)

VRayExporter.image_to_blender= BoolProperty(
	name= "Image to Blender",
	description= "Pass image to Blender on render end.",
	default= False
)

VRayExporter.log_window= BoolProperty(
	name= "Show log window",
	description= "Show log window (Linux).",
	default= False
)

VRayExporter.animation= BoolProperty(
	name= "Animation",
	description= "Render animation.",
	default= False
)

VRayExporter.use_hair= BoolProperty(
	name= "Hair",
	description= "Render hair.",
	default= True
)

VRayExporter.use_instances= BoolProperty(
	name= "Instances",
	description= "Use instances (saves memory and faster export)",
	default= False
)

VRayExporter.camera_loop= BoolProperty(
	name= "Camera loop",
	description= "Render views from all cameras.",
	default= False
)

VRayExporter.compat_mode= BoolProperty(
	name= "Compatibility mode",
	description= "Shading compatibility mode for old versions of V-Ray.",
	default= False
)

VRayExporter.active_layers= BoolProperty(
	name= "Active layers",
	description= "Render objects only from visible layers.",
	default= True
)

VRayExporter.auto_meshes= BoolProperty(
	name= "Auto export meshes",
	description= "Export meshes automatically before render.",
	default= 0
)

VRayExporter.autorun= BoolProperty(
	name= "Autorun",
	description= "Start V-Ray automatically after export.",
	default= 1
)

VRayExporter.debug= BoolProperty(
	name= "Debug",
	description= "Enable script\'s debug output.",
	default= 0
)

VRayExporter.output= EnumProperty(
	name= "Exporting directory",
	description= "Exporting directory.",
	items= (
		('USER',"User-defined directory",""),
		('SCENE',"Scene file directory",""),
		('TMP',"Global TMP directory","")
	),
	default= 'TMP'
)

VRayExporter.detect_vray= BoolProperty(
	name= "Detect V-Ray",
	description= "Detect V-Ray binary location.",
	default= True
)

VRayExporter.vray_binary= StringProperty(
	name= "Path",
	subtype= 'FILE_PATH',
	description= "Path to V-Ray binary."
)

VRayExporter.output_dir= StringProperty(
	name= "Directory",
	subtype= 'DIR_PATH',
	description= "User-defined output directory."
)

VRayExporter.output_unique= BoolProperty(
	name= "Use unique file name",
	description= "Use unique file name.",
	default= False
)


class VRayDR(bpy.types.IDPropertyGroup):
	pass

VRayScene.VRayDR= PointerProperty(
	name= "Distributed rendering",
	type=  VRayDR,
	description= "Distributed rendering settings."
)

VRayDR.on= BoolProperty(
	name= "Distributed rendering",
	description= "Distributed rendering.",
	default= False
)

VRayDR.port= IntProperty(
	name= "Distributed rendering port",
	description= "Distributed rendering port.",
	min= 0,
	max= 65535,
	default= 20204
)

VRayDR.shared_dir= StringProperty(
	name= "Shared directory",
	subtype= 'DIR_PATH',
	description= "Distributed rendering shader directory."
)

VRayDR.nodes_selected= IntProperty(
	name= "Render Node Index",
	default= -1,
	min= -1,
	max= 100
)

VRayDR.type= EnumProperty(
	name= "Type",
	description= "Distributed rendering network type.",
	items= (
		('WW', "Windows - Windows", "Window master & Windows nodes."),
		('WU', "Windows - Unix",    "Window master & Unix nodes."),
		('UU', "Unix - Unix",       "Unix master & Unix nodes.")
	),
	default= 'WU'
)


class VRayRenderNode(bpy.types.IDPropertyGroup):
	pass

VRayDR.nodes= CollectionProperty(
	name= "Render Nodes",
	type=  VRayRenderNode,
	description= "V-Ray render nodes."
)

VRayRenderNode.address= StringProperty(
	name= "IP/Hostname",
	description= "Render node IP or hostname."
)

	

'''
	GUI
'''
import properties_render
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('VRAY_RENDER')
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_render.RENDER_PT_output.COMPAT_ENGINES.add('VRAY_RENDER')
properties_render.RENDER_PT_output.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
del properties_render


narrowui= 200


class RENDER_MT_VRAY_im_preset(bpy.types.Menu):
	bl_label= "Irradiance Map Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "im")
	preset_operator = "script.execute_preset"
	draw = bpy.types.Menu.draw_preset


class RENDER_CHANNELS_OT_add(bpy.types.Operator):
	bl_idname=      'render_channels.add'
	bl_label=       "Add Render Channel"
	bl_description= "Add render channel"

	def invoke(self, context, event):
		sce= context.scene
		vsce= sce.vray

		render_channels= vsce.render_channels

		render_channels.add()
		render_channels[-1].name= "RenderChannel"

		return{'FINISHED'}


class RENDER_CHANNELS_OT_del(bpy.types.Operator):
	bl_idname=      'render_channels.remove'
	bl_label=       "Remove Render Channel"
	bl_description= "Remove render channel"

	def invoke(self, context, event):
		sce= context.scene
		vsce= sce.vray
		
		render_channels= vsce.render_channels
		
		if vsce.render_channels_index >= 0:
		   render_channels.remove(vsce.render_channels_index)
		   vsce.render_channels_index-= 1

		return{'FINISHED'}


class RENDER_NODES_OT_add(bpy.types.Operator):
	bl_idname=      'render_nodes.add'
	bl_label=       "Add Render Node"
	bl_description= "Add render node"

	def invoke(self, context, event):
		vs= context.scene.vray
		module= vs.VRayDR

		module.nodes.add()
		module.nodes[-1].name= "Render Node"

		return{'FINISHED'}


class RENDER_NODES_OT_del(bpy.types.Operator):
	bl_idname=      'render_nodes.remove'
	bl_label=       "Remove Render Nodel"
	bl_description= "Remove render node"

	def invoke(self, context, event):
		vs= context.scene.vray
		module= vs.VRayDR

		if module.nodes_selected >= 0:
		   module.nodes.remove(module.nodes_selected)
		   module.nodes_selected-= 1

		return{'FINISHED'}


def base_poll(cls, context):
	rd= context.scene.render
	return (rd.use_game_engine == False) and (rd.engine in cls.COMPAT_ENGINES)


class RenderButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render'


class RENDER_PT_vray_render(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Render"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		vs= context.scene.vray
		ve= vs.exporter
		SettingsOptions= vs.SettingsOptions

		split= layout.split()
		col= split.column()
		col.operator('render.render', text="Image", icon='RENDER_STILL')
		if not ve.auto_meshes:
			if wide_ui:
				col= split.column()
			col.operator('vray_export_meshes', icon='OUTLINER_OB_MESH')

		split= layout.split()
		col= split.column()
		col.label(text="Modules:")
		col.prop(vs.SettingsGI, 'on', text="Global Illumination")
		col.prop(vs.SettingsCaustics, 'on', text="Caustics")
		col.prop(ve, 'use_displace', text= "Displace")
		col.prop(vs.VRayDR, 'on')
		if wide_ui:
			col= split.column()
		col.label(text="Pipeline:")
		col.prop(ve, 'animation')
		col.prop(ve, 'use_instances')
		col.prop(ve, 'active_layers')
		col.prop(SettingsOptions, 'gi_dontRenderImage')


class VRAY_RENDER_SettingsOptions(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "Globals"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > 200

		VRayScene= context.scene.vray
		VRayExporter=    VRayScene.exporter
		SettingsOptions= VRayScene.SettingsOptions

		split= layout.split()
		col= split.column()
		col.label(text="Geometry:")
		col.prop(SettingsOptions, 'geom_displacement')
		col.prop(VRayExporter, 'use_hair')
		col.prop(SettingsOptions, 'geom_doHidden')
		col.prop(SettingsOptions, 'geom_backfaceCull')
		col.prop(SettingsOptions, 'ray_bias', text="Secondary bias")
		if wide_ui:
			col= split.column()
		col.label(text="Lights:")
		col.prop(SettingsOptions, 'light_doLights')
		# col.prop(SettingsOptions, 'light_doDefaultLights')
		# col.prop(SettingsOptions, 'light_doHiddenLights')
		col.prop(VRayScene, 'use_hidden_lights')
		col.prop(SettingsOptions, 'light_doShadows')
		col.prop(SettingsOptions, 'light_onlyGI')

		layout.label(text="Materials:")
		split= layout.split()
		col= split.column()
		sub= col.column()
		sub.active= False
		sub.prop(SettingsOptions, 'mtl_override_on')
		if SettingsOptions.mtl_override_on:
			sub.prop_search(SettingsOptions, 'mtl_override', bpy.data, 'materials', text="")
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


class RENDER_PT_vray_exporter(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "Exporter"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		ve= context.scene.vray.exporter

		split= layout.split()
		col= split.column()
		col.prop(ve, 'autorun')
		sub= col.column()
		sub.active= False
		sub.prop(ve, 'auto_meshes')
		col.prop(ve, 'debug')
		if wide_ui:
			col= split.column()
		col.prop(ve, 'mesh_active_layers', text= "Active layers meshes")
		col.prop(ve, 'image_to_blender')
		col.prop(ve, 'use_material_nodes')
		col.prop(ve, 'compat_mode')
		

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(ve, 'detect_vray')
		if not ve.detect_vray:
			split= layout.split()
			col= split.column()
			col.prop(ve, 'vray_binary')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(ve, 'output', text="Export to")
		if ve.output == 'USER':
			col.prop(ve, 'output_dir')
		col.prop(ve, 'output_unique')


class RENDER_PT_vray_cm(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Color mapping"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

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


class RENDER_PT_vray_aa(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Image sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

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


class RENDER_PT_vray_dmc(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "DMC Sampler"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

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


class RENDER_PT_vray_gi(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Global Illumination"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		vs= context.scene.vray
		module= vs.SettingsGI
		return base_poll(__class__, context) and module.on

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


class RENDER_PT_im(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Irradiance Map"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return base_poll(__class__, context) and module.on and module.primary_engine == 'IM'

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
			col.menu('RENDER_MT_VRAY_im_preset', text="Preset")

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
			col.prop(module,"interpolationType", text="Interp. type")
			col.prop(module,"lookupType")
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


class RENDER_PT_bf(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Brute Force"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return base_poll(__class__, context) and module.on and (module.primary_engine == 'BF' or module.secondary_engine == 'BF')

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


class RENDER_PT_lc(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Light Cache"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		module= context.scene.vray.SettingsGI
		return (base_poll(__class__, context) and module.on and (module.primary_engine == 'LC' or module.secondary_engine == 'LC'))

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
			col.prop(module, "scale", text="Sample scale")
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
			if module.filter_type == 'NEAREST':
				sub.prop(module, "filter_samples")
			else:
				sub.prop(module, "filter_size")

		split= layout.split(percentage=0.2)
		split.column().prop(module, "prefilter")
		colR= split.column()
		colR.active= module.prefilter
		colR.prop(module, "prefilter_samples")

		split= layout.split()
		split.column().prop(module, "use_for_glossy_rays")
		split.column().prop(module, "multiple_views")

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


class RENDER_PT_vray_Layers(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "Channels"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui = context.region.width > narrowui
		layout= self.layout
		
		sce= context.scene
		vsce= sce.vray
		render_channels= vsce.render_channels

		split= layout.split()
		row= split.row()
		row.template_list(vsce, 'render_channels', vsce, 'render_channels_index', rows= 3)
		col= row.column(align=True)
		col.operator('render_channels.add',    text="", icon="ZOOMIN")
		col.operator('render_channels.remove', text="", icon="ZOOMOUT")

		if vsce.render_channels_index >= 0 and len(render_channels) > 0:
			render_channel= render_channels[vsce.render_channels_index]
		
			layout.separator()

			layout.prop(render_channel, 'name')
			layout.prop(render_channel, 'type', text="Type")

			layout.separator()

			if render_channel.type != 'NONE':
				plugin= get_plugin(CHANNEL_PLUGINS, render_channel.type)
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


class RENDER_PT_vray_displace(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Displace"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		VRayExporter= context.scene.vray.exporter
		return base_poll(__class__, context) and VRayExporter.use_displace

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray
		SettingsDefaultDisplacement= VRayScene.SettingsDefaultDisplacement

		split= layout.split()
		col= split.column()
		col.prop(SettingsDefaultDisplacement, 'amount')
		col.prop(SettingsDefaultDisplacement, 'edgeLength')
		col.prop(SettingsDefaultDisplacement, 'maxSubdivs')
		if wide_ui:
			col= split.column()
		col.prop(SettingsDefaultDisplacement, 'override_on')
		col.prop(SettingsDefaultDisplacement, 'viewDependent')
		col.prop(SettingsDefaultDisplacement, 'tightBounds')
		col.prop(SettingsDefaultDisplacement, 'relative')


class RENDER_PT_vray_dr(RenderButtonsPanel, bpy.types.Panel):
	bl_label = "Distributed rendering"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		vs= context.scene.vray
		module= vs.VRayDR
		return base_poll(__class__, context) and module.on

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
		col.operator('render_nodes.add',    text="", icon="ZOOMIN")
		col.operator('render_nodes.remove', text="", icon="ZOOMOUT")

		if module.nodes_selected >= 0 and len(module.nodes) > 0:
			render_node= module.nodes[module.nodes_selected]
		
			layout.separator()

			layout.prop(render_node, 'name')
			layout.prop(render_node, 'address')


class RENDER_PT_VRAY_bake(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "Bake"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		VRayScene= context.scene.vray
		VRayBake= VRayScene.VRayBake
		self.layout.prop(VRayBake, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > 200

		VRayScene= context.scene.vray
		VRayBake= VRayScene.VRayBake

		layout= self.layout
		layout.active= VRayBake.use

		split= layout.split()
		col= split.column()
		col.prop_search(VRayBake, 'object',  context.scene, 'objects')

		if wide_ui:
			col= split.column()

		col.prop(VRayBake, 'dilation')
		col.prop(VRayBake, 'flip_derivs')


class VRAY_RENDER_SettingsSystem(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "System"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout
		wide_ui= context.region.width > 200

		VRayScene= context.scene.vray
		SettingsRaycaster=        VRayScene.SettingsRaycaster
		SettingsUnitsInfo=        VRayScene.SettingsUnitsInfo
		SettingsRegionsGenerator= VRayScene.SettingsRegionsGenerator
		SettingsOptions=          VRayScene.SettingsOptions

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

		layout.label(text="Units scale:")
		split= layout.split()
		col= split.column()
		col.prop(SettingsUnitsInfo, 'meters_scale', text="Metric")
		if wide_ui:
			col= split.column()
		col.prop(SettingsUnitsInfo, 'photometric_scale', text="Photometric")

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


class RENDER_PT_vray_about(RenderButtonsPanel, bpy.types.Panel):
	bl_label   = "About"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

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

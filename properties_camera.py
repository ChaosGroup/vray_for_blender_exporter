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

''' vb modules '''
from vb25.utils import *


class VRayCamera(bpy.types.IDPropertyGroup):
	pass

bpy.types.Camera.PointerProperty(
	attr= 'VRayCamera',
	type=  VRayCamera,
	name= "Camera",
	description= "Camera settings."
)

VRayCamera.BoolProperty(
	attr= 'hide_from_view',
	name= "Hide From View",
	description= "Hide objects from current view.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'hide_from_everything',
	name= "Hide from everything",
	description= "Hide objects completely.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'everything_auto',
	name= "Hide from everything (automatic)",
	description= "Create group with name \"hidefrom_<camera-name>\".",
	default= False
)

VRayCamera.StringProperty(
	attr= 'everything_objects',
	name= "Objects",
	description= "Objects to hide completely: name{;name;etc}",
	default= ""
)

VRayCamera.StringProperty(
	attr= 'everything_groups',
	name= "Groups",
	description= "Groups to hide completely: name{;name;etc}",
	default= ""
)

VRayCamera.BoolProperty(
	attr= 'hide_from_camera',
	name= "Hide from camera",
	description= "Hide objects from camera.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'hide_from_gi',
	name= "Hide from GI",
	description= "Hide objects from GI.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'hide_from_reflect',
	name= "Hide from reflections",
	description= "Hide objects from reflections.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'hide_from_refract',
	name= "Hide from refractions",
	description= "Hide objects from refractions.",
	default= False
)

VRayCamera.BoolProperty(
	attr= 'hide_from_shadows',
	name= "Hide from shadows",
	description= "Hide objects from shadows.",
	default= False
)



BoolProperty= bpy.types.Camera.BoolProperty
IntProperty= bpy.types.Camera.IntProperty
FloatProperty= bpy.types.Camera.FloatProperty
EnumProperty= bpy.types.Camera.EnumProperty
FloatVectorProperty= bpy.types.Camera.FloatVectorProperty


EnumProperty(   attr="vray_cam_mode",
				name="Mode",
				description="Camera mode.",
				items=(
					("NORMAL",   "Normal", ""),
					("PHYSICAL", "Physical", "")
				),
				default= "NORMAL")

'''
  SettingsCamera
'''
EnumProperty(   attr="vray_cam_type",
				name="Type",
				description="Camera type.",
				items=(
					("DEFAULT",            "Default", ""),
					("SPHERIFICAL",        "Spherifical", ""),
					("CYLINDRICAL_POINT",  "Cylindrical (point)", ""),
					("CYLINDRICAL_ORTHO",  "Cylindrical (ortho)", ""),
					("BOX",                "Box", ""),
					("FISH_EYE",           "Fish-eye", ""),
					("WARPED_SPHERICAL",   "Warped spherical", ""),
					("ORTHOGONAL",         "Orthogonal", ""),
					("PINHOLE",            "Pinhole", ""),
				),
				default= "DEFAULT")

BoolProperty(   attr="vray_cam_auto_fit",
				name="Auto-fit",
				description="The auto-fit option of the fish-eye camera.",
				default= True)

FloatProperty(	attr="vray_cam_height",
				name="Height",
				description="Height of the cylindrical (ortho) camera.",
				min=0.0, max=10000.0, soft_min=0.0, soft_max=10.0, default=400.0)

FloatProperty(	attr="vray_cam_dist",
				name="Distance",
				description="Distance to the sphere center.",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=10.0, default=2.0)

FloatProperty(	attr="vray_cam_curve",
				name="Curve",
				description="Controls the way the rendered images is warped.",
				min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default=1.0)

'''
  SettingsCameraDof
'''
BoolProperty(   attr="vray_cam_dof_on",
				name="DOF",
				description="Use depth of field.",
				default= False)

BoolProperty(   attr="vray_cam_dof_sides_on",
				name="This option allows you to simulate the polygonal shape of the aperture of real-world cameras.",
				description="Enable Bokeh effects.",
				default= False)

IntProperty(	attr="vray_cam_dof_sides_num",
				name="Number",
				description="Number of sides.",
				min=1, max=100, default=5)

IntProperty(	attr="vray_cam_dof_subdivs",
				name="Subdivs",
				description="Controls the quality of the DOF effect.",
				min=1, max=100, default=8)

FloatProperty(  attr="vray_cam_dof_anisotropy",
				name="Anisotropy",
				description="This allows the stretching of the bokeh effect horizontally or vertically.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

FloatProperty(  attr="vray_cam_dof_focal_dist",
				name="Focal distance",
				description="Determines the distance from the camera at which objects will be in perfect focus.",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=10.0, default=200.0)

FloatProperty(  attr="vray_cam_dof_aperture",
				name="Aperture",
				description="The size of the virtual camera aperture, in world units.",
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=5.0)

FloatProperty(  attr="vray_cam_dof_center_bias",
				name="Center bias",
				description="This determines the uniformity of the DOF effect.",
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=0.0)

FloatProperty(  attr="vray_cam_dof_rotation",
				name="Rotation",
				description="Specifies the orientation of the aperture shape.",
				min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default=0.0)


'''
  SettingsMotionBlur
'''
BoolProperty(   attr="vray_cam_motionblur_on",
				name="Motion blur",
				description="Turns motion blur on.",
				default= False)

FloatProperty(  attr="vray_cam_motionblur_interval_center",
				name="Interval center",
				description="Specifies the middle of the motion blur interval with respect to the frame.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.5)

FloatProperty(  attr="vray_cam_motionblur_duration",
				name="Duration",
				description="Specifies the duration, in frames, during which the camera shutter is open.",
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=1.0)

FloatProperty(  attr="vray_cam_motionblur_bias",
				name="Bias",
				description="This controls the bias of the motion blur effect.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

IntProperty(    attr="vray_cam_motionblur_subdivs",
				name="Subdivs",
				description="Determines the quality of the motion blur.",
				min=1, max=100, default=6)

IntProperty(    attr="vray_cam_motionblur_geom_samples",
				name="Geometry samples",
				description="This determines the number of geometry segments used to approximate motion blur.",
				min=1, max=100, default=2)

IntProperty(    attr="vray_cam_motionblur_low_samples",
				name="Low samples",
				description="This controls how many samples in time will be computed during irradiance map calculations.",
				min=1, max=100, default=1)


'''
  CameraPhysical
'''
FloatProperty(	attr="vray_cam_phys_f_number",
				name="F-number",
				description="Determines the width of the camera aperture and, indirectly, exposure.",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=10.0, default= 8.0)

VRayCamera.FloatVectorProperty(
	attr= "white_balance",
	name= "White balance",
	description= "White balance.",
	default= (1.0, 1.0, 1.0),
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	step= 3,
	precision= 3,
	options= {'ANIMATABLE'},
	subtype= 'COLOR',
	size= 3
)

FloatProperty(  attr="vray_cam_phys_latency",
				name="Latency",
				description="CCD matrix latency, in seconds.",  # for video camera
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=0.0)

FloatProperty(  attr="vray_cam_phys_lens_shift",
				name="Lens shift",
				description="Shift lenses for 2-point perspective.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

FloatProperty(  attr="vray_cam_phys_ISO",
				name="ISO",
				description="The film power (i.e. sensitivity).",
				min=0.0, max=10000.0, soft_min=0.0, soft_max=100.0, default=200.0)

FloatProperty(  attr="vray_cam_phys_shutter_speed",
				name="Shutter speed",
				description="The shutter speed, in inverse seconds.", # for still camera
				min= 1.0,
				max= 1000.0,
				soft_min=0.0,
				soft_max=1000.0,
				default=300.0)

FloatProperty(  attr="vray_cam_phys_focal_length",
				name="Focal length",
				description="Specifies the equivalen focal length of the camera lens.",
				min=0.0, max=200.0, soft_min=0.0, soft_max=10.0, default=40.0)

FloatProperty(  attr="vray_cam_phys_dof_display_threshold",
				name="DOF threshold",
				description="Display threshold for depth-of-field.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

FloatProperty(  attr="vray_cam_phys_distortion",
				name="Distortion",
				description="Specifies the distortion coefficient for the camera lens.",
				min=-1.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

IntProperty(    attr="vray_cam_phys_distortion_type",
				name="Distortion type",
				description="",
				min=0, max=2, default=0)

FloatProperty(  attr="vray_cam_phys_zoom_factor",
				name="Zoom factor",
				description="Zoom factor.",
				min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default=1.0)

FloatProperty(  attr="vray_cam_phys_film_width",
				name="Film width",
				description="Specifies the horizontal size of the film gate in milimeters.",
				min=0.0, max=200.0, soft_min=0.0, soft_max=10.0, default=36.0)

FloatProperty(  attr="vray_cam_phys_vignetting",
				name="Vignetting",
				description="The optical vignetting effect of real-world cameras.",
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=1.0)

FloatProperty(  attr="vray_cam_phys_shutter_angle",
				name="Shutter angle",
				description="Shutter angle (in degrees).", # for cinema camera
				min=0.0, max=1000.0, soft_min=0.0, soft_max=10.0, default=180.0)

FloatProperty(  attr="vray_cam_phys_shutter_offset", # for cinema camera
				name="Shutter offset",
				description="Shutter offset (in degress).",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=10.0, default=0.0)

BoolProperty(   attr="vray_cam_phys_exposure",
				name="Exposure",
				description="When this option is on, the f-number, Shutter speed and ISO settings will affect the image brightness.",
				default= True)

EnumProperty(   attr="vray_cam_phys_type",
				name="Type",
				description="The type of the physical camera.",
				items=(
					("STILL",     "Still", ""),
					("CINEMATIC", "Cinematic", ""),
					("VIDEO",     "Video",  "")
				),
				default= "STILL")

BoolProperty(   attr="vray_cam_physical",
				name="Physical",
				description="Detetnimes if the camera is physical.",
				default= False)

BoolProperty(   attr="vray_cam_phys_blades_enable",
				name="Bokeh effects",
				description="Defines the shape of the camera aperture.",
				default= False)

IntProperty(    attr="vray_cam_phys_blades_num",
				name="Blades number",
				description="Number of blades.",
				min=1, max=100, default=5)

FloatProperty(  attr="vray_cam_phys_blades_rotation",
				name="Blades rotation",
				description="Defines the rotation of the blades.",
				min=0.0, max=360.0, soft_min=0.0, soft_max=10.0, default=0.0)

FloatProperty(  attr="vray_cam_phys_center_bias",
				name="Center bias",
				description="Defines a bias shape for the bokeh effects.",
				min=0.0, max=100.0, soft_min=0.0, soft_max=10.0, default=0.0)

FloatProperty(  attr="vray_cam_phys_anisotropy",
				name="Anisotropy",
				description="Allows stretching of the bokeh effect horizontally or vertically to simulate anamorphic lenses.",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)

BoolProperty(   attr="vray_cam_phys_use_dof",
				name="Depth of field",
				description="Turns on depth of field sampling.",
				default= False)

BoolProperty(   attr="vray_cam_phys_use_moblur",
				name="Motion blur",
				description="Turns on motion blur sampling.",
				default= False)

IntProperty(    attr="vray_cam_phys_subdivs",
				name="Subdivs",
				description="The number of samples for calculating depth of field and/or motion blur.",
				min=1, max=100, default=6)


'''
  GUI
'''
narrowui= 200


import properties_data_camera
properties_data_camera.DATA_PT_context_camera.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_camera.DATA_PT_camera_display.COMPAT_ENGINES.add('VRAY_RENDER')
del properties_data_camera


def base_poll(cls, context):
	rd= context.scene.render
	return (context.camera) and (rd.engine in cls.COMPAT_ENGINES)


class DataButtonsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'


class DATA_PT_vray_camera(DataButtonsPanel, bpy.types.Panel):
	bl_label = "Parameters"

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		cam= context.camera
		ca= context.camera.VRayCamera

		wide_ui= context.region.width > narrowui

		layout.prop(cam, "vray_cam_mode", expand=True)

		if not cam.vray_cam_mode == 'PHYSICAL':
			if wide_ui:
				layout.prop(cam, "type", expand=True)
			else:
				layout.prop(cam, "type", text="")

		split= layout.split()
		col= split.column()
		if cam.type == 'PERSP':
			if cam.lens_unit == 'MILLIMETERS':
				col.prop(cam, "lens", text="Angle")
			elif cam.lens_unit == 'DEGREES':
				col.prop(cam, "angle")
			if wide_ui:
				col= split.column()
			col.prop(cam, "lens_unit", text="")

		layout.separator()

		if cam.vray_cam_mode == 'PHYSICAL':
			if cam.type == 'ORTHO':
				cam.type= 'PERSP'
			
			''' CameraPhysical '''
			split= layout.split()
			col= split.column()
			col.prop(cam, "vray_cam_phys_type", text="Type")

			split= layout.split()
			col= split.column()
			col.label(text="Parameters:")

			split= layout.split()
			col= split.column(align=True)
			col.prop(cam, "vray_cam_phys_film_width")
			col.prop(cam, "vray_cam_phys_focal_length")
			col.prop(cam, "vray_cam_phys_zoom_factor")
			col.prop(cam, "vray_cam_phys_distortion")
			col.prop(cam, "vray_cam_phys_lens_shift")
			
			if wide_ui:
				col= split.column(align=True)
			col.prop(cam, "vray_cam_phys_exposure")
			if cam.vray_cam_phys_exposure:
				col.prop(cam, "vray_cam_phys_f_number")
				if cam.vray_cam_phys_type == 'STILL':
					col.prop(cam, "vray_cam_phys_shutter_speed")
				elif cam.vray_cam_phys_type == 'CINEMATIC':
					col.prop(cam, "vray_cam_phys_shutter_angle")
					col.prop(cam, "vray_cam_phys_shutter_offset")
				else:
					col.prop(cam, "vray_cam_phys_latency")
				col.prop(cam, "vray_cam_phys_ISO")

			split= layout.split()
			col= split.column()
			sub= col.row()
			sub.label(text="White balance")
			sub.prop(ca, 'white_balance',text="")
			if wide_ui:
				col= split.column()

			split= layout.split()
			colL= split.column()
			colL.label(text="Sampling:")
			
			split= layout.split()
			colL= split.column()
			colL.prop(cam, "vray_cam_phys_use_dof")
			colL.prop(cam, "vray_cam_phys_use_moblur")

			colR= split.column(align=True)
			if cam.vray_cam_phys_use_dof:
				colR.prop(cam, "vray_cam_phys_blades_enable")

			if cam.vray_cam_phys_use_moblur or cam.vray_cam_phys_use_dof:
				colL.prop(cam, "vray_cam_phys_subdivs")

				if cam.vray_cam_phys_use_dof and cam.vray_cam_phys_blades_enable:
					colR.prop(cam, "vray_cam_phys_blades_num")
					colR.prop(cam, "vray_cam_phys_blades_rotation")
					colR.prop(cam, "vray_cam_phys_center_bias")
					colR.prop(cam, "vray_cam_phys_anisotropy")
			
		else:
			''' SettingsCamera '''
			if cam.type == 'ORTHO':
				col.prop(cam, "ortho_scale")
			else:
				split= layout.split()
				colL= split.column()
				colL.label(text="Type:")
				colR= split.column()
				colR.prop(cam, "vray_cam_type", text="")

			''' SettingsCameraDof '''
			split= layout.split()
			colL= split.column()
			colR= split.column()
			
			''' SettingsMotionBlur '''
			split= layout.split()
			colL= split.column()
			colR= split.column()


		split= layout.split()

		col = split.column(align=True)
		col.label(text="Clipping:")
		col.prop(cam, "clip_start", text="Start")
		col.prop(cam, "clip_end", text="End")

		if wide_ui:
			col= split.column()
		col.label(text="Depth of Field:")
		col.prop(cam, "dof_object", text="")
		col.prop(cam, "dof_distance", text="Distance")


class DATA_PT_hide_from_view(DataButtonsPanel, bpy.types.Panel):
	bl_label = "Hide objects"
	bl_default_closed = True

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		ca= context.camera.VRayCamera
		self.layout.prop(ca, "hide_from_view", text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		sce= context.scene
		ca= context.camera.VRayCamera

		layout= self.layout
		layout.active= ca.hide_from_view

		split= layout.split()
		col= split.column()
		col.prop(ca,'hide_from_everything', text="Completely")
		if ca.hide_from_everything:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(ca,'everything_auto',text="Auto")
			sub= split.column()
			sub.active= not ca.everything_auto
			sub.prop(ca,'everything_objects')
			sub.prop(ca,'everything_groups')
		else:
			col.prop(ca,'hide_from_camera', text="From camera")
			col.prop(ca,'hide_from_gi', text="From GI")
			col.prop(ca,'hide_from_reflect', text="From reflections")
			col.prop(ca,'hide_from_refract', text="From refractions")
			col.prop(ca,'hide_from_shadows', text="From shadows")
		



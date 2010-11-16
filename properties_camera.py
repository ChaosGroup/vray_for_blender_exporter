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


class VRayCamera(bpy.types.IDPropertyGroup):
	pass

bpy.types.Camera.vray= PointerProperty(
	name= "V-Ray Camera Settings",
	type=  VRayCamera,
	description= "V-Ray Camera / DoF / Motion Blur settings."
)

VRayCamera.mode= EnumProperty(
	name= "Mode",
	description= "Camera mode.",
	items=(
		('NORMAL',   "Normal",   ""),
		('PHYSICAL', "Physical", "")
	),
	default= 'NORMAL'
)


'''
  Hide From View
'''
VRayCamera.hide_from_view= BoolProperty(
	name= "Hide From View",
	description= "Hide objects from current view.",
	default= False
)

VRayCamera.hf_all= BoolProperty(
	name= "Hide from everything",
	description= "Hide objects completely.",
	default= False
)

VRayCamera.hf_all_auto= BoolProperty(
	name= "Hide from everything (automatic)",
	description= "Create group with name \"hf_<camera-name>\".",
	default= False
)

VRayCamera.hf_all_objects= StringProperty(
	name= "Objects",
	description= "Objects to hide completely: name{;name;etc}",
	default= ""
)

VRayCamera.hf_all_groups= StringProperty(
	name= "Groups",
	description= "Groups to hide completely: name{;name;etc}",
	default= ""
)

for key in ('camera','gi','reflect','refract','shadows'):
	setattr(VRayCamera, 'hf_%s' % key, bpy.props.BoolProperty(
		name= "Hide from %s" % key,
		description= "Hide objects from %s." % key,
		default= False)
	)

	setattr(VRayCamera, 'hf_%s_auto' % key, bpy.props.BoolProperty(
		name= "Auto",
		description= "Hide objects automaically from %s." % key,
		default= False)
	)

	setattr(VRayCamera, 'hf_%s_objects' % key, bpy.props.StringProperty(
		name= "Objects",
		description= "Objects to hide from %s." % key,
		default= "")
	)

	setattr(VRayCamera, 'hf_%s_groups' % key, bpy.props.StringProperty(
		name= "Groups",
		description= "Groups to hide from %s." % key,
		default= "")
	)


'''
  SettingsCamera
'''
class SettingsCamera(bpy.types.IDPropertyGroup):
	pass

VRayCamera.SettingsCamera= PointerProperty(
	name= "SettingsCamera",
	type=  SettingsCamera,
	description= "V-Ray camera settings."
)

SettingsCamera.type= EnumProperty(
	name= "Type",
	description= "Camera type.",
	items=(
		('DEFAULT',            "Default", ""),
		('SPHERIFICAL',        "Spherifical", ""),
		('CYLINDRICAL_POINT',  "Cylindrical (point)", ""),
		('CYLINDRICAL_ORTHO',  "Cylindrical (ortho)", ""),
		('BOX',                "Box", ""),
		('FISH_EYE',           "Fish-eye", ""),
		('WARPED_SPHERICAL',   "Warped spherical", ""),
		('ORTHOGONAL',         "Orthogonal", ""),
		('PINHOLE',            "Pinhole", ""),
	),
	default= 'DEFAULT'
)

SettingsCamera.auto_fit= BoolProperty(
	name= "Auto-fit",
	description= "The auto-fit option of the fish-eye camera.",
	default= True
)

SettingsCamera.height= FloatProperty(
	name= "Height",
	description= "Height of the cylindrical (ortho) camera.",
	min=0.0, max=10000.0,
	soft_min=0.0, soft_max=10.0,
	default=400.0
)

SettingsCamera.dist= FloatProperty(
	name="Distance",
	description="Distance to the sphere center.",
	min=0.0, max=1000.0,
	soft_min=0.0, soft_max=10.0,
	default=2.0
)

SettingsCamera.curve= FloatProperty(
	name="Curve",
	description="Controls the way the rendered images is warped.",
	min=0.0, max=10.0,
	soft_min=0.0, soft_max=10.0,
	default=1.0
)


'''
  SettingsCameraDof
'''
class SettingsCameraDof(bpy.types.IDPropertyGroup):
	pass

VRayCamera.SettingsCameraDof= PointerProperty(
	name= "SettingsCameraDof",
	type=  SettingsCameraDof,
	description= "Camera's DoF settings."
)

SettingsCameraDof.on= BoolProperty(
	name= "DOF",
	description= "Use depth of field.",
	default= False
)

SettingsCameraDof.sides_on= BoolProperty(
	name="This option allows you to simulate the polygonal shape of the aperture of real-world cameras.",
	description="Enable Bokeh effects.",
	default= False
)

SettingsCameraDof.sides_num= IntProperty(
	name="Number",
	description="Number of sides.",
	min=1, max=100,
	default=5
)

SettingsCameraDof.subdivs= IntProperty(
	name="Subdivs",
	description="Controls the quality of the DOF effect.",
	min=1, max=100,
	default=8
)

SettingsCameraDof.anisotropy= FloatProperty(
	name="Anisotropy",
	description="This allows the stretching of the bokeh effect horizontally or vertically.",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default=0.0
)

SettingsCameraDof.focal_dist= FloatProperty(
	name="Focal distance",
	description="Determines the distance from the camera at which objects will be in perfect focus.",
	min=0.0, max=1000.0,
	soft_min=0.0, soft_max=10.0,
	default=200.0
)

SettingsCameraDof.aperture= FloatProperty(
	name="Aperture",
	description="The size of the virtual camera aperture, in world units.",
	min=0.0, max=100.0,
	soft_min=0.0, soft_max=10.0,
	default=5.0
)

SettingsCameraDof.center_bias= FloatProperty(
	name="Center bias",
	description="This determines the uniformity of the DOF effect.",
	min=0.0, max=100.0,
	soft_min=0.0, soft_max=10.0,
	default=0.0
)

SettingsCameraDof.rotation= FloatProperty(
	name="Rotation",
	description="Specifies the orientation of the aperture shape.",
	min=0.0, max=10.0,
	soft_min=0.0, soft_max=10.0,
	default=0.0
)


'''
  SettingsMotionBlur
'''
class SettingsMotionBlur(bpy.types.IDPropertyGroup):
	pass

VRayCamera.SettingsMotionBlur= PointerProperty(
	name= "SettingsMotionBlur",
	type=  SettingsMotionBlur,
	description= "Camera's Motion Blur settings."
)

SettingsMotionBlur.on= BoolProperty(
	name="Motion blur",
	description="Turns motion blur on.",
	default= False
)

SettingsMotionBlur.interval_center= FloatProperty(
	name="Interval center",
	description="Specifies the middle of the motion blur interval with respect to the frame.",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default=0.5
)

SettingsMotionBlur.duration= FloatProperty(
	name="Duration",
	description="Specifies the duration, in frames, during which the camera shutter is open.",
	min=0.0, max=100.0,
	soft_min=0.0, soft_max=10.0,
	default=1.0
)

SettingsMotionBlur.bias= FloatProperty(
	name="Bias",
	description="This controls the bias of the motion blur effect.",
	min=0.0, max=1.0,
	soft_min=0.0, soft_max=1.0,
	default=0.0
)

SettingsMotionBlur.subdivs= IntProperty(
	name="Subdivs",
	description="Determines the quality of the motion blur.",
	min=1, max=100,
	default=6
)

SettingsMotionBlur.geom_samples= IntProperty(
	name="Geometry samples",
	description="This determines the number of geometry segments used to approximate motion blur.",
	min=1, max=100,
	default=2
)

SettingsMotionBlur.low_samples= IntProperty(
	name="Low samples",
	description="This controls how many samples in time will be computed during irradiance map calculations.",
	min=1, max=100,
	default=1
)

'''
  CameraPhysical
'''
class CameraPhysical(bpy.types.IDPropertyGroup):
	pass

VRayCamera.CameraPhysical= PointerProperty(
	name= "CameraPhysical",
	type=  CameraPhysical,
	description= "Physical Camera settings."
)

CameraPhysical.use= BoolProperty(
	name= "Enable physical camera",
	description= "Enable physical camera.",
	default= False
)

CameraPhysical.f_number= FloatProperty(
	name= "F-number",
	description= "Determines the width of the camera aperture and, indirectly, exposure.",
	min=0.0, max=1000.0,
	soft_min=0.0, soft_max=10.0,
	default= 8.0
)

CameraPhysical.white_balance= FloatVectorProperty(
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

CameraPhysical.latency= FloatProperty(
	name="Latency",
	description="CCD matrix latency, in seconds.",  # for video camera
	min=0.0, max=100.0,
	soft_min=0.0, soft_max=10.0,
	default=0.0
)

CameraPhysical.lens_shift= FloatProperty(
	name="Lens shift",
	description="Shift lenses for 2-point perspective.",
	min=0.0,      max=1.0,
	soft_min=0.0, soft_max=1.0,
	default=0.0
)

CameraPhysical.ISO= FloatProperty(
	name="ISO",
	description="The film power (i.e. sensitivity).",
	min=0.0,
	max=10000.0,
	soft_min=0.0,
	soft_max=100.0,
	default=200.0
)

CameraPhysical.shutter_speed= FloatProperty(
	name="Shutter speed",
	description="The shutter speed, in inverse seconds.", # for still camera
	min= 1.0,
	max= 1000.0,
	soft_min=0.0,
	soft_max=1000.0,
	default=300.0
)

CameraPhysical.focal_length= FloatProperty(
	name="Focal length",
	description="Specifies the equivalen focal length of the camera lens.",
	min=0.0,
	max=200.0,
	soft_min=0.0,
	soft_max=10.0,
	default=40.0
)

CameraPhysical.dof_display_threshold= FloatProperty(
	name="DOF threshold",
	description="Display threshold for depth-of-field.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=0.0
)

CameraPhysical.distortion= FloatProperty(
	name="Distortion",
	description="Specifies the distortion coefficient for the camera lens.",
	min=-1.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=0.0
)

CameraPhysical.distortion_type= IntProperty(
	name="Distortion type",
	description="",
	min=0,
	max=2,
	default=0
)

CameraPhysical.zoom_factor= FloatProperty(
	name="Zoom factor",
	description="Zoom factor.",
	min=0.0,
	max=10.0,
	soft_min=0.0,
	soft_max=10.0,
	default=1.0
)

CameraPhysical.film_width= FloatProperty(
	name="Film width",
	description="Specifies the horizontal size of the film gate in milimeters.",
	min=0.0,
	max=200.0,
	soft_min=0.0,
	soft_max=10.0,
	default=36.0
)

CameraPhysical.vignetting= FloatProperty(
	name="Vignetting",
	description="The optical vignetting effect of real-world cameras.",
	min=0.0,
	max=100.0,
	soft_min=0.0,
	soft_max=10.0,
	default=1.0
)

CameraPhysical.shutter_angle= FloatProperty(
	name="Shutter angle",
	description="Shutter angle (in degrees).", # for cinema camera
	min=0.0,
	max=1000.0,
	soft_min=0.0,
	soft_max=10.0,
	default=180.0
)

CameraPhysical.shutter_offset= FloatProperty(
	name="Shutter offset",
	description="Shutter offset (in degress).", # for cinema camera
	min=0.0,
	max=1000.0,
	soft_min=0.0,
	soft_max=10.0,
	default=0.0
)

CameraPhysical.exposure= BoolProperty(
	name="Exposure",
	description="When this option is on, the f-number, Shutter speed and ISO settings will affect the image brightness.",
	default= True
)

CameraPhysical.guess_lens_shift= BoolProperty(
	name= "Guess lens shift",
	description= "Guess lens shift.",
	default= False
)

CameraPhysical.type= EnumProperty(
	name="Type",
	description="The type of the physical camera.",
	items=(
		('STILL',     "Still",     ""),
		('CINEMATIC', "Cinematic", ""),
		('VIDEO',     "Video",     "")
	),
	default= 'STILL'
)

CameraPhysical.blades_enable= BoolProperty(
	name="Bokeh effects",
	description="Defines the shape of the camera aperture.",
	default= False
)

CameraPhysical.blades_num= IntProperty(
	name="Blades number",
	description="Number of blades.",
	min=1,
	max=100,
	default=5
)

CameraPhysical.blades_rotation= FloatProperty(
	name="Blades rotation",
	description="Defines the rotation of the blades.",
	min=0.0,
	max=360.0,
	soft_min=0.0,
	soft_max=10.0,
	default=0.0
)

CameraPhysical.center_bias= FloatProperty(
	name="Center bias",
	description="Defines a bias shape for the bokeh effects.",
	min=0.0,
	max=100.0,
	soft_min=0.0,
	soft_max=10.0,
	default=0.0
)

CameraPhysical.anisotropy= FloatProperty(
	name="Anisotropy",
	description="Allows stretching of the bokeh effect horizontally or vertically to simulate anamorphic lenses.",
	min=0.0,
	max=1.0,
	soft_min=0.0,
	soft_max=1.0,
	default=0.0
)

CameraPhysical.use_dof= BoolProperty(
	name="Depth of field",
	description="Turns on depth of field sampling.",
	default= False
)

CameraPhysical.use_moblur= BoolProperty(
	name="Motion blur",
	description="Turns on motion blur sampling.",
	default= False
)

CameraPhysical.subdivs= IntProperty(
	name="Subdivs",
	description="The number of samples for calculating depth of field and/or motion blur.",
	min=1,
	max=100,
	default=6
)



'''
  GUI
'''
narrowui= 200


import properties_data_camera
properties_data_camera.DATA_PT_context_camera.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_camera.DATA_PT_context_camera.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
properties_data_camera.DATA_PT_camera_display.COMPAT_ENGINES.add('VRAY_RENDER')
properties_data_camera.DATA_PT_camera_display.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
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

		ca= context.camera

		VRayCamera= ca.vray
		SettingsCamera= VRayCamera.SettingsCamera
		SettingsCameraDof= VRayCamera.SettingsCameraDof
		SettingsMotionBlur= VRayCamera.SettingsMotionBlur

		wide_ui= context.region.width > narrowui

		if wide_ui:
			layout.prop(ca, 'type', expand=True)
		else:
			layout.prop(ca, 'type', text="")

		split= layout.split()
		col= split.column()
		if ca.type == 'PERSP':
			if ca.lens_unit == 'MILLIMETERS':
				col.prop(ca, 'lens', text="Angle")
			elif ca.lens_unit == 'DEGREES':
				col.prop(ca, 'angle')
			if wide_ui:
				col= split.column()
			col.prop(ca, 'lens_unit', text="")

		layout.separator()

		'''
			SettingsCamera
		'''
		if ca.type == 'ORTHO':
			col.prop(ca, 'ortho_scale')
		else:
			split= layout.split()
			col= split.column()
			col.label(text="Type:")
			col= split.column()
			col.prop(SettingsCamera, 'type', text="")

		layout.separator()

		'''
			SettingsCameraDof
		'''
		# split= layout.split()
		# col= split.column()
		# col= split.column()

		'''
			SettingsMotionBlur
		'''
		# split= layout.split()
		# col= split.column()
		# col= split.column()

		split= layout.split()
		col = split.column(align=True)
		col.label(text="Clipping:")
		col.prop(ca, 'clip_start', text="Start")
		col.prop(ca, 'clip_end', text="End")
		if wide_ui:
			col= split.column()
		col.label(text="Depth of Field:")
		col.prop(ca, 'dof_object', text="")
		col.prop(ca, 'dof_distance', text="Distance")


class VRAY_CAMERA_physical(DataButtonsPanel, bpy.types.Panel):
	bl_label   = "Physical"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		ca= context.camera
		VRayCamera= ca.vray
		CameraPhysical= VRayCamera.CameraPhysical
		self.layout.prop(CameraPhysical, 'use', text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		ca= context.camera
		VRayCamera= ca.vray
		CameraPhysical= VRayCamera.CameraPhysical

		layout= self.layout
		layout.active= CameraPhysical.use

		split= layout.split()
		col= split.column()
		col.prop(CameraPhysical, 'type', text="Type")

		split= layout.split()
		col= split.column()
		col.label(text="Parameters:")

		split= layout.split()
		col= split.column(align=True)
		col.prop(CameraPhysical, 'film_width')
		col.prop(CameraPhysical, 'focal_length')
		col.prop(CameraPhysical, 'zoom_factor')
		col.prop(CameraPhysical, 'distortion')
		if not CameraPhysical.guess_lens_shift:
			col.prop(CameraPhysical, 'lens_shift')
		col.prop(CameraPhysical, 'guess_lens_shift')
		if wide_ui:
			col= split.column(align=True)
		col.prop(CameraPhysical, 'exposure')
		if CameraPhysical.exposure:
			col.prop(CameraPhysical, 'f_number')
			if CameraPhysical.type == 'STILL':
				col.prop(CameraPhysical, 'shutter_speed')
			elif CameraPhysical.type == 'CINEMATIC':
				col.prop(CameraPhysical, 'shutter_angle')
				col.prop(CameraPhysical, 'shutter_offset')
			else:
				col.prop(CameraPhysical, 'latency')
			col.prop(CameraPhysical, 'ISO')

		split= layout.split()
		col= split.column()
		sub= col.row()
		sub.label(text="White balance")
		sub.prop(CameraPhysical, 'white_balance', text="")

		if wide_ui:
			col= split.column()

		col.prop(CameraPhysical, 'vignetting')

		split= layout.split()
		colL= split.column()
		colL.label(text="Sampling:")

		split= layout.split()
		colL= split.column()
		colR= split.column(align=True)

		colL.prop(CameraPhysical, 'use_dof')
		colL.prop(CameraPhysical, 'use_moblur')

		if CameraPhysical.use_dof:
			colR.prop(CameraPhysical, 'blades_enable')

		if CameraPhysical.use_moblur or CameraPhysical.use_dof:
			colL.prop(CameraPhysical, 'subdivs')

			if CameraPhysical.use_dof and CameraPhysical.blades_enable:
				colR.prop(CameraPhysical, 'blades_num')
				colR.prop(CameraPhysical, 'blades_rotation')
				colR.prop(CameraPhysical, 'center_bias')
				colR.prop(CameraPhysical, 'anisotropy')


class VRAY_CAMERA_hide_from_view(DataButtonsPanel, bpy.types.Panel):
	bl_label   = "Hide objects"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		ca= context.camera
		VRayCamera= ca.vray
		self.layout.prop(VRayCamera, 'hide_from_view', text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		ca= context.camera
		VRayCamera= ca.vray

		layout= self.layout
		layout.active= VRayCamera.hide_from_view

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_all', text="Completely")
		if VRayCamera.hf_all:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_all_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_all_auto
			sub.prop_search(VRayCamera, 'hf_all_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_all_groups',   bpy.data,      'groups')

			layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_camera', text="From camera")
		if VRayCamera.hf_camera:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_camera_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_camera_auto
			sub.prop_search(VRayCamera, 'hf_camera_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_camera_groups',   bpy.data,      'groups')

			layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_gi', text="From GI")
		if VRayCamera.hf_gi:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_gi_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_gi_auto
			sub.prop_search(VRayCamera, 'hf_gi_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_gi_groups',   bpy.data,      'groups')

			layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_reflect', text="From reflections")
		if VRayCamera.hf_reflect:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_reflect_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_reflect_auto
			sub.prop_search(VRayCamera, 'hf_reflect_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_reflect_groups',   bpy.data,      'groups')

			layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_refract', text="From refractions")
		if VRayCamera.hf_refract:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_refract_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_refract_auto
			sub.prop_search(VRayCamera, 'hf_refract_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_refract_groups',   bpy.data,      'groups')

			layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayCamera, 'hf_shadows', text="From shadows")
		if VRayCamera.hf_shadows:
			split= layout.split(percentage=0.2)
			col= split.column()
			col.prop(VRayCamera, 'hf_shadows_auto', text="Auto")
			sub= split.column()
			sub.active= not VRayCamera.hf_shadows_auto
			sub.prop_search(VRayCamera, 'hf_shadows_objects',  context.scene, 'objects')
			sub.prop_search(VRayCamera, 'hf_shadows_groups',   bpy.data,      'groups')

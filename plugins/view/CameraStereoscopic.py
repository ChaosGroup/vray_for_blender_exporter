#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Maxim Seliverstoff
#
# Contributor: Andrei Izrantcev
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

import math

import bpy
import mathutils

from bpy.props import *

from vb30.lib import LibUtils


TYPE = 'CAMERA'
ID   = 'CameraStereoscopic'
NAME = 'Stereoscopic camera'
DESC = "V-Ray CameraStereoscopic settings"

PARAMS = (
	'stereo_base',
	'stereo_distance',
	'use_convergence',
)


def stereoRigUpdate(self, context):
	# Dirty hack to update stereo rig drivers
	context.scene.frame_set(context.scene.frame_current)


class CameraStereoscopic(bpy.types.PropertyGroup):
	use = BoolProperty(
		name        = "Enable Stereoscopic camera",
		description = "Enable Stereoscopic camera",
		default     = False
	)

	sucess_create = BoolProperty(
		name        = "flag",
		description = "flag",
		default     = False
	)

	use_convergence = BoolProperty(
		name        = "Use Convergence",
		description = "",
		default     = False,
		update      = stereoRigUpdate
	)

	stereo_base = FloatProperty(
		name        = "Eye Distance",
		description = "Determines the width of the camera aperture and, indirectly, exposure",
		min         = 0.0,
		max         = 100.0,
		soft_min    = 0.0,
		soft_max    = 1.0,
		precision   = 4,
		default     = 0.065,
		update      = stereoRigUpdate
	)

	stereo_distance= FloatProperty(
		name        = "Distance",
		description = "Determines the width of the camera aperture and, indirectly, exposure",
		min         = 0.0,
		max         = 100000.0,
		soft_min    = 0.0,
		soft_max    = 100.0,
		default     = 20.0,
		update      = stereoRigUpdate
	)

	LeftCam = StringProperty(
		name        = "LeftCam",
		description = "",
		default     = ""
	)

	RightCam = StringProperty(
		name        = "RightCam",
		description = "",
		default     = ""
	)

	TargetCam = StringProperty(
		name        = "TargetCam",
		description = "",
		default     = ""
	)

	show_limits = BoolProperty(
		name        = "Show Limits",
		description = "",
		default     = True,
		update      = stereoRigUpdate
	)

	show_cams = BoolProperty(
		name        = "Show L/R cameras",
		description = "",
		default     = True,
		update      = stereoRigUpdate
	)

	def CalcAngle(self, cam):
		stereo_base = cam.stereo_base
		focal_dist  = cam.stereo_distance
		if cam.use_convergence:
			return math.degrees(math.atan2((stereo_base/2), focal_dist))
		return 0.0


def create_stereo_cam(context):
	cam = context.object

	# print(cam.name)

	cam_obj = context.camera

	bpy.ops.object.add(type='CAMERA')
	left_cam = bpy.context.active_object
	left_cam.name = 'LeftCam'
	left_cam.parent = cam
	left_cam.lock_rotation = [True, True, True]
	left_cam.lock_scale = [True, True, True]
	left_cam.lock_location = [True, True, True]
	left_cam.location = [0,0,0]
	left_cam_obj = left_cam.data

	left_cam_obj.show_limits = True
	left_cam_obj.draw_size = cam_obj.draw_size
	cam_obj.vray.CameraStereoscopic.LeftCam = left_cam.name

	bpy.ops.object.add(type='CAMERA')
	right_cam = bpy.context.active_object
	right_cam.name = 'RightCam'
	right_cam.parent = cam
	right_cam.lock_rotation = [True, True, True]
	right_cam.lock_scale = [True, True, True]
	right_cam.lock_location = [True, True, True]
	right_cam.location = [0,0,0]
	right_cam_obj = right_cam.data
	right_cam_obj.show_limits = True
	right_cam_obj.draw_size = cam_obj.draw_size
	cam_obj.vray.CameraStereoscopic.RightCam = right_cam.name

	bpy.ops.object.add(type='EMPTY')
	target_cam = bpy.context.active_object
	target_cam.name = 'ZeroParallax'
	target_cam.empty_draw_size = 0.2
	target_cam.parent = cam
	target_cam.lock_rotation = [True, True, True]
	target_cam.lock_scale = [True, True, True]
	target_cam.lock_location = [True, True, True]
	target_cam.location = [0,0,-5]
	cam_obj.vray.CameraStereoscopic.TargetCam = target_cam.name

	left_cam_obj.dof_object = target_cam
	right_cam_obj.dof_object = target_cam

	left_cam_driver = left_cam_obj.driver_add('lens').driver
	left_cam_driver.type = 'SCRIPTED'
	left_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].lens"

	left_cam_driver = left_cam_obj.driver_add('show_limits').driver
	left_cam_driver.type = 'SCRIPTED'
	left_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.show_limits"

	left_cam_driver = left_cam.driver_add('rotation_euler',1).driver
	left_cam_driver.type = 'SCRIPTED'
	left_cam_driver.expression = "-radians(bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.CalcAngle(bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic))"

	left_cam_driver = left_cam.driver_add('hide').driver
	left_cam_driver.type = 'SCRIPTED'
	left_cam_driver.expression = "not bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.show_cams"

	right_cam_driver = right_cam_obj.driver_add('lens').driver
	right_cam_driver.type = 'SCRIPTED'
	right_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].lens"

	right_cam_driver = right_cam_obj.driver_add('show_limits').driver
	right_cam_driver.type = 'SCRIPTED'
	right_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.show_limits"

	right_cam_driver = right_cam.driver_add('rotation_euler',1).driver
	right_cam_driver.type = 'SCRIPTED'
	right_cam_driver.expression = "radians(bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.CalcAngle(bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic))"

	right_cam_driver = right_cam.driver_add('hide').driver
	right_cam_driver.type = 'SCRIPTED'
	right_cam_driver.expression = "not bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.show_cams"

	left_cam_driver = left_cam.driver_add('location',0).driver
	left_cam_driver.type = 'SCRIPTED'
	left_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.stereo_base/2*-1"

	right_cam_driver = right_cam.driver_add('location',0).driver
	right_cam_driver.type = 'SCRIPTED'
	right_cam_driver.expression = "bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.stereo_base/2"

	target_cam_driver = target_cam.driver_add('location',2).driver
	target_cam_driver.type = 'SCRIPTED'
	target_cam_driver.expression = "-bpy.data.cameras['"+cam_obj.name+"'].vray.CameraStereoscopic.stereo_distance"

	left_cam.hide_select   = True
	left_cam.hide_render   = True
	right_cam.hide_select  = True
	right_cam.hide_render  = True
	target_cam.hide_select = True
	target_cam.hide_render = True

	target_cam.select = False
	cam.select = True
	bpy.context.scene.objects.active = cam


def writeCamera(bus, camera, tm):
	o = bus['output']

	camName = LibUtils.CleanString(camera.name)

	o.set('CAMERA', 'RenderView', camName)
	o.writeHeader()
	o.writeAttibute("transform", tm)
	o.writeFooter()


def write(bus):
	scene  = bus['scene']
	camera = bus['camera']

	VRayScene      = scene.vray
	StereoSettings = VRayScene.VRayStereoscopicSettings

	VRayCamera = camera.data.vray
	CameraStereoscopic = VRayCamera.CameraStereoscopic

	if CameraStereoscopic.use and StereoSettings.use:
		camera_left  = bpy.data.objects.get(CameraStereoscopic.LeftCam)
		camera_right = bpy.data.objects.get(CameraStereoscopic.RightCam)

		writeCamera(bus, camera_left,  matrix_recalc(bus, camera_left,  "left"))
		writeCamera(bus, camera_right, matrix_recalc(bus, camera_right, "right"))


def matrix_recalc(bus, cam, pos):
	scene  = bus['scene']
	camera = bus['camera']

	VRayScene      = scene.vray
	StereoSettings = VRayScene.VRayStereoscopicSettings

	VRayCamera = camera.data.vray
	CameraStereoscopic = VRayCamera.CameraStereoscopic

	if pos == "left":
		shift = mathutils.Matrix.Translation((-CameraStereoscopic.stereo_base, 0, 0))
		mat_world = cam.matrix_world * shift
	else:
		mat_world = cam.matrix_world

	loc_w, rot_w, scale_w = mat_world.decompose()

	mat = cam.matrix_local
	loc, rot, scale = mat.decompose()
	mat_rot = rot_w.to_matrix()
	mat_rot = mat_rot.to_4x4()

	mat_loc = mathutils.Matrix.Translation((loc_w/2))

	if StereoSettings.adjust_resolution and StereoSettings.sm_mode != 'RENDER':
		mat_sca = mathutils.Matrix.Scale(2, 4, (0.0, 1.0, 0.0))
	else:
		mat_sca = mathutils.Matrix.Scale(1, 4)

	mat_out = mat_loc * mat_rot * mat_sca

	return mat_out


def remove_stereo_cam(context):
	cam_obj = context.camera.vray.CameraStereoscopic
	remove_obj(cam_obj.LeftCam)
	remove_obj(cam_obj.RightCam)
	remove_obj(cam_obj.TargetCam)


def remove_obj(name):
	ob = bpy.data.objects.get(name)

	for sce in bpy.data.scenes:
		try:
			sce.objects.unlink(ob)
		except:
			pass

	if ob.type != 'EMPTY':
		bpy.data.objects.remove(ob)


class VRAY_OT_create_stereo_cam(bpy.types.Operator):
	bl_idname      = 'vray.create_stereo_cam'
	bl_label       = "Show Stereo Camera"
	bl_description = "Create Visual model Stereo Camera"

	def execute(self, context):
		VRayCamera = context.camera.vray
		CameraStereoscopic = VRayCamera.CameraStereoscopic

		if not CameraStereoscopic.use:
			CameraStereoscopic.use = True
			create_stereo_cam(context)
		else:
			CameraStereoscopic.use = False
			remove_stereo_cam(context)

		return {'FINISHED'}


def GetRegClasses():
	return (
		CameraStereoscopic,
		VRAY_OT_create_stereo_cam,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)

	bpy.types.VRayCamera.CameraStereoscopic = bpy.props.PointerProperty(
		name        = "CameraStereoscopic",
		type        =  CameraStereoscopic,
		description = "Stereoscopic Camera settings"
	)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

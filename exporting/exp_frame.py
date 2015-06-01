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

import _vray_for_blender

from vb30 import debug
from vb30.lib import BlenderUtils

from . import exp_init
from . import exp_scene
from . import exp_anim_full


def GetCameraPhysicalMotionBlurFrames(bus):
    scene, camera = BlenderUtils.GetSceneAndCamera(bus)

    CameraPhysical = camera.data.vray.CameraPhysical

    mb_duration        = None
    mb_interval_center = None

    frameDuration = 1.0 / (scene.render.fps / scene.render.fps_base)

    # Still camera - use the shutter speed
    if CameraPhysical.type == '0':
        mb_duration        = 1.0 / (CameraPhysical.shutter_speed * frameDuration)
        mb_interval_center = mb_duration * 0.5;

    # Cinematic camera
    elif CameraPhysical.type == '1':
        mb_duration        = CameraPhysical.shutter_angle / 360.0
        mb_interval_center = CameraPhysical.shutter_offset / 360.0 + mb_duration * 0.5

    # Video camera
    elif CameraPhysical.type == '2':
        mb_duration        = 1.0 + CameraPhysical.latency / frameDuration
        mb_interval_center = -mb_duration * 0.5

    return mb_duration, mb_interval_center


def GetMotionBlurFrames(bus):
    scene, camera = BlenderUtils.GetSceneAndCamera(bus)

    VRayCamera = camera.data.vray

    CameraPhysical     = VRayCamera.CameraPhysical
    SettingsMotionBlur = VRayCamera.SettingsMotionBlur

    mb_duration        = None
    mb_interval_center = None

    if CameraPhysical.use and CameraPhysical.use_moblur:
        mb_duration, mb_interval_center = GetCameraPhysicalMotionBlurFrames(bus)
    elif SettingsMotionBlur.on:
        mb_duration        = SettingsMotionBlur.duration
        mb_interval_center = SettingsMotionBlur.interval_center

    return mb_duration, mb_interval_center


@debug.TimeIt
def ExportSingleFrame(bus):
    o      = bus['output']
    scene  = bus['scene']

    err = None

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    mb_duration, mb_interval_center = GetMotionBlurFrames(bus)

    if mb_duration:
        debug.Debug("MB Duration: %.3f sec" % mb_duration)
        debug.Debug("MB Interval Center: %.3f sec" % mb_interval_center)

        if mb_duration < 1.0:
            mb_duration = 1.0

        # We need to export +1 frames data
        mb_duration += 1

        frameStart = scene.frame_current
        frameEnd   = frameStart + mb_duration - 1
        frameStep  = scene.frame_step

        o.setAnimation(True)
        o.setFrameStart(frameStart)
        o.setFrameEnd(frameEnd)
        o.setFrameStep(frameStep)

        err = exp_anim_full.ExportFullRange(bus)

    else:
        _vray_for_blender.setFrame(scene.frame_current)
        err = exp_scene.ExportScene(bus)

    return err

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

import bpy

from vb30.lib import ExportUtils
from vb30.lib import SysUtils
from vb30.lib import BlenderUtils
from vb30.lib import PluginUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    o = bus['output']

    scene, ca = BlenderUtils.GetSceneAndCamera(bus)

    VRayScene = scene.vray
    VRayBake  = VRayScene.BakeView

    if VRayBake.use:
        return

    VRayCamera = ca.data.vray
    RenderView = VRayCamera.RenderView
    SettingsCamera = VRayCamera.SettingsCamera
    SettingsCameraDof = VRayCamera.SettingsCameraDof
    CameraStereoscopic = VRayCamera.CameraStereoscopic
    VRayStereoscopicSettings = VRayScene.VRayStereoscopicSettings

    fov, orthoWidth = BlenderUtils.GetCameraFOV(scene, ca)

    overrideParams['use_scene_offset'] = SysUtils.IsRTEngine(bus)
    overrideParams['clipping'] = RenderView.clip_near or RenderView.clip_far

    # if SettingsCamera.type not in {'SPHERIFICAL', 'BOX'}:
    if RenderView.clip_near:
        overrideParams['clipping_near'] = ca.data.clip_start
    if RenderView.clip_far:
        overrideParams['clipping_far'] = ca.data.clip_end

    if 'fov' not in overrideParams:
        overrideParams['fov'] = fov
    if 'transform' not in overrideParams:
        overrideParams['transform'] = ca.matrix_world.normalized()
    if 'orthographic' not in overrideParams:
        overrideParams['orthographic'] = ca.data.type == 'ORTHO'
    overrideParams['orthographicWidth'] = orthoWidth

    overrideParams['focalDistance'] = BlenderUtils.GetCameraDofDistance(ca)
    overrideParams['aperture']      = SettingsCameraDof.aperture

    if VRayStereoscopicSettings.use and not CameraStereoscopic.use:
        overrideParams['stereo_on']                 = True
        overrideParams['stereo_eye_distance']       = VRayStereoscopicSettings.eye_distance
        overrideParams['stereo_interocular_method'] = VRayStereoscopicSettings.interocular_method
        overrideParams['stereo_specify_focus']      = VRayStereoscopicSettings.specify_focus
        overrideParams['stereo_focus_distance']     = VRayStereoscopicSettings.focus_distance
        overrideParams['stereo_focus_method']       = VRayStereoscopicSettings.focus_method
        overrideParams['stereo_view']               = VRayStereoscopicSettings.view
    else:
        overrideParams['stereo_on']                 = None
        overrideParams['stereo_eye_distance']       = None
        overrideParams['stereo_interocular_method'] = None
        overrideParams['stereo_specify_focus']      = None
        overrideParams['stereo_focus_distance']     = None
        overrideParams['stereo_focus_method']       = None
        overrideParams['stereo_view']               = None

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

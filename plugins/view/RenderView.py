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

from vb30.lib import ExportUtils, SysUtils, BlenderUtils


TYPE = 'CAMERA'
ID   = 'RenderView'
NAME = 'Render view'
DESC = "Render view settings"

PluginParams = (
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'fov',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.785398,
    },
    {
        'attr' : 'focalDistance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'aperture',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'lens_rotation',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'frame_samples',
        'desc' : "Number of samples per frame for the transformation",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'clipping',
        'desc' : "true to enable clipping planes",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'clipping_near',
        'desc' : "The near clipping plane",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'clipping_far',
        'desc' : "The far clipping plane",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'zoom',
        'desc' : "Zoom factor",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'orthographic',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'orthographicWidth',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'dont_affect_settings',
        'desc' : "This is here so we can suppress a RenderView node from affecting the main VRayRenderer sequence and frame data",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_scene_offset',
        'desc' : "If true, the scene will be internally translated relative to the render view",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mayaFocalLength',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'mayaApperture',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'stereo_on',
        'desc' : "Enable stereo rendering",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'stereo_eye_distance',
        'desc' : "The distance between the two stereo views",
        'type' : 'FLOAT',
        'default' : 0.065,
    },
    {
        'attr' : 'stereo_interocular_method',
        'desc' : "Specifies the camera position relative to the left and right views",
        'type' : 'ENUM',
        'items' : (
            ('0', "Center",     ""),
            ('1', "Keep Left",  ""),
            ('2', "Keep Right", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'stereo_specify_focus',
        'desc' : "Specify a separate distance for the stereo focus",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'stereo_focus_distance',
        'desc' : "The focus distance",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'stereo_focus_method',
        'desc' : "The focus method",
        'type' : 'ENUM',
        'items' : (
            ('0', "Parallel", "Both cameras have their focus points directly in front of them"),
            ('1', "Rotation", "The stereoscopy is achieved by rotating the left and right views so that their focus points coincide at the distance from the eyes where the lines of sight for each eye converge called fusion distance"),
            ('2', "Shear",    "The orientation of both views remain the same but each eyes view is sheared along Z so that the two frustums converge at the fusion distance"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'stereo_view',
        'desc' : "Specifies which view to render",
        'type' : 'ENUM',
        'items' : (
            ('0', "Both",  "Both views will be rendered side by side"),
            ('1', "Left",  "Only the left view will be rendered"),
            ('2', "Right", "Only the right view will be rendered")
        ),
        'default' : '0',
    },

    {
        'attr' : 'clip_near',
        'desc' : "Clip near",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
    {
        'attr' : 'clip_far',
        'desc' : "Clip far",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    o = bus['output']
    scene = bus['scene']
    ca    = bus['camera']

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

    fov, orthoWidth = BlenderUtils.GetCameraFOV(ca)

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

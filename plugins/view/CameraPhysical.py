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
import math

from vb30.lib import ExportUtils, LibUtils, BlenderUtils


TYPE = 'CAMERA'
ID   = 'CameraPhysical'
NAME = 'Physical Camera'
DESC = "V-Ray physical camera settings"

PluginParams = (
    {
        'attr' : 'type',
        'desc' : "Camera type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Still",     ""),
            ('1', "Cinematic", ""),
            ('2', "Video",     ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'film_width',
        'desc' : "Specifies the horizontal size of the film gate in milimeters",
        'type' : 'FLOAT',
        'default' : 36,
    },
    {
        'attr' : 'focal_length',
        'desc' : "Specifies the equivalen focal length of the camera lens",
        'type' : 'FLOAT',
        'default' : 40,
    },
    {
        'attr' : 'zoom_factor',
        'desc' : "Zoom factor",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'distortion',
        'desc' : "Specifies the distortion coefficient for the camera lens",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'distortion_type',
        'desc' : "Distortion type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Quadratic", ""),
            ('1', "Cubic", ""),
            ('2', "Lens File", ""),
            # ('3', "Texture", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'f_number',
        'name' : "F-Number",
        'desc' : "Determines the width of the camera aperture and, indirectly, exposure",
        'type' : 'FLOAT',
        'default' : 8,
    },
    {
        'attr' : 'lens_shift',
        'desc' : "Shift lenses for 2-point perspective",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'shutter_speed',
        'desc' : "The shutter speed, in inverse seconds",
        'type' : 'FLOAT',
        'default' : 300,
    },
    {
        'attr' : 'shutter_angle',
        'desc' : "Shutter angle (in degrees)",
        'type' : 'FLOAT',
        'default' : 180,
    },
    {
        'attr' : 'shutter_offset',
        'desc' : "Shutter offset (in degress)",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'latency',
        'desc' : "CCD matrix latency, in seconds",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ISO',
        'name' : "ISO",
        'desc' : "The film power (i.e. sensitivity)",
        'type' : 'FLOAT',
        'default' : 200,
    },
    {
        'attr' : 'specify_focus',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'focus_distance',
        'desc' : "focus distance in mm",
        'type' : 'FLOAT',
        'default' : 200,
    },
    {
        'attr' : 'targeted',
        'desc' : "1-specify a target distance; 0-target distance not specified",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'target_distance',
        'desc' : "target distance",
        'type' : 'FLOAT',
        'default' : 200,
    },
    {
        'attr' : 'dof_display_threshold',
        'desc' : "Display threshold for depth-of-field",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'exposure',
        'desc' : "When this option is on, the F-Number, Shutter Speed and ISO settings will affect the image brightness",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'white_balance',
        'desc' : "White balance",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'vignetting',
        'desc' : "Strength of vignetting effect",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'blades_enable',
        'desc' : "Enable Bokeh effects",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'blades_num',
        'desc' : "Number of blades (0 means its disabled)",
        'type' : 'INT',
        'ui' : {
            'min' : 0,
        },
        'default' : 5,
    },
    {
        'attr' : 'blades_rotation',
        'desc' : "Defines the rotation of the blades (in radians)",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'center_bias',
        'desc' : "Defines a bias shape for the bokeh effects",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'anisotropy',
        'desc' : "Allows stretching of the bokeh effect horizontally or vertically to simulate anamorphic lenses",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'use_dof',
        'name' : "Use DOF",
        'desc' : "Turns on depth of field sampling",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_moblur',
        'name' : "Use Motion Blur",
        'desc' : "Turns on motion blur sampling",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivs',
        'desc' : "The number of samples for calculating depth of field and/or motion blur",
        'type' : 'INT',
        'default' : 6,
    },
    {
        'attr' : 'dont_affect_settings',
        'desc' : "This is here so we can suppress a PhysicalCamera node from affecting the main VRayRenderer sequence and frame data",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'lens_file',
        'desc' : "LENS file with camera lens-type image distortion description",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'specify_fov',
        'desc' : "Use field of view instead of use the focal length, film width, scale etc",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'fov',
        'desc' : "the FOV value (in radians) to use when specify_fov is true",
        'type' : 'FLOAT',
        'default' : 1.5708,
    },
    {
        'attr' : 'horizontal_shift',
        'desc' : "the horizontal lens shift",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'horizontal_offset',
        'desc' : "The horizontal offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'vertical_offset',
        'desc' : "The vertical offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'distortion_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'bmpaperture_enable',
        'desc' : "1- enable the use of bitmap aperture; 0- disable bitmap aperture",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bmpaperture_resolution',
        'desc' : "texture sampling resolution for the importance sampling",
        'type' : 'INT',
        'default' : 512,
    },
    {
        'attr' : 'bmpaperture_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'optical_vignetting',
        'desc' : "Optical vignetting (\"Cat's Eye Bokeh\") amount",
        'type' : 'FLOAT',
        'default' : 0,
    },

    {
        'attr' : 'auto_lens_shift',
        'desc' : "Calculate lens shift automatically",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
    {
        'attr' : 'use',
        'desc' : "Use Physical Camera",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)


def GetLensShift(ob):
    shift = 0.0
    constraint = None

    if len(ob.constraints) > 0:
        for co in ob.constraints:
            if co.type in {'TRACK_TO', 'DAMPED_TRACK', 'LOCKED_TRACK'}:
                constraint = co
                break

    if constraint:
        constraint_ob = constraint.target
        if constraint_ob:
            z_shift = ob.matrix_world.to_translation()[2] - constraint_ob.matrix_world.to_translation()[2]
            l = BlenderUtils.GetDistanceObOb(ob, constraint_ob)
            shift = -1.0 * z_shift / l
    else:
        rx = ob.rotation_euler[0]
        lsx = rx - math.pi / 2
        if math.fabs(lsx) > 0.0001:
            shift = math.tan(lsx)
        if math.fabs(shift) > math.pi:
            shift = 0.0

    return shift


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    if not propGroup.use:
        return

    scene  = bus['scene']
    camera = bus['camera']

    VRayCamera = camera.data.vray

    fov, orthoWidth = BlenderUtils.GetCameraFOV(camera)

    overrideParams.update({
        'fov' : fov,

        'focus_distance' : BlenderUtils.GetCameraDofDistance(camera),
        'specify_focus'  : True,

        'lens_shift'     : GetLensShift(camera) if propGroup.auto_lens_shift else propGroup.lens_shift,

        'horizontal_offset' : -camera.data.shift_x,
        'vertical_offset'   : -camera.data.shift_y,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

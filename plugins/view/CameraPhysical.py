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

from vb30.lib import ExportUtils
from vb30.lib import LibUtils
from vb30.lib import BlenderUtils
from vb30.lib import PluginUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


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

    scene, camera = BlenderUtils.GetSceneAndCamera(bus)

    VRayScene = scene.vray

    VRayCamera = camera.data.vray
    StereoSettings = VRayScene.VRayStereoscopicSettings

    fov, orthoWidth = BlenderUtils.GetCameraFOV(scene, camera)

    focus_distance = BlenderUtils.GetCameraDofDistance(camera)
    if focus_distance < 0.001:
        focus_distance = 5.0

    horizontal_offset = -camera.data.shift_x
    vertical_offset   = -camera.data.shift_y

    imageAspect = scene.render.resolution_x / scene.render.resolution_y
    if imageAspect < 1.0:
        offset_fix = 1.0 / imageAspect
        horizontal_offset *= offset_fix
        vertical_offset   *= offset_fix

    if StereoSettings.use:
        vertical_offset /= 2.0

    overrideParams.update({
        'fov' : fov,

        'focus_distance' : focus_distance,
        'specify_focus'  : True,

        'lens_shift'     : GetLensShift(camera) if propGroup.auto_lens_shift else propGroup.lens_shift,

        'horizontal_offset' : horizontal_offset,
        'vertical_offset'   : vertical_offset,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

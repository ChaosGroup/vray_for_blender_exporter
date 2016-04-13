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

from vb30.lib import LibUtils
from vb30.lib import ExportUtils
from vb30.lib import PluginUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    o      = bus['output']
    scene  = bus['scene']
    camera = bus['camera']

    VRayCamera = camera.data.vray
    CameraStereoscopic = VRayCamera.CameraStereoscopic

    # XXX: Some code is broken in VRayStereoscopicSettings
    # Export it only if we are use CameraStereoscopic to calculate views
    #
    if not CameraStereoscopic.use:
        return

    cam = bpy.data.objects.get(CameraStereoscopic.LeftCam)
    if cam:
        overrideParams['left_camera']  = LibUtils.CleanString(cam.name)

    cam = bpy.data.objects.get(CameraStereoscopic.RightCam)
    if cam:
        overrideParams['right_camera'] = LibUtils.CleanString(cam.name)

    # NOTE: Shademap is currently broken
    overrideParams['sm_mode'] = 0
    overrideParams['shademap_file'] = None

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

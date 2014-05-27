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

import _vray_for_blender

from vb30 import debug

from . import exp_camera, exp_scene, exp_init


def GetLoopCameras(scene):
    cameras = []

    for ob in scene.objects:
        if ob.type == 'CAMERA':
            if ob.data.vray.use_camera_loop:
                cameras.append(ob)

    return cameras


def IsHideFromViewUsed(cameras):
    for camera in cameras:
        if camera.data.vray.hide_from_view:
            return True
    return False


@debug.TimeIt
def ExportCameraLoop(bus):
    scene  = bus['scene']
    engine = bus['engine']
    camera = bus['camera']
    o      = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    cameras = GetLoopCameras(scene)
    if not len(cameras):
        return 'No cameras are selected for "Camera Loop"!'

    cameras = sorted(cameras, key=lambda c: c.name)

    # We will create animated camera from 'cameras'
    o.setAnimation(True)
    o.setFrameStart(1)
    o.setFrameEnd(len(cameras))
    o.setFrameStep(1)

    if IsHideFromViewUsed(cameras):
        debug.Debug('Using "Hide From View"...')

        # Since hide from view affect object properties we have to export in
        # animation mode 
        bus['exporter'] = exp_init.InitExporter(bus, isAnimation=True)

        for i, camera in enumerate(cameras):
            # Setup camera
            bus['camera'] = camera

            # Setup fake frame
            frame = i+1
            o.setFrame(frame)
            _vray_for_blender.setFrame(frame)

            # Since we are using 'Hide From View' we have to update
            # object's visibilities.
            # Export meshes only for the first frame since
            # 'Hide From View' affects only object level.
            #
            exp_scene.ExportScene(bus, exportNodes=True, exportMeshes=(frame==1))

    else:
        bus['exporter'] = exp_init.InitExporter(bus)

        # Export objects as usual
        exp_scene.ExportScene(bus)

        # Export animated camera from 'Camera Loop' cameras
        for i, camera in enumerate(cameras):
            # Setup camera
            bus['camera'] = camera

            # Setup fake frame
            frame = i+1
            o.setFrame(frame)

            exp_camera.ExportCamera(bus)

    exp_init.ShutdownExporter(bus)

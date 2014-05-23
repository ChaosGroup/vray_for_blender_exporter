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

from . import exp_camera


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


def ExportCameraLoop(bus, scene, engine):
    Debug("ExportCameraLoop()")

    o = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    cameras = GetLoopCameras(scene)

    if IsHideFromViewUsed(cameras):
        bus['exporter'] = _vray_for_blender.init(
            scene   = scene.as_pointer(),
            engine  = engine.as_pointer(),
            context = bpy.context.as_pointer(),

            useNodes = True,

            objectFile   = o.fileManager.getFileByPluginType('OBJECT'),
            geometryFile = o.fileManager.getFileByPluginType('GEOMETRY'),
            lightsFile   = o.fileManager.getFileByPluginType('LIGHT'),
            materialFile = o.fileManager.getFileByPluginType('MATERIAL'),
            textureFile  = o.fileManager.getFileByPluginType('TEXTURE'),

            isAnimation = False,
        )

        # Export objects as usual
        #
        ExportFrame(bus)

        # Export animated camera from 'Camera Loop' cameras
        #
        o.setAnimation(True)
        for i, camera in enumerate(cameras):
            # Setup camera
            bus['camera'] = camera

            # Setup fake frame
            frame = i+1
            o.setFrame(frame)

            exp_camera.ExportCamera(bus)

    else:
        bus['exporter'] = _vray_for_blender.init(
            scene   = scene.as_pointer(),
            engine  = engine.as_pointer(),
            context = bpy.context.as_pointer(),

            useNodes = True,

            objectFile   = o.fileManager.getFileByPluginType('OBJECT'),
            geometryFile = o.fileManager.getFileByPluginType('GEOMETRY'),
            lightsFile   = o.fileManager.getFileByPluginType('LIGHT'),
            materialFile = o.fileManager.getFileByPluginType('MATERIAL'),
            textureFile  = o.fileManager.getFileByPluginType('TEXTURE'),

            isAnimation = True,
            frameStart  = 1,
            frameStep   = 1,
        )

        for i, camera in enumerate(cameras):
            # Setup camera
            bus['camera'] = camera

            # Setup fake frame
            frame = i+1
            o.setFrame(frame)
            _vray_for_blender.setFrame(frame)

            # Export meshes only for the first frame since
            # 'Hide From View' affects only object level
            #
            exportMeshes = frame == 1

            # Since we are using 'Hide From View' we have to update
            # object's visibilities
            #
            ExportFrame(bus, exportNodes=True, exportMeshes=exportMeshes)

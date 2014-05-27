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

from . import exp_init
from . import exp_scene
from . import exp_camera


def ExportCameraOnly(bus):
    scene = bus['scene']
    o     = bus['output']

    # Init exporter
    bus['exporter'] = exp_init.InitExporter(bus, isAnimation=True)

    # Store current frame
    selected_frame = scene.frame_current

    # Set frame
    f = o.frameStart

    scene.frame_set(f)
    o.setFrame(f)
    _vray_for_blender.setFrame(f)

    # 1. Export full first frame
    err = exp_scene.ExportScene(bus)
    if err is not None:
        return err

    # 2. Export camera motion for the rest frames
    f += o.frameStep
    while(f <= o.frameEnd):
        scene.frame_set(f)
        o.setFrame(f)
        _vray_for_blender.setFrame(f)

        err = exp_camera.ExportCamera(bus)
        if err is not None:
            break

        f += o.frameStep

    exp_init.ShutdownExporter(bus)

    # Restore selected frame
    scene.frame_set(selected_frame)

    return None


def ExportFullNotMeshes(bus):
    scene = bus['scene']
    o     = bus['output']

    # Init exporter
    bus['exporter'] = exp_init.InitExporter(bus, isAnimation=True)

    # Store current frame
    selected_frame = scene.frame_current

    # Set frame
    f = o.frameStart

    scene.frame_set(f)
    o.setFrame(f)
    _vray_for_blender.setFrame(f)

    # 1. Export full first frame
    err = exp_scene.ExportScene(bus)
    if err is not None:
        return err

    # 2. Export nodes for rest frames
    f += o.frameStep
    while(f <= o.frameEnd):
        scene.frame_set(f)
        o.setFrame(f)
        _vray_for_blender.setFrame(f)

        err = exp_scene.ExportScene(bus, exportMeshes=False)
        if err is not None:
            break

        f += o.frameStep

    exp_init.ShutdownExporter(bus)

    # Restore selected frame
    scene.frame_set(selected_frame)

    return None


def ExportFullRange(bus):
    scene = bus['scene']
    o     = bus['output']

    err = None

    # Init exporter
    bus['exporter'] = exp_init.InitExporter(bus, isAnimation=True)

    # Store current frame
    selected_frame = scene.frame_current

    f = o.frameStart
    while(f <= o.frameEnd):
        scene.frame_set(f)

        o.setFrame(f)
        _vray_for_blender.setFrame(f)

        err = exp_scene.ExportScene(bus)
        if err is not None:
            break

        f += o.frameStep

    # Restore selected frame
    scene.frame_set(selected_frame)

    exp_init.ShutdownExporter(bus)

    return err


@debug.TimeIt
def ExportAnimation(bus, frameStart, frameEnd, frameStep):
    err = None

    scene = bus['scene']
    o     = bus['output']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    o.setAnimation(True)
    o.setFrameStart(frameStart)
    o.setFrameEnd(frameEnd)
    o.setFrameStep(frameStep)

    if VRayExporter.animation_type == 'NOTMESHES':
        err = ExportFullNotMeshes(bus)
    elif VRayExporter.animation_type == 'CAMERA':
        err = ExportCameraOnly(bus)
    else:
        err = ExportFullRange(bus, frameStart, frameEnd, frameStep)

    return err

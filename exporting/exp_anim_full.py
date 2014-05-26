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


@debug.TimeIt
def ExportAnimation(bus, frameStart, frameEnd, frameStep):
    debug.Debug("ExportAnimation()")

    err = None

    scene = bus['scene']
    o     = bus['output']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    o.setAnimation(True)

    o.setFrameStart(frameStart)
    o.setFrameEnd(frameEnd)

    # Set frame step; used to detect if we need
    # to export a keyframe in interpolate()
    o.setFrameStep(frameStep)

    # Store current frame
    selected_frame = scene.frame_current

    # Init exporter
    bus['exporter'] = exp_init.InitExporter(bus, isAnimation=True)

    f = frameStart
    while(f <= frameEnd):
        scene.frame_set(f)

        o.setFrame(f)
        _vray_for_blender.setFrame(f)

        err = exp_scene.ExportScene(bus)
        if err is not None:
            break

        f += frameStep

    # Restore selected frame
    scene.frame_set(selected_frame)

    exp_init.ShutdownExporter(bus)

    return err

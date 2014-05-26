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

from vb30.lib.VRayProcess import VRayProcess
from vb30.lib import SysUtils

from vb30 import debug

from . import exp_load


def Run(bus):
    debug.Debug("Run()")

    scene  = bus['scene']
    engine = bus['engine']
    o      = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    p = VRayProcess()
    p.setVRayStandalone(SysUtils.GetVRayStandalonePath())
    p.setSceneFile(o.fileManager.getOutputFilepath())
    p.setAutorun(VRayExporter.autorun)
    p.setVerboseLevel(VRayExporter.verboseLevel)
    p.setShowProgress(VRayExporter.showProgress)
    p.setDisplaySRGB(VRayExporter.display_srgb)

    # TODO: Rewrite into 'SettingsOutput'
    #
    # if scene.render.use_border:
    #     resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    #     resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)
    #
    #     x0 = resolution_x *        scene.render.border_min_x
    #     y0 = resolution_y * (1.0 - scene.render.border_max_y)
    #     x1 = resolution_x *        scene.render.border_max_x
    #     y1 = resolution_y * (1.0 - scene.render.border_min_y)
    #
    #     p.setRegion(x0, y0, x1, y1, useCrop=scene.render.use_crop_to_border)

    if engine.is_preview:
        p.setShowProgress(0)
        p.setVerboseLevel(0)
        p.setAutoclose(True)
        p.setDisplayVFB(False)

    if VRayExporter.animation and VRayExporter.animation_type == 'FRAMEBYFRAME':
        p.setWaitExit(True)
        p.setAutoclose(True)
        p.setFrames(scene.frame_current)
    elif VRayExporter.frames_to_export > 1:
        p.setFrames(scene.frame_current)
    elif o.isAnimation:
        p.setFrames(o.frameStart, o.frameEnd, o.frameStep)

    if not scene.render.threads_mode == 'AUTO':
        p.setThreads(scene.render.threads)

    if bpy.app.background or VRayExporter.wait:
        p.setWaitExit(True)
        if bpy.app.background:
            p.setDisplayVFB(False) # Disable VFB
            p.setAutoclose(True)   # Exit on render end

    p.run()

    if engine.is_preview:
        exp_load.LoadImage(scene, engine, o, p)


def RunEx(bus):
    debug.Debug("RunEx()")

    try:
        Run(bus)
    except Exception as e:
        debug.ExceptionInfo(e)
        return "Run error! Check system console!"

    return None

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

from vb30.exporting.cloud_job import VCloudJob

from vb30.lib.VRayProcess import VRayProcess
from vb30.lib import SysUtils

from vb30 import debug

from . import exp_load

import webbrowser


def Run(bus):
    debug.Debug("Run()")

    scene  = bus['scene']
    engine = bus['engine']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter
    VRayDR       = VRayScene.VRayDR

    vrayCmd = SysUtils.GetVRayStandalonePath()
    if not vrayCmd:
        raise Exception("V-Ray not found!")

    imageToBlender = VRayExporter.animation_mode == 'NONE' and not scene.render.use_border and VRayExporter.auto_save_render and VRayExporter.image_to_blender

    p = VRayProcess()
    p.setVRayStandalone(vrayCmd)
    p.setSceneFile(bus['outputFilePath'])
    p.setAutorun(VRayExporter.autorun)
    p.setVerboseLevel(VRayExporter.verboseLevel)
    p.setShowProgress(VRayExporter.showProgress)
    p.setDisplaySRGB(scene.display_settings.display_device == 'sRGB')
    p.setDisplayVFB(VRayExporter.display)
    p.setAutoclose(VRayExporter.autoclose)

    if SysUtils.IsGPUEngine(bus):
        p.setRtEngine(VRayExporter.device_gpu_type, VRayScene.SettingsRTEngine)

    # TODO: Rewrite into 'SettingsOutput'
    if scene.render.use_border:
        resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
        resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

        x0 = resolution_x *        scene.render.border_min_x
        y0 = resolution_y * (1.0 - scene.render.border_max_y)
        x1 = resolution_x *        scene.render.border_max_x
        y1 = resolution_y * (1.0 - scene.render.border_min_y)

        p.setRegion(x0, y0, x1, y1, useCrop=scene.render.use_crop_to_border)

    if imageToBlender:
        p.setWaitExit(True)
        p.setAutoclose(True)

    if engine.is_preview:
        p.setPreview(True)
        p.setShowProgress(0)
        p.setVerboseLevel(0)
        p.setAutoclose(True)
        p.setDisplayVFB(False)

    if VRayDR.on:
        if len(VRayDR.nodes):
            transferAssets = VRayDR.assetSharing == 'TRANSFER'
            if transferAssets:
                if VRayDR.checkAssets:
                    transferAssets = 2

            p.setDistributed(2 if VRayDR.renderOnlyOnNodes else 1)

            hosts = []
            for n in VRayDR.nodes:
                if n.use:
                    hosts.append("%s:%s" % (n.address,n.port) if n.port_override else n.address)

            p.setRenderhosts(hosts)
            p.setPortNumber(VRayDR.port)
            p.setTransferAssets(transferAssets)
            p.setLimitHosts(VRayDR.limitHosts)

    if VRayExporter.animation_mode == 'NONE':
        p.setFrames(scene.frame_current)

    elif VRayExporter.animation_mode == 'FRAMEBYFRAME':
        p.setWaitExit(True)
        p.setAutoclose(True)
        p.setFrames(scene.frame_current)

    else:
        p.setFrames(bus['frameStart'], bus['frameEnd'], bus['frameStep'])

    if not scene.render.threads_mode == 'AUTO':
        p.setThreads(scene.render.threads)

    if bpy.app.background or VRayExporter.wait:
        p.setWaitExit(True)
        if bpy.app.background:
            if not VRayExporter.display_vfb_in_batch:
                p.setDisplayVFB(False) # Disable VFB
            p.setAutoclose(True)   # Exit on render end

    if VRayExporter.gen_run_file:
        p.setGenRunFile(True)

    if VRayExporter.submit_to_vray_cloud:
        p.setAutorun(False)

    exportExitStatus = p.run()

    if exportExitStatus == 0 and VRayExporter.submit_to_vray_cloud:
        job = VCloudJob(bus)
        cloudExitStatus = job.submitToCloud()
        if cloudExitStatus == -404:
            print("V-Ray Cloud binary is not detected on your system!")
            webbrowser.open("https://www.chaosgroup.com/cloud")

    if imageToBlender or engine.is_preview:
        exp_load.LoadImage(scene, engine, bus['renderedImagePath'], p)


def RunEx(bus):
    debug.Debug("RunEx()")

    try:
        Run(bus)
    except Exception as e:
        debug.ExceptionInfo(e)
        return "Run error: %s" % e

    return None

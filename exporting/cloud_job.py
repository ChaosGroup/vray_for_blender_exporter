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
from vb30.exporting import exp_anim_camera_loop

import subprocess

def getFrameRange(scene):
    VRayExporter = scene.vray.Exporter
    
    if VRayExporter.animation_mode == 'NONE':
        return ''

    frame_range = '{}-{}'
    if not VRayExporter.animation_mode == 'CAMERA_LOOP':
        frame_range =  frame_range.format(scene.frame_start, scene.frame_end)
    else: # if camera loop is enabled
        loop_cameras = exp_anim_camera_loop.GetLoopCameras(scene)
        frame_range = frame_range.format(1, len(loop_cameras))

    return frame_range


class VCloudJob:
    def __init__(self, bus):
        scene  = bus['scene']
        output = bus['output']

        VRayScene = scene.vray
        VRayExporter = VRayScene.Exporter
        VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

        self.project = VRayExporter.vray_cloud_project_name
        self.name = VRayExporter.vray_cloud_job_name
        self.sceneFile = output.fileManager.getOutputFilepath()
        
        if VRayScene.SettingsImageSampler.type == '3':
            self.renderMode = "progressive"
        else:
            self.renderMode = "bucket"

        self.width = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
        self.height = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

        self.animation = not VRayExporter.animation_mode == 'NONE'
        if self.animation:
            self.frameRange = getFrameRange(scene)
            self.frameStep = scene.frame_step

        self.ignoreWarnings = True


    def submitCmd(self):
        VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

        cmd = [VRayPreferences.vray_cloud_binary, "job", "submit"]

        cmd.append("--project")
        cmd.append(self.project)

        cmd.append("--name")
        cmd.append(LibUtils.FormatName(self.name))

        cmd.append("--sceneFile")
        cmd.append(self.sceneFile)

        cmd.append("--renderMode")
        cmd.append(self.renderMode)

        cmd.append("--width")
        cmd.append(str(self.width))

        cmd.append("--height")
        cmd.append(str(self.height))

        if self.animation:
            cmd.append("--animation")

            cmd.append("--frameRange")
            cmd.append(self.frameRange)

            cmd.append("--frameStep")
            cmd.append(str(self.frameStep))

        if self.ignoreWarnings:
            cmd.append("--ignoreWarnings")

        return cmd

            
    def createProjectCmd(self):
        VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

        return [VRayPreferences.vray_cloud_binary, "project", "create", "--name", self.project]

    
    def submitToCloud(self):
        """
        Submits this job to Chaos Cloud. Tries to create a project before submitting.
        Exit code:
            -404: Chaos Cloud binary is not detected on the system, done nothing
            -2:   created project, failed to submit job
            -1:   failed to create project, failed to submit job
            0 :   job submitted successfully 
        """
        VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

        exitCode = 0
        if VRayPreferences.detect_vray_cloud:
            createProjectResult = subprocess.call(self.createProjectCmd())
            submitJobResult     = subprocess.call(self.submitCmd())
            
            if submitJobResult != 0:
                if createProjectResult != 0:
                    exitCode = -1
                else:
                    exitCode = -2
        else:
            exitCode = -404;

        return exitCode
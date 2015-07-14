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

import os
import re
import struct
import subprocess
import signal
import sys
import shutil
import tempfile

from vb30 import debug

from . import PathUtils
from . import BlenderUtils


class VRayProcess:
    def __init__(self):
        self.filepath = ""
        self.waitExit = False
        self.autorun  = True

        # Process
        self.process  = None

        # Performance
        self.numThreads = 0

        # Input data
        self.sceneFile = ""
        self.include = ""

        # Animation
        self.frames = ""

        # Distributed Rendering
        self.distributed = 0
        self.renderhost = ""
        self.portNumber = 20207
        self.limitHosts = 0

        self.transferAssets = 0
        self.cachedAssetsLimitType = 0
        self.cachedAssetsLimitValue = 0.0
        self.overwriteLocalCacheSettings = 0

        # VFB Display Options
        self.useRegion = False
        self.useCrop   = False

        self.autoClose = 0
        self.setfocus = 1
        self.display = 1
        self.displayAspect = 0
        self.displayLUT = 0
        self.displaySRGB = 2
        self.region = ""

        # Output file
        self.imgFile = ""
        self.noFrameNumbers = 0

        # Realtime engine
        self.rtEngine = None
        self.rtNoise = 0.001
        self.rtSampleLevel = 0
        self.rtTimeOut = 0.0

        # Progress output
        self.verboseLevel = '3'
        self.showProgress = '1'
        self.progressIncrement = 10
        self.progressUpdateFreq = 200
        self.progressUseColor = 1
        self.progressUseCR = 1

        # Unused params
        #
        # self.interactive = 0

        # These params will be setup via 'SettingsOutput'
        #
        # imgHeight
        # imgWidth
        # region
        # crop
        self.isPreview = False

        self.gen_run_file = False

    def setVRayStandalone(self, filepath):
        self.filepath = filepath

    def setAutorun(self, autorun):
        self.autorun = autorun

    def setSceneFile(self, sceneFile):
        self.sceneFile = sceneFile

    def setWaitExit(self, waitExit):
        self.waitExit = waitExit

    def setDisplaySRGB(self, useSRBG):
        self.displaySRGB = 1 if useSRBG else 2

    def setDisplayVFB(self, displayVFB):
        self.display = displayVFB

    def setAutoclose(self, autoclose):
        self.autoClose = autoclose

    def setOutputFile(self, imgFile):
        self.imgFile = imgFile

    def setVerboseLevel(self, verboseLevel):
        self.verboseLevel = verboseLevel

    def setShowProgress(self, progress):
        self.showProgress = progress

    def setThreads(self, threads):
        self.numThreads = threads

    def setRegion(self, x0, y0, x1, y1, useCrop=False):
        self.useRegion = True
        self.useCrop   = useCrop
        self.region = "%i;%i;%i;%i" % (x0, y0, x1, y1)

    def setFrames(self, frameStart=None, frameEnd=None, frameStep=None):
        if frameStart is not None:
            self.frames  = "%d" % frameStart
        if frameEnd is not None:
            self.frames += "-%d" % frameEnd
        if frameStep is not None:
            self.frames += ",%d" % frameStep

    def setDistributed(self, d):
        self.distributed = d

    def setRenderhosts(self, hosts):
        self.renderhost = ";".join(hosts)

    def setPortNumber(self, n):
        self.portNumber = n

    def setLimitHosts(self, n):
        self.limitHosts = n

    def setTransferAssets(self, v):
        self.transferAssets = v

    def setPreview(self, v):
        self.isPreview = v

    def setGenRunFile(self, v):
        self.gen_run_file = v

    def setRtEngine(self, RTEngine, SettingsRTEngine):
        DEVICE = {
            '0' : 1,
            '4' : 5,
        }

        self.rtEngine = DEVICE[RTEngine.use_opencl]
        self.rtNoise       = SettingsRTEngine.noise_threshold
        self.rtSampleLevel = SettingsRTEngine.max_sample_level
        self.rtTimeOut     = SettingsRTEngine.max_render_time

    def getCommandLine(self):
        cmd = [self.filepath]
        cmd.append('-verboseLevel=%s' % self.verboseLevel)
        cmd.append('-showProgress=%s' % self.showProgress)
        cmd.append('-display=%i' % self.display)
        cmd.append('-displaySRGB=%i' % self.displaySRGB)
        cmd.append('-autoClose=%i' % self.autoClose)

        if self.distributed:
            cmd.append('-distributed=%i' % self.distributed)
            cmd.append('-portNumber=%i' % self.portNumber)
            cmd.append('-renderhost=%s' % self.renderhost)
            cmd.append('-transferAssets=%i' % self.transferAssets)
            cmd.append('-limitHosts=%i' % self.limitHosts)

        if self.numThreads:
            cmd.append('-numThreads=%s' % self.numThreads)

        if self.useRegion:
            regionType = "crop" if self.useCrop else "region"
            cmd.append('-%s=%s' % (regionType, self.region))

        if self.imgFile:
            cmd.append('-imgFile=%s' % PathUtils.Quotes(self.imgFile))

        if self.frames:
            cmd.append('-frames=%s' % self.frames)

        if self.rtEngine is not None:
            cmd.append('-rtEngine=%i'      % self.rtEngine)
            cmd.append('-rtTimeOut=%.3f'   % self.rtTimeOut)
            cmd.append('-rtNoise=%.3f'     % self.rtNoise)
            cmd.append('-rtSampleLevel=%i' % self.rtSampleLevel)

        cmd.append('-sceneFile=%s' % PathUtils.Quotes(self.sceneFile))

        return cmd


    def run(self):
        cmd     = self.getCommandLine()
        errCode = 0

        if not self.isPreview:
            commandLine = " ".join(cmd)

            debug.PrintInfo("Command Line: %s" % commandLine)

            if self.gen_run_file:
                baseFile = self.sceneFile
                if bpy.data.filepath:
                    baseFile = bpy.data.filepath

                sceneFileName = bpy.path.display_name_from_filepath(baseFile)
                runExt        = "bat" if sys.platform == 'win32' else "sh"
                cmdSep        = "^" if sys.platform == 'win32' else "\\"
                allTheRest    = "%%*" if sys.platform == 'win32' else "$*"

                runFilename = "render_%s.%s" % (sceneFileName, runExt)
                runFilepath = os.path.join(os.path.dirname(baseFile), runFilename)

                debug.PrintInfo("Generating %s..." % runFilename)

                cmdJoin = " %s\n" % cmdSep

                fileCmdLine  = "%s %s\n" % (PathUtils.Quotes(cmd[0], force=True), cmdSep)
                fileCmdLine += cmdJoin.join(cmd[1:])

                with open(runFilepath, 'w') as f:
                    f.write(fileCmdLine)
                    f.write(" %s\n%s" % (cmdSep, allTheRest))
                    f.write("\n")

                if sys.platform not in {'win32'}:
                    os.chmod(runFilepath, 0o744)

        VRayExporter = bpy.context.scene.vray.Exporter

        if not VRayExporter.vfb_global_preset_file_use:
            vray_vfb_global_preset_vars = {'VRAY_VFB_GLOBAL_PRESET_FILE_USE', 'VRAY_VFB_GLOBAL_PRESET_FILE'}
            for var in vray_vfb_global_preset_vars:
                if var in os.environ:
                    del os.environ[var]
        else:
            os.environ['VRAY_VFB_GLOBAL_PRESET_FILE_USE'] = "%i" % VRayExporter.vfb_global_preset_file_use
            os.environ['VRAY_VFB_GLOBAL_PRESET_FILE'] = BlenderUtils.GetFullFilepath(VRayExporter.vfb_global_preset_file)

        if self.autorun:
            self.process = subprocess.Popen(cmd)
            if self.waitExit:
                errCode = self.process.wait()

        return errCode


    def kill(self):
        if self.is_running():
            self.process.terminate()
        self.process = None


    def is_running(self):
        if self.process is None:
            return False
        if self.process.poll() is None:
            return True
        return False

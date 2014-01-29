#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

import os
import re
import struct
import subprocess
import signal
import sys
import tempfile

from vb25.debug import Debug


if sys.platform not in {'win32'}:
    import fcntl


class VRayProcess():
    # Process management
    vrayExe = None
    process = None
    procExitReady = None

    # Command line arguments
    # Render Input
    sceneFile = None
    include = None

    # Render Output
    imgFile = None
    noFrameNumbers = None

    # VFB Display Options
    display = None
    autoclose = None
    setfocus = None
    displaySRGB = None
    displayLUT = None
    displayAspect = None

    # Console Output
    showProgress  = None
    progressUseCR = None
    verboseLevel  = None

    # Working mode: 'NORMAL', 'CMD', 'SPAWN'
    mode = None

    # Distributed Rendering
    transferAssets = None

    def __init__(self):
        self.vrayExe = "vray"
        self.verboseLevel = 1
        self.showProgress = 1
        self.cmdMode = 1
        self.display = 1

    # def __del__(self):
    #     self.kill()

    def init(self, vrayExe):
        self.vrayExe = vrayExe

    def setSceneFile(self, sceneFile):
        if self.sceneFile is not None:
            if self.sceneFile != sceneFile:
                self.sceneFile = sceneFile
                self.restart()
        self.sceneFile = sceneFile

    def setMode(self, mode):
        Debug("VRayProcess::setMode(%s)" % mode)

        needRestart = False
        if self.mode is not None:
            if self.mode != mode:
                needRestart = True

        self.mode = mode
        
        if self.mode == 'NORMAL':
            self.cmdMode = 0
        else:
            self.cmdMode = 1
        
        if needRestart:
            self.restart()

    def getCommandLine(self):
        procArgs = [self.vrayExe]
        procArgs.append('-verboseLevel=%i' % self.verboseLevel)
        procArgs.append('-showProgress=%i' % self.showProgress)
        procArgs.append('-display=%i' % self.display)
        procArgs.append('-sceneFile=%s' % self.sceneFile)
        if self.cmdMode:
            procArgs.append('-cmdMode=%s' % self.cmdMode)
        procArgs.append('-displaySRGB=%i' % (1 if self.displaySRGB else 2))

        return procArgs

    def run(self):
        Debug("VRayProcess::run")

        if self.is_running():
            return

        procArgs = self.getCommandLine()

        if self.mode in {'SPAWN'}:
            self.process = subprocess.Popen(procArgs, bufsize=256, stdout=subprocess.PIPE)

            if sys.platform not in {'win32'}:
                fd = self.process.stdout.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        else:
            self.process = subprocess.Popen(procArgs)

    def restart(self):
        Debug("VRayProcess::restart")

        self.kill()
        self.run()

    def kill(self):
        Debug("VRayProcess::kill")

        if self.is_running():
            self.process.terminate()

        self.process = None

    def is_running(self):
        if self.mode in {'CMD', 'SPAWN'}:
            if self.process is None:
                return False
            if self.process.poll() is None:
                return True
        return False

    def get_progress(self):
        msg  = None
        prog = None

        if self.mode not in {'SPAWN'}:
            return {None, None}

        if not self.is_running():
            return {None, None}

        stdout_lines = None
        try:
            self.process.stdout.flush()
            stdout_lines = self.process.stdout.readlines(256)
        except:
            pass

        if stdout_lines:
            for stdout_line in stdout_lines:
                line = stdout_line.decode('ascii').strip()

                if self.debug:
                    print(line)

                if line.find("Building light cache") != -1:
                    msg = "Light cache"
                elif line.find("Prepass") != -1:
                    prepass_num = line[line.find("Prepass")+7:line.find("of")].strip()
                    msg = "Irradiance map (prepass %s)" % (prepass_num)
                elif line.find("Rendering image") != -1:
                    msg = "Rendering"
                elif line.find("Building caustics") != -1:
                    msg = "Caustics"
                elif line.find("Frame took") != -1:
                    self.procRenderFinished = True

                if msg is None:
                    continue

                p_start = line.find("...: ") + 5
                p_end   = line.find("%")

                if p_start != -1 and p_end != -1 and p_end > p_start:
                    p_str = line[p_start:p_end].strip()
                    if len(p_str):
                        prog = float(p_str) / 100.0
                        break
        return msg, prog

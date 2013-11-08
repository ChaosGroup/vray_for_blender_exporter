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
import socket
import subprocess
import signal
import sys
import tempfile
import time

import vb25

from .VRaySocket import VRaySocket

if sys.platform not in {'win32'}:
    import fcntl


class MyProcess():
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

    # Woring mode: 'NORMAL', 'CMD', 'SPAWN'
    mode = None

    # Distributed Rendering
    transferAssets = None

    # Command socket
    socket = None

    # Misc
    debug = None

    def __init__(self):
        self.debug = True
        self.socket = VRaySocket

        self.vrayExe = "vray"
        self.verboseLevel = 1
        self.showProgress = 1
        self.cmdMode = 1
        self.display = 1

    def __del__(self):
        self.kill()

    def init(self, vrayExe):
        self.vrayExe = vrayExe

    def setSceneFile(self, sceneFile):
        self.sceneFile = sceneFile

    def setMode(self, mode):
        if self.mode:
            if self.mode != mode:
                self.mode = mode
                self.restart()
        self.mode = mode

    def getCommandLine(self):
        procArgs = [self.vrayExe]
        procArgs.append('-verboseLevel=%i' % self.verboseLevel)
        procArgs.append('-showProgress=%i' % self.showProgress)
        procArgs.append('-display=%i' % self.display)

        if self.mode in {'CMD', 'SPAWN'}:
            procArgs.append('-cmdMode=1')
        else:
            procArgs.append('-sceneFile=%s' % self.sceneFile)
        
        print("Command line: %s" % " ".join(procArgs))

        return procArgs

    def run(self):
        print("VRayProcess::run")

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

        time.sleep(1.0)

        self.socket.connect()


    def restart(self):
        print("VRayProcess::restart")

        self.kill()
        self.run()


    def kill(self):
        print("VRayProcess::kill")

        self.quit()

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


    def load_scene(self):
        if not self.sceneFile:
            vb25.utils.vb25.utils.debug(None, "Scene file is not set", error=True)
            return

        if self.mode not in {'CMD', 'SPAWN'}:
            return

        self.socket.send("stop")
        self.socket.send("unload")
        self.socket.send("load %s" % self.sceneFile)


    def unload_scene(self):
        print("VRayProcess::unload_scene")
        self.socket.send("unload")


    def append_scene(self, filepath=None):
        print("VRayProcess::append_scene")

        scenePath = filepath
        if scenePath is None:
            scenePath = self.sceneFile
        if not scenePath:
            return

        self.socket.send("append %s" % scenePath)


    def reload_scene(self):
        """
        Reload scene
        """
        print("VRayProcess::reload_scene")

        self.unload_scene()
        self.load_scene()


    def render(self):
        """
        Start rendering
        """
        print("VRayProcess::render")

        if self.mode in {'CMD', 'SPAWN'}:
            self.socket.send("render", result=False)


    def quit(self):
        """
        Close V-Ray
        """
        print("VRayProcess::quit")

        if self.mode in {'CMD', 'SPAWN'}:
            self.socket.send("stop")
            self.socket.send("quit")
            self.socket.disconnect()

    def recieve_raw_image(self, bufSize):
        self.socket.send("getRawImage", result=False)
        
        pixels = None

        try:
            pixels = self.socket.recv(bufSize)
            print("Get %i bytes stream" % len(pixels))
        except:
            pass

        return pixels


    def recieve_image(self, progressFile):
        jpeg_image = None
        jpeg_size  = 0
        buff  = []

        if not self.is_running():
            self.procRenderFinished = True
            return 'V-Ray is not running'

        # Request image
        self.socket.send("getImage 90 1", result=False)

        # Read image stream size
        jpeg_size_bytes = self.socket.recv(4)

        # Check if 'fail' recieved
        if jpeg_size_bytes == b'fail':
            self.socket.recv(3) # Read 'e', 'd', '\0'
            self.procRenderFinished = True
            return 'getImage failed'

        try:
            # Get stream size in bytes
            jpeg_size = struct.unpack("<L", jpeg_size_bytes)[0]

            # print("JPEG stream size =%i"%(jpeg_size))

            # Read JPEG stream
            jpeg_image = self.socket.recv(jpeg_size)

            # Write stream to file
            open(progressFile, 'wb').write(jpeg_image)
        except:
            return 'JPEG stream recieve fail'

        return None


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


VRayProcess = MyProcess()

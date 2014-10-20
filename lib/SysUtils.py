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

import getpass
import os
import socket
import sys
import shutil
import platform

import bpy

from vb30 import debug


def GetUsername():
    if sys.platform == 'win32':
        return "standalone"
    else:
        return getpass.getuser()


def GetHostname():
    return socket.gethostname()


def GetArch():
    bitness = platform.architecture()[0]
    if bitness == '32':
        return 'x86'
    return 'x86_64'


def GetVRayStandalones():
    VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

    vrayExe   = "vray.exe" if sys.platform == 'win32' else "vray"
    splitChar = ';'        if sys.platform == 'win32' else ':'

    vrayPaths = {}

    def getPaths(pathStr):
        if pathStr:
            return pathStr.strip().replace('\"','').split(splitChar)
        return []

    for var in reversed(sorted(os.environ.keys())):
        envVar = os.getenv(var)
        if not envVar:
            continue

        if var.startswith('VRAY_PATH') or var == 'PATH':
            for path in getPaths(envVar):
                vrayExePath = os.path.join(path, vrayExe)
                if os.path.exists(vrayExePath):
                    vrayPaths[var] = vrayExePath

        elif '_MAIN_' in var:
            if var.startswith('VRAY_FOR_MAYA'):
                for path in getPaths(envVar):
                    vrayExePath = os.path.join(path, "bin", vrayExe)
                    if os.path.exists(vrayExePath):
                        vrayPaths[var] = vrayExePath

            elif var.startswith('VRAY30_RT_FOR_3DSMAX'):
                for path in getPaths(envVar):
                    vrayExePath = os.path.join(path, vrayExe)
                    if os.path.exists(vrayExePath):
                        vrayPaths[var] = vrayExePath

    if sys.platform in {'darwin'}:
        import glob

        instLogFilepath = "/var/log/chaos_installs"
        if os.path.exists(instLogFilepath):
            instLog = open(instLogFilepath, 'r').readlines()
            for l in instLog:
                if 'V-Ray Standalone' in l and '[UN]' not in l:
                    installName, path = l.strip().split('=')

                    path = os.path.normpath(os.path.join(path.strip(), '..', '..', '..', "bin"))

                    possiblePaths = glob.glob('%s/*/*/vray' % path)
                    if len(possiblePaths):
                        vrayPaths[installName] = possiblePaths[0]

    return vrayPaths


def GetVRayStandalonePath():
    VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

    vray_bin = "vray"
    if sys.platform == 'win32':
        vray_bin += ".exe"

    def get_env_paths(var):
        split_char= ';' if sys.platform == 'win32' else ":"
        env_var= os.getenv(var)
        if env_var:
            return env_var.replace('\"','').split(split_char)
        return []

    def find_vray_std_osx_official():
        vrayPath = "/Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/bin/snow_leopard_x86/gcc-4.2/vray"
        if os.path.exists(vrayPath):
            return vrayPath
        return None

    def find_vray_std_osx():
        import glob
        instLogFilepath = "/var/log/chaos_installs"
        if not os.path.exists(instLogFilepath):
            return None
        instLog = open(instLogFilepath, 'r').readlines()
        for l in instLog:
            # Example path:
            #  /Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/uninstall/linuxinstaller.app/Contents
            #
            if 'V-Ray Standalone' in l and '[UN]' not in l:
                _tmp_, path = l.strip().split('=')

                # Going up to /Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/bin
                path = os.path.normpath(os.path.join(path.strip(), '..', '..', '..', "bin"))

                possiblePaths = glob.glob('%s/*/*/vray' % path)
                if len(possiblePaths):
                    return possiblePaths[0]
                return None
        return None

    def find_vray_binary(paths):
        if paths:
            for p in paths:
                if p:
                    vray_path= os.path.join(p,vray_bin)
                    if os.path.exists(vray_path):
                        return vray_path
        return None

    if not VRayPreferences.detect_vray and VRayPreferences.vray_binary:
        manualVRayPath = bpy.path.abspath(VRayPreferences.vray_binary)
        if os.path.exists(manualVRayPath):
            return manualVRayPath

    # Check 'VRAY_PATH' environment variable
    #
    vray_standalone_paths= get_env_paths('VRAY_PATH')
    if vray_standalone_paths:
        vray_standalone= find_vray_binary(vray_standalone_paths)
        if vray_standalone:
            return vray_standalone

    # On OS X check default path and install log
    #
    if sys.platform in {'darwin'}:
        path = find_vray_std_osx_official()
        if path is not None:
            return path
        path = find_vray_std_osx()
        if path is not None:
            return path

    # Try to find Standalone in V-Ray For Maya
    #
    for var in reversed(sorted(os.environ.keys())):
        if var.startswith('VRAY_FOR_MAYA'):
            if var.find('MAIN') != -1:
                debug.PrintInfo("Searching in: %s" % var)
                vray_maya = find_vray_binary([os.path.join(path, 'bin') for path in get_env_paths(var)])
                if vray_maya:
                    debug.PrintInfo("V-Ray found in: %s" % vray_maya)
                    return vray_maya

    # Try to find vray binary in %PATH%
    debug.PrintError("V-Ray not found! Trying to start \"%s\" command from $PATH..." % vray_bin)

    return shutil.which(vray_bin)


def GetExporterPath():
    for path in bpy.utils.script_paths(os.path.join('addons','vb30')):
        if path:
            return path
    return None


def GetUserConfigDir():
    userConfigDirpath = os.path.join(bpy.utils.user_resource('CONFIG'), "vrayblender")
    if not os.path.exists(userConfigDirpath):
        os.makedirs(userConfigDirpath)
    return userConfigDirpath


def GetVRsceneTemplate(filename):
    templatesDir = os.path.join(GetExporterPath(), "templates")
    templateFilepath = os.path.join(templatesDir, filename)

    templateFilepathUser = os.path.join(GetUserConfigDir(), "templates", "%s.user" % filename)

    if os.path.exists(templateFilepathUser):
        templateFilepath = templateFilepathUser

    if not os.path.exists(templateFilepath):
        return ""

    return open(templateFilepath, 'r').read()


def GetPreviewBlend():
    userPreview = os.path.join(GetUserConfigDir(), "preview.blend")
    if os.path.exists(userPreview):
        return userPreview
    return os.path.join(GetExporterPath(), "preview", "preview.blend")


def IsRTEngine(bus):
    if bus["engine"].bl_idname == 'VRAY_RENDER_RT':
        return True
    if bus["scene"].vray.RTEngine.enabled:
        return True
    return False

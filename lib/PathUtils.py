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

import os
import sys
import tempfile
import pathlib
import filecmp
import shutil

import bpy

from vb30 import debug

from . import SysUtils


def GetFilename(filepath, ext=True):
    filename = os.path.basename(bpy.path.abspath(filepath))
    if not ext:
        filename, fileext = os.path.splitext(filename)
    return filename


def GetTmpDirectory():
    return tempfile.gettempdir()


# Convert slashes to unix style
#
def UnifyPath(filepath, relative=False):
    if relative:
        if filepath.startswith('//'):
            return filepath[2:].replace('\\', '/')

    filepath = os.path.normpath(bpy.path.abspath(filepath))
    filepath = filepath.replace('\\', '/')

    return filepath


def path_sep_to_unix(filepath):
    # if sys.platform != 'win32':
    filepath = filepath.replace('\\\\', '/')
    filepath = filepath.replace('\\', '/')

    return filepath


def Quotes(path):
    if sys.platform == 'win32':
        return path
    return '"%s"' % (path)


def GetPreviewDir():
    previewRoot   = tempfile.gettempdir()
    previewSubdir = "vrayblender_preview_%s" % SysUtils.GetUsername()
    if sys.platform == 'linux':
        previewRoot = "/dev/shm"
    previewDir = os.path.join(previewRoot, previewSubdir)
    return CreateDirectory(previewDir)


def CopyTree(src, dst, symlinks=False, ignore=None):
    if sys.platform == 'win32':
        os.system('robocopy /E "%s" "%s"' % (src, dst))
    else:
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)


def CreateDirectory(directory):
    directory = path_sep_to_unix(directory)
    if not os.path.exists(directory):
        debug.Debug('Creating directory "%s"...' % directory)
        try:
            os.mkdir(directory)
        except OSError:
            debug.Debug('Error creating directory: "%s"' % directory, msgType='ERROR')
            directory = tempfile.gettempdir()
            debug.Debug("Using TMP path: %s" % directory)
    return directory


def CreateDirectoryFromFilepath(filepath):
    dirPath, fileName = os.path.split(bpy.path.abspath(filepath))
    dirPath = CreateDirectory(dirPath)
    return os.path.join(dirPath, fileName)


# @srcFilepath - full absolute path
#
def CopyDRAsset(bus, srcFilepath):
    scene = bus['scene']

    VRayScene = scene.vray
    VRayDR    = VRayScene.VRayDR

    srcFilepath = os.path.normpath(srcFilepath)
    dstRoot     = CreateDirectory(bpy.path.abspath(VRayDR.shared_dir))

    ExtToSubdir = {
        'ies'    : "ies",
        'lens'   : "misc",
        'vrmesh' : "proxy",
        'vrmap'  : "lightmaps",
    }

    srcFilename = os.path.basename(srcFilepath)

    srcFiletype = os.path.splitext(srcFilename)[1]

    assetSubdir = ExtToSubdir.get(srcFiletype.lower(), "textures")

    if assetSubdir:
        dstRoot = CreateDirectory(os.path.join(dstRoot, assetSubdir))

    dstFilepath = os.path.join(dstRoot, srcFilename)

    if not os.path.exists(srcFilepath):
        # debug.PrintError('"%s" file does not exists!' % srcFilepath)
        return srcFilepath

    if not os.path.isfile(srcFilepath):
        debug.PrintError('"%s" is not a file!' % srcFilepath)
        return srcFilepath

    else:
        if os.path.exists(dstFilepath):
            if not filecmp.cmp(srcFilepath, dstFilepath):
                debug.Debug('Copying "%s" to "%s"'% (debug.Color(srcFilename, 'magenta'), dstRoot))

                shutil.copyfile(srcFilepath, dstFilepath)

            else:
                debug.Debug('File "%s" exists and not modified.'% debug.Color(srcFilename, 'magenta'))

        else:
            debug.Debug('Copying "%s" to "%s"' % (debug.Color(srcFilename, 'magenta'), dstRoot))

            shutil.copyfile(srcFilepath, dstFilepath)

    if VRayDR.networkType == 'WW':
        return pathlib.Path(r'\\') / SysUtils.GetHostname() / VRayDR.share_name / assetSubdir / srcFilename

    return dstFilepath

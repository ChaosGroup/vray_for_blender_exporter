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

import bpy

from vb30 import debug

from . import SysUtils

def GetFilename(filepath, ext=True):
    filename = os.path.basename(bpy.path.abspath(filepath))
    if not ext:
        filename, fileext = os.path.splitext(filename)
    return filename


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
    if sys.platform == 'linux':
        return "/dev/shm/vrayblender_preview"
    return os.path.join(tempfile.gettempdir(), "vrayblender_preview_%s" % SysUtils.GetUsername())


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


def create_dir_from_filepath(filepath):
    file_path, file_name= os.path.split(bpy.path.abspath(filepath))
    file_path= create_dir(file_path)
    return os.path.join(file_path, file_name)


# Get full filepath
# Also copies file to DR shared folder
def get_full_filepath(bus, ob, filepath):
    def rel_path(filepath):
        if filepath[:2] == "//":
            return True
        else:
            return False

    scene= bus['scene']

    VRayDR= scene.vray.VRayDR

    # If object is linked and path is relative
    # we need to find correct absolute path
    if ob and ob.library and rel_path(filepath):
        lib_path= os.path.dirname(bpy.path.abspath(ob.library.filepath))
        filepath= os.path.normpath(os.path.join(lib_path,filepath[2:]))

    # Full absolute file path
    src_file = bpy.path.abspath(filepath)
    src_file = path_sep_to_unix(src_file)
    src_file = os.path.normpath(src_file)

    if not VRayDR.on:
        return src_file

    # File name
    src_filename= os.path.basename(src_file)

    # DR shared directory
    dest_path= bus['filenames']['DR']['dest_dir']

    # If shared directory is not set
    # just return absolute file path
    if not dest_path:
        return src_file

    file_type= os.path.splitext(src_file)[1]

    component_subdir= ""
    if file_type.lower() in {'ies','lens'}:
        component_subdir= "misc"
    elif file_type.lower() == "vrmesh":
        component_subdir= "proxy"
    elif file_type.lower() == "vrmap":
        component_subdir= "lightmaps"
    else:
        component_subdir= "textures"

    if component_subdir:
        dest_path= create_dir(os.path.join(dest_path, component_subdir))

    # Copy file to the shared directory
    dest_file= os.path.join(dest_path, src_filename)

    if os.path.isfile(src_file):
        if os.path.exists(dest_file):
            # Copy only if the file was changed
            if not filecmp.cmp(dest_file, src_file):
                debug(scene, "Copying \"%s\" to \"%s\""% (color(src_filename, 'magenta'), dest_path))
                shutil.copyfile(src_file, dest_file)
            else:
                debug(scene, "File \"%s\" exists and not modified."% (color(src_filename, 'magenta')))
        else:
            debug(scene, "Copying \"%s\" to \"%s\"" % (color(src_filename, 'magenta'), dest_path))
            shutil.copyfile(src_file, dest_file)
    else:
        debug(scene, "\"%s\" is not a file!" % (src_file), error= True)
        return src_file

    if VRayDR.type == 'WW':
        return "//%s/%s/%s/%s/%s"%(HOSTNAME,
                                   VRayDR.share_name,
                                   bus['filenames']['DR']['sub_dir'], component_subdir, src_filename)

    return bus['filenames']['DR']['prefix'] + os.sep + component_subdir + os.sep + src_filename

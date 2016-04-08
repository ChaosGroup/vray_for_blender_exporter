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

import bpy

from vb30 import debug
from vb30.lib import ExportUtils
from vb30.lib import PluginUtils
from vb30.lib import PathUtils
from vb30.lib import LibUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene  = bus['scene']
    o      = bus['output']
    camera = bus['camera']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter
    BakeView     = VRayScene.BakeView
    img_width  = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    img_height = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

    # NOTE: Camera could be None when saving a preset, for example
    if camera:
        VRayCamera = camera.data.vray
        CameraStereoscopic = VRayCamera.CameraStereoscopic

        if VRayScene.RTEngine.enabled:
            if VRayScene.SettingsRTEngine.stereo_mode:
                img_width *= 2
        else:
            if VRayScene.VRayStereoscopicSettings.use and not CameraStereoscopic.use:
                if VRayScene.VRayStereoscopicSettings.adjust_resolution:
                    img_width *= 2

    if BakeView.use:
        if BakeView.square_resolution:
            img_height = img_width

    overrideParams['img_width']  = img_width
    overrideParams['img_height'] = img_height
    overrideParams['bmp_width']  = img_width
    overrideParams['bmp_height'] = img_height
    overrideParams['rgn_width']  = img_width
    overrideParams['rgn_height'] = img_height
    overrideParams['r_width']    = img_width
    overrideParams['r_height']   = img_height

    if not (o.isPreviewRender() or VRayExporter.auto_save_render):
        overrideParams['img_file'] = ""
        overrideParams['img_dir']  = ""
    else:
        # NOTE: Could happen when saving preset
        if hasattr(o, 'getFileManager'):
            pm = o.getFileManager().getPathManager()
            img_file = pm.getImgFilename()
            img_dir  = pm.getImgDirpath()

            if not img_file:
                debug.PrintError("Image output filename is not set!")
                return None

            if not img_dir:
                debug.PrintError("Image output directory is not set!")
                return None

            # In case filename is setup as some filepath
            img_file = os.path.basename(bpy.path.abspath(img_file))

            overrideParams['img_file'] = img_file
            overrideParams['img_dir']  = img_dir

            if o.isPreviewRender():
                overrideParams['img_file_needFrameNumber'] = False

            if propGroup.img_format in {'EXR', 'VRST'}:
                if not propGroup.relements_separateFiles:
                    overrideParams['img_rawFile'] = True

    # NOTE: When loading preview image for World
    # image alpha will be replaced with black color.
    # We don't want this, so simply use JPEG,
    # that doesn't have alpha channel
    if o.isPreviewRender():
        overrideParams['img_noAlpha'] = True

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

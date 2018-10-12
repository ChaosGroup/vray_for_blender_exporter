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

import time
import os

from vb30 import debug

@debug.TimeIt
def LoadImage(scene, engine, imageFile, p):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.animation_mode not in {'NONE'}:
        return

    imageToBlender = VRayExporter.auto_save_render and VRayExporter.image_to_blender
    if not (engine.is_preview or imageToBlender):
        return

    debug.Debug('ImageFile [%s]' % imageFile)

    # There was some version that was always adding frame number
    imageFilePreviewCompat = imageFile.replace("preview.exr", "preview.000%i.exr" % scene.frame_current)

    resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

    # TODO: Create VRayImage loader and load image while rendering
    #
    while not engine.test_break():
        if not p.is_running():
            result = engine.begin_result(0, 0, resolution_x, resolution_y)
            if engine.test_break():
                break
            layer = result.layers[0]
            try:
                if os.path.exists(imageFile):
                    layer.load_from_file(imageFile)
                elif engine.is_preview and os.path.exists(imageFilePreviewCompat):
                    layer.load_from_file(imageFilePreviewCompat)
            except Exception as e:
                debug.Debug("Error loading file! [%s]" % e, msgType='ERROR')
            if engine.test_break():
                break
            engine.end_result(result)
            break
        time.sleep(0.001)

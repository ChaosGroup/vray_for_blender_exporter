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

from vb30 import debug


def LoadImage(scene, engine, o, p):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.animation_mode not in {'NONE'}:
        return

    imageToBlender = VRayExporter.auto_save_render and VRayExporter.image_to_blender
    if not (engine.is_preview or imageToBlender):
        return

    pm = o.getFileManager().getPathManager()

    imageFile = pm.getImgLoadFilepath()

    resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

    # TODO: Create VRayImage loader and load image while rendering
    #
    while True:
        if not p.is_running():
            result = engine.begin_result(0, 0, resolution_x, resolution_y)
            layer = result.layers[0]
            try:
                layer.load_from_file(imageFile)
            except:
                debug.Debug("Error loading file!", msgType='ERROR')
            engine.end_result(result)
            break
        time.sleep(0.1)

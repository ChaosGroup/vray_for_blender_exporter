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

import _vray_for_blender

from vb30.lib import BlenderUtils

from vb30 import debug


@debug.TimeIt
def ExportObjects(bus, exportNodes=True, exportMeshes=None):
    o      = bus['output']
    scene  = bus['scene']
    camera = bus['camera']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    # Setup object to skip, this is mainly from "Effect" gizmos
    skipObjects = [ob.as_pointer() for ob in bus['skipObjects']]
    _vray_for_blender.setSkipObjects(bus['exporter'], skipObjects)

    # Setup "Hide From View"
    hideFromView = BlenderUtils.GetCameraHideLists(camera)
    _vray_for_blender.setHideFromView(bus['exporter'], hideFromView)

    # Finally export stuff
    exportGeometry = exportMeshes if exportMeshes is not None else VRayExporter.auto_meshes

    _vray_for_blender.exportScene(
        bus['exporter'],
        exportNodes,
        exportGeometry
    )

    # Clean current frame name cache
    bus['cache']['plugins'] = set()
    _vray_for_blender.clearCache()
    o.resetNamesCache()

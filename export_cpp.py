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

import _vray_for_blender

from vb30.lib.VRayStream import VRayStream
from vb30                import utils
from vb30                import export


def ExportFrame(bus):
    scene = bus['scene']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    export.ExportSettings(bus)

    _vray_for_blender.setSkipObjects(bus['exporter'], set())
    _vray_for_blender.exportScene(bus['exporter'], True, True)

    # Clean current frame name cache
    _vray_for_blender.clearCache()


def Export(data, scene, engine, is_preview=False, is_viewport=False):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter
    o            = VRayStream

    o.setMode('VRSCENE')
    o.overwriteGeometry = VRayExporter.auto_meshes

    bus = {
        'camera'     : scene.camera,
        'context'    : {},
        'engine'     : engine,
        'frame'      : scene.frame_current,
        'gizmos'     : set(),
        'output'     : o,
        'preview'    : is_preview,
        'scene'      : scene,
        'visibility' : utils.get_visibility_lists(scene.camera),
        'volumes'    : set(),

        'cache' : {
            'plugins' : set(),
            'mesh'    : set(),
            'nodes'   : set(),
        },

        'defaults' : {
            'brdf'     : "BRDFNOBRDFISSET",
            'material' : "MANOMATERIALISSET",
            'texture'  : "TENOTEXTUREIESSET",
            'uvwgen'   : "DEFAULTUVWC",
            'blend'    : "TEDefaultBlend",
        },
    }

    # Init output files
    # XXX: Refactor this
    err = utils.init_files(bus)
    if err:
        return err

    isAnimation   = VRayExporter.animation and VRayExporter.animation_type in {'FULL'}
    checkAnimated = int(VRayExporter.check_animated)

    bus['exporter'] = _vray_for_blender.init(
        scene   = scene.as_pointer(),
        engine  = engine.as_pointer(),
        context = bpy.context.as_pointer(),

        objectFile   = o.getFileByType('OBJECT'),
        geometryFile = o.getFileByType('GEOMETRY'),
        lightsFile   = o.getFileByType('LIGHT'),

        useNodes = True
    )

    _vray_for_blender.initCache(isAnimation, checkAnimated)

    ExportFrame(bus)

    _vray_for_blender.clearFrames()

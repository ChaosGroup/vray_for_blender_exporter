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

# Exporter workflow:
#   - Export "Environment" with Python and "Effects" with Python and C++ Python API
#     and prepare exclude lists for further exclusion from 'Nodes'
#   - Export lights with Python
#   - Export geometry, objects and particles/dupli with C++
#   - Export material nodetrees with C++
#   - Export "Render Elements" with Python
#   - Start static/animation render
#   - Load image back for "Preview" renderer or if "Image To Blender" is turned on
#

import bpy

import _vray_for_blender

from vb30.lib.VRayStream import VRayPluginExporter
from vb30                import utils
from vb30                import export
from vb30                import debug


def ExportFrame(bus):
    scene = bus['scene']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    # Export lights
    for ob in export.GetObjects(bus):
        if ob.type == 'LAMP':
            # Node struct
            bus['node'] = {
                # Currently processes object
                'object' : ob,

                # Object visibility
                'visible' : ob,

                # Attributes for particle / dupli export
                'base' : ob,
                'dupli' : {},
                'particle' : {},
            }

            export.write_lamp(bus)

    _vray_for_blender.setSkipObjects(bus['exporter'], set())
    _vray_for_blender.exportScene(bus['exporter'], True, VRayExporter.auto_meshes)

    # Clean current frame name cache
    _vray_for_blender.clearCache()



def ExportAnimation(bus):
    scene = bus['scene']
    o     = bus['output']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.animation_type == 'FRAMEBYFRAME':
        if VRayExporter.use_still_motion_blur:
            pass
    else:
        o.frameStep = scene.frame_step

        # Store current frame
        selected_frame = scene.frame_current

        f = scene.frame_start
        while(f <= scene.frame_end):
            scene.frame_set(f)
            o.frameNumber = f

            ExportFrame(bus)

            f += scene.frame_step

        # Restore selected frame
        scene.frame_set(selected_frame)


def ExportEx(data, scene, engine, isPreview=False):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    isAnimation   = VRayExporter.animation and VRayExporter.animation_type in {'FULL'}

    o = VRayPluginExporter()
    o.overwriteGeometry = VRayExporter.auto_meshes
    o.isAnimation       = isAnimation

    bus = {
        'camera'     : scene.camera,
        'context'    : {},
        'engine'     : engine,
        'frame'      : scene.frame_current,
        'gizmos'     : set(),
        'output'     : o,
        'preview'    : isPreview,
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

    bus['exporter'] = _vray_for_blender.init(
        scene   = scene.as_pointer(),
        engine  = engine.as_pointer(),
        context = bpy.context.as_pointer(),

        objectFile   = o.getFileByType('OBJECT'),
        geometryFile = o.getFileByType('GEOMETRY'),
        lightsFile   = o.getFileByType('LIGHT'),

        useNodes     = True,
        materialFile = o.getFileByType('MATERIAL'),
        textureFile  = o.getFileByType('TEXTURE'),
    )

    _vray_for_blender.initCache(isAnimation, 1)

    o.write('MAIN', "\n")
    o.write('MAIN', utils.get_vrscene_template("defaults.vrscene"))

    export.ExportSettings(bus)

    if VRayExporter.animation:
        ExportAnimation(bus)
    else:
        ExportFrame(bus)

    _vray_for_blender.clearFrames()

    o.closeFiles()

    return None


def Export(data, scene, engine, isPreview=False):
    try:
        # Do everythign here; basically because we want to close files
        # if smth goes wrong...
        #
        ExportEx(data, scene, engine, isPreview)
    except Exception as e:
        debug.ExceptionInfo(e)
        # Close files here
        # o.closeFiles()
        return "Export error! Check system console!"

    return None

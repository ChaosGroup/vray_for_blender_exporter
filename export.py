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
import time
import datetime

import bpy

from vb30.lib.VRayStream import getExportFilesPaths

from vb30.lib import SysUtils, BlenderUtils, PathUtils

from vb30.nodes import export as NodesExport

from vb30.exporting import exp_run

from vb30 import debug

import _vray_for_blender_rt


def nonRenderVrsceneExport(vrscene, useAnimation=False, frames=None, onlySelected=False, groupName=None, objectName=None, ntree=None, assetType=None):
    scene = bpy.context.scene

    arguments = {
        'context'      : bpy.context.as_pointer(),
        'engine'       : 0,
        'data'         : bpy.data.as_pointer(),
        'scene'        : scene.as_pointer(),
        'mainFile'     : vrscene,
        'objectFile'   : vrscene,
        'envFile'      : vrscene,
        'geometryFile' : vrscene,
        'lightsFile'   : vrscene,
        'materialFile' : vrscene,
        'textureFile'  : vrscene,
        'cameraFile'   : vrscene,
    }

    exporter = _vray_for_blender_rt.init(**arguments)
    if not exporter:
        return None

    optionsArgs = {
        'exporter': exporter,
        'useAnimation': useAnimation,
    }

    if useAnimation and frames:
        optionsArgs['firstFrame'] = frames[0]
        optionsArgs['lastFrame'] = frames[1]

    if onlySelected:
        optionsArgs['onlySelected'] = True
    if groupName:
        optionsArgs['groupName'] = groupName
    if objectName:
        optionsArgs['objectName'] = objectName
    if ntree:
        optionsArgs['ntreeId'] = ntree.id_data.as_pointer()
        optionsArgs['ntree'] = ntree.as_pointer()
        if assetType:
            optionsArgs['assetType'] = assetType

    if _vray_for_blender_rt.set_export_options(**optionsArgs):
        _vray_for_blender_rt.render(exporter)

    _vray_for_blender_rt.free(exporter)

    if not frames:
        frames = (scene.frame_start, scene.frame_end)
    return (vrscene, frames)



def ExportEx(bus):
    debug.Debug("ExportEx()")

    err = None

    scene  = bus['scene']
    engine = bus['engine']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    pathSettings = getExportFilesPaths(engine, scene)
    bus['outputFilePath'] = pathSettings['scene']['MAIN']

    try:

        if not VRayExporter.animation_mode in {'NONE', 'CAMERA_LOOP'}:
            bus['frameStart'] = scene.frame_start
            bus['frameEnd'] = scene.frame_end
            bus['frameStep'] = scene.frame_step
        elif VRayExporter.animation_mode == 'CAMERA_LOOP':
            cameraCount = len([1 for o in scene.objects if o.type == 'CAMERA' and o.data.vray.use_camera_loop])
            bus['frameStart'] = 1
            bus['frameEnd'] = cameraCount
            bus['frameStep'] = 1

        init = {
            'context'      : bpy.context.as_pointer(),
            'engine'       : engine.as_pointer(),
            'data'         : bpy.data.as_pointer(),
            'scene'        : scene.as_pointer(),
            'mainFile'     : pathSettings['scene']['MAIN'],
            'objectFile'   : pathSettings['scene']['OBJECT'],
            'envFile'      : pathSettings['scene']['WORLD'],
            'geometryFile' : pathSettings['scene']['GEOMETRY'],
            'lightsFile'   : pathSettings['scene']['LIGHT'],
            'materialFile' : pathSettings['scene']['MATERIAL'],
            'textureFile'  : pathSettings['scene']['TEXTURE'],
            'cameraFile'   : pathSettings['scene']['CAMERA'],
        }

        # Free anything we have
        if engine.renderer:
            del engine.renderer

        renderer = _vray_for_blender_rt.init(**init)
        if renderer:
            setattr(engine, 'renderer', renderer)
            _vray_for_blender_rt.render(renderer)

    except Exception as e:
        debug.ExceptionInfo(e)
        err = str(e)

    return err


def ExportAndRun(engine, scene):
    if engine.test_break():
        return "Export is interrupted!"

    VRayScene    = scene.vray

    bus = {
        'engine' : engine,
        'scene'  : scene,
        'camera' : scene.camera,
    }

    if bus['camera'].type != 'CAMERA':
        return "Scene's active camera is not of type camera"

    err = ExportEx(bus)
    if err is not None:
        return err

    err = exp_run.RunEx(bus)
    if err is not None:
        return err

    return None


# First check the animation type:
#
# 'FRAMEBYFRAME' "Export and render frame by frame"
# 'FULL'         "Export full animation range then render"
# 'NOTMESHES'    "Export full animation range without meshes"
# 'CAMERA'       "Export full animation of camera motion"
#
# 'FRAMEBYFRAME' should also support exporting of 2 (or more) frames at once for correct motion blur
#
def RenderScene(engine, scene):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    err = None

    if VRayExporter.animation_mode == 'FRAMEBYFRAME':
        # Store current frame
        selected_frame = scene.frame_current

        f = scene.frame_start
        while(f <= scene.frame_end):
            scene.frame_set(f)

            err = ExportAndRun(engine, scene)
            if err is not None:
                break

            f += scene.frame_step

        # Restore selected frame
        scene.frame_set(selected_frame)

    else:
        err = ExportAndRun(engine, scene)

    return err

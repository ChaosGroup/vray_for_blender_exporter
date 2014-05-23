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

import time

import bpy

import _vray_for_blender

from vb30.plugins import PLUGINS, PLUGINS_ID

from vb30.lib import BlenderUtils, SysUtils, ExportUtils, LibUtils

from vb30.lib.VRayProcess import VRayProcess
from vb30.lib.VRayStream  import VRayExportFiles
from vb30.lib.VRayStream  import VRayPluginExporter
from vb30.lib.VRayStream  import VRayFilePaths

from vb30.nodes import export as NodesExport

from vb30 import debug

from vb30.debug import Debug

from vb30 import exporting


   ###    ##    ## #### ##     ##    ###    ######## ####  #######  ##    ## 
  ## ##   ###   ##  ##  ###   ###   ## ##      ##     ##  ##     ## ###   ## 
 ##   ##  ####  ##  ##  #### ####  ##   ##     ##     ##  ##     ## ####  ## 
##     ## ## ## ##  ##  ## ### ## ##     ##    ##     ##  ##     ## ## ## ## 
######### ##  ####  ##  ##     ## #########    ##     ##  ##     ## ##  #### 
##     ## ##   ###  ##  ##     ## ##     ##    ##     ##  ##     ## ##   ### 
##     ## ##    ## #### ##     ## ##     ##    ##    ####  #######  ##    ## 

def ExportAnimation(bus):
    Debug("ExportAnimation()")

    scene = bus['scene']
    o     = bus['output']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    # Set frame step; used to detect if we need
    # to export a keyframe in interpolate()
    o.setFrameStep(scene.frame_step)

    # Store current frame
    selected_frame = scene.frame_current

    f = scene.frame_start
    while(f <= scene.frame_end):
        scene.frame_set(f)
        o.setFrame(f)
        _vray_for_blender.setFrame(f)

        ExportFrame(bus)

        f += scene.frame_step

    # Restore selected frame
    scene.frame_set(selected_frame)


######## ##     ## ########   #######  ########  ######## 
##        ##   ##  ##     ## ##     ## ##     ##    ##    
##         ## ##   ##     ## ##     ## ##     ##    ##    
######      ###    ########  ##     ## ########     ##    
##         ## ##   ##        ##     ## ##   ##      ##    
##        ##   ##  ##        ##     ## ##    ##     ##    
######## ##     ## ##         #######  ##     ##    ##    

def Export(bus, scene, engine, isPreview=False):
    Debug("Export()")

    o = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    o.write('MAIN', "\n")
    o.write('MAIN', SysUtils.GetVRsceneTemplate("defaults.vrscene"))

    ExportSettings(bus)

    ExportRenderElements(bus)

    if VRayExporter.animation:
        if VRayExporter.animation_type == 'FRAMEBYFRAME':
            ExportAnimationFrameByFrame(bus)
        else:
            ExportAnimation(bus)
    else:
        if VRayExporter.use_still_motion_blur:
            ExportTwoFrames(bus, scene, engine)
        elif VRayExporter.camera_loop:
            ExportCameraLoop(bus, scene, engine)

    _vray_for_blender.clearFrames()

    return None


######## ##     ## ########   #######  ########  ########    ######## ##     ## 
##        ##   ##  ##     ## ##     ## ##     ##    ##       ##        ##   ##  
##         ## ##   ##     ## ##     ## ##     ##    ##       ##         ## ##   
######      ###    ########  ##     ## ########     ##       ######      ###    
##         ## ##   ##        ##     ## ##   ##      ##       ##         ## ##   
##        ##   ##  ##        ##     ## ##    ##     ##       ##        ##   ##  
######## ##     ## ##         #######  ##     ##    ##       ######## ##     ## 

def ExportEx(scene, engine, o, isPreview=False):
    Debug("ExportEx()")

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter
    VRayDR       = VRayScene.VRayDR

    err = None

    isAnimation = VRayExporter.animation and VRayExporter.animation_type in {'FULL'}

    separateFiles = VRayExporter.useSeparateFiles
    if VRayDR.on:
        if VRayDR.transferAssets == '0':
            separateFiles = False

    fm = VRayExportFiles()
    fm.setSeparateFiles(separateFiles)
    fm.setExportDirectory("/tmp/vrayblender_bdancer")
    fm.setBaseName("scene")
    fm.setOverwriteGeometry(VRayExporter.auto_meshes)

    if VRayDR.on:
        pass

    try:
        fm.init()
    except Exception as e:
        debug.ExceptionInfo(e)
        return "Error initing files!"

    o.setFileManager(fm)
    o.setPreview(isPreview)
    o.setAnimation(isAnimation)

    try:
        # We do everything here basically because we want to close files
        # if smth goes wrong...
        Export(bus, scene, engine, isPreview)
    except Exception as e:
        debug.ExceptionInfo(e)
        err = "Export error! Check system console!"
    finally:
        o.done()

    return err


def LoadImage(scene, engine, o, p):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.animation:
        return

    imageToBlender = VRayExporter.auto_save_render and VRayExporter.image_to_blender
    if not (engine.is_preview or imageToBlender):
        return

    imageFile = o.getImageFile()

    resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

    # TODO: Create VRayImage loader and load image while rendering
    #
    while True:
        if engine.test_break():
            break
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


########  ##     ## ##    ## 
##     ## ##     ## ###   ## 
##     ## ##     ## ####  ## 
########  ##     ## ## ## ## 
##   ##   ##     ## ##  #### 
##    ##  ##     ## ##   ### 
##     ##  #######  ##    ## 

def Run(scene, engine, o):
    Debug("Run()")

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    p = VRayProcess()
    p.setVRayStandalone(SysUtils.GetVRayStandalonePath())
    p.setSceneFile(o.fileManager.getOutputFilepath())
    p.setAutorun(VRayExporter.autorun)
    p.setVerboseLevel(VRayExporter.verboseLevel)
    p.setShowProgress(VRayExporter.showProgress)
    p.setDisplaySRGB(VRayExporter.display_srgb)

    # TODO: Rewrite into 'SettingsOutput'
    #
    # if scene.render.use_border:
    #     resolution_x = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    #     resolution_y = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)
    #
    #     x0 = resolution_x *        scene.render.border_min_x
    #     y0 = resolution_y * (1.0 - scene.render.border_max_y)
    #     x1 = resolution_x *        scene.render.border_max_x
    #     y1 = resolution_y * (1.0 - scene.render.border_min_y)
    #
    #     p.setRegion(x0, y0, x1, y1, useCrop=scene.render.use_crop_to_border)

    if engine.is_preview:
        p.setOutputFile(preview_file)
        p.setShowProgress(0)
        p.setVerboseLevel(0)
        p.setAutoclose(True)
        p.setDisplayVFB(False)

    if o.isAnimation:
        p.setFrames(scene.frame_start, scene.frame_end, scene.frame_step)

    if not scene.render.threads_mode == 'AUTO':
        p.setThreads(scene.render.threads)

    if bpy.app.background or VRayExporter.wait:
        p.setWaitExit(True)
        if bpy.app.background:
            p.setDisplayVFB(False) # Disable VFB
            p.setAutoclose(True)   # Exit on render end

    p.run()

    LoadImage(scene, engine, o, p)


def RunEx(scene, engine, o):
    Debug("RunEx()")

    try:
        Run(scene, engine, o)
    except Exception as e:
        debug.ExceptionInfo(e)
        return "Run error! Check system console!"
    return None


######## ########     ###    ##     ## ########    ########  ##    ##    ######## ########     ###    ##     ## ######## 
##       ##     ##   ## ##   ###   ### ##          ##     ##  ##  ##     ##       ##     ##   ## ##   ###   ### ##       
##       ##     ##  ##   ##  #### #### ##          ##     ##   ####      ##       ##     ##  ##   ##  #### #### ##       
######   ########  ##     ## ## ### ## ######      ########     ##       ######   ########  ##     ## ## ### ## ######   
##       ##   ##   ######### ##     ## ##          ##     ##    ##       ##       ##   ##   ######### ##     ## ##       
##       ##    ##  ##     ## ##     ## ##          ##     ##    ##       ##       ##    ##  ##     ## ##     ## ##       
##       ##     ## ##     ## ##     ## ########    ########     ##       ##       ##     ## ##     ## ##     ## ######## 

def ExportAnimationFrameByFrame(bus):
    Debug("ExportAnimationFrameByFrame()")


# First check the animation type
#
# 'FRAMEBYFRAME' "Export and render frame by frame"
# 'FULL'         "Export full animation range then render"
# 'NOTMESHES'    "Export full animation range without meshes"
# 'CAMERA'       "Export full animation of camera motion"
#
# 'FRAMEBYFRAME' should also support exporting of 2 (or more) frames at once for correct motion blur
#

def InitBus(engine, scene):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    return {
        'output' : o,

        'engine' : engine,
        'scene'  : scene,
        'camera' : scene.camera,

        'frame'  : scene.frame_current,

        'skipObjects'        : set(),
        'environment_volume' : set(),
        'gizmos'             : set(),

        'lightlinker' : {},

        'preview'    : isPreview,

        # Used to pass nodes into plugin exporter
        # to access some special data like 'fake' textures
        'context' : {
            'node' : None,
        },

        'cache' : {
            'plugins' : set(),
            'mesh'    : set(),
        },

        'defaults' : {
            'brdf'     : "BRDFNOBRDFISSET",
            'material' : "MANOMATERIALISSET",
            'texture'  : "TENOTEXTUREIESSET",
            'uvwgen'   : "DEFAULTUVWC",
            'blend'    : "TEDefaultBlend",
        },
    }


def RenderScene(engine, scene):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    fp = VRayFilePaths()

    err = export.ExportEx(bus)
    if err is not None:
        return err

    err = export.RunEx(bus)
    if err is not None:
        return err

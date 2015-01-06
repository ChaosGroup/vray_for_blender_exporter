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

import _vray_for_blender

from vb30.lib import BlenderUtils
from vb30.lib import PathUtils
from vb30.lib import VRayStream

from vb30 import proxy as ProxyTools

TYPE = 'SYSTEM'
ID   = 'ExportSets'
NAME = 'Export Sets'
DESC = "Custom export sets"


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##

def ExportObjects(objects, filepath, animation='NONE', frameStart=1, frameEnd=10):
    scene = bpy.context.scene

    vrsceneFile = open(filepath, 'w')

    o = VRayStream.VRaySimplePluginExporter(outputFile=vrsceneFile)

    exporter = _vray_for_blender.init(
        engine  = 0,
        context = bpy.context.as_pointer(),
        scene   = scene.as_pointer(),
        data    = bpy.data.as_pointer(),

        mainFile     = o.output,
        objectFile   = o.output,
        envFile      = o.output,
        geometryFile = o.output,
        lightsFile   = o.output,
        materialFile = o.output,
        textureFile  = o.output,

        drSharePath = "",
    )

    def _export_objects(objects):
        # Init stuff for dupli / particles / etc
        _vray_for_blender.exportObjectsPre(exporter)
        for ob in objects:
            print(ob.name)
            _vray_for_blender.exportObject(ob.as_pointer(), bpy.data.as_pointer(), exporter)
        # Write dupli / particles / etc
        _vray_for_blender.exportObjectsPost(exporter)

    # NOTE: Have to do it before export pre init
    if animation not in {'NONE'}:
        _vray_for_blender.initAnimation(True,
            frameStart,
            frameEnd
        )

    if animation not in {'NONE'}:
        while frameStart <= frameEnd:
            print(frameStart)

            scene.frame_set(frameStart)
            _vray_for_blender.setFrame(frameStart)

            _export_objects(objects)

            frameStart += scene.frame_step
    else:
        _export_objects(objects)

    o.done()
    vrsceneFile.close()
    _vray_for_blender.clearFrames()
    _vray_for_blender.clearCache()
    _vray_for_blender.exit(exporter)


def ExportExportSetItem(item):
    scene = bpy.context.scene
    frameCurrent = scene.frame_current

    dirPath  = item.dirpath
    fileName = item.filename
    if not fileName.endswith(".vrscene"):
        fileName += ".vrscene"

    # Create output path
    dirPath = BlenderUtils.GetFullFilepath(dirPath)
    dirPath = PathUtils.CreateDirectory(dirPath)

    vrsceneFilepath = os.path.join(dirPath, fileName)
    objects         = BlenderUtils.GetGroupObjects(item.group)

    frameStart = item.frame_start if item.use_animation == 'MANUAL' else scene.frame_start
    frameEnd   = item.frame_end   if item.use_animation == 'MANUAL' else scene.frame_end

    ExportObjects(objects, vrsceneFilepath, item.use_animation, frameStart, frameEnd)

    # Restore current frame
    scene.frame_set(frameCurrent)

    return vrsceneFilepath


########  ########   #######  ########         ######   ########   #######  ##     ## ########
##     ## ##     ## ##     ## ##     ##       ##    ##  ##     ## ##     ## ##     ## ##     ##
##     ## ##     ## ##     ## ##     ##       ##        ##     ## ##     ## ##     ## ##     ##
########  ########  ##     ## ########        ##   #### ########  ##     ## ##     ## ########
##        ##   ##   ##     ## ##              ##    ##  ##   ##   ##     ## ##     ## ##
##        ##    ##  ##     ## ##              ##    ##  ##    ##  ##     ## ##     ## ##
##        ##     ##  #######  ##               ######   ##     ##  #######   #######  ##

class VRayExportSetItem(bpy.types.PropertyGroup):
    use = bpy.props.BoolProperty(
        name        = "Use Export Set",
        description = "Use export set",
        default     = True
    )

    dirpath = bpy.props.StringProperty(
        name        = "Dirpath",
        subtype     = 'DIR_PATH',
        default     = "//vrscene/",
        description = "Export directory"
    )

    filename = bpy.props.StringProperty(
        name        = "Filename",
        default     = "MySet",
        description = "Filename (without .vrscene)"
    )

    group = bpy.props.StringProperty(
        name        = "Export Group",
        description = "Group of objects to export"
    )

    use_animation = bpy.props.EnumProperty(
        name        = "Animation",
        description = "Export animated asset",
        items = (
            ('NONE',   "None",   "No animation"),
            ('MANUAL', "Manual", "Set frame range manually"),
            ('SCENE',  "Scene",  "Get frame range from scene")
        ),
        default     = 'NONE'
    )

    frame_start = bpy.props.IntProperty(
        name = "Frame Start",
        default = 1,
    )

    frame_end = bpy.props.IntProperty(
        name = "Frame End",
        default = 250,
    )


class VRayExportSet(bpy.types.PropertyGroup):
    list_items = bpy.props.CollectionProperty(
        type = VRayExportSetItem
    )

    list_item_selected = bpy.props.IntProperty(
        default = -1,
        min     = -1,
        max     = 100
    )

    generate_preview = bpy.props.BoolProperty(
        name        = "Generate Preview Mesh",
        description = "Generate preview mesh file",
        default     = True
    )

    max_preview_faces = bpy.props.IntProperty(
        name    = "Max. Preview Faces",
        default = 100000,
        min     = 1000,
        max     = 1000000
    )


 #######  ########  ######## ########     ###    ########  #######  ########   ######
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ##
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ##
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ##
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ######

class VRayOpExportSetSelected(bpy.types.Operator):
    bl_idname      = "vray.expset_export_selected"
    bl_label       = "Export Selected Set"
    bl_description = "Export selected export set"

    def execute(self, context):
        VRayScene = context.scene.vray
        VRayExporter  = VRayScene.Exporter
        ExportSets    = VRayScene.ExportSets

        if ExportSets.list_item_selected >= 0 and len(ExportSets.list_items) > 0:
            listItem = ExportSets.list_items[ExportSets.list_item_selected]

            vrsceneFilepath = ExportExportSetItem(listItem)

            if ExportSets.generate_preview:
                # NOTE: Generate animated preview?
                ProxyTools.LaunchPly2Vrmesh(vrsceneFilepath,
                    previewFaces=ExportSets.max_preview_faces,
                    previewOnly=True)

            return {'FINISHED'}

        return {'CANCELLED'}


class VRayOpExportSetAll(bpy.types.Operator):
    bl_idname      = "vray.expset_export_all"
    bl_label       = "Export Sets"
    bl_description = "Export sets"

    def execute(self, context):
        return {'FINISHED'}


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayExportSetItem,
        VRayExportSet,
        VRayOpExportSetSelected,
        VRayOpExportSetAll,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    setattr(bpy.types.VRayScene, 'ExportSets', bpy.props.PointerProperty(
        type = VRayExportSet,
        description = "Custom export sets"
    ))


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

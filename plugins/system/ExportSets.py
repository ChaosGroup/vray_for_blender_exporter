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
import _vray_for_blender_rt

from vb30.lib import BlenderUtils
from vb30.lib import PathUtils
from vb30.lib import VRayStream

from vb30.lib.VRayStream import getExportFilesPaths

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

def ExportExportSetItem(item, selectedOnly=False):
    scene = bpy.context.scene

    dirPath  = item.dirpath
    fileName = item.filename
    if not fileName.endswith(".vrscene"):
        fileName += ".vrscene"

    # Create output path
    dirPath = BlenderUtils.GetFullFilepath(dirPath)
    dirPath = PathUtils.CreateDirectory(dirPath)
    vrsceneFilepath = os.path.join(dirPath, fileName)

    arguments = {
        'context'      : bpy.context.as_pointer(),
        'engine'       : 0,
        'data'         : bpy.data.as_pointer(),
        'scene'        : scene.as_pointer(),
        'mainFile'     : vrsceneFilepath,
        'objectFile'   : vrsceneFilepath,
        'envFile'      : vrsceneFilepath,
        'geometryFile' : vrsceneFilepath,
        'lightsFile'   : vrsceneFilepath,
        'materialFile' : vrsceneFilepath,
        'textureFile'  : vrsceneFilepath,
        'cameraFile'   : vrsceneFilepath,
    }
    exporter = _vray_for_blender_rt.init(**arguments)
    if not exporter:
        return None

    frameStart = item.frame_start if item.use_animation == 'MANUAL' else scene.frame_start
    frameEnd   = item.frame_end   if item.use_animation == 'MANUAL' else scene.frame_end

    optionsArgs = {
        'exporter': exporter,
        'firstFrame': frameStart,
        'lastFrame': frameEnd,
        'useAnimation': item.use_animation != 'NONE',
    }

    if selectedOnly:
        optionsArgs['groupName'] = item.group

    if _vray_for_blender_rt.set_export_options(**optionsArgs):
        _vray_for_blender_rt.render(exporter)

    _vray_for_blender_rt.free(exporter)

    return (vrsceneFilepath, (frameStart, frameEnd))


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


class VRayOpExportSetBase:
    def execute(self, context):
        VRayScene = context.scene.vray
        VRayExporter  = VRayScene.Exporter
        ExportSets    = VRayScene.ExportSets

        if ExportSets.list_item_selected >= 0 and len(ExportSets.list_items) > 0:
            listItem = ExportSets.list_items[ExportSets.list_item_selected]
            hasAnimation = listItem.use_animation != 'NONE'

            exportResult = ExportExportSetItem(listItem, selectedOnly=self.selectedOnly)

            if ExportSets.generate_preview and exportResult:
                if hasAnimation:
                    err = ProxyTools.LaunchPly2Vrmesh(exportResult[0],
                        previewFaces=ExportSets.max_preview_faces,
                        previewOnly=True,
                        frames=exportResult[1])
                else:
                    err = ProxyTools.LaunchPly2Vrmesh(exportResult[0],
                        previewFaces=ExportSets.max_preview_faces,
                        previewOnly=True)
                if err:
                    self.report({'ERROR'}, err)

            return {'FINISHED'}

        return {'CANCELLED'}


class VRayOpExportSetSelected(bpy.types.Operator, VRayOpExportSetBase):
    bl_idname      = "vray.expset_export_selected"
    bl_label       = "Export Selected Set"
    bl_description = "Export selected export set"
    selectedOnly   = True


class VRayOpExportSetAll(bpy.types.Operator, VRayOpExportSetBase):
    bl_idname      = "vray.expset_export_all"
    bl_label       = "Export Sets"
    bl_description = "Export sets"
    selectedOnly   = False


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

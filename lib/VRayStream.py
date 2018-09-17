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
import mathutils

import time
import datetime
import os
import sys

from vb30.debug import Debug

from . import LibUtils, PathUtils, SysUtils, BlenderUtils
from . import PluginUtils


PluginTypeToFile = {
    'MAIN'            : 'scene',
    'RENDERCHANNEL'   : 'scene',
    'SETTINGS'        : 'scene',
    'SETTINGS_GLOBAL' : 'scene',
    'OBJECT'          : 'nodes',
    'GEOMETRY'        : 'geometry',
    'CAMERA'          : 'camera',
    'LIGHT'           : 'lights',
    'TEXTURE'         : 'textures',
    'UVWGEN'          : 'textures',
    'BRDF'            : 'materials',
    'MATERIAL'        : 'materials',
    'EFFECT'          : 'environment',
    'WORLD'           : 'environment',
}

NoAttrPlugins = {
    'FilterCatmullRom',
}

def initPathSettings(engine, scene):
    settings = {
        'separateFiles':   False,
        'exportFilename':  "preview",
        'exportDirectory': PathUtils.GetPreviewDir(),
        'imgDirectory':    PathUtils.GetPreviewDir(),
        'imgFilename':     "preview.exr",
        'imgLoadFilename': "preview.exr",
    }

    if engine and engine.is_preview:
        return settings

    VRayScene = scene.vray

    VRayExporter    = VRayScene.Exporter
    VRayDR          = VRayScene.VRayDR
    SettingsOutput  = VRayScene.SettingsOutput
    SettingsOptions = VRayScene.SettingsOptions

    # Blend-file name without extension
    blendfile_name = PathUtils.GetFilename(bpy.data.filepath, ext=False) if bpy.data.filepath else "default"

    # Default export directory is system's %TMP%
    default_dir = PathUtils.GetTmpDirectory()

    # Export and output directory
    export_filepath = os.path.join(default_dir, "vrayblender_"+SysUtils.GetUsername())
    export_filename = "scene"
    output_filepath = default_dir

    if VRayExporter.output == 'USER':
        if VRayExporter.output_dir:
            export_filepath = bpy.path.abspath(VRayExporter.output_dir)

    elif VRayExporter.output == 'SCENE' and bpy.data.filepath:
        sceneFiledir = os.path.dirname(bpy.data.filepath)
        export_filepath = os.path.join(sceneFiledir, "vrscene")

    if VRayExporter.output_unique:
        export_filename = blendfile_name

    if VRayExporter.output == 'USER':
        export_filepath = bpy.path.abspath(VRayExporter.output_dir)

    settings['separateFiles'] = VRayExporter.useSeparateFiles
    if VRayDR.on:
        if VRayDR.assetSharing == 'TRANSFER':
            # "Transfer Asssets" feature doesn't support "#include" statement ATM,
            # so export everything in a single file
            settings['separateFiles'] = False
        elif VRayDR.assetSharing == 'SHARE':
            export_filepath = bpy.path.abspath(VRayDR.shared_dir)

    if VRayExporter.submit_to_vray_cloud:
        settings['separateFiles'] = False

    settings['exportDirectory'] = PathUtils.CreateDirectory(export_filepath)
    settings['exportFilename']  = export_filename

    if VRayExporter.auto_save_render:
        if SettingsOutput.img_dir:
            img_dir = SettingsOutput.img_dir
            if not BlenderUtils.RelativePathValid(img_dir):
                img_dir = default_dir

            output_filepath = bpy.path.abspath(img_dir)
            output_filepath = LibUtils.FormatName(output_filepath)

        # Render output dir
        settings['imgDirectory'] = PathUtils.CreateDirectory(output_filepath)

        # Render output file name
        img_format = {
            '0' : "png",
            '1' : "jpg",
            '2' : "tiff",
            '3' : "tga",
            '4' : "sgi",
            '5' : "exr",
            '6' : "vrimg",
        }
        ext = img_format[SettingsOutput.img_format]

        file_name = "render"
        if SettingsOutput.img_file:
            file_name = SettingsOutput.img_file
            file_name = LibUtils.FormatName(file_name)
            load_file_name = file_name
        settings['imgFilename'] = "%s.%s" % (file_name, ext)

        # Render output - load file name
        if SettingsOutput.img_file_needFrameNumber:
            load_file_name = "%s.%.4i" % (load_file_name, scene.frame_current)

        settings['imgLoadFilename'] = "%s.%s" % (load_file_name, ext)

    return settings


def getExportFilesPaths(engine, scene):
    pathSettings = initPathSettings(engine, scene)
    filePaths = {}

    if not pathSettings['separateFiles']:
        filename = "%s.vrscene" % pathSettings['exportFilename']
        filepath = os.path.join(pathSettings['exportDirectory'], filename)
        fullPath  = os.path.abspath(os.path.normpath(filepath))

        for pluginType in PluginTypeToFile:
            fileType = PluginTypeToFile[pluginType]
            if fileType not in filePaths:
                filePaths[fileType] = fullPath

    else:
        for pluginType in PluginTypeToFile:
            fileType = PluginTypeToFile[pluginType]
            if fileType in filePaths:
                continue

            filename = "%s_%s.vrscene" % (pathSettings['exportFilename'], fileType)
            filepath = os.path.join(pathSettings['exportDirectory'], filename)

            filePaths[fileType] = os.path.abspath(os.path.normpath(filepath))

    fileTypePaths = {}
    for pluginType in PluginTypeToFile:
        typeName = PluginTypeToFile[pluginType]
        fileTypePaths[pluginType] = filePaths[typeName]

    return {
        'path': pathSettings,
        'scene': fileTypePaths
    }


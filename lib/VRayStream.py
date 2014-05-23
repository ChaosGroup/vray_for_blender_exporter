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

from . import LibUtils
from . import PathUtils


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


class VRayFilePaths:
    exportFilename  = None
    exportDirectory = None

    # Export directory could be local but filepath
    # could be network, for example.
    filePrefix      = None

    # Export scene data into separate files
    separateFiles   = None

    # Used to load image back to Blender
    imgFilepath     = None
    imgLoadFilepath = None

    # Used to copy assets in a correspondent subdirectory
    assetSubdirs = None

    def setExportDirectory(self, dirPath):
        self.exportDirectory = dirPath

    def setExportFilename(self, fileName):
        self.exportFilename = fileName

    def setSeparateFiles(self, separate):
        self.separateFiles = separate

    def getExportDirectory(self):
        return self.exportDirectory

    def getFilePrefix(self):
        return self.filePrefix

    def getImgLoadFilepath(self):
        return self.imgLoadFilepath

    def useSeparateFiles(self):
        return self.separateFiles

    def printInfo(self):
        Debug('Export directory: "%s"' % self.exportDirectory)
        if self.assetSubdirs:
            Debug('Asset directories:')
            Debug('  Images: "%s"' % self.assetSubdirs['image'])
            Debug('  IES: "%s"'    % self.assetSubdirs['ies'])
            Debug('  Proxy: "%s"'  % self.assetSubdirs['proxy'])
            Debug('  Misc: "%s"'   % self.assetSubdirs['misc'])
        Debug('Export filename: "%s"' % self.exportFilename)
        if self.filePrefix:
            Debug('Expicit prefix: "%s"' % self.filePrefix)
        Debug('Export filename: "%s"' % self.exportFilename)
        Debug('Separate files: %s' % self.separateFiles)

        if self.imgFilepath:
            Debug('Output file: "%s"' % self.imgFilepath)
            Debug('Load file:   "%s"' % self.imgLoadFilepath)

    def initFromScene(self, scene, engine):
        VRayScene = scene.vray
        
        VRayExporter    = VRayScene.exporter
        VRayDR          = VRayScene.VRayDR
        SettingsOutput  = VRayScene.SettingsOutput
        SettingsOptions = VRayScene.SettingsOptions

        # Blend-file name without extension
        blendfile_name = PathUtils.GetFilename(bpy.data.filepath, ext=False) if bpy.data.filepath else "default"

        # Default export directory is system's %TMP%
        default_dir = tempfile.gettempdir()

        # Export and output directory
        export_filepath = os.path.join(default_dir, "vrayblender_"+get_username())
        export_filename = "scene"
        output_filepath = default_dir

        if SettingsOutput.img_dir:
            img_dir = SettingsOutput.img_dir
            if not RelativePathValid(img_dir):
                img_dir = default_dir
            output_filepath = bpy.path.abspath(img_dir)
            output_filepath = LibUtils.FormatName(output_filepath, scene, blendfile_name)

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

        if engine.is_preview:
            self.exportfileName = "preview"
            self.separateFiles  = False
            self.exportDirectory = PathUtils.GetPreviewDir()
        else:
            if VRayDR.on:
                export_filename = blendfile_name

            # Distributed rendering
            # If not transferring assets
            if VRayDR.on and VRayDR.transferAssets == '0':
                sharedDir = VRayDR.shared_dir
                if sharedDir == "":
                    sharedDir = default_dir
                abs_shared_dir  = os.path.normpath(bpy.path.abspath(sharedDir))
                export_filepath = os.path.normpath(os.path.join(abs_shared_dir, blendfile_name + os.sep))

                bus['filenames']['DR']               = {}
                bus['filenames']['DR']['shared_dir'] = abs_shared_dir
                bus['filenames']['DR']['sub_dir']    = blendfile_name
                bus['filenames']['DR']['dest_dir']   = export_filepath
                bus['filenames']['DR']['prefix']     = bus['filenames']['DR']['dest_dir']
                bus['filenames']['DR']['tex_dir']    = os.path.join(export_filepath, "textures")
                bus['filenames']['DR']['ies_dir']    = os.path.join(export_filepath, "IES")

        self.export_directory = PathUtils.CreateDirectory(export_filepath)

        if VRayExporter.auto_save_render:
            # Render output dir
            bus['filenames']['output'] = PathUtils.CreateDirectory(output_filepath)

            # Render output file name
            ext = SettingsOutput.img_format.lower()

            file_name = "render"
            if SettingsOutput.img_file:
                file_name = SettingsOutput.img_file
                file_name = LibUtils.FormatName(file_name, scene, blendfile_name)
                load_file_name = file_name
            bus['filenames']['output_filename'] = "%s.%s" % (file_name, ext)

            # Render output - load file name
            if SettingsOutput.img_file_needFrameNumber:
                load_file_name = "%s.%.4i" % (load_file_name, scene.frame_current)
            bus['filenames']['output_loadfile'] = "%s.%s" % (load_file_name, ext)

        # Lightmaps path
        # bus['filenames']['lightmaps']= create_dir(os.path.join(export_filepath, "lightmaps"))


class VRayExportFiles:
    def __init__(self):
        # Export directory
        self.exportDir = None

        # *.vrscene files dict
        self.files = {}

        # Filename prefix
        self.baseName = "scene"

        # Whether to use unique prefix
        self.useBaseName = False

        # If to overwrite geometry
        self.overwriteGeometry = True

        # Write particular plugin types to the correspondent file
        self.separateFiles = True

        # Write included files relative
        self.includeRelative = True

        # Use this prefix instead of directory path
        self.explicitPrefix = None

    def setSeparateFiles(self, separateFiles):
        self.setSeparateFiles = separateFiles

    def setExportDirectory(self, exportDir):
        self.exportDir = exportDir

    def setBaseName(self, baseName):
        self.basename = baseName

    def setOverwriteGeometry(self, overwriteGeometry):
        self.overwriteGeometry = overwriteGeometry

    def setPrefix(self, prefix):
        self.explicitPrefix = prefix

    def init(self):
        self.files = {}

        if not self.separateFiles:
            filename = "%s.vrscene" % self.baseName
            filepath = os.path.join(self.exportDir, filename)

            self.files['scene'] = open(filepath, 'w')
        else:
            for pluginType in PluginTypeToFile:
                fileType = PluginTypeToFile[pluginType]
                if fileType in self.files:
                    continue

                filename = "%s_%s.vrscene" % (self.baseName, fileType)
                filepath = os.path.join(self.exportDir, filename)

                fmode = 'w'
                if fileType == 'geometry' and not self.overwriteGeometry:
                    fmode = 'r'

                self.files[fileType] = open(filepath, fmode)

        self.writeHeaders()

        return None


    def writeHeaders(self):
        if not self.files:
            return

        for fileType in self.files:
            if fileType == 'geometry' and not self.overwriteGeometry:
                continue
            self.files[fileType].write("// V-Ray For Blender\n")
            self.files[fileType].write("// %s\n" % datetime.datetime.now().strftime("%A, %d %B %Y %H:%M"))


    def writeIncludes(self):
        if not self.files:
            return

        if self.separateFiles:
            mainFile = self.files['scene']

            for fileType in self.files:
                if fileType == 'scene':
                    continue

                f = self.files[fileType]
                filepath = f.name
                filename = os.path.basename(filepath)

                includeFilepath = filepath
                if self.includeRelative:
                    includeFilepath = filename
                if self.explicitPrefix:
                    includeFilepath = os.path.join(self.explicitPrefix, filename)

                mainFile.write('\n#include "%s"' % includeFilepath)
            mainFile.write('\n')


    def closeFiles(self):
        if not self.files:
            return
        Debug("VRayExportFiles::closeFiles()")
        for fileType in self.files:
            f = self.files[fileType]
            if f and not f.closed:
                f.close()


    def getFileByPluginType(self, pluginType):
        fileType = PluginTypeToFile[pluginType]
        return self.files[fileType]


    def getOutputFile(self, pluginType=None):
        if not self.separateFiles:
            return self.files['scene']
        if not pluginType:
            return self.files['scene']
        return self.getFileByPluginType(pluginType)


    def getOutputFilepath(self, pluginType=None):
        f = self.getOutputFile(pluginType)
        if f:
            return f.name
        return None


class VRayPluginExporter:
    def __init__(self):
        self.fileManager = None

        # Currently processed plugin
        self.pluginType  = None
        self.pluginID    = None
        self.pluginName  = None
        self.pluginAttrs = None

        # Param cache
        # Used to export only changed attributes
        self.pluginCache = dict()
        # Used to export data only once per frame
        self.namesCache  = set()

        # Export properties for animation
        # This option could be set not for real animation, but
        # also for features like "Still Motion Blur" or "Camera Loop"
        self.isAnimation = False
        self.frameNumber = 1
        self.frameStep   = 1

        # Preview renderer
        self.isPreview   = False
        self.imgFile     = ""

    def setAnimation(self, animation):
        self.isAnimation = animation

    def setFrameStep(self, frameStep):
        self.frameStep = frameStep

    def setFrame(self, frame):
        self.frameNumber = frame
        self.namesCache  = set()

    def setFileManager(self, fm):
        self.fileManager = fm

    def setPreview(self, isPreview):
        self.isPreview = isPreview

    def isPreviewRender(self):
        return self.isPreview


    # Set params for currently exported plugin
    #
    def set(self, pluginType, pluginID, pluginName):
        self.pluginType  = pluginType
        self.pluginID    = pluginID
        self.pluginName  = pluginName
        self.pluginAttrs = {}


    # Useless right now; keep for compatibility
    #
    def writeHeader(self):
        if self.pluginName in self.namesCache:
            self.pluginID   = None
            self.pluginName = None
        else:
            self.namesCache.add(self.pluginName)


    # This function will fill pluginAttrs dict
    # Actual write is perfomed by writeFooter
    #
    # self.pluginCache = {
    #   'PluginName' : {
    #       'attrName': (frameNumber, attrValue),
    #       ...
    #   },
    #   ...
    # }
    #
    def _getCachedValue(self, attrName):
        if self.pluginName not in self.pluginCache:
            self.pluginCache[self.pluginName] = {}
            return None,None
        if attrName in self.pluginCache[self.pluginName]:
            attrCache = self.pluginCache[self.pluginName][attrName]
            return attrCache[0], attrCache[1]
        return None,None

    def _storeValueInCache(self, attrName, attrValue):
        self.pluginCache[self.pluginName][attrName] = (self.frameNumber, attrValue)

    def writeAttibute(self, attrName, val):
        # Could also mean that plugin is already exported
        #
        if not self.pluginID and not self.pluginName:
            return

        # If it's not an animation export simply write attr value
        #
        if not self.isAnimation:
            self.pluginAttrs[attrName] = LibUtils.FormatValue(val)

        # If it's an animation we should check the cache and export
        # new value or ever create a keyframe
        #
        else:
            newValue = LibUtils.FormatValue(val)
            cFrame, cValue = self._getCachedValue(attrName)

            attrValue = None

            if cValue is None:
                attrValue  = "interpolate((%i,%s))" % (self.frameNumber, newValue)
            else:
                if newValue == cValue:
                    # New value is the same no need to export
                    return
                else:
                    prevFrame = self.frameNumber - self.frameStep

                    # Cached value is more then frame step back -
                    # need a keyframe
                    if cFrame < prevFrame:
                        attrValue  = "interpolate("
                        attrValue += "(%i,%s)," % (prevFrame,        cValue)
                        attrValue += "(%i,%s)"  % (self.frameNumber, newValue)
                        attrValue += ")"

                    # Cached value is from previous frame -
                    # simply new frame data
                    else:
                        attrValue  = "interpolate((%i,%s))" % (self.frameNumber, newValue)

            # Store in cache
            self._storeValueInCache(attrName, newValue)

            # Store value for writing
            self.pluginAttrs[attrName] = attrValue


    # This will actually write plugin data to file
    #
    def writeFooter(self):
        if not self.fileManager:
            Debug("File manager is not set!", msgType='ERROR')
            return

        # Could also mean that plugin is already exported
        #
        if not self.pluginID and not self.pluginName:
            return

        # No attributes are collected for write
        if not self.pluginAttrs:
            return

        p = "\n%s %s {" % (self.pluginID, self.pluginName)
        for attrName in sorted(self.pluginAttrs.keys()):
            p += "\n\t%s=%s;" % (attrName, self.pluginAttrs[attrName])
        p += "\n}\n"

        self.fileManager.getOutputFile(self.pluginType).write(p)

        # Reset current plugin
        self.pluginType  = None
        self.pluginID    = None
        self.pluginName  = None
        self.pluginAttrs = None


    # Writes arbitary data to file
    #
    def write(self, pluginType, data):
        if not self.fileManager:
            Debug("File manager is not set!", msgType='ERROR')
            return

        self.fileManager.getFileByPluginType(pluginType).write(data)


    def resetNamesCache(self):
        self.namesCache = set()


    def done(self):
        if not self.fileManager:
            Debug("File manager is not set!", msgType='ERROR')
        else:
            self.fileManager.writeIncludes()
            self.fileManager.closeFiles()

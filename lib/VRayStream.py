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


########     ###    ######## ##     ##  ######
##     ##   ## ##      ##    ##     ## ##    ##
##     ##  ##   ##     ##    ##     ## ##
########  ##     ##    ##    #########  ######
##        #########    ##    ##     ##       ##
##        ##     ##    ##    ##     ## ##    ##
##        ##     ##    ##    ##     ##  ######

class VRayFilePaths:
    exportFilename  = None
    exportDirectory = None

    # Export directory could be local but filepath
    # could be network, for example.
    filePrefix      = None

    # Export scene data into separate files
    separateFiles   = None

    # Used to load image back to Blender
    imgDirectory    = None
    imgFilename     = None
    imgLoadFilename = None

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

    def getExportFilename(self):
        return self.exportFilename

    def getFilePrefix(self):
        return self.filePrefix

    def getImgDirpath(self):
        return self.imgDirectory

    def getImgFilename(self):
        return self.imgFilename

    def getImgLoadFilepath(self):
        return os.path.join(self.imgDirectory, self.imgLoadFilename)

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
        Debug('Separate files: %s' % self.separateFiles)

        if self.imgFilename is not None:
            Debug('Output directory: "%s"' % self.imgDirectory)
            Debug('Output file: "%s"' % self.imgFilename)
            Debug('Load file:   "%s"' % self.imgLoadFilename)

    def initFromScene(self, engine, scene):
        if engine.is_preview:
            self.separateFiles   = False
            self.exportFilename  = "preview"
            self.exportDirectory = PathUtils.GetPreviewDir()
            self.imgDirectory    = PathUtils.GetPreviewDir()
            self.imgFilename     = "preview.exr"
            self.imgLoadFilename = "preview.exr"

        else:
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

            if VRayDR.on:
                if VRayDR.assetSharing == 'TRANSFER':
                    # "Transfer Asssets" feature doesn't support "#include" statement ATM,
                    # so export everything in a single file
                    self.separateFiles = False
                elif VRayDR.assetSharing == 'SHARE':
                    export_filepath = bpy.path.abspath(VRayDR.shared_dir)

            self.exportDirectory = PathUtils.CreateDirectory(export_filepath)
            self.exportFilename  = export_filename

            if VRayExporter.auto_save_render:
                if SettingsOutput.img_dir:
                    img_dir = SettingsOutput.img_dir
                    if not BlenderUtils.RelativePathValid(img_dir):
                        img_dir = default_dir

                    output_filepath = bpy.path.abspath(img_dir)
                    output_filepath = LibUtils.FormatName(output_filepath)

                # Render output dir
                self.imgDirectory = PathUtils.CreateDirectory(output_filepath)

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
                self.imgFilename = "%s.%s" % (file_name, ext)

                # Render output - load file name
                if SettingsOutput.img_file_needFrameNumber:
                    load_file_name = "%s.%.4i" % (load_file_name, scene.frame_current)

                self.imgLoadFilename = "%s.%s" % (load_file_name, ext)


######## #### ##       ########  ######
##        ##  ##       ##       ##    ##
##        ##  ##       ##       ##
######    ##  ##       ######    ######
##        ##  ##       ##             ##
##        ##  ##       ##       ##    ##
##       #### ######## ########  ######

class VRayExportFiles:
    def __init__(self, pm):
        # Paths manager
        self.pm = pm

        # *.vrscene files dict
        self.files = {}

        # Export directory
        self.exportDir = pm.getExportDirectory()

        # Filename prefix
        self.baseName = pm.getExportFilename()

        # If to overwrite geometry
        self.overwriteGeometry = True

        # Write particular plugin types to the correspondent file
        self.separateFiles = pm.useSeparateFiles()

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

    def getPathManager(self):
        return self.pm

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
        if not self.separateFiles:
            return

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
        Debug("VRayExportFiles::closeFiles()")
        if not self.files:
            return
        for fileType in self.files:
            f = self.files[fileType]
            if f and not f.closed:
                f.close()


    def getFileByPluginType(self, pluginType):
        if not self.separateFiles:
            return self.files['scene']
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


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##

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
        self.frameStart  = 1
        self.frameEnd    = 2

        # Preview renderer
        self.isPreview   = False
        self.imgFile     = ""

    def setAnimation(self, animation):
        self.isAnimation = animation

    def setFrameStart(self, start):
        self.frameStart = start

    def setFrameEnd(self, end):
        self.frameEnd = end

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

    def getFileManager(self):
        return self.fileManager

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
        if not self.pluginAttrs and self.pluginID not in NoAttrPlugins:
            return

        p = "\n%s %s {" % (self.pluginID, self.pluginName)
        for attrName in sorted(self.pluginAttrs.keys()):
            p += "\n\t%s=%s;" % (attrName, self.pluginAttrs[attrName])
        p += "\n}\n"

        outputFile = self.fileManager.getOutputFile(self.pluginType)
        if self.pluginID == 'VRayStereoscopicSettings':
            outputFile = self.fileManager.getOutputFile('CAMERA')

        outputFile.write(p)

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


class VRaySimplePluginExporter:
    def __init__(self, outputFilepath=None, outputFile=None):
        self.output = outputFile if outputFile else open(outputFilepath, 'w')

        self.namesCache = set()

        # Currently processed plugin
        self.pluginType  = None
        self.pluginID    = None
        self.pluginName  = None
        self.pluginAttrs = None

    def __del__(self):
        self.done()

    # Set params for currently exported plugin
    #
    def set(self, pluginType, pluginID, pluginName):
        self.pluginType  = pluginType
        self.pluginID    = pluginID
        self.pluginName  = pluginName
        self.pluginAttrs = {}

    # Useless right now; keep for compatibility
    def writeHeader(self):
        if self.pluginName in self.namesCache:
            self.pluginID   = None
            self.pluginName = None

    def writeAttibute(self, attrName, val):
        # Could also mean that plugin is already exported
        if not self.pluginID and not self.pluginName:
            return
        # Store value for writing
        self.pluginAttrs[attrName] = LibUtils.FormatValue(val)

    # This will actually write plugin data to file
    def writeFooter(self):
        # Could also mean that plugin is already exported
        if not self.pluginID and not self.pluginName:
            return
        # No attributes are collected for write
        if not self.pluginAttrs:
            return

        p = "\n%s %s {" % (self.pluginID, PluginUtils.PluginName(self.pluginName))
        for attrName in sorted(self.pluginAttrs.keys()):
            p += "\n\t%s=%s;" % (attrName, self.pluginAttrs[attrName])
        p += "\n}\n"

        self.output.write(p)

        # Reset current plugin
        self.pluginType  = None
        self.pluginID    = None
        self.pluginName  = None
        self.pluginAttrs = None

    # Writes arbitary data to file
    def write(self, pluginType, data):
        self.output.write(data)

    def isPreviewRender(self):
        return False

    def done(self):
        if self.output and not self.output.closed:
            self.output.close()

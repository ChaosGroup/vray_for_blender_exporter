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

import mathutils

import time
import datetime
import os
import sys

from vb30       import utils
from vb30.debug import Debug

from .            import utils as LibUtils
from .VRayProcess import VRayProcess


PluginTypeToFile = {
    'MAIN'          : 'scene',
    'RENDERCHANNEL' : 'scene',
    'SETTINGS'      : 'scene',
    'OBJECT'        : 'nodes',
    'GEOMETRY'      : 'geometry',
    'CAMERA'        : 'camera',
    'LIGHT'         : 'lights',
    'TEXTURE'       : 'textures',
    'UVWGEN'        : 'textures',
    'BRDF'          : 'materials',
    'MATERIAL'      : 'materials',
    'EFFECT'        : 'environment',
    'WORLD'         : 'environment',
}


class VRayPluginExporter:
    # Export directory
    exportDir = None

    # *.vrscene files dict
    files = None

    # Filename prefix
    baseName = None

    # Whether to use unique prefix
    useBaseName = None

    # Write particular plugin types to the correspondent file
    separateFiles = None

    # If to overwrite geometry
    overwriteGeometry = None
    drSettings = None

    # Currently processed plugin
    pluginType  = None
    pluginID    = None
    pluginName  = None
    pluginAttrs = None

    # V-Ray Standalone process
    autorun = None
    process = None

    # Param cache
    # Used to send only changed attributes
    #
    pluginCache = None
    namesCache  = None

    # Export properties for animation
    #
    # This option could be set not for real animation, but
    # also for features like "Still Motion Blur" or "Camera Loop"
    #
    isAnimation = None
    frameNumber = None
    frameStep   = None


    def __init__(self):
        self.baseName = "scene"
        self.useBaseName = False
        self.separateFiles = False
        self.overwriteGeometry = True

        self.autorun = True
        self.process = VRayProcess()

        self.pluginCache = dict()
        self.namesCache  = set()


    ######## #### ##       ########  ######  
    ##        ##  ##       ##       ##    ## 
    ##        ##  ##       ##       ##       
    ######    ##  ##       ######    ######  
    ##        ##  ##       ##             ## 
    ##        ##  ##       ##       ##    ## 
    ##       #### ######## ########  ######  

    def initFiles(self, exportDir=None, baseName=None, separateFiles=True, overwriteGeometry=True, drSettings=None):
        self.exportDir = exportDir
        self.baseName = baseName if self.useBaseName else "scene"
        self.separateFiles = separateFiles
        self.overwriteGeometry = overwriteGeometry
        self.drSettings = drSettings

        self.files = {}

        if not self.separateFiles:
            filename = "%s.vrscene" % self.baseName
            filepath = os.path.join(self.exportDir, filename)

            try:
                self.files['scene'] = open(filepath, 'w')
            except IOError:
                Debug("File is busy! Looks like V-Ray is still running!", msgType='ERROR')
                return 1
        
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

                try:
                    self.files[fileType] = open(filepath, fmode)
                except IOError:
                    Debug("File is busy! Looks like V-Ray is still running!", msgType='ERROR')
                    return 1

        for fileType in self.files:
            if fileType == 'geometry' and not self.overwriteGeometry:
                continue
            self.files[fileType].write("// V-Ray For Blender\n")
            self.files[fileType].write("// %s\n" % datetime.datetime.now().strftime("%A, %d %B %Y %H:%M"))


    def writeIncludes(self):
        if self.files is None:
            return

        mainFile = self.files['scene']

        if self.separateFiles:
            for fileType in self.files:
                if fileType == 'scene':
                    continue
                f = self.files[fileType]
                mainFile.write('\n#include "%s"' % os.path.basename(f.name))
            mainFile.write('\n')


    def closeFiles(self):
        # Could be if exporter wasn't used
        if self.files is None:
            return

        self.writeIncludes()

        for fileType in self.files:
            self.files[fileType].close()


    def getFileByType(self, pluginType):
        fileType = PluginTypeToFile[pluginType]
        return self.files[fileType]


    def getOutputFile(self):
        if not self.separateFiles:
            return self.files['scene']
        if not self.pluginType:
            Debug("Plugin type is not specified!", msgType='ERROR')
            return self.files['scene']
        return self.getFileByType(self.pluginType)


    ######## ##     ## ########   #######  ########  ######## 
    ##        ##   ##  ##     ## ##     ## ##     ##    ##    
    ##         ## ##   ##     ## ##     ## ##     ##    ##    
    ######      ###    ########  ##     ## ########     ##    
    ##         ## ##   ##        ##     ## ##   ##      ##    
    ##        ##   ##  ##        ##     ## ##    ##     ##    
    ######## ##     ## ##         #######  ##     ##    ##    

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
            print(self.pluginName, attrName, " not self.isAnimation")
            
            self.pluginAttrs[attrName] = LibUtils.FormatValue(val)

        # If it's an animation we should check the cache and export
        # new value or ever create a keyframe
        #
        else:
            print(self.pluginName, attrName, " not self.isAnimation")

            newValue = LibUtils.FormatValue(val)
            cFrame, cValue = self._getCachedValue(attrName)

            attrValue = None

            if cValue is None:
                attrValue  = "interpolate((%i,%s))" % (self.frameNumber, newValue)
            else:
                if newValue == cValue:
                    print(self.pluginName, attrName, "SAME_VALUE")
                    # New value is the same no need to export
                    return
                else:
                    prevFrame = self.frameNumber - self.frameStep

                    # Cached value is more then frame step back -
                    # need a keyframe
                    if cFrame < prevFrame:
                        print(self.pluginName, attrName, "NEW_VALUE_KEYFRAME")

                        attrValue  = "interpolate("
                        attrValue += "(%i,%s)," % (prevFrame,        cValue)
                        attrValue += "(%i,%s)"  % (self.frameNumber, newValue)
                        attrValue += ")"

                    # Cached value is from previous frame -
                    # simply new frame data
                    else:
                        print(self.pluginName, attrName, "NEW_VALUE")
                        attrValue  = "interpolate((%i,%s))" % (self.frameNumber, newValue)

            # Store in cache
            self._storeValueInCache(attrName, newValue)

            # Store value for writing
            self.pluginAttrs[attrName] = attrValue


    # This will actually write plugin data to file
    #
    def writeFooter(self):
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

        self.getOutputFile().write(p)

        # Reset current plugin
        self.pluginType  = None
        self.pluginID    = None
        self.pluginName  = None
        self.pluginAttrs = None


    # Writes arbitary data to file
    #
    def write(self, pluginType, data):
        self.getFileByType(pluginType).write(data)

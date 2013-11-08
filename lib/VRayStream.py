#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

# Wrapper for files and socket communication
import mathutils

import datetime
import os
import sys

from vb25.debug import Debug
from vb25       import utils

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
    'EFFECT'        : 'evnironment',
    'WORLD'         : 'evnironment',
}


class VRayExporter():
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
    pluginType = None
    pluginID   = None
    pluginName = None

    # Work mode: 'VRSCENE', 'SOCKET', 'NETWORK'
    mode = None
    animation = False
    frame = None

    # V-Ray Standalone process
    autorun = None
    process = None

    paramCache = None

    def __init__(self):
        self.baseName = "scene"
        self.useBaseName = False
        self.separateFiles = False
        self.overwriteGeometry = True

        self.mode = 'VRSCENE'
        self.animation = False
        self.frame = 1.0

        self.autorun = True
        self.process = VRayProcess

        self.paramCache = {}

    def __del__(self):
        self.closeFiles()

        if self.process is not None:
            self.process.kill()

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

        self.files = dict()

        if self.mode in {'VRSCENE'}:
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

                    if fileType == 'geometry' and not self.overwriteGeometry:
                        continue

                    self.files[fileType] = open(filepath, 'w')

            for fileType in self.files:
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


    ######## ##     ## ########   #######  ########  ######## 
    ##        ##   ##  ##     ## ##     ## ##     ##    ##    
    ##         ## ##   ##     ## ##     ## ##     ##    ##    
    ######      ###    ########  ##     ## ########     ##    
    ##         ## ##   ##        ##     ## ##   ##      ##    
    ##        ##   ##  ##        ##     ## ##    ##     ##    
    ######## ##     ## ##         #######  ##     ##    ##    

    def set(self, pluginType, pluginID, pluginName):
        self.pluginType = pluginType
        self.pluginID   = pluginID
        self.pluginName = pluginName

    def writeHeader(self):
        if self.mode not in {'VRSCENE'}:
            return
        o = self.getOutputFile()
        o.write("\n%s %s {" % (self.pluginID, self.pluginName))

    def writeFooter(self):
        if self.mode not in {'VRSCENE'}:
            return
        output = self.getOutputFile()
        output.write("\n}\n")

    def getCacheValue(self, pluginName, attribute):
        if pluginName not in self.paramCache:
            return None
        if attribute not in self.paramCache[pluginName]:
            return None
        return self.paramCache[pluginName][attribute]

    def setCacheValue(self, pluginName, attribute, value):
        if pluginName not in self.paramCache:
            self.paramCache[pluginName] = {}
        self.paramCache[pluginName][attribute] = value

    def isCachedValue(self, pluginName, attribute, value):
        if value == self.getCacheValue(pluginName, attribute):
            return True
        return False

    def sendAttribute(self, pluginName, attibute, cValue, value):
        if not self.isCachedValue(pluginName, attibute, cValue):
            # Update cache
            self.setCacheValue(pluginName, attibute, cValue)
            # Send value
            self.process.socket.send("set %s.%s=%s" % (pluginName, attibute, value))

    def writeAttibute(self, attibute, value):
        """
        Writes data to a respective file or sends over socket
        """
        formatValue = None
        if self.animation:
            formatValue = LibUtils.AnimValue(self.frame, value)
        else:
            formatValue = LibUtils.FormatValue(value)
        valueToCache = LibUtils.FormatValue(value)

        if self.mode in {'SOCKET', 'NETWORK'}:
            self.sendAttribute(self.pluginName, attibute, valueToCache, formatValue)
        else:
            o = self.getOutputFile()
            o.write("\n\t%s=%s;" % (attibute, formatValue))

            # Store param cache for RT
            if self.pluginName not in self.paramCache:
                self.paramCache[self.pluginName] = {}
            self.paramCache[self.pluginName][attibute] = valueToCache

    def write(self, pluginType, data):
        """
        Writes arbitary data to file
        """
        if self.mode not in {'VRSCENE'}:
            return
        o = self.getFileByType(pluginType)
        o.write(data)


     ######   #######  ##     ## ##     ##    ###    ##    ## ########   ######  
    ##    ## ##     ## ###   ### ###   ###   ## ##   ###   ## ##     ## ##    ## 
    ##       ##     ## #### #### #### ####  ##   ##  ####  ## ##     ## ##       
    ##       ##     ## ## ### ## ## ### ## ##     ## ## ## ## ##     ##  ######  
    ##       ##     ## ##     ## ##     ## ######### ##  #### ##     ##       ## 
    ##    ## ##     ## ##     ## ##     ## ##     ## ##   ### ##     ## ##    ## 
     ######   #######  ##     ## ##     ## ##     ## ##    ## ########   ######  

    # Load / reload scene from file
    def load(self, filepath=None):
        print("VRayExporter::load")
        if self.process.mode in {'NORMAL'}:
            return
        self.process.load_scene()

    def commit(self):
        print("VRayExporter::commit")

        self.process.render()

    def getFileByType(self, pluginType):
        fileType = PluginTypeToFile[pluginType]
        return self.files[fileType]

    def getOutputFile(self):
        if self.mode not in {'VRSCENE'}:
            return None
        if not self.separateFiles:
            return self.files['scene']
        if not self.pluginType:
            Debug("Plugin type is not specified!", msgType='ERROR')
            return self.files['scene']
        return self.getFileByType(self.pluginType)

    def getSceneFilepath(self):
        sceneFile = self.getFileByType('MAIN')
        return sceneFile.name


     ######  ######## ######## ##     ## ########  
    ##    ## ##          ##    ##     ## ##     ## 
    ##       ##          ##    ##     ## ##     ## 
     ######  ######      ##    ##     ## ########  
          ## ##          ##    ##     ## ##        
    ##    ## ##          ##    ##     ## ##        
     ######  ########    ##     #######  ##        

    def setMode(self, mode):
        print("VRayExporter::setMode")
        self.mode = mode

    def setProcessMode(self, mode='NORMAL'):
        self.process.setMode(mode)


    ########  ########   #######   ######  ########  ######   ######  
    ##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ## 
    ##     ## ##     ## ##     ## ##       ##       ##       ##       
    ########  ########  ##     ## ##       ######    ######   ######  
    ##        ##   ##   ##     ## ##       ##             ##       ## 
    ##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ## 
    ##        ##     ##  #######   ######  ########  ######   ######  

    def initProcess(self, vrayExe):
        print("VRayExporter::initProcess")

        self.process.init(vrayExe)

    def startProcess(self):
        print("VRayExporter::startProcess")

        self.process.setSceneFile(self.getSceneFilepath())
        self.process.run()

    def stopProcess(self):
        print("VRayExporter::stopProcess")

        self.process.kill()

    def getPixels(self, bufSize):
        return self.process.recieve_raw_image(bufSize)


VRayStream = VRayExporter()

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

import os
import sys

from .VRaySocket import VRaySocket
from vb25.debug import Debug


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


class VRayStream:
    # Paths
    exportDir = None

    # Filename prefix
    baseName = None

    # Destination
    files = None
    socket = None

    # Write particular plugin types to correspondent files  
    separateFiles = None

    # If overwrite geometry (used for manual mesh export)
    overwriteGeometry = None
    drSettings = None

    # Currently processes plugin
    pluginType = None
    pluginID   = None
    pluginName = None

    # Work mode: 'VRSCENE', 'SOCKET', 'NETWORK'
    mode = None

    def __init__(self):
        pass

    def __del__(self):
        self.close()

    def init(self, mode=None, exportDir=None, baseName=None, separateFiles=True, overwriteGeometry=True, drSettings=None):
        self.mode = mode
        self.exportDir = exportDir
        self.baseName = baseName
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

        elif self.mode in {'SOCKET'}:
            self.socket = VRaySocket()

    def set(self, pluginType, pluginID, pluginName):
        self.pluginType = pluginType
        self.pluginID   = pluginID
        self.pluginName = pluginName

        if self.mode in {'SOCKET', 'NETWORK'}:
            self.socket.connect()

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

    # Write data to a respective file or transfer data
    def writeAttibute(self, attibute, value):
        if self.mode in {'SOCKET', 'NETWORK'}:
            self.socket.send("set %s.%s=%s" % (self.pluginName, attibute, value))
        else:
            o = self.getOutputFile()
            o.write("\n\t%s=%s;" % (attibute, value))

    # Write arbitary data
    def write(self, fileType, data):
        if self.mode not in {'VRSCENE'}:
            return
        if not fileType in self.files:
            return
        o = self.files[fileType]
        o.write(data)

    def commit(self):
        if self.mode not in {'SOCKET', 'NETWORK'}:
            return
        self.socket.send("render")
        self.socket.disconnect()

    # Will close files and write "includes" to the main scene file
    def close(self):
        if self.mode in {'SOCKET', 'NETWORK'}:
            self.commit()
        else:
            mainFile = self.files['scene']

            if self.separateFiles:
                for fileType in self.files:
                    f = self.files[fileType]
                    mainFile.write('\n#include "%s"' % os.path.basename(f.name))
                mainFile.write('\n')

            for fileType in self.files:
                self.files[fileType].close()

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

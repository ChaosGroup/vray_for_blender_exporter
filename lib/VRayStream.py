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

from . import VRaySocket


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

    # Dict with the opened files
    files = None

    # Write particular plugin types to correspondent files  
    useSeparateFiles = None

    # Don't overwrite geometry (used for manual mesh export)
    dontOverwriteGeometry = None

    # Currently processes plugin
    pluginType = None
    pluginName = None

    # Work mode: 'VRSCENE', 'SOCKET', 'NETWORK'
    mode = None

    def __init__(self, workMode='VRSCENE'):
        self.init(workMode)

    def __del__(self):
        self.close()

    def init(self, workMode=None, exportDir=None, baseName=None, separateFiles=True, overwriteGeometry=True):
        self.mode = workMode

    def set(self, pluginType, pluginName):
        self.pluginType = pluginType
        self.pluginName = pluginName

    def writeHeader(self, pluginInstanceName):
        if self.mode not in {'VRSCENE'}:
            return
        output = self.getOutputFile()
        output.write("\n%s %s {" % (self.pluginName, pluginInstanceName))

    def writeFooter(self):
        if self.mode not in {'VRSCENE'}:
            return
        output = self.getOutputFile()
        output.write("\n}\n")

    # Write data to a respective file or transfer data
    #
    def write(self, pluginModule, datablock, mappedParams):
        pass

    # Will close files and write "includes" to the main scene file
    def close(self):
        pass

    def getOutputFile(self):        
        if self.mode not in {'VRSCENE'}:
            return None
        if not self.useSeparateFiles:
            return self.files['SETTINGS']
        if not self.pluginType:
            Debug("Plugin type is not specified!", msgType='ERROR')
            return self.files['SETTINGS']
        return self.files[self.pluginType]

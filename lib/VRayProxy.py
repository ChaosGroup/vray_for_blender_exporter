#
# V-Ray/Blender
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

import struct
import os
import sys
import zlib

# Debug stuff
#
USE_DEBUG = False

# Colored output
#
COLOR_RED     = "\033[0;31m"
COLOR_GREEN   = "\033[0;32m"
COLOR_YELLOW  = "\033[0;33m"
COLOR_BLUE    = "\033[0;34m"
COLOR_MAGENTA = "\033[0;35m"
COLOR_DEFAULT = "\033[0m"

# VRayProxy constants
#
MVF_GEOMETRY_VOXEL = 1
MVF_PREVIEW_VOXEL  = 2

VoxelFlags = {
    MVF_GEOMETRY_VOXEL : 'MVF_GEOMETRY_VOXEL',
    MVF_PREVIEW_VOXEL  : 'MVF_PREVIEW_VOXEL',
}

#
# CHANNELS
#
VERT_GEOM_CHANNEL        = 0
FACE_TOPO_CHANNEL        = 1
VOXEL_INFO_CHANNEL       = 3
VERT_NORMAL_CHANNEL      = 4
VERT_NORMAL_TOPO_CHANNEL = 5
FACE_INFO_CHANNEL        = 6
VERT_VELOCITY_CHANNEL    = 7
MAYA_INFO_CHANNEL        = 8
POINTCLOUD_INFO_CHANNEL  = 10
POINTCLOUD_GEOM_CHANNEL  = 100
VERT_TEX_CHANNEL0        = 1000
VERT_TEX_TOPO_CHANNEL0   = 2000

ChannelID = {
    VERT_GEOM_CHANNEL        : 'VERT_GEOM_CHANNEL',
    FACE_TOPO_CHANNEL        : 'FACE_TOPO_CHANNEL',
    VOXEL_INFO_CHANNEL       : 'VOXEL_INFO_CHANNEL',
    VERT_NORMAL_CHANNEL      : 'VERT_NORMAL_CHANNEL',
    VERT_NORMAL_TOPO_CHANNEL : 'VERT_NORMAL_TOPO_CHANNEL',
    FACE_INFO_CHANNEL        : 'FACE_INFO_CHANNEL',
    VERT_VELOCITY_CHANNEL    : 'VERT_VELOCITY_CHANNEL',
    MAYA_INFO_CHANNEL        : 'MAYA_INFO_CHANNEL',
    POINTCLOUD_INFO_CHANNEL  : 'POINTCLOUD_INFO_CHANNEL',
    POINTCLOUD_GEOM_CHANNEL  : 'POINTCLOUD_GEOM_CHANNEL',
    VERT_TEX_CHANNEL0        : 'VERT_TEX_CHANNEL0',
    VERT_TEX_TOPO_CHANNEL0   : 'VERT_TEX_TOPO_CHANNEL0',
}


MF_VERT_CHANNEL            =  1
MF_TOPO_CHANNEL            =  2
MF_INFO_CHANNEL            =  4
MF_FACE_CHANNEL            =  8
MF_COMPRESSED              = 16
MF_MAYA_INFO_CHANNEL       = 32
MF_POINTCLOUD_CHANNEL      = 64
MF_POINTCLOUD_INFO_CHANNEL = 28

ChannelFlags = {
    MF_VERT_CHANNEL            : 'MF_VERT_CHANNEL',
    MF_TOPO_CHANNEL            : 'MF_TOPO_CHANNEL',
    MF_INFO_CHANNEL            : 'MF_INFO_CHANNEL',
    MF_FACE_CHANNEL            : 'MF_FACE_CHANNEL',
    MF_COMPRESSED              : 'MF_COMPRESSED',
    MF_MAYA_INFO_CHANNEL       : 'MF_MAYA_INFO_CHANNEL',
    MF_POINTCLOUD_CHANNEL      : 'MF_POINTCLOUD_CHANNEL',
    MF_POINTCLOUD_INFO_CHANNEL : 'MF_POINTCLOUD_INFO_CHANNEL',
}



class MeshFileReader(object):
    meshFile = None

    def report(self, *args):
        if USE_DEBUG:
            print(args)

    def binRead(self, format, length):
        rawData = self.meshFile.read(length)
        data    = struct.unpack(format, rawData)
        return data



class VoxelChannel(MeshFileReader):
    elementSize  = None
    numElements  = None
    channelID    = None
    depChannelID = None
    flags        = None

    data         = None

    def __init__(self, meshFile):
        self.meshFile = meshFile

    def loadInfo(self):
        self.elementSize  = self.binRead("I", 4)[0]
        self.numElements  = self.binRead("I", 4)[0]
        self.channelID    = self.binRead("H", 2)[0]
        self.depChannelID = self.binRead("H", 2)[0]
        self.flags        = self.binRead("I", 4)[0]

    def printInfo(self):
        self.report("Channel")
        self.report("  elementSize  =%i" % (self.elementSize))
        self.report("  numElements  =%i" % (self.numElements))        
        self.report("  channelID    =%s" % (ChannelID[self.channelID] if self.channelID in ChannelID else str(self.channelID)))
        self.report("  depChannelID =%i" % (self.depChannelID))

        flagsList = []
        for key in sorted(ChannelFlags.keys()):
            if key & self.flags:
                flagsList.append(ChannelFlags[key])
        self.report("  flags        =%s" % (", ".join(flagsList)))

    def loadData(self):        
        self.report("Channel Data")

        elementsSize = self.elementSize * self.numElements

        dataSize = elementsSize
        if self.flags & MF_COMPRESSED:
            self.report("  Data is compressed")
            dataSize = self.binRead("I", 4)[0]

        self.report("  Data size =%i" % (dataSize))

        # Load only channels we need
        if self.channelID in [VERT_GEOM_CHANNEL, FACE_TOPO_CHANNEL]:
            channelRawData = self.meshFile.read(dataSize)

            if self.flags & MF_COMPRESSED:
                self.data = zlib.decompressobj().decompress(channelRawData)

                # self.report("  Compressed data:", channelRawData)
                # self.report("  Uncompressed data:", self.data)
                self.report("  Expected / uncompressed size:", elementsSize, len(self.data))
            else:
                self.data = channelRawData
        else:
            self.meshFile.seek(dataSize, os.SEEK_CUR)

    def loadChechsum(self):
        self.report("Channel Checksums")

        for i in range(self.numElements):
            channelCRC  = self.binRead("I", 4)[0]

            self.report("  %i: checksum =%i" % (i, channelCRC))



class VoxelChannels(MeshFileReader):
    channels = None

    def __init__(self, meshFile):
        self.meshFile = meshFile
        self.channels = []
    
    def loadInfo(self, voxelOffset=None):
        self.channelCount = self.binRead("I", 4)[0]

        for i in range(self.channelCount):
            voxelChannel = VoxelChannel(self.meshFile)
            voxelChannel.loadInfo()

            self.channels.append(voxelChannel)

    def printInfo(self):
        self.report("Voxel")
        self.report("  Channels count =%i" % (len(self.channels)))
        
        for channel in self.channels:
            channel.printInfo()

    def loadData(self):
        for channel in self.channels:
            channel.loadData()

    def getChannelByType(self, channelType=VERT_GEOM_CHANNEL):
        for channel in self.channels:
            if channel.channelID == channelType:
                return channel
        return None

    def getFaceTopoChannel(self):
        return self.getChannelByType(FACE_TOPO_CHANNEL)
    
    def getVertGeomChannel(self):
        return self.getChannelByType(VERT_GEOM_CHANNEL)



class MeshVoxel(MeshFileReader):
    fileOffset = None
    bbox       = None
    flags      = None

    channels = None

    def __init__(self, meshFile):
        self.meshFile = meshFile
        self.channels = VoxelChannels(self.meshFile)

    def loadInfo(self):
        self.fileOffset = self.binRead("Q", 8)[0]
        self.bbox       = self.binRead("6f", 24)
        self.flags      = self.binRead("I", 4)[0]

    def printInfo(self):
        self.report("Voxel")
        self.report("  fileOffset =%i" % (self.fileOffset))
        self.report("  bbox       =%s" % ("%.2f,%.2f,%.2f; %.2f,%.2f,%.2f" % (self.bbox)))
        self.report("  flags      =%s" % (VoxelFlags[self.flags]))

    def loadData(self):
        self.meshFile.seek(self.fileOffset)

        self.channels.loadInfo()
        self.channels.printInfo()
        self.channels.loadData()

    def chunk(self, input, size):
        return tuple(zip(*([iter(input)]*size)))

    def getFaces(self):
        faceTopoChannel = self.channels.getFaceTopoChannel()        
        
        if faceTopoChannel is None:
            return ()
        
        intArray   = struct.unpack("%ii"%(len(faceTopoChannel.data) / 4), faceTopoChannel.data)
        facesArray = self.chunk(intArray, 3)
        
        return facesArray

    def getVertices(self):
        vertexChannel = self.channels.getVertGeomChannel()
        
        if vertexChannel is None:
            return ()

        floatArray  = struct.unpack("%if"%(len(vertexChannel.data) / 4), vertexChannel.data)
        vertexArray = self.chunk(floatArray, 3)
        
        return vertexArray



class MeshFile(MeshFileReader):
    meshFilepath = None

    vrayID       = None
    fileVersion  = None
    lookupOffset = None

    voxels    = None
    numVoxels = None

    def __init__(self, filepath):
        self.meshFilepath = os.path.expanduser(filepath)
        self.meshFile     = open(self.meshFilepath, "rb")

        self.voxels = []

    def __del__(self):
        if self.meshFile is None:
            return
        self.meshFile.close()
    
    def readFile(self):
        self.vrayID = self.binRead("7s", 7)[0][:-1]
        
        if self.vrayID == b'vrmesh':
            self.fileVersion = self.binRead("I", 4)[0]
        else:
            # Old format
            self.meshFile.seek(0)
            self.vrayID = self.binRead("4s", 4)[0][:-1]
            self.fileVersion = 0

        self.lookupOffset = self.binRead("Q", 8)[0]

        self.report("MeshFile:", self.meshFilepath)
        self.report("  fileID       =%s" % (self.vrayID))
        self.report("  fileVersion  = 0x%X" % (self.fileVersion))
        self.report("  lookupOffset =%i" % (self.lookupOffset))
        
        self.meshFile.seek(self.lookupOffset)
        self.numVoxels = self.binRead("I", 4)[0]

        self.report("  numVoxels    =%i" % (self.numVoxels))
        self.report("")

        for i in range(self.numVoxels):
            voxel = MeshVoxel(self.meshFile)
            voxel.loadInfo()
            voxel.printInfo()

            self.voxels.append(voxel)

        for voxel in self.voxels:
            voxel.loadData()

        return None

    def getVoxelByType(self, voxelType=MVF_PREVIEW_VOXEL):
        for voxel in self.voxels:
            if voxel.flags == voxelType:
                return voxel
        return None


def main():
    testFile = "~/devel/vrayblender/test-suite/armadillo.vrmesh"

    meshFile = MeshFile(testFile)
    result = meshFile.readFile()
    
    if result is not None:
        self.report("Error parsing file:", testFile)
        sys.exit(1)

    previewVoxel = meshFile.getVoxelByType(MVF_PREVIEW_VOXEL)

    faces = previewVoxel.getFaces()
    vertices = previewVoxel.getVertices()

    print("Vertices:", vertices)
    print("Faces:", faces)


if __name__ == '__main__':
    main()

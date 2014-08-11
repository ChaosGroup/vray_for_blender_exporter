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

import _vray_for_blender

import bpy


def InitAnimation(bus, isAnimation=False):
    o = bus['output']

    _vray_for_blender.initAnimation(
        isAnimation,
        o.frameStart,
        o.frameStep
    )


def InitExporter(bus):
    scene  = bus['scene']
    engine = bus['engine']
    o      = bus['output']

    VRayScene = scene.vray
    VRayDR    = VRayScene.VRayDR

    drSharePath = ""
    if VRayDR.on:
        if VRayDR.assetSharing == 'SHARE':
            drSharePath = bpy.path.abspath(VRayDR.shared_dir)

    exporter = _vray_for_blender.init(
        engine  = engine.as_pointer(),
        context = bpy.context.as_pointer(),
        scene   = scene.as_pointer(),
        data    = bpy.data.as_pointer(),

        mainFile     = o.fileManager.getFileByPluginType('MAIN'),
        objectFile   = o.fileManager.getFileByPluginType('OBJECT'),
        envFile      = o.fileManager.getFileByPluginType('WORLD'),
        geometryFile = o.fileManager.getFileByPluginType('GEOMETRY'),
        lightsFile   = o.fileManager.getFileByPluginType('LIGHT'),
        materialFile = o.fileManager.getFileByPluginType('MATERIAL'),
        textureFile  = o.fileManager.getFileByPluginType('TEXTURE'),

        drSharePath = drSharePath,
    )

    return exporter


def ShutdownExporter(bus):
    _vray_for_blender.clearFrames()

    if 'exporter' in bus:
        _vray_for_blender.exit(bus['exporter'])
        del bus['exporter']

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

import math
import os
import string
import socket
import sys
import tempfile
import time

import bpy
import mathutils

from bpy.app.handlers import persistent

from vb25         import process, utils, render
from vb25.lib     import VRayProcess, VRaySocket
from vb25.lib     import utils as LibUtils
from vb25.debug   import Debug
from vb25.plugins import PLUGINS
from vb25.process import is_running
from vb25.nodes   import export as NodeExport


# Objects count
# Used to detect if object was added or removed
# and call full scene reload
OB_COUNT = 0

# Scene file path
SCE_FILE = ""


@persistent
def scene_update_post(scene):
    global OB_COUNT
    global SCE_FILE

    if not (bpy.data.groups.is_updated or
            bpy.data.node_groups.is_updated or
            bpy.data.objects.is_updated or
            bpy.data.scenes.is_updated or
            bpy.data.actions.is_updated):
        return

    if not scene.render.engine == 'VRAY_RENDER_RT':
        return

    if not scene.vray.RTEngine.interactive:
        return

    Debug("scene_update_post()", msgType='ERROR')

    bus = {}
    bus['mode'] = 'SOCKET'
    bus['volumes'] = set()
    bus['context'] = {}
    bus['cache'] = {
        'plugins' : set(),
        'mesh'    : set(),
        'nodes'   : set(),
    }

    tag_reload = False
    ob_count   = len(bpy.data.objects)

    if OB_COUNT != ob_count:
        OB_COUNT   = ob_count
        tag_reload = True

    if tag_reload and SCE_FILE:
        Debug("Reloading scene from *.vrscene files...", msgType='INFO')
        export_scene(scene, 'VRAY_UPDATE_CALL')
        process.reload_scene(SCE_FILE)
        return

    if bpy.data.node_groups.is_updated:
        for ntree in bpy.data.node_groups:
            if not ntree.is_updated or not ntree.is_updated_data:
                continue

            if ntree.bl_idname in {'VRayNodeTreeMaterial'}:
                NodeExport.WriteVRayMaterialNodeTree(bus, ntree)

    if bpy.data.objects.is_updated:
        cmd_socket = VRaySocket()

        for ob in bpy.data.objects:
            if ob.type in {'EMPTY'}:
                continue

            if ob.is_updated or ob.data.is_updated:
                if ob.type == 'CAMERA':
                    VRayCamera     = ob.data.vray
                    CameraPhysical = VRayCamera.CameraPhysical

                    if CameraPhysical.use:
                        cmd_socket.send("set PhysicalCamera.ISO=%.3f" % CameraPhysical.ISO)
                        cmd_socket.send("set PhysicalCamera.fov=%.3f" % ob.data.angle)

                    cmd_socket.send("set CameraView.use_scene_offset=0")
                    cmd_socket.send("set CameraView.fov=%.3f" % ob.data.angle)
                    cmd_socket.send("set CameraView.transform=%s" % (utils.transform(ob.matrix_world).replace(" ","").replace("\n","").replace("\t","")))

            if ob.is_updated:
                cmd_socket.send("set %s.transform=%s" % (LibUtils.GetObjectName(ob), utils.transform(ob.matrix_world).replace(" ","").replace("\n","").replace("\t","")))

        cmd_socket.send("render")
        cmd_socket.disconnect()


def register():
    bpy.app.handlers.scene_update_post.append(scene_update_post)


def unregister():
    bpy.app.handlers.scene_update_post.remove(scene_update_post)

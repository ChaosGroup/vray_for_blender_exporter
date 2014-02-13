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

from bpy.app.handlers import persistent

from vb30.plugins import PLUGINS_ID

from vb30.nodes import export as NodeExport
from vb30.debug import Debug

from vb30.lib.VRayStream import VRayStream
from vb30.lib import utils as LibUtils
from vb30.lib import ExportUtils

from vb30 import utils
from vb30 import export


def HashNodeTreeLinks(ntree):
    addrSum = 0
    for l in ntree.links:
        addrSum += l.from_socket.as_pointer()
        addrSum += l.to_socket.as_pointer()
    return addrSum


def IsNtreeLinksUpdated(ntree, update=True):
    cacheLinks = VRayStream.ntreeCache.get(ntree.name, 0)
    newLinks   = HashNodeTreeLinks(ntree)
    if cacheLinks != newLinks:
        if update:
            VRayStream.ntreeCache[ntree.name] = newLinks
        return True
    return False


def AreNtreesLinksUpdated():
    # NOTE: Disable this by now...
    return False

    for ntree in bpy.data.node_groups:
        if IsNtreeLinksUpdated(ntree, update=False):
            return True
    return False


def GetBus():
    scene = bpy.context.scene

    return {
        # Data exporter
        # Refactor this if needed
        'output' : VRayStream,

        # We always need to access scene data
        'scene' : scene,

        # Current frame
        'frame' : scene.frame_current,

        # Active camera
        'camera' : scene.camera,

        # We will override some params in case of preview
        'preview' : False,

        # Set of environment effects objects
        'volumes' : set(),

        # Set of fog gizmos, to exclude from 'Node' creation
        'gizmos' : set(),

        # Prevents export data duplication
        'cache' : {
            'plugins' : set(),
            'mesh'    : set(),
            'nodes'   : set(),
        },

        # We need to know render engine type
        'engine' : 'VRAY_RENDER_RT',

        # Some storage
        'context' : {},

        # Fail safe defaults
        'defaults' : {
            'brdf' : "BRDFNOBRDFISSET",
            'material' : "MANOMATERIALISSET",
            'texture' : "TENOTEXTUREIESSET",
            'uvwgen' : "DEFAULTUVWC",
            'blend' : "TEDefaultBlend",
        }
    }


@persistent
def rt_scene_update_post(scene, context=None, is_viewport=True):
    if not scene.render.engine == 'VRAY_RENDER_RT':
        return

    if not VRayStream.process.is_running():
        return

    nodeGroupsUpdated = (bpy.data.node_groups.is_updated or AreNtreesLinksUpdated())

    if not (nodeGroupsUpdated or bpy.data.scenes.is_updated):
        return

    Debug("rt_scene_update_post()")

    VRayStream.setMode('SOCKET')

    bus = GetBus()

    bus.update({
        'bContext' : context,
        'is_viewport' : is_viewport,
    })

    VRayScene = scene.vray

    if nodeGroupsUpdated:
        for ntree in bpy.data.node_groups:
            if ntree.is_updated or IsNtreeLinksUpdated(ntree, True):
                if ntree.bl_idname in {'VRayNodeTreeMaterial'}:
                    NodeExport.WriteVRayMaterialNodeTree(bus, ntree)

        VRayStream.commit()

    if bpy.data.scenes.is_updated:
        for pluginName in {'SettingsRTEngine'}:
            pluginModule = PLUGINS_ID[pluginName]
            propGroup = getattr(VRayScene, pluginName)

            overrideParams = {}

            ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

        PLUGINS_ID['SettingsEnvironment'].write(bus)

        VRayStream.commit()


@persistent
def rt_object_update(ob):
    if not VRayStream.process.is_running():
        return

    Debug("rt_object_update(%s)" % ob.name)

    VRayStream.setMode('SOCKET')

    scene = bpy.context.scene

    bus = GetBus()

    bus.update({
        'node' : {
            'object' : ob,
            'visible' : ob,
            'base' : ob,
            'dupli' : {},
            'particle' : {},
        },
    })

    if ob.type == 'EMPTY':
        pass
    elif ob.type == 'CAMERA':
        VRayCamera = ob.data.vray

        for pluginName in {'RenderView'}:
            pluginModule = PLUGINS_ID[pluginName]
            propGroup = getattr(VRayCamera, pluginName)

            overrideParams = {}

            ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)
    else:
        pluginName = LibUtils.GetObjectName(ob)

        VRayStream.set('OBJECT', 'Node', pluginName)
        VRayStream.writeAttibute('transform', LibUtils.FormatValue(ob.matrix_world))

    VRayStream.commit()


@persistent
def rt_object_data_update(ob):
    if not VRayStream.process.is_running():
        return

    # TODO: update new mesh using 'append'
    #
    # if ob.type in GEOMETRY_TYPES:

    if ob.type not in {'LAMP', 'CAMERA'}:
        return

    Debug("rt_object_data_update(%s)" % ob.name)

    VRayStream.setMode('SOCKET')

    bus = GetBus()

    bus.update({
        'node' : {
            'object' : ob,
            'visible' : ob,
            'base' : ob,
            'dupli' : {},
            'particle' : {},
        },
    })

    if ob.type == 'LAMP':
        export.write_lamp(bus)
    elif ob.type == 'CAMERA':
        VRayCamera = ob.data.vray

        for pluginName in {'RenderView', 'SettingsCamera', 'CameraPhysical'}:
            pluginModule = PLUGINS_ID[pluginName]
            propGroup = getattr(VRayCamera, pluginName)

            overrideParams = {}

            ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

    VRayStream.commit()


def AddRTCallbacks():
    # Transforms and general attributes
    if rt_object_update not in bpy.app.handlers.object_update:
        bpy.app.handlers.object_update.append(rt_object_update)

    # Camera, Lamp settings are stored on data level
    if rt_object_data_update not in bpy.app.handlers.object_data_update:
        bpy.app.handlers.object_data_update.append(rt_object_data_update)

    # Node trees, environment
    if rt_scene_update_post not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.append(rt_scene_update_post)


def RemoveRTCallbacks():
    if rt_object_update in bpy.app.handlers.object_update:
        bpy.app.handlers.object_update.remove(rt_object_update)

    if rt_object_data_update in bpy.app.handlers.object_data_update:
        bpy.app.handlers.object_data_update.remove(rt_object_data_update)

    if rt_scene_update_post in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.remove(rt_scene_update_post)


def register():
    pass


def unregister():
    RemoveRTCallbacks()

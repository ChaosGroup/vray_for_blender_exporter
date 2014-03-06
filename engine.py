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

import os

import bpy
import bgl
import math

import _vray_for_blender

from .lib.VRayStream import VRayStream
from .lib import ExportUtils
from .plugins import PLUGINS_ID

from . import utils
from . import export
from . import debug

from . import realtime


def Init():
    _vray_for_blender.start(os.path.join(utils.get_vray_exporter_path(), "plugins_desc"))


def Shutdown():
    _vray_for_blender.free()


def ErrorReport(engine, err):
    if not err:
        return
    if err == 1:
        engine.report({'ERROR'}, "Files are busy! Looks like V-Ray is still running!")
    else:
        engine.report({'ERROR'}, "Error: %s" % err)


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False

    err = None

    def update(self, data, scene):
        debug.Debug("VRayRenderer::update()")

        realtime.RemoveRTCallbacks()

        self.err = export.Export(data, scene, self.bl_idname)
        ErrorReport(self, self.err)

    def render(self, scene):
        debug.Debug("VRayRenderer::render()")
        
        if self.err:
            return

        export.Run(scene, self.bl_idname)


# class VRayRendererPreview(bpy.types.RenderEngine):
#     bl_idname      = 'VRAY_RENDER_PREVIEW'
#     bl_label       = "V-Ray (With Material Preview)"
#     bl_use_preview = True

#     err = None

#     def update(self, data, scene):
#         debug.Debug("VRayRendererPreview::update(is_preview=%i)" % self.is_preview)

#         realtime.RemoveRTCallbacks()

#         if self.is_preview:
#             if scene.render.resolution_x < 64:
#                 # Don't render icons
#                 return

#         self.err = export.Export(data, scene, self.bl_idname, self.is_preview)
#         ErrorReport(self, err)

#     def render(self, scene):
#         debug.Debug("VRayRendererPreview::render(is_preview=%i)" % self.is_preview)
#         if self.err:
#             return

#         if self.is_preview:
#             if scene.render.resolution_x < 64:
#                 # Don't render icons
#                 return

#         export.Run(scene, self.bl_idname)


class VRayRendererRT(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_RT'
    bl_label       = "V-Ray Realtime"
    bl_use_preview =  False

    err = None

    def viewRealtime(self, context):
        VRayStream.setMode('SOCKET')

        bus = realtime.GetBus()

        VRayScene = context.scene.vray

        fov = None
        if context.space_data.camera:
            fov = context.space_data.camera.data.angle
        else:
            fov = 2.0 * math.atan((32.0 / 2.0) / context.space_data.lens)

        tm  = context.region_data.view_matrix.inverted()

        pluginModule = PLUGINS_ID['RenderView']
        propGroup = context.scene.camera.data.vray.RenderView

        overrideParams = {
            'fov' : fov,
            'transform' : tm,
            'orthographic' : not context.region_data.is_perspective,
        }

        ExportUtils.WritePlugin(bus, pluginModule, 'RenderView', propGroup, overrideParams)

        VRayStream.commit()

    def view_update(self, context):
        print("VRayRendererRT::view_update()")
        self.viewRealtime(context)

    def view_draw(self, context):
        print("VRayRendererRT::view_draw()")
        self.viewRealtime(context)

    def update(self, data, scene):
        debug.Debug("VRayRendererRT::update()")

        self.err = export.Export(data, scene, self.bl_idname)
        ErrorReport(self, self.err)

        realtime.AddRTCallbacks()

    def render(self, scene):
        debug.Debug("VRayRendererRT::render()")

        if self.err:
            return

        export.Run(scene, self.bl_idname)


def GetRegClasses():
    return (
        VRayRenderer,
        # VRayRendererPreview,
        VRayRendererRT,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

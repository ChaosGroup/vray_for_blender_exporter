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
from . import export_cpp
from . import debug


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

        self.err = export_cpp.Export(data, scene, self)
        ErrorReport(self, self.err)

    def render(self, scene):
        debug.Debug("VRayRenderer::render()")
        
        if self.err:
            return

        export.Run(scene, self.bl_idname)


class VRayRendererPreview(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_PREVIEW'
    bl_label       = "V-Ray (With Material Preview)"
    bl_use_preview = True

    err = None

    def update(self, data, scene):
        debug.Debug("VRayRendererPreview::update(is_preview=%i)" % self.is_preview)

        realtime.RemoveRTCallbacks()

        if self.is_preview:
            if scene.render.resolution_x < 64:
                # Don't render icons
                return

        self.err = export.Export(data, scene, self.bl_idname, self.is_preview)
        ErrorReport(self, err)

    def render(self, scene):
        debug.Debug("VRayRendererPreview::render(is_preview=%i)" % self.is_preview)
        if self.err:
            return

        if self.is_preview:
            if scene.render.resolution_x < 64:
                # Don't render icons
                return

        export.Run(scene, self.bl_idname)


def GetRegClasses():
    return (
        VRayRenderer,
        VRayRendererPreview,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

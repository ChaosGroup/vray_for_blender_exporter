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

import _vray_for_blender

from . import utils
from . import export
from . import export_cpp


def Init():
    _vray_for_blender.start(os.path.join(utils.get_vray_exporter_path(), "plugins_desc"))


def Shutdown():
    _vray_for_blender.free()


def ExportScene(engine, data, scene):
    if engine.is_preview:
        if scene.render.resolution_x < 64: # Don't render icons
            return
    engine.err = export_cpp.Export(data, scene, engine, engine.is_preview)
    if engine.err is not None:
        engine.report({'ERROR'}, engine.err)


def StartRenderer(engine, scene):
    if engine.is_preview:
        if scene.render.resolution_x < 64: # Don't render icons
            return

    if engine.err is not None:
        engine.report({'ERROR'}, engine.err)
        return

    err = export.Run(scene, engine)
    if err is not None:
        engine.report({'ERROR'}, err)

    engine.err = None


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False

    err = None

    def update(self, data, scene):
        ExportScene(self, data, scene)

    def render(self, scene):
        StartRenderer(self, scene)


class VRayRendererPreview(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_PREVIEW'
    bl_label       = "V-Ray (With Material Preview)"
    bl_use_preview = True

    err = None

    def update(self, data, scene):
        ExportScene(self, data, scene)

    def render(self, scene):
        StartRenderer(self, scene)


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

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

import bpy

from vb25 import render
from vb25 import realtime


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False

    def render(self, scene):
        err = render.render(self, scene)
        if err is not None:
            self.report({'ERROR'}, err)


class VRayRendererPreview(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_PREVIEW'
    bl_label       = "V-Ray (Material Preview)"
    bl_use_preview = True

    def render(self, scene):
        VRayScene    = scene.vray
        VRayExporter = VRayScene.exporter

        if scene.name == "preview":
            if scene.render.resolution_x < 64:
                return
            render.render(self, scene, preview=True)
        else:
            err = render.render(self, scene)

            if err is not None:
                self.report({'ERROR'}, err)


class VRayRendererRT(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_RT'
    bl_label       = "V-Ray (Realtime)"
    bl_use_preview =  False

    width  = None
    height = None

    def render(self, scene):
        realtime.export_scene(scene, self.bl_idname)


def GetRegClasses():
    return (
        VRayRenderer,
        VRayRendererPreview,
        VRayRendererRT,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

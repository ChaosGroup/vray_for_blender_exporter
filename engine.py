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
import bgl

from . import export
from . import debug

from realtime import scene_update_post


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False

    def update(self, data, scene):
        debug.Debug("VRayRenderer::update()")

        export.Export(data, scene, self.bl_idname)

    def render(self, scene):
        debug.Debug("VRayRenderer::render()")

        export.Run(scene, self.bl_idname)


class VRayRendererPreview(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_PREVIEW'
    bl_label       = "V-Ray (With Material Preview)"
    bl_use_preview = True

    def update(self, data, scene):
        debug.Debug("VRayRendererPreview::update(is_preview=%i)" % self.is_preview)

        if self.is_preview:
            if scene.render.resolution_x < 64:
                # Don't render icons
                return

        export.Export(data, scene, self.bl_idname, self.is_preview)

    def render(self, scene):
        debug.Debug("VRayRendererPreview::render(is_preview=%i)" % self.is_preview)

        if self.is_preview:
            if scene.render.resolution_x < 64:
                # Don't render icons
                return

        export.Run(scene, self.bl_idname)


class VRayRendererRT(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_RT'
    bl_label       = "V-Ray Realtime"
    bl_use_preview =  False

    def view_update(self, context):
        # debug.Debug("VRayRendererRT::view_update()", msgType='ERROR')
        # scene_update_post(context.scene, context=context, is_viewport=True)
        pass

    def view_draw(self, context):
        pass

    def update(self, data, scene):
        debug.Debug("VRayRendererRT::update()")

        # Export scene to the vrscene files
        # Realime update will be done in 'scene_update_post'
        #
        export.Export(data, scene, self.bl_idname)

    def render(self, scene):
        debug.Debug("VRayRendererRT::render()")

        export.Run(scene, self.bl_idname)


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

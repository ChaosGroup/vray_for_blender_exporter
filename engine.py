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
import sys
import subprocess

import bpy

import _vray_for_blender_rt

from vb30.lib import SysUtils
from vb30 import export


# This will hold handle to subprocess.Popen to the zmq server if
# it is started in local mode, and it should be terminated on Shutdown()
#
_zmq_process = None


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname = 'VRAY_RENDER'
    bl_label  = "V-Ray"
    bl_use_preview = False
    bl_preview_filepath = SysUtils.GetPreviewBlend()

    renderer = None

    def _debug(self, msg):
        if bpy.app.debug:
            sys.stderr.write("%s::%s\n" % (self.__class__.__name__, msg))
            sys.stderr.flush()

    def _get_settings(self):
        # In case of preview "scene" argument will point
        # to the preview scene, but we need to use settings
        # from the actual scene
        #
        return bpy.context.scene.vray.Exporter

    def _free(self):
        if self.renderer is not None:
            _vray_for_blender_rt.free(self.renderer)

        self.renderer = None

    def __init__(self):
        self._debug("__init__()")
        self._free()

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'}:
            # Start server if needed
            pass

    def __del__(self):
        self._debug("__del__()")
        self._free()

    # Production rendering
    #
    def update(self, data, scene):
        self._debug("update()")

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'}:
            # Start server if needed
            pass

        self._free()

        self.renderer = _vray_for_blender_rt.init(
            context=bpy.context.as_pointer(),
            engine=self.as_pointer(),
            data=data.as_pointer(),
            scene=scene.as_pointer(),
        )

        _vray_for_blender_rt.update(self.renderer)

    def render(self, scene):
        self._debug("render()")

        if self.is_preview:
            pass
        else:
            pass

        if self.renderer:
            _vray_for_blender_rt.render(self.renderer)

    # Interactive rendering
    #
    def view_update(self, context):
        self._debug("view_update()")

        vrayExporter = self._get_settings()

        if not self.renderer:
            self.renderer = _vray_for_blender_rt.init_rt(
                context=context.as_pointer(),
                engine=self.as_pointer(),
                data=bpy.data.as_pointer(),
                scene=bpy.context.scene.as_pointer(),
            )

        if self.renderer:
            _vray_for_blender_rt.view_update(self.renderer)

    def view_draw(self, context):
        # self._debug("view_draw()")

        if self.renderer:
            _vray_for_blender_rt.view_draw(self.renderer)


def init():
    _vray_for_blender_rt.load(os.path.join(SysUtils.GetExporterPath(), "plugins_desc"))


def shutdown():
    _vray_for_blender_rt.unload()

    if _zmq_process is not None:
        _zmq_process.terminate()


def register():
    bpy.utils.register_class(VRayRenderer)


def unregister():
    bpy.utils.unregister_class(VRayRenderer)

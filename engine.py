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

import _vray_for_blender

_has_rt = True
try:
    import _vray_for_blender_rt
except:
    _has_rt = False

from .lib import SysUtils
from .    import export


# This will hold handle to subprocess.Popen to the zmq server if
# it is started in local mode, and it should be terminated on Shutdown()
#
zmq_backend = None


def Init():
    jsonDirpath = os.path.join(SysUtils.GetExporterPath(), "plugins_desc")
    _vray_for_blender.start(jsonDirpath)
    if _has_rt:
        _vray_for_blender_rt.load(jsonDirpath)


def Shutdown():
    _vray_for_blender.free()
    if _has_rt:
        _vray_for_blender_rt.unload()

    if _has_rt and zmq_backend:
        try:
            zmq_backend.terminate()
        except:
            pass


class VRayRendererBase(bpy.types.RenderEngine):
    def render(self, scene):
        if self.is_preview:
            if scene.render.resolution_x < 64: # Don't render icons
                return

        err = export.RenderScene(self, scene)
        if err is not None:
            self.report({'ERROR'}, err)


class VRayRenderer(VRayRendererBase):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False


class VRayRendererPreview(VRayRendererBase):
    bl_idname = 'VRAY_RENDER_PREVIEW'
    bl_label  = "V-Ray (With Material Preview)"

    bl_use_preview      =  True
    bl_preview_filepath = SysUtils.GetPreviewBlend()


class VRayRendererRT(VRayRendererBase):
    bl_idname = 'VRAY_RENDER_RT'
    bl_label  = "V-Ray (With Viewport Rendering)"

    bl_use_preview      = True
    bl_preview_filepath = SysUtils.GetPreviewBlend()

    zmq_should_start = False

    exporter = None

    def debug(self, msg):
        if False:
            sys.stderr.write(msg)
            sys.stderr.write("\n")
            sys.stderr.flush()

    def __init__(self):
        self.debug("VRayRendererRT::__init__()")
        self.exporter = None

    def __del__(self):
        self.debug("VRayRendererRT::__del__()")
        self._clean_up()

    def _clean_up(self):
        if self.exporter:
            _vray_for_blender_rt.free(self.exporter)
            self.exporter = None

    def _init_zmq(self, exporter):
        global zmq_backend

        self.zmq_should_start = exporter.backend == 'ZMQ' and\
                                exporter.backend_worker == 'LOCAL'

        if self.zmq_should_start and not zmq_backend or\
            zmq_backend and zmq_backend.poll() is not None:

            executable_path = SysUtils.GetZmqPath()
            if not executable_path or not os.path.exists(executable_path):
                self.debug("Can't find V-Ray ZMQ Server!")
            else:
                port = str(exporter.zmq_port)
                zmq_backend = subprocess.Popen([executable_path, "-p", port])

    def update(self, data, scene):
        self.debug("VRayRendererRT::update()")

    def render(self, scene):
        self.debug("VRayRendererRT::render()")

        settings = scene.vray.Exporter
        self._clean_up()
        self._init_zmq(settings)

        self.exporter = _vray_for_blender_rt.create(
            False,
            settings.animation_mode == 'FULL'
        )

        _vray_for_blender_rt.init(
            self.exporter,
            0,
            self.as_pointer(),
            bpy.data.as_pointer(),
            scene.as_pointer(),
            0, 0, 0
        )

        if settings.animation_mode == 'FULL':
            frame = scene.frame_current
            start_frame = frame

            while frame <= scene.frame_end:
                scene.frame_set(frame)
                res = _vray_for_blender_rt.export(self.exporter)

                if not res or self.test_break():
                    self.report({'ERROR'}, 'Renderer interrupted!')
                    self._clean_up()
                    break

                frame += scene.frame_step

            scene.frame_set(start_frame)
        else:
            _vray_for_blender_rt.export(self.exporter)

    def view_update(self, context):
        self.debug("VRayRendererRT::view_update()")

        self._init_zmq(context.scene.vray.Exporter)

        if not self.exporter:
            self.exporter = _vray_for_blender_rt.create(True, False)
            _vray_for_blender_rt.init(
                self.exporter,
                context.as_pointer(),
                self.as_pointer(),
                context.blend_data.as_pointer(),
                context.scene.as_pointer(),
                context.region.as_pointer(),
                context.space_data.as_pointer(),
                context.region_data.as_pointer(),
            )
            _vray_for_blender_rt.export(self.exporter)
        else:
            _vray_for_blender_rt.update(self.exporter)

    def view_draw(self, context):
        self.debug("VRayRendererRT::view_draw()")
        if self.exporter:
            _vray_for_blender_rt.draw(self.exporter,
                context.space_data.as_pointer(),
                context.region_data.as_pointer()
            )


def GetRegClasses():
    reg_classes = [
        VRayRenderer,
        VRayRendererPreview,
    ]
    if _has_rt:
        reg_classes.append(VRayRendererRT)
    return reg_classes


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

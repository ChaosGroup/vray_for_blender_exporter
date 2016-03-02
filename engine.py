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

from vb30.lib.VRayStream import VRayExportFiles
from vb30.lib.VRayStream import VRayFilePaths


# This will hold handle to subprocess.Popen to the zmq server if
# it is started in local mode, and it should be terminated on Shutdown()
#
_zmq_process = None

def _debug(msg):
    import inspect
    if True:
        sys.stderr.write("Python: %s::%s\n" % (inspect.stack()[1][3], msg))
        sys.stderr.flush()

def get_file_manager(exporter, engine, scene):
    pm = VRayFilePaths()

    # Setting user defined value here
    # It could be overriden in 'initFromScene'
    # depending on VRayDR settings
    pm.setSeparateFiles(exporter.useSeparateFiles)

    pm.initFromScene(engine, scene)
    pm.printInfo()

    fm = VRayExportFiles(pm)
    fm.setOverwriteGeometry(exporter.auto_meshes)

    try:
        fm.init()
    except Exception as e:
        _debug(e)
        return "Error initing files!"

    return fm


def _check_zmq_process(port):
    global _zmq_process

    if not _zmq_process or _zmq_process and _zmq_process.poll() is not None:
        executable_path = SysUtils.GetZmqPath()

        if not executable_path or not os.path.exists(executable_path):
            _debug("Can't find V-Ray ZMQ Server!")
        else:
            if 'VRAY_ZMQSERVER_APPSDK_PATH' not in os.environ:
                _debug("VRAY_ZMQSERVER_APPSDK_PATH is not set!")
            else:
                appsdkPath = os.environ['VRAY_ZMQSERVER_APPSDK_PATH']
                os.environ['VRAY_PATH'] = os.path.dirname(appsdkPath)
                if 'LD_LIBRARY_PATH' in os.environ:
                    os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ':' + os.environ['VRAY_PATH']

                _zmq_process = subprocess.Popen([executable_path, "-p", port])


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname = 'VRAY_RENDER'
    bl_label  = "V-Ray"
    bl_use_preview = True
    bl_preview_filepath = SysUtils.GetPreviewBlend()

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
        if hasattr(self, 'renderer') and self.renderer is not None:
            _vray_for_blender_rt.free(self.renderer)
        self.renderer = None

        if hasattr(self, 'file_manager') and self.file_manager:
            self.file_manager.writeIncludes()
            self.file_manager.closeFiles()
        self.file_manager = None

    def __init__(self):
        self.renderer = None
        self.file_manager = None

        self._debug("__init__()")

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'} and vrayExporter.backend_worker == 'LOCAL':
            _check_zmq_process(str(vrayExporter.zmq_port))

    def __del__(self):
        self._debug("__del__()")
        self._free()

    # Production rendering
    #
    def update(self, data, scene):
        self._debug("update()")

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'} and vrayExporter.backend_worker == 'LOCAL':
            _check_zmq_process(str(vrayExporter.zmq_port))

        if not self.renderer:
            self.file_manager = get_file_manager(vrayExporter, self, scene)
            self.renderer = _vray_for_blender_rt.init(
                context=bpy.context.as_pointer(),
                engine=self.as_pointer(),
                data=data.as_pointer(),
                scene=scene.as_pointer(),

                mainFile     = self.file_manager.getFileByPluginType('MAIN'),
                objectFile   = self.file_manager.getFileByPluginType('OBJECT'),
                envFile      = self.file_manager.getFileByPluginType('WORLD'),
                geometryFile = self.file_manager.getFileByPluginType('GEOMETRY'),
                lightsFile   = self.file_manager.getFileByPluginType('LIGHT'),
                materialFile = self.file_manager.getFileByPluginType('MATERIAL'),
                textureFile  = self.file_manager.getFileByPluginType('TEXTURE'),
            )

        if vrayExporter.animation_mode == 'NONE':
            _vray_for_blender_rt.update(self.renderer)

    def render(self, scene):
        self._debug("render()")

        vrayExporter = self._get_settings()

        if self.renderer:
            if vrayExporter.animation_mode == 'NONE':
                _vray_for_blender_rt.render(self.renderer)
            else:
                _vray_for_blender_rt.update(self.renderer)


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
        # _debug("view_draw()")

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

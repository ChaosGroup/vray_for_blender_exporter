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
    if bpy.app.debug:
        sys.stderr.write("Python-engine: %s::%s\n" % (inspect.stack()[1][3], msg))
        sys.stderr.flush()

def get_file_manager(exporter, engine, scene):
    _debug('Creating files for export')

    try:
        pm = VRayFilePaths()

        # Setting user defined value here
        # It could be overriden in 'initFromScene'
        # depending on VRayDR settings
        pm.setSeparateFiles(exporter.useSeparateFiles)

        pm.initFromScene(engine, scene)
        pm.printInfo()

        fm = VRayExportFiles(pm)
        fm.setOverwriteGeometry(exporter.auto_meshes)

        fm.init()
    except Exception as e:
        _debug(e)
        return "Error initing files!"

    return fm


def _check_zmq_process(port, log_lvl):
    global _zmq_process

    log_lvl_translate = {
        'ERROR': '4',
        'WARNING': '3',
        'DEBUG': '2',
        'INFO': '1',
    }

    if _zmq_process is not None:
        _zmq_process.poll()
        _debug("ZMQ: %s -> code[%s]" % (_zmq_process, _zmq_process.returncode))

    if _zmq_process is None or _zmq_process.returncode is not None:
        executable_path = SysUtils.GetZmqPath()

        if not executable_path or not os.path.exists(executable_path):
            _debug("Can't find V-Ray ZMQ Server!")
        else:
            try:
                env = os.environ.copy()
                if sys.platform == "win32":
                    if 'VRAY_ZMQSERVER_APPSDK_PATH' not in env:
                        sys.stderr.write('Python-engine: Environment variable VRAY_ZMQSERVER_APPSDK_PATH is missing!')
                        sys.stderr.flush()
                    else:
                        appsdk = os.path.dirname(env['VRAY_ZMQSERVER_APPSDK_PATH'])
                        env['PATH'] = '%s;%s' % (env['PATH'], appsdk)
                        env['VRAY_PATH'] = appsdk
                cmd = [executable_path, "-p", port, "-log", log_lvl_translate[log_lvl]]
                _debug(' '.join(cmd))
                _zmq_process = subprocess.Popen(cmd, env=env)
            except Exception as e:
                _debug(e)



class VRayRenderer(bpy.types.RenderEngine):
    bl_idname = 'VRAY_RENDER'
    bl_label  = "V-Ray"
    bl_use_preview = True
    bl_preview_filepath = SysUtils.GetPreviewBlend()

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

        _debug("__init__()")

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'} and vrayExporter.backend_worker == 'LOCAL':
            _check_zmq_process(str(vrayExporter.zmq_port), vrayExporter.zmq_log_level)

    def __del__(self):
        _debug("__del__()")
        self._free()

    # Production rendering
    #
    def update(self, data, scene):
        _debug("update()")

        vrayExporter = self._get_settings()
        if vrayExporter.backend in {'ZMQ'} and vrayExporter.backend_worker == 'LOCAL':
            _check_zmq_process(str(vrayExporter.zmq_port), vrayExporter.zmq_log_level)

        if not self.renderer:
            arguments = {
                'context': bpy.context.as_pointer(),
                'engine': self.as_pointer(),
                'data': data.as_pointer(),
                'scene': scene.as_pointer(),
            }

            if vrayExporter.backend == 'STD':
                self.file_manager = get_file_manager(vrayExporter, self, scene)

                arguments['mainFile']     = self.file_manager.getFileByPluginType('MAIN')
                arguments['objectFile']   = self.file_manager.getFileByPluginType('OBJECT')
                arguments['envFile']      = self.file_manager.getFileByPluginType('WORLD')
                arguments['geometryFile'] = self.file_manager.getFileByPluginType('GEOMETRY')
                arguments['lightsFile']   = self.file_manager.getFileByPluginType('LIGHT')
                arguments['materialFile'] = self.file_manager.getFileByPluginType('MATERIAL')
                arguments['textureFile']  = self.file_manager.getFileByPluginType('TEXTURE')

            self.renderer = _vray_for_blender_rt.init(**arguments)

        if vrayExporter.animation_mode == 'NONE':
            _vray_for_blender_rt.update(self.renderer)

    def render(self, scene):
        _debug("render()")

        vrayExporter = self._get_settings()

        if self.renderer:
            if vrayExporter.animation_mode == 'NONE':
                _vray_for_blender_rt.render(self.renderer)
            else:
                _vray_for_blender_rt.update(self.renderer)


    # Interactive rendering
    #
    def view_update(self, context):
        _debug("view_update()")

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

#
# Copyright 2011-2013 Blender Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# <pep8 compliant>

import os
import bpy

from vb30.lib import SysUtils

import _vray_for_blender_rt


def get_stdosl_path():
    def getPaths(pathStr):
        if pathStr:
            return pathStr.strip().replace('\"','').split(os.pathsep)
        return []

    env = os.environ
    for key in sorted(env.keys()):
        if key.startswith('VRAY_OSL_PATH_'):
            for p in getPaths(env[key]):
                stdPath = os.path.join(p, 'stdosl.h')
                if os.path.exists(stdPath):
                    return stdPath

    cyclesPath = SysUtils.GetCyclesShaderPath()
    if cyclesPath:
        return os.path.join(cyclesPath, 'stdosl.h')

    return ''


_vray_for_blender_rt.osl_set_stdosl_path(get_stdosl_path())


def update_script_node(node, report):
    _vray_for_blender_rt.osl_update_node(node.id_data.as_pointer(), node.as_pointer(), bpy.data.filepath)


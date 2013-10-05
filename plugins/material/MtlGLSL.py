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

from vb25.lib   import ExportUtils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'MATERIAL'
ID   = 'MtlGLSL'
NAME = 'GLSL'
DESC = ""

PluginParams = (
    {
        'attr' : 'shader_file',
        'desc' : "",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'shader_node',
        'desc' : "Name of the target graph node if XMSL file is specified",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'textures',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'uvw_generators',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'transparency',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'transparency_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'use_shader_alpha',
        'desc' : "Switch for using either the transparency parameteres or the shader alpha result",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'uniforms',
        'desc' : "Non-varying state variables referenced by the shader",
        'type' : 'LIST',
        'default' : None,
    },
    {
        'attr' : 'max_ray_depth',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'clamp_result',
        'desc' : "Flag that shows whether to clamp final result or not",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'clamp_value',
        'desc' : "The upper clamp limit for the result color should the clamp_result flag is true",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

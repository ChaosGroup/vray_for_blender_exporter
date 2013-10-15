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


TYPE = 'TEXTURE'
ID   = 'TexPtex'
NAME = 'Ptex'
DESC = ""

PluginParams = (
    {
        'attr' : 'ptex_file',
        'desc' : "The Ptex texture file",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'use_image_sequence',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'image_number',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'image_offset',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'ifl_start_frame',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'ifl_playback_rate',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ifl_end_condition',
        'desc' : "Image file list (IFL) end condition: 0 - Loop; 1 - Ping Pong; 2 - Hold;",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'filter_type',
        'desc' : "Type of filter used for the texture",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'width',
        'desc' : "width parameter used for filtering",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'blur',
        'desc' : "blur parameter used for filtering",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'sharpness',
        'desc' : "Sharpness parameter for the general bicubic filter",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'lerp',
        'desc' : "Interpolation between mipmap levels",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reverse_vertices',
        'desc' : "Reverses the order of vertices",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'cache_size',
        'desc' : "The size of the texture cache(in MB)",
        'type' : 'INT',
        'default' : 50,
    },
    {
        'attr' : 'r_channel',
        'desc' : "The index of the channel which will be used as a red channel",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'g_channel',
        'desc' : "The index of the channel which will be used as a green channel",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'b_channel',
        'desc' : "The index of the channel which will be used as a blue channel",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'a_channel',
        'desc' : "The index of the channel which will be used as a alpha channel",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'auto_color',
        'desc' : "Use automatic color channel selection",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'auto_alpha',
        'desc' : "Use automatic alpha channel selection",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'alpha_type',
        'desc' : "Where to take the alpha from",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'color_space',
        'desc' : "0 - linear, 1 - gamma corrected, 2 - sRGB",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'gamma',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    # {
    #     'attr' : 'vertices',
    #     'desc' : "",
    #     'type' : 'VECTOR',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'origFaces',
    #     'desc' : "",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'faces',
    #     'desc' : "",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'origFacesDegree',
    #     'desc' : "",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    {
        'attr' : 'color',
        'desc' : "The final texture color",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'color_gain',
        'desc' : "A multiplier for the texture color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color_offset',
        'desc' : "An additional offset for the texture color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
)

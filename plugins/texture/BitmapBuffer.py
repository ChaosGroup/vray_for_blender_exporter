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

from pynodes_framework import idref

from vb25.lib   import ExportUtils, utils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui
from vb25.utils import get_full_filepath


TYPE = 'TEXTURE'
ID   = 'BitmapBuffer'
NAME = 'Image File'
DESC = "Image File"

PluginParams = (
    {
        'attr' : 'filter_type',
        'desc' : "-1 - nearest; 0 - no filtering; 1 - mip-map filtering; 2 - summed area table filtering",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'filter_blur',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
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
    {
        'attr' : 'maya_compatible',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'allow_negative_colors',
        'desc' : "if false negative colors will be clamped",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'interpolation',
        'desc' : "Interpolation method for the mip-map filtering (0 - bilinear, 1 - bicubic, 2 - biquadratic)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'load_file',
        'desc' : "if set to false, the file would not be loaded",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'frame_sequence',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'frame_number',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'frame_offset',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'use_data_window',
        'desc' : "true to use the data window information in e.g. OpenEXR files; otherwise false",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'psd_group_name',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'psd_alpha_name',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
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
        'attr' : 'file',
        'desc' : "The file name; can contain <UDIM> or <UVTILE> tags for Mari or Mudbox tiles respectively, or $nU and $nV for explicit tiles; lower-case tags consider the tiles as starting from 0 whereas upper-case tags start from 1",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'skip' : True,
        'default' : "",
    },
)

PluginRefParams = (
    {
        'attr' : 'image',
        'name' : "Image",
        'desc' : "Image pointer",
        'type' : 'IMAGE',
        'default' : None,
    },
)


def nodeDraw(context, layout, BitmapBuffer):
    split = layout.split()
    row = split.row(align=True)
    idref.draw_idref(row, BitmapBuffer, 'image', text="")
    row.operator("vray.open_image", icon='ZOOMIN', text="")


def writeDatablock(bus, pluginName, PluginParams, BitmapBuffer, mappedParams):
    ofile = bus['files']['textures']
    scene = bus['scene']

    ofile.write("\n%s %s {" % (ID, pluginName))

    if BitmapBuffer.image:
        filepath = get_full_filepath(bus, BitmapBuffer.image, BitmapBuffer.image.filepath)
        ofile.write('\n\tfile="%s";' % utils.AnimatedValue(scene, filepath))

    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, BitmapBuffer, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName

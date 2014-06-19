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

import bpy

from vb30.lib import DrawUtils, ExportUtils, PathUtils, BlenderUtils
from vb30 import debug


TYPE = 'TEXTURE'
ID   = 'BitmapBuffer'
NAME = 'Image File'
DESC = "Image File"

PluginParams = (
    {
        'attr' : 'filter_type',
        'desc' : "Filtering",
        'type' : 'ENUM',
        'items' : (
            ('-1', "Nearest", "Nearest"),
            ('0',  "None",    "None"),
            ('1',  "Mip-Map", "Mip-map filtering"),
            ('2',  "Area",    "Summed area filtering"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'filter_blur',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'color_space',
        'desc' : "Color space",
        'type' : 'ENUM',
        'items' : (
            ('0', "Linear",          ""),
            ('1', "Gamma corrected", ""),
            ('2', "sRGB",            "")
        ),
        'default' : '2',
    },
    {
        'attr' : 'gamma',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.0,
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
        'default' : True,
    },
    {
        'attr' : 'interpolation',
        'desc' : "Interpolation method for the Mip-Map filtering",
        'type' : 'ENUM',
        'items' : (
            ('0', "Bilinear", ""),
            ('1', "Bicubic", ""),
            ('2', "Quadratic", ""),
        ),
        'default' : '0',
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
        'desc' : "Image file list (IFL) end condition",
        'type' : 'ENUM',
        'items' : (
            ('0', "Loop", ""),
            ('1', "Ping Pong",  ""),
            ('2', "Hold", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'file',
        'desc' : "The file name; can contain <UDIM> or <UVTILE> tags for Mari or Mudbox tiles respectively,or $nU and $nV for explicit tiles; lower-case tags consider the tiles as starting from 0 whereas upper-case tags start from 1",
        'type' : 'STRING',
        'default' : "",
    },

    {
        'attr' : 'bitmap',
        'desc' : "Output BitmapBuffer plugin",
        'type' : 'OUTPUT_PLUGIN',
        'skip' : True,
        'default' : "",
    },
)


def nodeDraw(context, layout, node):
    if not node.texture:
        layout.label("Missing texture!")
        return

    layout.template_ID(node.texture, 'image', open='image.open')


def gui(context, layout, BitmapBuffer, node):
    if not node.texture:
        return

    if node.texture.image:
        if not context.scene.render.engine == 'VRAY_RENDER_PREVIEW':
            layout.template_preview(node.texture)
        layout.prop(node.texture.image, 'filepath')
    else:
        layout.template_ID(node.texture, 'image', open='image.open')
    layout.separator()

    DrawUtils.Draw(context, layout, BitmapBuffer, PluginParams)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']

    VRayScene = scene.vray
    VRayDR    = VRayScene.VRayDR

    node = bus['context'].get('node')
    if not node:
        debug.PrintError('Incorrect node context!')
        return None

    if not node.texture:
        debug.PrintError('Incorrect node texture!')
        return None

    image = node.texture.image
    if not image:
        debug.PrintError('Node "%s": Image is not set!' % node.name)
    else:
        filepath = BlenderUtils.GetFullFilepath(image.filepath, holder=image)

        if VRayDR.on:
            if VRayDR.assetSharing == 'SHARE':
                filepath = PathUtils.CopyDRAsset(bus, filepath)

        overrideParams['file'] = filepath

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

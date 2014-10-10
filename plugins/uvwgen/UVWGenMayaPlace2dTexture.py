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

import math

import bpy

from vb30.lib import DrawUtils, ExportUtils, LibUtils


TYPE = 'UVWGEN'
ID   = 'UVWGenMayaPlace2dTexture'
NAME = 'Channel (Named)'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvw_channel',
        'desc' : "Optional channel index, if uv_set_name is not found",
        'type' : 'INT',
        'default' : 0,
    },
    # {
    #     'attr' : 'uvw_channel_tex',
    #     'desc' : "Used when more than one mesh has UV linking specified for this 2d placement. If present will override uvw_channel",
    #     'type' : 'INT_TEXTURE',
    #     'default' : 1,
    # },
    {
        'attr' : 'uvwgen',
        'desc' : "Optional UVWGen from which the initial uvw coordinates will be taken, instead of the surface point",
        'type' : 'UVWGEN',
        'default' : "",
    },
    # {
    #     'attr' : 'coverage_u',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'coverage_u_tex',
        'name' : 'Coverage U',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    # {
    #     'attr' : 'coverage_v',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'coverage_v_tex',
        'name' : 'Coverage V',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    # {
    #     'attr' : 'translate_frame_u',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'translate_frame_u_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'translate_frame_v',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'translate_frame_v_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'rotate_frame',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'rotate_frame_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'skip' : True,
        'default' : 0,
    },
    {
        'attr' : 'mirror_u',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mirror_v',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'wrap_u',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'wrap_v',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'stagger',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    # {
    #     'attr' : 'repeat_u',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'repeat_u_tex',
        'name' : 'Repeat U',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    # {
    #     'attr' : 'repeat_v',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'repeat_v_tex',
        'name' : 'Repeat V',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    # {
    #     'attr' : 'offset_u',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'offset_u_tex',
        'name' : 'Offset U',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'offset_v',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'offset_v_tex',
        'name' : 'Offset V',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'rotate_uv',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'rotate_uv_tex',
        'name' : 'Rotate UV',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'noise_u',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'noise_u_tex',
        'name' : 'Noise U',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    # {
    #     'attr' : 'noise_v',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    {
        'attr' : 'noise_v_tex',
        'name' : 'Noise V',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'nsamples',
        'desc' : "The number of parameter samples to take for motion blur: 0 - means the global value; 1 - means motion blur should be disabled for this plugin",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'uv_set_name',
        'desc' : "The name of the uv channel that should be used",
        'type' : 'STRING',
        'default' : "",
    },
)


def nodeDraw(context, layout, UVWGenMayaPlace2dTexture):
    ob = context.object

    split = layout.split(percentage=0.3)
    split.label(text="Layer:")
    if ob and ob.type == 'MESH':
        split.prop_search(UVWGenMayaPlace2dTexture, 'uv_set_name',
                          ob.data, 'uv_textures',
                          text="")
    else:
        split.prop(UVWGenMayaPlace2dTexture, 'uv_set_name', text="")

    split = layout.split()
    col = split.column(align=True)
    col.prop(UVWGenMayaPlace2dTexture, 'mirror_u')
    col.prop(UVWGenMayaPlace2dTexture, 'mirror_v')

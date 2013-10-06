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


TYPE = 'UVWGEN'
ID   = 'xsiUVWGenChannel'
NAME = 'Channel (XSI)'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvw_transform',
        'desc' : "Initial transformation on the uvw coordinates, before mirror, crop etc",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'uvw_transform_tex',
        'desc' : "",
        'type' : 'TRANSFORM_TEXTURE',
        'default' : None,
    },
    {
        'attr' : 'tex_transform',
        'desc' : "Final transformation on the resulting uvw coordinates, after mirror, crop etc",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'nsamples',
        'desc' : "Number of uvw transform samples",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrap_u',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrap_v',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrap_w',
        'desc' : "0 - no wrapping, 1 - wrap, 2 - mirror tile",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_u',
        'desc' : "1 to crop in the u-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_v',
        'desc' : "1 to crop in the v-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'crop_w',
        'desc' : "1 to crop in the w-direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'coverage',
        'desc' : "Coverage",
        'type' : 'VECTOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'uvw_coords',
        'desc' : "The uvw coordinates for the specified channel at the current shading point",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'wrap_mode',
        'desc' : "Wrap mode (0 - wrap on 0.5 boundary; 1 - wrap on integer boundary",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'duvw_scale',
        'desc' : "Additional scale factor for the texture derivatives",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'uvw_channel',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'channel_type',
        'desc' : "Type of the channel used. 0 - uvw, 1 - vertex colors",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'uvwgen',
        'desc' : "Optional UVWGen from which the initial uvw coordinates will be taken, instead of the surface point",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'u_alternate',
        'desc' : "alternate image in u direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'v_alternate',
        'desc' : "alternate image in v direction",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'x_remapMin',
        'desc' : "min remap in x direction",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'y_remapMin',
        'desc' : "min remap in y direction",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'z_remapMin',
        'desc' : "min remap in z direction",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'x_remapMax',
        'desc' : "max remap in x direction",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'y_remapMax',
        'desc' : "max remap in y direction",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'z_remapMax',
        'desc' : "max remap in z direction",
        'type' : 'FLOAT',
        'default' : 1,
    },
)


def nodeDraw(context, layout, xsiUVWGenChannel):
    layout.prop(xsiUVWGenChannel, 'uvw_channel')
    

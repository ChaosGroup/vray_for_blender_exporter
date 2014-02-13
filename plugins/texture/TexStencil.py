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

import TexCommonParams3dsMax


TYPE = 'TEXTURE'
ID   = 'TexStencil'
NAME = 'Stencil'
DESC = "Stencil texture"

PluginParams = list(TexCommonParams3dsMax.PluginParams)

PluginParams.extend([
    {
        'attr' : 'image',
        'name' : "Stencil",
        'desc' : "The texture that is used as a stencil",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'mask',
        'desc' : "Represents the Stencil's transparency",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'key_masking',
        'desc' : "If true, selects the areas in the texture similar to or equal to the Color Key and masks them out",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'positive_key',
        'desc' : "If true, inverts the Chroma Key mask(only the colors specified in the Color Key and HSV Range are displayed)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'color_key',
        'desc' : "The color to be masked in the texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'hue_range',
        'desc' : "The range of hues centered on the Color Key color which are also masked",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'sat_range',
        'desc' : "The range of saturations centered on the Color Key color which are also masked",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'val_range',
        'desc' : "The range of values centered on the Color Key color which are also masked",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'default_color',
        'desc' : "Represents the texture that is underneath",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'edge_blend',
        'desc' : "Controls the sharpness of the texture edges",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'uvwgen',
        'desc' : "UVWGen from which the uvw coordinates will be taken",
        'type' : 'UVWGEN',
        'default' : "",
    },
])

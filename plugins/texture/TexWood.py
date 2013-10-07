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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexWood'
NAME = 'Wood'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },

    {
        'attr' : 'filler_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'vein_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'vein_spread',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'layer_size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.05,
    },
    {
        'attr' : 'randomness',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'age',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 20,
    },
    {
        'attr' : 'grain_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'grain_contr',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'grain_spacing',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'center_u',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'center_v',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : -0.5,
    },
    {
        'attr' : 'amplitude_x',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'amplitude_y',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ratio',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.35,
    },
    {
        'attr' : 'ripples_x',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ripples_y',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ripples_z',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'depth_min',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'depth_max',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 8,
    },
])

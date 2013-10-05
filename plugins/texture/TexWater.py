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
ID   = 'TexWater'
NAME = 'Water'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvwgen',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'height_mult',
        'desc' : "multiplier for the height of the water",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'wind_direction',
        'desc' : "direction of the wind",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'wind_magnitude',
        'desc' : "magnitude of the wind",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'wind_direction_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'choppy_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'movement_rate',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'seed',
        'desc' : "Used to produce different waters",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'resolution',
        'desc' : "Resolution -> real resolution is 2^res",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'patch_size',
        'desc' : "Size of the patch -> real resolution is 2^res",
        'type' : 'FLOAT',
        'default' : 128,
    },
)

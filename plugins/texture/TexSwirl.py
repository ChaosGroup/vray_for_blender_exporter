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
ID   = 'TexSwirl'
NAME = 'Swirl'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'color1',
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'color2',
        'desc' : "Second color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'swirl_intensity',
        'desc' : "Swirl Intensity",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'color_contrast',
        'desc' : "Color Contrast",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'swirl_amount',
        'desc' : "Swirl Amount",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'constant_detail',
        'desc' : "Constant Detail",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'center_x',
        'desc' : "Center Position X",
        'type' : 'FLOAT',
        'default' : -0.5,
    },
    {
        'attr' : 'center_y',
        'desc' : "Center Position Y",
        'type' : 'FLOAT',
        'default' : -0.5,
    },
    {
        'attr' : 'random_seed',
        'desc' : "Random Seed",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'twist',
        'desc' : "Twist",
        'type' : 'FLOAT',
        'default' : 1,
    },
])

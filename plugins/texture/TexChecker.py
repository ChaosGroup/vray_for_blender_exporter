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

from vb25.lib import ExportUtils, AttributeUtils

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexChecker'
NAME = 'Checker'
DESC = "Checker texture"

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'white_color',
        'desc' : "The white checker color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'black_color',
        'desc' : "The black checker color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'contrast',
        'desc' : "Contrast value",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
])

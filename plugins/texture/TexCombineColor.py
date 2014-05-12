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

TYPE = 'TEXTURE'
ID   = 'TexCombineColor'
NAME = 'Combine Color'
DESC = ""

PluginParams = (
    {
        'attr' : 'color',
        'desc' : "The color value",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'texture',
        'desc' : "The texture",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'texture_multiplier',
        'desc' : "The texture multiplier (blends between the value and the texture)",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'result_invert',
        'desc' : "true to invert the result",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'result_multiplier',
        'desc' : "A multiplier for the resulit (after inversion, if result_invert is true)",
        'type' : 'FLOAT',
        'default' : 1,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'color')

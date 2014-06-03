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

TYPE = 'TEXTURE'
ID   = 'TexVectorProduct'
NAME = 'Vector Product'
DESC = "Vector product"

MENU = "Math"

PluginParams = (
    {
        'attr' : 'operation',
        'desc' : "Operation",
        'type' : 'ENUM',
        'items' : (
            ('0', "No operation", ""),
            ('1', "Dot Product", ""),
            ('2', "Cross Product", ""),
            ('3', "Vector Matrix Product", ""),
            ('4', "Point Matrix Product", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'input1',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'input2',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM_TEXTURE',
        'default' : None,
    },
    {
        'attr' : 'normalize',
        'desc' : "When this is true the output vector will be normalized (in case of dot product, the input vectors are normalized before the operation)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'color',
        'desc' : "",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
)

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
ID   = 'TexVectorOp'
NAME = 'Vector Operations'
DESC = "Vector operations"

MENU = "Math"

PluginParams = (
    {
        'attr' : 'vector_a',
        'desc' : "The first vector",
        'type' : 'VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'vector_b',
        'desc' : "The first vector",
        'type' : 'VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'mult_a',
        'desc' : "Multiplier for the first vector",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'mult_b',
        'desc' : "Multiplier for the second vector",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'dot_product',
        'desc' : "The dot product",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'cross_product',
        'desc' : "The cross product",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'sum',
        'desc' : "The sum",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'difference',
        'desc' : "The difference",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'result_a',
        'desc' : "The first vector times the first multiplier",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'result_b',
        'desc' : "The second vector times the second multiplier",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'x',
        'desc' : "The x-component of the first vector",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'y',
        'desc' : "The y-component of the first vector",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'z',
        'desc' : "The z-component of the first vector",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
)

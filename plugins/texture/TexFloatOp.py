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


TYPE = 'TEXTURE'
ID   = 'TexFloatOp'
NAME = 'FloatOp'
DESC = "Float operations"

PluginParams = (
    {
        'attr' : 'float_a',
        'name' : "A",
        'desc' : "Float operand A",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'float_b',
        'name' : "B",
        'desc' : "Float operand B",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'product',
        'name' : "Product",
        'desc' : "A * B",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'options' : {'HIDDEN'},
        'default' : 1.0,
    },
    {
        'attr' : 'ratio',
        'desc' : "A/B",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'sum',
        'desc' : "A+B",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'difference',
        'desc' : "A-B",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'power',
        'desc' : "The first number raised to the power of the second number",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'sin',
        'desc' : "sin(A*B)",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'cos',
        'desc' : "cos(A*B)",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'min',
        'desc' : "min(A, B)",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'max',
        'desc' : "max(A, B)",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
)


def writeDatablock(bus, pluginName, PluginParams, FloatOp, mappedParams):
    ofile = bus['files']['textures']
    scene = bus['scene']

    ofile.write("\n%s %s {" % (ID, pluginName))

    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, FloatOp, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName

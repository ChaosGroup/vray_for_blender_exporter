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

from vb30.lib import ExportUtils
from vb30.lib import utils as LibUtils


TYPE = 'TEXTURE'
ID   = 'TexDirt'
NAME = 'Dirt'
DESC = ""

PluginParams = (
    {
        'attr' : 'white_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'black_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'radius',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'skip' : True,
        'default' : 0.1,
    },
    {
        'attr' : 'distribution',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'falloff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'bias_x',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'bias_y',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'bias_z',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ignore_for_gi',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'consider_same_object_only',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'invert_normal',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'double_sided',
        'desc' : "if true, the occlusion on both sides of the surface will be calculated",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'work_with_transparency',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ignore_self_occlusion',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'render_nodes',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'render_nodes_inclusive',
        'desc' : "if true the render_nodes list is inclusive",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_result_nodes',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'affect_result_nodes_inclusive',
        'desc' : "if true the affect_result_nodes list is inclusive",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mode',
        'desc' : "Mode",
        'type' : 'ENUM',
        'items': (
            ('0', "Ambient Occlusion", ""),
            ('1', "Phong Reflection Occlusion", ""),
            ('2', "Blinn Reflection Occlusion", ""),
            ('3', "Ward Reflection Occlusion", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'environment_occlusion',
        'desc' : "true to compute the environment for unoccluded samples",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_reflection_elements',
        'desc' : "true to add the occlusion to relection render elements when mode>0",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glossiness',
        'desc' : "A texture for the glossiness when mode>0",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
)


PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "align" : false,
        "attrs" : [
            { "name" : "mode", "expand" : false }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "distribution" },
                    { "name" : "glossiness" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "falloff" },
                    { "name" : "subdivs" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "align" : true,
        "attrs" : [
            { "name" : "bias_x", "label" : "X" },
            { "name" : "bias_y", "label" : "Y" },
            { "name" : "bias_z", "label" : "Z" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "invert_normal" },
                    { "name" : "ignore_for_gi" },
                    { "name" : "ignore_self_occlusion" },
                    { "name" : "consider_same_object_only" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "affect_reflection_elements" },
                    { "name" : "work_with_transparency" },
                    { "name" : "environment_occlusion" },
                    { "name" : "double_sided" }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "render_nodes_inclusive" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : false,
                "attrs" : [
                    { "name" : "affect_result_nodes_inclusive" }
                ]
            }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, mappedParams):
    scene = bus['scene']
    o     = bus['output']

    radiusResult = propGroup.radius

    if 'radius' in mappedParams:
        if type(mappedParams['radius']) is float:
            radiusResult = LibUtils.AnimatedValue(scene, mappedParams['radius'])
        else:
            radiusTexName = pluginName + "Radius"
            radiusResult = radiusTexName + "::product"

            o.set('TEXTURE', 'TexFloatOp', radiusTexName)
            o.writeHeader()
            o.writeAttibute("float_a", mappedParams['radius'])
            o.writeAttibute("float_b", LibUtils.AnimatedValue(scene, propGroup.radius))
            o.writeFooter()

    o.set(pluginModule.TYPE, pluginModule.ID, pluginName)
    o.writeHeader()
    o.writeAttibute("radius", radiusResult)

    ExportUtils.WritePluginParams(bus, pluginModule, pluginName, propGroup, mappedParams)

    o.writeFooter()

    return pluginName

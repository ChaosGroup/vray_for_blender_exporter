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

from vb25.lib        import ExportUtils, utils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


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
            ('0', "Ambient occlusion", ""),
            ('1', "Phong reflection occlusion", ""),
            ('2', "Blinn reflection occlusion", ""),
            ('3', "Ward reflection occlusion", ""),
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


def gui(context, layout, TexDirt):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    layout.prop(TexDirt, 'mode')

    layout.separator()

    split = layout.split()
    col = split.column()
    sub_radius = col.column(align=True)
    sub_radius.prop(TexDirt,'radius')

    col.prop(TexDirt,'distribution')
    if TexDirt.mode != 'AO':
        col.prop(TexDirt, 'glossiness')
    if wide_ui:
        col = split.column()
    col.prop(TexDirt, 'falloff')
    col.prop(TexDirt, 'subdivs')
    if TexDirt.mode != 'AO':
        col.prop(TexDirt, 'affect_reflection_elements')

    layout.separator()

    split = layout.split()
    row = split.row(align=True)
    row.prop(TexDirt, 'bias_x')
    row.prop(TexDirt, 'bias_y')
    row.prop(TexDirt, 'bias_z')

    layout.separator()

    split = layout.split()
    col = split.column()
    col.prop(TexDirt, 'invert_normal')
    col.prop(TexDirt, 'ignore_for_gi')
    col.prop(TexDirt, 'ignore_self_occlusion')
    col.prop(TexDirt, 'consider_same_object_only')
    if wide_ui:
        col = split.column()
    col.prop(TexDirt, 'work_with_transparency')
    col.prop(TexDirt, 'environment_occlusion')
    col.prop(TexDirt, 'double_sided')

    layout.separator()

    split = layout.split()
    col = split.column()
    col.prop_search(TexDirt,  'render_nodes',
                    bpy.data, 'groups',
                    text="Exclude")
    col.prop(TexDirt, 'render_nodes_inclusive')

    split = layout.split()
    col = split.column()
    col.prop_search(TexDirt,  'affect_result_nodes',
                    bpy.data, 'groups',
                    text="Result Affect")
    col.prop(TexDirt, 'affect_result_nodes_inclusive')


def writeDatablock(bus, pluginName, PluginParams, TexDirt, mappedParams):
    ofile = bus['files']['nodetree']
    scene = bus['scene']

    radiusTexResult = None

    if 'radius' in mappedParams:
        radiusTexName = pluginName + "Radius"
        radiusTexResult = radiusTexName + "::product"

        ofile.write("\nTexFloatOp %s {" % radiusTexName)
        ofile.write("\n\tfloat_a=%s;" % mappedParams['radius'])
        ofile.write("\n\tfloat_b=%s;" % utils.AnimatedValue(scene, TexDirt.radius))
        ofile.write("\n}\n")

    ofile.write("\n%s %s {" % (ID, pluginName))

    if radiusTexResult:
        ofile.write("\n\tradius=%s;" % radiusTexResult)
    else:
        ofile.write("\n\tradius=%s;" % utils.AnimatedValue(scene, TexDirt.radius))

    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, TexDirt, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName

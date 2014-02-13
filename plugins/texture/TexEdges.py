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

from vb30.lib import ExportUtils


TYPE = 'TEXTURE'
ID   = 'TexEdges'
NAME = 'Edges'
DESC = ""

PluginParams = (
    {
        'attr' : 'edges_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'bg_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'width_type',
        'desc' : "Width Type",
        'type' : 'ENUM',
        'items' : (
            ('0', "World", ""),
            ('1', "Pixels", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'pixel_width',
        'name' : 'Width',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    # {
    #     'attr' : 'world_width',
    #     'desc' : "",
    #     'type' : 'FLOAT_TEXTURE',
    #     'default' : 0.01,
    # },
    {
        'attr' : 'show_hidden_edges',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'show_subtriangles',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "width_type" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "pixel_width", "label" : "Width" }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "show_hidden_edges" },
            { "name" : "show_subtriangles" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'world_width' : overrideParams['pixel_width'],
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

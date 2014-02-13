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

import TexCommonParams3dsMax


TYPE = 'TEXTURE'
ID   = 'TexCompMax'
NAME = 'Comp Max'
DESC = ""

PluginParams = list(TexCommonParams3dsMax.PluginParams)

PluginParams.extend([
    {
        'attr' : 'sourceA',
        'name' : 'Source A',
        'desc' : "Left hand side texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'sourceB',
        'name' : 'Source B',
        'desc' : "Right hand side texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'operator',
        'desc' : "Operator",
        'type' : 'ENUM',
        'items' : (
            ('0', "Add", ""),
            ('1', "Subtract", ""),
            ('2', "Difference", ""),
            ('3', "Multiply", ""),
            ('4', "Divide", ""),
            ('5', "Minimum", ""),
            ('6', "Maximum", ""),
        ),
        'default' : '0',
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "operator" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams3dsMax.PluginWidget)


def nodeDraw(context, layout, TexCompMax):
    layout.prop(TexCompMax, 'operator', text="")

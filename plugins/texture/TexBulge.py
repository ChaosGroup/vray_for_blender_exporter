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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexBulge'
NAME = 'Bulge'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)

PluginParams.extend([
    {
        'attr' : 'u_width',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'v_width',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "align" : true,
        "attrs" : [
            { "name" : "u_width" },
            { "name" : "v_width" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)


def nodeDraw(context, layout, TexBulge):
    split = layout.split()
    col = split.column(align=True)
    col.prop(TexBulge, 'u_width')
    col.prop(TexBulge, 'v_width')

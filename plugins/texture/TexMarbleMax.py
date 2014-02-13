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
ID   = 'TexMarbleMax'
NAME = 'MarbleMax'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)

PluginParams.extend([
    {
        'attr' : 'color1',
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color2',
        'desc' : "Second color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'size',
        'desc' : "Size",
        'type' : 'FLOAT',
        'default' : 70,
    },
    {
        'attr' : 'vein_width',
        'desc' : "Vein width",
        'type' : 'FLOAT',
        'default' : 0.02,
    },

    {
        'attr' : 'use_3d_mapping',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "size" },
            { "name" : "vein_width" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "use_3d_mapping" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)

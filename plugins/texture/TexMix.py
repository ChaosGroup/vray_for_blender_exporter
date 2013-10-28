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

import TexCommonParams3dsMax


TYPE = 'TEXTURE'
ID   = 'TexMix'
NAME = 'Mix'
DESC = ""

PluginParams = list(TexCommonParams3dsMax.PluginParams)

PluginParams.extend([
    {
        'attr' : 'color1',
        'name' : "Source A",
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color2',
        'name' : "Source B",
        'desc' : "Second color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'mix_map',
        'desc' : "Mix amount texture",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'transition_upper',
        'desc' : "Transition zone - upper",
        'type' : 'FLOAT',
        'default' : 0.7,
    },
    {
        'attr' : 'transition_lower',
        'desc' : "Transition zone - lower",
        'type' : 'FLOAT',
        'default' : 0.3,
    },

    # {
    #     'attr' : 'mix_amount',
    #     'desc' : "Mix amount",
    #     'type' : 'FLOAT',
    #     'default' : 0,
    # },
    # {
    #     'attr' : 'use_curve',
    #     'desc' : "If true the blend curve is used",
    #     'type' : 'INT',
    #     'default' : 0,
    # },
])

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "transition_upper" },
            { "name" : "transition_lower" }
        ]
    },

    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams3dsMax.PluginWidget)

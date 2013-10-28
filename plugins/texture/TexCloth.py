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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexCloth'
NAME = 'Cloth'
DESC = ""

PluginParams = list(TexCommonParams.PluginParams)

PluginParams.extend([
    {
        'attr' : 'gap_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'u_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'v_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'u_width',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.75,
    },
    {
        'attr' : 'v_width',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.75,
    },
    {
        'attr' : 'u_wave',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'v_wave',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'width_spread',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'bright_spread',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },

    {
        'attr' : 'randomness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
])

PluginWidget = """
{ "widgets": [
    {TEX_COMMON}
]}
"""
PluginWidget = PluginWidget.replace('{TEX_COMMON}', TexCommonParams.PluginWidget)

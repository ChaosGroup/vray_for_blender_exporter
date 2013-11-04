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


TYPE = 'BRDF'
ID   = 'BRDFSSS'
NAME = 'SSS'
DESC = ""

PluginParams = (
    {
        'attr' : 'color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color_tex',
        'name' : "Color",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'color_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'translucency',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'translucency_tex',
        'name' : "Translucency",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'translucency_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'glossiness',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'glossiness_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'glossiness_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'thickness',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'scatter_coeff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'scatter_direction',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "thickness" },
                    { "name" : "subdivs" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "scatter_coeff", "label" : "Coeff" },
                    { "name" : "scatter_direction", "label" : "Direction" }
                ]
            }
        ]
    }
]}
"""

def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'color' : (0.0, 0.0, 0.0),
        'color_tex_mult' : 1.0,
        'translucency' : (0.0, 0.0, 0.0),
        'translucency_tex_mult' : 1.0,
        'glossiness' : (0.0, 0.0, 0.0),
        'glossiness_tex_mult' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

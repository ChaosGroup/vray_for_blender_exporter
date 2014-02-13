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
import mathutils

from vb30.lib import ExportUtils


TYPE = 'BRDF'
ID   = 'BRDFGlass'
NAME = 'Glass'
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
        'attr' : 'transparency',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'transparency_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ior',
        'desc' : "IOR for the glass; this is ignored if the surface has a volume shader (the volume IOR is used)",
        'type' : 'FLOAT',
        'default' : 1.55,
    },
    {
        'attr' : 'ior_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'affect_shadows',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_alpha',
        'desc' : "Determines how refractions affect the alpha channel",
        'type' : 'ENUM',
        'items' : (
            ('0',  "Color Only",   "The transperency will affect only the RGB channel of the final render"),
            ('1',  "Color+Alpha",  "This will cause the material to transmit the alpha of the reflected objects, instead of displaying an opaque alpha"),
            ('2',  "All Channels", "All channels and render elements will be affected by the transperency of the material"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'trace_refractions',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'trace_depth',
        'desc' : "The maximum refraction bounces (-1 is controlled by the global options)",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'exit_color_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reflect_exit_color',
        'desc' : "The color to use when the maximum depth is reached",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'refract_exit_color',
        'desc' : "The color to use when maximum depth is reached when exit_color_on is true",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'volume',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "trace_refractions" },
                    { "name" : "trace_depth" },
                    { "name" : "cutoff" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "affect_alpha" },
                    { "name" : "affect_shadows" }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "exit_color_on" }
        ]
    },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "exit_color_on" },
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "reflect_exit_color"}
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "refract_exit_color" }
                ]
            }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'ior' : 1.0,
        'color' : mathutils.Color((0.0, 0.0, 0.0)),
        'color_tex_mult' : 1.0,
        'transparency' : mathutils.Color((0.0, 0.0, 0.0)),
        'transparency_tex_mult' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

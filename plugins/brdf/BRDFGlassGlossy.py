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
ID   = 'BRDFGlassGlossy'
NAME = 'Glass Glossy'
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
    {
        'attr' : 'ior_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'glossiness',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.8,
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
        'attr' : 'dispersion_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dispersion',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'interpolation_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'imap_min_rate',
        'name' : "Min Rate",
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'imap_max_rate',
        'name' : "Max Rate",
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'imap_color_thresh',
        'name' : "Color Thresh",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'imap_norm_thresh',
        'name' : "Normal Thresh",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'imap_samples',
        'name' : "Samples",
        'desc' : "",
        'type' : 'INT',
        'default' : 20,
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
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "dispersion_on", "label" : "Use Dispersion" }
                ]
            },
            {   "layout" : "COLUMN",
                "active" : { "prop" : "dispersion_on" },
                "attrs" : [
                    { "name" : "dispersion" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "interpolation_on", "label" : "Use Interpolation" }
        ]
    },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "interpolation_on" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "imap_min_rate" },
                    { "name" : "imap_max_rate" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "imap_samples" },
                    { "name" : "imap_color_thresh" },
                    { "name" : "imap_norm_thresh" }
                ]
            }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'color' : mathutils.Color((0.0, 0.0, 0.0)),
        'color_tex_mult' : 1.0,
        'transparency' : mathutils.Color((0.0, 0.0, 0.0)),
        'transparency_tex_mult' : 1.0,
        'glossiness' : 1.0,
        'glossiness_tex_mult' : 1.0,
        'ior' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)


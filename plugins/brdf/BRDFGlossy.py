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
ID   = 'BRDFGlossy'
NAME = 'Glossy'
DESC = "Glossy reflection shader (BRDFBlinn, BRDFPhong, BRDFWard)"

PluginParams = (
    # {
    #     'attr' : 'color',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (1, 1, 1),
    # },
    {
        'attr' : 'color_tex',
        'name' : "Reflection",
        'desc' : "Reflection amount",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    # {
    #     'attr' : 'color_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    # {
    #     'attr' : 'transparency',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    # {
    #     'attr' : 'transparency_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'back_side',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'trace_reflections',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'trace_depth',
        'desc' : "The maximum reflection depth (-1 is controlled by the global options)",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'affect_alpha',
        'desc' : "Specifies how render channels are propagated through the BRDF (0 - only the color channel; 1 - color and alpha; 2 - all channels",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'reflect_exit_color',
        'desc' : "The color to use when the maximum depth is reached",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'reflect_dim_distance',
        'desc' : "How much to dim reflection as length of rays increases",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'reflect_dim_distance_on',
        'desc' : "True to enable dim distance",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reflect_dim_distance_falloff',
        'desc' : "Fall off for the dim distance",
        'type' : 'FLOAT',
        'default' : 0,
    },
    # {
    #     'attr' : 'hilightGlossiness',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1.0,
    # },
    {
        'attr' : 'hilightGlossiness_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    # {
    #     'attr' : 'hilightGlossiness_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    # {
    #     'attr' : 'reflectionGlossiness',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1.0,
    # },
    {
        'attr' : 'reflectionGlossiness_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    # {
    #     'attr' : 'reflectionGlossiness_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'glossyAsGI',
        'desc' : "Determines if the glossy rays are treated by V-Ray as GI rays",
        'type' : 'ENUM',
        'items' : (
            ('0', "Never", "Never"),
            ('1', "GI Rays", "Only for rays that are already marked as GI rays"),
            ('2', "Always", "Always"),
        ),
        'default' : '1',
    },
    {
        'attr' : 'soften_edge',
        'desc' : "Soften edge of the BRDF at light/shadow transition",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'interpolation_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'imap_min_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'imap_max_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'imap_color_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'imap_norm_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'imap_samples',
        'desc' : "",
        'type' : 'INT',
        'default' : 20,
    },
    {
        'attr' : 'anisotropy',
        'desc' : "Reflection anisotropy in the range (-1, 1)",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'anisotropy_uvwgen',
        'desc' : "",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'anisotropy_rotation',
        'desc' : "Anisotropy rotation in the range [0, 1]",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'fix_dark_edges',
        'desc' : "true to fix dark edges with glossy reflections; only set this to false for compatibility with older versions",
        'type' : 'BOOL',
        'default' : True,
    },

    {
        'attr' : 'brdf_type',
        'desc' : "BRDF type",
        'type' : 'ENUM',
        'items' : (
            ('PHONG', "Phong", "BRDFPhong"),
            ('BLINN', "Blinn", "BRDFBlinn"),
            ('WARD',  "Ward",  "BRDFWard"),
        ),
        'skip'    : True,
        'default' : 'BLINN',
    },
)

BRDF_TYPE = {
    'PHONG' : "BRDFPhong",
    'BLINN' : "BRDFBlinn",
    'WARD'  : "BRDFWard",
}


def writeDatablock(bus, pluginName, PluginParams, BRDFGlossy, mappedParams):
    ofile = bus['files']['materials']
    scene = bus['scene']

    brdf_type = BRDF_TYPE[BRDFGlossy.brdf_type]

    ofile.write("\n%s %s {" % (brdf_type, pluginName))
    ofile.write("\n\tcolor=Color(0.0,0.0,0.0);")
    ofile.write("\n\tcolor_tex_mult=1.0;")
    ofile.write("\n\ttransparency=Color(0.0,0.0,0.0);")
    ofile.write("\n\ttransparency_tex_mult=1.0;")
    ofile.write("\n\thilightGlossiness=Color(0.0,0.0,0.0);")
    ofile.write("\n\thilightGlossiness_tex_mult=1.0;")
    ofile.write("\n\treflectionGlossiness=Color(0.0,0.0,0.0);")
    ofile.write("\n\treflectionGlossiness_tex_mult=1.0;")

    ExportUtils.WritePluginParams(bus, ofile, BRDFGlossy, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName


def nodeDraw(context, layout, BRDFGlossy):
    layout.prop(BRDFGlossy, 'brdf_type', text="Type")


def gui(context, layout, BRDFGlossy):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    split= layout.split()
    col= split.column()
    col.prop(BRDFGlossy, 'subdivs')
    if wide_ui:
        col= split.column()
    col.prop(BRDFGlossy, 'trace_depth')

    split= layout.split()
    col= split.column()
    col.prop(BRDFGlossy, 'cutoff')
    col.prop(BRDFGlossy, 'back_side')
    col.prop(BRDFGlossy, 'trace_reflections')
    if wide_ui:
        col= split.column()
    col.prop(BRDFGlossy, 'reflect_dim_distance_on')
    sub = col.column()
    sub.active = BRDFGlossy.reflect_dim_distance_on
    sub.prop(BRDFGlossy, 'reflect_dim_distance')
    sub.prop(BRDFGlossy, 'reflect_dim_distance_falloff')

    layout.separator()

    layout.prop(BRDFGlossy, 'glossyAsGI')

    layout.separator()

    split= layout.split()
    col= split.column()
    col.prop(BRDFGlossy, 'soften_edge')
    if wide_ui:
        col= split.column()
    col.prop(BRDFGlossy, 'fix_dark_edges')

    layout.separator()

    split= layout.split()
    col= split.column()
    col.prop(BRDFGlossy, 'interpolation_on')
    if BRDFGlossy.interpolation_on:
        split= layout.split()
        col= split.column()
        col.prop(BRDFGlossy, 'imap_min_rate')
        col.prop(BRDFGlossy, 'imap_max_rate')
        col.prop(BRDFGlossy, 'imap_samples')
        if wide_ui:
            col= split.column()
        col.prop(BRDFGlossy, 'imap_color_thresh')
        col.prop(BRDFGlossy, 'imap_norm_thresh')

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

TYPE = 'SETTINGS'
ID   = 'SettingsImageSampler'
NAME = 'Image Sampler'
DESC = ""

PluginParams = (
    {
        'attr' : 'type',
        'desc' : "The type of the image sampler",
        'type' : 'ENUM',
        'items' : (
            ('0', "Fixed", ""),
            ('1', "Adaptive DMC", ""),
            ('2', "Adaptive Subdivision", ""),
            ('3', "Progressive", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'fixed_subdivs',
        'name' : "Subdivs",
        'desc' : "Subdivs value for the fixed sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'fixed_per_pixel_filtering',
        'name' : "Per Pixel Filtering",
        'desc' : "true to enable per-pixel filtering for the fixed sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dmc_minSubdivs',
        'name' : "Min. Subdivs",
        'desc' : "Min. subdivs value for the adaptive DMC image sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'dmc_maxSubdivs',
        'name' : "Max. Subdivs",
        'desc' : "Max. subdivs value for the adaptive DMC image sampler",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'dmc_threshold',
        'name' : "Threshold",
        'desc' : "Color threshold for the adaptive DMC image sampler",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'dmc_show_samples',
        'name' : "Show Samples",
        'desc' : "true to show the samples for the adaptive DMC image sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dmc_per_pixel_filtering',
        'name' : "Per Pixel Filtering",
        'desc' : "true to enable per-pixel filtering for the adaptive DMC image sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_minRate',
        'name' : "Min. Rate",
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'subdivision_maxRate',
        'name' : "Max. Rate",
        'desc' : "",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'subdivision_jitter',
        'name' : "Jitter",
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'subdivision_threshold',
        'name' : "Threshold",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.15,
    },
    {
        'attr' : 'subdivision_edges',
        'name' : "Edges",
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_normals',
        'name' : "Normals",
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_normals_threshold',
        'name' : "Normals Threshold",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'subdivision_show_samples',
        'name' : "Show Samples",
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'progressive_minSubdivs',
        'name' : "Min. Subdivs",
        'desc' : "Min. subdivs value for the progressive image sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'progressive_maxSubdivs',
        'name' : "Max. Subdivs",
        'desc' : "Max. subdivs value for the progressive image sampler",
        'type' : 'INT',
        'default' : 100,
    },
    {
        'attr' : 'progressive_threshold',
        'name' : "Threshold",
        'desc' : "Noise threshold for the progressive image sampler",
        'type' : 'FLOAT',
        'precision' : 4,
        'default' : 0.01,
    },
    {
        'attr' : 'progressive_maxTime',
        'name' : "Max. Time",
        'desc' : "Max. render time for the progressive image sampler",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'progressive_bundleSize',
        'name' : "Bundle Size",
        'desc' : "Bundle size for the progressive image sampler",
        'type' : 'INT',
        'default' : 64,
    },
    {
        'attr' : 'progressive_showMask',
        'name' : "Show Mask",
        'desc' : "If true, the AA mask will be rendered",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'min_shade_rate',
        'name' : "Min Sading Rate",
        'desc' : "",
        'type' : 'INT',
        'default' : 2,
    },

    {
        'attr' : 'use_dmc_treshhold',
        'name' : "Use DMC sampler threshold",
        'desc' : "Use threshold specified in the \"DMC sampler\"",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
    {
        'attr' : 'filter_type',
        'desc' : "Antialiasing filter type",
        'type' : 'ENUM',
        'items' : (
            ('NONE',               "None",               ""),
            ('FilterArea',         "Area",               ""),
            ('FilterBox',          "Box",                ""),
            ('FilterCatmullRom',   "Catmull-Rom",        ""),
            ('FilterCookVariable', "Cook Variable",      ""),
            ('FilterGaussian',     "Gaussian",           ""),
            ('FilterLanczos',      "Lanczos",            ""),
            ('FilterMitNet',       "Mitchell-Netravali", ""),
            ('FilterSinc',         "Sinc",               ""),
            ('FilterTriangle',     "Triangle",           ""),
        ),
        'skip' : True,
        'default' : 'NONE',
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "type" }
        ]
    },
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "min_shade_rate" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "COLUMN",
        "show" : { "prop" : "type", "condition" : "0" },
        "attrs" : [
            { "name" : "fixed_subdivs" },
            { "name" : "fixed_per_pixel_filtering" }
        ]
    },

    {   "layout" : "SPLIT",
        "show" : { "prop" : "type", "condition" : "1" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "dmc_minSubdivs" },
                    { "name" : "dmc_maxSubdivs" },
                    { "name" : "dmc_threshold" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "dmc_show_samples" },
                    { "name" : "dmc_per_pixel_filtering" },
                    { "name" : "use_dmc_treshhold" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "show" : { "prop" : "type", "condition" : "2" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "subdivision_minRate" },
                    { "name" : "subdivision_maxRate" },
                    { "name" : "subdivision_threshold" },
                    { "name" : "subdivision_normals_threshold" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "subdivision_show_samples" },
                    { "name" : "subdivision_jitter" },
                    { "name" : "subdivision_edges" },
                    { "name" : "subdivision_normals" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "show" : { "prop" : "type", "condition" : "3" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "progressive_minSubdivs" },
                    { "name" : "progressive_maxSubdivs" },
                    { "name" : "progressive_threshold" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "progressive_maxTime" },
                    { "name" : "progressive_bundleSize" },
                    { "name" : "progressive_showMask" }
                ]
            }
        ]
    }
]}
"""


# TODO: resolve use_dmc_treshhold
# TODO: resolve filter export
# TODO: Resolve draft / preview
# TODO: Try using progressive sampler for preview with render time restriction
#
# bus['files']['scene'].write("\nSettingsImageSampler {")
# bus['files']['scene'].write("\n\ttype=0;")
# bus['files']['scene'].write("\n\tfixed_subdivs=1;")
# bus['files']['scene'].write("\n}\n")

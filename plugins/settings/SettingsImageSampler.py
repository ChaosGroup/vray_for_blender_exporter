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

TYPE = 'SETTINGS'
ID   = 'SettingsImageSampler'
NAME = 'SettingsImageSampler'
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
        'default' : '0',
    },
    {
        'attr' : 'fixed_subdivs',
        'desc' : "Subdivs value for the fixed sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'fixed_per_pixel_filtering',
        'desc' : "true to enable per-pixel filtering for the fixed sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dmc_minSubdivs',
        'desc' : "Min. subdivs value for the adaptive DMC image sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'dmc_maxSubdivs',
        'desc' : "Max. subdivs value for the adaptive DMC image sampler",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'dmc_threshold',
        'desc' : "Color threshold for the adaptive DMC image sampler",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'dmc_show_samples',
        'desc' : "true to show the samples for the adaptive DMC image sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dmc_per_pixel_filtering',
        'desc' : "true to enable per-pixel filtering for the adaptive DMC image sampler",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_minRate',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'subdivision_maxRate',
        'desc' : "",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'subdivision_jitter',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'subdivision_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.15,
    },
    {
        'attr' : 'subdivision_edges',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_normals',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'subdivision_normals_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'subdivision_show_samples',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'progressive_minSubdivs',
        'desc' : "Min. subdivs value for the progressive image sampler",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'progressive_maxSubdivs',
        'desc' : "Max. subdivs value for the progressive image sampler",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'progressive_threshold',
        'desc' : "Noise threshold for the progressive image sampler",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'progressive_maxTime',
        'desc' : "Max. render time for the progressive image sampler",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'progressive_bundleSize',
        'desc' : "Bundle size for the progressive image sampler",
        'type' : 'INT',
        'default' : 64,
    },
    {
        'attr' : 'progressive_showMask',
        'desc' : "If true, the AA mask will be rendered",
        'type' : 'INT',
        'default' : 0,
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
]}
"""

# TODO: resolve use_dmc_treshhold
# TODO: resolve filter export

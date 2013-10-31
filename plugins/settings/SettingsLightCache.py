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
ID   = 'SettingsLightCache'
NAME = 'SettingsLightCache'
DESC = ""

PluginParams = (
    {
        'attr' : 'subdivs',
        'desc' : "This determines how many paths are traced from the camera. The actual number of paths is the square of the subdivs",
        'type' : 'INT',
        'default' : 1000,
    },
    {
        'attr' : 'sample_size',
        'desc' : "This determines the spacing of the samples in the light cache",
        'type' : 'FLOAT',
        'default' : 0.03,
    },
    {
        'attr' : 'filter_type',
        'desc' : "The filter determines how irradiance is interpolated from the samples in the light cache",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('1', "Nearest", ""),
            ('2', "Fixed", "")
        ),
        'default' : '1',
    },
    {
        'attr' : 'filter_samples',
        'desc' : "How many of the nearest samples to look up from the light cache",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'filter_size',
        'desc' : "The size of the filter",
        'type' : 'FLOAT',
        'default' : 0.06,
    },
    {
        'attr' : 'prefilter',
        'desc' : "Filter light cache sampler before rendering",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'prefilter_samples',
        'desc' : "Number of prefilter samples",
        'type' : 'INT',
        'default' : 10,
    },
    {
        'attr' : 'depth',
        'desc' : "Light cache trace depth",
        'type' : 'INT',
        'default' : 100,
    },
    {
        'attr' : 'show_calc_phase',
        'desc' : "Turning this option on will show the paths that are traced",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'store_direct_light',
        'desc' : "With this option, the light cache will also store and interpolate direct light",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'world_scale',
        'desc' : "This parameter determines the units of the \"Sample size\" and the \"Filter size\"",
        'type' : 'ENUM',
        'items' : (
            ('0', "Screen", ""),
            ('1', "World", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'mode',
        'desc' : "Light cache mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Single Frame", ""),
            ('1', "From File", ""),
            ('2', "Fly-Through", ""),
            ('3', "Progressive Path Tracing", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'file',
        'desc' : "Light cache file",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/light_cache.vrmap",
    },
    {
        'attr' : 'dont_delete',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'auto_save',
        'desc' : "Auto save Light Cache",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'auto_save_file',
        'desc' : "Light cache auto save file name",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/light_cache.vrmap",
    },
    {
        'attr' : 'num_passes',
        'desc' : "The light cache is computed in several passes, which are then combined into the final light cache",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'use_for_glossy_rays',
        'desc' : "If this option is on, the light cache will be used to compute lighting for glossy rays as well, in addition to normal GI rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adaptive_sampling',
        'desc' : "When this option is on, V-Ray will store additional information about the incoming light for each light cache sample, and try to put more samples into the directions from which more light coming",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'multiple_views',
        'desc' : "When this option is on, V-Ray will calculate the light cache samples for the entire camera path, instead of just the current view, in the same way as this is done for the Fly-through mode",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'retrace_enabled',
        'desc' : "Enable retrace of light cache",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'retrace_threshold',
        'desc' : "Retrace treshold, relative to the light cache sample size",
        'type' : 'FLOAT',
        'default' : 1,
    },

    {
        'attr' : 'num_passes_auto',
        'name' : "Auto Num. Passes",
        'desc' : "Set number of passes to threads number",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

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
ID   = 'SettingsPhotonMap'
NAME = 'Photon Map'
DESC = ""

PluginParams = (
    {
        'attr' : 'bounces',
        'desc' : "The number of light bounces approximated by the photon map",
        'type' : 'INT',
        'default' : 10,
    },
    {
        'attr' : 'max_photons',
        'desc' : "This option specifies how many photons will be taken into consideration when approximating the irradiance at the shaded point",
        'type' : 'INT',
        'default' : 30,
    },
    {
        'attr' : 'prefilter',
        'desc' : "This will cause V-Ray to precompute the irradiance at the photon hit points stored in the photon map",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'prefilter_samples',
        'desc' : "This controls how many irradiance samples will be taken from the photon map once it is converted to an irradiance map",
        'type' : 'INT',
        'default' : 10,
    },
    {
        'attr' : 'mode',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'file',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'auto_search_distance',
        'desc' : "Try to compute a suitable distance within which to search for photons",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'search_distance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'convex_hull_estimate',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dont_delete',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'auto_save',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'auto_save_file',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'store_direct_light',
        'desc' : "Store direct illumination in the photon map as well",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'multiplier',
        'desc' : "This allows you to control the brightness of the photon map",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'max_density',
        'desc' : "This parameter allows you to limit the resolution (and thus the memory) of the photon map",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'retrace_corners',
        'desc' : "When this is greater than 0.0, V-Ray will use brute force GI near corners, instead of the photon map, in order to obtain a more accurate result and to avoid splotches in these areas",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'retrace_bounces',
        'desc' : "Controls how many bounces will be made when retracing corners",
        'type' : 'INT',
        'default' : 10,
    },
    {
        'attr' : 'show_calc_phase',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

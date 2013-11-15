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
ID   = 'SettingsCaustics'
NAME = 'SettingsCaustics'
DESC = ""

PluginParams = (
    {
        'attr' : 'on',
        'name' : "Use Caustics",
        'desc' : "Enable caustics computation",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'max_photons',
        'desc' : "",
        'type' : 'INT',
        'default' : 30,
    },
    {
        'attr' : 'search_distance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'max_density',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'multiplier',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'mode',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "New",  ""),
            ('1', "From File", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'file',
        'desc' : "",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'dont_delete',
        'desc' : "Don't delete at render end",
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

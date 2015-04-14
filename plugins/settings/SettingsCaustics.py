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
ID   = 'SettingsCaustics'
NAME = 'Caustics'
DESC = ""

PluginParams = (
    {
        'attr' : 'on',
        'name' : "Use Caustics",
        'desc' : "Enable caustics computation",
        'type' : 'BOOL',
        'default' : False,
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
        'desc' : "File to take caustics map from when 'Mode' is 'From File'",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/caustics.vrmap",
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
        'name' : "File",
        'desc' : "Auto save filepath",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/caustics.vrmap",
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
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "mode" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "mode", "value" : 0 },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "multiplier" },
                    { "name" : "search_distance" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "max_photons" },
                    { "name" : "max_density" },
                    { "name" : "show_calc_phase" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "file", "active" : { "prop" : "mode", "value" : 1 } }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "auto_save" },
            { "name" : "auto_save_file", "active" : { "prop" : "auto_save" } }
        ]
    }
]}
"""

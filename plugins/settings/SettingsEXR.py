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
ID   = 'SettingsEXR'
NAME = 'SettingsEXR'
DESC = ""

PluginParams = (
    {
        'attr' : 'compression',
        'desc' : "Compression for OpenEXR output",
        'type' : 'ENUM',
        'items' : (
            ('0', "Default", ""),
            ('1', "No Compression", ""),
            ('2', "RLE", ""),
            ('3', "ZIPS", ""),
            ('4', "ZIP", ""),
            ('5', "PIZ", ""),
            ('6', "pxr24", ""),
        ),
        'default' : '3',
    },
    {
        'attr' : 'bits_per_channel',
        'desc' : "Bits per channel",
        'type' : 'ENUM',
        'items' : (
            ('16', "16", ""),
            ('32', "32", ""),
        ),
        'default' : '16',
    },
    {
        'attr' : 'extra_attributes',
        'desc' : "Extra attributes to write in the header",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'auto_data_window',
        'desc' : "true to enable auto data window based on the alpha channel when writing scanline-based multichannel OpenEXR files",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'write_integer_ids',
        'desc' : "true to write integer elemnt ids when using Image Format exr",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "compression"},
            { "name" : "bits_per_channel"}
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "extra_attributes"}
        ]
    },
    
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "auto_data_window"},
            { "name" : "write_integer_ids"}
        ]
    }
]}
"""

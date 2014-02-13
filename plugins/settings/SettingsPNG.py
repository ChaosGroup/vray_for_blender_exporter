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
ID   = 'SettingsPNG'
NAME = 'PNG'
DESC = ""

PluginParams = (
    {
        'attr' : 'compression',
        'desc' : "Compression for PNG output (0-9)",
        'type' : 'INT',
        'ui' : {
            'min' : 0,
            'max' : 9,
        },
        'default' : 9,
    },
    {
        'attr' : 'bits_per_channel',
        'desc' : "Bits per channel (8 or 16)",
        'type' : 'ENUM',
        'items' : (
            ('8',  "8", ""),
            ('16', "16", ""),
        ),
        'default' : '16',
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "compression"},
            { "name" : "bits_per_channel" }
        ]
    }
]}
"""

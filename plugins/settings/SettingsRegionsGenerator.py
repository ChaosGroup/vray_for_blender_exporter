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
ID   = 'SettingsRegionsGenerator'
NAME = 'Regions Generator'
DESC = "Regions generator settings"

PluginParams = (
    {
        'attr' : 'xc',
        'name' : "W",
        'desc' : "Determines the maximum region width in pixels (Bucket W/H is selected) or the number of regions in the horizontal direction (when Region Count is selected)",
        'type' : 'INT',
        'default' : 48,
    },
    {
        'attr' : 'yc',
        'name' : "H",
        'desc' : "Determines the maximum region height in pixels (Bucket W/H is selected) or the number of regions in the vertical direction (when Region Count is selected)",
        'type' : 'INT',
        'default' : 48,
    },
    {
        'attr' : 'xymeans',
        'name' : 'XY Means',
        'desc' : "Size in pixels or number of regions",
        'type' : 'ENUM',
        'items' : (
            ('0', "Region Count", ""),
            ('1', "Bucket W/H", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'seqtype',
        'desc' : "Determines the order in which the regions are rendered",
        'type' : 'ENUM',
        'items' : (
            ('0', "Top-Bottom", ""),
            ('1', "Left-Right", ""),
            ('2', "Checker", ""),
            ('3', "Spiral", ""),
            ('4', "Triangulation", ""),
            ('5', "Hilbert", ""),
        ),
        'default' : '4',
    },
    {
        'attr' : 'reverse',
        'desc' : "Reverses the region sequence order",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'dynbuckets',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },

    {
        'attr' : 'lock_size',
        'desc' : "Lock bucket size (X = Y)",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)

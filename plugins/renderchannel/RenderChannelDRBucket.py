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

TYPE = 'RENDERCHANNEL'
ID   = 'RenderChannelDRBucket'
NAME = 'DR Bucket'
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "",
        'type' : 'STRING',
        'default' : "DR",
    },
    {
        'attr' : 'text_alignment',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "Left", ""),
            ('1', "Center", ""),
            ('2', "Right", ""),
        ),
        'default' : '1',
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')
    layout.prop(propGroup, 'text_alignment')

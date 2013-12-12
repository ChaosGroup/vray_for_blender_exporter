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
ID   = 'RenderChannelExtraTex'
NAME = 'ExtraTex'
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "",
        'type' : 'STRING',
        'default' : NAME,
    },
    {
        'attr' : 'consider_for_aa',
        'name' : "Consider For AA",
        'desc' : "Consider this render element for antialiasing (may slow down rendering)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_matte_objects',
        'desc' : "Affect Matte Objects",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'texmap',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'filtering',
        'desc' : "Filtering",
        'type' : 'BOOL',
        'default' : True,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')

    layout.prop(propGroup, 'affect_matte_objects')
    layout.prop(propGroup, 'filtering')
    layout.prop(propGroup, 'consider_for_aa')

#
# V-Ray/Blender
#
# http://chaosgroup.com
#
# Author: Andrey M. Izrantsev (aka bdancer)
# E-Mail: izrantsev@cgdo.ru
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

import bpy

from vb30.lib import ExportUtils


TYPE = 'RENDERCHANNEL'
ID   = 'RenderChannelLightSelect'
NAME = 'Light Select'
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "Channel name",
        'type' : 'STRING',
        'default' : NAME,
    },
    {
        'attr' : 'color_mapping',
        'desc' : "Color Mapping",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'consider_for_aa',
        'name' : "Consider For AA",
        'desc' : "Consider this render element for antialiasing (may slow down rendering)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'filtering',
        'desc' : "Filtering",
        'type' : 'BOOL',
        'default' : False,
    },

    {
        'attr' : 'lights',
        'desc' : "Light list to appear in this channel",
        'type' : 'PLUGIN',
        'skip' : True,
        'default' : "",
    },
    {
        'attr' : 'type',
        'name' : "Type",
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('RAW',      "Raw",      ""),
            ('DIFFUSE',  "Diffuse",  ""),
            ('SPECULAR', "Specular", ""),
        ),
        'skip' : True,
        'default' : 'RAW',
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')
    layout.prop(propGroup, 'type')
    layout.prop(propGroup, 'color_mapping')
    layout.prop(propGroup, 'consider_for_aa')


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    o = bus['output']

    o.set(TYPE, 'RenderChannelColor', pluginName)
    o.writeHeader()
    ExportUtils.WritePluginParams(bus, pluginModule, pluginName, propGroup, overrideParams)
    o.writeFooter()

    return pluginName

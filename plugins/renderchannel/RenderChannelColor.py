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

import bpy

from vb30.lib import ExportUtils


TYPE = 'RENDERCHANNEL'
ID   = 'RenderChannelColor'
NAME = 'Color Channel'
DESC = "Generic render element"

ColorChannelNamesMenu = (
    ('1'  , "RGB", ""),
    ('101', "Diffuse", ""),
    ('102', "Reflection", ""),
    ('103', "Refraction", ""),
    ('104', "Self Illumination", ""),
    ('105', "Shadow", ""),
    ('106', "Specular", ""),
    ('107', "Lightning", ""),
    ('108', "GI", ""),
    ('109', "Caustics", ""),
    ('110', "Raw GI", ""),
    ('111', "Raw Lightning", ""),
    ('112', "Raw Shadow", ""),
    ('113', "Velocity", ""),
    ('118', "Reflection Filter", ""),
    ('119', "Raw Reflection", ""),
    ('120', "Refraction Filter", ""),
    ('121', "Raw Refraction", ""),
    ('122', "Real Color", ""),
    ('124', "Background", ""),
    ('125', "Alpha", ""),
    ('126', "Color", ""),
    ('127', "Wire Color", ""),
    ('128', "Matte Shadow", ""),
    ('129', "Total Lightning", ""),
    ('130', "Raw Total Lightning", ""),
    ('131', "Bump Normal", ""),
    ('132', "Samplerate", ""),
    ('133', "SSS", ""),
    ('115', "Material ID", ""),
    ('100', "Atmosphere", ""),
)

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "Channel name",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'color_mapping',
        'desc' : "Color Mapping",
        'type' : 'BOOL',
        'default' : True,
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
        'default' : True,
    },
    {
        'attr' : 'alias',
        'name' : "Type",
        'desc' : "",
        'type' : 'ENUM',
        'items' : ColorChannelNamesMenu,
        'default' : '101',
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')
    layout.prop(propGroup, 'alias')
    layout.prop(propGroup, 'color_mapping')
    layout.prop(propGroup, 'consider_for_aa')
    layout.prop(propGroup, 'filtering')


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    if not propGroup.name:
        overrideParams['name'] = ColorChannelNames[propGroup.alias].replace(" ", "")

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

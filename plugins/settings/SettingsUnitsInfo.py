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


TYPE = 'SETTINGS'
ID   = 'SettingsUnitsInfo'
NAME = 'SettingsUnitsInfo'
DESC = ""

PluginParams = (
    {
        'attr' : 'meters_scale',
        'desc' : "The number by which a 3d distance must be multiplied to covert it into meters",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'photometric_scale',
        'desc' : "The number by which the power of photometric lights should be scaled when rendering",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'scene_upDir',
        'desc' : "The 'up' direction for the scene",
        'type' : 'VECTOR',
        'default' : (0, 0, 1),
    },
    {
        'attr' : 'seconds_scale',
        'desc' : "The number by which a scene time unit must be multiplied to convert it to seconds",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    unit_settings = bpy.context.scene.unit_settings

    if unit_settings.system != 'NONE':
        overrideParams['meters_scale'] = unit_settings.scale_length

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

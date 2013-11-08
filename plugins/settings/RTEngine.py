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

from vb25.lib import ExportUtils


TYPE = 'SETTINGS'
ID   = 'RTEngine'
NAME = 'Realtime Engine'
DESC = "V-Ray Realtime Engine"

PluginParams = (
    {
        'attr' : 'enabled',
        'desc' : "Enable Realtime Engine",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_opencl',
        'name' : "Device",
        'desc' : "Device type",
        'type' : 'ENUM',
        'items' : (
            ('0', "CPU", ""),
            ('1', "GPU (Single)", ""),
            ('2', "GPU (Multi)", ""),
            ('4', "GPU (CUDA)", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'separate_window',
        'desc' : "Use a separate window for the Realtime Engine",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "use_opencl" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'enabled' : True if bus['scene'].render.engine == 'VRAY_RENDER_RT' else propGroup.enabled,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

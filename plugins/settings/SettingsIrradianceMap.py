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

from vb30.lib import ExportUtils
from vb30.lib import PluginUtils
from vb30 import debug

PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    VRayExporter = scene.vray.Exporter

    if propGroup.min_rate > propGroup.max_rate:
        debug.PrintInfo('Irradiance Map "Min. Rate" is more then "Max. Rate"!')

        overrideParams['min_rate'] = propGroup.max_rate
        overrideParams['max_rate'] = propGroup.min_rate

    if VRayExporter.draft:
        overrideParams['subdivs'] = propGroup.subdivs / 5.0

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

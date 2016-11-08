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


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter
    VRayDR       = VRayScene.VRayDR

    if VRayDR.on:
        if VRayDR.assetSharing == 'TRANSFER':
            overrideParams['misc_transferAssets'] = True

    propGroup = getattr(VRayScene, pluginName)
    attributes = sorted(pluginModule.PluginParams, key=lambda t: t['attr'])

    for attrDesc in attributes:
        key = attrDesc['attr']
        if key in propGroup and attrDesc['default'] != getattr(propGroup, key):
            overrideParams[key] = getattr(propGroup, key)

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

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
from vb30.lib import PluginUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def _updateSystemGamma(self, context):
    if self.sync_with_gamma:
        view_settings = context.scene.view_settings
        view_settings.gamma = 1.0 / self.gamma

# Inject update callback
for attrDesc in globals()['PluginParams']:
    if attrDesc['attr'] in {'gamma', 'sync_with_gamma'}:
        attrDesc['update'] = _updateSystemGamma


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    current_scene_cm = bpy.context.scene.vray.SettingsColorMapping

    if bus['preview'] and current_scene_cm.preview_use_scene_cm:
        # Use color mapping settings from current scene not from preview scene
        propGroup = current_scene_cm

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

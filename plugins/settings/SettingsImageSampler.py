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
from vb30.lib import BlenderUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']

    VRayScene = scene.vray
    SettingsDMCSampler = VRayScene.SettingsDMCSampler

    if propGroup.use_dmc_treshhold:
        overrideParams['dmc_threshold'] = SettingsDMCSampler.adaptive_threshold

    if propGroup.progressive_minSubdivs > propGroup.progressive_maxSubdivs:
        overrideParams['progressive_minSubdivs'] = propGroup.progressive_maxSubdivs
        overrideParams['progressive_maxSubdivs'] = propGroup.progressive_minSubdivs

    if propGroup.dmc_minSubdivs > propGroup.dmc_maxSubdivs:
        overrideParams['dmc_minSubdivs'] = propGroup.dmc_maxSubdivs
        overrideParams['dmc_maxSubdivs'] = propGroup.dmc_minSubdivs

    if propGroup.subdivision_minRate > propGroup.subdivision_maxRate:
        overrideParams['subdivision_minRate'] = propGroup.subdivision_maxRate
        overrideParams['subdivision_maxRate'] = propGroup.subdivision_minRate

    if propGroup.render_mask_mode == '2':
        ob_names = []
        if propGroup.render_mask_objects_selected:
            for obb in bpy.context.scene.object_bases:
                if obb.select:
                    ob_names.append(BlenderUtils.GetObjectName(obb.object))
        else:
            if propGroup.render_mask_objects:
                ob_names = BlenderUtils.GetGroupObjectsNames(propGroup.render_mask_objects)

        if not ob_names:
            overrideParams['render_mask_mode'] = '0'
        else:
            overrideParams['render_mask_objects'] = "List(%s)" % ",".join(ob_names)

    elif propGroup.render_mask_mode == '3':
        if not propGroup.render_mask_object_ids:
            overrideParams['render_mask_mode'] = '0'
        else:
            mask_object_ids = propGroup.render_mask_object_ids.split(";")
            overrideParams['render_mask_object_ids'] = "ListInt(%s)" % ",".join(mask_object_ids)

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

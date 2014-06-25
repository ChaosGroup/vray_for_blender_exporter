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

from vb30.plugins import PLUGINS
from vb30.lib     import ExportUtils


# Exports global render settings
# Must be called once before the object export
#
def ExportSettings(bus):
    scene = bus['scene']

    VRayScene       = scene.vray
    VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

    VRayExporter   = VRayScene.Exporter
    VRayDR         = VRayScene.VRayDR

    SettingsOutput = VRayScene.SettingsOutput
    SettingsGI     = VRayScene.SettingsGI

    for pluginType in {'SETTINGS', 'SETTINGS_GLOBAL'}:
        for pluginName in PLUGINS[pluginType]:
            if pluginName in {'BakeView',
                              'VRayStereoscopicSettings',
                              'SettingsPtexBaker',
                              'SettingsVertexBaker',
                              'SettingsCurrentFrame',
                              'SettingsLightTree',
                              'SettingsVRST',
                              'SettingsEnvironment'}:
                continue

            if pluginName in {'SettingsEXR',
                              'SettingsVFB'}:
                continue

            if pluginName in {'Includer'}:
                continue

            pluginModule = PLUGINS[pluginType][pluginName]

            propGroup      = None
            overrideParams = {}

            if pluginName == 'SettingsRegionsGenerator':
                propGroup = getattr(VRayScene, pluginName)

                overrideParams = {
                    'xc' : propGroup.xc,
                    'yc' : propGroup.xc if propGroup.lock_size else propGroup.yc,
                }
            elif pluginName.startswith('Filter'):
                continue
            elif pluginName in {'SphericalHarmonicsExporter', 'SphericalHarmonicsRenderer'}:
                propGroup = getattr(VRayScene, pluginName)

                if SettingsGI.primary_engine != '4':
                    continue

                if VRayExporter.spherical_harmonics == 'BAKE':
                    if pluginName == 'SphericalHarmonicsRenderer':
                        continue
                else:
                    if pluginName == 'SphericalHarmonicsExporter':
                        continue
            else:
                propGroup = getattr(VRayScene, pluginName)

            if not propGroup:
                continue

            ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

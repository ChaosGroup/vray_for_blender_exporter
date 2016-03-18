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

from vb30.plugins import PLUGINS, PLUGINS_ID
from vb30.lib     import ExportUtils
from vb30.lib     import SysUtils


# Exports global render settings
# Must be called once before the object export
#
ImageFormatPlugins = {
    'SettingsPNG',
    'SettingsJPEG',
    'SettingsTIFF',
    'SettingsTGA',
    'SettingsSGI',
    'SettingsEXR',
    'SettingsVRST',
}

def ExportSettingsPlugin(bus, pluginType, pluginName):
    scene = bus['scene']

    VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

    VRayScene = scene.vray
    VRayExporter   = VRayScene.Exporter
    VRayDR         = VRayScene.VRayDR
    SettingsOutput = VRayScene.SettingsOutput
    SettingsGI     = VRayScene.SettingsGI
    SettingsImageSampler = VRayScene.SettingsImageSampler

    pluginModule = PLUGINS_ID[pluginName]

    propGroup      = None
    overrideParams = {}

    if pluginName == 'SettingsRegionsGenerator':
        propGroup = getattr(VRayScene, pluginName)

        overrideParams = {
            'xc' : propGroup.xc,
            'yc' : propGroup.xc if propGroup.lock_size else propGroup.yc,
        }

    elif pluginName.startswith('Filter'):
        propGroup = getattr(VRayScene, pluginName)
        if SettingsImageSampler.filter_type != pluginName:
            return

    elif pluginName in {'SphericalHarmonicsExporter', 'SphericalHarmonicsRenderer'}:
        propGroup = getattr(VRayScene, pluginName)

        if SettingsGI.primary_engine != '4':
            return

        if VRayExporter.spherical_harmonics == 'BAKE':
            if pluginName == 'SphericalHarmonicsRenderer':
                return
        else:
            if pluginName == 'SphericalHarmonicsExporter':
                return
    else:
        propGroup = getattr(VRayScene, pluginName)

    if not propGroup:
        return

    ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)


def ExportSettings(bus):
    scene = bus['scene']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    for pluginType in {'SETTINGS', 'SETTINGS_GLOBAL'}:
        for pluginName in PLUGINS[pluginType]:
            # NOTE: We will export them later to be sure
            # they go after SettingsOutput
            if pluginName in ImageFormatPlugins:
                continue

            if pluginName in {
                # TODO: These plugins have to be implemented
                'SettingsPtexBaker',
                'SettingsVertexBaker',
                'SettingsImageFilter',
                # These plugins will be exported manually
                'Includer',
                'SettingsEnvironment',
                'OutputDeepWriter',
                # These plugins are exported from camera export
                'BakeView',
                'VRayStereoscopicSettings',
                # Unused plugins for now
                'SettingsCurrentFrame',
                'SettingsLightTree',
                'SettingsColorMappingModo',
                'SettingsDR',
                # Deprecated
                'SettingsPhotonMap',
            }:
                continue

            if not SysUtils.IsRTEngine(bus):
                if pluginName in {'RTEngine', 'SettingsRTEngine'}:
                    continue

            if not VRayScene.SettingsVFB.use:
                if pluginName in {'EffectLens'}:
                    continue

            ExportSettingsPlugin(bus, pluginType, pluginName)

    for pluginName in ImageFormatPlugins:
        ExportSettingsPlugin(bus, pluginType, pluginName)

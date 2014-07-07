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

from vb30.ui import classes as UiClasses


TYPE = 'UTILITIES'
ID   = 'VRayQuickSettings'
NAME = 'Quick Settings'
DESC = "Quick settings"


def recalculateValue(self, context):
    def GetValueInRange(val_pers, val_min, val_max):
        return val_min + (val_pers * (val_max - val_min))

    brute_force_min = 8
    brute_force_max = 64
    light_cache_min = 500
    light_cache_max = 3000
    shade_rate_max  = 64
    im_subdivs_min = 30
    im_subdivs_max = 150

    VRayScene = context.scene.vray

    SettingsGI            = VRayScene.SettingsGI
    SettingsImageSampler  = VRayScene.SettingsImageSampler
    SettingsDMCGI         = VRayScene.SettingsDMCGI
    SettingsLightCache    = VRayScene.SettingsLightCache
    SettingsIrradianceMap = VRayScene.SettingsIrradianceMap

    if self.presets == 'NONE':
        return

    # GI Quality
    #
    brute_force_subdivs = GetValueInRange(self.gi_quality, brute_force_min, brute_force_max)
    light_cache_subdivs = GetValueInRange(self.gi_quality, light_cache_min, light_cache_max)
    im_subdivs          = GetValueInRange(self.gi_quality, im_subdivs_min,  im_subdivs_max)

    if self.presets == 'EXTERIOR':
        SettingsDMCGI.subdivs = brute_force_subdivs

    elif self.presets == 'INTERIOR':
        SettingsIrradianceMap.subdivs = im_subdivs

    elif self.presets == 'STUDIO':
        SettingsDMCGI.subdivs      = brute_force_subdivs
        SettingsLightCache.subdivs = light_cache_subdivs

    # Shading Quality
    #
    SettingsImageSampler.min_shade_rate = self.shading_quality * (shade_rate_max - 1) + 1

    # AA Quality
    #
    SettingsImageSampler.dmc_maxSubdivs = self.aa_quality * (self.max_aa_subdivs - 1) + 1


def recalculatePreset(self, context):
    VRayScene = context.scene.vray
    SettingsGI = VRayScene.SettingsGI

    if self.presets == 'NONE':
        return

    elif self.presets == 'EXTERIOR':
        SettingsGI.on = True
        SettingsGI.primary_engine   = '2'
        SettingsGI.secondary_engine = '2'

        self.gi_quality = 0.0
        self.aa_quality = 0.01
        self.shading_quality = 0.32

    elif self.presets == 'INTERIOR':
        SettingsGI.on = True
        SettingsGI.primary_engine   = '0'
        SettingsGI.secondary_engine = '3'

        self.gi_quality = 0.0
        self.aa_quality = 0.03
        self.shading_quality = 0.0

    elif self.presets == 'VFX':
        SettingsGI.on = False
        SettingsGI.secondary_engine = '3'

        self.gi_quality = 0.0
        self.aa_quality = 0.01
        self.shading_quality = 0.04

    elif self.presets == 'STUDIO':
        SettingsGI.on = True
        SettingsGI.primary_engine   = '2'
        SettingsGI.secondary_engine = '3'

        self.gi_quality = 0.0
        self.aa_quality = 0.01
        self.shading_quality = 0.57


class VRayQuickSettings(bpy.types.PropertyGroup):
    presets = bpy.props.EnumProperty(
        name = "Presets",
        description = "",
        items = (
            ('NONE',     "None",       ""),
            ('EXTERIOR', "Arch. Ext.", "For architectural exteriors without too much bounced light"),
            ('INTERIOR', "Arch. Int.", "For architectural interiors where light bounces are important"),
            ('VFX',      "VFX",        "For VFX-style scenes which may not need global illumination"),
            ('STUDIO',   "Studio",     "For product design visualizations"),
        ),
        update = recalculatePreset,
        default = 'NONE'
    )

    gi_quality = bpy.props.FloatProperty(
        name = "GI Quality",
        description = "",
        subtype = 'PERCENTAGE',
        min = 0.0,
        max = 1.0,
        update = recalculateValue,
    )

    shading_quality = bpy.props.FloatProperty(
        name = "Shading Quality",
        description = "",
        subtype = 'PERCENTAGE',
        min = 0.0,
        max = 1.0,
        update = recalculateValue,
    )

    aa_quality = bpy.props.FloatProperty(
        name = "AA Quality",
        description = "",
        subtype = 'PERCENTAGE',
        min = 0.0,
        max = 1.0,
        update = recalculateValue,
    )

    max_aa_subdivs = bpy.props.IntProperty(
        name = "Max. AA Subdivs",
        description = "",
        min = 1,
        max = 1024,
        default = 25,
        update = recalculateValue,
    )


def GetRegClasses():
    return (
        VRayQuickSettings,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    setattr(bpy.types.VRayScene, 'VRayQuickSettings', bpy.props.PointerProperty(
        type =  VRayQuickSettings,
    ))


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

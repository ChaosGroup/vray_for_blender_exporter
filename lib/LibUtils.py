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

import re
import datetime
import struct
import uuid

import bpy
import mathutils

from . import PathUtils


LampSubType = {
    'AREA'  :  None,
    'HEMI'  :  None,
    'POINT' : 'omni_type',
    'SPOT'  : 'spot_type',
    'SUN'   : 'direct_type',
}

LampSubtypeToPlugin = {
    'AMBIENT' : 'LightAmbientMax',
    'DIRECT'  : 'LightDirectMax',
    'IES'     : 'LightIESMax',
    'OMNI'    : 'LightOmniMax',
    'SPHERE'  : 'LightSphere',
    'SPOT'    : 'LightSpotMax',
    'SUN'     : 'SunLight',
}

FormatToSettings = {
    '0' : 'SettingsPNG',
    '1' : 'SettingsJPEG',
    '2' : 'SettingsTIFF',
    '3' : 'SettingsTGA',
    '4' : 'SettingsSGI',
    '5' : 'SettingsEXR',
    '6' : 'SettingsVRST',
}


def GetUUID():
    return str(uuid.uuid1()).split("-")[0]


def GetLightPluginName(lamp):
    if lamp.type == 'HEMI':
        return 'LightDome'
    if lamp.type == 'AREA':
        return 'LightRectangle'
    return LampSubtypeToPlugin[getattr(lamp.vray, LampSubType[lamp.type])]


def GetLightPropGroup(lamp):
    return getattr(lamp.vray, GetLightPluginName(lamp))


def GetAsList(value):
    l = []
    if type(value) is list:
        l.extend(value)
    else:
        l.append(value)
    return l


# Strips string from deprecated chars
#
# NOTE: Some unicode conversion support?
#
def CleanString(s, stripSigns=True):
    if stripSigns:
        s = s.replace("+", "p")
        s = s.replace("-", "m")
    for i in range(len(s)):
        c = s[i]
        if c in "|@":
            continue
        if not ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')):
            s = s.replace(c, "_")
    return s


# This funciton will substitue special format sequences with
# the correspondent values
#
def GetDefFormatDict():
    blendFileName = None
    sceneName     = None
    cameraName    = None

    # During registration bpy.data is not yet ready
    if type(bpy.data) is bpy.types.BlendData:
        scene = bpy.context.scene

        # Blend-file name without extension
        blendFileName = PathUtils.GetFilename(bpy.data.filepath, ext=False) if bpy.data.filepath else "default"

        blendFileName = CleanString(blendFileName, stripSigns=False)
        sceneName     = CleanString(scene.name)
        cameraName    = CleanString(scene.camera.name) if scene.camera else None

    formatDict = {
        '$C': ("Camera Name", cameraName if cameraName else "CameraName"),
        '$S': ("Scene Name", sceneName),
        '$F': ("Blendfile Name", blendFileName),
    }

    return formatDict


def FormatVariablesDesc():
    FormatVariablesDict = GetDefFormatDict()

    format_vars = ["%s - %s" % (v, FormatVariablesDict[v][0]) for v in FormatVariablesDict]

    format_help = "; ".join(format_vars)
    format_help += "; Any time variable (see Python's \"datetime\" module help)"

    return format_help


def FormatName(s, formatDict=None):
    if not formatDict:
        formatDict = GetDefFormatDict()

    for v in formatDict:
        s = s.replace(v, formatDict[v][1])

    t = datetime.datetime.now()
    for v in re.findall("%\w", s):
        try:
            s = s.replace(v, t.strftime(v))
        except:
            pass

    return s


def GetPropGroup(parentID, propGroupPath):
    path = propGroupPath.split(".")
    propGroup = parentID
    for p in path:
        propGroup = getattr(propGroup, p)
    return propGroup

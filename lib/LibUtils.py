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

import datetime
import struct
import uuid

import bpy
import mathutils

import _vray_for_blender


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
    'PNG'  : 'SettingsPNG',
    'JPG'  : 'SettingsJPEG',
    'TIFF' : 'SettingsTIFF',
    'TGA'  : 'SettingsTGA',
    'SGI'  : 'SettingsSGI',
    'EXR'  : 'SettingsEXR',
    'VRST' : 'SettingsVRST',
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


# Return value in .vrscene format
#
def FormatValue(t, subtype=None, quotes=False, ascii=False):
    if type(t) is bool:
        return "%i"%(t)
    elif type(t) is int:
        return "%i"%(t)
    elif type(t) is float:
        return "%.6g"%(t)
    elif type(t) is mathutils.Matrix:
        if len(t.col) == 4:
            if ascii or bpy.context.scene.render.engine == 'VRAY_RENDER_RT':
                return "Transform(Matrix(Vector(%.6g,%f,%f),Vector(%.6g,%.6g,%.6g),Vector(%.6g,%.6g,%.6g)),Vector(%.12f,%.12f,%.12f))" % (t[0][0], t[1][0], t[2][0], t[0][1], t[1][1], t[2][1], t[0][2], t[1][2], t[2][2], t[0][3], t[1][3], t[2][3])
            return _vray_for_blender.getTransformHex(t.copy())
        else:
            return "Matrix(Vector(%.6g,%f,%f),Vector(%.6g,%.6g,%.6g),Vector(%.6g,%.6g,%.6g))" % (t[0][0], t[1][0], t[2][0], t[0][1], t[1][1], t[2][1], t[0][2], t[1][2], t[2][2])
    elif type(t) is mathutils.Vector:
        return "Vector(%.3g,%.3g,%.3g)" % (t.x,t.y,t.z)
    elif type(t) is mathutils.Color:
        if subtype:
            return "AColor(%.3g,%.3g,%.3g,1.0)" % (t.r,t.g,t.b)
        return "Color(%.3g,%.3g,%.3g)" % (t.r,t.g,t.b)
    elif type(t) is str:
        if t == "True":
            return "1"
        if t == "False":
            return "0"
    if quotes:
        return '"%s"' % t
    return t


# This funciton will substitue special format sequences with
# the correspondent values
#
def GetFormatVariablesDict(values):
    t = datetime.datetime.now()

    return (
        (r'%C',   "Camera Name", CleanString(values.get('camera_name', "")) if values else "CameraName"),
        (r'%S',   "Scene Name", CleanString(values.get('scene_name', "")) if values else "SceneName"),
        (r'%F',   "Blendfile Name", CleanString(values.get('blend_name', "render"), stripSigns=False) if values else "FileName"),
        (r'%T_H', "Hour (24-hour clock)", str(t.hour)),
        (r'%T_h', "Hour (12-hour clock)", t.strftime("%I%p")),
        (r'%T_M', "Minute", str(t.minute)),
        (r'%T_S', "Second", str(t.second)),
        (r'%T_d', "Day", str(t.day)),
        (r'%T_m', "Month (abbreviated name)", t.strftime("%b")),
        (r'%T_y', "Year", str(t.year)),
    )


def FormatVariablesDesc():
    FormatVariablesDict = GetFormatVariablesDict(None)

    format_vars = ["%s - %s" % (v[0], v[1]) for v in FormatVariablesDict]

    format_help = "Variables: "
    format_help += "; ".join(format_vars)

    return format_help


def FormatName(s, values):
    FormatVariablesDict = GetFormatVariablesDict(values)
    for v in FormatVariablesDict:
        s = s.replace(v[0], v[2])
    return s

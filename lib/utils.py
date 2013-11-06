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

import struct

import bpy
import mathutils

from . import paths


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

ObjectPrefix = {
    'LAMP'   : 'LA',
    'CAMERA' : 'CA',
}


def FilterObjectListByType(objectList, objectType):
    objectList = filter(lambda x: x.type == objectType, objectList)


def GetLightPluginName(lamp):
    if lamp.type == 'HEMI':
        return 'LightDome'
    if lamp.type == 'AREA':
        return 'LightRectangle'
    return LampSubtypeToPlugin[getattr(lamp.vray, LampSubType[lamp.type])]


def IsAnimated(ob):
    if ob.animation_data:
        return True
    if hasattr(ob, 'data') and ob.data:
        if ob.data.animation_data:
            return True
    return False


def CleanString(s, stripSigns=True):
    """
    Strip string from deprecated chars
    """
    if stripSigns:
        s = s.replace("+", "p")
        s = s.replace("-", "m")
    for i in range(len(s)):
        c = s[i]
        if not ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')):
            s = s.replace(c, "_")
    return s


def GetObjectName(ob, prefix=None):
    if prefix is None: 
        prefix = ObjectPrefix.get(ob.type, 'OB')
    name = prefix + ob.name
    if ob.library:
        name = 'LI' + paths.GetFilename(ob.library.filepath) + name
    return CleanString(name)


def GetGroupObjects(groupName):
    obList = []
    if groupName in bpy.data.groups:
        obList.extend(bpy.data.groups[groupName].objects)
    return obList


def GetGroupObjectsNames(groupName):
    obList = [GetObjectName(ob) for ob in GetGroupObjects(groupName)]
    return obList


def GetSmokeModifier(ob):
    if len(ob.modifiers):
        for md in ob.modifiers:
            if md.type == 'SMOKE' and md.smoke_type == 'DOMAIN':
                return md
    return None


def GetSceneObject(scene, objectName):
    if objectName not in scene.objects:
        return None
    return scene.objects[objectName]


# Helper function to convert a value to
# hex in vrscene format
def FormatHexValue(value):
    if type(value) is float:
        bytes = struct.pack('<f', value)
    else:
        bytes = struct.pack('<i', value)
    return ''.join([ "%02X" % b for b in bytes ])


# Helper function to convert mathutils.Vector to
# hex vector in vrscene format
def FormatHexVector(vector):
    return ''.join([ to_vrscene_hex(v) for v in vector ])


# Return value in .vrscene format
def FormatValue(t, subtype=None, quotes=False):
    if type(t) is bool:
        return "%i"%(t)
    elif type(t) is int:
        return "%i"%(t)
    elif type(t) is float:
        return "%.6f"%(t)
    elif type(t) is mathutils.Matrix:
        return "Transform(Matrix(Vector(%.6f,%f,%f),Vector(%.6f,%.6f,%.6f),Vector(%.6f,%.6f,%.6f)),Vector(%.12f,%.12f,%.12f))" % (t[0][0], t[1][0], t[2][0], t[0][1], t[1][1], t[2][1], t[0][2], t[1][2], t[2][2], t[0][3], t[1][3], t[2][3])
    elif type(t) is mathutils.Vector:
        return "Vector(%.3f,%.3f,%.3f)" % (t.x,t.y,t.z)
    elif type(t) is mathutils.Color:
        if subtype:
            return "AColor(%.3f,%.3f,%.3f,1.0)" % (t.r,t.g,t.b)
        return "Color(%.3f,%.3f,%.3f)" % (t.r,t.g,t.b)
    elif type(t) is str:
        if t == "True":
            return "1"
        if t == "False":
            return "0"
    if quotes:
        return '"%s"' % t
    return t


# Return animatable value in .vrscene format
def AnimatedValue(scene, value, quotes=False):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    frame = scene.frame_current
    
    if VRayExporter.camera_loop:
        frame = VRayExporter.customFrame

    val = FormatValue(value, quotes=quotes)

    if VRayScene.RTEngine.enabled and VRayScene.RTEngine.use_opencl:
        return val

    if not VRayExporter.animation and not VRayExporter.use_still_motion_blur:
        return val

    return "interpolate((%i,%s))" % (frame, val)

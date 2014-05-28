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

import os
import tempfile

import bpy

from . import LibUtils


ObjectPrefix = {
    'LAMP'   : 'LA',
    'CAMERA' : 'CA',
}


def SceneLampIt(scene, obType=None):
    for ob in scene.objects:
        if ob.type == 'LAMP':
            yield ob


def ObjectMaterialsIt(objects):
    for ob in objects:
        if not len(ob.material_slots):
            continue
        for ms in ob.material_slots:
            if not ms.material:
                continue
            yield ms.material


def ObjectTexturesIt(objects):
    for ob in objects:
        if not len(ob.material_slots):
            continue
        for ms in ob.material_slots:
            if not ms.material:
                continue
            for ts in ms.material.texture_slots:
                if ts and ts.texture:
                    yield ts.texture


def IsTexturePreview(scene):
    texPreviewOb = scene.objects.get('texture', None)
    if texPreviewOb and texPreviewOb.is_visible(scene):
        return texPreviewOb
    return None


def GetPreviewTexture(ob):
    if not len(ob.material_slots):
        return None
    if not ob.material_slots[0].material:
        return None
    ma = ob.material_slots[0].material
    if not len(ma.texture_slots):
        return None
    slot = ma.texture_slots[0]
    if not slot.texture:
        return None
    return slot.texture


def IsAnimated(o):
    if o.animation_data and o.animation_data.action:
        return True
    elif hasattr(o, 'parent') and o.parent:
        return IsAnimated(o.parent)
    return False


def IsDataAnimated(o):
    if not o.data:
        return False
    if o.data.animation_data and o.data.animation_data.action:
        return True
    return False


def GetObjectList(object_names_string=None, group_names_string=None):
    object_list = []

    if object_names_string:
        ob_names = object_names_string.split(';')
        for ob_name in ob_names:
            if ob_name in bpy.data.objects:
                object_list.append(bpy.data.objects[ob_name])

    if group_names_string:
        gr_names = group_names_string.split(';')
        for gr_name in gr_names:
            if gr_name in bpy.data.groups:
                object_list.extend(bpy.data.groups[gr_name].objects)

    dupliGroup = []
    for ob in object_list:
        if ob.dupli_type == 'GROUP' and ob.dupli_group:
            dupliGroup.extend(ob.dupli_group.objects)
    object_list.extend(dupliGroup)

    return object_list


def GetCameraHideLists(camera):
    VRayCamera = camera.data.vray

    visibility = {
        'all'     : set(),
        'camera'  : set(),
        'gi'      : set(),
        'reflect' : set(),
        'refract' : set(),
        'shadows' : set(),
    }

    if VRayCamera.hide_from_view:
        for hide_type in visibility:
            if getattr(VRayCamera, 'hf_%s' % hide_type):
                if getattr(VRayCamera, 'hf_%s_auto' % hide_type):
                    obList = GetObjectList(group_names_string='hf_%s' % camera.name)
                else:
                    obList = GetObjectList(getattr(VRayCamera, 'hf_%s_objects' % hide_type),
                                           getattr(VRayCamera, 'hf_%s_groups' % hide_type))
                for o in obList:
                    visibility[hide_type].add(o.as_pointer())

    return visibility


def GetEffectsExcludeList(scene):
    # TODO: Rewrite to nodes!
    #
    VRayScene = scene.vray
    exclude_list = []
    VRayEffects  = VRayScene.VRayEffects
    if VRayEffects.use:
        for effect in VRayEffects.effects:
            if effect.use:
                if effect.type == 'FOG':
                    EnvironmentFog = effect.EnvironmentFog
                    fog_objects = GetObjectList(EnvironmentFog.objects, EnvironmentFog.groups)
                    for ob in fog_objects:
                        if ob not in exclude_list:
                            exclude_list.append(ob.as_pointer())
    return exclude_list


def FilterObjectListByType(objectList, objectType):
    return filter(lambda x: x.type == objectType, objectList)


def GetObjectName(ob, prefix=None):
    if prefix is None:
        prefix = ObjectPrefix.get(ob.type, 'OB')
    name = prefix + ob.name
    if ob.library:
        name = 'LI' + paths.GetFilename(ob.library.filepath) + name
    return LibUtils.CleanString(name)


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


def GetDistanceObOb(ob1, ob2):
    t1 = ob1.matrix_world.translation
    t2 = ob2.matrix_world.translation
    d = t1 - t2
    return d.length


def GetUserConfigDir():
    userConfigDirpath = os.path.join(bpy.utils.user_resource('CONFIG'), "vrayblender")
    if not os.path.exists(userConfigDirpath):
        os.makedirs(userConfigDirpath)
    return userConfigDirpath


def ObjectOnVisibleLayers(scene, ob):
    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.activeLayers == 'ALL':
        return True

    activeLayers = scene.layers
    if VRayExporter.activeLayers == 'CUSTOM':
        activeLayers = VRayExporter.customRenderLayers

    for l in range(20):
        if ob.layers[l] and activeLayers[l]:
            return True

    return False


def ObjectVisible(bus, ob):
    scene = bus['scene']

    VRayScene = scene.vray
    VRayExporter    = VRayScene.Exporter
    SettingsOptions = VRayScene.SettingsOptions

    if not ObjectOnVisibleLayers(scene,ob):
        if ob.type == 'LAMP':
            if not SettingsOptions.light_doHiddenLights:
                return False
        if not SettingsOptions.geom_doHidden:
            return False

    if ob.hide_render:
        if ob.type == 'LAMP':
            if not SettingsOptions.light_doHiddenLights:
                return False
        if not SettingsOptions.geom_doHidden:
            return False

    return True


def IsPathRelative(path):
    return path.startswith("//")


def RelativePathValid(path):
    if not IsPathRelative(path):
        return True
    if bpy.data.filepath:
        return True
    return False


def GetFullFilepath(filepath, holder=None):
    fullFilepath = filepath

    if not IsPathRelative(filepath):
        fullFilepath = filepath

    elif not (holder and holder.library):
        if RelativePathValid(filepath):
            fullFilepath = bpy.path.abspath(filepath)
        else:
            fullFilepath = os.path.join(tempfile.gettempdir(), filepath[2:])

    else:
        # Path is from linked library and is relative
        # Remove "//"
        filepath = filepath[2:]

        # Use library dirpath as relative root
        libraryDirpath = os.path.dirname(bpy.path.abspath(holder.library.filepath))

        fullFilepath = os.path.normpath(os.path.join(libraryDirpath, filepath))

    fullFilepath = os.path.normpath(fullFilepath)

    return fullFilepath

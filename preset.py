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

import bpy

from vb30.plugins import PLUGINS, PLUGINS_ID

from vb30.lib import VRayStream
from vb30.lib import ExportUtils, SysUtils, LibUtils, PathUtils, BlenderUtils

from vb30.nodes import importing
from vb30.vray_tools.VRaySceneParser import ParseVrscene

from vb30 import debug


 ######  ######## ######## ######## #### ##    ##  ######    ######
##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##       ##          ##       ##     ##  ####  ## ##        ##
 ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
      ## ##          ##       ##     ##  ##  #### ##    ##        ##
##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
 ######  ########    ##       ##    #### ##    ##  ######    ######

PresetTypePlugins = {
    'gi' : (
        'SettingsGI',
        'SettingsLightCache',
        'SettingsDMCGI',
        'SettingsIrradianceMap',
        'SphericalHarmonicsRenderer',
        'SphericalHarmonicsExporter',
    ),
    'im' : (
        'SettingsIrradianceMap',
    ),
}

##     ## ######## ##    ## ##     ##    ########     ###     ######  ########
###   ### ##       ###   ## ##     ##    ##     ##   ## ##   ##    ## ##
#### #### ##       ####  ## ##     ##    ##     ##  ##   ##  ##       ##
## ### ## ######   ## ## ## ##     ##    ########  ##     ##  ######  ######
##     ## ##       ##  #### ##     ##    ##     ## #########       ## ##
##     ## ##       ##   ### ##     ##    ##     ## ##     ## ##    ## ##
##     ## ######## ##    ##  #######     ########  ##     ##  ######  ########

class VRayPresetMenuBase(bpy.types.Menu):
    def path_menu(self, searchpaths):
        filter_ext = lambda ext: ext.lower() == ".vrscene"

        if not searchpaths:
            self.layout.label("* No Preset Data *")

        files = []
        for directory in searchpaths:
            files.extend([(f, os.path.join(directory, f))
                          for f in os.listdir(directory)
                          if (not f.startswith("."))
                          if ((filter_ext is None) or
                              (filter_ext(os.path.splitext(f)[1])))
                          ])

        files.sort()

        for f, filepath in files:
            props = self.layout.operator("vray.preset_apply",
                                         text=bpy.path.display_name(f),
                                         translate=False)

            props.filepath    = filepath
            props.menu_idname = self.bl_idname

    def draw(self, context):
        presetPaths = {
            os.path.join(SysUtils.GetExporterPath(), "presets", self.preset_subdir),
            os.path.join(BlenderUtils.GetUserConfigDir(), "presets", self.preset_subdir),
        }

        paths = []
        for path in presetPaths:
            if os.path.exists(path):
                paths.append(path)

        self.path_menu(paths)


   ###    ########  ########  ##       ##    ##
  ## ##   ##     ## ##     ## ##        ##  ##
 ##   ##  ##     ## ##     ## ##         ####
##     ## ########  ########  ##          ##
######### ##        ##        ##          ##
##     ## ##        ##        ##          ##
##     ## ##        ##        ########    ##

class VRayPresetApply(bpy.types.Operator):
    bl_idname = "vray.preset_apply"
    bl_label = "Apply V-Ray preset"

    filepath = bpy.props.StringProperty(
        subtype = 'FILE_PATH',
        options = {'SKIP_SAVE'},
    )

    menu_idname = bpy.props.StringProperty(
        name        = "Menu ID Name",
        description = "ID name of the menu this was called from",
        options     = {'SKIP_SAVE'},
    )

    def execute(self, context):
        filepath = self.filepath

        # Сhange the menu title to the most recently chosen option
        preset_class = getattr(bpy.types, self.menu_idname)
        preset_class.bl_label = bpy.path.display_name(os.path.basename(filepath))

        # Apply preset
        #
        debug.PrintInfo('Applying preset from "%s"' % filepath)

        vrsceneDict = ParseVrscene(filepath)

        for pluginDesc in vrsceneDict:
            pluginID    = pluginDesc['ID']
            pluginName  = pluginDesc['Name']
            pluginAttrs = pluginDesc['Attributes']

            pluginModule = PLUGINS_ID.get(pluginID)
            if pluginModule is None:
                continue

            propGroup = getattr(context.scene.vray, pluginID)

            for attrName in pluginAttrs:
                attrDesc  = importing.getParamDesc(pluginModule.PluginParams, attrName)
                if attrDesc is None:
                    continue

                attrValue = pluginAttrs[attrName]
                if attrDesc['type'] == 'ENUM':
                    attrValue = str(attrValue)

                setattr(propGroup, attrName, attrValue)

        return {'FINISHED'}


   ###    ########  ########           ##    ########  ######## ##     ##  #######  ##     ## ########
  ## ##   ##     ## ##     ##         ##     ##     ## ##       ###   ### ##     ## ##     ## ##
 ##   ##  ##     ## ##     ##        ##      ##     ## ##       #### #### ##     ## ##     ## ##
##     ## ##     ## ##     ##       ##       ########  ######   ## ### ## ##     ## ##     ## ######
######### ##     ## ##     ##      ##        ##   ##   ##       ##     ## ##     ##  ##   ##  ##
##     ## ##     ## ##     ##     ##         ##    ##  ##       ##     ## ##     ##   ## ##   ##
##     ## ########  ########     ##          ##     ## ######## ##     ##  #######     ###    ########

class VRayPresetAddBase:
    name = bpy.props.StringProperty(
        name        = "Name",
        description = "Name of the preset, used to make the path name",
        maxlen      =  64,
        options     = {'SKIP_SAVE'},
        default     = ""
    )

    preset_menu = bpy.props.StringProperty(
        name    = "Preset Menu",
        options = {'SKIP_SAVE'},
    )

    remove_active = bpy.props.BoolProperty(
        default = False,
        options = {'HIDDEN', 'SKIP_SAVE'},
    )

    def draw(self, context):
        self.layout.prop(self, 'name')

    def invoke(self, context, event):
        if not self.remove_active:
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):
        preset_menu_class = getattr(bpy.types, self.preset_menu)
        preset_type = preset_menu_class.preset_subdir

        presetSubdir = PathUtils.CreateDirectory(os.path.join(BlenderUtils.GetUserConfigDir(), "presets"))
        exportPath   = PathUtils.CreateDirectory(os.path.join(presetSubdir, preset_type))

        presetName = preset_menu_class.bl_label if self.remove_active else self.name

        fileName = "%s.vrscene" % LibUtils.CleanString(bpy.path.display_name(presetName))

        outputFilepath = os.path.normpath(os.path.join(exportPath, fileName))

        if self.remove_active:
            # NOTE: Remove function is locked to user config directory,
            # so system settings are safe

            debug.PrintInfo('Removing preset file: "%s"' % outputFilepath)
            if not os.path.exists(outputFilepath):
                return {'CANCELLED'}
            try:
                os.remove(outputFilepath)
            except:
                debug.PrintError('Error removing preset file: "%s"!' % outputFilepath)

            # Set default menu name
            preset_menu_class.bl_label = bpy.path.display_name(preset_type)

        else:
            bus = {
                'output' : VRayStream.VRaySimplePluginExporter(outputFilepath),
                'scene'  : context.scene,
                'camera' : context.scene.camera,
            }

            pluginPresetIDs = None
            if preset_type == 'global':
                pluginPresetIDs = (pID for pID in sorted(PLUGINS['SETTINGS']))
            else:
                pluginPresetIDs = PresetTypePlugins[preset_type]

            for pluginID in pluginPresetIDs:
                pluginModule = PLUGINS_ID.get(pluginID)
                if pluginModule is None:
                    continue

                if not hasattr(context.scene.vray, pluginID):
                    continue

                propGroup = getattr(context.scene.vray, pluginID)

                ExportUtils.WritePlugin(bus, pluginModule, pluginID.lower(), propGroup, {})

        return {'FINISHED'}


##     ## ######## ##    ## ##     ##
###   ### ##       ###   ## ##     ##
#### #### ##       ####  ## ##     ##
## ### ## ######   ## ## ## ##     ##
##     ## ##       ##  #### ##     ##
##     ## ##       ##   ### ##     ##
##     ## ######## ##    ##  #######

class VRayPresetMenuGlobal(VRayPresetMenuBase):
    bl_label      = "Global Presets"
    preset_subdir = "global"


class VRayPresetAddGlobal(VRayPresetAddBase, bpy.types.Operator):
    bl_idname      = "vray.preset_add_global"
    bl_label       = "Save Global Preset"
    bl_description = "Save global preset"

    def __init__(self):
        self.preset_menu = 'VRayPresetMenuGlobal'


class VRayPresetMenuGI(VRayPresetMenuBase):
    bl_label      = "GI Presets"
    preset_subdir = "gi"


class VRayPresetAddGI(VRayPresetAddBase, bpy.types.Operator):
    bl_idname      = "vray.preset_add_gi"
    bl_label       = "Save Global Preset"
    bl_description = "Save global preset"

    def __init__(self):
        self.preset_menu = 'VRayPresetMenuGlobal'


class VRayPresetMenuIM(VRayPresetMenuBase):
    bl_label        = "Irradiance Map Presets"
    preset_subdir   = "im"


########  ########     ###    ##      ##
##     ## ##     ##   ## ##   ##  ##  ##
##     ## ##     ##  ##   ##  ##  ##  ##
##     ## ########  ##     ## ##  ##  ##
##     ## ##   ##   ######### ##  ##  ##
##     ## ##    ##  ##     ## ##  ##  ##
########  ##     ## ##     ##  ###  ###

def PresetBase(layout, menuName, menuOperator):
    menuClass = getattr(bpy.types, menuName)

    row = layout.row(align=True)
    row.menu(menuName, text=menuClass.bl_label)
    row.operator(menuOperator, text="", icon="ZOOMIN")
    row.operator(menuOperator, text="", icon="ZOOMOUT").remove_active = True
    layout.separator()


def WidgetPresetGlobal(layout):
    PresetBase(layout, 'VRayPresetMenuGlobal', "vray.preset_add_global")


def WidgetPresetGI(layout):
    PresetBase(layout, 'VRayPresetMenuGI', "vray.preset_add_gi")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayPresetAddGlobal,
        VRayPresetMenuGlobal,

        VRayPresetAddGI,
        VRayPresetMenuGI,

        VRayPresetMenuIM,

        VRayPresetApply,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

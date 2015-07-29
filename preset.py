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

from vb30.vray_tools.VRaySceneParser import ParseVrscene

from vb30.lib import VRayStream
from vb30.lib import ExportUtils, SysUtils, LibUtils, PathUtils, BlenderUtils

from vb30.nodes import importing as NodesImport
from vb30.nodes import tools     as NodesTools
from vb30.nodes import export    as NodesExport
from vb30.nodes import sockets   as NodesSockets

from vb30.ui import classes

from vb30 import debug

import _vray_for_blender


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
    preset_operator = None

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
            props = self.layout.operator(self.preset_operator,
                                         text=bpy.path.display_name(f),
                                         translate=False)

            props.filepath    = filepath
            props.menu_idname = self.bl_idname

    def draw(self, context):
        presetPaths = {
            os.path.join(SysUtils.GetExporterPath(), "presets", self.preset_subdir),
            os.path.join(SysUtils.GetUserConfigDir(), "presets", self.preset_subdir),
        }

        paths = []
        for path in presetPaths:
            if os.path.exists(path):
                paths.append(path)

        if hasattr(self, 'menu_item_save') and self.menu_item_save:
            op = self.layout.operator('vray.export_asset', text="Save Selected", icon='FILE_TICK')
            op.asset_type = self.preset_subdir
            self.layout.separator()

        self.path_menu(paths)


   ###    ########  ########  ##       ##    ##
  ## ##   ##     ## ##     ## ##        ##  ##
 ##   ##  ##     ## ##     ## ##         ####
##     ## ########  ########  ##          ##
######### ##        ##        ##          ##
##     ## ##        ##        ##          ##
##     ## ##        ##        ########    ##

class VRayPresetExecuteBase:
    filepath = bpy.props.StringProperty(
        subtype = 'FILE_PATH',
        options = {'SKIP_SAVE'},
    )

    menu_idname = bpy.props.StringProperty(
        name        = "Menu ID Name",
        description = "ID name of the menu this was called from",
        options     = {'SKIP_SAVE'},
    )

    def _execute(self, context, vrsceneDict):
        return {'FINISHED'}

    def execute(self, context):
        filepath = self.filepath

        # Сhange the menu title to the most recently chosen option
        preset_class = getattr(bpy.types, self.menu_idname)
        preset_class.bl_label = bpy.path.display_name(os.path.basename(filepath))

        # Apply preset
        #
        debug.PrintInfo('Applying preset from "%s"' % filepath)

        vrsceneDict = ParseVrscene(filepath)

        return self._execute(context, vrsceneDict)


class VRayPresetApply(VRayPresetExecuteBase, bpy.types.Operator):
    bl_idname = "vray.preset_apply"
    bl_label = "Apply V-Ray preset"

    def _execute(self, context, vrsceneDict):
        for pluginDesc in vrsceneDict:
            pluginID    = pluginDesc['ID']
            pluginName  = pluginDesc['Name']
            pluginAttrs = pluginDesc['Attributes']

            pluginModule = PLUGINS_ID.get(pluginID)
            if pluginModule is None:
                continue

            if not hasattr(context.scene.vray, pluginID):
                # TODO: Add warning?
                continue

            propGroup = getattr(context.scene.vray, pluginID)

            for attrName in pluginAttrs:
                attrDesc  = NodesImport.getParamDesc(pluginModule.PluginParams, attrName)
                if attrDesc is None:
                    continue

                attrValue = pluginAttrs[attrName]
                if attrDesc['type'] == 'ENUM':
                    attrValue = str(attrValue)

                setattr(propGroup, attrName, attrValue)

        return {'FINISHED'}


class VRayPresetApplyNode(VRayPresetExecuteBase, bpy.types.Operator):
    bl_idname = "vray.preset_node_apply"
    bl_label = "Apply V-Ray node preset"

    def _execute(self, context, vrsceneDict):
        space = context.space_data
        ntree = space.edit_tree

        # Deselect before import
        NodesTools.deselectNodes(ntree)

        # Get fake asset node
        assetDesc = NodesImport.getPluginByType(vrsceneDict, "Asset")
        assetType = assetDesc['Name']

        # Import template
        lastNode = None

        if assetType == 'Material':
            maName = assetDesc['Attributes']['material']
            maDesc = NodesImport.getPluginByName(vrsceneDict, maName)

            maNode = NodesImport.createNode(ntree, None, vrsceneDict, maDesc)

            # NOTE: Depends on how user saves the preset
            if 'Material' not in maNode.outputs:
                lastNode = maNode

            else:
                outputNode = ntree.nodes.new('VRayNodeOutputMaterial')
                ntree.links.new(maNode.outputs['Material'], outputNode.inputs['Material'])
                lastNode = outputNode

        elif assetType == 'Texture':
            texName = assetDesc['Attributes']['texture']
            texDesc = NodesImport.getPluginByName(vrsceneDict, texName)

            lastNode = NodesImport.createNode(ntree, None, vrsceneDict, texDesc)

        elif assetType == 'Channel':
            chanNames = assetDesc['Attributes']['channel']
            if len(chanNames):
                channContainer = ntree.nodes.new('VRayNodeRenderChannels')

                for i,chanName in enumerate(reversed(chanNames)):
                    chanSockName = "Channel %i" % i
                    NodesSockets.AddInput(channContainer, 'VRaySocketRenderChannel', chanSockName)

                    chanDesc = NodesImport.getPluginByName(vrsceneDict, chanName)
                    chanNode = NodesImport.createNode(ntree, None, vrsceneDict, chanDesc)

                    ntree.links.new(chanNode.outputs['Channel'], channContainer.inputs[chanSockName])

                lastNode = channContainer

        if lastNode:
            NodesTools.rearrangeTree(ntree, lastNode)

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

        presetSubdir = PathUtils.CreateDirectory(os.path.join(SysUtils.GetUserConfigDir(), "presets"))
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
    preset_operator = "vray.preset_apply"

class VRayPresetAddGlobal(VRayPresetAddBase, bpy.types.Operator):
    bl_idname      = "vray.preset_add_global"
    bl_label       = "Save Global Preset"
    bl_description = "Save global preset"

    def __init__(self):
        self.preset_menu = 'VRayPresetMenuGlobal'


class VRayPresetMenuGI(VRayPresetMenuBase):
    bl_label      = "GI Presets"
    preset_subdir = "gi"
    preset_operator = "vray.preset_apply"


class VRayPresetAddGI(VRayPresetAddBase, bpy.types.Operator):
    bl_idname      = "vray.preset_add_gi"
    bl_label       = "Save GI Preset"
    bl_description = "Save GI preset"

    def __init__(self):
        self.preset_menu = 'VRayPresetMenuGI'


class VRayPresetMenuIM(VRayPresetMenuBase):
    bl_label        = "Irradiance Map Presets"
    preset_subdir   = "im"
    preset_operator = "vray.preset_apply"


class VRayPresetMenuNodeBase(VRayPresetMenuBase):
    preset_operator = "vray.preset_node_apply"


class VRayPresetMenuNodeTexture(VRayPresetMenuNodeBase):
    bl_label        = "Texture"
    preset_subdir   = "texture"
    menu_item_save  = True


class VRayPresetMenuNodeMaterial(VRayPresetMenuNodeBase):
    bl_label        = "Material"
    preset_subdir   = "material"
    menu_item_save  = True


class VRayPresetMenuNodeRenderChannel(VRayPresetMenuNodeBase):
    bl_label        = "Render Channel"
    preset_subdir   = "channel"
    menu_item_save  = True


class VRayPresetMenuNodeEffects(VRayPresetMenuNodeBase):
    bl_label        = "Effects"
    preset_subdir   = "effects"
    menu_item_save  = True


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


class VRayNodeTemplatesSubMenus(bpy.types.Menu):
    bl_idname = "VRayNodeTemplatesSubMenus"
    bl_label  = "Templates"

    def draw(self, context):
        self.layout.menu("VRayPresetMenuNodeMaterial", icon='MATERIAL')
        self.layout.menu("VRayPresetMenuNodeTexture",  icon='TEXTURE')
        self.layout.menu("VRayPresetMenuNodeRenderChannel", icon='SCENE_DATA')
        self.layout.menu("VRayPresetMenuNodeEffects", icon='GHOST_ENABLED')


def VRayNodeTemplatesMenu(self, context):
    if classes.PollTreeType(None, context):
        self.layout.menu("VRayNodeTemplatesSubMenus", icon='NODETREE')


   ###     ######   ######  ######## ########
  ## ##   ##    ## ##    ## ##          ##
 ##   ##  ##       ##       ##          ##
##     ##  ######   ######  ######      ##
#########       ##       ## ##          ##
##     ## ##    ## ##    ## ##          ##
##     ##  ######   ######  ########    ##

class VRayNodeExportAsset(bpy.types.Operator):
    bl_idname      = "vray.export_asset"
    bl_label       = "Export Node Asset"
    bl_description = ""

    asset_name = bpy.props.StringProperty(
        name        = "Name",
        description = "Name of the asset, used to make the path name",
        maxlen      =  64,
        options     = {'SKIP_SAVE'},
        default     = ""
    )

    asset_type = bpy.props.EnumProperty(
        name        = "Type",
        description = "Type of the asset, used to make menu name",
        items = (
            ('texture',  "Texture",  ""),
            ('material', "Material", ""),
            ('channel',  "Render Channel", ""),
            ('effects',  "Effects", ""),
        ),
        default = "texture"
    )

    def draw(self, context):
        self.layout.prop(self, 'asset_name')
        self.layout.prop(self, 'asset_type')

    def invoke(self, context, event):
        if len(context.selected_nodes) > 1:
            self.report({'ERROR'}, "Select only one last node!")
            return {'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if not self.asset_name:
            self.report({'ERROR'}, "Asset name is not set!")
            return {'CANCELLED'}

        presetsPath       = PathUtils.CreateDirectory(os.path.join(SysUtils.GetUserConfigDir(), "presets"))
        userNodeAssetPath = PathUtils.CreateDirectory(os.path.join(presetsPath, self.asset_type))

        fileName = "%s.vrscene" % LibUtils.CleanString(bpy.path.display_name(self.asset_name))

        outputFilepath = os.path.normpath(os.path.join(userNodeAssetPath, fileName))

        # Create exporter (output)
        o = VRayStream.VRaySimplePluginExporter(outputFilepath)

        exporter = _vray_for_blender.init(
            engine  = 0,
            context = bpy.context.as_pointer(),
            scene   = bpy.context.scene.as_pointer(),
            data    = bpy.data.as_pointer(),

            mainFile     = o.output,
            objectFile   = o.output,
            envFile      = o.output,
            geometryFile = o.output,
            lightsFile   = o.output,
            materialFile = o.output,
            textureFile  = o.output,

            drSharePath = "",
        )

        # Get selected nodes
        ntree        = context.space_data.edit_tree
        selectedNode = context.selected_nodes[0]

        if selectedNode.bl_idname == 'VRayNodeRenderChannels':
            pluginNames = []

            for inSock in selectedNode.inputs:
                pluginNames.append(NodesExport.WriteConnectedNode(None, ntree, inSock))

            pluginName = "List(%s)" % ",".join(pluginNames)

        else:
            if selectedNode.bl_idname == 'VRayNodeOutputMaterial':
                selectedNode = NodesExport.GetConnectedNode(ntree, selectedNode.inputs['Material'])

            pluginName = _vray_for_blender.exportNode(
                ntree.as_pointer(),
                selectedNode.as_pointer(),
                None
            )

        # Write fake Asset node
        o.set('MAIN', 'Asset', self.asset_type.capitalize())
        o.writeHeader()
        o.writeAttibute(self.asset_type, pluginName)
        o.writeFooter()
        o.done()

        _vray_for_blender.exit(exporter)

        return {'FINISHED'}


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
        VRayPresetApplyNode,

        VRayPresetMenuNodeEffects,
        VRayPresetMenuNodeRenderChannel,
        VRayPresetMenuNodeTexture,
        VRayPresetMenuNodeMaterial,
        VRayNodeTemplatesSubMenus,

        VRayNodeExportAsset,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.NODE_MT_add.append(VRayNodeTemplatesMenu)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.NODE_MT_add.remove(VRayNodeTemplatesMenu)

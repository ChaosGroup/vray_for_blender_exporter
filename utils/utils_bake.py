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

from vb30.ui import classes
from vb30.lib import LibUtils
from vb30 import debug


SettingsBackup = {}


def ValueBackup(propGroup, attrName):
    global SettingsBackup

    propGroupName = propGroup.bl_rna.name

    if propGroupName not in SettingsBackup:
        SettingsBackup[propGroupName] = {}

    SettingsBackup[propGroupName][attrName] = getattr(propGroup, attrName)


def ValueRestore(propGroup, attrName):
    global SettingsBackup

    propGroupName = propGroup.bl_rna.name

    setattr(propGroup, attrName, SettingsBackup[propGroupName][attrName])


class VRayBatchBakeItem(bpy.types.PropertyGroup):
    ob  = bpy.props.PointerProperty(
        type = bpy.types.Object
    )

    use = bpy.props.BoolProperty(
        default = True
    )


class VRAY_UL_BakeRenderItem(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, 'use', text="")
        sub = row.column()
        sub.active = item.use
        if item.ob:
            sub.label(item.ob.name, icon='OBJECT_DATA')
        else:
            sub.label("Object not found!", icon='ERROR')


class VRayPropGroupMultiBakeSmartUVProject(bpy.types.PropertyGroup):
    angle_limit = bpy.props.FloatProperty(
            name="Angle Limit",
            description="Lower for more projection groups, higher for less distortion",
            min=1.0, max=89.0,
            default=66.0,
    )

    island_margin = bpy.props.FloatProperty(
            name="Island Margin",
            description="Margin to reduce bleed from adjacent islands",
            min=0.0, max=1.0,
            default=0.0,
    )

    user_area_weight = bpy.props.FloatProperty(
            name="Area Weight",
            description="Weight projections vector by faces with larger areas",
            min=0.0, max=1.0,
            default=0.0,
    )

    use_aspect = bpy.props.BoolProperty(
            name="Correct Aspect",
            description="Map UVs taking image aspect ratio into account",
            default=True
    )


class VRayPropGroupMultiBakeLightmapPackProject(bpy.types.PropertyGroup):
    PREF_BOX_DIV = bpy.props.IntProperty(
            name="Pack Quality",
            description="Pre Packing before the complex boxpack",
            min=1, max=48,
            default=12,
    )

    PREF_MARGIN_DIV = bpy.props.FloatProperty(
            name="Margin",
            description="Size of the margin as a division of the UV",
            min=0.001, max=1.0,
            default=0.1,
    )


class VRayPropGroupMultiBake(bpy.types.PropertyGroup):
    work_mode = bpy.props.EnumProperty(
        name        = "Mode",
        description = "Bake mode",
        items       = (
            ('SELECTION', "Selection", "Bake selected objects"),
            ('LIST',      "List",      "Bake objects from list"),
        ),
        default     = 'SELECTION'
    )

    uv_map = bpy.props.EnumProperty(
        name        = "UV Map",
        description = "UV map to use",
        items       = (
            ('UV_DEFAULT',   "Default", "Use first found UV map"),
            ('UV_VRAYBAKE',  "\"VRayBake\"", "Use map with name \"VRayBake\""),
            ('UV_NEW_SMART', "Add UV Map: Smart UV Project", "Add \"Smart UV Project\" projection (adds \"VRayBakeSmart\")"),
            ('UV_NEW_LM',    "Add UV Map: Lightmap Pack", "Add \"Lightmap Pack\" projection (adds \"VRayBakeLightmap\")"),
        ),
        default     = 'UV_DEFAULT'
    )

    output_dirpath = bpy.props.StringProperty(
        name    = "Directory Path",
        subtype = 'DIR_PATH',
        default = "//bake_$F",
        description = "Output directory (Variables: %s; $O - Object name)" % LibUtils.FormatVariablesDesc()
    )

    output_filename = bpy.props.StringProperty(
        name    = "File Name",
        default = "bake_$O",
        description = "Output filename (Variables: %s; $O - Object name)" % LibUtils.FormatVariablesDesc()
    )

    smart_uv = bpy.props.PointerProperty(
        type =  VRayPropGroupMultiBakeSmartUVProject,
    )

    lightmap_uv = bpy.props.PointerProperty(
        type =  VRayPropGroupMultiBakeLightmapPackProject,
    )

    list_items = bpy.props.CollectionProperty(
        type = VRayBatchBakeItem
    )

    list_item_selected = bpy.props.IntProperty(
        default = -1,
        min     = -1,
        max     = 100
    )


class VRayOpBatchBakeAddItems(bpy.types.Operator):
    bl_idname      = 'vray.batch_bake_add_selection'
    bl_label       = "Add Selection"
    bl_description = "Add selected objects to baking list"

    def execute(self, context):
        VRayScene = context.scene.vray
        BatchBake = VRayScene.BatchBake

        for ob in context.selected_objects:
            if ob.type not in {'MESH'}:
                continue

            addOb = True
            for item in BatchBake.list_items:
                if ob == item.ob:
                    addOb = False
                    break

            if addOb:
                BatchBake.list_items.add()
                BatchBake.list_items[-1].ob = ob

        BatchBake.list_item_selected = len(BatchBake.list_items) - 1

        return {'FINISHED'}


class VRAY_PT_Bake(classes.VRayRenderPanel):
    bl_label = "Bake"
    bl_panel_groups = classes.PanelGroups

    @classmethod
    def poll_custom(cls, context):
        VRayBake = context.scene.vray.BakeView
        return VRayBake.use

    def draw(self, context):
        layout = self.layout

        VRayScene = context.scene.vray
        BatchBake = VRayScene.BatchBake
        VRayBake  = VRayScene.BakeView

        split = layout.split()
        row = split.row(align=True)
        row.operator("vray.batch_bake", icon='GROUP_UVS', text="Bake")
        row.prop(context.scene.render, "use_lock_interface", text="")
        layout.separator()

        layout.label("Mode:")
        layout.prop(BatchBake, 'work_mode', expand=True)

        if BatchBake.work_mode == 'LIST':
            layout.label("Objects To Bake:")
            classes.DrawListWidget(layout, context.scene, 'vray.BatchBake', 'VRAY_UL_BakeRenderItem',
                "Bake Object",
                itemAddOp='vray.batch_bake_add_selection')
        else:
            layout.separator()

        box = layout.box()
        box.label("Bake Settings:")
        box.prop(BatchBake, 'uv_map')
        if BatchBake.uv_map == 'UV_NEW_SMART':
            uvbox = box.box()
            uvbox.label("Smart UV Project Settings:")
            uvboxsplit = uvbox.split()
            uvboxcol = uvboxsplit.column(align=True)
            uvboxcol.prop(BatchBake.smart_uv, 'angle_limit')
            uvboxcol.prop(BatchBake.smart_uv, 'island_margin')
            uvboxcol.prop(BatchBake.smart_uv, 'user_area_weight')
            uvboxcol = uvboxsplit.column()
            uvboxcol.prop(BatchBake.smart_uv, 'use_aspect')
        elif BatchBake.uv_map == 'UV_NEW_LM':
            uvbox = box.box()
            uvbox.label("Lightmap Pack Settings:")
            uvboxsplit = uvbox.split()
            uvboxcol = uvboxsplit.column(align=True)
            uvboxcol.prop(BatchBake.lightmap_uv, 'PREF_BOX_DIV')
            uvboxcol.prop(BatchBake.lightmap_uv, 'PREF_MARGIN_DIV')

        box.separator()
        split = box.split()
        col = split.column()
        col.prop(VRayBake, 'dilation')
        col = split.column()
        col.prop(VRayBake, 'flip_derivs')
        col.prop(VRayBake, 'square_resolution')

        layout.separator()
        layout.prop(BatchBake, 'output_dirpath')
        layout.prop(BatchBake, 'output_filename')


def RestoreSettings(scene):
    global SettingsBackup

    VRayScene = scene.vray
    VRayScene.Exporter.wait = False

    for propGroupName in SettingsBackup:
        for attrName in SettingsBackup[propGroupName]:
            if hasattr(VRayScene, propGroupName):
                propGroup = getattr(VRayScene, propGroupName)
                if hasattr(propGroup, attrName):
                    setattr(propGroup, attrName, SettingsBackup[propGroupName][attrName])

    ValueRestore(VRayScene.Exporter, 'autoclose')
    ValueRestore(VRayScene.Exporter, 'auto_save_render')

    VRayScene.BakeView.uv_channel = 0
    VRayScene.BakeView.bake_node  = ""

    SettingsBackup = {}


def GetUVChannelIndex(ob, mapName):
    uv_idx = 0
    for uvMap in ob.data.uv_textures:
        if uvMap.name == mapName:
            return uv_idx
        uv_idx += 1
    return None


class VRayOpBatchBake(bpy.types.Operator):
    bl_idname      = "vray.batch_bake"
    bl_label       = "Batch Bake"
    bl_description = "Batch bake tool"

    def execute(self, context):
        VRayScene = context.scene.vray
        BatchBake = VRayScene.BatchBake
        VRayBake  = VRayScene.BakeView

        # Copy selection
        selection = [ob for ob in context.selected_objects]

        formatDict = LibUtils.GetDefFormatDict()

        obList = None
        if BatchBake.work_mode == 'SELECTION':
            obList = selection
        elif BatchBake.work_mode == 'LIST':
            obList = [item.ob for item in BatchBake.list_items if item.use and item.ob]

        numObjects = len(obList)

        # Backup some settings
        ValueBackup(VRayScene.SettingsOutput, 'img_dir')
        ValueBackup(VRayScene.SettingsOutput, 'img_file')
        ValueBackup(VRayScene.Exporter, 'autoclose')
        ValueBackup(VRayScene.Exporter, 'auto_save_render')

        if numObjects:
            VRayScene.Exporter.auto_save_render = True

            # We have to wait for render end
            # only if baking multiple objects
            if numObjects > 1:
                VRayScene.Exporter.wait = True
                VRayScene.Exporter.autoclose = True

            try:
                for ob in obList:
                    debug.PrintInfo("Baking: %s..." % ob.name)
                    VRayScene.Exporter.currentBakeObject = ob

                    # UV channel to use for baking
                    uv_channel = None

                    # Find UV map index
                    if BatchBake.uv_map == 'UV_DEFAULT':
                        if len(ob.data.uv_layers):
                            uv_channel = 0

                    elif BatchBake.uv_map == 'UV_VRAYBAKE':
                        uv_channel = GetUVChannelIndex(ob, "VRayBake")

                    # Add projection if need
                    elif BatchBake.uv_map.startswith('UV_NEW_'):
                        uvName = None
                        if BatchBake.uv_map == 'UV_NEW_SMART':
                            uvName = "VRayBakeSmart"
                        elif BatchBake.uv_map == 'UV_NEW_LM':
                            uvName = "VRayBakeLightmap"

                        uv_channel = GetUVChannelIndex(ob, uvName)
                        if uv_channel is None:
                            if ob.mode in {'EDIT'}:
                                bpy.ops.object.mode_set(mode='OBJECT')

                            bpy.ops.object.select_all(action='DESELECT')

                            ob.select = True
                            context.scene.objects.active = ob

                            if BatchBake.uv_map == 'UV_NEW_SMART':
                                bpy.ops.object.mode_set(mode='EDIT')
                                bpy.ops.mesh.select_all(action='SELECT')

                                layer = ob.data.uv_textures.new(name=uvName)
                                layer.active = True

                                bpy.ops.uv.smart_project(
                                    angle_limit      = BatchBake.smart_uv.angle_limit,
                                    island_margin    = BatchBake.smart_uv.island_margin,
                                    user_area_weight = BatchBake.smart_uv.user_area_weight,
                                )

                                bpy.ops.mesh.select_all(action='DESELECT')
                                bpy.ops.object.mode_set(mode='OBJECT')

                            elif BatchBake.uv_map == 'UV_NEW_LM':
                                bpy.ops.uv.lightmap_pack(
                                    PREF_CONTEXT     = 'ALL_FACES',
                                    PREF_NEW_UVLAYER = True,
                                    PREF_BOX_DIV     = BatchBake.lightmap_uv.PREF_BOX_DIV,
                                    PREF_MARGIN_DIV  = BatchBake.lightmap_uv.PREF_MARGIN_DIV,
                                )
                                ob.data.uv_textures[-1].name = uvName

                            uv_channel = len(ob.data.uv_textures) - 1

                    if uv_channel is None:
                        debug.PrintError("UV Map is not found!")
                        continue

                    # Bake settings
                    VRayScene.BakeView.bake_node  = ob.name
                    VRayScene.BakeView.uv_channel = uv_channel

                    # Setup vars
                    formatDict['$O'] = ("Object Name", LibUtils.CleanString(ob.name, stripSigns=False))

                    # Render
                    VRayScene.SettingsOutput.img_file = LibUtils.FormatName(BatchBake.output_filename, formatDict)
                    VRayScene.SettingsOutput.img_dir  = LibUtils.FormatName(BatchBake.output_dirpath,  formatDict)

                    bpy.ops.render.render()

            except Exception as e:
                debug.PrintError("Erorr baking objects!")
                debug.ExceptionInfo(e)

        # Restore selection
        for ob in selection:
            ob.select = True

        RestoreSettings(context.scene)

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
        VRayPropGroupMultiBakeSmartUVProject,
        VRayPropGroupMultiBakeLightmapPackProject,
        VRayBatchBakeItem,
        VRAY_UL_BakeRenderItem,
        VRayOpBatchBakeAddItems,
        VRayPropGroupMultiBake,
        VRayOpBatchBake,
        VRAY_PT_Bake,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.VRayScene.BatchBake = bpy.props.PointerProperty(
        name        = "V-Ray Batch Bake Settings",
        type        =  VRayPropGroupMultiBake,
        description = "V-Ray batch bake settings"
    )


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

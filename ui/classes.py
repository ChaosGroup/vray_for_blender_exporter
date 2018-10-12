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

from vb30.lib import LibUtils
from vb30.lib import DrawUtils
from vb30     import plugins


########  ######## ######## #### ##    ## ########  ######
##     ## ##       ##        ##  ###   ## ##       ##    ##
##     ## ##       ##        ##  ####  ## ##       ##
##     ## ######   ######    ##  ## ## ## ######    ######
##     ## ##       ##        ##  ##  #### ##             ##
##     ## ##       ##        ##  ##   ### ##       ##    ##
########  ######## ##       #### ##    ## ########  ######

VRayEngines = {
    'VRAY_RENDERER'
}

PanelGroups = {
    '0' : (
        'VRAY_RP_render',
        'VRAY_RP_cloud',
        'VRAY_RP_Device',
        'VRayPanelBake',
        'VRAY_RP_SettingsCaustics',
        'VRAY_RP_VRayStereoscopicSettings',
        'VRAY_RP_dimensions',
        'VRAY_RP_output',
    ),
    '1' : (
        'VRAY_RP_Globals',
        'VRAY_RP_displace',
        'VRAY_RP_cm',
    ),
    '2' : (
        'VRAY_RP_gi',
        'VRAY_RP_GI_sh',
        'VRAY_RP_GI_im',
        'VRAY_RP_GI_bf',
        'VRAY_RP_GI_lc',
    ),
    '3' : (
        'VRAY_RP_aa',
        'VRAY_RP_dmc',
    ),
    '4' : (
        'VRAY_RP_exporter',
        'VRAY_RP_dr',
        'VRAY_RP_SettingsSystem',
        'VRAY_RP_SettingsVFB',
    ),
}

narrowui = 200


##     ## ######## #### ##        ######
##     ##    ##     ##  ##       ##    ##
##     ##    ##     ##  ##       ##
##     ##    ##     ##  ##        ######
##     ##    ##     ##  ##             ##
##     ##    ##     ##  ##       ##    ##
 #######     ##    #### ########  ######

def TreeHasNodes(ntree):
    if not ntree:
        return False
    if not len(ntree.nodes):
        return False
    return True


def GetContextType(context):
    if hasattr(context, 'node'):
        return 'NODE'
    if hasattr(context, 'material'):
        return 'MATERIAL'
    return None


def GetRegionWidthFromContext(context):
    contextType = GetContextType(context)
    if contextType == 'NODE':
        return context.node.width
    elif hasattr(context, 'region'):
        return context.region.width
    # Assume wide region width
    return 1024


def PollBase(cls, context):
    poll_engine = context.scene.render.engine in cls.COMPAT_ENGINES
    poll_custom = True
    if hasattr(cls, 'poll_custom'):
        poll_custom = cls.poll_custom(context)
    poll_group = True
    if hasattr(cls, 'poll_group'):
        poll_group = cls.poll_group(context)
    return poll_engine and poll_custom and poll_group


def PollEngine(context):
    return context.scene.render.engine in VRayEngines


def PollTreeType(cls, context):
    is_vray      = PollEngine(context)
    is_vray_tree = context.space_data.tree_type.startswith('VRayNodeTree')
    return is_vray and is_vray_tree


########  ########     ###    ##      ##
##     ## ##     ##   ## ##   ##  ##  ##
##     ## ##     ##  ##   ##  ##  ##  ##
##     ## ########  ##     ## ##  ##  ##
##     ## ##   ##   ######### ##  ##  ##
##     ## ##    ##  ##     ## ##  ##  ##
########  ##     ## ##     ##  ###  ###

def DrawPluginUIAuto(context, layout, propGroup, pluginID):
    pluginModule = plugins.GetPluginByName(pluginID)

    if not pluginModule:
        Debug("Plugin \"%s\" module not found!" % pluginID)
        return

    if not hasattr(pluginModule, 'PluginWidget'):
        return

    DrawUtils.RenderTemplate(context, layout, propGroup, pluginModule)


def DrawPluginUI(context, layout, propGroupHolder, propGroup, pluginType, vrayPlugin):
    if hasattr(vrayPlugin, 'gui'):
        vrayPlugin.gui(context, layout, propGroup, propGroupHolder)
    if hasattr(vrayPlugin, 'PluginWidget'):
        DrawUtils.RenderTemplate(context, layout, propGroup, vrayPlugin)
    else:
        DrawUtils.Draw(context, layout, propGroup, vrayPlugin.PluginParams)


def DrawNodePanel(context, layout, node, PLUGINS):
    vrayPlugin = None
    toShow     = True

    if node.bl_idname.startswith('VRayNodeMeta'):
        node.draw_buttons_ext(context, layout)
        return

    if not hasattr(node, 'vray_type'):
        toShow = False
    else:
        if node.vray_type == 'NONE' or node.vray_plugin == 'NONE':
            toShow = False
        else:
            if not hasattr(node, node.vray_plugin):
                toShow = False
            pluginTypes = PLUGINS[node.vray_type]

            if node.vray_plugin in pluginTypes:
                vrayPlugin = pluginTypes[node.vray_plugin]

    if not toShow or not vrayPlugin:
        layout.label(text="Selected node has no attibutes to show...")
    else:
        layout.label(text="Node: %s" % node.name)
        layout.separator()

        propGroup = getattr(node, node.vray_plugin)

        DrawPluginUI(context, layout, node, propGroup, node.vray_plugin, vrayPlugin)


def NtreeWidget(layout, propGroup, label, addOp, addOpContext):
    split = layout.split(percentage=0.3)

    col = split.column()
    col.label("%s:" % label)

    col = split.column()
    row = col.row(align=True)

    if propGroup.ntree:
        op = row.operator("vray.nodetree_rename_to", icon='SYNTAX_OFF', text="")
        op.to_data = addOpContext
        op.ntree   = propGroup.ntree.name

        # op = row.operator("vray.select_ntree_in_editor", icon='UI', text="")
        # op.ntree = propGroup.ntree.name

    row.prop_search(propGroup, 'ntree', bpy.data, 'node_groups', text="")
    if not propGroup.ntree:
        row.operator(addOp, icon='ZOOMIN', text="")


def DrawListWidget(layout, parentID, propGroupPath, listType, defItemName, itemAddOp='DEFAULT', itemRenderFunc=None):
    listPropGroup = LibUtils.GetPropGroup(parentID, propGroupPath)

    row = layout.row()
    row.template_list(listType, "",
        listPropGroup, 'list_items',
        listPropGroup, 'list_item_selected',
        rows=5)

    col = row.column()
    sub = col.row()
    subsub = sub.column(align=True)
    if itemAddOp in {'DEFAULT'}:
        op = subsub.operator('vray.ui_list_item_add', icon="ZOOMIN", text="")
        op.list_parent   = parentID
        op.list_attr     = propGroupPath
        op.def_item_name = defItemName
    else:
        subsub.operator(itemAddOp, icon="ZOOMIN", text="")

    sub= col.row()
    op = subsub.operator('vray.ui_list_item_del', icon="ZOOMOUT", text="")
    op.list_parent = parentID
    op.list_attr   = propGroupPath
    subsub = sub.column(align=True)
    op = subsub.operator("vray.ui_list_item_up",   icon='TRIA_UP',   text="")
    op.list_parent = parentID
    op.list_attr   = propGroupPath
    op = subsub.operator("vray.ui_list_item_down", icon='TRIA_DOWN', text="")
    op.list_parent = parentID
    op.list_attr   = propGroupPath

    if itemRenderFunc:
        if listPropGroup.list_item_selected >= 0 and len(listPropGroup.list_items) > 0:
            listItem = listPropGroup.list_items[listPropGroup.list_item_selected]

            layout.separator()
            itemRenderFunc(layout, listItem)


########     ###     ######  ########     ######  ##          ###     ######   ######  ########  ######
##     ##   ## ##   ##    ## ##          ##    ## ##         ## ##   ##    ## ##    ## ##       ##    ##
##     ##  ##   ##  ##       ##          ##       ##        ##   ##  ##       ##       ##       ##
########  ##     ##  ######  ######      ##       ##       ##     ##  ######   ######  ######    ######
##     ## #########       ## ##          ##       ##       #########       ##       ## ##             ##
##     ## ##     ## ##    ## ##          ##    ## ##       ##     ## ##    ## ##    ## ##       ##    ##
########  ##     ##  ######  ########     ######  ######## ##     ##  ######   ######  ########  ######

class VRayPanel(bpy.types.Panel):
    COMPAT_ENGINES = VRayEngines

    @classmethod
    def poll(cls, context):
        return PollBase(cls, context)


class VRayDataPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'data'


class VRayGeomPanel(VRayDataPanel):
    incompatTypes  = {'LAMP', 'CAMERA', 'SPEAKER', 'ARMATURE', 'EMPTY', 'META'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type not in cls.incompatTypes and PollBase(cls, context)


class VRayCameraPanel(VRayDataPanel):
    @classmethod
    def poll(cls, context):
        return context.camera and PollBase(cls, context)


class VRayLampPanel(VRayDataPanel):
    @classmethod
    def poll(cls, context):
        return context.lamp and PollBase(cls, context)


class VRayMaterialPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'material'

    @classmethod
    def poll(cls, context):
        return context.material and PollBase(cls, context)


class VRayObjectPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'object'

    incompatTypes  = {'LAMP', 'CAMERA', 'SPEAKER', 'ARMATURE'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type not in cls.incompatTypes and PollBase(cls, context)


class VRayParticlePanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'particle'

    @classmethod
    def poll(cls, context):
        return context.particle_system and PollBase(cls, context)


class VRayRenderPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'render'

    @classmethod
    def poll_group(cls, context):
        VRayExporter = context.scene.vray.Exporter
        if not VRayExporter.ui_render_grouping:
            return True

        activeGroup = VRayExporter.ui_render_context
        if cls.__name__ in cls.bl_panel_groups[activeGroup]:
            return True

        return False


class VRayRenderLayersPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'render_layer'

    @classmethod
    def poll(cls, context):
        return PollBase(cls, context)


class VRayScenePanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'scene'

    @classmethod
    def poll(cls, context):
        return PollBase(cls, context)


class VRayTexturePanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'texture'

    @classmethod
    def poll(cls, context):
        return context.texture and PollBase(cls, context)


class VRayWorldPanel(VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'world'

    @classmethod
    def poll(cls, context):
        return context.world and PollBase(cls, context)


##       ####  ######  ########
##        ##  ##    ##    ##
##        ##  ##          ##
##        ##   ######     ##
##        ##        ##    ##
##        ##  ##    ##    ##
######## ####  ######     ##

class VRayOpListBase:
    list_parent   = bpy.props.PointerProperty(type=bpy.types.ID)
    list_attr     = bpy.props.StringProperty()
    def_item_name = bpy.props.StringProperty()


class VRayOpListItemNew(VRayOpListBase, bpy.types.Operator):
    bl_idname      = 'vray.ui_list_item_add'
    bl_label       = "Add Item"
    bl_description = "Add list item"

    def execute(self, context):
        listAttr = LibUtils.GetPropGroup(self.list_parent, self.list_attr)
        listAttr.list_items.add()
        listAttr.list_items[-1].name = self.def_item_name
        listAttr.list_item_selected = len(listAttr.list_items) - 1
        return {'FINISHED'}


class VRayOpListItemDel(VRayOpListBase, bpy.types.Operator):
    bl_idname      = 'vray.ui_list_item_del'
    bl_label       = "Delete Item"
    bl_description = "Delete list item"

    def execute(self, context):
        listAttr = LibUtils.GetPropGroup(self.list_parent, self.list_attr)

        if listAttr.list_item_selected >= 0:
           listAttr.list_items.remove(listAttr.list_item_selected)
           listAttr.list_item_selected -= 1

        if len(listAttr.list_items):
            if listAttr.list_item_selected < 0:
               listAttr.list_item_selected = 0
        else:
            listAttr.list_item_selected = -1

        return {'FINISHED'}


class VRayOpListItemUp(VRayOpListBase, bpy.types.Operator):
    bl_idname      = 'vray.ui_list_item_up'
    bl_label       = "Move Item Up"
    bl_description = "Move list item up"

    def execute(self, context):
        listAttr = LibUtils.GetPropGroup(self.list_parent, self.list_attr)
        if listAttr.list_item_selected <= 0:
            return {'CANCELLED'}

        listAttr.list_items.move(listAttr.list_item_selected,
                                 listAttr.list_item_selected-1)
        listAttr.list_item_selected -= 1

        return {'FINISHED'}


class VRayOpListItemDown(VRayOpListBase, bpy.types.Operator):
    bl_idname      = 'vray.ui_list_item_down'
    bl_label       = "Move Item Down"
    bl_description = "Move list item down"

    def execute(self, context):
        listAttr = LibUtils.GetPropGroup(self.list_parent, self.list_attr)
        if listAttr.list_item_selected < 0:
            return {'CANCELLED'}
        if listAttr.list_item_selected >= len(listAttr.list_items)-1:
            return {'CANCELLED'}

        listAttr.list_items.move(listAttr.list_item_selected,
                                 listAttr.list_item_selected+1)
        listAttr.list_item_selected += 1

        return {'FINISHED'}


# The draw_item function is called for each item of the collection that is visible in the list.
#   data is the RNA object containing the collection,
#   item is the current drawn item of the collection,
#   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
#     have custom icons ID, which are not available as enum items).
#   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
#     active item of the collection).
#   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
#   index is index of the current item in the collection.

class VRayListUse(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(item.name)
        layout.prop(item, 'use', text="")


class VRayList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(item.name)


class VRayListDR(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        port_override = ":%s" % item.port if item.port_override else ""

        layout.label("%s [%s%s]" % (item.name, item.address, port_override))
        layout.prop(item, 'use', text="")


class VRayListMaterialSlots(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob   = data
        slot = item
        ma   = slot.material

        split = layout.split(percentage=0.75)

        if ma:
            split.label(text=ma.name, translate=False, icon_value=icon)
            split.prop(slot, 'link', text="", emboss=False, translate=False)
        else:
            split.label(text="")


class VRayListNodeTrees(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text="", icon=item.bl_icon)
        layout.label(text=item.name, translate=False)


class VRayListMaterials(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(percentage=0.1)

        split.column().prop(item, 'diffuse_color', text="")
        split.column().label(text=item.name, translate=False)
        if hasattr(item, 'vray'):
            icon = item.vray.ntree.bl_icon if item.vray.ntree else 'NONE'
            split.column().prop(item.vray, 'ntree', text="", icon=icon)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayListNodeTrees,
        VRayListMaterialSlots,
        VRayListUse,
        VRayListDR,
        VRayList,
        VRayListMaterials,

        VRayOpListItemNew,
        VRayOpListItemDel,
        VRayOpListItemUp,
        VRayOpListItemDown,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

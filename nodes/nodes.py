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
import math
import sys

import bpy
import mathutils
import nodeitems_utils

from pynodes_framework import base, parameter

from vb30.plugins import PLUGINS
from vb30.debug   import Debug, PrintDict
from vb30.lib     import AttributeUtils, ClassUtils, CallbackUI, DrawUtils
from vb30.ui      import classes

from .        import tree
from .sockets import AddInput, AddOutput


VRayNodeTypes = {
    'BRDF'          : [],
    'EFFECT'        : [],
    'GEOMETRY'      : [],
    'LIGHT'         : [],
    'MATERIAL'      : [],
    'TEXTURE'       : [],
    'UVWGEN'        : [],
    'RENDERCHANNEL' : [],
}

VRayNodeTypeIcon = {
    'BRDF'          : 'TEXTURE_SHADED',
    'EFFECT'        : 'GHOST_ENABLED',
    'GEOMETRY'      : 'MESH_DATA',
    'LIGHT'         : 'LAMP',
    'MATERIAL'      : 'MATERIAL',
    'TEXTURE'       : 'TEXTURE',
    'UVWGEN'        : 'GROUP_UVS',
    'RENDERCHANNEL' : 'SCENE_DATA',
}


##     ## ######## ##    ## ##     ##
###   ### ##       ###   ## ##     ##
#### #### ##       ####  ## ##     ##
## ### ## ######   ## ## ## ##     ##
##     ## ##       ##  #### ##     ##
##     ## ##       ##   ### ##     ##
##     ## ######## ##    ##  #######

class VRayNodeCategory(nodeitems_utils.NodeCategory):
    pass


def GetCategories():
    return [
        VRayNodeCategory('VRAY', "V-Ray Textures", items=[ nodeitems_utils.NodeItem(vrayNodeType.bl_rna.identifier, label=vrayNodeType.bl_label) for vrayNodeType in VRayNodeTypes['TEXTURE'] ] ),
    ]


def add_nodetype(layout, t):
    icon = 'NONE'
    name = t.bl_rna.name

    if hasattr(t, 'bl_icon'):
        icon = t.bl_icon

    op = layout.operator("vray.add_node", text=name, icon=icon)
    op.type = t.bl_rna.identifier
    op.use_transform = True


class VRayNodesMenuRenderChannels(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuRenderChannels"
    bl_label  = "Render Channels"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeRenderChannels)

        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['RENDERCHANNEL'], key=lambda t: t.bl_label)):
            if i and i % 15 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuEnvironment(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuEnvironment"
    bl_label  = "Environment"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeEnvironment)


class VRayNodesMenuOutput(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuOutput"
    bl_label  = "Output"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeOutputMaterial)
        add_nodetype(self.layout, bpy.types.VRayNodeWorldOutput)
        add_nodetype(self.layout, bpy.types.VRayNodeObjectOutput)
        add_nodetype(self.layout, bpy.types.VRayNodeBlenderOutputGeometry)
        add_nodetype(self.layout, bpy.types.VRayNodeBlenderOutputMaterial)


class VRayNodesMenuGeom(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuGeom"
    bl_label  = "Geometry"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['GEOMETRY'], key=lambda t: t.bl_label)):
            if i and i % 15 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuMapping(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuMapping"
    bl_label  = "Mapping"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['UVWGEN'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuTexture(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuTexture"
    bl_label  = "Texture"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['TEXTURE'], key=lambda t: t.bl_label)):
            if i and i % 15 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuBRDF(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuBRDF"
    bl_label  = "BRDF"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['BRDF'], key=lambda t: t.bl_label)):
            if i and i % 10 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuSelector(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuSelector"
    bl_label  = "Selectors"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeSelectObject)
        add_nodetype(self.layout, bpy.types.VRayNodeSelectGroup)
        add_nodetype(self.layout, bpy.types.VRayNodeSelectNodeTree)


class VRayNodesMenuMaterial(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuMaterial"
    bl_label  = "Material"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['MATERIAL'], key=lambda t: t.bl_label)):
            if i and i % 10 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuEffects(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuEffects"
    bl_label  = "Effects"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeEffectsHolder)

        for vrayNodeType in sorted(VRayNodeTypes['EFFECT'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuLights(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuLights"
    bl_label  = "Lights"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['LIGHT'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuMath(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuMath"
    bl_label  = "Math"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeTransform)
        add_nodetype(self.layout, bpy.types.VRayNodeMatrix)
        add_nodetype(self.layout, bpy.types.VRayNodeVector)

        for vrayNodeType in sorted(VRayNodeTypes['TEXTURE'], key=lambda t: t.bl_label):
            if hasattr(vrayNodeType, 'bl_menu'):
                if vrayNodeType.bl_menu == 'Math':
                    add_nodetype(self.layout, vrayNodeType)


class VRayNodesFromBlender(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesFromBlender"
    bl_label  = "Blender"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.ShaderNodeNormal)
        add_nodetype(self.layout, bpy.types.ShaderNodeTexImage)


def VRayNodesMenu(self, context):
    self.layout.menu("VRayNodesFromBlender", icon='BLENDER')
    self.layout.menu("VRayNodesMenuGeom", icon='MESH_DATA')
    self.layout.menu("VRayNodesMenuLights", icon='LAMP')
    self.layout.menu("VRayNodesMenuBRDF", icon='TEXTURE_SHADED')
    self.layout.menu("VRayNodesMenuMaterial", icon='MATERIAL')
    self.layout.menu("VRayNodesMenuTexture", icon='TEXTURE')
    self.layout.menu("VRayNodesMenuMapping", icon='GROUP_UVS')
    self.layout.menu("VRayNodesMenuMath", icon='MANIPUL')
    self.layout.menu("VRayNodesMenuSelector", icon='ZOOM_SELECTED')
    self.layout.menu("VRayNodesMenuOutput", icon='OBJECT_DATA')
    self.layout.menu("VRayNodesMenuEnvironment", icon='WORLD')
    self.layout.menu("VRayNodesMenuEffects", icon='GHOST_ENABLED')
    self.layout.menu("VRayNodesMenuRenderChannels", icon='SCENE_DATA')


 ######  ##          ###     ######   ######     ##     ## ######## ######## ##     ##  #######  ########   ######
##    ## ##         ## ##   ##    ## ##    ##    ###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
##       ##        ##   ##  ##       ##          #### #### ##          ##    ##     ## ##     ## ##     ## ##
##       ##       ##     ##  ######   ######     ## ### ## ######      ##    ######### ##     ## ##     ##  ######
##       ##       #########       ##       ##    ##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##    ## ##       ##     ## ##    ## ##    ##    ##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
 ######  ######## ##     ##  ######   ######     ##     ## ########    ##    ##     ##  #######  ########   ######

def VRayNodeDraw(self, context, layout):
    if not hasattr(self, 'vray_type') or not hasattr(self, 'vray_plugin'):
        return

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]

    # Draw node properties using 'nodeDraw'
    #
    if hasattr(vrayPlugin, 'nodeDraw'):
        # XXX: The only way to use images by now
        # Remove after Blender fix
        if self.vray_plugin in {'BitmapBuffer', 'TexGradRamp', 'TexRemap'}:
            vrayPlugin.nodeDraw(context, layout, self)
        else:
            vrayPlugin.nodeDraw(context, layout, getattr(self, self.vray_plugin))


def VRayNodeDrawSide(self, context, layout):
    if not hasattr(self, 'vray_type') or not hasattr(self, 'vray_plugin'):
        return

    if self.vray_type == 'LIGHT' and self.vray_plugin not in {'LightMesh'}:
        # We only need sockets from 'LIGHT' nodes.
        # Params will be taken from lamp propGroup
        #
        return

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]

    classes.DrawPluginUI(
        context,
        layout,
        self,                            # PropertyGroup holder
        getattr(self, self.vray_plugin), # PropertyGroup
        self.vray_plugin,                # Plugin name
        vrayPlugin                       # Plugin module
    )


def VRayNodeInit(self, context):
    if not hasattr(self, 'vray_type') or self.vray_type == 'NONE':
        return
    if not hasattr(self, 'vray_plugin') or self.vray_plugin == 'NONE':
        return

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]
    bpyType    = getattr(bpy.types, self.vray_plugin)

    for attr in vrayPlugin.PluginParams:
        attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

        attr_options = attr.get('option')

        if attr['type'] in AttributeUtils.InputTypes:
            TypeToSocket = AttributeUtils.TypeToSocket
            if self.vray_type == 'LIGHT':
                TypeToSocket = AttributeUtils.TypeToSocketNoValue

            if attr_options:
                if 'LINKED_ONLY' in attr_options:
                    TypeToSocket = AttributeUtils.TypeToSocketNoValue

            AddInput(self, TypeToSocket[attr['type']], attr_name, attr['attr'], attr['default'])

        if attr['type'] in AttributeUtils.OutputTypes:
            AddOutput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'])

    if self.vray_type == 'TEXTURE':
        # Some plugins already have properly defined outputs
        #
        if self.vray_plugin in {'BitmapBuffer'}:
            pass
        elif self.vray_plugin in {'TexVector'}:
            AddOutput(self, 'VRaySocketVector', "Vector")
        else:
            AddOutput(self, 'VRaySocketColor', "Output")
    elif self.vray_type == 'UVWGEN':
        AddOutput(self, 'VRaySocketCoords', "Mapping", 'uvwgen')
    elif self.vray_type == 'BRDF':
        AddOutput(self, 'VRaySocketBRDF', "BRDF")
    elif self.vray_type == 'GEOMETRY':
        AddOutput(self, 'VRaySocketGeom', "Geomtery")
    elif self.vray_type == 'MATERIAL':
        AddOutput(self, 'VRaySocketMtl', "Material")
    elif self.vray_type == 'EFFECT':
        AddOutput(self, 'VRaySocketEffectOutput', "Output")
    elif self.vray_type == 'RENDERCHANNEL':
        AddOutput(self, 'VRaySocketRenderChannelOutput', "Channel")

    if self.vray_plugin in {'TexGradRamp', 'TexRemap'}:
        if not self.texture:
            self.texture = bpy.data.textures.new(".Ramp_%s" % self.name, 'NONE')
            self.texture.use_color_ramp = True
            self.texture.use_fake_user  = True

    elif self.vray_plugin == 'LightMesh':
        AddOutput(self, 'VRaySocketGeom', "Light")

    elif self.bl_idname == 'VRayNodeBitmapBuffer':
        if not self.texture:
            self.texture = bpy.data.textures.new(".Bitmap_%s" % self.name, 'IMAGE')
            self.texture.use_fake_user  = True


def VRayNodeCopy(self, node):
    if self.vray_plugin in {'TexGradRamp', 'TexRemap'}:
        self.texture = bpy.data.textures.new(".Ramp_%s" % self.name, 'NONE')
        self.texture.use_color_ramp = True
    elif self.bl_idname == 'VRayNodeBitmapBuffer':
        self.texture = node.texture


def VRayNodeFree(self):
    if self.vray_plugin in {'TexGradRamp', 'TexRemap'}:
        if self.texture:
            self.texture.user_clear()
            bpy.data.textures.remove(self.texture)


def VRayNodeDrawLabel(self):
    if bpy.context.scene.vray.Exporter.debug:
        return "%s [%s]" % (self.name, self.vray_plugin)
    return self.name


########  ##    ## ##    ##    ###    ##     ## ####  ######     ##    ##  #######  ########  ########  ######
##     ##  ##  ##  ###   ##   ## ##   ###   ###  ##  ##    ##    ###   ## ##     ## ##     ## ##       ##    ##
##     ##   ####   ####  ##  ##   ##  #### ####  ##  ##          ####  ## ##     ## ##     ## ##       ##
##     ##    ##    ## ## ## ##     ## ## ### ##  ##  ##          ## ## ## ##     ## ##     ## ######    ######
##     ##    ##    ##  #### ######### ##     ##  ##  ##          ##  #### ##     ## ##     ## ##             ##
##     ##    ##    ##   ### ##     ## ##     ##  ##  ##    ##    ##   ### ##     ## ##     ## ##       ##    ##
########     ##    ##    ## ##     ## ##     ## ####  ######     ##    ##  #######  ########  ########  ######

usePynodesFramwork = False
useCatergories     = False

category_textures = None
if useCatergories:
    category_textures = tree.VRayNodeTree.add_category("Textures", "Textures")

DynamicClasses = []


def LoadDynamicNodes():
    global DynamicClasses
    global VRayNodeTypes

    DynamicClasses = []

    # Manually defined classes
    #
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    # Runtime Node classes generation
    #
    for pluginType in VRayNodeTypes:
        VRayNodeTypes[pluginType] = []

        for pluginName in sorted(PLUGINS[pluginType]):
            # Skip manually created nodes
            if pluginName in {'BRDFLayered', 'TexLayered'}:
                continue

            # Plugin was not registered by the plugin manager,
            # skip it then.
            if not hasattr(bpy.types, pluginName):
                continue

            vrayPlugin  = PLUGINS[pluginType][pluginName]
            textureBpyType = getattr(bpy.types, pluginName)
            textureMenuType = getattr(vrayPlugin, 'MENU', None)

            # Debug("Creating Node from plugin: %s" % pluginName, msgType='INFO')

            DynNodeClassName = "VRayNode%s" % (pluginName)

            DynNodeClassAttrs = {
                'bl_idname' : DynNodeClassName,
                'bl_label'  : vrayPlugin.NAME,
                'bl_icon'   : VRayNodeTypeIcon.get(pluginType, 'VRAY_LOGO_MONO'),
                'bl_menu'   : textureMenuType,
            }

            if usePynodesFramwork:
                # !!! Associates nodes with a socket type
                DynNodeClassAttrs['socket_type'] = tree.VRayTreeSockets

                for attr in vrayPlugin.PluginParams:
                    attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

                    if attr['type'] not in AttributeUtils.OutputTypes and attr['type'] not in AttributeUtils.InputTypes:
                        continue

                    isOutput = attr['type'] in AttributeUtils.OutputTypes

                    if attr['type'] in {'FLOAT_TEXTURE'}:
                        # Debug("  Adding attribute '%s' {%s}" % (attr_name, attr['type']))
                        DynNodeClassAttrs[attr['attr']] = parameter.NodeParamFloat(name=attr_name, is_output=isOutput, description=attr['desc'])

                PrintDict("DynNodeClassAttrs for %s" % pluginName, DynNodeClassAttrs)

                DynNodeClass = type(
                    DynNodeClassName,
                    (bpy.types.Node, base.Node),
                    DynNodeClassAttrs
                )

            else:
                DynNodeClassAttrs['init']             = VRayNodeInit
                DynNodeClassAttrs['copy']             = VRayNodeCopy
                DynNodeClassAttrs['free']             = VRayNodeFree
                DynNodeClassAttrs['draw_buttons']     = VRayNodeDraw
                DynNodeClassAttrs['draw_buttons_ext'] = VRayNodeDrawSide
                DynNodeClassAttrs['draw_label']       = VRayNodeDrawLabel

                DynNodeClass = type(
                    DynNodeClassName,  # Name
                    (bpy.types.Node, base.Node), # Inheritance
                    DynNodeClassAttrs  # Attributes
                )

            if useCatergories:
                if pluginType == 'TEXTURE':
                    category_textures()(DynNodeClass)

            setattr(DynNodeClass, 'vray_type',   bpy.props.StringProperty(default=pluginType))
            setattr(DynNodeClass, 'vray_plugin', bpy.props.StringProperty(default=pluginName))

            if pluginName in  {'TexGradRamp', 'TexRemap', 'BitmapBuffer'}:
                setattr(DynNodeClass, 'texture', bpy.props.PointerProperty(
                    name = "Texture",
                    type = bpy.types.Texture,
                    description = "Fake texture for internal usage",
                ))

            bpy.utils.register_class(DynNodeClass)

            ClassUtils.RegisterPluginPropertyGroup(DynNodeClass, vrayPlugin)

            VRayNodeTypes[pluginType].append(getattr(bpy.types, DynNodeClassName))

            DynamicClasses.append(DynNodeClass)


    # Add manually defined classes
    VRayNodeTypes['BRDF'].append(bpy.types.VRayNodeBRDFLayered)
    VRayNodeTypes['TEXTURE'].append(bpy.types.VRayNodeTexLayered)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

StaticClasses = (
    VRayNodesFromBlender,
    VRayNodesMenuBRDF,
    VRayNodesMenuEffects,
    VRayNodesMenuEnvironment,
    VRayNodesMenuGeom,
    VRayNodesMenuLights,
    VRayNodesMenuMapping,
    VRayNodesMenuMaterial,
    VRayNodesMenuOutput,
    VRayNodesMenuSelector,
    VRayNodesMenuTexture,
    VRayNodesMenuRenderChannels,
    VRayNodesMenuMath,
)


def GetRegClasses():
    return StaticClasses


def register():
    LoadDynamicNodes()

    bpy.types.NODE_MT_add.append(VRayNodesMenu)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    for regClass in DynamicClasses:
        bpy.utils.unregister_class(regClass)

    bpy.types.NODE_MT_add.remove(VRayNodesMenu)

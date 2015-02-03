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

from vb30.plugins import PLUGINS
from vb30.debug   import Debug, PrintDict
from vb30.lib     import AttributeUtils, ClassUtils, CallbackUI, DrawUtils, LibUtils
from vb30.ui      import classes

from .        import tree
from .        import utils as NodeUtils
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
    split_items = 15

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in classes.VRayEngines


def BuildItemsList(nodeType, subType=None):
    return [ nodeitems_utils.NodeItem(t.bl_rna.identifier, label=t.bl_label) for t in VRayNodeTypes[nodeType] ]


def GetCategories():
    return [
        VRayNodeCategory(
            'VRAY_BLENDER',
            "Blender",
            items = [
                nodeitems_utils.NodeItem("ShaderNodeNormal", label="Normal"),
                nodeitems_utils.NodeItem("ShaderNodeVectorCurve", label="Curves"),
                nodeitems_utils.NodeItem("ShaderNodeGroup", label="Group"),
                nodeitems_utils.NodeItem("NodeGroupInput", label="Group Input"),
                nodeitems_utils.NodeItem("NodeGroupOutput", label="Group Output"),
            ],
            icon = 'BLENDER'
        ),
        VRayNodeCategory(
            'VRAY_MATERIAL',
            "Material",
            items = BuildItemsList('MATERIAL'),
            icon  = 'MATERIAL'
        ),
        VRayNodeCategory(
            'VRAY_BRDF',
            "BRDF",
            items = BuildItemsList('BRDF'),
            icon  = 'TEXTURE_SHADED'
        ),
        VRayNodeCategory(
            'VRAY_TEXTURE',
            "Textures",
            items = [
                nodeitems_utils.NodeItem("VRayNodeMetaImageTexture"),
            ] + BuildItemsList('TEXTURE'),
            icon  = 'TEXTURE'
        ),
        VRayNodeCategory(
            'VRAY_UVWGEN',
            "Mapping",
            items = BuildItemsList('UVWGEN'),
            icon  = 'GROUP_UVS'
        ),
        VRayNodeCategory(
            'VRAY_GEOMETRY',
            "Geometry",
            items = BuildItemsList('GEOMETRY'),
            icon  = 'MESH_DATA'
        ),
        VRayNodeCategory(
            "VRAY_LIGHT",
            "Lights",
            items = BuildItemsList('LIGHT'),
            icon = 'LAMP',
        ),
        VRayNodeCategory(
            "VRAY_MATH",
            "Math",
            items = [
                nodeitems_utils.NodeItem("VRayNodeTransform"),
                nodeitems_utils.NodeItem("VRayNodeMatrix"),
                nodeitems_utils.NodeItem("VRayNodeVector"),
                # for vrayNodeType in sorted(VRayNodeTypes['TEXTURE'], key=lambda t: t.bl_label):
                #     if hasattr(vrayNodeType, 'bl_menu'):
                #         if vrayNodeType.bl_menu == 'Math':
                #             add_nodetype(self.layout, vrayNodeType)
            ],
            icon = 'MANIPUL',
        ),
        VRayNodeCategory(
            'VRAY_OUTPUTS',
            "Outputs",
            items = [
                nodeitems_utils.NodeItem("VRayNodeOutputMaterial"),
                nodeitems_utils.NodeItem("VRayNodeWorldOutput"),
                nodeitems_utils.NodeItem("VRayNodeObjectOutput"),
                nodeitems_utils.NodeItem("VRayNodeBlenderOutputGeometry"),
                nodeitems_utils.NodeItem("VRayNodeBlenderOutputMaterial"),

            ],
            icon  = 'OBJECT_DATA'
        ),
        VRayNodeCategory(
            'VRAY_SELECTORS',
            "Selectors",
            items = [
                nodeitems_utils.NodeItem("VRayNodeSelectObject"),
                nodeitems_utils.NodeItem("VRayNodeSelectGroup"),
            ],
            icon  = 'ZOOM_SELECTED'
        ),
        VRayNodeCategory(
            'VRAY_ENVIRONMENT',
            "Environment",
            items = [
                nodeitems_utils.NodeItem("VRayNodeEnvironment"),

            ],
            icon  = 'WORLD'
        ),
        VRayNodeCategory(
            "VRAY_EFFECT",
            "Effects",
            items = [
                nodeitems_utils.NodeItem("VRayNodeEffectsHolder"),
            ] + BuildItemsList('EFFECT'),
            icon  = 'GHOST_ENABLED',
        ),
        VRayNodeCategory(
            'VRAY_RENDERCHANNEL',
            "Render Channels",
            items = [
                nodeitems_utils.NodeItem("VRayNodeRenderChannels", label="Channels Container"),
            ] + BuildItemsList('RENDERCHANNEL'),
            icon  = 'SCENE_DATA'
        ),
        VRayNodeCategory(
            "VRAY_LAYOUT",
            "Layout",
            items = [
                nodeitems_utils.NodeItem("NodeFrame"),
                nodeitems_utils.NodeItem("NodeReroute"),
                nodeitems_utils.NodeItem("VRayNodeDebugSwitch"),
            ],
            icon = 'VIEW3D_VEC'
        ),
    ]


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
    propGroup  = getattr(self, self.vray_plugin)

    # Draw node properties using 'nodeDraw'
    #
    if hasattr(vrayPlugin, 'nodeDraw'):
        # XXX: The only way to use images by now
        # Remove after Blender fix
        if self.vray_plugin in {'BitmapBuffer', 'TexGradRamp', 'TexRemap'}:
            vrayPlugin.nodeDraw(context, layout, self)
        else:
            vrayPlugin.nodeDraw(context, layout, propGroup)

    elif hasattr(vrayPlugin, 'Widget') and 'node_widgets' in vrayPlugin.Widget:
        for widget in vrayPlugin.Widget['node_widgets']:
            DrawUtils.RenderWidget(context, propGroup, layout, widget)


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

    AddDefaultInputsOutputs(self, vrayPlugin)

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
        AddOutput(self, 'VRaySocketGeom', "Geometry")
    elif self.vray_type == 'MATERIAL':
        AddOutput(self, 'VRaySocketMtl', "Material")
    elif self.vray_type == 'EFFECT':
        AddOutput(self, 'VRaySocketEffectOutput', "Output")
    elif self.vray_type == 'RENDERCHANNEL':
        AddOutput(self, 'VRaySocketRenderChannelOutput', "Channel")

    if self.vray_plugin == 'LightMesh':
        AddOutput(self, 'VRaySocketGeom', "Light")

    if self.vray_plugin in {'TexGradRamp', 'TexRemap'}:
        if not self.texture:
            NodeUtils.CreateRampTexture(self)

    elif self.bl_idname == 'VRayNodeBitmapBuffer':
        if not self.texture:
            NodeUtils.CreateBitmapTexture(self)


def VRayNodeCopy(self, node):
    if self.vray_plugin in {'TexGradRamp', 'TexRemap'}:
        NodeUtils.CreateRampTexture(self)
        NodeUtils.CopyRamp(node.texture.color_ramp, self.texture.color_ramp)

    elif self.bl_idname == 'VRayNodeBitmapBuffer':
        NodeUtils.CreateBitmapTexture(self)

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]

    propGroup     = getattr(node, self.vray_plugin)
    propGroupCopy = getattr(self, self.vray_plugin)

    for attrDesc in vrayPlugin.PluginParams:
        attrName = attrDesc['attr']

        # NOTE: Not all attributes has property
        if not hasattr(propGroup, attrName):
            continue

        setattr(propGroupCopy, attrName, getattr(propGroup, attrName))

    for inSock in self.inputs:
        if not hasattr(inSock, 'value'):
            continue
        inSock.value = node.inputs[inSock.name].value


def VRayNodeFree(self):
    pass


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

DynamicClasses = []


def LoadDynamicNodes():
    global DynamicClasses
    global VRayNodeTypes

    DynamicClasses = []

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

            DynNodeClassName = "VRayNode%s" % (pluginName)

            DynNodeClassAttrs = {
                'bl_idname' : DynNodeClassName,
                'bl_label'  : vrayPlugin.NAME,
                'bl_icon'   : VRayNodeTypeIcon.get(pluginType, 'VRAY_LOGO_MONO'),
                'bl_menu'   : textureMenuType,

                'init'             : VRayNodeInit,
                'copy'             : VRayNodeCopy,
                'free'             : VRayNodeFree,
                'draw_buttons'     : VRayNodeDraw,
                'draw_buttons_ext' : VRayNodeDrawSide,
                'draw_label'       : VRayNodeDrawLabel,

                'vray_type'   : bpy.props.StringProperty(default=pluginType),
                'vray_plugin' : bpy.props.StringProperty(default=pluginName),
            }

            DynNodeClass = type(
                DynNodeClassName,  # Name
                (bpy.types.Node,), # Inheritance
                DynNodeClassAttrs  # Attributes
            )

            if pluginName in  {'TexGradRamp', 'TexRemap', 'BitmapBuffer'}:
                NodeUtils.CreateFakeTextureAttribute(DynNodeClass)

            bpy.utils.register_class(DynNodeClass)

            ClassUtils.RegisterPluginPropertyGroup(DynNodeClass, vrayPlugin)

            VRayNodeTypes[pluginType].append(getattr(bpy.types, DynNodeClassName))

            DynamicClasses.append(DynNodeClass)

    # Add manually defined classes
    VRayNodeTypes['BRDF'].append(bpy.types.VRayNodeBRDFLayered)
    VRayNodeTypes['TEXTURE'].append(bpy.types.VRayNodeTexLayered)
    VRayNodeTypes['TEXTURE'].append(bpy.types.VRayNodeTexMulti)
    VRayNodeTypes['MATERIAL'].append(bpy.types.VRayNodeMtlMulti)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##


def register():
    LoadDynamicNodes()

    nodeitems_utils.register_node_categories('VRAY_NODES', GetCategories())


def unregister():
    nodeitems_utils.unregister_node_categories('VRAY_NODES')

    for regClass in DynamicClasses:
        bpy.utils.unregister_class(regClass)

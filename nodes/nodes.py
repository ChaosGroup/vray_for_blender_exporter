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

import re
import math
import sys

import bpy
import mathutils

from pynodes_framework import base, parameter

from vb25.plugins import PLUGINS
from vb25.debug   import Debug, PrintDict
from vb25.lib     import AttributeUtils, ClassUtils, CallbackUI, DrawUtils

from .        import tree
from .sockets import AddInput, AddOutput


##     ## ######## #### ##       #### ######## #### ########  ######
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##
##     ##    ##     ##  ##        ##     ##     ##  ######    ######
##     ##    ##     ##  ##        ##     ##     ##  ##             ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
 #######     ##    #### ######## ####    ##    #### ########  ######

def GetActiveNode(nodetree):
    if not nodetree:
        return None
    return nodetree.nodes[-1]


######## ######## ##     ## ######## ##     ## ########  ########
   ##    ##        ##   ##     ##    ##     ## ##     ## ##
   ##    ##         ## ##      ##    ##     ## ##     ## ##
   ##    ######      ###       ##    ##     ## ########  ######
   ##    ##         ## ##      ##    ##     ## ##   ##   ##
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##
   ##    ######## ##     ##    ##     #######  ##     ## ########

class VRayNodeTexLayered(bpy.types.Node, tree.VRayTreeNode):
    bl_idname = 'VRayNodeTexLayered'
    bl_label  = 'Texture Layered'
    bl_icon   = 'VRAY_LOGO'

    def init(self, context):
        for i in range(2):
            humanIndex = i + 1

            texSockName    = "Texture %i" % humanIndex
            weightSockName = "Weight %i" % humanIndex

            self.inputs.new('VRaySocketColor', texSockName)
            self.inputs.new('VRaySocketFloatColor', weightSockName)

            self.inputs[weightSockName].value = 1.0

        self.outputs.new('VRaySocketColor', "Output")


########  ########  ########  ########
##     ## ##     ## ##     ## ##
##     ## ##     ## ##     ## ##
########  ########  ##     ## ######
##     ## ##   ##   ##     ## ##
##     ## ##    ##  ##     ## ##
########  ##     ## ########  ##

class VRayNodeBRDFLayered(bpy.types.Node, tree.VRayTreeNode):
    bl_idname = 'VRayNodeBRDFLayered'
    bl_label  = 'Layered'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'BRDF'
    vray_plugin = 'BRDFLayered'

    additive_mode = bpy.props.BoolProperty(
        name        = "Additive Mode",
        description = "Additive mode",
        default     = False
    )

    def init(self, context):
        for i in range(2):
            humanIndex = i + 1

            brdfSockName   = "BRDF %i" % humanIndex
            weightSockName = "Weight %i" % humanIndex

            self.inputs.new('VRaySocketBRDF',  brdfSockName)
            self.inputs.new('VRaySocketFloatColor', weightSockName)

            self.inputs[weightSockName].value = 1.0

        self.outputs.new('VRaySocketBRDF', "BRDF")

    def draw_buttons(self, context, layout):
        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_add_brdf_layered_sockets', icon="ZOOMIN", text="Add")
        row.operator('vray.node_del_brdf_layered_sockets', icon="ZOOMOUT", text="")

        layout.prop(self, 'additive_mode')


##     ## ######## ##    ## ##     ##
###   ### ##       ###   ## ##     ##
#### #### ##       ####  ## ##     ##
## ### ## ######   ## ## ## ##     ##
##     ## ##       ##  #### ##     ##
##     ## ##       ##   ### ##     ##
##     ## ######## ##    ##  #######

VRayNodeTypes = {
    'TEXTURE'  : [],
    'BRDF'     : [],
    'MATERIAL' : [],
    'GEOMETRY' : [],
    'UVWGEN'   : [],
}


def add_nodetype(layout, t):
    layout.operator("node.add_node", text=t.bl_label).type=t.bl_rna.identifier


class VRayNodesMenuOutput(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuOutput"
    bl_label  = "Output"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeBlenderOutput)
        add_nodetype(self.layout, bpy.types.VRayNodeOutputMaterial)
        add_nodetype(self.layout, bpy.types.VRayNodeWorldOutput)
        add_nodetype(self.layout, bpy.types.VRayNodeObjectOutput)


class VRayNodesMenuGeom(bpy.types.Menu, tree.VRayData):
    bl_idname = "VRayNodesMenuGeom"
    bl_label  = "Geomtery"

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


def VRayNodesMenu(self, context):
    self.layout.menu("VRayNodesMenuBRDF")
    self.layout.menu("VRayNodesMenuTexture")
    self.layout.menu("VRayNodesMenuMapping")
    self.layout.menu("VRayNodesMenuMaterial")
    self.layout.menu("VRayNodesMenuOutput")
    self.layout.menu("VRayNodesMenuSelector")
    self.layout.menu("VRayNodesMenuGeom")


#### ##    ## #### ########
 ##  ###   ##  ##     ##
 ##  ####  ##  ##     ##
 ##  ## ## ##  ##     ##
 ##  ##  ####  ##     ##
 ##  ##   ###  ##     ##
#### ##    ## ####    ##

def VRayNodeDraw(self, context, layout):
    if not hasattr(self, 'vray_type') or not hasattr(self, 'vray_plugin'):
        return

    if context.scene.vray.exporter.debug:
        layout.label(text="Type: %s"   % self.vray_type)
        layout.label(text="Plugin: %s" % self.vray_plugin)

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]
    if hasattr(vrayPlugin, 'nodeDraw'):
        vrayPlugin.nodeDraw(context, layout, getattr(self, self.vray_plugin))


def VRayNodeDrawSide(self, context, layout):
    if not hasattr(self, 'vray_type') or not hasattr(self, 'vray_plugin'):
        return

    if context.scene.vray.exporter.nodesUseSidePanel:
        vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]

        if hasattr(vrayPlugin, 'gui'):
            vrayPlugin.gui(context, layout, getattr(self, self.vray_plugin))
        else:
            DrawUtils.Draw(context, layout, getattr(self, self.vray_plugin), vrayPlugin.PluginParams)


def VRayNodeInit(self, context):
    if not hasattr(self, 'vray_type') or self.vray_type == 'NONE':
        return
    if not hasattr(self, 'vray_plugin') or self.vray_plugin == 'NONE':
        return

    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]
    bpyType    = getattr(bpy.types, self.vray_plugin)

    for attr in vrayPlugin.PluginParams:
        attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

        if attr['type'] in AttributeUtils.InputTypes:
            AddInput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'], attr['default'])

        if attr['type'] in AttributeUtils.OutputTypes:
            AddOutput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'])

    if self.vray_type == 'TEXTURE':
        AddOutput(self, 'VRaySocketColor', "Output")
    elif self.vray_type == 'UVWGEN':
        AddOutput(self, 'VRaySocketCoords', "Mapping", 'uvwgen')
    elif self.vray_type == 'BRDF':
        AddOutput(self, 'VRaySocketBRDF', "BRDF")
    elif self.vray_type == 'GEOMETRY':
        AddOutput(self, 'VRaySocketGeom', "Geomtery")
    elif self.vray_type == 'MATERIAL':
        AddOutput(self, 'VRaySocketMtl', "Material")


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

    # Manually defined classes
    #
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    # Runtime Node classes generation
    #
    for pluginType in VRayNodeTypes:
        VRayNodeTypes[pluginType] = []

        for pluginName in sorted(PLUGINS[pluginType]):
            # Skip manually created plugins
            if pluginName in ['BRDFLayered']:
                continue

            # Plugin was not registered by the plugin manager,
            # skit it then.
            if not hasattr(bpy.types, pluginName):
                continue

            vrayPlugin  = PLUGINS[pluginType][pluginName]
            textureBpyType = getattr(bpy.types, pluginName)

            # Debug("Creating Node from plugin: %s" % pluginName, msgType='INFO')

            DynNodeClassName = "VRayNode%s" % (pluginName)

            DynNodeClassAttrs = {
                'bl_idname' : DynNodeClassName,
                'bl_label'  : vrayPlugin.NAME,
                'bl_icon'   : 'VRAY_LOGO',

                'vray_type'   : pluginType,
                'vray_plugin' : pluginName,
            }

            # XXX: Loads fine, but sockets are not drawn
            usePynodesFramwork = False

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
                DynNodeClassAttrs['draw_buttons']     = VRayNodeDraw
                DynNodeClassAttrs['draw_buttons_ext'] = VRayNodeDrawSide

                DynNodeClass = type(
                    DynNodeClassName,  # Name
                    (bpy.types.Node,), # Inheritance
                    DynNodeClassAttrs  # Attributes
                )

            bpy.utils.register_class(DynNodeClass)

            ClassUtils.RegisterPluginPropertyGroup(DynNodeClass, vrayPlugin)

            VRayNodeTypes[pluginType].append(getattr(bpy.types, DynNodeClassName))

            DynamicClasses.append(DynNodeClass)

    # Add manually defined classes
    VRayNodeTypes['BRDF'].append(bpy.types.VRayNodeBRDFLayered)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

StaticClasses = (
    VRayNodeTexLayered,
    VRayNodeBRDFLayered,

    VRayNodesMenuTexture,
    VRayNodesMenuBRDF,
    VRayNodesMenuMapping,
    VRayNodesMenuMaterial,
    VRayNodesMenuOutput,
    VRayNodesMenuSelector,
    VRayNodesMenuGeom,
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

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

from vb25.lib import AttributeUtils
from vb25.lib import ClassUtils
from vb25.lib import CallbackUI

from .tree import *


########  ######## ######## #### ##    ## ########  ######  
##     ## ##       ##        ##  ###   ## ##       ##    ## 
##     ## ##       ##        ##  ####  ## ##       ##       
##     ## ######   ######    ##  ## ## ## ######    ######  
##     ## ##       ##        ##  ##  #### ##             ## 
##     ## ##       ##        ##  ##   ### ##       ##    ## 
########  ######## ##       #### ##    ## ########  ######  

VRAY_SOCKET_TYPE = {
    'BRDF'          : 'VRaySocketBRDF',
    'MATERIAL'      : 'VRaySocketMtl',
    'COLOR'         : 'VRaySocketColor',
    'TEXTURE'       : 'VRaySocketColor',
    'FLOAT_TEXTURE' : 'VRaySocketFloatColor',
}


##     ## ######## #### ##       #### ######## #### ########  ######  
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##       
##     ##    ##     ##  ##        ##     ##     ##  ######    ######  
##     ##    ##     ##  ##        ##     ##     ##  ##             ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
 #######     ##    #### ######## ####    ##    #### ########  ######  

def AddInput(node, socketType, socketName, attrName=None, default=None):
    if socketName in node.inputs:
        return

    Debug("Adding input socket: '%s' <= '%s'" % (socketName, attrName), msgType='INFO')

    node.inputs.new(socketType, socketName)

    createdSocket = node.inputs[socketName]

    if attrName is not None:
        createdSocket.vray_attr = attrName

    if default is not None:
        if socketType in {'VRaySocketColor', 'VRaySocketVector'}:
            createdSocket.value = (default[0], default[1], default[2])
            Debug("  Setting default value: (%.3f, %.3f, %.3f)" % (default[0], default[1], default[2]), msgType='INFO')
        else:
            createdSocket.value = default
            Debug("  Setting default value: %s" % default, msgType='INFO')


def AddOutput(node, socketType, socketName, attrName=None):
    if socketName in node.outputs:
        return

    Debug("Adding output socket: '%s' <= '%s'" % (socketName, attrName), msgType='INFO')

    node.outputs.new(socketType, socketName)

    createdSocket = node.outputs[socketName]

    if attrName is not None:
        createdSocket.vray_attr = attrName


def GetActiveNode(nodetree):
    if not nodetree:
        return None
    return nodetree.nodes[-1]


 #######  ##     ## ######## ########  ##     ## ######## 
##     ## ##     ##    ##    ##     ## ##     ##    ##    
##     ## ##     ##    ##    ##     ## ##     ##    ##    
##     ## ##     ##    ##    ########  ##     ##    ##    
##     ## ##     ##    ##    ##        ##     ##    ##    
##     ## ##     ##    ##    ##        ##     ##    ##    
 #######   #######     ##    ##         #######     ##    

# <lukas_t> instead of limiting to 1 node instance you could also allow
#           multiple nodes but have an exclusive "enable" option on them
# <lukas_t> enable node -> all others of same type get disabled

class VRayNodeOutput(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeOutput'
    bl_label  = 'Material Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'
    
    def init(self, context):
        AddInput(self, 'VRaySocketMtl', "Material")


class VRayNodeWorldOutput(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeWorldOutput'
    bl_label  = 'World Output'
    bl_icon   = 'VRAY_LOGO'

    gi_tex = bpy.props.BoolProperty(
        name        = "Override GI",
        description = "Override environment for GI",
        default     = False
    )
    
    reflect_tex = bpy.props.BoolProperty(
        name        = "Override Reflect",
        description = "Override environment for reflection",
        default     = False
    )

    refract_tex = bpy.props.BoolProperty(
        name        = "Override Refract",
        description = "Override environment for refraction",
        default     = False
    )

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def draw_buttons(self, context, layout):
        layout.prop(self, 'gi_tex')
        layout.prop(self, 'reflect_tex')
        layout.prop(self, 'refract_tex')

    def init(self, context):
        AddInput(self, 'VRaySocketColor', "Background", 'bg_tex')
        AddInput(self, 'VRaySocketColor', "GI",         'gi_tex')
        AddInput(self, 'VRaySocketColor', "Reflection", 'reflect_tex')
        AddInput(self, 'VRaySocketColor', "Refraction", 'refract_tex')


 ######   #######   #######  ########  ########   ######  
##    ## ##     ## ##     ## ##     ## ##     ## ##    ## 
##       ##     ## ##     ## ##     ## ##     ## ##       
##       ##     ## ##     ## ########  ##     ##  ######  
##       ##     ## ##     ## ##   ##   ##     ##       ## 
##    ## ##     ## ##     ## ##    ##  ##     ## ##    ## 
 ######   #######   #######  ##     ## ########   ######  

class VRayNodeUVChannel(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeUVChannel'
    bl_label  = 'UV Channel'
    bl_icon   = 'VRAY_LOGO'

    uv_layer = bpy.props.StringProperty(
        name        = "Layer",
        description = "UV layer name",
        default     = ""
    )

    repeat_u = bpy.props.FloatProperty(
        name        = "Tile U",
        description = "Tile in U",
        min         = 0.0,
        max         = 1000.0,
        soft_min    = 1,
        soft_max    = 20.0,
        default     = 1.0
    )

    repeat_v = bpy.props.FloatProperty(
        name        = "Tile V",
        description = "Tile in V",
        min         = 0.0,
        max         = 1000.0,
        soft_min    = 1.0,
        soft_max    = 20.0,
        default     = 1.0
    )

    mirror_u = bpy.props.BoolProperty(
        name        = "Mirror U",
        description = "Mirror in U",
        default     = False
    )

    mirror_v = bpy.props.BoolProperty(
        name        = "Mirror V",
        description = "Mirror in V",
        default     = False
    )

    rotate_frame = bpy.props.FloatProperty(
        name        = "Rotation",
        description = "Texture rotation",
        subtype     = 'ANGLE',
        soft_min    = -math.pi,
        soft_max    =  math.pi,
        default     = 0.0
    )

    def init(self, context):
        AddInput(self,  'VRaySocketCoords', "Mapping", 'uvwgen')
        AddOutput(self, 'VRaySocketCoords', "Mapping", 'uvwgen')

    def draw_buttons(self, context, layout):
        ob = context.object

        split = layout.split(percentage=0.3)
        split.label(text="Layer:")
        if ob and ob.type == 'MESH':
            split.prop_search(self,    'uv_layer',
                              ob.data, 'uv_textures',
                              text="")
        else:
            split.prop(self, 'uv_layer', text="")
        
        split = layout.split()
        col = split.column(align=True)
        col.prop(self, 'repeat_u')
        col.prop(self, 'repeat_v')

        split = layout.split()
        col = split.column(align=True)
        col.prop(self, 'mirror_u')
        col.prop(self, 'mirror_v')
        
        split = layout.split()
        split.prop(self, 'rotate_frame')


######## ######## ##     ## ######## ##     ## ########  ######## 
   ##    ##        ##   ##     ##    ##     ## ##     ## ##       
   ##    ##         ## ##      ##    ##     ## ##     ## ##       
   ##    ######      ###       ##    ##     ## ########  ######   
   ##    ##         ## ##      ##    ##     ## ##   ##   ##       
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##       
   ##    ######## ##     ##    ##     #######  ##     ## ######## 

class VRayNodeTexLayered(bpy.types.Node, VRayTreeNode):
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

class VRayNodeBRDFLayered(bpy.types.Node, VRayTreeNode):
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
    'UVWGEN'   : [],
}


def add_nodetype(layout, t):
    layout.operator("node.add_node", text=t.bl_label).type=t.bl_rna.identifier


class VRayNodesMenuOutput(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuOutput"
    bl_label  = "Output"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeOutput)
        add_nodetype(self.layout, bpy.types.VRayNodeWorldOutput)        


class VRayNodesMenuMapping(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuMapping"
    bl_label  = "Mapping"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['UVWGEN'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuTexture(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuTexture"
    bl_label  = "Texture"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['TEXTURE'], key=lambda t: t.bl_label)):
            if i and i % 15 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuBRDF(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuBRDF"
    bl_label  = "BRDF"

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()
        for i,vrayNodeType in enumerate(sorted(VRayNodeTypes['BRDF'], key=lambda t: t.bl_label)):
            if i and i % 10 == 0:
                sub = row.column()
            add_nodetype(sub, vrayNodeType)


class VRayNodesMenuMaterial(bpy.types.Menu, VRayData):
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
    if context.scene.vray.exporter.nodesUseSidePanel:
        vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]
        if not hasattr(vrayPlugin, 'gui'):
            return
        vrayPlugin.gui(context, layout, getattr(self, self.vray_plugin))


def VRayNodeInit(self, context):
    if not hasattr(self, 'vray_type') or self.vray_type == 'NONE':
        return
    if not hasattr(self, 'vray_plugin') or self.vray_plugin == 'NONE':
        return
    
    vrayPlugin = PLUGINS[self.vray_type][self.vray_plugin]
    bpyType    = getattr(bpy.types, self.vray_plugin)

    if hasattr(vrayPlugin, 'PluginParams'):
        for attr in vrayPlugin.PluginParams:
            attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

            if attr['type'] in AttributeUtils.InputTypes:
                AddInput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'], attr['default'])

            if attr['type'] in AttributeUtils.OutputTypes:
                AddOutput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'])
    
    else:
        Debug("Plugin \"%s\" uses legacy registration system!" % self.vray_plugin, msgType='INFO')

        for prop in bpyType.bl_rna.properties:
            if prop.name in ['RNA', 'Name']:
                continue
            
            # Debug("  Property: %s \"%s\" [%s]" % (prop.identifier, prop.name, prop.default))
            if prop.name in self.inputs:
                continue

            if hasattr(vrayPlugin, 'MAPPED_PARAMS'):
                if prop.identifier in vrayPlugin.MAPPED_PARAMS:
                    socketType = VRAY_SOCKET_TYPE[vrayPlugin.MAPPED_PARAMS[prop.identifier]]
                    
                    default = prop.default
                    if prop.type == 'FLOAT' and prop.subtype == 'COLOR':
                        default = prop.default_array

                    AddInput(self, socketType, prop.name, prop.identifier, default)
            else:
                # Try to guess type
                if prop.type == 'STRING':
                    AddInput(self, 'VRaySocketBRDF', prop.name, prop.identifier)
                elif prop.type == 'FLOAT':
                    if prop.subtype == 'COLOR':
                        AddInput(self, 'VRaySocketColor', prop.name, prop.identifier, prop.default_array)

    if self.vray_type == 'TEXTURE':
        AddOutput(self, 'VRaySocketColor', "Output")
    
    elif self.vray_type == 'UVWGEN':    
        AddOutput(self, 'VRaySocketCoords', "Mapping", 'uvwgen')
    
    elif self.vray_type == 'BRDF':
        AddOutput(self, 'VRaySocketBRDF', "BRDF")

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

            # Debug("Creating Node from plugin: %s" % (pluginName), msgType='INFO')

            DynNodeClassName = "VRayNode%s" % (pluginName)

            DynNodeClassAttrs = {
                'bl_idname' : DynNodeClassName,
                'bl_label'  : vrayPlugin.NAME,
                'bl_icon'   : 'VRAY_LOGO',

                'vray_type'   : pluginType,
                'vray_plugin' : pluginName,
            }

            if 1:
                # XXX: Loads fine, but sockets are not drawn
                #
                for attr in vrayPlugin.PluginParams:
                    attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))
                
                    if attr['type'] not in AttributeUtils.OutputTypes and attr['type'] not in AttributeUtils.InputTypes:
                        continue
                
                    isOutput = attr['type'] in AttributeUtils.OutputTypes
                
                    if attr['type'] in {'FLOAT_TEXTURE'}:
                        Debug("Adding attribute: %s" % attr_name)
                        DynNodeClassAttrs[attr['attr']] = parameter.NodeParamFloat(attr_name, is_output=isOutput, description=attr['desc'])

                DynNodeClass = type(
                    # Name
                    DynNodeClassName,
                    
                    # Inheritance
                    (bpy.types.Node, base.Node, VRayTreeNode),
                    
                    # Attributes
                    DynNodeClassAttrs
                )
            else:
                DynNodeClassAttrs['init']             = VRayNodeInit
                DynNodeClassAttrs['draw_buttons']     = VRayNodeDraw
                DynNodeClassAttrs['draw_buttons_ext'] = VRayNodeDrawSide

                DynNodeClass = type(
                    DynNodeClassName,
                    (bpy.types.Node, VRayTreeNode),
                    DynNodeClassAttrs
                )

            bpy.utils.register_class(DynNodeClass)
          
            # Load attributes
            if hasattr(vrayPlugin, 'add_properties'):
                vrayPlugin.add_properties(DynNodeClass)
            else:
                ClassUtils.RegisterPluginPropertyGroup(DynNodeClass, vrayPlugin)
  
            ClassUtils.RegisterPluginPropertyGroup(DynNodeClass, vrayPlugin)
            
            VRayNodeTypes[pluginType].append(getattr(bpy.types, DynNodeClassName))

            DynamicClasses.append(DynNodeClass)

    # Add manually defined classes
    VRayNodeTypes['BRDF'].append(bpy.types.VRayNodeBRDFLayered)
    VRayNodeTypes['UVWGEN'].append(bpy.types.VRayNodeUVChannel)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

StaticClasses = (
   
    VRayNodeTree,
    VRayWorldNodeTree,
  
    VRayNodeOutput,
    VRayNodeWorldOutput,

    VRayNodeUVChannel,
    VRayNodeTexLayered,    
    VRayNodeBRDFLayered,

    VRayNodesMenuTexture,
    VRayNodesMenuBRDF,
    VRayNodesMenuMapping,
    VRayNodesMenuMaterial,
    VRayNodesMenuOutput,
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

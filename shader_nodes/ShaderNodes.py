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

import bpy
import mathutils

from pprint import pprint

from vb25.plugins import PLUGINS, load_plugins, gen_menu_items


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

    print("Adding socket: '%s' <= '%s'" % (socketName, attrName))

    node.inputs.new(socketType, socketName)

    createdSocket = node.inputs[socketName]

    if attrName is not None:
        createdSocket.vray_attr = attrName

    if default is not None:
        if socketType == 'VRaySocketColor':
            createdSocket.value = (default[0], default[1], default[2])
            print("  Setting default value: (%.3f, %.3f, %.3f)" % (default[0], default[1], default[2]))

        else:
            createdSocket.value = default
            print("  Setting default value: %s" % default)


def AddOutput(node, socketType, socketName):
    if socketName in node.outputs:
        return
    node.outputs.new(socketType, socketName)


def GetNodeTreeFromContext(context):
    ob = context.active_object
    if ob and ob.type not in {'LAMP', 'CAMERA'}:
        ma = ob.active_material
        if ma is None:
            return None

        nt_name = ma.vray.nodetree
        if not nt_name:
            return None
        
        if nt_name in bpy.data.node_groups:
            return bpy.data.node_groups[ma.vray.nodetree]

    return None


def GetActiveNode(nodetree):
    if not nodetree:
        return None
    return nodetree.nodes[-1]


 #######  ########  ######## ########     ###    ########  #######  ########   ######  
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ## 
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##       
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######  
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ## 
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ## 
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ###### 

class VRAY_OT_add_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_material_nodes"
    bl_label       = "Use Nodes"
    bl_description = ""

    def execute(self, context):
        idblock = context.material

        nt = bpy.data.node_groups.new(idblock.name, type='VRayShaderTreeType')
        nt.use_fake_user = True

        idblock.vray.nodetree = nt.name

        nt.nodes.new('VRayNodeOutput')

        return {'FINISHED'}


class VRAY_OT_node_add_brdf_layered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_add_brdf_layered_sockets'
    bl_label       = "Add BRDFLayered Socket"
    bl_description = "Adds BRDFLayered sockets"

    def execute(self, context):
        node = context.node
        
        newIndex = int(len(node.inputs) / 2) + 1

        # BRDFLayered sockets are always in pairs
        #
        brdfSockName   = "BRDF %i" % newIndex
        weightSockName = "Weight %i" % newIndex

        node.inputs.new('VRaySocketBRDF',  brdfSockName)
        node.inputs.new('VRaySocketFloatColor', weightSockName)

        node.inputs[weightSockName].value = 1.0

        return {'FINISHED'}


class VRAY_OT_node_del_brdf_layered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_del_brdf_layered_sockets'
    bl_label       = "Remove BRDFLayered Socket"
    bl_description = "Removes BRDFLayered socket (only not linked sockets will be removed)"

    def execute(self, context):
        node = context.node

        nSockets = len(node.inputs)

        if not nSockets:
            return {'FINISHED'}

        for i in range(nSockets-1, -1, -1):
            s = node.inputs[i]
            if not s.is_linked:
                index = re.findall(r'\d+', s.name)[0]

                brdfSockName   = "BRDF %s" % index
                weightSockName = "Weight %s" % index

                if not node.inputs[brdfSockName].is_linked and not node.inputs[weightSockName].is_linked:          
                    node.inputs.remove(node.inputs[brdfSockName])
                    node.inputs.remove(node.inputs[weightSockName])
                    break

        return {'FINISHED'}


class VRAY_OT_node_add_socket_color(bpy.types.Operator):
    bl_idname      = 'vray.node_add_socket_color'
    bl_label       = "Add Color Socket"
    bl_description = "Adds color socket"

    def execute(self, context):
        return {'FINISHED'}


class VRAY_OT_node_del_socket_color(bpy.types.Operator):
    bl_idname      = 'vray.node_del_socket_color'
    bl_label       = "Remove Color Socket"
    bl_description = "Removes color socket (only not linked sockets will be removed)"

    def execute(self, context):
        return {'FINISHED'}


######## ########  ######## ######## 
   ##    ##     ## ##       ##       
   ##    ##     ## ##       ##       
   ##    ########  ######   ######   
   ##    ##   ##   ##       ##       
   ##    ##    ##  ##       ##       
   ##    ##     ## ######## ######## 

class VRayData:
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in ['VRAY_RENDER', 'VRAY_RENDER_PREVIEW']


class VRayNodeTree(bpy.types.NodeTree, VRayData):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayShaderTreeType'
    bl_icon   = 'VRAY_LOGO'

    # Return a node tree from the context to be used in the editor
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma != None:
                nt_name = ma.vray.nodetree
                if nt_name != '' and nt_name in bpy.data.node_groups:
                    return bpy.data.node_groups[ma.vray.nodetree], ma, ma
        elif ob and ob.type == 'LAMP':
            la = ob.data
            nt_name = la.vray.nodetree
            if nt_name != '' and nt_name in bpy.data.node_groups:
                return bpy.data.node_groups[la.vray.nodetree], la, la
        return (None, None, None)


class VRayTreeNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayShaderTreeType'


 #######  ##     ## ######## ########  ##     ## ######## 
##     ## ##     ##    ##    ##     ## ##     ##    ##    
##     ## ##     ##    ##    ##     ## ##     ##    ##    
##     ## ##     ##    ##    ########  ##     ##    ##    
##     ## ##     ##    ##    ##        ##     ##    ##    
##     ## ##     ##    ##    ##        ##     ##    ##    
 #######   #######     ##    ##         #######     ##    

class VRayNodeOutput(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeOutput'
    bl_label  = 'Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    # BUG: This doesn't work
    def poll_instance(self, node_tree):
        # There could be only one output node
        for n in node_tree.nodes:
            if n.bl_idname == self.bl_idname:
                return None
        return True

    def init(self, context):
        self.inputs.new('VRaySocketMtl', "Material")


 ######   #######   ######  ##    ## ######## ########  ######  
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
##       ##     ## ##       ##  ##   ##          ##    ##       
 ######  ##     ## ##       #####    ######      ##     ######  
      ## ##     ## ##       ##  ##   ##          ##          ## 
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
 ######   #######   ######  ##    ## ########    ##     ######  

class VRaySocketFloatColor(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketFloatColor'
    bl_label  = 'Float color socket'

    value = bpy.props.FloatProperty(
        name = "Value",
        description = "Intensity",
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = 0.5
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, 'value', text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 0.4, 1.00)


class VRaySocketColor(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketColor'
    bl_label  = 'Color socket'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            split = layout.split(percentage=0.3)
            split.prop(self, 'value', text="")
            split.label(text=text)

    def draw_color(self, context, node):
        return (0.250, 0.273, 0.750, 1.00)


class VRaySocketCoords(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketCoords'
    bl_label  = 'Mapping socket'

    value = bpy.props.StringProperty(
        name        = "Defautl Coordinates",
        description = "Defautl coordinates",
        default     = "DEFAULTUVWC"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.250, 0.273, 0.750, 1.00)


class VRaySocketBRDF(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketBRDF'
    bl_label  = 'BRDF socket'

    value = bpy.props.StringProperty(
        name        = "Defautl BRDF",
        description = "Defautl BRDF",
        default     = "BRDFNOBRDFISSET"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.156, 0.750, 0.304, 1.000)


class VRaySocketMtl(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketMtl'
    bl_label  = 'Material socket'

    value = bpy.props.StringProperty(
        name        = "Defautl Material",
        description = "Defautl material",
        default     = "MANOMATERIALISSET"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.000, 0.468, 0.087, 1.000)


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
        self.inputs.new('VRaySocketCoords', "UV")

        self.outputs.new('VRaySocketCoords', "UV")

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
}


def add_nodetype(layout, t):
    layout.operator("node.add_node", text=t.bl_label).type=t.bl_rna.identifier


class VRayNodesMenuOutput(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuOutput"
    bl_label  = "Output"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeOutput)


class VRayNodesMenuMapping(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuMapping"
    bl_label  = "Mapping"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeUVChannel)


class VRayNodesMenuTexture(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuTexture"
    bl_label  = "Texture"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['TEXTURE'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuBRDF(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuBRDF"
    bl_label  = "BRDF"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['BRDF'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuMaterial(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuMaterial"
    bl_label  = "Material"

    def draw(self, context):
        for vrayNodeType in sorted(VRayNodeTypes['MATERIAL'], key=lambda t: t.bl_label):
            add_nodetype(self.layout, vrayNodeType)


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

    for prop in bpyType.bl_rna.properties:
        if prop.name in ['RNA', 'Name']:
            continue
        
        # print("  Property: %s \"%s\" [%s]" % (prop.identifier, prop.name, prop.default))
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
        AddInput(self, 'VRaySocketCoords', "Mapping", 'uvwgen')
        AddOutput(self, 'VRaySocketColor', "Output")
    
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

            if not hasattr(bpy.types, pluginName):
                continue

            vrayPlugin  = PLUGINS[pluginType][pluginName]
            textureBpyType = getattr(bpy.types, pluginName)

            # print("Creating Node from plugin: %s" % (pluginName))

            DynNodeClassName = "VRayNode%s" % (pluginName)

            DynNodeClassAttrs = {
                'bl_idname' : DynNodeClassName,
                'bl_label'  : vrayPlugin.NAME,
                'bl_icon'   : 'VRAY_LOGO',

                'vray_type'   : pluginType,
                'vray_plugin' : pluginName,

                'init'             : VRayNodeInit,
                'draw_buttons'     : VRayNodeDraw,
                'draw_buttons_ext' : VRayNodeDrawSide,
            }

            DynNodeClass = type(            
                DynNodeClassName,               # Name            
                (bpy.types.Node, VRayTreeNode), # Inheritance            
                DynNodeClassAttrs               # Attributes
            )

            bpy.utils.register_class(DynNodeClass)
            
            # Load attributes
            #
            vrayPlugin.add_properties(DynNodeClass)
            
            VRayNodeTypes[pluginType].append(getattr(bpy.types, DynNodeClassName))

            DynamicClasses.append(DynNodeClass)

    # Add manually defined classes
    #
    VRayNodeTypes['BRDF'].append(getattr(bpy.types, 'VRayNodeBRDFLayered'))


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

StaticClasses = [
    VRAY_OT_node_add_brdf_layered_sockets,
    VRAY_OT_node_del_brdf_layered_sockets,
    VRAY_OT_node_add_socket_color,
    VRAY_OT_node_del_socket_color,
    VRAY_OT_add_nodetree,
    
    VRayNodeTree,

    VRaySocketFloatColor,
    VRaySocketColor,
    VRaySocketCoords,
    VRaySocketBRDF,
    VRaySocketMtl,
    
    VRayNodeUVChannel,

    VRayNodeTexLayered,
    
    VRayNodeBRDFLayered,

    VRayNodeOutput,

    VRayNodesMenuTexture,
    VRayNodesMenuBRDF,
    VRayNodesMenuMapping,
    VRayNodesMenuMaterial,
    VRayNodesMenuOutput,
]


def GetRegClasses():
    return StaticClasses


def register():
    LoadDynamicNodes()

    # Menu
    #
    bpy.types.NODE_MT_add.append(VRayNodesMenu)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    for regClass in DynamicClasses:
        bpy.utils.unregister_class(regClass)

    # Menu
    #
    bpy.types.NODE_MT_add.remove(VRayNodesMenu)

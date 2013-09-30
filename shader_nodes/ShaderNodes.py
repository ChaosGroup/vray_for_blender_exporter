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


##     ## ######## #### ##       #### ######## #### ########  ######  
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##       
##     ##    ##     ##  ##        ##     ##     ##  ######    ######  
##     ##    ##     ##  ##        ##     ##     ##  ##             ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
 #######     ##    #### ######## ####    ##    #### ########  ######  

def AddInput(node, socketType, socketName, default=None):
    if socketName in node.inputs:
        return
    node.inputs.new(socketType, socketName)

    if default is not None:
        if socketType == 'NodeSocketColor':
            node.inputs[socketName].default_value = (default[0], default[1], default[2], 1.0)


def AddOutput(node, socketType, socketName):
    if socketName in node.outputs:
        return
    node.outputs.new(socketType, socketName)


def GetNodeTreeFromContex(context):
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

        node.inputs.new('NodeSocketColor', brdfSockName)
        node.inputs.new('NodeSocketFloat', weightSockName)

        node.inputs[weightSockName].default_value = 1.0

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

    # BUG: This doesn't work
    def poll_instance(self, node_tree):
        # There could be only one output node
        for n in node_tree.nodes:
            if n.bl_idname == self.bl_idname:
                return None
        return True

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")
        # self.inputs.new('NodeSocketColor', "Volume")


 ######   #######   ######  ##    ## ######## ########  ######  
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
##       ##     ## ##       ##  ##   ##          ##    ##       
 ######  ##     ## ##       #####    ######      ##     ######  
      ## ##     ## ##       ##  ##   ##          ##          ## 
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
 ######   #######   ######  ##    ## ########    ##     ######  

class VRayCoordsSocket(bpy.types.NodeSocket):
    bl_idname = 'VRayCoordsSocket'
    bl_label  = 'Mapping socket'

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 1.0)


##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ##  ##   ##  
##     ##   ## ##   
 #######     ###   

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
        self.outputs.new('VRayCoordsSocket', "Output")

    def draw_buttons(self, context, layout):
        ob = context.object

        split = layout.split(percentage=0.3)
        split.label(text="Layer:")
        if ob and ob.type == 'MESH':
            split.prop_search(self,    'uv_layer',
                              ob.data, 'uv_textures',
                              text="")
        else:
            split.prop(slot, 'uv_layer', text="")
        
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

            self.inputs.new('NodeSocketColor', texSockName)
            self.inputs.new('NodeSocketFloat', weightSockName)

            self.inputs[weightSockName].default_value = 1.0

        self.outputs.new('NodeSocketColor', "Output")


########  ########  ########  ######## 
##     ## ##     ## ##     ## ##       
##     ## ##     ## ##     ## ##       
########  ########  ##     ## ######   
##     ## ##   ##   ##     ## ##       
##     ## ##    ##  ##     ## ##       
########  ##     ## ########  ##       

class VRayNodeBRDFVRayMtl(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeBRDFVRayMtl'
    bl_label  = 'VRayMtl'
    bl_icon   = 'VRAY_LOGO'

    showAll = bpy.props.BoolProperty(
        name        = "Show All",
        description = "Show all properties",
        default     = False
    )

    def init(self, context):
        self.inputs.new('NodeSocketColor',  "Diffuse")
        self.outputs.new('NodeSocketColor', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'showAll')
        if self.showAll:
            PLUGINS['BRDF']['BRDFVRayMtl'].gui(context, layout.box(), self.BRDFVRayMtl, node=self)

    def draw_buttons_ext(self, context, layout):
        PLUGINS['BRDF']['BRDFVRayMtl'].gui(context, layout, self.BRDFVRayMtl)


class VRayNodeBRDFLayered(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeBRDFLayered'
    bl_label  = 'Layered'
    bl_icon   = 'VRAY_LOGO'

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

            self.inputs.new('NodeSocketColor', brdfSockName)
            self.inputs.new('NodeSocketFloat', weightSockName)

            self.inputs[weightSockName].default_value = 1.0

        self.outputs.new('NodeSocketColor', "Output")

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
    'TEXTURE' : [],
    'BRDF'    : [],
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


class VRayNodesMenuTextures(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuTextures"
    bl_label  = "Textures"

    def draw(self, context):
        for vrayNodeType in VRayNodeTypes['TEXTURE']:
            add_nodetype(self.layout, vrayNodeType)


class VRayNodesMenuBRDF(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenuBRDF"
    bl_label  = "BRDF"

    def draw(self, context):
        for vrayNodeType in VRayNodeTypes['BRDF']:
            add_nodetype(self.layout, vrayNodeType)


def VRayNodesMenu(self, context):
    self.layout.menu("VRayNodesMenuBRDF",     icon='VRAY_LOGO')
    self.layout.menu("VRayNodesMenuTextures", icon='VRAY_LOGO')
    self.layout.menu("VRayNodesMenuMapping",  icon='VRAY_LOGO')
    self.layout.menu("VRayNodesMenuOutput",   icon='VRAY_LOGO')


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
    
    VRayCoordsSocket,
    
    VRayNodeUVChannel,

    VRayNodeTexLayered,
    
    VRayNodeBRDFVRayMtl,
    VRayNodeBRDFLayered,

    VRayNodeOutput,

    VRayNodesMenuTextures,
    VRayNodesMenuBRDF,
    VRayNodesMenuMapping,
    VRayNodesMenuOutput,
]

DynamicClasses = []


def GetRegClasses():
    return StaticClasses


def register():
    global DynamicClasses
    global VRayNodeTypes

    DynamicClasses = []
 
    # Manually defined classes
    #
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    # Load attributes to manually defined classes
    #
    PLUGINS['BRDF']['BRDFVRayMtl'].add_properties(VRayNodeBRDFVRayMtl)

    VRayNodeTypes['BRDF'].append(getattr(bpy.types, 'VRayNodeBRDFVRayMtl'))
    VRayNodeTypes['BRDF'].append(getattr(bpy.types, 'VRayNodeBRDFLayered'))

    # Runtime Node classes generation
    #
    for pluginType in ['TEXTURE', 'BRDF']:
        VRayNodeTypes[pluginType] = []

        for pluginName in sorted(PLUGINS[pluginType]):
            if not pluginName in dir(bpy.types):
                continue

            vrayPlugin  = PLUGINS[pluginType][pluginName]
            textureBpyType = getattr(bpy.types, pluginName)

            # print("Creating Node from plugin: %s" % (pluginName))

            TextureNodeClassName = "VRayNode%s" % (pluginName)

            TextureNodeClassAttrs = {
                'bl_idname'   : TextureNodeClassName,
                'bl_label'    : vrayPlugin.NAME,
                'bl_icon'     : 'VRAY_LOGO',

                'vray_plugin' : pluginName,

                'showAll'     : bpy.props.BoolProperty(
                                    name        = "Show All",
                                    description = "Show all properties",
                                    default     = False
                                ),
            }

            if pluginType == 'TEXTURE':
                def TextureNodeInit(self, context):
                    # print("Plugin: %s" % (self.vray_plugin))

                    texBpyType = getattr(bpy.types, self.vray_plugin)

                    for prop in texBpyType.bl_rna.properties:
                        if prop.name in ['RNA', 'Name']:
                            continue                
                        
                        # print("  Property: %s [%s]" % (prop.name, prop.default))

                        if prop.type == 'FLOAT' and prop.subtype == 'COLOR':
                            if prop.name not in self.inputs:
                                AddInput(self, 'NodeSocketColor', prop.name, prop.default_array)

                    AddInput(self, 'VRayCoordsSocket', "Mapping")

                    AddOutput(self, 'NodeSocketColor', "Output")

                def TextureNodeDraw(self, context, layout):
                    layout.prop(self, 'showAll')

                    if not self.showAll:
                        return
                                
                    vrayPlugin = PLUGINS[pluginType][self.vray_plugin]
                    
                    if not hasattr(vrayPlugin, 'gui'):
                        return

                    vrayPlugin.gui(layout, self.width, getattr(self, self.vray_plugin))

                def TextureNodeDrawSide(self, context, layout):
                    return

                TextureNodeClassAttrs['init']             = TextureNodeInit
                TextureNodeClassAttrs['draw_buttons']     = TextureNodeDraw
                TextureNodeClassAttrs['draw_buttons_ext'] = TextureNodeDrawSide

            else:
                def BRDFNodeInit(self, context):
                    # print("Plugin: %s" % (self.vray_plugin))

                    texBpyType = getattr(bpy.types, self.vray_plugin)

                    for prop in texBpyType.bl_rna.properties:
                        if prop.name in ['RNA', 'Name']:
                            continue                
                        
                        # print("  Property: %s [%s]" % (prop.name, prop.default))

                        if prop.type == 'FLOAT' and prop.subtype == 'COLOR':
                            if prop.name not in self.inputs:
                                AddInput(self, 'NodeSocketColor', prop.name, prop.default_array)

                    AddOutput(self, 'NodeSocketColor', "Output")

                def BRDFNodeDraw(self, context, layout):
                    layout.prop(self, 'showAll')

                    if not self.showAll:
                        return
                                
                    vrayPlugin = PLUGINS[pluginType][self.vray_plugin]
                    
                    if not hasattr(vrayPlugin, 'gui'):
                        return

                    vrayPlugin.gui(layout, self.width, getattr(self, self.vray_plugin))

                def BRDFNodeDrawSide(self, context, layout):
                    return

                TextureNodeClassAttrs['init']             = BRDFNodeInit
                TextureNodeClassAttrs['draw_buttons']     = BRDFNodeDraw
                TextureNodeClassAttrs['draw_buttons_ext'] = BRDFNodeDrawSide

            TextureNodeClass = type(            
                TextureNodeClassName,           # Name            
                (bpy.types.Node, VRayTreeNode), # Inheritance            
                TextureNodeClassAttrs           # Attributes
            )

            bpy.utils.register_class(TextureNodeClass)
            
            # Load attributes
            #
            vrayPlugin.add_properties(TextureNodeClass)
            
            VRayNodeTypes[pluginType].append(getattr(bpy.types, TextureNodeClassName))

            DynamicClasses.append(TextureNodeClass)
  
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

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

import bpy
import mathutils
import re

from pprint import pprint

from vb25.plugins import PLUGINS, load_plugins, gen_menu_items


##     ## ######## #### ##       #### ######## #### ########  ######  
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##       
##     ##    ##     ##  ##        ##     ##     ##  ######    ######  
##     ##    ##     ##  ##        ##     ##     ##  ##             ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
 #######     ##    #### ######## ####    ##    #### ########  ######  

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


##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ##  ##   ##  
##     ##   ## ##   
 #######     ###   

class VRayUVSocket(bpy.types.NodeSocket):
    bl_idname = 'VRayUVSocket'
    bl_label  = 'V-Ray UV generator socket'

    mappingTypes = [
        ("CHAN",  "Channel",   ""),
        ("GEN",   "Generated", ""),
        ("WORLD", "World",     ""),
    ]

    mappingType = bpy.props.EnumProperty(
        name        = "Mapping Type",
        description = "Just an example",
        items       = mappingTypes,
        default     = 'CHAN'
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "mappingType", text=text)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


class VRayNodeUVChannel(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeUVChannel'
    bl_label  = 'VRay UV Channel'
    bl_icon   = 'VRAY_LOGO'

    uv_layer = bpy.props.StringProperty(
        name        = "Layer",
        description = "UV layer name",
        default     = ""
    )

    def init(self, context):
        self.outputs.new('VRayUVSocket', "Output")

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


######## ######## ##     ## ######## ##     ## ########  ######## 
   ##    ##        ##   ##     ##    ##     ## ##     ## ##       
   ##    ##         ## ##      ##    ##     ## ##     ## ##       
   ##    ######      ###       ##    ##     ## ########  ######   
   ##    ##         ## ##      ##    ##     ## ##   ##   ##       
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##       
   ##    ######## ##     ##    ##     #######  ##     ## ######## 

class VRayNodeTexture(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeTexture'
    bl_label  = 'VRay Texture'
    bl_icon   = 'VRAY_LOGO'

    showAll = bpy.props.BoolProperty(
        name        = "Show All",
        description = "Show all properties",
        default     = False
    )

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Diffuse")
        self.inputs.new('VRayUVSocket', "UV")

        self.outputs.new('NodeSocketColor', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'textureType')

        if self.textureType == 'NONE':
            return

        layout.prop(self, 'showAll')
        if self.showAll:
            PLUGINS['TEXTURE'][self.textureType].gui(layout, self.width, getattr(self, self.textureType))


########  ########  ########  ######## 
##     ## ##     ## ##     ## ##       
##     ## ##     ## ##     ## ##       
########  ########  ##     ## ######   
##     ## ##   ##   ##     ## ##       
##     ## ##    ##  ##     ## ##       
########  ##     ## ########  ##       

class VRayNodeBRDFVRayMtl(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeBRDFVRayMtl'
    bl_label  = 'BRDFVRayMtl'
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
    bl_label  = 'BRDFLayered'
    bl_icon   = 'VRAY_LOGO'

    additive_mode = bpy.props.BoolProperty(
        name        = "Additive Mode",
        description = "Additive mode",
        default     = False
    )

    def init(self, context):
        for i in range(2):
            brdfSockName   = "BRDF %i" % i
            weightSockName = "Weight %i" % i

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

def add_nodetype(layout, t):
    layout.operator("node.add_node", text=t.bl_label).type=t.bl_rna.identifier


def vray_shader_nodes_menu(self, context):
    self.layout.menu("VRayNodesMenu", icon='VRAY_LOGO')


class VRayNodesMenu(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenu"
    bl_label  = "V-Ray Nodes"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeBRDFVRayMtl)
        add_nodetype(self.layout, bpy.types.VRayNodeBRDFLayered)
        add_nodetype(self.layout, bpy.types.VRayNodeTexture)
        add_nodetype(self.layout, bpy.types.VRayNodeUVChannel)
        add_nodetype(self.layout, bpy.types.VRayNodeOutput)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

def GetRegClasses():
    return (
        VRAY_OT_node_add_brdf_layered_sockets,
        VRAY_OT_node_del_brdf_layered_sockets,
        VRAY_OT_node_add_socket_color,
        VRAY_OT_node_del_socket_color,
        VRAY_OT_add_nodetree,
        VRayNodeTree,
        VRayUVSocket,
        VRayNodeUVChannel,
        VRayNodeBRDFVRayMtl,
        VRayNodeTexture,
        VRayNodeBRDFLayered,
        VRayNodeOutput,
        VRayNodesMenu,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    PLUGINS['BRDF']['BRDFVRayMtl'].add_properties(VRayNodeBRDFVRayMtl)

    load_plugins(PLUGINS['TEXTURE'], VRayNodeTexture)

    VRayNodeTexture.textureType = bpy.props.EnumProperty(
        name        = "Texture Type",
        description = "V-Ray texture type",
        items       = gen_menu_items(PLUGINS['TEXTURE']),
        default     = 'NONE'
    )

    bpy.types.NODE_MT_add.append(vray_shader_nodes_menu)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.NODE_MT_add.remove(vray_shader_nodes_menu)

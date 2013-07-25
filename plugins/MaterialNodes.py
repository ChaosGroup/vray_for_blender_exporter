#
# V-Ray/Blender
#
# http://vray.cgdo.ru
#
# Author: Andrey M. Izrantsev (aka bdancer)
# E-Mail: izrantsev@cgdo.ru
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

from vb25.plugins import BRDFVRayMtl


TYPE = 'NODE'
ID   = 'MaterialNodes'
NAME = 'MaterialNodes'
PID  = 1


# Shortcut for node type menu
#
def add_nodetype(layout, t):
    layout.operator("node.add_node", text=t.bl_label).type=t.bl_rna.identifier


class VRayData:
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in ['VRAY_RENDER', 'VRAY_RENDER_PREVIEW']


# V-Ray Nodes menu
#
class VRayNodesMenu(bpy.types.Menu, VRayData):
    bl_idname = "VRayNodesMenu"
    bl_label  = "V-Ray Nodes"

    def draw(self, context):
        add_nodetype(self.layout, bpy.types.VRayNodeVRayMtl)
        add_nodetype(self.layout, bpy.types.VRayNodeBRDFLayered)
        add_nodetype(self.layout, bpy.types.VRayNodeOutput)


# Menu extention function for 'NODE_MT_add'
#
def vray_shader_nodes_menu(self, context):
    self.layout.menu("VRayNodesMenu", icon='VRAY_LOGO')


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

    # BUG: This doesn't work. Using manual menu extension by now
    #
    def draw_add_menu(self, context, layout):
        layout.label("V-Ray")
        add_nodetype(layout, bpy.types.VRayTestNode)


class MyCustomSocket(bpy.types.NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = 'Custom Node Socket'

    # Enum items list
    my_items = [
        ("DOWN", "Down", "Where your feet are"),
        ("UP", "Up", "Where your head should be"),
        ("LEFT", "Left", "Not right"),
        ("RIGHT", "Right", "Not left")
    ]

    myEnumProperty = bpy.props.EnumProperty(name="Direction", description="Just an example", items=my_items, default='UP')

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "myEnumProperty", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Base class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class VRayTreeNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'VRayShaderTreeType'


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

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")
        self.inputs.new('NodeSocketColor', "Volume")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        # print("Copying from node ", node)
        pass

    # Free function to clean up on removal.
    def free(self):
        #print("Removing node ", self, ", Goodbye!")
        pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        # layout.label("Node settings")
        # layout.prop(self, "myFloatProperty")
        # layout.prop(self, "myStringProperty")
        pass

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        # layout.menu("VRayNodesMenu", icon='VRAY_LOGO', text="Create Node")
        pass


class VRayNodeBRDFVRayMtl(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeVRayMtl'
    bl_label  = 'VRayMtl'
    bl_icon   = 'VRAY_LOGO'

    showAll = bpy.props.BoolProperty(
        name        = "Show All",
        description = "Show all properties",
        default     = False
    )

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Diffuse")
        self.outputs.new('NodeSocketColor', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'showAll')

        if self.showAll:
            BRDFVRayMtl.gui(context, layout.box(), self.BRDFVRayMtl, node=self)

    def draw_buttons_ext(self, context, layout):
        BRDFVRayMtl.gui(context, layout, self.BRDFVRayMtl)


class VRayNodeBRDFLayered(bpy.types.Node, VRayTreeNode):
    bl_idname = 'VRayNodeBRDFLayered'
    bl_label  = 'VRayBlendMtl'
    bl_icon   = 'VRAY_LOGO'

    additive_mode = bpy.props.BoolProperty(
        name        = "Additive Mode",
        description = "Additive mode",
        default     = False
    )

    def init(self, context):
        # BUG: Adding new sockets doesn't update existing nodes
        #
        self.inputs.new('NodeSocketColor', "Material1")
        self.inputs.new('NodeSocketFloat', "Weight1")

        self.inputs.new('NodeSocketColor', "Material2")
        self.inputs.new('NodeSocketFloat', "Weight2")

        self.inputs.new('NodeSocketColor', "Material3")
        self.inputs.new('NodeSocketFloat', "Weight3")

        self.outputs.new('NodeSocketColor', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'additive_mode')


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


def register():
    bpy.utils.register_class(VRayNodeTree)
    bpy.utils.register_class(MyCustomSocket)

    bpy.utils.register_class(VRayNodeBRDFVRayMtl)
    BRDFVRayMtl.add_properties(VRayNodeBRDFVRayMtl)

    bpy.utils.register_class(VRayNodeBRDFLayered)
    bpy.utils.register_class(VRayNodeOutput)

    bpy.utils.register_class(VRayNodesMenu)

    bpy.utils.register_class(VRAY_OT_add_nodetree)

    bpy.types.NODE_MT_add.append(vray_shader_nodes_menu)


def unregister():
    bpy.utils.unregister_class(VRayNodeTree)
    bpy.utils.unregister_class(MyCustomSocket)

    bpy.utils.unregister_class(VRayNodeBRDFVRayMtl)
    bpy.utils.unregister_class(VRayNodeBRDFLayered)
    bpy.utils.unregister_class(VRayNodeOutput)

    bpy.utils.unregister_class(VRayNodesMenu)

    bpy.utils.unregister_class(VRAY_OT_add_nodetree)

    bpy.types.NODE_MT_add.remove(vray_shader_nodes_menu)

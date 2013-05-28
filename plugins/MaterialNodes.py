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


TYPE = 'NODE'
ID   = 'MaterialNodes'
NAME = 'MaterialNodes'
PID  = 1


# Shortcut for node type menu
def add_nodetype(layout, type):
    layout.operator("node.add_node", text=type.bl_label).type = type.bl_rna.identifier


class VRayNodeTree(bpy.types.NodeTree):
    bl_label  = "V-Ray Node Tree"
    bl_idname = 'VRayShaderTreeType'
    bl_icon   = 'MATERIAL'

    @classmethod
    def poll(cls, context):
        return True
        return context.scene.render.engine in ['VRAY_RENDER', 'VRAY_RENDER_PREVIEW']

    # Return a node tree from the context to be used in the editor
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma != None:
                nt_name = ma.vray.nodetree
                if nt_name != '':
                    return bpy.data.node_groups[ma.vray.nodetree], ma, ma
        elif ob and ob.type == 'LAMP':
            la = ob.data
            nt_name = la.vray.nodetree
            if nt_name != '':
                return bpy.data.node_groups[la.vray.nodetree], la, la
        return (None, None, None)

    def draw_add_menu(self, context, layout):
        layout.label("V-Ray")
        add_nodetype(layout, bpy.types.VRayCustomNode)


# Base class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class VRayTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'VRayShaderTreeType'


class VRayCustomNode(bpy.types.Node, VRayTreeNode):
    bl_label  = 'V-Ray Node'
    bl_idname = 'VRayTestNode'
    bl_icon   = 'VRAY_LOGO'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    myStringProperty = bpy.props.StringProperty()
    myFloatProperty = bpy.props.FloatProperty(default=3.1415926)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('CustomSocketType', "Hello")
        self.inputs.new('NodeSocketFloat', "World")
        self.inputs.new('NodeSocketVector', "!")

        self.outputs.new('NodeSocketColor', "How")
        self.outputs.new('NodeSocketColor', "are")
        self.outputs.new('NodeSocketFloat', "you")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label("Node settings")
        layout.prop(self, "myFloatProperty")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "myFloatProperty")
        # myStringProperty button will only be visible in the sidebar
        layout.prop(self, "myStringProperty")


# A customized group-like node.
class MyCustomGroup(bpy.types.NodeGroup, VRayTreeNode):
    # === Basics ===
    # Description string
    '''A custom group node'''
    # Label for nice name display
    bl_label = 'Custom Group Node'
    bl_group_tree_idname = 'CustomTreeType'

    orks = bpy.props.IntProperty(default=3)
    dwarfs = bpy.props.IntProperty(default=12)
    wizards = bpy.props.IntProperty(default=1)

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "orks")
        col.prop(self, "dwarfs")
        col.prop(self, "wizards")

        layout.label("The Node Tree:")
        layout.prop(self, "node_tree", text="")


def register():
    bpy.utils.register_class(VRayNodeTree)
    bpy.utils.register_class(VRayCustomNode)


def unregister():
    bpy.utils.unregister_class(VRayNodeTree)
    bpy.utils.unregister_class(VRayCustomNode)


if __name__ == "__main__":
    register()

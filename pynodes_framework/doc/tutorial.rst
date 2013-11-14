**************************
PyNodes Framework Tutorial
**************************

This tutorial will guide you through the basic steps of creating a node interface utilizing the pynodes framework. The examples used here are minimal in functionality beyond the node editor for the sake of clarity.

A node interface can be used as a frontend for a python-based component system. In this tutorial we will use nodes to define simple mathematical expressions such as "(4 + 3) / 3.1415", and then evaluate them with an operator. For a more complex example please check out the "Modifier Nodes" addon: TODO

* The Node Tree Type *

The node tree type is a central part of each node system. The Blender node editor works on one node tree at a time and many of its features are centered around it, such as context switching and certain operators.

import bpy
from pynodes_framework import *

class MathNodeTree(bpy.types.NodeTree, node_base.NodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"
    
Note that this class is based on both the standard node tree class from bpy.types as well as the node_base class from the pynodes framework. This aggregation principle is used in other classes too. It makes it easier to create complex class structures and control registration with the Blender RNA.

** Node tree poll **

The new "Math" tree type will show up in the Blender node editor as a selection item with the "PLUS" icon. If you want to hide the node tree under certain circumstances, define the optional poll function:

import bpy
from pynodes_framework import *

class MathNodeTree(bpy.types.NodeTree, node_base.NodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"

    def poll(self, context):
        # only show in the editor if active object is an empty
        return context.active_object and context.active_object.type == 'EMPTY'

** Node Categorizer **

The node category system was implemented to simplify the creation of 'Add' menus, toolbar panels and the search operator for adding nodes. The pynodes framework adds a small python class on top of this to simplify categorizing nodes without having to create and maintain an explicit list.

import bpy
from pynodes_framework import *

class MathNodeTree(bpy.types.NodeTree, node_base.NodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"
    
math_node_category = node_category.NodeCategorizer(MathNodeTree)

This math_node_category object can be used as a decorator on node classes. For examples see TODO below.

** Registering Classes **

In order to actually use our new classes we have to first register them with the RNA system. This is standard procedure in bpy scripts:

import bpy
from pynodes_framework import *

class MathNodeTree(bpy.types.NodeTree, node_base.NodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"
    
math_node_category = node_category.NodeCategorizer(MathNodeTree)

def register():
    bpy.utils.register_module(__name__)

    math_node_category.register()

def unregister():
    math_node_category.unregister()

    bpy.utils.unregister_module(__name__)

# this is useful for re-registering when scripts are reloaded with F8
if __name__ == "__main__":
    register()

If you want to have more control over which types actually get registered you can also register individual classes manually, instead of everything in the module:

def register():
    bpy.utils.register_class(MathNodeTree)
    # add any later node or UI classes here

    math_node_category.register()

def unregister():
    math_node_category.unregister()

    bpy.utils.unregister_class(MathNodeTree)
    # add any later node or UI classes here

* Our first nodes *

At this point you can run the script and it will show the new node tree type in the node editor. Time to add actual nodes. The two classes below shall become our first simple nodes for doing basic arithmetic.

import bpy
from pynodes_framework import *

class MathNodeTree(bpy.types.NodeTree, node_base.NodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"
    
math_node_category = node_category.NodeCategorizer(MathNodeTree)

class AddNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeAdd"
    bl_label = "Add"

class SubtractNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeSubtract"
    bl_label = "Subtract"

def register():
    bpy.utils.register_module(__name__)

    math_node_category.register()

def unregister():
    math_node_category.unregister()

    bpy.utils.unregister_module(__name__)

** Categorizing Nodes **

After running this script you can see the new types as "bpy.types.MathNodeAdd", "bpy.typesMathNodeSubtract" in the python console. But they are not showing up in the Add menu, the toolbar or the Search operator yet. For this we need to put them into a category, which will become a submenu/panel in the UI:

@math_node_category("Arithmetic")
class AddNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeAdd"
    bl_label = "Add"

@math_node_category("Arithmetic")
class SubtractNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeSubtract"
    bl_label = "Add"

** Adding Sockets **

Now you can add nodes comfortably in the UI. But when you do you will notice they don't have any inputs or outputs yet, which makes them rather useless.

With the pynodes framework adding input/output sockets to nodes is very similar to adding bpy.props to other Blender types (see for example TODO). Without the framework you need to call API functions on the node.inputs/node.outputs collections explicitly, and also define properties for input values yourself. The pynodes framework combines all this in a simple oneliner:

@math_node_category("Arithmetic")
class AddNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeAdd"
    bl_label = "Add"

    input_a = NodeParam(datatype="FLOAT", label="Value")
    input_b = NodeParam(datatype="FLOAT", label="Value")
    result = NodeParam(datatype="FLOAT", label="Result", is_output=True)

@math_node_category("Arithmetic")
class SubtractNode(bpy.types.Node, node_base.Node):
    bl_idname = "MathNodeSubtract"
    bl_label = "Add"

    input_a = NodeParam(datatype="FLOAT", label="Value")
    input_b = NodeParam(datatype="FLOAT", label="Value")
    result = NodeParam(datatype="FLOAT", label="Result", is_output=True)

After these changes any newly added node will have 2 input sockets and 1 output socket, providing the interface for a typical binary arithmetic operator.

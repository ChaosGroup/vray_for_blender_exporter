# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from pynodes_framework import base, category
from pynodes_framework.parameter import *

class MathNodeSocket(bpy.types.NodeSocket, base.NodeSocket):
    bl_idname = "MathNodeSocket"
    parameter_types = [NodeParamFloat]

class MathNodeTree(bpy.types.NodeTree, base.NodeTree, category.CategoryNodeTree):
    bl_idname = "MathNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Math"
    socket_type = MathNodeSocket

class MathNode(base.Node):
    socket_type = MathNodeSocket

    # Determines if we can add a node to some tree.
    @classmethod
    def poll(cls, node_tree):
        return node_tree and isinstance(node_tree, MathNodeTree)


category_arithmetic = MathNodeTree.add_category("Arithmetic", "Arithmetic math operations", hint=0)



@category_arithmetic()
class AddNode(bpy.types.Node, MathNode):
    bl_idname = "MathNodeAdd"
    bl_label = "Add"

    input_a = NodeParamFloat(name="Value")
    input_b = NodeParamFloat(name="Value")
    result = NodeParamFloat(name="Result", is_output=True)

@category_arithmetic()
class SubtractNode(bpy.types.Node, MathNode):
    bl_idname = "MathNodeSubtract"
    bl_label = "Subtract"

    input_a = NodeParamFloat(name="Value")
    input_b = NodeParamFloat(name="Value")
    result = NodeParamFloat(name="Result", is_output=True)


def register():
    bpy.utils.register_class(MathNodeSocket)
    bpy.utils.register_class(MathNodeTree)
    bpy.utils.register_class(AddNode)
    bpy.utils.register_class(SubtractNode)

    MathNodeTree.register_categories()

def unregister():
    MathNodeTree.unregister_categories()

    bpy.utils.unregister_class(MathNodeSocket)
    bpy.utils.unregister_class(MathNodeTree)
    bpy.utils.unregister_class(AddNode)
    bpy.utils.unregister_class(SubtractNode)

if __name__ == "__main__":
    register()

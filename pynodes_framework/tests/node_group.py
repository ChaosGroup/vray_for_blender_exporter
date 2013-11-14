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
from pynodes_framework import base, category, group
from pynodes_framework.parameter import *

class ExampleNodeSocket(bpy.types.NodeSocket, base.NodeSocket):
    bl_idname = "ExampleNodeSocket"
    parameter_types = [NodeParamFloat]

#! base.NodeTree is included in group.NodeGroupTree
class ExampleNodeTree(bpy.types.NodeTree, group.NodeGroupTree, category.CategoryNodeTree):
    bl_idname = "ExampleNodeTree"
    bl_icon = 'PLUS'
    bl_label = "Example"
    socket_type = ExampleNodeSocket

class ExampleNode(base.Node):
    socket_type = ExampleNodeSocket

    # Determines if we can add a node to some tree.
    @classmethod
    def poll(cls, node_tree):
        return node_tree and isinstance(node_tree, ExampleNodeTree)


category_group = ExampleNodeTree.add_category("Group", "Node groups", hint=1)



@category_group(10)
class GroupNode(bpy.types.Node, ExampleNode, group.NodeGroup):
    bl_idname = "ExampleNodeGroup"
    bl_label = "Group"

    # Poll function for the nodetree property
    def nodetree_poll(self, nodetree):
        return isinstance(nodetree, ExampleNodeTree)


@category_group(1)
class GroupInputNode(bpy.types.Node, ExampleNode, group.NodeGroupInput):
    bl_idname = "ExampleNodeGroupInput"
    bl_label = "Group Input"


@category_group(2)
class GroupOutputNode(bpy.types.Node, ExampleNode, group.NodeGroupOutput):
    bl_idname = "ExampleNodeGroupOutput"
    bl_label = "Group Output"


def register():
    #! For node groups each parameter class needs to register a "template" class,
    # which defines the properties in the interface.
    NodeParamFloat.register_template()

    bpy.utils.register_class(ExampleNodeSocket)
    #! NodeGroupTree subclasses require specialized registration function (RNA quirks)
    ExampleNodeTree.register_class()
    bpy.utils.register_class(GroupNode)
    bpy.utils.register_class(GroupInputNode)
    bpy.utils.register_class(GroupOutputNode)

    ExampleNodeTree.register_categories()

def unregister():
    NodeParamFloat.unregister_template()

    bpy.utils.unregister_class(ExampleNodeSocket)
    ExampleNodeTree.unregister_class()
    bpy.utils.unregister_class(GroupNode)
    bpy.utils.unregister_class(GroupInputNode)
    bpy.utils.unregister_class(GroupOutputNode)

    ExampleNodeTree.unregister_categories()

if __name__ == "__main__":
    register()

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
from bpy.types import Menu, Operator, Panel, PropertyGroup, UIList
from bpy_types import RNAMetaPropGroup
from bpy.props import *
from bpy.app.handlers import persistent
from mathutils import *

from pynodes_framework import base, parameter
from pynodes_framework.idref import IDRefProperty, draw_idref
from pynodes_framework.dyn_property_group import *
from itertools import chain


"""
def _rna_node_subclasses(base):
    for c in base.__subclasses__():
        if issubclass(c, bpy.types.Node):
            yield c
        else:
            for sc in _rna_node_subclasses(c):
                yield sc
"""

def _generate_identifier(basename, check_duplicate=None):
    import re
    # remove non-alphanumeric chars
    type_basename = re.sub('[^a-zA-Z0-9_]', '', basename)
    # make it unique by appending a number if necessary
    type_name = type_basename
    if check_duplicate:
        unum = 1
        while check_duplicate(type_name):
            unum += 1
            type_name = "%s_%d" % (type_basename, unum)
    return type_name


def _generate_interface_item_type(prefix, parameter_types):
    """Creates a PropertyGroup for NodeGroupTree interface collections"""

    name = "%s_InterfaceItem" % prefix

    def interface_update(self, context):
        nodetree = self.id_data
        nodetree.update_interface()
    datatype_enum = parameter.parameter_enum(parameter_types)
    attr = {
        "name"          : StringProperty(name="Name", update=interface_update),
        "identifier"    : StringProperty(name="Identifier", description="Unique identifier string", options={'HIDDEN'}),
        "datatype"      : EnumProperty(name="Data Type", description="Data type of the socket", items=datatype_enum, options=set(), update=interface_update),
        "use_socket"    : BoolProperty(name="Use Socket", description="Create a socket for this parameter", default=True, update=interface_update),
        "make_socket"   : lambda self, node, is_output: self.template().make_socket(node, is_output, self.name, self.identifier),
        "verify_socket" : lambda self, socket: self.template().verify_socket(socket, self.name),
        "draw_socket"   : lambda self, layout, data, prop, text: self.template().draw_socket(layout, data, prop, text),
        "color"         : property(fget=lambda self: self.template().color),
        }

    # PropertyGroup that defines parameter details
    cls = type(name, (PropertyGroup,), attr)

    # this maps the parameter type to the associated class
    template_type_map = { pt.datatype_identifier : pt.template_type for pt in parameter_types }
    # register a dynamic pointer based on the parameter type
    bpy_register_dynpointer(cls, "template",
                            DynPointerProperty(name="Template", description="Template for generating a node socket",
                                               refine=lambda self: template_type_map[self.datatype]))
    for pt in parameter_types:
        bpy_register_dynpointer_type(cls, "template", pt.template_type)
    return cls

class MetaNodeGroupTree(RNAMetaPropGroup):
    def __new__(cls, name, bases, attr):
        tree_cls = RNAMetaPropGroup.__new__(cls, name, bases, attr)

        # Generate a PropertyGroup for interface items
        socket_type = getattr(tree_cls, "socket_type", None)
        if socket_type:
            item_cls = _generate_interface_item_type(name, socket_type.parameter_types)
            # store in the tree class to associate them
            tree_cls.interface_item_type = item_cls

            tree_cls.interface_inputs = CollectionProperty(name="Inputs", description="Interface inputs", type=item_cls)
            tree_cls.interface_outputs = CollectionProperty(name="Outputs", description="Interface outputs", type=item_cls)

        return tree_cls

# Mix-in base class for trees supported in node groups
class NodeGroupTree(base.NodeTree, metaclass=MetaNodeGroupTree):
    @classmethod
    def register_class(cls):
        bpy.utils.register_class(cls.interface_item_type)
        bpy.utils.register_class(cls)

    @classmethod
    def unregister_class(cls):
        bpy.utils.unregister_class(cls)
        bpy.utils.unregister_class(cls.interface_item_type)

    ### Interface Collections ###
    # NB: interface collections get defined in MetaNodeGroupTree, since they require a custom RNA type

    # update callback ensures only either an input or output item is active, never both
    # trick: to avoid cyclic updates, set the id property directly, this bypasses the RNA property
    def _active_interface_input_update(self, context):
        if self.active_interface_input >= 0:
            self["active_interface_output"] = -1
    def _active_interface_output_update(self, context):
        if self.active_interface_output >= 0:
            self["active_interface_input"] = -1
    active_interface_input = IntProperty(name="Active Input", default=-1, update=_active_interface_input_update)
    active_interface_output = IntProperty(name="Active Output", default=-1, update=_active_interface_output_update)

    next_interface_uuid = IntProperty(name="Next Interface UUID", description="Next unique index for interface items", default=1)

    def _interface_item_add(self, collection, active_prop, name, datatype, **kw):
        # set this in advance to prevent unnecessary updates
        self._update_interface = True

        item = collection.add()

        item.identifier = "item_%d" % self.next_interface_uuid
        self.next_interface_uuid += 1

        item.name = name
        item.datatype = datatype
        for attr, value in kw.items():
            setattr(item, attr, value)

        setattr(self, active_prop, len(collection) - 1)

        self.update_interface()

        return item

    def _interface_item_remove(self, collection, active_prop, index):
        # set this in advance to prevent unnecessary updates
        self._update_interface = True

        collection.remove(index)

        active = getattr(self, active_prop)
        if active > index:
            setattr(self, active_prop, max(min(active - 1, len(collection) - 1), -1))
        else:
            setattr(self, active_prop, min(active, len(collection) - 1))

        self.update_interface()

    def _interface_item_move(self, collection, active_prop, from_index, to_index):
        # sanity check
        if from_index < 0 or from_index >= len(collection) or to_index < 0 or to_index >= len(collection):
            return

        # set this in advance to prevent unnecessary updates
        self._update_interface = True

        collection.move(from_index, to_index)

        active = getattr(self, active_prop)
        if active == from_index:
            setattr(self, active_prop, to_index)
        elif active > from_index and active <= to_index:
            setattr(self, active_prop, active - 1)

        self.update_interface()

    def interface_input_add(self, name, datatype, **kw):
        return self._interface_item_add(self.interface_inputs, "active_interface_input", name, datatype, **kw)
    def interface_input_remove(self, index):
        return self._interface_item_remove(self.interface_inputs, "active_interface_input", index)
    def interface_input_move(self, from_index, to_index):
        return self._interface_item_move(self.interface_inputs, "active_interface_input", from_index, to_index)

    def interface_output_add(self, name, datatype, **kw):
        return self._interface_item_add(self.interface_outputs, "active_interface_output", name, datatype, **kw)
    def interface_output_remove(self, index):
        return self._interface_item_remove(self.interface_outputs, "active_interface_output", index)
    def interface_output_move(self, from_index, to_index):
        return self._interface_item_move(self.interface_outputs, "active_interface_output", from_index, to_index)

    #def update(self):
    #    self._do_update_interface()

    # Register the property group used for storing interface values
    # Register properties in that group for each interface item
    def _rna_interface_props_type_verify(self):
        def check_duplicate(identifier):
            for nodetree in bpy.data.node_groups:
                if isinstance(nodetree, NodeGroupTree) and nodetree.get("_rna_identifier", "") == identifier:
                    return True
            return False

        identifier = self.get("_rna_identifier", None)

        if identifier is not None and check_duplicate(identifier):
            # XXX the existing nodes need to be updated
            # THIS IS A PROBLEM! e.g. when using linked node trees etc.

            # delete the previous type
            name = "PyNodesGroupProperties__%s" % identifier
            prop_cls = getattr(bpy.types, name, None)
            if prop_cls:
                bpy_unregister_dynpointer_type(PyNodesGroupInterface, "properties", prop_cls)
                bpy.utils.unregister_class(prop_cls)
            identifier = None

        if identifier is None:
            # generate a new unique identifier
            identifier = _generate_identifier(self.name, check_duplicate)
            self["_rna_identifier"] = identifier

            # create a property group for interface values
            name = "PyNodesGroupProperties__%s" % identifier
            prop_cls = type(name, (PropertyGroup,), {})

            # register in bpy and as a DynPointer type in PyNodesGroupInterface
            bpy.utils.register_class(prop_cls)
            bpy_register_dynpointer_type(PyNodesGroupInterface, "properties", prop_cls)

            # store for lookup later
            self["_rna_interface_props_type"] = name

        # create the actual properties for interface sockets
        for item in chain(self.interface_inputs, self.interface_outputs):
            prop = item.template().prop(item.name)
            if prop:
                setattr(self.interface_props_type, item.identifier, prop)

    # Unregister the property group for interface values
    def _rna_interface_props_type_unregister(self):
        identifier = self.get("_rna_identifier", None)
        if identifier is None:
            return

        name = "PyNodesGroupProperties__%s" % identifier
        prop_cls = getattr(bpy.types, name, None)
        if prop_cls:
            bpy_unregister_dynpointer_type(PyNodesGroupInterface, "properties", prop_cls)
            bpy.utils.unregister_class(prop_cls)


    @property
    def interface_props_type(self):
        name = self.get("_rna_interface_props_type", None)
        return None if name is None else getattr(bpy.types, name, None)

    @classmethod
    def _bpy_nodetrees(cls):
        """ Utility generator for iterating over node trees in bpy.data """
        if hasattr(bpy.data, "node_groups"): # handles _RestrictData case when we can't access bpy.data
            for nodetree in bpy.data.node_groups:
                if isinstance(nodetree, cls):
                    yield nodetree

    @classmethod
    def _bpy_nodes(cls, nodetype=None):
        """ Utility generator for iterating over nodes in bpy.data """
        for nodetree in cls._bpy_nodetrees():
            for node in nodetree.nodes:
                if nodetype is None or isinstance(node, nodetype):
                    yield node

    def _do_update_interface(self):
        if not self.get("_update_interface", False):
            return

        self._rna_interface_props_type_verify()

        # update sockets in group and interface nodes
        for node in self._bpy_nodes(NodeInterfaceBase):
            if node._interface_nodetree == self:
                node._verify_sockets()

        self["_update_interface"] = False

    def update_interface(self):
        if not self.get("_update_interface", False):
            self["_update_interface"] = True
            self._do_update_interface()

# Verify the RNA for all the node group trees
def _rna_verify_all_groups():
    for nodetree in NodeGroupTree._bpy_nodetrees():
        nodetree._rna_interface_props_type_verify()

# Unregister the RNA for all the node group trees
def _rna_unregister_all_groups():
    for nodetree in NodeGroupTree._bpy_nodetrees():
        nodetree._rna_interface_props_type_unregister()

# Handler for verifying node group tree RNA after file load
@persistent
def _on_load_rna_verify_all_groups(dummy):
    _rna_verify_all_groups()


# XXX Intermediate PropertyGroup type to store interface properties.
# This is necessary because when creating the properties pointer directly in NodeInterfaceBase
# it cannot be updated afterward, since NodeInterfaceBase is not a RNA struct type itself ...
class PyNodesGroupInterface(PropertyGroup, metaclass=MetaDynPointerContainer(RNAMetaPropGroup)):
    def _properties_refine(self, node):
        nodetree = node._interface_nodetree
        return None if nodetree is None else nodetree.interface_props_type
    properties = DynPointerProperty(name="Interface Properties", description="Values for a group node interface", refine=_properties_refine)

# XXX has to be registered here to work for PointerProperty
bpy.utils.register_class(PyNodesGroupInterface)


# Serves as a base class for group nodes and input/output nodes
class NodeInterfaceBase(base.Node):
    interface = PointerProperty(name="Interface", description="Interface values for node groups", type=PyNodesGroupInterface)

    def socket_data(self):
        # the interface.properties group holds all the group interface values
        return self.interface.properties(self)


class NodeGroup(NodeInterfaceBase):
    # recursion check function, False if any node group in the tree contains self already
    def contains_nodetree(self, nodetree):
        if self.nodetree is None:
            return False
        elif self.nodetree == nodetree:
            return True
        else:
            for node in self.nodetree.nodes:
                if isinstance(node, NodeGroup) and node.contains_nodetree(nodetree):
                    return True
        return False

    def nodetree_poll_recursion(self, value):
        # recursion check function, False if any node group in the tree contains self already
        def contains_self(nodetree):
            if nodetree is None:
                return False
            for node in nodetree.nodes:
                if node == self:
                    return True
                elif isinstance(node, NodeGroup) and contains_self(node.nodetree):
                    return True
            return False

        # additional custom poll function from subclasses to check for certain types
        # NB: subclasses MUST define this poll function themselves!
        if not self.nodetree_poll(value):
            return False
        if contains_self(value):
            return False
        return True

    def nodetree_update(self, context):
        self._verify_sockets()

    nodetree = IDRefProperty("Node Tree", "Internal node tree of the group", idtype='NODETREE', options={'FAKE_USER'},
                             poll=nodetree_poll_recursion, update=nodetree_update)

    @property
    def _interface_nodetree(self):
        return self.nodetree

    def node_parameters(self, output):
        for param in super().node_parameters(output):
            yield param

        if self.nodetree is not None:
            if output:
                for temp in self.nodetree.interface_outputs:
                    yield temp
            else:
                for temp in self.nodetree.interface_inputs:
                    yield temp

    def draw_buttons(self, context, layout):
        draw_idref(layout, self, "nodetree")

    def poll_instance(self, nodetree):
        # avoid recursion
        if self.contains_nodetree(nodetree):
            return False


class NodeGroupInput(NodeInterfaceBase):
    bl_label = "Group Input"

    @property
    def _interface_nodetree(self):
        return self.id_data

    def node_parameters(self, output):
        for param in super().node_parameters(output):
            yield param

        # NB: inverted inputs/outputs for interface nodes
        if output:
            for temp in self.id_data.interface_inputs:
                yield temp

    def init(self, context):
        # ensure we add existing interface sockets
        self._verify_sockets()


class NodeGroupOutput(NodeInterfaceBase):
    bl_label = "Group Output"

    @property
    def _interface_nodetree(self):
        return self.id_data

    def node_parameters(self, output):
        for param in super().node_parameters(output):
            yield param

        # NB: inverted inputs/outputs for interface nodes
        if not output:
            for temp in self.id_data.interface_outputs:
                yield temp

    def init(self, context):
        # ensure we add existing interface sockets
        self._verify_sockets()


### Node Group UI ###

class PyNodesTreeInterfaceListInputs(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        active_index = getattr(active_data, active_propname)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            op = layout.operator("pynodes.tree_interface_remove", text="", icon='X', emboss=False)
            op.in_out = 'IN'
            op.index = index
            layout.template_node_socket(item.template().color)
            if index == active_index:
                layout.prop(item, "name", text="", translate=False)
            else:
                layout.label(text=item.name, translate=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.template_node_socket(item.template().color)


class PyNodesTreeInterfaceListOutputs(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        active_index = getattr(active_data, active_propname)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if index == active_index:
                layout.prop(item, "name", text="", translate=False)
            else:
                layout.label(text=item.name, translate=False)
            layout.template_node_socket(item.template().color)
            op = layout.operator("pynodes.tree_interface_remove", text="", icon='X', emboss=False)
            op.in_out = 'OUT'
            op.index = index
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.template_node_socket(item.template().color)


class PyNodesTreeInterfacePanel(Panel):
    bl_idname = "PYNODES_PT_tree_interface_panel"
    bl_label = "Interface"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if not space.edit_tree:
            return False
        if not isinstance(space.edit_tree, NodeGroupTree):
            return False
        return True

    def draw(self, context):
        space = context.space_data
        nodetree = space.edit_tree
        layout = self.layout

        row = layout.row(align=False)
        row.alignment = 'CENTER'

        row.menu("pynodes.tree_interface_add_input_menu", text="", icon='PLUS')

        row2 = row.row(align=True)
        op = row2.operator("pynodes.tree_interface_move", text="", icon='TRIA_DOWN')
        op.direction = 'DOWN'
        op = row2.operator("pynodes.tree_interface_move", text="", icon='TRIA_UP')
        op.direction = 'UP'

        row.menu("pynodes.tree_interface_add_output_menu", text="", icon='PLUS')

        split = layout.split(0.5, align=True)
        split.template_list("PyNodesTreeInterfaceListInputs", "inputs", nodetree, "interface_inputs", nodetree, "active_interface_input")
        split.template_list("PyNodesTreeInterfaceListOutputs", "outputs", nodetree, "interface_outputs", nodetree, "active_interface_output")

        if nodetree.active_interface_input >= 0:
            active = nodetree.interface_inputs[nodetree.active_interface_input]
        elif nodetree.active_interface_output >= 0:
            active = nodetree.interface_outputs[nodetree.active_interface_output]
        else:
            active = None

        if active is not None:
            layout.prop(active, "name")
            layout.prop(active, "datatype")

            active.template().draw(layout, context)


### Node Group Operators ###

in_out_items = [
    ('IN',  "In",  "Input"),
    ('OUT', "Out", "Output"),
    ]

def _poll_group_tree_active(cls, context):
    space = context.space_data
    if space.type != 'NODE_EDITOR':
        return False
    if space.edit_tree is None:
        return False
    if not isinstance(space.edit_tree, NodeGroupTree):
        return False
    # XXX we need all these node types specified, can this be done nicer?
    if not (hasattr(space.edit_tree, "group_node_type") and hasattr(space.edit_tree, "group_node_input_type") and hasattr(space.edit_tree, "group_node_output_type")):
        return False
    return True

class PyNodesGroupEdit(Operator):
    """ Open or close a node group """
    bl_idname = "pynodes.group_edit"
    bl_label = "Edit"
    bl_options = {'REGISTER', 'UNDO'}

    exit = BoolProperty(name="Exit", description="Exit the current group node", default=False)

    poll = classmethod(_poll_group_tree_active)

    def execute(self, context):
        space = context.space_data
        node = context.active_node

        exit = self.exit

        if not isinstance(node, NodeGroup):
            exit = True
        elif node.nodetree is None:
            return {'CANCELLED'}

        if exit:
            space.path.pop()
        else:
            space.path.push(node.nodetree, node)

        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


# always copy these node properties
_node_properties_include = {'name'}
# but don't copy other generic node properties
_node_properties_exclude = set(bpy.types.Node.bl_rna.properties.keys()) - _node_properties_include

def _nodes_bbox(nodes):
    xmin = xmax = ymin = ymax = 0.0
    first = True
    for node in nodes:
        width, height = node.dimensions[:]
        nxmin, nymax = node.location[:]
        # location is upper left corner
        nxmax = nxmin + width
        nymin = nymax - height

        if first:
            xmin, xmax, ymin, ymax = nxmin, nxmax, nymin, nymax
            first = False
        else:
            if xmin > nxmin:
                xmin = nxmin
            if xmax < nxmax:
                xmax = nxmax
            if ymin > nymin:
                ymin = nymin
            if ymax < nymax:
                ymax = nymax

    return (xmin, ymin, xmax, ymax)

class PyNodesGroupMake(Operator):
    """Create a new node group from selected nodes"""
    bl_idname = "pynodes.group_make"
    bl_label = "Make from selected"
    bl_options = {'REGISTER', 'UNDO'}

    use_only_selected = BoolProperty(name="Only Selected", description="Allow only selected nodes in the group", default=True)
    open_new_group = BoolProperty(name="Open New Group", description="Open the node group as the active tree after creating it", default=False)

    poll = classmethod(_poll_group_tree_active)

    def test_nodes(self, ntree):
        """Test connections of selected nodes to ensure they can be grouped together"""

        def input_nodes(node):
            for link in ntree.links:
                if link.to_node == node:
                    yield link.from_node

        def output_nodes(node):
            for link in ntree.links:
                if link.from_node == node:
                    yield link.to_node

        # these are selected OR have selected nodes on the input AND output side
        grouped_nodes = set()
        # these are NOT selected and have NO selected nodes on the input side
        free_input_nodes = set()
        # these are NOT selected and have NO selected nodes on the output side
        free_output_nodes = set()

        visited = set()
        error = False
        def test_recursive(node):
            if node in visited:
                return
            visited.add(node)

            if node.select:
                is_grouped_node = True
            else:
                is_free_input = True
                for inode in input_nodes(node):
                    test_recursive(inode)
                    if inode not in free_input_nodes:
                        is_free_input = False
                if is_free_input:
                    free_input_nodes.add(node)

                is_free_output = True
                for onode in output_nodes(node):
                    test_recursive(onode)
                    if onode not in free_output_nodes:
                        is_free_output = False
                if is_free_output:
                    free_output_nodes.add(node)

                # nodes are not in the group if all inputs or all outputs are free
                is_grouped_node = not (is_free_input or is_free_output)

                if is_grouped_node and self.use_only_selected:
                    self.report({'ERROR'}, "Cannot make group, unselected node %r has selected inputs and outputs" % node.name)
                    error = True

            if is_grouped_node:
                grouped_nodes.add(node)

        for node in ntree.nodes:
            test_recursive(node)

        return grouped_nodes, error

    def copy_node(self, oldnew_map, ngroup, node, offset):
        # attributes to copy to the new node
        def attributes():
            for attr in node.bl_rna.properties.keys():
                if attr not in _node_properties_exclude:
                    yield attr

        new_node = ngroup.nodes.new(type=node.bl_idname)
        oldnew_map[node] = new_node

        for attr in attributes():
            setattr(new_node, attr, getattr(node, attr))

        # location follows simple layout
        new_node.location = node.location + offset

        for socket in node.inputs:
            oldnew_map[socket] = (new_node, new_node._find_input(socket.identifier)[1])
        for socket in node.outputs:
            oldnew_map[socket] = (new_node, new_node._find_output(socket.identifier)[1])

        return new_node

    def execute(self, context):
        space = context.space_data
        ntree = space.edit_tree

        grouped_nodes, error = self.test_nodes(ntree)
        if error or not grouped_nodes:
            return {'CANCELLED'}

        # create group tree of same type as the edit tree
        ngroup = bpy.data.node_groups.new("NodeGroup", ntree.bl_idname)

        oldnew_map = {}

        # extent of the node selection, for basic layout
        bbox = _nodes_bbox(grouped_nodes)
        # offset such that nodes are centered
        offset = 0.5*(Vector((bbox[0], bbox[1])) + Vector((bbox[2], bbox[3])))

        for node in grouped_nodes:
            self.copy_node(oldnew_map, ngroup, node, -offset)

        # input/output nodes in the group
        input_node = ngroup.nodes.new(type=ntree.group_node_input_type)
        input_offset = Vector((-input_node.width, 30.0))
        input_node.location = Vector((bbox[0] - 100.0 - offset[0], 0.0)) + input_offset
        output_node = ngroup.nodes.new(type=ntree.group_node_output_type)
        output_offset = Vector((0.0, 30.0))
        output_node.location = Vector((bbox[2] + 100.0 - offset[0], 0.0)) + output_offset

        # create an instance of the new group in place of the previous nodes
        gnode = ntree.nodes.new(type=ntree.group_node_type)
        gnode.nodetree = ngroup
        gnode_offset = Vector((-0.5*gnode.width, 30.0))
        gnode.location = offset + gnode_offset

        for link in ntree.links:
            new_from_node, new_from_socket = oldnew_map.get(link.from_socket, (None, None))
            new_to_node, new_to_socket = oldnew_map.get(link.to_socket, (None, None))

            if new_from_socket and new_to_socket:
                # internal group link
                ngroup.links.new(new_from_socket, new_to_socket)

            elif new_from_socket:
                # link from group output
                item = ngroup.interface_output_add(link.from_socket.name, link.from_socket.datatype)
                item.template().from_param(link.from_node.find_node_parameter(link.from_socket))

                _, output_to_socket = output_node._find_input(item.identifier)
                ngroup.links.new(new_from_socket, output_to_socket)

                _, output_from_socket = gnode._find_output(item.identifier)
                ntree.links.new(output_from_socket, link.to_socket)

            elif new_to_socket:
                # link to group input
                item = ngroup.interface_input_add(link.to_socket.name, link.to_socket.datatype)
                item.template().from_param(link.to_node.find_node_parameter(link.to_socket))

                _, input_from_socket = input_node._find_output(item.identifier)
                ngroup.links.new(input_from_socket, new_to_socket)

                _, input_to_socket = gnode._find_input(item.identifier)
                ntree.links.new(link.from_socket, input_to_socket)

        # remove previous nodes, they're now in the group
        for node in grouped_nodes:
            ntree.nodes.remove(node)

        # make the new node active
        gnode.select = True
        ntree.nodes.active = gnode

        # deselect nodes in the group by default
        for node in ngroup.nodes:
            node.select = False
        ngroup.nodes.active = None

        # open the new node group
        if self.open_new_group:
            space.path.push(ngroup, gnode)

        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class _PyNodesTreeInterfaceAddMenuBase():
    def draw(self, context):
        ntree = context.space_data.edit_tree
        if ntree is None:
            return

        layout = self.layout
        for pt in ntree.socket_type.parameter_types:
            row = layout.row()

            # XXX FIXME messes up the layout for some reason
            #row.template_node_socket(pt.color)

            op = row.operator("pynodes.tree_interface_add", text=pt.datatype_name)
            op.in_out = self.in_out
            op.name = self.name
            op.datatype = pt.datatype_identifier

class PyNodesTreeInterfaceAddInputMenu(_PyNodesTreeInterfaceAddMenuBase, Menu):
    bl_idname = "pynodes.tree_interface_add_input_menu"
    bl_label = "Add Input"
    name = "Input"
    in_out = "IN"

class PyNodesTreeInterfaceAddOutputMenu(_PyNodesTreeInterfaceAddMenuBase, Menu):
    bl_idname = "pynodes.tree_interface_add_output_menu"
    bl_label = "Add Output"
    name = "Output"
    in_out = "OUT"


class PyNodesTreeInterfaceAdd(Operator):
    """ Add an interface item to the node tree """
    bl_idname = "pynodes.tree_interface_add"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    in_out = EnumProperty(name="In Out", description="Input or Output", items=in_out_items, default='IN')
    name = StringProperty(name="Name", description="Interface item name", default="")
    def _datatype_enum(self, context):
        space = context.space_data
        if space.type != 'NODE_EDITOR' or space.edit_tree is None:
            return []
        return parameter.parameter_enum(space.edit_tree.socket_type.parameter_types)
    datatype = EnumProperty(name="Data Type", items=_datatype_enum)

    def execute(self, context):
        space = context.space_data
        nodetree = space.edit_tree
        if self.in_out == 'IN':
            nodetree.interface_input_add(self.name, self.datatype)
        elif self.in_out == 'OUT':
            nodetree.interface_output_add(self.name, self.datatype)
        return {'FINISHED'}


class PyNodesTreeInterfaceRemove(Operator):
    """ Remove an interface item of the node tree """
    bl_idname = "pynodes.tree_interface_remove"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}

    in_out = EnumProperty(name="In Out", description="Input or Output", items=in_out_items, default='IN')
    index = IntProperty(name="Index", default=-1)

    def execute(self, context):
        space = context.space_data
        nodetree = space.edit_tree
        if self.in_out == 'IN':
            nodetree.interface_input_remove(self.index)
        elif self.in_out == 'OUT':
            nodetree.interface_output_remove(self.index)
        return {'FINISHED'}


class PyNodesTreeInterfaceMove(Operator):
    """ Move the active interface item of the node tree """
    bl_idname = "pynodes.tree_interface_move"
    bl_label = "Move"
    bl_options = {'REGISTER', 'UNDO'}

    direction_items = [
        ("UP",      "Up",       ""),
        ("DOWN",    "Down",     ""),
        ]

    direction = EnumProperty(name="Direction", description="Up or Down", items=direction_items, default='UP')

    def execute(self, context):
        space = context.space_data
        nodetree = space.edit_tree

        delta = 1 if self.direction == 'DOWN' else -1
        active_input = nodetree.active_interface_input
        active_output = nodetree.active_interface_output
        if active_input >= 0:
            nodetree.interface_input_move(active_input, active_input + delta)
        elif active_output >= 0:
            nodetree.interface_output_move(active_output, active_output + delta)
        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(PyNodesTreeInterfaceListInputs)
    bpy.utils.register_class(PyNodesTreeInterfaceListOutputs)
    bpy.utils.register_class(PyNodesTreeInterfacePanel)

    bpy.utils.register_class(PyNodesGroupEdit)
    bpy.utils.register_class(PyNodesGroupMake)
    bpy.utils.register_class(PyNodesTreeInterfaceAddInputMenu)
    bpy.utils.register_class(PyNodesTreeInterfaceAddOutputMenu)
    bpy.utils.register_class(PyNodesTreeInterfaceAdd)
    bpy.utils.register_class(PyNodesTreeInterfaceRemove)
    bpy.utils.register_class(PyNodesTreeInterfaceMove)

    # keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')

    kmi = km.keymap_items.new(PyNodesGroupEdit.bl_idname, 'TAB', 'PRESS')
    kmi = km.keymap_items.new(PyNodesGroupEdit.bl_idname, 'TAB', 'PRESS', shift=True)
    kmi.properties.exit = True

    kmi = km.keymap_items.new(PyNodesGroupMake.bl_idname, 'G', 'PRESS', ctrl=True)
    kmi.properties.use_only_selected = False

    addon_keymaps.append((km, kmi))

    _rna_verify_all_groups()
    bpy.app.handlers.load_post.append(_on_load_rna_verify_all_groups)

def unregister():
    for handler in bpy.app.handlers.load_post:
        if handler == _on_load_rna_verify_all_groups:
            bpy.app.handlers.load_post.remove(handler)
    _rna_unregister_all_groups()

    # keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(PyNodesTreeInterfaceListInputs)
    bpy.utils.unregister_class(PyNodesTreeInterfaceListOutputs)
    bpy.utils.unregister_class(PyNodesTreeInterfacePanel)

    bpy.utils.unregister_class(PyNodesGroupEdit)
    bpy.utils.unregister_class(PyNodesGroupMake)
    bpy.utils.unregister_class(PyNodesTreeInterfaceAddInputMenu)
    bpy.utils.unregister_class(PyNodesTreeInterfaceAddOutputMenu)
    bpy.utils.unregister_class(PyNodesTreeInterfaceAdd)
    bpy.utils.unregister_class(PyNodesTreeInterfaceRemove)
    bpy.utils.unregister_class(PyNodesTreeInterfaceMove)

    bpy.utils.unregister_class(PyNodesGroupInterface)

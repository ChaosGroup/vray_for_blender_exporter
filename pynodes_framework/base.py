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
from bpy.types import PropertyGroup
from bpy_types import StructRNA, RNAMetaPropGroup, OrderedDictMini
from bpy.props import *
from collections import OrderedDict
from pynodes_framework.parameter import *
from pynodes_framework.idref import MetaIDRefContainer


class MetaNodeSocket(RNAMetaPropGroup):
    def __new__(cls, name, bases, classdict):
        socket_cls = RNAMetaPropGroup.__new__(cls, name, bases, classdict)

        # define the "datatype" property
        socket_cls.datatype = EnumProperty(name="Data Type", items=parameter_enum(socket_cls.parameter_types))

        return socket_cls

class NodeSocket(metaclass=MetaNodeSocket):
    parameter_types = [] # should be defined in subclasses

    # shortcut to the property value, needs explicit node
    def value(self, node):
        return getattr(node.socket_data(), self.identifier)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text)
        else:
            node.find_node_parameter(self).draw_socket(layout, node.socket_data(), self.identifier, text)

    def draw_color(self, context, node):
        return node.find_node_parameter(self).color


class NodeTree():
    pass


class NodeOrderedDict(dict):
    def __init__(self, *args):
        dict.__init__(self, args)
        self.node_parameters = OrderedDict()

    def __setitem__(self, key, value):
        if isinstance(value, NodeParameter):
            # use the attribute name as the parameter identifier
            value.identifier = key
            # make sure the param replacement is appended at the end
            if key in self.node_parameters:
                del self.node_parameters[key]
            self.node_parameters[key] = value
        else:
            dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        if key in self.node_parameters:
            del self.node_parameters[key]


class MetaNode(MetaIDRefContainer(RNAMetaPropGroup)):
    def __prepare__(name, bases, **kwargs):
        return NodeOrderedDict()

    def _verify_parameter(self, param):
        if param.prop:
            setattr(self, param.identifier, param.prop)

    def __setattr__(self, key, value):
        if isinstance(value, NodeParameter):
            # use the attribute name as the parameter identifier
            value.identifier = key
            # make sure the param replacement is appended at the end
            if key in self._node_type_parameters:
                del self._node_type_parameters[key]
            self._node_type_parameters[key] = value

            self._verify_parameter(value)
        else:
            super().__setattr__(key, value)

    def __new__(cls, name, bases, classdict):
        # Wrapper for node.init, to add sockets from templates
        init_base = classdict.get('init', None)
        def init_node(self, context):
            self._verify_sockets()
            if init_base:
                init_base(self, context)
        classdict["init"] = init_node

        if classdict.__class__ is NodeOrderedDict:
            node_type_parameters = classdict.node_parameters
        else:
            node_type_parameters = OrderedDict()
        classdict["_node_type_parameters"] = node_type_parameters

        nodecls = super().__new__(cls, name, bases, classdict)

        # Dynamic UI draw functions list for appending custom draw snippets
        # Unlike other Blender GenericUI classes this avoids changing the draw_buttons
        # class attribute later on, so it can be wrapper further by other metaclasses down the line.
        draw_buttons_sub = getattr(nodecls, "draw_buttons", None)
        def draw_buttons(self, context, layout):
            if draw_buttons_sub:
                draw_buttons_sub(self, context, layout)

            # ensure menus always get default context
            operator_context_default = layout.operator_context

            for func in nodecls._draw_funcs:
                # so bad menu functions don't stop
                # the entire menu from drawing
                try:
                    func(self, context, layout)
                except:
                    import traceback
                    traceback.print_exc()

                layout.operator_context = operator_context_default

        nodecls.draw_buttons = draw_buttons
        nodecls._draw_funcs = []

        # Add properties from node type parameters
        for param in node_type_parameters.values():
            nodecls._verify_parameter(param)

        return nodecls


class Node(metaclass=MetaNode):
    def _find_input(self, identifier):
        for i, socket in enumerate(self.inputs):
            if socket.identifier == identifier:
                return i, socket
        return -1, None
    def _find_output(self, identifier):
        for i, socket in enumerate(self.outputs):
            if socket.identifier == identifier:
                return i, socket
        return -1, None

    def socket_data(self):
        return self

    def node_parameters(self, output):
        for param in self._node_type_parameters.values():
            if param.is_output == output:
                yield param

    def find_node_parameter(self, socket):
        for param in self.node_parameters(socket.is_output):
            if param.identifier == socket.identifier:
                return param
        raise KeyError("Node parameter %r not found in %s" % (socket.identifier, "outputs" if socket.is_output else "inputs"))

    def _verify_sockets(self):
        for output in {False, True}:
            if output:
                sockets = self.outputs
                find_socket = self._find_output
            else:
                sockets = self.inputs
                find_socket = self._find_input

            unused = { socket for socket in sockets }

            socket_index = 0
            for param in self.node_parameters(output):
                if not param.use_socket:
                    continue

                pos, socket = find_socket(param.identifier)
                if socket:
                    param.verify_socket(socket)
                    sockets.move(pos, socket_index)
                    unused.remove(socket)
                    socket_index += 1
                else:
                    socket = param.make_socket(self, output)
                    if socket:
                        assert(socket.identifier == param.identifier)
                        # socket gets appended at the end, move to correct position
                        sockets.move(len(sockets)-1, socket_index)
                        socket_index += 1

            # remove unused old sockets
            # XXX unset old properties here!
            for socket in unused:
                sockets.remove(socket)

    ### Dynamic UI ###
    # copied from bpy_types._GenericUI

    def draw_buttons(self, context, layout):
        pass

    @classmethod
    def append(cls, draw_func):
        """
        Append a draw function to this node,
        takes the same arguments as the node draw_buttons function
        """
        cls._draw_funcs.append(draw_func)

    @classmethod
    def prepend(cls, draw_func):
        """
        Prepend a draw function to this node, takes the same arguments as
        the node draw_buttons function
        """
        cls._draw_funcs.insert(0, draw_func)

    @classmethod
    def remove(cls, draw_func):
        """Remove a draw function that has been added to this node"""
        try:
            cls._draw_funcs.remove(draw_func)
        except:
            pass

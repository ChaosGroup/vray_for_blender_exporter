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

import bpy, bmesh, mathutils
from bpy_types import RNAMetaPropGroup
from bpy.types import PropertyGroup
from bpy.props import *
from mathutils import *
from copy import deepcopy
from pynodes_framework.idref import IDRefProperty

def _set_prop_update(prop, update):
    if prop is None:
        return

    if isinstance(prop, tuple): # standard bpy.props
        # property types that don't support update callback (uses the builtin function to detect them)
        if prop[0] in { CollectionProperty()[0] }:
            return

        # don't want to overwrite, should be defined as a subclass attribute
        assert(prop[1].get("update", None) is None)
        prop[1]["update"] = update

    elif isinstance(prop, IDRefProperty):
        # don't want to overwrite, should be defined as a subclass attribute
        assert(getattr(prop, "update", None) is None)
        prop.update = update

def _prop_dict(prop):
    if prop is None:
        return {}

    if isinstance(prop, tuple): # standard bpy.props
        return prop[1]

    elif isinstance(prop, IDRefProperty):
        return prop.__dict__


def _link_limit(is_output):
    return 0 if is_output else 1

def _make_socket(template, node, is_output, name, identifier):
    coll = node.outputs if is_output else node.inputs
    socket = coll.new(type=node.socket_type.bl_idname, name=name, identifier=identifier)
    socket.datatype = template.datatype_identifier
    socket.link_limit = _link_limit(is_output)

    return socket

def _verify_socket(template, socket, name):
    socket.name = name
    socket.datatype = template.datatype_identifier
    socket.link_limit = _link_limit(socket.is_output)

# NB: This class is not directly based on PropertyGroup because RNA register check
# requires the StructRNA type to be first base ...
# PropertyGroup base is added in the MetaNodeParameter class below!
class NodeParameter__Template():
    """Base class for node parameter template"""

    def make_socket(self, node, is_output, name, identifier):
        return _make_socket(self, node, is_output, name, identifier)

    def verify_socket(self, socket, name):
        _verify_socket(self, socket, name)

def _generate_parameter_template(param_cls):
    """Construct a template PropertyGroup that defines a parameter"""

    # copy attributes from param_cls, with a few exceptions that don't work for PropertyGroup
    attr_exclude = set(dir(NodeParameter)) | { '__init__', '__new__', 'template_properties', 'template_draw' }
    attr = { key : getattr(param_cls, key) for key in dir(param_cls) if key not in attr_exclude }

    attr["draw"] = param_cls.template_draw
    attr["draw_socket"] = param_cls.draw_socket

    # insert template_properties dict
    for name, prop in param_cls.template_properties.items():
        # make a copy of the property definition
        # this prevents issues when making further subclasses,
        # using the same property dictionary
        prop_copy = deepcopy(prop)

        # property update callback to trigger group node updates
        def template_update(self, context):
            nodetree = self.id_data
            nodetree.update_interface()
        _set_prop_update(prop_copy, template_update)

        # insert into the class dict
        attr[name] = prop_copy

    # function for generating a RNA property, using the parameter class constructor
    template_prop_args = param_cls.template_properties.keys()
    def template_prop(self, name):
        kw = { arg : getattr(self, arg) for arg in template_prop_args }
        param = param_cls(name=name, is_output=False, use_socket=True, **kw)
        return param.prop
    attr["prop"] = template_prop

    def template_from_param(self, param):
        """Copy property details from an existing socket parameter to a template"""
        props = _prop_dict(param.prop)
        for arg in template_prop_args:
            if arg in props:
                setattr(self, arg, props.get(arg))
    attr["from_param"] = template_from_param

    temp_cls = type("%s__Template" % param_cls.__name__, (PropertyGroup, NodeParameter__Template), attr)
    return temp_cls


class MetaNodeParameter(type):
    def __new__(cls, name, bases, classdict):
        param_cls = type.__new__(cls, name, bases, classdict)

        if hasattr(param_cls, "datatype_identifier"):
            temp_cls = _generate_parameter_template(param_cls)
            # associate the parameter class to the template class
            param_cls.template_type = temp_cls

        return param_cls

class NodeParameter(metaclass=MetaNodeParameter):
    # define in subclasses if needed
    def value_update(node, context):
        pass

    def __init__(self, name, is_output=False, use_socket=True, prop=None):
        _set_prop_update(prop, self.__class__.value_update)

        self.name = name
        self.prop = prop
        self.is_output = is_output
        self.use_socket = use_socket

    def make_socket(self, node, is_output):
        return _make_socket(self, node, is_output, self.name, self.identifier)

    def verify_socket(self, socket):
        _verify_socket(self, socket, self.name)

    def draw_socket(self, layout, data, prop, text):
        layout.label(text=text)

    template_properties = {}

    def template_draw(self, layout, context):
        pass

    @classmethod
    def register_template(cls):
        bpy.utils.register_class(cls.template_type)

    @classmethod
    def unregister_template(cls):
        bpy.utils.unregister_class(cls.template_type)


def parameter_enum(parameter_types):
    """Generates RNA enum items from a list of parameter types"""
    return [(pt.datatype_identifier, pt.datatype_name, "" if pt.__doc__ is None else pt.__doc__) for pt in parameter_types]


################################
### Standard Parameter Types ###
################################

# some utilities for easy filtering of invalid bpy.props arguments

def dict_key_union(d, include):
    return { key : value for key, value in d if key in include }

def dict_key_diff(d, exclude):
    return { key : value for key, value in d if key not in exclude }

def _filter_kw(kw, propfunc, exclude=set()):
    # XXX inspect does not with bpy builtin functions, ah well ...
#    import inspect
#    valid = set(inspect.getargspec(propfunc)[0]) - { "name", "description" } - exclude
    invalid = { "name", "description" } | exclude
    return { key : value for key, value in kw.items() if key not in invalid }


class NodeParamFloat(NodeParameter):
    """Floating point number"""
    datatype_identifier = "FLOAT"
    datatype_name = "Float"
    color = (0.63, 0.63, 0.63, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatProperty(name, **_filter_kw(kw, FloatProperty)))

    def draw_socket(self, layout, data, prop, text):
        layout.prop(data, prop, text=text)

    template_properties = {
        "default"       : FloatProperty(name="Default"),
        "subtype"       : EnumProperty(name="Subtype", default="NONE", items = [
                            ("NONE",        "None",         ""),
                            ("UNSIGNED",    "Unsigned",     ""),
                            ("PERCENTAGE",  "Percentage",   ""),
                            ("FACTOR",      "Factor",       ""),
                            ("ANGLE",       "Angle",        ""),
                            ("TIME",        "Time",         ""),
                            ("DISTANCE",    "Distance",     ""),
                            ]),
        "min"           : FloatProperty(name="Minimum", default=-10000),
        "max"           : FloatProperty(name="Maximum", default=10000),
        "soft_min"      : FloatProperty(name="Button Minimum", default=-1000),
        "soft_max"      : FloatProperty(name="Button Maximum", default=1000),
        "precision"     : IntProperty(name="Precision", default=2),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "subtype")
        layout.prop(self, "default")
        row = layout.row()
        col = row.column(align=True)
        col.prop(self, "min", text="Min")
        col.prop(self, "max", text="Max")
        col = row.column(align=True)
        col.prop(self, "soft_min", text="UI Min")
        col.prop(self, "soft_max", text="UI Max")
        layout.prop(self, "precision")

class NodeParamInt(NodeParameter):
    """Integer number"""
    datatype_identifier = "INT"
    datatype_name = "Int"
    color = (0.06, 0.52, 0.15, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=IntProperty(name, **_filter_kw(kw, IntProperty)))

    def draw_socket(self, layout, data, prop, text):
        layout.prop(data, prop, text=text)

    template_properties = {
        "default" : IntProperty(name="Default"),
        "subtype" : EnumProperty(name="Subtype", default="NONE", items = [
                            ("NONE",        "None",         ""),
                            ("UNSIGNED",    "Unsigned",     ""),
                            ("PERCENTAGE",  "Percentage",   ""),
                            ("FACTOR",      "Factor",       ""),
                            ("ANGLE",       "Angle",        ""),
                            ("TIME",        "Time",         ""),
                            ("DISTANCE",    "Distance",     ""),
                            ]),
        "min"           : IntProperty(name="Minimum", default=-10000),
        "max"           : IntProperty(name="Maximum", default=10000),
        "soft_min"      : IntProperty(name="Button Minimum", default=-1000),
        "soft_max"      : IntProperty(name="Button Maximum", default=1000),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")
        layout.prop(self, "subtype")
        row = layout.row()
        col = row.column(align=True)
        col.prop(self, "min", text="Min")
        col.prop(self, "max", text="Max")
        col = row.column(align=True)
        col.prop(self, "soft_min", text="UI Min")
        col.prop(self, "soft_max", text="UI Max")

class NodeParamBool(NodeParameter):
    """Boolean value"""
    datatype_identifier = "BOOL"
    datatype_name = "Bool"
    color = (0.70, 0.65, 0.19, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=BoolProperty(name, **_filter_kw(kw, BoolProperty)))

    def draw_socket(self, layout, data, prop, text):
        layout.prop(data, prop, text=text)

    template_properties = {
        "default" : BoolProperty(name="Default"),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")

class NodeParamVector(NodeParameter):
    """Generic 3D vector"""
    datatype_identifier = "VECTOR"
    datatype_name = "Vector"
    color = (0.39, 0.39, 0.78, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, expand=False, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatVectorProperty(name, size=3, **_filter_kw(kw, FloatVectorProperty, {'size'})))
        self.expand = expand

    def draw_socket(self, layout, data, prop, text):
        if self.expand:
            layout.prop(data, prop, text="", expand=True)
        else:
            layout.template_component_menu(data, prop, name=text)

    template_properties = {
        "default" : FloatVectorProperty(name="Default", size=3),
        "subtype" : EnumProperty(name="Subtype", default="NONE", items = [
                    ("NONE",            "None",             ""),
                    ("TRANSLATION",     "Translation",      ""),
                    ("DIRECTION",       "Direction",        ""),
                    ("VELOCITY",        "Velocity",         ""),
                    ("ACCELERATION",    "Acceleration",     ""),
                    ("EULER",           "Euler",            ""),
                    ("XYZ",             "XYZ",              ""),
                    ]),
        "expand" : BoolProperty(name="Expand", description="Expand items list in the UI", default=False),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")
        layout.prop(self, "subtype")
        layout.prop(self, "expand")

class NodeParamPoint(NodeParameter):
    """3D position vector"""
    datatype_identifier = "POINT"
    datatype_name = "Point"
    color = (0.39, 0.39, 0.78, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, expand=False, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatVectorProperty(name, size=3, subtype='TRANSLATION', **_filter_kw(kw, FloatVectorProperty, {'size'})))
        self.expand = expand

    def draw_socket(self, layout, data, prop, text):
        if self.expand:
            layout.prop(data, prop, text="", expand=True)
        else:
            layout.template_component_menu(data, prop, name=text)

    template_properties = {
        "default" : FloatVectorProperty(name="Default", size=3, subtype='TRANSLATION'),
        "expand" : BoolProperty(name="Expand", description="Expand items list in the UI", default=False),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")
        layout.prop(self, "expand")

class NodeParamNormal(NodeParameter):
    """Normalized 3D direction vector"""
    datatype_identifier = "NORMAL"
    datatype_name = "Normal"
    color = (0.39, 0.39, 0.78, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, expand=False, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatVectorProperty(name, size=3, subtype='DIRECTION', **_filter_kw(kw, FloatVectorProperty, {'size'})))
        self.expand = expand

    def draw_socket(self, layout, data, prop, text):
        if self.expand:
            layout.prop(data, prop, text="", expand=True)
        else:
            layout.template_component_menu(data, prop, name=text)

    template_properties = {
        "default" : FloatVectorProperty(name="Default", size=3, subtype='DIRECTION'),
        "expand" : BoolProperty(name="Expand", description="Expand items list in the UI", default=False),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")
        layout.prop(self, "expand")

class NodeParamString(NodeParameter):
    """String"""
    datatype_identifier = "STRING"
    datatype_name = "String"
    color = (1.00, 1.00, 1.00, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=StringProperty(name, **_filter_kw(kw, StringProperty)))

    def draw_socket(self, layout, data, prop, text):
        row = layout.row()
        row.prop(data, prop, text="")
        row.label(text=text)

    template_properties = {
        "default" : StringProperty(name="Default"),
        "subtype" : EnumProperty(name="Subtype", default="NONE", items = [
                    ("NONE",            "None",             ""),
                    ("FILE_PATH",       "File Path",        ""),
                    ("DIR_PATH",        "Directory Path",   ""),
                    ("FILE_NAME",       "File Name",        ""),
                    ]),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")
        layout.prop(self, "subtype")

class NodeParamEnumItem(PropertyGroup):
    identifier = StringProperty(name="Identifier")
    description = StringProperty(name="Description")

class NodeParamEnum(NodeParameter):
    """Value from a predefined set of options"""
    datatype_identifier = "ENUM"
    datatype_name = "Enum"
    color = (0.06, 0.52, 0.15, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, expand=False, **kw):
        # XXX TODO convert item collection argument into valid RNA enum items list
        NodeParameter.__init__(self, name, is_output, use_socket, prop=EnumProperty(name, **kw))
        self.expand = expand

    def draw_socket(self, layout, data, prop, text):
        layout.prop(data, prop, text=text, expand=self.expand)

    def _template_default_items(self, context):
        return [(item.name, item.description, 'NONE') for item in self.items]
    template_properties = {
        "default" : EnumProperty(name="Default", items=_template_default_items),
        "items" : CollectionProperty(name="Items", type=NodeParamEnumItem),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")

class NodeParamColor(NodeParameter):
    """RGBA color"""
    datatype_identifier = "COLOR"
    datatype_name = "Color"
    color = (0.78, 0.78, 0.16, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatVectorProperty(name, size=4, subtype='COLOR', min=0.0, max=1.0,
                               **_filter_kw(kw, FloatVectorProperty, {'size', 'subtype', 'min', 'max'})))

    def draw_socket(self, layout, data, prop, text):
        row = layout.row()
        row.alignment = 'LEFT'
        row.prop(data, prop, text="")
        row.label(text=text)

    template_properties = {
        "default" : FloatVectorProperty(name="Default", size=4, subtype='COLOR', min=0.0, max=1.0),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")

class NodeParamMatrix(NodeParameter):
    """4x4 transformation matrix"""
    datatype_identifier = "MATRIX"
    datatype_name = "Matrix"
    color = (0.07, 0.59, 0.80, 1.0)

    def __init__(self, name, is_output=False, use_socket=True, **kw):
        # convert matrix value into flat sequence
        default = kw.get("default", None)
        if default is not None and isinstance(default, Matrix):
            kw["default"] = (c for r in default[0:4] for c in r[0:4])
        NodeParameter.__init__(self, name, is_output, use_socket, prop=FloatVectorProperty(name, size=16, subtype='MATRIX', **_filter_kw(kw, FloatVectorProperty, {'size', 'subtype'})))

    template_properties = {
        "default" : FloatVectorProperty(name="Default", size=16, subtype='MATRIX'),
        }

    def template_draw(self, layout, context):
        layout.prop(self, "default")

# Default set of parameter types
#parameter_types_all = [NodeParamFloat, NodeParamInt, NodeParamBool, NodeParamColor,
#                       NodeParamVector, NodeParamPoint, NodeParamNormal, NodeParamMatrix,
#                       NodeParamString, NodeParamEnum]

#def register():
#    bpy.utils.register_class(NodeParamEnumItem)
#    for pt in parameter_types_all:
#        pt.register_template()

#def unregister():
#    bpy.utils.unregister_class(NodeParamEnumItem)
#    for pt in parameter_types_all:
#        pt.unregister_template()

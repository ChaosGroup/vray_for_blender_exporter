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

from bpy.props import PointerProperty
from bpy.types import PropertyGroup


### Dynamic PointerProperty ###

def _type_attr(attr, t):
    return "%s__T%s" % (attr, t.__name__)

def _type_attr_names(attr, cls):
    prefix = "%s__T" % attr
    for name in dir(cls):
        if name.startswith(prefix):
            yield name

def _idprop_names(attr, self):
    prefix = "%s__T" % attr
    for name in self.keys():
        if name.startswith(prefix):
            yield name

def bpy_register_dynpointer(cls, attr, dynptr_prop):
    name = dynptr_prop.name
    description = dynptr_prop.description

    def pointer_get(self, *args, **kw):
        ptr_type = dynptr_prop.refine(self, *args, **kw)
        if ptr_type is None:
            return None
        type_attr = _type_attr(attr, ptr_type)
        return getattr(self, type_attr)
    setattr(cls, attr, pointer_get)

    def clear(self, *args, **kw):
        ptr_type = dynptr_prop.refine(self, *args, **kw)
        type_attr = None if ptr_type is None else _type_attr(attr, ptr_type)
        for name in _idprop_names(attr, self):
            if name != type_attr:
                del self[name]
    setattr(cls, "%s__clear" % attr, clear)

    def clear_all(self):
        for name in _idprop_names(attr, self):
            del self[name]
    setattr(cls, "%s__clear_all" % attr, clear_all)

def bpy_unregister_dynpointer(cls, attr):
    for name in _type_attr_names(attr, cls):
        delattr(cls, name)
    delattr(cls, "%s__clear" % attr)
    delattr(cls, "%s__clear_all" % attr)
    delattr(cls, attr)

def bpy_register_dynpointer_type(cls, attr, ptr_type):
    type_attr = _type_attr(attr, ptr_type)
    prop = PointerProperty(type=ptr_type)
    setattr(cls, type_attr, prop)

def bpy_unregister_dynpointer_type(cls, attr, ptr_type):
    type_attr = _type_attr(attr, ptr_type)
    if hasattr(cls, type_attr):
        delattr(cls, type_attr)

def MetaDynPointerContainer(base=type):
    class MetaWrap(base):
        # setattr wrapper to register new DynPointerProperty
        def __setattr__(self, key, value):
            if isinstance(value, DynPointerProperty):
                bpy_register_dynpointer(self, key, value)
            else:
                super().__setattr__(key, value)

        def __new__(cls, name, bases, classdict):
            container_cls = base.__new__(cls, name, bases, classdict)

            dynptr_items = [(attr, item) for attr, item in container_cls.__dict__.items() if isinstance(item, DynPointerProperty)]
            for attr, item in dynptr_items:
                bpy_register_dynpointer(container_cls, attr, item)

            return container_cls
    return MetaWrap

class DynPointerProperty():
    def __init__(self, name="", description="", refine=lambda self: None, options={'ANIMATABLE'}):
        self.name = name
        self.description = description
        self.refine = refine
        self.options = options


"""
### Dynamic PropertyGroup ###

def dyn_property_group(types=[], type_get=lambda self: None):
    def wrap(cls):
        if not issubclass(cls, PropertyGroup):
            raise Exception("dyn_property_group decorator can only be used on PropertyGroup subtypes")
            return cls

        base_getattr = PropertyGroup.__getattribute__
        base_setattr = PropertyGroup.__setattr__

        def impl_prop(t):
            return "impl__%s" % t.__name__

        # property groups for dynamic attributes
        for t in types:
            setattr(cls, impl_prop(t), PointerProperty(type=t, options={'HIDDEN'}))

        def impl_get(self):
            impl_type = type_get(self)
            return base_getattr(self, impl_prop(impl_type))

        # get/set methods for automatic deferring to impl property groups
        def type_getattr(self, name):
            try:
                return base_getattr(self, name)
            except:
                impl = impl_get(self)
                return getattr(impl, name)
        def type_setattr(self, name, value):
            try:
                # XXX ugly: __getattribute__ raises exception if attribute is undefined
                # using this to switch to impl attribute
                base_getattr(self, name)
                base_setattr(self, name, value)
            except:
                print("setting %r = %r" % (name, value))
                impl = impl_get(self)
                setattr(impl, name, value)
        cls.__getattr__ = type_getattr
        cls.__setattr__ = type_setattr

        return cls

    return wrap
"""

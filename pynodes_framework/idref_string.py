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
from bpy.props import EnumProperty, IntProperty, StringProperty

from pynodes_framework.id_info import *
from pynodes_framework.id_info import _id_type_identifier_map


### String-based implementation of IDRefProperty ###

def ptr_id(ptr):
    return hash(ptr.as_pointer()) % 65536


def bpy_register_idref(cls, attr, idrefprop):
    idlist = get_idtype_list(idrefprop.idtype)
    name_attr = "%s__name__" % attr

    setattr(cls, "%s__idtype__" % attr, idrefprop.idtype)
    setattr(cls, "%s__icon__" % attr, id_type_icon(idrefprop.idtype))
    setattr(cls, "%s__options__" % attr, idrefprop.options)

    def name_get(self):
        return self.get(name_attr, "")

    def name_set(self, value):
        idvalue = idlist().get(value, None)
        if idvalue is not None:
            if idrefprop.poll and not idrefprop.poll(self, idvalue):
                return
        if idvalue is not None or (not value and 'NEVER_NULL' not in idrefprop.options):
            self[name_attr] = value
        if idvalue is not None and 'FAKE_USER' in idrefprop.options:
            idvalue.use_fake_user = True

    setattr(cls, name_attr, bpy.props.StringProperty(
        name="%s ID Name" % idrefprop.name,
        description="ID data block name for pseudo IDRef pointer",
        options={'HIDDEN'} | (idrefprop.options & {'ANIMATABLE', 'SKIP_SAVE', 'LIBRARY_EDITABLE'}),
        update=idrefprop.update,
        get=name_get,
        set=name_set,
        ))

    def pointer_get(self):
        name = self.get(name_attr, "")
        value = idlist().get(name, None)
        # Reset the name idproperty if invalid
        # XXX this is not 100% reliable, but better than keeping invalid names around
        # XXX does not work on read-only ID data
#        if value is None:
#            self[name_attr] = ""
        return value

    update_func = idrefprop.update
    def pointer_set(self, value):
        if value is None:
            if 'NEVER_NULL' in idrefprop.options:
                return
            del self[name_attr]

            if update_func:
                # use implicit bpy.context for update callback
                update_func(self, bpy.context)

        else:
            if idrefprop.poll and not idrefprop.poll(self, value):
                return
            if value.name not in idlist():
                return
            if 'FAKE_USER' in idrefprop.options:
                value.use_fake_user = True
            self[name_attr] = value.name

            if update_func:
                # use implicit bpy.context for update callback
                update_func(self, bpy.context)

    def pointer_del(self):
        delattr(self, name_attr)

    prop = property(pointer_get, pointer_set, pointer_del, idrefprop.description)
    # Note: replaces the temporary IDRefProperty item!            
    setattr(cls, attr, prop)

    # Enum property callbacks, wrapping the actual id property
    # This can be used for a ui button

    def enum_items(self, context):
        # NB: hack for avoiding volatile string variables from bpy,
        # use a global list for storing the enum items reliably
        global _enum_items
        #_enum_items = [("-1", "", "", 'NONE', -1)]
        _enum_items = []
        for ptr in idlist():
            if idrefprop.poll and not idrefprop.poll(self, ptr):
                continue
            _enum_items.append((str(ptr_id(ptr)), "".join(ptr.name), "", 'NONE', ptr_id(ptr)))
        return _enum_items

    def enum_get(self):
        ptr = pointer_get(self)
        return ptr_id(ptr) if ptr else -1
     
    def enum_set(self, value):
        if value == -1:
            pointer_set(self, None)
        else:
            for ptr in idlist():
                if ptr_id(ptr) == value:
                    pointer_set(self, ptr)
                    return

    enum_prop = EnumProperty(name=idrefprop.name, description=idrefprop.description, items=enum_items, get=enum_get, set=enum_set)
    setattr(cls, "%s__enum__" % attr, enum_prop)


def bpy_unregister_idref(cls, attr):
    delattr(cls, attr)


# XXX could be injected into UILayout as a template
def draw_idref(layout, data, prop, text=""):
    icon = getattr(data, "%s__icon__" % prop, 'NONE')
    options = getattr(data, "%s__options__" % prop, set())

    row = layout.row(align=True)
    row.context_pointer_set("idref_data", data)

    row.prop(data, "%s__enum__" % prop, text=text, icon=icon)

    ptr = getattr(data, prop)
    if ptr and 'NEVER_NULL' not in options:
        props = row.operator("UI_OT_idref_unlink", text="", icon="X")
        props.propname = prop

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
from bpy.props import EnumProperty, IntProperty

from pynodes_framework.id_info import *


### Driver-based implementation of IDRefProperty ###
# This is nice because it uses real pointers, so name changes won't affect them
# However, there are severe limitations for drivers on PropertyGroups, which make this difficult


def find_driver_target(self, prop):
    driver_prop = "%s__driver_storage__" % prop
    if self.id_data is None:
        return None
    if self.id_data.animation_data is None:
        return None

    data_path = self.path_from_id(driver_prop)
    for fcurve in self.id_data.animation_data.drivers:
        if fcurve.data_path == data_path:
            if fcurve.driver.variables:
                return fcurve.driver.variables[0].targets[0]
            return None

def verify_driver_target(self, prop, idtype):
    driver_prop = "%s__driver_storage__" % prop
    driver = self.driver_add(driver_prop).driver
    # we need exactly 1 variable
    if not driver.variables:
        var = driver.variables.new()
    else:
        var = driver.variables[0]
        # remove remaining variables
        unused_vars = driver.variables[1:]
        for v in unused_vars:
            driver.variables.remove(v)

    target = var.targets[0]
    target.id_type = idtype
    return target

def bpy_register_idref(cls, attr, idrefprop):
    driver_attr = "%s__driver_storage__" % attr
    driver_prop = IntProperty(name="IDRef Property", description="Dummy property to store IDRef pointers in drivers")
    setattr(cls, driver_attr, driver_prop)

    def pointer_get(self):
        target = find_driver_target(self, attr)
        return target.id if target else None

    def pointer_set(self, value):
        if value is None:
            if 'NEVER_NULL' in idrefprop.options:
                return
            target = find_driver_target(self, attr)
            if target:
                target.id = None
        else:
            if idrefprop.poll and not idrefprop.poll(self, value):
                return
            target = verify_driver_target(self, attr, idrefprop.idtype)
            target.id = value
            if 'FAKE_USER' in idrefprop.options:
                value.use_fake_user = True

    def pointer_del(self):
        self.driver_remove(driver_attr)

    # Note: replaces the temporary IDRefProperty item!            
    prop = property(pointer_get, pointer_set, pointer_del, idrefprop.description)
    setattr(cls, attr, prop)

    # Enum property callbacks, wrapping the actual id property
    # These are for an additional pseudo-id property, so we can intercept pointer updates
    # from the UI button and set the driver id pointer. This is not possible
    # with the id property, because we cannot catch updates.

    idlist = get_idtype_list(idrefprop.idtype)

    def enum_items(self, context):
        # NB: hack for avoiding volatile string variables from bpy,
        # use a global list for storing the enum items reliably
        global _enum_items
        #_enum_items = [("-1", "", "", 'NONE', -1)]
        _enum_items = []
        for ptr in idlist():
            if idrefprop.poll and not idrefprop.poll(self, ptr):
                continue
            _enum_items.append((str(ptr.as_pointer()), "".join(ptr.name), "", 'NONE', ptr.as_pointer()))
        return _enum_items

    def enum_get(self):
        ptr = pointer_get(self)
        return ptr.as_pointer() if ptr else -1
     
    def enum_set(self, value):
        if value == -1:
            pointer_set(self, None)
        else:
            for ptr in idlist():
                if ptr.as_pointer() == value:
                    pointer_set(self, ptr)
                    return

    enum_attr = "%s__enum__" % attr
    enum_prop = EnumProperty(name=idrefprop.name, description=idrefprop.description, items=enum_items, get=enum_get, set=enum_set, update=idrefprop.update)
    setattr(cls, enum_attr, enum_prop)

    setattr(cls, "%s__icon__" % attr, id_type_icon(idrefprop.idtype))
    setattr(cls, "%s__options__" % attr, idrefprop.options)

def bpy_unregister_idref(cls, attr):
    driver_attr = "%s__driver_storage__" % attr
    delattr(cls, driver_attr)
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

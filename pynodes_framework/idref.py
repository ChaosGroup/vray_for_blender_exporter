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
from bpy_types import RNAMetaPropGroup
from bpy.types import Operator
from bpy.props import StringProperty

from pynodes_framework.id_info import *


#__idref_impl__ = 'STRING'
__idref_impl__ = 'DRIVER'

if __idref_impl__ == 'STRING':
    from pynodes_framework import idref_string
    draw_idref = idref_string.draw_idref
    bpy_register_idref = idref_string.bpy_register_idref
    bpy_unregister_idref = idref_string.bpy_unregister_idref
elif __idref_impl__ == 'DRIVER':
    from pynodes_framework import idref_driver
    draw_idref = idref_driver.draw_idref
    bpy_register_idref = idref_driver.bpy_register_idref
    bpy_unregister_idref = idref_driver.bpy_unregister_idref


def MetaIDRefContainer(base=RNAMetaPropGroup):
    class MetaWrap(base):
        # setattr wrapper to register new IDRefProperty
        def __setattr__(self, key, value):
            if isinstance(value, IDRefProperty):
                bpy_register_idref(self, key, value)
            else:
                super().__setattr__(key, value)

        def __new__(cls, name, bases, classdict):
            container_cls = base.__new__(cls, name, bases, classdict)

            idref_items = [(attr, item) for attr, item in container_cls.__dict__.items() if isinstance(item, IDRefProperty)]
            for attr, item in idref_items:
                bpy_register_idref(container_cls, attr, item)

            return container_cls
    return MetaWrap


class IDRefProperty():
    def __init__(self, name="", description="", idtype='OBJECT', options={'ANIMATABLE'}, update=None, poll=None):
        self.name = name
        self.description = description
        self.idtype = idtype
        self.options = options
        self.update = update
        self.poll = poll


class IDRefUnlinkOperator(Operator):
    """Default operator for setting IDRefProperty to None"""
    bl_idname = "ui.idref_unlink"
    bl_label = "Unlink"

    propname = StringProperty(name="Property", description="Name of the IDRef property to unlink")

    def execute(self, context):
        data = getattr(context, "idref_data", None)
        if data is None:
            self.report({'ERROR_INVALID_CONTEXT'}, "IDRef data context undefined")
            return {'CANCELLED'}

        prop = self.propname
        if not prop:
            self.report({'ERROR'}, "IDRef property name undefined")
            return {'CANCELLED'}

        setattr(data, prop, None)
        return {'FINISHED'}

bpy.utils.register_class(IDRefUnlinkOperator)

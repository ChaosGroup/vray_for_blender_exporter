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
from bpy.types import PropertyGroup, Operator, Panel

from bpy.props import PointerProperty
from pynodes_framework.idref import *


# ID property for an Object
propdef_a = IDRefProperty(name="Object", description="Custom object reference", idtype='OBJECT')


# ID property for an Image, using only PNG
def _prop_b_poll(self, img):
    return img.file_format == 'PNG'
propdef_b = IDRefProperty(name="PNG Image", description="A PNG image", idtype='IMAGE',
                          poll=_prop_b_poll)


# ID property for a Scene, not using Cycles and printing a message on update
def _prop_c_poll(self, scene):
    return scene.render.engine != 'CYCLES'
def _prop_c_update(self, context):
    print("Scene %r was selected" % self.custom_scene.name)
propdef_c = IDRefProperty(name="Scene", description="Scene that doesn't use Cycles renderer", idtype='SCENE',
                          poll=_prop_c_poll, update=_prop_c_update)


# Create a custom ID property in World
# IDRefProperty in existing types must be registered manually
bpy_register_idref(bpy.types.World, "custom_object", propdef_a)

# Simple PropertyGroup containing an IDRefProperty
# Uses a MetaIDRefContainer metaclass for automatically registering IDRefProperty attributes
class MyPropGroup(bpy.types.PropertyGroup, metaclass=MetaIDRefContainer()):
    custom_image = propdef_b
    custom_scene = propdef_c

bpy.utils.register_class(MyPropGroup)
# Create a group property in World
bpy.types.World.custom_group = PointerProperty(type=MyPropGroup)


# Simple panel for showing ID property buttons
class MyIDRefPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "IDRefProperty Tests"

    def draw(self, context):
        layout = self.layout
        world = context.scene.world
        if world is None:
            return

        draw_idref(layout, world, "custom_object")

        col = layout.column(align=True)
        draw_idref(col, world.custom_group, "custom_image")
        draw_idref(col, world.custom_group, "custom_scene")

bpy.utils.register_class(MyIDRefPanel)



bpy.context.scene.world.custom_object = bpy.data.objects[0]
print("World %r custom_object 1: %r" % (bpy.context.scene.world.name, bpy.context.scene.world.custom_object))
bpy.context.scene.world.custom_object = bpy.data.objects[1]
print("World %r custom_object 2: %r" % (bpy.context.scene.world.name, bpy.context.scene.world.custom_object))
bpy.context.scene.world.custom_object = None
print("World %r custom_object 3: %r" % (bpy.context.scene.world.name, bpy.context.scene.world.custom_object))


bpy.context.scene.world.custom_group.custom_image = bpy.data.images[0]
bpy.context.scene.world.custom_group.custom_scene = bpy.data.scenes[0]
print("MyPropGroup custom_image 1: %r" % bpy.context.scene.world.custom_group.custom_image)
print("MyPropGroup custom_scene 1: %r" % bpy.context.scene.world.custom_group.custom_scene)


# clean up
#bpy_unregister_idref(bpy.types.World, "custom_object")

#bpy.utils.unregister_class(MyPropGroup)
#del bpy.types.World.custom_group

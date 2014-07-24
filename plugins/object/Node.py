#
# V-Ray/Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import random

import bpy
import mathutils


TYPE = 'OBJECT'
ID   = 'Node'
NAME = 'Node'
DESC = "Node settings"


gUserAttributeTypeToValue = {
    '0' : "value_int",
    '1' : "value_float",
    '2' : "value_color",
    '3' : "value_string"
}


class VRayUserAttributeOpPromote(bpy.types.Operator):
    bl_idname      = 'vray.user_attribute_promote'
    bl_label       = "Promote"
    bl_description = "Promote user attribute to selected objects"

    def execute(self, context):
        activeObject    = context.active_object
        selectedObjects = context.selected_objects

        activeNode = activeObject.vray.Node
        activeAttrIndex = activeNode.user_attributes_selected

        activeAttrCount = len(activeNode.user_attributes)
        if not activeAttrIndex >= 0 or not activeAttrCount:
            return {'CANCELLED'}

        activeAttribute = activeNode.user_attributes[activeAttrIndex]

        attrName = activeAttribute.name
        attrType = activeAttribute.value_type
        attrValueName = gUserAttributeTypeToValue[attrType]

        activeAttrValue = getattr(activeAttribute, attrValueName)

        for ob in filter(lambda x: x != activeObject, selectedObjects):
            Node = ob.vray.Node

            attr = None
            if attrName in Node.user_attributes:
                attr = Node.user_attributes[attrName]
                # NOTE: Type could be changed
                attr.value_type = attrType
            else:
                attr = Node.user_attributes.add()
                attr.name       = attrName
                attr.value_type = attrType

            if not activeNode.user_attributes_rnd_use:
                setattr(attr, attrValueName, activeAttrValue)

            else:
                if activeAttribute.value_type == '3':
                    attr.value_string = activeAttribute.value_string
                else:
                    newValue = None
                    if activeAttribute.value_type == '0':
                        newValue = random.randrange(activeNode.user_attributes_int_rnd_min,
                            activeNode.user_attributes_int_rnd_max)
                    elif activeAttribute.value_type == '1':
                        random.random()
                        randFloat = random.random()
                        randRange = activeNode.user_attributes_float_rnd_max - activeNode.user_attributes_float_rnd_min
                        newValue = activeNode.user_attributes_float_rnd_min + randFloat * randRange
                    elif activeAttribute.value_type == '2':
                        random.random()
                        randR = random.random()
                        random.random()
                        randG = random.random()
                        random.random()
                        randB = random.random()
                        newValue = mathutils.Color((randR, randG, randB))
                    setattr(attr, attrValueName, newValue)

        return {'FINISHED'}


class VRayUserAttributeItem(bpy.types.PropertyGroup):
    value_type = bpy.props.EnumProperty(
        name = "Type",
        items = (
            ('0', "Int",    ""),
            ('1', "Float",  ""),
            ('2', "Color",  ""),
            ('3', "String", ""),
        ),
        default = '1'
    )

    value_int    = bpy.props.IntProperty(default=0)
    value_float  = bpy.props.FloatProperty(default=0.0)
    value_string = bpy.props.StringProperty(default="")

    value_color = bpy.props.FloatVectorProperty(
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    use = bpy.props.BoolProperty(
        name = "",
        description = "Use Attribute",
        default = True
    )


class VRayListUserAttributes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(item.name)
        row.prop(item, 'value_type', text="")
        row.prop(item, gUserAttributeTypeToValue[item.value_type], text="")
        row.prop(item, 'use', text="")


class VRayNode(bpy.types.PropertyGroup):
    user_attributes = bpy.props.CollectionProperty(
        name = "User Attributes",
        type =  VRayUserAttributeItem,
        description = "User attributes"
    )

    user_attributes_selected = bpy.props.IntProperty(
        default = -1,
        options = {'HIDDEN', 'SKIP_SAVE'},
        min = -1,
        max = 100
    )

    user_attributes_rnd_use = bpy.props.BoolProperty(name="Randomize", default=False)
    user_attributes_float_rnd_min = bpy.props.FloatProperty(name="Min", default=0.0)
    user_attributes_float_rnd_max = bpy.props.FloatProperty(name="Max", default=1.0)
    user_attributes_int_rnd_min = bpy.props.IntProperty(name="Min", default=0)
    user_attributes_int_rnd_max = bpy.props.IntProperty(name="Max", default=100)


class VRayUserAttributeAdd(bpy.types.Operator):
    bl_idname      = 'vray.user_attribute_add'
    bl_label       = "Add User Attribute"
    bl_description = "Add user attribute"

    def execute(self, context):
        Node = context.object.vray.Node

        Node.user_attributes.add()
        Node.user_attributes[-1].name = "MyAttr"

        return {'FINISHED'}


class VRayUserAttributeDel(bpy.types.Operator):
    bl_idname      = 'vray.user_attribute_del'
    bl_label       = "Delete User Attribute"
    bl_description = "Delete user attribute"

    def execute(self, context):
        Node = context.object.vray.Node

        if Node.user_attributes_selected >= 0:
           Node.user_attributes.remove(Node.user_attributes_selected)
           Node.user_attributes_selected -= 1

        if len(Node.user_attributes) == 0:
           Node.user_attributes_selected = -1

        if len(Node.user_attributes) == 1:
           Node.user_attributes_selected = 0

        return {'FINISHED'}


def GetRegClasses():
    return (
        VRayUserAttributeItem,
        VRayUserAttributeAdd,
        VRayUserAttributeDel,
        VRayListUserAttributes,
        VRayNode,
        VRayUserAttributeOpPromote,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    setattr(bpy.types.VRayObject, 'Node', bpy.props.PointerProperty(
        name = "Node",
        type =  VRayNode,
        description = "Node settings"
    ))


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

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

import bpy

from vb30.debug import Debug, PrintDict

from . import AttributeUtils


def RegisterPluginPropertyGroup(dataPointer, pluginModule):
    propGroupName = pluginModule.ID
    typeName      = "VRay%s" % propGroupName

    DynPropGroup = None

    if hasattr(bpy.types, typeName):
        DynPropGroup = getattr(bpy.types, typeName)

    else:
        classMembers = dict()

        for param in pluginModule.PluginParams:
            AttributeUtils.GenerateAttribute(classMembers, param)

        if hasattr(pluginModule, 'PluginRefParams'):
            for param in pluginModule.PluginRefParams:
                AttributeUtils.GenerateAttribute(classMembers, param)

        DynPropGroup = type(
            typeName,
            (bpy.types.PropertyGroup,),
            classMembers
        )

        bpy.utils.register_class(DynPropGroup)

    setattr(dataPointer, propGroupName, bpy.props.PointerProperty(
        attr        = propGroupName,
        name        = propGroupName,
        type        = DynPropGroup,
        description = pluginModule.DESC
    ))

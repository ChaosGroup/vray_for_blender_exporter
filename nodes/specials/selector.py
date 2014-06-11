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

from ..        import tree
from ..sockets import AddInput, AddOutput


class VRayNodeSelectNodeTree(bpy.types.Node):
    bl_idname = 'VRayNodeSelectNodeTree'
    bl_label  = 'Node Tree Select'
    bl_icon   = 'NODETREE'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    treeName = bpy.props.StringProperty(
        name        = "Tree",
        description = "Tree name",
        default     = ""
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketObject', "Tree")

    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'treeName',
                           bpy.data, 'node_groups',
                           text="")


class VRayNodeSelectObject(bpy.types.Node):
    bl_idname = 'VRayNodeSelectObject'
    bl_label  = 'Object Select'
    bl_icon   = 'OBJECT_DATA'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    objectName = bpy.props.StringProperty(
        name        = "Object",
        description = "Object name",
        default     = ""
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketObject', "Object")


    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'objectName',
                           context.scene, 'objects',
                           text="")


class VRayNodeSelectGroup(bpy.types.Node):
    bl_idname = 'VRayNodeSelectGroup'
    bl_label  = 'Group Select'
    bl_icon   = 'GROUP'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    groupName = bpy.props.StringProperty(
        name        = "Group",
        description = "Group name",
        default     = ""
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketObject', "Group")


    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'groupName',
                           bpy.data, 'groups',
                           text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayNodeSelectNodeTree,
        VRayNodeSelectObject,
        VRayNodeSelectGroup,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

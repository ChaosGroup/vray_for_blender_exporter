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



 #######  ########  ######## ########     ###    ########  #######  ########   ######
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ##
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ##
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ##
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ######

# This opeator will create a socket with the vray_attrNumber
# This will allow as to collect attrubutes after matching the name
#
class VRayListHolderAddSockets(bpy.types.Operator):
    bl_idname      = 'vray.node_list_socket_add'
    bl_label       = "Add Socket"
    bl_description = "Adds socket"

    socketType = bpy.props.StringProperty()
    socketName = bpy.props.StringProperty()
    vray_attr  = bpy.props.StringProperty()

    def execute(self, context):
        if not self.socketType or not self.socketName:
            return {'CANCELLED'}

        node     = context.node
        newIndex = len(node.inputs) + 1

        socketName = "%s %i" % (self.socketName, newIndex)
        attrName   = "%s%i" % (self.vray_attr, newIndex)

        AddInput(node, self.socketType, socketName, attrName=attrName)

        return {'FINISHED'}


class VRayListHolderDelSockets(bpy.types.Operator):
    bl_idname      = 'vray.node_list_socket_del'
    bl_label       = "Remove Socket"
    bl_description = "Removes empty socket"

    def execute(self, context):
        node = context.node

        nSockets = len(node.inputs)

        if not nSockets:
            return {'FINISHED'}

        for i in range(nSockets-1, -1, -1):
            s = node.inputs[i]
            if not s.is_linked:
                node.inputs.remove(s)
                break

        return {'FINISHED'}


##    ##  #######  ########  ########
###   ## ##     ## ##     ## ##
####  ## ##     ## ##     ## ##
## ## ## ##     ## ##     ## ######
##  #### ##     ## ##     ## ##
##   ### ##     ## ##     ## ##
##    ##  #######  ########  ########

class VRayListHolder(bpy.types.Node):
    bl_idname = 'VRayListHolder'
    bl_label  = 'Effects Container'
    bl_icon   = 'GHOST_ENABLED'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    socketType = None
    socketName = None

    def init(self, context):
        AddInput(self, 'VRaySocketEffect', GetSocketName(1))
        AddOutput(self, 'VRaySocketObject', "Sphere Fade")

    def draw_buttons(self, context, layout):
        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_list_socket_add', icon="ZOOMIN", text="Add")
        row.operator('vray.node_list_socket_del', icon="ZOOMOUT", text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayListHolderAddSockets,
        VRayListHolderDelSockets,
        VRayListHolder,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

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
from ..operators import sockets as SocketOperators


 #######  ########  ######## ########     ###    ########  #######  ########   ######
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ##
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ##
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ##
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ######

class VRayNodeEffectsHolderAddSocket(SocketOperators.VRayNodeAddCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_effects_add'
    bl_label       = "Add Effect Socket"
    bl_description = "Adds Effect sockets"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketEffect'
        self.vray_socket_name = "Effect"


class VRayNodeEffectsHolderDelSocket(SocketOperators.VRayNodeDelCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_effects_del'
    bl_label       = "Remove Effect Socket"
    bl_description = "Removes Effect socket (only not linked sockets will be removed)"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketEffect'
        self.vray_socket_name = "Effect"


##    ##  #######  ########  ########  ######
###   ## ##     ## ##     ## ##       ##    ##
####  ## ##     ## ##     ## ##       ##
## ## ## ##     ## ##     ## ######    ######
##  #### ##     ## ##     ## ##             ##
##   ### ##     ## ##     ## ##       ##    ##
##    ##  #######  ########  ########  ######

class VRayNodeEffectsHolder(bpy.types.Node):
    bl_idname = 'VRayNodeEffectsHolder'
    bl_label  = 'Effects Container'
    bl_icon   = 'GHOST_ENABLED'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    def init(self, context):
        AddInput(self, 'VRaySocketEffect', "Effect 1")
        AddOutput(self, 'VRaySocketObject', "Effects")

    def draw_buttons(self, context, layout):
        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_effects_add', icon="ZOOMIN", text="Add")
        row.operator('vray.node_effects_del', icon="ZOOMOUT", text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayNodeEffectsHolderAddSocket,
        VRayNodeEffectsHolderDelSocket,
        VRayNodeEffectsHolder,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

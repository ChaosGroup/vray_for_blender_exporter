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


def GetSocketName(index):
    return "Effect %i" % index


 #######  ########  ######## ########     ###    ########  #######  ########   ######
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ##
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ##
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ##
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ######

class VRayEffectsHolderAddSockets(bpy.types.Operator):
    bl_idname      = 'vray.node_effects_add'
    bl_label       = "Add Effect Socket"
    bl_description = "Adds effect sockets"

    def execute(self, context):
        node = context.node

        newIndex = len(node.inputs) + 1

        AddInput(node, 'VRaySocketEffect', GetSocketName(newIndex))

        return {'FINISHED'}


class VRayEffectsHolderDelSockets(bpy.types.Operator):
    bl_idname      = 'vray.node_effects_del'
    bl_label       = "Remove Effect Socket"
    bl_description = "Removes empty effect socket"

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
        AddInput(self, 'VRaySocketEffect', GetSocketName(1))
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
        VRayEffectsHolderAddSockets,
        VRayEffectsHolderDelSockets,

        VRayNodeEffectsHolder,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

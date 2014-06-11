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

class VRAY_OT_node_add_render_channel_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_add_render_channel_sockets'
    bl_label       = "Add Render Channel Socket"
    bl_description = "Adds Render Channel sockets"

    def execute(self, context):
        node = context.node

        newIndex = len(node.inputs)+ 1
        sockName = "Channel %i" % newIndex

        AddInput(node, 'VRaySocketRenderChannel', sockName)

        return {'FINISHED'}


class VRAY_OT_node_del_render_channel_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_del_render_channel_sockets'
    bl_label       = "Remove Render Channel Socket"
    bl_description = "Removes Render Channel socket (only not linked sockets will be removed)"

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

class VRayNodeRenderChannels(bpy.types.Node):
    bl_idname = 'VRayNodeRenderChannels'
    bl_label  = 'Render Channles Container'
    bl_icon   = 'SCENE_DATA'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    unfiltered_fragment_method = bpy.props.EnumProperty(
        name = "Fragment Method",
        description = "Determines which fragment to use for unfiltered render elements",
        items = (
            ('0', "Best Coverage", ""),
            ('1', "Closest To Camera", ""),
        ),
        default = '0'
    )

    deep_merge_mode = bpy.props.EnumProperty(
        name = "Deep Merge Mode",
        description = "Determines how to blend fragments within a pixel",
        items = (
            ('0', "By Render ID", ""),
            ('1', "By Z-Depth", ""),
        ),
        default = '0'
    )

    deep_merge_coeff = bpy.props.FloatProperty(
        name = "Deep Merge Coeff",
        description = "Determines the z-depth blending sensitivity",
        min = 0.0,
        default = 1.0,
    )

    def init(self, context):
        AddInput(self, 'VRaySocketRenderChannel', "Channel 1")

    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        col.prop(self, 'unfiltered_fragment_method')
        col.prop(self, 'deep_merge_mode')
        sub = col.column()
        sub.active = self.deep_merge_mode == '1'
        sub.prop(self, 'deep_merge_coeff')

        layout.separator()

        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_add_render_channel_sockets', icon="ZOOMIN", text="Add")
        row.operator('vray.node_del_render_channel_sockets', icon="ZOOMOUT", text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_OT_node_add_render_channel_sockets,
        VRAY_OT_node_del_render_channel_sockets,
        VRayNodeRenderChannels,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

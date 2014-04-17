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

from pynodes_framework import base

from ..        import tree
from ..sockets import AddInput, AddOutput


 ######   #######   ######  ##    ## ######## ########  ######  
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
##       ##     ## ##       ##  ##   ##          ##    ##       
 ######  ##     ## ##       #####    ######      ##     ######  
      ## ##     ## ##       ##  ##   ##          ##          ## 
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ## 
 ######   #######   ######  ##    ## ########    ##     ######  

class VRaySocketTexLayered(bpy.types.NodeSocket, base.NodeSocket):
    bl_idname = 'VRaySocketTexLayered'
    bl_label  = 'TexLayered Socket'

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    value = bpy.props.EnumProperty(
        name = "Blend Mode",
        description = "Blend mode",
        items = (
            ('0',  "None", ""),
            ('1',  "Over", ""),
            ('2',  "In", ""),
            ('3',  "Out", ""),
            ('4',  "Add", ""),
            ('5',  "Subtract", ""),
            ('6',  "Multiply", ""),
            ('7',  "Difference", ""),
            ('8',  "Lighten", ""),
            ('9',  "Darken", ""),
            ('10', "Saturate", ""),
            ('11', "Desaturate", ""),
            ('12', "Illuminate", "")
        ),
        default = '1'
    )

    def draw(self, context, layout, node, text):
        layout.prop(self, 'value', text="")

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


 #######  ########  ######## ########     ###    ########  #######  ########   ######  
##     ## ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ## ##    ## 
##     ## ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ## ##       
##     ## ########  ######   ########  ##     ##    ##    ##     ## ########   ######  
##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##         ## 
##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##    ## 
 #######  ##        ######## ##     ## ##     ##    ##     #######  ##     ##  ######  

class VRAY_OT_node_add_texlayered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_add_texlayered_sockets'
    bl_label       = "Add TexLayered Socket"
    bl_description = "Adds TexLayered sockets"

    def execute(self, context):
        node = context.node

        newIndex = len(node.inputs) + 1
        sockName = "Texture %i" % newIndex

        AddInput(node, 'VRaySocketTexLayered', sockName)

        return {'FINISHED'}


class VRAY_OT_node_del_texlayered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_del_texlayered_sockets'
    bl_label       = "Remove TexLayered Socket"
    bl_description = "Removes TexLayered socket (only not linked sockets will be removed)"

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

class VRayNodeTexLayered(bpy.types.Node, tree.VRayTreeNode):
    bl_idname = 'VRayNodeTexLayered'
    bl_label  = 'Layered'
    bl_icon   = 'TEXTURE'

    vray_type   = 'TEXTURE'
    vray_plugin = 'TexLayered'

    def init(self, context):
        for i in range(2):
            humanIndex = i + 1

            texSockName = "Texture %i" % humanIndex

            AddInput(self, 'VRaySocketTexLayered', texSockName)

        AddOutput(self, 'VRaySocketColor',      "Output")
        AddOutput(self, 'VRaySocketFloatColor', "Out Transparency", 'out_transparency')
        AddOutput(self, 'VRaySocketFloatColor', "Out Alpha",        'out_alpha')
        AddOutput(self, 'VRaySocketFloatColor', "Out Intensity",    'out_intensity')

    def draw_buttons(self, context, layout):
        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_add_texlayered_sockets', icon="ZOOMIN", text="Add")
        row.operator('vray.node_del_texlayered_sockets', icon="ZOOMOUT", text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_OT_node_add_texlayered_sockets,
        VRAY_OT_node_del_texlayered_sockets,

        VRaySocketTexLayered,
        VRayNodeTexLayered,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

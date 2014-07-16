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


 ######   #######   ######  ##    ## ######## ########  ######
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ##
##       ##     ## ##       ##  ##   ##          ##    ##
 ######  ##     ## ##       #####    ######      ##     ######
      ## ##     ## ##       ##  ##   ##          ##          ##
##    ## ##     ## ##    ## ##   ##  ##          ##    ##    ##
 ######   #######   ######  ##    ## ########    ##     ######

class VRaySocketTexLayered(bpy.types.NodeSocket):
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

class VRayNodeTexLayeredAddSocket(SocketOperators.VRayNodeAddCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_add_texlayered_sockets'
    bl_label       = "Add TexLayered Socket"
    bl_description = "Adds TexLayered sockets"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketTexLayered'
        self.vray_socket_name = "Texture"


class VRayNodeTexLayeredDelSocket(SocketOperators.VRayNodeDelCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_del_texlayered_sockets'
    bl_label       = "Remove TexLayered Socket"
    bl_description = "Removes TexLayered socket (only not linked sockets will be removed)"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketTexLayered'
        self.vray_socket_name = "Texture"


##    ##  #######  ########  ########  ######
###   ## ##     ## ##     ## ##       ##    ##
####  ## ##     ## ##     ## ##       ##
## ## ## ##     ## ##     ## ######    ######
##  #### ##     ## ##     ## ##             ##
##   ### ##     ## ##     ## ##       ##    ##
##    ##  #######  ########  ########  ######


######## ######## ##     ##    ##          ###    ##    ## ######## ########  ######## ########  
   ##    ##        ##   ##     ##         ## ##    ##  ##  ##       ##     ## ##       ##     ## 
   ##    ##         ## ##      ##        ##   ##    ####   ##       ##     ## ##       ##     ## 
   ##    ######      ###       ##       ##     ##    ##    ######   ########  ######   ##     ## 
   ##    ##         ## ##      ##       #########    ##    ##       ##   ##   ##       ##     ## 
   ##    ##        ##   ##     ##       ##     ##    ##    ##       ##    ##  ##       ##     ## 
   ##    ######## ##     ##    ######## ##     ##    ##    ######## ##     ## ######## ########  

class VRayNodeTexLayered(bpy.types.Node):
    bl_idname = 'VRayNodeTexLayered'
    bl_label  = 'Layered'
    bl_icon   = 'TEXTURE'

    vray_type   = 'TEXTURE'
    vray_plugin = 'TexLayered'

    alpha_from_intensity = bpy.props.BoolProperty(
        name        = "Alpha From Intersity",
        description = "Object",
        default     =  False
    )

    invert = bpy.props.BoolProperty(
        name        = "Invert",
        description = "Invert",
        default     =  False
    )

    invert_alpha = bpy.props.BoolProperty(
        name        = "Invert Alpha",
        description = "Invert Alpha",
        default     =  False
    )

    def init(self, context):
        AddInput(self, 'VRaySocketFloatColor', "Alpha",        'alpha',        1.0)
        AddInput(self, 'VRaySocketFloatColor', "Alpha Mult",   'alpha_mult',   1.0)
        AddInput(self, 'VRaySocketFloatColor', "Alpha Offset", 'alpha_offset', 0.0)

        AddInput(self, 'VRaySocketColor', "No UV Color", 'nouvw_color', (0.5,0.5,0.5))

        AddInput(self, 'VRaySocketColor', "Color Mult",   'color_mult',   (1.0,1.0,1.0))
        AddInput(self, 'VRaySocketColor', "Color Offset", 'color_offset', (0.0,0.0,0.0))

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
        col = split.column()
        col.prop(self, 'invert')
        col.prop(self, 'invert_alpha')
        col.prop(self, 'alpha_from_intensity')

        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_add_texlayered_sockets', icon="ZOOMIN", text="Add")
        row.operator('vray.node_del_texlayered_sockets', icon="ZOOMOUT", text="")


######## ######## ##     ##    ##     ## ##     ## ##       ######## #### 
   ##    ##        ##   ##     ###   ### ##     ## ##          ##     ##  
   ##    ##         ## ##      #### #### ##     ## ##          ##     ##  
   ##    ######      ###       ## ### ## ##     ## ##          ##     ##  
   ##    ##         ## ##      ##     ## ##     ## ##          ##     ##  
   ##    ##        ##   ##     ##     ## ##     ## ##          ##     ##  
   ##    ######## ##     ##    ##     ##  #######  ########    ##    #### 

class VRaySocketTexMulti(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketTexMulti'
    bl_label  = 'TexMulti Socket'

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    value = bpy.props.IntProperty(
        name = "ID",
        description = "ID",
    )

    def draw(self, context, layout, node, text):
        layout.prop(self, 'value', text="")

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRayNodeTexMultiAddSocket(SocketOperators.VRayNodeAddCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_add_texmulti_socket'
    bl_label       = "Add TexMulti Socket"
    bl_description = "Adds TexMulti sockets"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketTexMulti'
        self.vray_socket_name = "Texture"

    def set_value(self, nodeSock, value):
        nodeSock.value = value


class VRayNodeTexMultiDelSocket(SocketOperators.VRayNodeDelCustomSocket, bpy.types.Operator):
    bl_idname      = 'vray.node_del_texmulti_socket'
    bl_label       = "Remove TexMulti Socket"
    bl_description = "Removes TexMulti socket (only not linked sockets will be removed)"

    def __init__(self):
        self.vray_socket_type = 'VRaySocketTexMulti'
        self.vray_socket_name = "Texture"


class VRayNodeTexMulti(bpy.types.Node):
    bl_idname = 'VRayNodeTexMulti'
    bl_label  = 'Multi ID'
    bl_icon   = 'TEXTURE'

    vray_type   = 'TEXTURE'
    vray_plugin = 'TexMulti'

    mode = bpy.props.EnumProperty(
        name = "Mode",
        description = "The mode for the texture",
        items = (
            ('0', "Face Material ID", ""),
            ('1', "Object ID",        ""),
        ),
        default = '0'
    )

    def init(self, context):
        AddOutput(self, 'VRaySocketColor', "Output")

        AddInput(self, 'VRaySocketColor', "Default")

        for i in range(3):
            humanIndex = i + 1
            texSockName = "Texture %i" % humanIndex
            AddInput(self, 'VRaySocketTexMulti', texSockName, default=humanIndex)

    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        col.prop(self, 'mode')

        split = layout.split()
        row = split.row(align=True)
        row.operator('vray.node_add_texmulti_socket', icon="ZOOMIN", text="Add")
        row.operator('vray.node_del_texmulti_socket', icon="ZOOMOUT", text="")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRaySocketTexLayered,
        VRayNodeTexLayeredAddSocket,
        VRayNodeTexLayeredDelSocket,
        VRayNodeTexLayered,

        VRaySocketTexMulti,
        VRayNodeTexMultiAddSocket,
        VRayNodeTexMultiDelSocket,
        VRayNodeTexMulti,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

#
# V-Ray For Blender
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

from vb30.debug import Debug


def CheckLinkedSockets(node_sockets):
    for sock in node_sockets:
        if sock.is_linked:
            return True
    return False


def AddInput(node, socketType, socketName, attrName=None, default=None):
    if socketName in node.inputs:
        return

    Debug("Adding input socket: '%s' <= '%s'" % (socketName, attrName), msgType='INFO')

    node.inputs.new(socketType, socketName)

    createdSocket = node.inputs[socketName]

    if attrName is not None:
        createdSocket.vray_attr = attrName

    if default is not None:
        # Some socket intensionally have no 'value'
        if hasattr(createdSocket, 'value'):
            if socketType in {'VRaySocketColor', 'VRaySocketVector'}:
                createdSocket.value = (default[0], default[1], default[2])
            else:
                createdSocket.value = default


def AddOutput(node, socketType, socketName, attrName=None):
    if socketName in node.outputs:
        return

    Debug("Adding output socket: '%s' <= '%s'" % (socketName, attrName), msgType='INFO')

    node.outputs.new(socketType, socketName)

    createdSocket = node.outputs[socketName]

    if attrName is not None:
        createdSocket.vray_attr = attrName


def _is_connected_muted(socket):
    def _get_connected_node(nodeSocket):
        for l in nodeSocket.links:
            if l.from_node:
                return l.from_node
        return None

    muted = False
    conNode = _get_connected_node(socket)
    if conNode:
        muted = conNode.mute
    return muted


class VRaySocketMult:
    multiplier = bpy.props.FloatProperty(
        name        = "Multiplier",
        description = "Multiplier",
        subtype     = 'PERCENTAGE',
        precision   = 0,
        min         = 0.0,
        soft_max    = 100.0,
        default     = 100.0
    )

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text)
        else:
            showValue = _is_connected_muted(self) if self.is_linked else True
            if showValue:
                layout.prop(self, 'value', text=text)
            else:
                layout.prop(self, 'multiplier', text="%s Mult." % text)


class VRaySocketColorMult(VRaySocketMult):
    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text)
        else:
            showValue = _is_connected_muted(self) if self.is_linked else True
            if showValue:
                split = layout.split(percentage=0.4)
                split.prop(self, 'value', text="")
                split.label(text=text)
            else:
               layout.prop(self, 'multiplier', text="%s Mult." % text)


class VRaySocketUse:
    use = bpy.props.BoolProperty(
        name        = "Use",
        description = "Use socket",
        default     = True
    )


 ######   ########  #######  ##     ## ######## ######## ########  ##    ##
##    ##  ##       ##     ## ###   ### ##          ##    ##     ##  ##  ##
##        ##       ##     ## #### #### ##          ##    ##     ##   ####
##   #### ######   ##     ## ## ### ## ######      ##    ########     ##
##    ##  ##       ##     ## ##     ## ##          ##    ##   ##      ##
##    ##  ##       ##     ## ##     ## ##          ##    ##    ##     ##
 ######   ########  #######  ##     ## ########    ##    ##     ##    ##

class VRaySocketGeom(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketGeom'
    bl_label  = 'Geomtery socket'

    value = bpy.props.StringProperty(
        name = "Geometry",
        description = "Geometry",
        default = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.15, 0.15, 0.15, 1.0)


 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##

class VRaySocketObject(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketObject'
    bl_label  = 'Object socket'

    value = bpy.props.StringProperty(
        name = "Object",
        description = "Object",
        default = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.0, 1.0, 1.0, 1.0)


#### ##    ## ########
 ##  ###   ##    ##
 ##  ####  ##    ##
 ##  ## ## ##    ##
 ##  ##  ####    ##
 ##  ##   ###    ##
#### ##    ##    ##

class VRaySocketInt(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketInt'
    bl_label  = 'Integer socket'

    value = bpy.props.IntProperty(
        name = "Value",
        description = "Value",
        min = -1024,
        max =  1024,
        soft_min = -100,
        soft_max =  100,
        default = 1
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text)
        else:
            layout.prop(self, 'value', text=text)

    def draw_color(self, context, node):
        return (0.1, 0.4, 0.4, 1.00)


class VRaySocketIntNoValue(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketIntNoValue'
    bl_label  = 'Integer socket'

    value = bpy.props.IntProperty(
        name = "Value",
        description = "Value",
        min = -1024,
        max =  1024,
        soft_min = -100,
        soft_max =  100,
        default = 1
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.1, 0.4, 0.4, 1.00)


######## ##        #######     ###    ########
##       ##       ##     ##   ## ##      ##
##       ##       ##     ##  ##   ##     ##
######   ##       ##     ## ##     ##    ##
##       ##       ##     ## #########    ##
##       ##       ##     ## ##     ##    ##
##       ########  #######  ##     ##    ##

class VRaySocketFloat(bpy.types.NodeSocket, VRaySocketMult):
    bl_idname = 'VRaySocketFloat'
    bl_label  = 'Float socket'

    value = bpy.props.FloatProperty(
        name = "Value",
        description = "Value",
        precision = 3,
        min = -100000.0,
        max =  100000.0,
        soft_min = -100.0,
        soft_max =  100.0,
        default = 0.5
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw_color(self, context, node):
        return (0.1, 0.4, 0.4, 1.00)


class VRaySocketFloatNoValue(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketFloatNoValue'
    bl_label  = 'Float socket'

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 0.4, 1.00)


######## ##        #######     ###    ########     ######   #######  ##        #######  ########
##       ##       ##     ##   ## ##      ##       ##    ## ##     ## ##       ##     ## ##     ##
##       ##       ##     ##  ##   ##     ##       ##       ##     ## ##       ##     ## ##     ##
######   ##       ##     ## ##     ##    ##       ##       ##     ## ##       ##     ## ########
##       ##       ##     ## #########    ##       ##       ##     ## ##       ##     ## ##   ##
##       ##       ##     ## ##     ##    ##       ##    ## ##     ## ##       ##     ## ##    ##
##       ########  #######  ##     ##    ##        ######   #######  ########  #######  ##     ##

class VRaySocketFloatColor(bpy.types.NodeSocket, VRaySocketMult):
    bl_idname = 'VRaySocketFloatColor'
    bl_label  = 'Float color socket'

    value = bpy.props.FloatProperty(
        name = "Value",
        description = "Value",
        precision = 3,
        min = -100000.0,
        max =  100000.0,
        soft_min = -100.0,
        soft_max =  100.0,
        default = 0.5
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw_color(self, context, node):
        return (0.4, 0.4, 0.4, 1.00)


 ######   #######  ##        #######  ########
##    ## ##     ## ##       ##     ## ##     ##
##       ##     ## ##       ##     ## ##     ##
##       ##     ## ##       ##     ## ########
##       ##     ## ##       ##     ## ##   ##
##    ## ##     ## ##       ##     ## ##    ##
 ######   #######  ########  #######  ##     ##

class VRaySocketColor(bpy.types.NodeSocket, VRaySocketColorMult):
    bl_idname = 'VRaySocketColor'
    bl_label  = 'Color socket'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRaySocketColorNoValue(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketColorNoValue'
    bl_label  = 'Color socket'

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRaySocketColorUse(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketColorUse'
    bl_label  = 'Color socket with use flag'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    use = bpy.props.BoolProperty(
        name        = "Use",
        description = "Use socket",
        default     = False
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            split = layout.split(percentage=0.2)
            split.active = self.use
            split.prop(self, 'use', text="")
            split.label(text)
        else:
            row = layout.row(align=False)
            row.active = self.use
            row.prop(self, 'use', text="")
            rowCol = row.row()
            rowCol.scale_x = 0.3
            rowCol.prop(self, 'value', text="")
            row.label(text=text)

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


class VRaySocketColorMult(bpy.types.NodeSocket, VRaySocketMult):
    bl_idname = 'VRaySocketColorMult'
    bl_label  = 'Color socket with multiplier'

    value = bpy.props.FloatVectorProperty(
        name = "Color",
        description = "Color",
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        default = (1.0, 1.0, 1.0)
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw_color(self, context, node):
        return (1.000, 0.819, 0.119, 1.000)


##     ## ########  ######  ########  #######  ########
##     ## ##       ##    ##    ##    ##     ## ##     ##
##     ## ##       ##          ##    ##     ## ##     ##
##     ## ######   ##          ##    ##     ## ########
 ##   ##  ##       ##          ##    ##     ## ##   ##
  ## ##   ##       ##    ##    ##    ##     ## ##    ##
   ###    ########  ######     ##     #######  ##     ##

class VRaySocketVector(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketVector'
    bl_label  = 'Vector socket'

    value = bpy.props.FloatVectorProperty(
        name = "Vector",
        description = "Vector",
        subtype = 'TRANSLATION',
        soft_min = -1.0,
        soft_max = 1.0,
        default = (0.0, 0.0, 0.0)
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text)
        else:
            layout.label(text=text)
            layout.prop(self, 'value', text="")

    def draw_color(self, context, node):
        return (0.388, 0.388, 0.78, 1.000000)


 ######   #######   #######  ########  ########   ######
##    ## ##     ## ##     ## ##     ## ##     ## ##    ##
##       ##     ## ##     ## ##     ## ##     ## ##
##       ##     ## ##     ## ########  ##     ##  ######
##       ##     ## ##     ## ##   ##   ##     ##       ##
##    ## ##     ## ##     ## ##    ##  ##     ## ##    ##
 ######   #######   #######  ##     ## ########   ######

class VRaySocketCoords(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketCoords'
    bl_label  = 'Mapping socket'

    value = bpy.props.StringProperty(
        name        = "Defautl Coordinates",
        description = "Defautl coordinates",
        default     = "DEFAULTUVWC"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.250, 0.273, 0.750, 1.00)


class VRaySocketBRDF(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketBRDF'
    bl_label  = 'BRDF socket'

    value = bpy.props.StringProperty(
        name        = "Defautl BRDF",
        description = "Defautl BRDF",
        default     = "BRDFNOBRDFISSET"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.156, 0.750, 0.304, 1.000)


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

class VRaySocketMtl(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketMtl'
    bl_label  = 'Material Socket'

    value = bpy.props.StringProperty(
        name        = "Defautl Material",
        description = "Defautl material",
        default     = "MANOMATERIALISSET"
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.000, 0.468, 0.087, 1.000)


########   ##        ##     ##   ######    ####  ##    ##
##     ##  ##        ##     ##  ##    ##    ##   ###   ##
##     ##  ##        ##     ##  ##          ##   ####  ##
########   ##        ##     ##  ##   ####   ##   ## ## ##
##         ##        ##     ##  ##    ##    ##   ##  ####
##         ##        ##     ##  ##    ##    ##   ##   ###
##         ########   #######    ######    ####  ##    ##


class VRaySocketPlugin(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketPlugin'
    bl_label  = 'Plugin Socket'

    value = bpy.props.StringProperty(
        name        = "Plugin Name",
        description = "Plugin Name",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (1.000, 0.000, 1.000, 1.000)


########  ######## ##    ## ########  ######## ########      ######  ##     ##    ###    ##    ## ##    ## ######## ##
##     ## ##       ###   ## ##     ## ##       ##     ##    ##    ## ##     ##   ## ##   ###   ## ###   ## ##       ##
##     ## ##       ####  ## ##     ## ##       ##     ##    ##       ##     ##  ##   ##  ####  ## ####  ## ##       ##
########  ######   ## ## ## ##     ## ######   ########     ##       ######### ##     ## ## ## ## ## ## ## ######   ##
##   ##   ##       ##  #### ##     ## ##       ##   ##      ##       ##     ## ######### ##  #### ##  #### ##       ##
##    ##  ##       ##   ### ##     ## ##       ##    ##     ##    ## ##     ## ##     ## ##   ### ##   ### ##       ##
##     ## ######## ##    ## ########  ######## ##     ##     ######  ##     ## ##     ## ##    ## ##    ## ######## ########

class VRaySocketRenderChannel(bpy.types.NodeSocket, VRaySocketUse):
    bl_idname = 'VRaySocketRenderChannel'
    bl_label  = 'Render Channel Socket'

    value = bpy.props.StringProperty(
        name        = "",
        description = "",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.active = self.use
        split = layout.split()
        row = split.row(align=True)
        row.label(text)
        row.prop(self, 'use', text="")

    def draw_color(self, context, node):
        return (0.075, 0.619, 1.0, 1.000)


class VRaySocketRenderChannelOutput(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketRenderChannelOutput'
    bl_label  = 'Render Channel Ouput Socket'

    value = bpy.props.StringProperty(
        name        = "",
        description = "",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.075, 0.619, 1.0, 1.000)


######## ######## ######## ########  ######  ########  ######
##       ##       ##       ##       ##    ##    ##    ##    ##
##       ##       ##       ##       ##          ##    ##
######   ######   ######   ######   ##          ##     ######
##       ##       ##       ##       ##          ##          ##
##       ##       ##       ##       ##    ##    ##    ##    ##
######## ##       ##       ########  ######     ##     ######

class VRaySocketEffect(bpy.types.NodeSocket, VRaySocketUse):
    bl_idname = 'VRaySocketEffect'
    bl_label  = 'Effect Socket'

    value = bpy.props.StringProperty(
        name        = "",
        description = "",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.active = self.use
        split = layout.split()
        row = split.row(align=True)
        row.label(text)
        row.prop(self, 'use', text="")

    def draw_color(self, context, node):
        return (0.075, 0.619, 1.0, 1.000)


class VRaySocketEffectOutput(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketEffectOutput'
    bl_label  = 'Effect Socket Socket'

    value = bpy.props.StringProperty(
        name        = "",
        description = "",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.075, 0.619, 1.0, 1.000)


######## ########     ###    ##    ##  ######  ########  #######  ########  ##     ##
   ##    ##     ##   ## ##   ###   ## ##    ## ##       ##     ## ##     ## ###   ###
   ##    ##     ##  ##   ##  ####  ## ##       ##       ##     ## ##     ## #### ####
   ##    ########  ##     ## ## ## ##  ######  ######   ##     ## ########  ## ### ##
   ##    ##   ##   ######### ##  ####       ## ##       ##     ## ##   ##   ##     ##
   ##    ##    ##  ##     ## ##   ### ##    ## ##       ##     ## ##    ##  ##     ##
   ##    ##     ## ##     ## ##    ##  ######  ##        #######  ##     ## ##     ##

class VRaySocketTransform(bpy.types.NodeSocket):
    bl_idname = 'VRaySocketTransform'
    bl_label  = 'Transform Socket Socket'

    value = bpy.props.StringProperty(
        name        = "",
        description = "",
        default     = ""
    )

    vray_attr = bpy.props.StringProperty(
        name = "V-Ray Attribute",
        description = "V-Ray plugin attribute name",
        options = {'HIDDEN'},
        default = ""
    )

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.075, 0.619, 1.0, 1.000)


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRaySocketGeom,
        VRaySocketObject,
        VRaySocketInt,
        VRaySocketIntNoValue,
        VRaySocketFloat,
        VRaySocketFloatColor,
        VRaySocketFloatNoValue,
        VRaySocketColor,
        VRaySocketColorNoValue,
        VRaySocketColorUse,
        VRaySocketColorMult,
        VRaySocketVector,
        VRaySocketCoords,
        VRaySocketBRDF,
        VRaySocketMtl,
        VRaySocketRenderChannel,
        VRaySocketRenderChannelOutput,
        VRaySocketEffect,
        VRaySocketEffectOutput,
        VRaySocketTransform,
        VRaySocketPlugin,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

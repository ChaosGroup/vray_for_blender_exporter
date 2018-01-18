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
import copy
import hashlib
import mathutils

from vb30.lib import AttributeUtils
from vb30.debug import Debug
from vb30.plugins import PLUGINS_ID

DYNAMIC_SOCKET_OVERRIDES = {}
DYNAMIC_SOCKET_CLASSES = set()
DYNAMIC_SOCKET_CLASS_NAMES = set()


def CheckLinkedSockets(node_sockets):
    for sock in node_sockets:
        if sock.is_linked:
            return True
    return False


def FindPluginUIAttr(plugin, attrName):
    pluginParams = PLUGINS_ID[plugin].PluginParams
    for param in pluginParams:
        if param['attr'] == attrName:
            return param.get('ui', dict())
    return None


def GetDynamicSocketClass(pluginName, socketTypeName, attrName):
    def abbreviateTitle(str):
        return ''.join(filter(lambda c: c >= 'A' and c <= 'Z', str))

    # make the typeName unique per type, node and attribute
    suffix = '%s_%s' % (abbreviateTitle(pluginName), attrName)
    typeName = '%s_%s' % (socketTypeName, suffix)
    # bpy has obscene limitation of 64 symbols for class name!
    if len(typeName) >= 64:
        hashed = hashlib.sha1(typeName.encode('utf-8')).hexdigest()
        hashLen = 64 - 1 - (len(socketTypeName) + 1)
        typeName = "%s_%s" % (socketTypeName, hashed[0:hashLen])
    return typeName


def RegisterDynamicSocketClass(pluginName, socketTypeName, attrName):
    global DYNAMIC_SOCKET_CLASSES
    global DYNAMIC_SOCKET_CLASS_NAMES

    if not attrName:
        Debug("Could not register dynamic socket type for %s::%s" % (node.bl_idname, socketTypeName), msgType='ERROR')
        return

    if socketTypeName not in DYNAMIC_SOCKET_OVERRIDES:
        return

    typeName = GetDynamicSocketClass(pluginName, socketTypeName, attrName)

    if not hasattr(bpy.types, typeName):
        INFO_BASESES = 0
        INFO_DYNAMIC_ATTR = 1
        INFO_ATTRIBUTES = 2

        typeInfo = copy.deepcopy(DYNAMIC_SOCKET_OVERRIDES[socketTypeName])
        overrideName = typeInfo[INFO_DYNAMIC_ATTR][0]
        overrideType = typeInfo[INFO_DYNAMIC_ATTR][1]
        overrideParams = typeInfo[INFO_DYNAMIC_ATTR][2]

        pluginParam = FindPluginUIAttr(pluginName, attrName)
        if pluginParam:
            overrideParams['soft_min'] = pluginParam.get('soft_min', -100)
            overrideParams['soft_max'] = pluginParam.get('soft_max',  100)
        typeInfo[INFO_ATTRIBUTES][overrideName] = overrideType(**overrideParams)

        typeInfo[INFO_ATTRIBUTES]['bl_idname'] = typeName
        typeInfo[INFO_ATTRIBUTES]['vray_socket_base_type'] = bpy.props.StringProperty(
            name = "V-Ray Attribute",
            description = "V-Ray plugin socket attribute",
            options = {'HIDDEN'},
            default = ""
        )
        newType = type(
            typeName,
            typeInfo[INFO_BASESES],
            typeInfo[INFO_ATTRIBUTES],
        )
        bpy.utils.register_class(newType)
        DYNAMIC_SOCKET_CLASSES.add(newType)
        DYNAMIC_SOCKET_CLASS_NAMES.add(typeName)


def AddInput(node, socketType, socketName, attrName=None, default=None):
    if socketName in node.inputs:
        return

    baseType = socketType
    foundPlugin = None
    if attrName and socketType in DYNAMIC_SOCKET_OVERRIDES:
        # get possible plugins for this node
        test_plugins = []
        if hasattr(node, 'vray_plugin'):
            test_plugins.append(node.vray_plugin)
        if hasattr(node, 'vray_plugins'):
            for plugin in node.vray_plugins:
                test_plugins.append(plugin)

        for attr in dir(node):
            if attr in PLUGINS_ID:
                test_plugins.append(attr)

        # test each plugin to find where this attribute comes from
        for plugin in test_plugins:
            dynamicType = GetDynamicSocketClass(plugin, socketType, attrName)
            if dynamicType in DYNAMIC_SOCKET_CLASS_NAMES:
                foundPlugin = plugin
                socketType = dynamicType
                break

        # fall-back to static socket type
        if len(test_plugins) == 0:
            Debug("Can't find vray_plugins for %s" % node.bl_idname, msgType='ERROR')
            foundPlugin = 'NONE'
            socketType = baseType

        if not foundPlugin:
            Debug("Can't find dynamic socket type for: %s::%s" % (node.bl_idname, socketName), msgType='ERROR')
            return

    # register the socket for this node
    node.inputs.new(socketType, socketName)
    createdSocket = node.inputs[socketName]

    if attrName is not None:
        if not hasattr(createdSocket, 'vray_attr'):
            Debug("vray_attr mising from socketType: %s::%s" % (node.bl_idname, socketName), msgType='ERROR')
        else:
            createdSocket.vray_attr = attrName

    if hasattr(createdSocket, 'vray_socket_base_type'):
        createdSocket.vray_socket_base_type = baseType

    if default is not None:
        # Some socket intensionally have no 'value'
        if hasattr(createdSocket, 'value'):
            # we are interested if the base type is not scalar
            if baseType in {'VRaySocketColor', 'VRaySocketVector'}:
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
        elif self.is_linked and not _is_connected_muted(self):
            split = layout.split(percentage=0.4)
            split.prop(self, 'value', text="")
            split.prop(self, 'multiplier', text=text)
        elif type(self.value) is mathutils.Color:
            split = layout.split(percentage=0.4)
            split.prop(self, 'value', text="")
            split.label(text=text)
        else:
            layout.prop(self, 'value', text=text)


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

class VRaySocketColor(bpy.types.NodeSocket, VRaySocketMult):
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

DYNAMIC_SOCKET_OVERRIDES = {
    'VRaySocketInt': (
        (bpy.types.NodeSocket, ),
        (
            'value', bpy.props.IntProperty, {
                'name':  "Value",
                'description':  "Value",
                'min':  -1024,
                'max':   1024,
                'soft_min':  -100,
                'soft_max':   100,
                'default':  1
            }
        ),
        {
            'bl_label': 'Integer socket',
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw': VRaySocketInt.draw,
            'draw_color': VRaySocketInt.draw_color,
        }
    ),
    'VRaySocketIntNoValue': (
        (bpy.types.NodeSocket, ),
        (
            'value', bpy.props.IntProperty, {
                'name': "Value",
                'description': "Value",
                'min': -1024,
                'max':  1024,
                'soft_min': -100,
                'soft_max':  100,
                'default': 1
            }
        ),
        {
            'bl_label' : 'Integer socket',
            'vray_attr' : bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw': VRaySocketIntNoValue.draw,
            'draw_color': VRaySocketIntNoValue.draw_color,
        }
    ),
    'VRaySocketFloat': (
        (bpy.types.NodeSocket, VRaySocketMult),
        (
            'value', bpy.props.FloatProperty, {
                'name': "Value",
                'description': "Value",
                'precision': 3,
                'min': -100000.0,
                'max':  100000.0,
                'soft_min': -100.0,
                'soft_max':  100.0,
                'default': 0.5
            }
        ),
        {
            'bl_label': 'Float socket',
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw_color': VRaySocketFloat.draw_color
        }
    ),
    'VRaySocketFloatColor': (
        (bpy.types.NodeSocket, VRaySocketMult),
        (
            'value', bpy.props.FloatProperty, {
                'name': "Value",
                'description': "Value",
                'precision': 3,
                'min': -100000.0,
                'max':  100000.0,
                'soft_min': -100.0,
                'soft_max':  100.0,
                'default': 0.5
            }
        ),
        {
            'bl_label' : 'Float color socket',
            'vray_attr' : bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw_color': VRaySocketFloatColor.draw_color
        }
    ),
    'VRaySocketColor': (
        (bpy.types.NodeSocket, VRaySocketMult),
        (
            'value', bpy.props.FloatVectorProperty, {
                'name': "Color",
                'description': "Color",
                'subtype': 'COLOR',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.0,
                'soft_max': 1.0,
                'default': (1.0, 1.0, 1.0)
            }
        ),
        {
            'bl_label': 'Color socket',
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw_color': VRaySocketColor.draw_color
        }
    ),
    'VRaySocketColorUse': (
        (bpy.types.NodeSocket, ),
        (
            'value', bpy.props.FloatVectorProperty, {
                'name': "Color",
                'description': "Color",
                'subtype': 'COLOR',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.0,
                'soft_max': 1.0,
                'default': (1.0, 1.0, 1.0)
            }
        ),
        {
            'bl_label':  'Color socket with use flag',
            'use': bpy.props.BoolProperty(
                name        = "Use",
                description = "Use socket",
                default     = False
            ),
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw': VRaySocketColorUse.draw,
            'draw_color': VRaySocketColorUse.draw_color,
        }
    ),
    'VRaySocketColorMult': (
        (bpy.types.NodeSocket, VRaySocketMult),
        (
            'value', bpy.props.FloatVectorProperty, {
                'name': "Color",
                'description': "Color",
                'subtype': 'COLOR',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.0,
                'soft_max': 1.0,
                'default': (1.0, 1.0, 1.0)
            }
        ),
        {
            'bl_label':  'Color socket with multiplier',
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw_color': VRaySocketColorMult.draw_color,
        }
    ),
    'VRaySocketVector': (
        (bpy.types.NodeSocket, ),
        (
            'value', bpy.props.FloatVectorProperty, {
                'name': "Vector",
                'description': "Vector",
                'subtype': 'TRANSLATION',
                'soft_min': -1.0,
                'soft_max': 1.0,
                'default': (0.0, 0.0, 0.0)
            }
        ),
        {
            'bl_label':  'Vector socket',
            'vray_attr': bpy.props.StringProperty(
                name = "V-Ray Attribute",
                description = "V-Ray plugin attribute name",
                options = {'HIDDEN'},
                default = ""
            ),
            'draw': VRaySocketVector.draw,
            'draw_color': VRaySocketVector.draw_color,
        }
    )
}


def InitDynamicSocketTypes():
    skip_plugins = {"GeomVRayPattern", "Node", "VRayExporter", "Includer",
        "CameraStereoscopic", "ExportSets", "VRayQuickSettings"}

    for pluginId in PLUGINS_ID:
        if pluginId in skip_plugins:
            continue
        pluginDesc = PLUGINS_ID[pluginId]
        if not hasattr(pluginDesc, 'PluginParams'):
            Debug("Plugin [%s] missing Pluginparams" % pluginId, msgType='ERROR')
            continue
        pluginParams = pluginDesc.PluginParams
        for param in pluginParams:
            attrName = param.get('attr', None)
            paramType = param.get('type', None)
            paramSocketType = AttributeUtils.TypeToSocket.get(param.get('type', None), None)
            if not paramSocketType:
                continue
            RegisterDynamicSocketClass(pluginId, paramSocketType, attrName)


def register():
    InitDynamicSocketTypes()

    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)



def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    for regClass in DYNAMIC_SOCKET_CLASSES:
        bpy.utils.unregister_class(regClass)

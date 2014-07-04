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

import os
import binascii
import struct

import bpy
import mathutils

from vb30.plugins import PLUGINS_ID
from vb30.lib     import AttributeUtils
from vb30.lib     import PathUtils

from vb30 import debug

from .sockets import AddInput, AddOutput
from .utils   import GetConnectedNode


def getOutputSocket(pluginID):
    if pluginID == "BRDFLayered":
        return "BRDF"
    elif pluginID == "BitmapBuffer":
        return "Bitmap"
    elif pluginID in PLUGINS_ID:
        pluginModule = PLUGINS_ID[pluginID]

        if pluginModule.TYPE == 'MATERIAL':
            return "Material"
        elif pluginModule.TYPE == 'UVWGEN':
            return "Mapping"
        elif pluginModule.TYPE == 'BRDF':
            return "BRDF"
        elif pluginModule.TYPE == 'GEOMETRY':
            return "Geomtery"
        elif pluginModule.TYPE == 'EFFECT':
            return "Output"
        elif pluginModule.TYPE == 'RENDERCHANNEL':
            return "Channel"
        elif pluginModule.TYPE == 'TEXTURE':
            return "Output"

    return "Output"


def getPluginByName(vrsceneDict, pluginName):
    for pluginDesc in vrsceneDict:
        if pluginDesc['Name'] == pluginName:
            return pluginDesc
    return None


def getPluginByType(vrsceneDict, pluginID):
    for pluginDesc in vrsceneDict:
        if pluginDesc['ID'] == pluginID:
            return pluginDesc
    return None


def getParamDesc(pluginParams, attrName):
    for paramDesc in pluginParams:
        if paramDesc['attr'] == attrName:
            return paramDesc
    return None


def getSocketName(pluginParams, attrName):
    attrDesc = getParamDesc(pluginParams, attrName)
    if not attrDesc:
        return None
    return attrDesc.get('name', AttributeUtils.GetNameFromAttr(attrDesc['attr']))


def getOutputSocketByAttr(node, attrName):
    for sock in node.outputs:
        if hasattr(sock, 'vray_attr'):
            if sock.vray_attr == attrName:
                return sock
    return getOutputSocket(node.vray_type)


def FindAndCreateNode(vrsceneDict, pluginName, ntree, prevNode):
    if not pluginName:
        return None
    pluginDesc = getPluginByName(vrsceneDict, pluginName)
    if not pluginDesc:
        return None
    return createNode(ntree, prevNode, vrsceneDict, pluginDesc)


######## ######## ##     ##       ##          ###    ##    ## ######## ########  ######## ########
   ##    ##        ##   ##        ##         ## ##    ##  ##  ##       ##     ## ##       ##     ##
   ##    ##         ## ##         ##        ##   ##    ####   ##       ##     ## ##       ##     ##
   ##    ######      ###          ##       ##     ##    ##    ######   ########  ######   ##     ##
   ##    ##         ## ##         ##       #########    ##    ##       ##   ##   ##       ##     ##
   ##    ##        ##   ##        ##       ##     ##    ##    ##       ##    ##  ##       ##     ##
   ##    ######## ##     ##       ######## ##     ##    ##    ######## ##     ## ######## ########

def createNodeTexLayered(ntree, n, vrsceneDict, pluginDesc):
    textures    = pluginDesc['Attributes']['textures']
    blend_modes = pluginDesc['Attributes']['blend_modes']

    texLayeredNode = ntree.nodes.new('VRayNodeTexLayered')

    for i,tex in enumerate(reversed(textures)):
        humanIndex = i + 1
        texSockName = "Texture %i" % humanIndex

        # NOTE: Node already has two inputs
        if i > 1:
            AddInput(texLayeredNode, 'VRaySocketTexLayered', texSockName)

        texSocket = texLayeredNode.inputs[texSockName]
        texSocket.value = str(blend_modes[i])

        texPlugName   = tex
        texPlugOutput = None
        texNode       = None

        # It looks like param is color
        # This is support for cases like this:
        #    textures = List(AColor(0.0,0.0,0.0,1.0),SomeTexture);
        if type(texPlugName) is tuple:
            texAColor = {
                'ID'         : 'TexAColor',
                'Name'       : 'Color',
                'Attributes' : {
                    'texture' : texPlugName
                }
            }
            texNode = createNode(ntree, texLayeredNode, vrsceneDict, texAColor)

        # Params is texture
        else:
            if texPlugName.find("::") != -1:
                texPlugName, texPlugOutput = texPlugName.split("::")
                texPlugOutput = AttributeUtils.GetNameFromAttr(texPlugOutput)

            texPlugin = getPluginByName(vrsceneDict, texPlugName)
            if texPlugin is None:
                print("Plugin '%s' not found in the vrscene file!" % texPlugName)
                continue

            texNode = createNode(ntree, texLayeredNode, vrsceneDict, texPlugin)

        if texPlugOutput is None:
            texPlugOutput = getOutputSocket(texPlugin['ID'])

        if texNode:
            ntree.links.new(texNode.outputs[texPlugOutput], texSocket)

    for attrName in pluginDesc['Attributes']:
        # Skip lists
        if attrName in {'textures', 'blend_modes'}:
            continue

        attrValue = pluginDesc['Attributes'][attrName]

        if hasattr(texLayeredNode, attrName):
            setattr(texLayeredNode, attrName, attrValue)

    return texLayeredNode


########  ########  ########  ########       ##          ###    ##    ## ######## ########  ######## ########
##     ## ##     ## ##     ## ##             ##         ## ##    ##  ##  ##       ##     ## ##       ##     ##
##     ## ##     ## ##     ## ##             ##        ##   ##    ####   ##       ##     ## ##       ##     ##
########  ########  ##     ## ######         ##       ##     ##    ##    ######   ########  ######   ##     ##
##     ## ##   ##   ##     ## ##             ##       #########    ##    ##       ##   ##   ##       ##     ##
##     ## ##    ##  ##     ## ##             ##       ##     ##    ##    ##       ##    ##  ##       ##     ##
########  ##     ## ########  ##             ######## ##     ##    ##    ######## ##     ## ######## ########

def createNodeBRDFLayered(ntree, n, vrsceneDict, pluginDesc):
    def processSocket(thisNode, socket, attrValue):
        # Could happen with some broken files
        if not attrValue:
            return

        plName   = attrValue
        plOutput = None
        if plName.find("::") != -1:
            plName, plOutput = plName.split("::")
            plOutput = AttributeUtils.GetNameFromAttr(plOutput)

        pl = getPluginByName(vrsceneDict, plName)
        if pl:
            # Get default output
            if plOutput is None:
                plOutput = getOutputSocket(pl['ID'])

            inNode = createNode(ntree, thisNode, vrsceneDict, pl)
            if inNode:
                ntree.links.new(inNode.outputs[plOutput], socket)
        else:
            socket.value = attrValue

    brdfs   = pluginDesc['Attributes'].get('brdfs')
    weights = pluginDesc['Attributes'].get('weights')

    brdfLayeredNode = ntree.nodes.new('VRayNodeBRDFLayered')

    if brdfs:
        for i,brdf in enumerate(brdfs):
            humanIndex = i + 1

            brdfSockName   = "BRDF %s"   % humanIndex
            weightSockName = "Weight %s" % humanIndex

            # NOTE: Node already has two inputs
            if not brdfSockName in brdfLayeredNode.inputs:
                AddInput(brdfLayeredNode, 'VRaySocketBRDF',       brdfSockName)
                AddInput(brdfLayeredNode, 'VRaySocketFloatColor', weightSockName)
                brdfLayeredNode.inputs[weightSockName].value = 1.0

            brdfSocket   = brdfLayeredNode.inputs[brdfSockName]
            weightSocket = brdfLayeredNode.inputs[weightSockName]

            processSocket(brdfLayeredNode, brdfSocket,   brdf)

            # NOTE: 'weights' could be optional
            if weights:
                processSocket(brdfLayeredNode, weightSocket, weights[i])

    for attrName in pluginDesc['Attributes']:
        # Skip lists
        if attrName in {'brdfs', 'weights'}:
            continue

        attrValue = pluginDesc['Attributes'][attrName]

        if hasattr(brdfLayeredNode, attrName):
            setattr(brdfLayeredNode, attrName, attrValue)

    return brdfLayeredNode


########  #### ######## ##     ##    ###    ########        ########  ##     ## ######## ######## ######## ########
##     ##  ##     ##    ###   ###   ## ##   ##     ##       ##     ## ##     ## ##       ##       ##       ##     ##
##     ##  ##     ##    #### ####  ##   ##  ##     ##       ##     ## ##     ## ##       ##       ##       ##     ##
########   ##     ##    ## ### ## ##     ## ########        ########  ##     ## ######   ######   ######   ########
##     ##  ##     ##    ##     ## ######### ##              ##     ## ##     ## ##       ##       ##       ##   ##
##     ##  ##     ##    ##     ## ##     ## ##              ##     ## ##     ## ##       ##       ##       ##    ##
########  ####    ##    ##     ## ##     ## ##              ########   #######  ##       ##       ######## ##     ##

def LoadImage(imageFilepath, importDir, bitmapTexture, makeRelative=False):
    if imageFilepath is not None:
        if not os.path.exists(imageFilepath):
            debug.PrintError("Couldn't find file: %s" % imageFilepath)
            debug.PrintError("Trying to search under import diretory...")

            # NOTE: Windows style filepath could be stored here
            # Convert to UNIX slashes
            imageFilepath = PathUtils.UnifyPath(imageFilepath)

            if importDir:
                imageFilepath = os.path.join(importDir, os.path.basename(imageFilepath))

        if not os.path.exists(imageFilepath):
            debug.PrintError("Unable to find file: %s" % imageFilepath)
        else:
            imageBlockName = bpy.path.display_name_from_filepath(imageFilepath)
            imageFilepath = imageFilepath.replace("\\", "/")

            if imageBlockName in bpy.data.images:
                bitmapTexture.image = bpy.data.images[imageBlockName]
            else:
                bitmapTexture.image = bpy.data.images.load(imageFilepath)
                bitmapTexture.image.name = imageBlockName

            if makeRelative:
                bitmapTexture.image.filepath = bpy.path.relpath(bitmapTexture.image.filepath)


def createNodeBitmapBuffer(ntree, n, vrsceneDict, pluginDesc):
    pluginModule = PLUGINS_ID.get('BitmapBuffer')

    bitmatBuffer = ntree.nodes.new('VRayNodeBitmapBuffer')
    propGroup = bitmatBuffer.BitmapBuffer

    bitmapTexture = bitmatBuffer.texture

    imageFilepath = pluginDesc['Attributes'].get('file')

    importSettings = getPluginByName(vrsceneDict, "Import Settings")
    if importSettings:
        importDir = importSettings['Attributes']['dirpath']

    LoadImage(imageFilepath, importDir, bitmapTexture)

    for attrName in pluginDesc['Attributes']:
        attrDesc  = getParamDesc(pluginModule.PluginParams, attrName)

        attrValue = pluginDesc['Attributes'][attrName]

        if hasattr(propGroup, attrName):
            if attrDesc['type'] == 'ENUM':
                attrValue = str(attrValue)
                if not AttributeUtils.ValueInEnumItems(attrDesc, attrValue):
                    debug.PrintError("Unsupported ENUM value '%s' for attribute: %s.%s" %
                        (attrValue, 'BitmapBuffer', attrName))
                    continue
            setattr(propGroup, attrName, attrValue)

    return bitmatBuffer


########     ###    ##     ## ########   ######
##     ##   ## ##   ###   ### ##     ## ##    ##
##     ##  ##   ##  #### #### ##     ## ##
########  ##     ## ## ### ## ########   ######
##   ##   ######### ##     ## ##              ##
##    ##  ##     ## ##     ## ##        ##    ##
##     ## ##     ## ##     ## ##         ######

CollapsibleTypes = {
    'TexAColor',
    'TexCombineColor',
}


def CollapseToValue(pluginDesc):
    pluginID    = pluginDesc['ID']
    pluginAttrs = pluginDesc['Attributes']

    if pluginID == 'TexAColor':
        color = pluginAttrs['texture']
        # 'color' is mapped, nothing to do
        if type(color) is str:
            return None
        return color

    elif pluginID == 'TexCombineColor':
        color   = pluginAttrs['color']
        texture = pluginAttrs['texture']

        texture_multiplier = pluginAttrs['texture_multiplier']

        # 'texture' is mapped, nothing to do
        if type(texture) is str:
            return None

        # TODO: Finish value calculations

        return 0.0

    return None


def FillRamp(vrsceneDict, ramp, colors, positions):
    RampElements = []

    for col, pos in zip(colors, positions):
        rampElement = {
            'color'    : col,
            'position' : pos,
        }

        for key in rampElement:
            value = rampElement[key]

            if type(value) is str:
                conPlugin   = getPluginByName(vrsceneDict, value)
                conPluginID = conPlugin['ID']

                if conPluginID not in CollapsibleTypes:
                    debug.PrintError("Plugin '%s': Unsupported parameter value! This shouldn't happen! Please, report this!" % conPluginID)
                    rampElement[key] = None
                else:
                    rampElement[key] = CollapseToValue(conPlugin)

        RampElements.append(rampElement)

    # Create ramp elements
    # Ramp already has 2 elements
    elementsToCreate = len(RampElements) - 2
    for i in range(elementsToCreate):
        # We will setup proper position later
        ramp.elements.new(0.0)

    # Setup elements values
    elementStep = 1.0 / len(ramp.elements)

    for i,rampElement in enumerate(RampElements):
        col = rampElement['color']
        if col is None:
            col = (1.0,1.0,1.0)

        pos = rampElement['position']
        if pos is None:
            pos = i * elementStep

        el = ramp.elements[i]
        el.color    = col
        el.position = pos


def createNodeTexGradRamp(ntree, prevNode, vrsceneDict, pluginDesc):
    pluginModule = PLUGINS_ID.get('TexGradRamp')
    texGradRamp  = ntree.nodes.new('VRayNodeTexGradRamp')
    propGroup    = texGradRamp.TexGradRamp

    attributes   = pluginDesc['Attributes']

    FillRamp(vrsceneDict,
        texGradRamp.texture.color_ramp,
        attributes['colors'],
        attributes['positions']
    )

    return texGradRamp


def createNodeTexRemap(ntree, prevNode, vrsceneDict, pluginDesc):
    pluginModule = PLUGINS_ID.get('TexRemap')
    texTexRemap  = ntree.nodes.new('VRayNodeTexRemap')
    propGroup    = texTexRemap.TexRemap

    attributes   = pluginDesc['Attributes']

    FillRamp(vrsceneDict,
        texTexRemap.texture.color_ramp,
        attributes['color_colors'],
        attributes['color_positions']
    )

    return texTexRemap


 ######   ######## ##    ## ######## ########  ####  ######
##    ##  ##       ###   ## ##       ##     ##  ##  ##    ##
##        ##       ####  ## ##       ##     ##  ##  ##
##   #### ######   ## ## ## ######   ########   ##  ##
##    ##  ##       ##  #### ##       ##   ##    ##  ##
##    ##  ##       ##   ### ##       ##    ##   ##  ##    ##
 ######   ######## ##    ## ######## ##     ## ####  ######

def createNode(ntree, prevNode, vrsceneDict, pluginDesc):
    from vb30.plugins import PLUGINS_ID

    pluginID    = pluginDesc['ID']
    pluginName  = pluginDesc['Name']
    pluginAttrs = pluginDesc['Attributes']

    for n in ntree.nodes:
        if n.name == pluginName:
            return ntree.nodes[pluginName]

    if pluginID == 'TexLayered':
        return createNodeTexLayered(ntree, prevNode, vrsceneDict, pluginDesc)

    elif pluginID == 'BRDFLayered':
        return createNodeBRDFLayered(ntree, prevNode, vrsceneDict, pluginDesc)

    elif pluginID == 'BitmapBuffer':
        return createNodeBitmapBuffer(ntree, prevNode, vrsceneDict, pluginDesc)

    elif pluginID == 'TexGradRamp':
        return createNodeTexGradRamp(ntree, prevNode, vrsceneDict, pluginDesc)

    elif pluginID == 'TexRemap':
        return createNodeTexRemap(ntree, prevNode, vrsceneDict, pluginDesc)

    else:
        pluginModule = PLUGINS_ID.get(pluginID)
        if pluginModule is None:
            debug.PrintError("Plugin '%s' is not yet supported! This shouldn't happen! Please, report this!" % pluginID)
            return None

        n = ntree.nodes.new('VRayNode%s' % pluginID)
        n.name = pluginName

        # This property group holds all plugin settings
        #
        propGroup = getattr(n, pluginID)

        # Now go through all plugin attributes and check
        # if we should create other nodes or simply set the value
        #
        for attrName in pluginAttrs:
            attrValue = pluginAttrs[attrName]

            # NOTE: Fixes vrscene exported from other applications using deprecated 'bump_tex'
            # attribute
            fixBump = False
            if attrName == 'bump_tex':
                fixBump  = True
                attrName = 'bump_tex_color'

            attrDesc  = getParamDesc(pluginModule.PluginParams, attrName)
            if attrDesc is None:
                # XXX: This could happen when loading VISMATS; error message disabled here...
                # print("Plugin '%s': Attribute '%s' is not yet supported! This is very strange!" % (pluginID, attrName))
                continue

            attrSocketName = getSocketName(pluginModule.PluginParams, attrName)

            # Attribute is a output type - nothing to do
            if attrDesc['type'] in AttributeUtils.OutputTypes:
                continue

            if attrDesc['type'] == 'MATRIX':
                mNode = ntree.nodes.new('VRayNodeMatrix')

                m = mathutils.Matrix()
                m.identity()

                if type(attrValue) in {list, tuple}:
                    for c in range(3):
                        for r in range(3):
                            m[c][r] = attrValue[r][c]

                else:
                    tmArray = struct.unpack("fffffffff", binascii.unhexlify(bytes(attrValue, 'ascii')))
                    i = 0
                    for c in range(3):
                        for r in range(3):
                            m[c][r] = tmArray[i]
                            i += 1

                _tmp, rotate, scale = m.decompose()
                rotate = rotate.to_euler('XYZ')

                tmNode.rotate = (rotate[0], rotate[1], rotate[2])
                tmNode.scale  = (scale[0],  scale[1],  scale[2])

                ntree.links.new(
                    mNode.outputs['Matrix'],
                    n.inputs[attrSocketName]
                )

                continue

            if attrDesc['type'] == 'TRANSFORM':
                tmNode = ntree.nodes.new('VRayNodeTransform')

                m = mathutils.Matrix()
                m.identity()

                if type(attrValue) in {list, tuple}:
                    tmM    = attrValue[0]
                    tmOffs = attrValue[1]

                    for c in range(3):
                        for r in range(3):
                            m[c][r] = tmM[r][c]
                    for c in range(3):
                        m[c][3] = tmOffs[c]

                else:
                    tmArray = struct.unpack("fffffffffddd", binascii.unhexlify(bytes(attrValue, 'ascii')))
                    i = 0
                    for c in range(3):
                        for r in range(3):
                            m[c][r] = tmArray[i]
                            i += 1

                offset, rotate, scale = m.decompose()
                rotate = rotate.to_euler('XYZ')

                tmNode.offset = (offset[0], offset[1], offset[2])
                tmNode.rotate = (rotate[0], rotate[1], rotate[2])
                tmNode.scale  = (scale[0],  scale[1],  scale[2])

                ntree.links.new(
                    tmNode.outputs['Transform'],
                    n.inputs[attrSocketName]
                )

                continue

            if attrDesc['type'] not in AttributeUtils.InputTypes:
                # Attribute is not mappable, so simply set it's value
                if attrDesc['type'] == 'ENUM':
                    attrValue = str(attrValue)

                    if not AttributeUtils.ValueInEnumItems(attrDesc, attrValue):
                        debug.PrintError("Unsupported ENUM value '%s' for attribute: %s.%s" %
                            (attrValue, pluginID, attrName))
                        attrValue = None

                if attrValue is not None:
                    setattr(propGroup, attrName, attrValue)

            else:
                # Attribute could possibly be mapped with other node
                # Check if we could find requested node in a vrsceneDict
                if type(attrValue) is str:
                    inPluginName   = attrValue
                    inPluginOutput = None

                    # Check if a specific output is requested (like MyTexture::out_intensity)
                    if inPluginName.find("::") != -1:
                        inPluginName, inPluginOutput = attrValue.split("::")

                    # Set socket value
                    connectedPlugin = getPluginByName(vrsceneDict, inPluginName)
                    if connectedPlugin is None:
                        if type(attrValue) is str:
                            # TODO: finish this or check if None is ok here
                            if attrDesc['type'] == 'ENUM':
                                pass
                        else:
                            attrSocket = n.inputs[attrSocketName]
                            attrSocket.value = attrValue

                    # Create connected plugin
                    else:
                        connectedPluginID = connectedPlugin['ID']

                        # TODO:
                        # 1. Check if connected pluginID is in collapseable type
                        # 2. Check if it doesn't have any input connections
                        # 3. Collapse to value

                        inPluginOutputSocketName = AttributeUtils.GetNameFromAttr(inPluginOutput) if inPluginOutput else getOutputSocket(connectedPluginID)

                        connectedNode = createNode(ntree, n, vrsceneDict, connectedPlugin)
                        if connectedNode:
                            ntree.links.new(connectedNode.outputs[inPluginOutputSocketName], n.inputs[attrSocketName])

                            if fixBump:
                                ntree.links.new(
                                    getOutputSocketByAttr(connectedNode, 'out_intensity'),
                                    n.inputs['Float Texture']
                                )

                # Attr is not linked - set socket default value
                else:
                    attrSocket = n.inputs[attrSocketName]

                    # Fix for color attribute
                    if type(attrValue) in [list, tuple]:
                        if len(attrValue) == 4:
                            attrValue = attrValue[:3]

                    attrSocket.value = attrValue

    return n

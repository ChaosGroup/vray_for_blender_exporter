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

from vb30.lib import LibUtils
from vb30.lib import AttributeUtils

from . import sockets as SocketUtils


def GetNodeName(ntree, node):
    return LibUtils.CleanString("NT%sN%s" % (ntree.name, node.name))


def GetConnectedNode(ntree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_node:
            return l.from_node
    return None


def GetConnectedSocket(ntree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_socket:
            return l.from_socket
    return None


def GetNodesByType(ntree, nodeType):
    for n in ntree.nodes:
        if n.bl_idname == nodeType:
            yield n


def GetNodeByType(ntree, nodeType):
    if not ntree:
        return None
    for n in ntree.nodes:
        if n.bl_idname == nodeType:
            return n
    return None


def CopyRamp(ramp, rampCopy):
    # Create ramp elements
    # Ramp already has 2 elements
    elementsToCreate = len(ramp.elements) - 2
    for i in range(elementsToCreate):
        # We will setup proper position later
        rampCopy.elements.new(0.0)

    for i,rampElement in enumerate(ramp.elements):
        el = rampCopy.elements[i]
        el.color    = rampElement.color
        el.position = rampElement.position


def CreateFakeName():
    return ".VRayFakeTexture@%s" % LibUtils.GetUUID()


def CreateFakeTextureAttribute(cls, attrName='texture'):
    setattr(cls, attrName, bpy.props.PointerProperty(
        name = "Texture",
        type = bpy.types.Texture,
        description = "Fake texture for internal usage",
    ))

    # NOTE: We will store associated texture name for further possible
    # refactor to find the texture used by this datablock simply by name
    # and restore pointers
    #
    setattr(cls, '%s_name' % attrName, bpy.props.StringProperty(
        name = "Texture Name",
        options = {'HIDDEN'},
        description = "Associated texture name",
        default = 'NONE'
    ))


def CreateRampTexture(self, attrName='texture'):
    texName = CreateFakeName()

    tex = bpy.data.textures.new(texName, 'NONE')
    tex.use_color_ramp = True
    tex.use_fake_user = True

    setattr(self, attrName, tex)
    setattr(self, '%s_name' % attrName, texName)


def CreateBitmapTexture(self, attrName='texture'):
    texName = CreateFakeName()

    tex = bpy.data.textures.new(texName, 'IMAGE')
    tex.use_fake_user = True

    setattr(self, attrName, tex)
    setattr(self, '%s_name' % attrName, texName)


def AddDefaultInputs(self, vrayPlugin, attrFilter=None):
    for attr in vrayPlugin.PluginParams:
        attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

        attr_options = attr.get('options', [])

        if attrFilter and attr['attr'] in attrFilter:
            continue

        if attr['type'] in AttributeUtils.InputTypes:
            TypeToSocket = AttributeUtils.TypeToSocket
            if self.vray_type == 'LIGHT' or 'LINKED_ONLY' in attr_options:
                TypeToSocket = AttributeUtils.TypeToSocketNoValue

            SocketUtils.AddInput(self, TypeToSocket[attr['type']], attr_name, attr['attr'], attr['default'])


def AddDefaultOutputs(self, vrayPlugin):
    for attr in vrayPlugin.PluginParams:
        attr_name = attr.get('name', AttributeUtils.GetNameFromAttr(attr['attr']))

        attr_options = attr.get('options', {})

        if attr['type'] in AttributeUtils.OutputTypes:
            SocketUtils.AddOutput(self, AttributeUtils.TypeToSocket[attr['type']], attr_name, attr['attr'])


def AddDefaultInputsOutputs(self, vrayPlugin):
    AddDefaultInputs(self, vrayPlugin)
    AddDefaultOutputs(self, vrayPlugin)


def CreateNode(ntree, nodeType, nodeName=None, unique=True):
    nodeLabel = nodeName

    if nodeName is None:
        nodeName = LibUtils.GetUUID()

    if nodeName in ntree.nodes:
        if not unique:
            return ntree.nodes[nodeName]
        else:
            nodeName = LibUtils.GetUUID() + nodeName

    node = ntree.nodes.new(nodeType)
    node.name  = nodeName
    node.label = nodeLabel

    return node


def getInputSocketByVRayAttr(node, attrName):
    for sock in node.inputs:
        if hasattr(sock, 'vray_attr') and sock.vray_attr == attrName:
            return sock

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

from pprint import pprint

import bpy

from vb30.lib import AttributeUtils

from vb30.vray_tools.VRaySceneParser import GetMaterialsNames, ParseVrscene
from vb30.vray_tools.VrmatParser     import GetXMLMaterialsNames
from vb30.nodes.sockets              import AddInput, AddOutput
from vb30.nodes.export               import GetConnectedNode


TYPE = 'MATERIAL'
ID   = 'MtlVRmat'
NAME = "VRmat"
DESC = "VRmat material"

PluginParams = (
    {
        'attr' : 'filename',
        'name' : "Filepath",
        'desc' : "Filepath",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'mtlname',
        'name' : "Name",
        'desc' : "Material name",
        'type' : 'STRING',
        'default' : "",
    },

    {
        'attr' : 'expanded_material',
        'name' : "Material",
        'desc' : "Expanded material",
        'skip' : True,
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'expanded',
        'name' : "Expanded",
        'desc' : "Material is expanded to nodes",
        'type' : 'BOOL',
        'options' : 'HIDDEN',
        'skip' : True,
        'default' : False,
    },
)


class VRayMaterialNameMenu(bpy.types.Menu):
    bl_label = "Select Material Name"
    bl_idname = "VRayMaterialNameMenu"

    ma_list = []

    def draw(self, context):
        row = self.layout.row()
        sub = row.column()

        for i,maName in enumerate(self.ma_list):
            if i and i % 15 == 0:
                sub = row.column()
            sub.operator("vray.set_vrscene_material_name", text=maName).name = maName


class VRaySetMaterialName(bpy.types.Operator):
    bl_idname      = "vray.set_vrscene_material_name"
    bl_label       = "Set Material Name"
    bl_description = "Set material name from *.vrscene file"

    name = bpy.props.StringProperty()

    def execute(self, context):
        node = context.active_node
        if not node:
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        MtlVRmat.mtlname = self.name

        return {'FINISHED'}


class VRayGetMaterialName(bpy.types.Operator):
    bl_idname      = "vray.get_vrscene_material_name"
    bl_label       = "Get Material Name"
    bl_description = "Get material name from *.vrscene file"

    def execute(self, context):
        node = context.active_node
        if not node:
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        if not MtlVRmat.filename:
            return {'CANCELLED'}

        filePath = os.path.normpath(bpy.path.abspath(MtlVRmat.filename))
        if not os.path.exists(filePath):
            return {'CANCELLED'}

        if filePath.endswith(".vrscene"):
            VRayMaterialNameMenu.ma_list = GetMaterialsNames(filePath)
        else:
            VRayMaterialNameMenu.ma_list = GetXMLMaterialsNames(filePath)

        bpy.ops.wm.call_menu(name=VRayMaterialNameMenu.bl_idname)

        return {'FINISHED'}


NODE_LEVEL_WIDTH = 350.0


def getOutputSocket(pluginID):
    from vb30.plugins import PLUGINS_ID

    if pluginID in PLUGINS_ID:
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
    elif pluginID == "BRDFLayered":
        return "BRDF"

    return "Output"


def getPluginByName(vrsceneDict, pluginName):
    for pluginDesc in vrsceneDict:
        if pluginDesc['Name'] == pluginName:
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


def getNodeHeight(n):
    socketHeigth = 25
    return n.height + socketHeigth * (len(n.inputs) + len(n.outputs))


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
        if texPlugName.find("::") != -1:
            texPlugName, texPlugOutput = texPlugName.split("::")
            texPlugOutput = AttributeUtils.GetNameFromAttr(texPlugOutput)

        texPlugin = getPluginByName(vrsceneDict, texPlugName)
        if texPlugin is None:
            print("Plugin '%s' not found in the vrscene file!" % inPluginName)
            continue

        if texPlugOutput is None:
            texPlugOutput = getOutputSocket(texPlugin['ID'])

        texNode = createNode(ntree, texLayeredNode, vrsceneDict, texPlugin)

        ntree.links.new(texNode.outputs[texPlugOutput], texSocket)

    for attrName in pluginDesc['Attributes']:
        # Skip lists
        if attrName in {'textures', 'blend_modes'}:
            continue

        attrValue = pluginDesc['Attributes'][attrName]

        if hasattr(texLayeredNode, attrName):
            setattr(texLayeredNode, attrName, attrValue)

    return texLayeredNode


def createNodeBRDFLayered(ntree, n, vrsceneDict, pluginDesc):
    def processSocket(thisNode, socket, attrValue):
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

            ntree.links.new(inNode.outputs[plOutput], socket)
        else:
            socket.value = attrValue

        return inNode

    brdfs   = pluginDesc['Attributes']['brdfs']
    weights = pluginDesc['Attributes']['weights']

    brdfLayeredNode = ntree.nodes.new('VRayNodeBRDFLayered')

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
        processSocket(brdfLayeredNode, weightSocket, weights[i])

    for attrName in pluginDesc['Attributes']:
        # Skip lists
        if attrName in {'brdfs', 'weights'}:
            continue

        attrValue = pluginDesc['Attributes'][attrName]

        if hasattr(brdfLayeredNode, attrName):
            setattr(brdfLayeredNode, attrName, attrValue)

    return brdfLayeredNode


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

    else:
        pluginModule = PLUGINS_ID.get(pluginID)
        if pluginModule is None:
                print("Plugin '%s' is not yet supported! This shouldn't happen!" % pluginID)
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
            attrDesc  = getParamDesc(pluginModule.PluginParams, attrName)

            attrSocketName = getSocketName(pluginModule.PluginParams, attrName)

            # Attribute is a output type - nothing to do
            if attrDesc['type'] in AttributeUtils.OutputTypes:
                continue

            # Attribute could possibly be mapped with other node
            # Check if we could find requested node in a vrsceneDict
            #
            if attrDesc['type'] in AttributeUtils.InputTypes:
                if type(attrValue) is str:
                    inPluginName   = attrValue
                    inPluginOutput = None

                    # Check if a specific output is requested (like MyTexture::out_intensity)
                    #
                    if inPluginName.find("::") != -1:
                        inPluginName, inPluginOutput = attrValue.split("::")

                    # Set socket value
                    #
                    connectedPlugin = getPluginByName(vrsceneDict, inPluginName)
                    if connectedPlugin is None:
                        attrSocket = n.inputs[attrSocketName]
                        attrSocket.value = attrValue

                    # Create connected plugin
                    #
                    else:
                        connectedPluginID = connectedPlugin['ID']

                        inPluginOutputSocketName = AttributeUtils.GetNameFromAttr(inPluginOutput) if inPluginOutput else getOutputSocket(connectedPluginID)

                        connectedNode = createNode(ntree, n, vrsceneDict, connectedPlugin)
                        if connectedNode:
                            ntree.links.new(connectedNode.outputs[inPluginOutputSocketName], n.inputs[attrSocketName])

                else:
                    attrSocket = n.inputs[attrSocketName]
                    attrSocket.value = attrValue

                continue

            # Attribute is not mappable, so simply set it's value
            if attrDesc['type'] == 'ENUM':
                attrValue = str(attrValue)

            setattr(propGroup, attrName, attrValue)

    return n


def collectLeafs(tree, ntree, n, depth):
    for inSock in n.inputs:
        if inSock.is_linked:
            inNode = GetConnectedNode(ntree, inSock)
            if not depth in tree:
                tree[depth] = []
            tree[depth].append(inNode)
            tree = collectLeafs(tree, ntree, inNode, depth+1)
    return tree


def rearrangeTree(ntree, n, depth=0):
    tree = {
        depth : [n],
    }

    tree = collectLeafs(tree, ntree, n, depth+1)

    # pprint(tree)

    for level in sorted(tree):
        levelNodes = tree[level]
        levelHeigth = 0

        for node in levelNodes:
            levelHeigth += getNodeHeight(node)

        levelTop        = levelHeigth
        levelHeightHalf = levelHeigth / 2.0

        for node in levelNodes:
            node.location.x = n.location.x - (level * NODE_LEVEL_WIDTH)
            node.location.y = levelTop - levelHeightHalf

            levelTop -= getNodeHeight(node)


class VRayMaterialCollapse(bpy.types.Operator):
    bl_idname      = "vray.material_ntree_save"
    bl_label       = "Expand Material"
    bl_description = "Save expanded material to the *.vrscene file"

    def execute(self, context):
        return {'CANCELLED'}


class VRayMaterialExpand(bpy.types.Operator):
    bl_idname      = "vray.material_ntree_load"
    bl_label       = "Expand Material"
    bl_description = "Expand selected material from the *.vrscene file"

    def execute(self, context):
        node = context.node
        if not node:
            print("No active node!")
            return {'CANCELLED'}
        if node.bl_idname != "VRayNodeMtlVRmat":
            print("Selected node is not of type VRayNodeMtlVRmat!")
            return {'CANCELLED'}

        MtlVRmat = node.MtlVRmat
        if not MtlVRmat.filename:
            print("Filepath is not set!")
            return {'CANCELLED'}

        if not MtlVRmat.mtlname:
            print("Material is not chosen!")
            return {'CANCELLED'}

        filePath = os.path.normpath(bpy.path.abspath(MtlVRmat.filename))
        if not os.path.exists(filePath):
            print("File doesn't exist!")
            return {'CANCELLED'}

        if not filePath.endswith(".vrscene"):
            print("File is not a vrscene!")
            return {'CANCELLED'}

        vrsceneDict = ParseVrscene(filePath)

        # Preview data from the file
        #
        # for pluginDesc in vrsceneDict:
        #     pluginID    = pluginDesc['ID']
        #     pluginName  = pluginDesc['Name']
        #     pluginAttrs = pluginDesc['Attributes']
        #
        #     print("Plugin:")
        #     print("  Type: %s" % pluginID)
        #     print("  Name: %s" % pluginName)
        #     print("  Attributes:")
        #     for attrName in pluginAttrs:
        #         print("    %s = %s" % (attrName, pluginAttrs[attrName]))

        # Find requested material plugin
        #
        mtlName     = MtlVRmat.mtlname
        mtlPlugDesc = getPluginByName(vrsceneDict, mtlName)

        if not mtlPlugDesc:
            print("Requested material is not found!")
            return {'CANCELLED'}

        # XXX: The most stupid way to get active node tree!
        # Find out the proper one...
        #
        ntree = context.area.spaces[0].node_tree

        # Now lets start creating nodes
        #
        mtlNode = createNode(ntree, node, vrsceneDict, mtlPlugDesc)

        # Connect material output to our node
        #
        ntree.links.new(mtlNode.outputs['Material'], node.inputs['Material'])

        rearrangeTree(ntree, node)

        return {'FINISHED'}


def nodeDraw(context, layout, MtlVRmat):
    split = layout.split(percentage=0.2, align=True)
    split.column().label("File:")
    split.column().prop(MtlVRmat, 'filename', text="")

    split = layout.split(percentage=0.2, align=True)
    split.column().label("Name:")
    row = split.column().row(align=True)
    row.prop(MtlVRmat, 'mtlname', text="")
    row.operator("vray.get_vrscene_material_name", text="", icon='IMASEL')

    layout.separator()
    split = layout.split()
    row = split.row(align=True)
    row.operator("vray.material_ntree_load", text="Load", icon='FILE_FOLDER')
    row.operator("vray.material_ntree_save", text="Save", icon='FILE_TICK')


def GetRegClasses():
    return (
        VRayMaterialCollapse,
        VRayMaterialExpand,
        VRayMaterialNameMenu,
        VRayGetMaterialName,
        VRaySetMaterialName,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

from pprint import pprint

import bpy
import mathutils

from vb25.plugins import PLUGINS
from vb25.utils   import *


##     ## ######## #### ##       #### ######## #### ########  ######  
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##       
##     ##    ##     ##  ##        ##     ##     ##  ######    ######  
##     ##    ##     ##  ##        ##     ##     ##  ##             ## 
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ## 
 #######     ##    #### ######## ####    ##    #### ########  ######  

def GetConnectedNode(nodeTree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_node:
            return l.from_node
    return None


def GetNodeByType(nodetree, nodeType):
    for n in nodetree.nodes:
        if n.bl_idname == nodeType:
            return n
    return None


def GetOutputNode(nodetree):
    return GetNodeByType(nodetree, 'VRayNodeOutput')


 ######   #######   #######  ########  ########   ######  
##    ## ##     ## ##     ## ##     ## ##     ## ##    ## 
##       ##     ## ##     ## ##     ## ##     ## ##       
##       ##     ## ##     ## ########  ##     ##  ######  
##       ##     ## ##     ## ##   ##   ##     ##       ## 
##    ## ##     ## ##     ## ##    ##  ##     ## ##    ## 
 ######   #######   #######  ##     ## ########   ######  

def WriteUVWGenMayaPlace2dTexture(bus, nodetree, node):
    ofile = bus['files']['textures']
    scene = bus['scene']

    pluginName = clean_string("nt%sns%s" % (nodetree.name, node.name))

    ofile.write("\nUVWGenMayaPlace2dTexture %s {" % pluginName)
    if node.uv_layer:
        ofile.write('\n\tuv_set_name="%s";' % clean_string(node.uv_layer))
    else:
        ofile.write('\n\tuvw_channel=0;')
    ofile.write("\n\tmirror_u=%d;" % node.mirror_u)
    ofile.write("\n\tmirror_v=%d;" % node.mirror_v)
    ofile.write("\n\trepeat_u=%d;" % node.repeat_u)
    ofile.write("\n\trepeat_v=%d;" % node.repeat_v)
    ofile.write("\n\trotate_frame=%.3f;" % node.rotate_frame)
    ofile.write("\n}\n")

    return pluginName


##          ###    ##    ## ######## ########  ######## ########  
##         ## ##    ##  ##  ##       ##     ## ##       ##     ## 
##        ##   ##    ####   ##       ##     ## ##       ##     ## 
##       ##     ##    ##    ######   ########  ######   ##     ## 
##       #########    ##    ##       ##   ##   ##       ##     ## 
##       ##     ##    ##    ##       ##    ##  ##       ##     ## 
######## ##     ##    ##    ######## ##     ## ######## ########       

def WriteVRayNodeBRDFLayered(bus, nodetree, node):
    ofile = bus['files']['materials']
    scene = bus['scene']

    pluginName = clean_string("nt%sn%s" % (nodetree.name, node.name))

    brdfs   = []
    weights = []
    for i in range(int(len(node.inputs) / 2)):
        layer = i+1
        brdfSocket   = "BRDF %i"   % layer
        weightSocket = "Weight %i" % layer

        if not node.inputs[brdfSocket].is_linked:
            continue

        brdfNode = GetConnectedNode(nodetree, node.inputs[brdfSocket])
        brdfs.append(WriteNode(bus, nodetree, brdfNode))

        if node.inputs[weightSocket].is_linked:
            weigthNode = GetConnectedNode(nodetree, node.inputs[weightSocket])
            weights.append(WriteNode(bus, nodetree, weigthNode))
        else:
            weightParam = "%sW%sI%i"%(pluginName, brdfs[i], i)
            ofile.write("\nTexAColor %s {" % (weightParam))
            ofile.write("\n\ttexture=%s;" % (a(scene, [node.inputs[weightSocket].value]*4)))
            ofile.write("\n}\n")
            weights.append(weightParam)

    ofile.write("\nBRDFLayered %s {" % pluginName)
    ofile.write("\n\tbrdfs=List(%s);" % ','.join(brdfs))
    ofile.write("\n\tweights=List(%s);" % ','.join(weights))
    ofile.write("\n\tadditive_mode=%s;" % p(node.additive_mode))
    ofile.write("\n}\n")

    return pluginName


######## ##     ## ########   #######  ########  ######## 
##        ##   ##  ##     ## ##     ## ##     ##    ##    
##         ## ##   ##     ## ##     ## ##     ##    ##    
######      ###    ########  ##     ## ########     ##    
##         ## ##   ##        ##     ## ##   ##      ##    
##        ##   ##  ##        ##     ## ##    ##     ##    
######## ##     ## ##         #######  ##     ##    ##    

def WriteConnectedNode(bus, nodetree, nodeSocket):
    print("Processing socket: %s [%s]" % (nodeSocket.name, nodeSocket.vray_attr))

    if nodeSocket.is_linked:
        connectedNode = GetConnectedNode(nodetree, nodeSocket)
        if connectedNode:
            return WriteNode(bus, nodetree, connectedNode)

    return nodeSocket.value


def WriteNode(bus, nodetree, node):
    print("Processing node: %s..." % node.name)

    # Write some nodes in a special way
    if node.bl_idname == 'VRayNodeBRDFLayered':
        return WriteVRayNodeBRDFLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeUVChannel':
        return WriteUVWGenMayaPlace2dTexture(bus, nodetree, node)

    pluginName = clean_string("NT%sN%s" % (nodetree.name, node.name))

    vrayType   = node.vray_type
    vrayPlugin = node.vray_plugin

    print("Generating plugin \"%s\" [%s, %s]" % (pluginName, vrayType, vrayPlugin))

    dataPointer = getattr(node, vrayPlugin)

    socketParams = {}

    for nodeSocket in node.inputs:
        vrayAttr = nodeSocket.vray_attr

        socketParams[vrayAttr] = WriteConnectedNode(bus, nodetree, nodeSocket)

    return PLUGINS[vrayType][vrayPlugin].writeDatablock(bus, dataPointer, pluginName, socketParams)


def WriteVRayMaterialNodeTree(bus, nodetree):
    outputNode = GetOutputNode(nodetree)
    if not outputNode:
        return bus['defaults']['material']

    materialSocket = outputNode.inputs['Material']
    if not materialSocket.is_linked:
        return bus['defaults']['material']

    return WriteConnectedNode(bus, nodetree, materialSocket)


def ExportVRayNodes(bus, datablock):
    if not datablock.vray.nodetree:
        return None

    if not datablock.vray.nodetree in bpy.data.node_groups:
        return None

    nodetree = bpy.data.node_groups[datablock.vray.nodetree]

    if type(datablock) == bpy.types.Material:
        return WriteVRayMaterialNodeTree(bus, nodetree)

    return None


def ExportNodeMaterial(bus):
    ma = bus['material']['material']

    if not ma.vray.nodetree:
        return bus['defaults']['material']
    
    return ExportVRayNodes(bus, ma)

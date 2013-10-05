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

import bpy
import mathutils
 
from vb25.lib     import ExportUtils
from vb25.plugins import PLUGINS
from vb25.debug   import Debug
from vb25.utils   import clean_string


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


def GetConnectedSocket(nodeTree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_socket:
            return l.from_socket
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

    uvwgen = None
    uvwgenSocket = node.inputs['Mapping']
    if uvwgenSocket.is_linked:
        uvwgenNode = GetConnectedNode(nodetree, uvwgenSocket)
        uvwgen     = WriteNode(bus, nodetree, uvwgenNode)

    pluginName = clean_string("nt%sns%s" % (nodetree.name, node.name))

    ofile.write("\nUVWGenMayaPlace2dTexture %s {" % pluginName)
    if node.uv_layer:
        ofile.write('\n\tuv_set_name="%s";' % clean_string(node.uv_layer))
    ofile.write("\n\tmirror_u=%d;" % node.mirror_u)
    ofile.write("\n\tmirror_v=%d;" % node.mirror_v)
    ofile.write("\n\trepeat_u=%d;" % node.repeat_u)
    ofile.write("\n\trepeat_v=%d;" % node.repeat_v)
    ofile.write("\n\trotate_frame=%.3f;" % node.rotate_frame)
    if uvwgen is not None:
        ofile.write("\n\tuvwgen=%s;" % uvwgen)
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
    Debug("Processing socket: %s [%s]" % (nodeSocket.name, nodeSocket.vray_attr))

    if nodeSocket.is_linked:
        connectedNode   = GetConnectedNode(nodetree, nodeSocket)
        connectedSocket = GetConnectedSocket(nodetree, nodeSocket)
        if connectedNode:
            vrayPlugin = WriteNode(bus, nodetree, connectedNode)

            if connectedSocket.vray_attr:
                # XXX: use as a workaround
                # TODO: get plugin desc and check if the attr is output,
                # but skip uvwgen anyway.
                #
                if connectedSocket.vray_attr not in ['uvwgen']:
                    vrayPlugin = "%s::%s" % (vrayPlugin, connectedSocket.vray_attr)
            
            return vrayPlugin

    return nodeSocket.value


def WriteNode(bus, nodetree, node):
    Debug("Processing node: %s..." % node.name)

    # Write some nodes in a special way
    if node.bl_idname == 'VRayNodeBRDFLayered':
        return WriteVRayNodeBRDFLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeUVChannel':
        return WriteUVWGenMayaPlace2dTexture(bus, nodetree, node)

    pluginName = clean_string("NT%sN%s" % (nodetree.name, node.name))

    if 'cache' in bus:
        if pluginName in bus['cache']['nodes']:
            return pluginName

        bus['cache']['nodes'].append(pluginName)

    vrayType   = node.vray_type
    vrayPlugin = node.vray_plugin

    Debug("Generating plugin \"%s\" [%s, %s]" % (pluginName, vrayType, vrayPlugin), msgType='INFO')

    dataPointer = getattr(node, vrayPlugin)

    socketParams = {}

    for nodeSocket in node.inputs:
        vrayAttr = nodeSocket.vray_attr

        socketParams[vrayAttr] = WriteConnectedNode(bus, nodetree, nodeSocket)

    result     = None
    pluginDesc = PLUGINS[vrayType][vrayPlugin]

    if hasattr(pluginDesc, 'writeDatablock'):
        result = pluginDesc.writeDatablock(bus, dataPointer, pluginName, socketParams)
    else:
        result = ExportUtils.WriteDatablock(bus, vrayPlugin, pluginName, PLUGINS[vrayType][vrayPlugin].PluginParams, dataPointer, socketParams)

    return result


def WriteVRayMaterialNodeTree(bus, nodetree):
    outputNode = GetNodeByType(nodetree, 'VRayNodeOutput')
    if not outputNode:
        Debug("Output node not found!", msgType='ERROR')
        return None

    materialSocket = outputNode.inputs['Material']
    if not materialSocket.is_linked:
        Debug("NodeTree: %s" % nodetree.name, msgType='ERROR')
        Debug("  Node: %s" % outputNode.name, msgType='ERROR')
        Debug("  Error: Material socket is not connected!", msgType='ERROR')
        return None

    return WriteConnectedNode(bus, nodetree, materialSocket)


def ExportNodeMaterial(bus):
    ma = bus['material']['material']
 
    if not ma.vray.ntree:
        Debug("Node tree is no set for material \"%s\"!" % ma.name, msgType='ERROR')
        return bus['defaults']['material']

    pluginName = WriteVRayMaterialNodeTree(bus, ma.vray.ntree)
    if pluginName is None:
        return bus['defaults']['material']
    
    return pluginName

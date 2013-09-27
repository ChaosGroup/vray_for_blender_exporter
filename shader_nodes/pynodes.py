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
    for node in nodeTree.links:
        if node.to_socket == nodeSocket:
            return node.from_node
    return None


def GetNodeByType(nodetree, nodeType):
    for n in nodetree.nodes:
        if n.bl_idname == nodeType:
            return n
    return None


def GetOutputNode(nodetree):
    return GetNodeByType(nodetree, 'VRayNodeOutput')


##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ## ##     ## 
##     ##  ##   ##  
##     ##   ## ##   
 #######     ###    

def WriteUVWGenMayaPlace2dTexture(bus, nodetree, node):
    ofile = bus['files']['textures']
    scene = bus['scene']

    pluginName = clean_string("nt%sns%s" % (nodetree.name, node.name))

    ofile.write("\nUVWGenMayaPlace2dTexture %s {" % pluginName)
    if node.uv_layer:
        ofile.write('\n\tuv_set_name="%s";' % clean_string(node.uv_layer))
    else:
        ofile.write('\n\tuvw_channel=0;')
    # ofile.write("\n\tmirror_u=%d;" % VRayTexture.mirror_u)
    # ofile.write("\n\tmirror_v=%d;" % VRayTexture.mirror_v)
    # ofile.write("\n\trepeat_u=%d;" % VRayTexture.tile_u)
    # ofile.write("\n\trepeat_v=%d;" % VRayTexture.tile_v)
    # ofile.write("\n\trotate_frame=%.3f;" % VRaySlot.texture_rot)
    ofile.write("\n}\n")

    return pluginName


######## ######## ##     ## ######## ##     ## ########  ######## 
   ##    ##        ##   ##     ##    ##     ## ##     ## ##       
   ##    ##         ## ##      ##    ##     ## ##     ## ##       
   ##    ######      ###       ##    ##     ## ########  ######   
   ##    ##         ## ##      ##    ##     ## ##   ##   ##       
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##       
   ##    ######## ##     ##    ##     #######  ##     ## ######## 
   
def WriteNodeTexture(bus, nodetree, node):
    ofile = bus['files']['textures']
    
    ofile.write("\n// Tree: \"%s\"" % (nodetree.name))
    ofile.write("\n// Node: \"%s\"" % (node.name))
    ofile.write("\n// Type:  %s"    % (node.bl_idname))
    ofile.write("\n//")

    pluginName = clean_string("nt%sn%s" % (nodetree.name, node.name))

    uvSocket = node.inputs['UV']

    if uvSocket.is_linked:
        uvNode = GetConnectedNode(nodetree, uvSocket)

        bus['uvwgen'] = WriteUVWGenMayaPlace2dTexture(bus, nodetree, uvNode)

    mappedParams = {}

    return PLUGINS['TEXTURE'][node.textureType].writeDatablock(bus, getattr(node, node.textureType), pluginName, mappedParams)


########  ########  ########  ######## 
##     ## ##     ## ##     ## ##       
##     ## ##     ## ##     ## ##       
########  ########  ##     ## ######   
##     ## ##   ##   ##     ## ##       
##     ## ##    ##  ##     ## ##       
########  ##     ## ########  ##       

def WriteBRDFDiffuseColor(bus, nodetree, nodeSocket):
    ofile = bus['files']['materials']
    scene = bus['scene']

    pluginName = clean_string("nt%sns%s" % (nodetree.name, nodeSocket.name))

    ofile.write("\nBRDFDiffuse %s {" % (pluginName))
    ofile.write("\n\tcolor=%s;" % (a(scene, nodeSocket.default_value)))
    ofile.write("\n}")

    return pluginName


def WriteVRayNodeBRDFVRayMtl(bus, nodetree, node):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ofile.write("\n// Tree: \"%s\"" % (nodetree.name))
    ofile.write("\n// Node: \"%s\"" % (node.name))
    ofile.write("\n// Type:  %s"    % (node.bl_idname))
    ofile.write("\n//")

    texturedSockets = {
        'diffuse' : {
            'socket' : node.inputs['Diffuse'],
            'value'  : None
        },
    }

    for key in texturedSockets:
        texturedSocket = texturedSockets[key]

        texSocket = texturedSocket['socket']       
        texNode   = GetConnectedNode(nodetree, texSocket)
        
        if not texNode:
            texturedSocket['value'] = texSocket.default_value
        else:
            texturedSocket['value'] = WriteShaderNode(bus, nodetree, texNode)

    bus['textures'] = {}
    for key in texturedSockets:
        bus['textures'][key] = texturedSockets[key]['value']

    return PLUGINS['BRDF']['BRDFVRayMtl'].write(bus, VRayBRDF=node)


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
        brdfs.append(WriteShaderNode(bus, nodetree, brdfNode))

        if node.inputs[weightSocket].is_linked:
            weigthNode = GetConnectedNode(nodetree, node.inputs[weightSocket])
            weights.append(WriteShaderNode(bus, nodetree, weigthNode))
        else:
            weightParam = "%sW%sI%i"%(pluginName, brdfs[i], i)
            ofile.write("\nTexAColor %s {" % (weightParam))
            ofile.write("\n\ttexture=%s;" % (a(scene, [node.inputs[weightSocket].default_value]*4)))
            ofile.write("\n}\n")
            weights.append(weightParam)

    ofile.write("\nBRDFLayered %s {" % pluginName)
    ofile.write("\n\tbrdfs=List(%s);" % ','.join(brdfs))
    ofile.write("\n\tweights=List(%s);" % ','.join(weights))
    ofile.write("\n\tadditive_mode=%s;" % p(node.additive_mode))
    ofile.write("\n}\n")

    return pluginName


##     ##    ###    ######## ######## ########  ####    ###    ##       
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##       
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##       
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##       
##     ## #########    ##    ##       ##   ##    ##  ######### ##       
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##       
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ######## 

def WriteShaderNode(bus, nodetree, node):
    if node.bl_idname == 'VRayNodeBRDFVRayMtl':
        return WriteVRayNodeBRDFVRayMtl(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeBRDFLayered':
        return WriteVRayNodeBRDFLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeTexture':
        return WriteNodeTexture(bus, nodetree, node)
    return "BRDFNOBRDFISSET"


def WriteVRayMaterialNodeTree(bus, nodetree):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ob   = bus['node']['object']
    base = bus['node']['base']

    ma = bus['material']['material']

    outputNode = GetOutputNode(nodetree)
    if not outputNode:
        return bus['defaults']['material']

    colorSocket = outputNode.inputs['Color']
    colorNode   = GetConnectedNode(nodetree, colorSocket)

    if colorNode:
        brdf = WriteShaderNode(bus, nodetree, colorNode)

        pluginName = get_name(ma, prefix='MA')

        ofile.write("\nMtlSingleBRDF %s {" % (pluginName))
        ofile.write("\n\tbrdf=%s;" % brdf)
        ofile.write("\n\tallow_negative_colors=1;")
        ofile.write("\n}\n")

        return pluginName

    return WriteBRDFDiffuseColor(bus, nodetree, colorSocket)


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

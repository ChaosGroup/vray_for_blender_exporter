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

import _vray_for_blender

from vb25.lib     import ExportUtils
from vb25.lib     import utils as LibUtils
from vb25.plugins import PLUGINS
from vb25.debug   import Debug, PrintDict
from vb25.utils   import clean_string


##     ## ######## #### ##       #### ######## #### ########  ######
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##
##     ##    ##     ##  ##        ##     ##     ##  ######    ######
##     ##    ##     ##  ##        ##     ##     ##  ##             ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
 #######     ##    #### ######## ####    ##    #### ########  ######

def GetNodeName(ntree, node):
    return clean_string("NT%sN%s" % (ntree.name, node.name))


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


def GetNodeByType(ntree, nodeType):
    for n in ntree.nodes:
        if n.bl_idname == nodeType:
            return n
    return None


def GetOutputNode(ntree):
    return GetNodeByType(ntree, 'VRayNodeOutputMaterial')


def GetOutputName(ntree):
    outputNode = GetNodeByType(ntree, 'VRayNodeOutputMaterial')
    if not outputNode:
        return bus['defaults']['material']

    materialSocket = outputNode.inputs['Material']
    if not materialSocket.is_linked:
        return bus['defaults']['material']

    connectedNode = GetConnectedNode(ntree, materialSocket)
    if not connectedNode:
        return bus['defaults']['material']

    return GetNodeName(ntree, connectedNode)


 ######  ######## ##       ########  ######  ########  #######  ########   ######  
##    ## ##       ##       ##       ##    ##    ##    ##     ## ##     ## ##    ## 
##       ##       ##       ##       ##          ##    ##     ## ##     ## ##       
 ######  ######   ##       ######   ##          ##    ##     ## ########   ######  
      ## ##       ##       ##       ##          ##    ##     ## ##   ##         ## 
##    ## ##       ##       ##       ##    ##    ##    ##     ## ##    ##  ##    ## 
 ######  ######## ######## ########  ######     ##     #######  ##     ##  ######  

def WriteVRayNodeSelectObject(bus, nodetree, node):
    scene = bus['scene']
    if not node.objectName:
        return []
    if node.objectName not in scene.objects:
        return []
    return [scene.objects[node.objectName]]


def WriteVRayNodeSelectGroup(bus, nodetree, node):
    if not node.groupName:
        return []
    if node.groupName not in bpy.data.groups:
        return []
    return bpy.data.groups[node.groupName].objects


########  ##       ######## ##    ## ########  ######## ########      #######  ########        ## ########  ######  ######## 
##     ## ##       ##       ###   ## ##     ## ##       ##     ##    ##     ## ##     ##       ## ##       ##    ##    ##    
##     ## ##       ##       ####  ## ##     ## ##       ##     ##    ##     ## ##     ##       ## ##       ##          ##    
########  ##       ######   ## ## ## ##     ## ######   ########     ##     ## ########        ## ######   ##          ##    
##     ## ##       ##       ##  #### ##     ## ##       ##   ##      ##     ## ##     ## ##    ## ##       ##          ##    
##     ## ##       ##       ##   ### ##     ## ##       ##    ##     ##     ## ##     ## ##    ## ##       ##    ##    ##    
########  ######## ######## ##    ## ########  ######## ##     ##     #######  ########   ######  ########  ######     ##    

def WriteVRayNodeBlenderOutputGeometry(bus, nodetree, node):
    scene = bus['scene']
    ob    = bus['node']['object']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.exporter

    # XXX: Resolve manual meshes export
    #
    if not VRayExporter.auto_meshes:
        return bus['node']['geometry']

    if bus['node']['geometry'] not in bus['cache']['mesh']:
        bus['cache']['mesh'].add(bus['node']['geometry'])

        _vray_for_blender.exportMesh(
            bpy.context.as_pointer(), # Context
            ob.as_pointer(),          # Object
            bus['node']['geometry'],  # Result plugin name
            bus['files']['geom']      # Output file
        )

    return bus['node']['geometry']


def WriteVRayNodeBlenderOutputMaterial(bus, nodetree, node):
    ofile = bus['files']['materials']
    scene = bus['scene']
    ob    = bus['node']['object']

    if not len(ob.material_slots):
        bus['node']['material'] = bus['defaults']['material']
        return bus['node']['material']

    VRayScene = scene.vray

    VRayExporter    = VRayScene.exporter
    SettingsOptions = VRayScene.SettingsOptions

    # Multi-material name
    mtl_name = LibUtils.GetObjectName(ob, prefix='OBMA')

    # Collecting and exporting object materials
    mtls_list = []
    ids_list  = []
    ma_id     = 0

    for slot in ob.material_slots:
        if not slot.material:
            continue

        ma = slot.material

        if not ma.vray.dontOverride and SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
            ma = get_data_by_name(scene, 'materials', SettingsOptions.mtl_override)

        if not ma.vray.ntree:
            continue

        nodeMaterial = WriteVRayMaterialNodeTree(bus, ma.vray.ntree)

        ma_id += 1
        mtls_list.append(nodeMaterial)
        ids_list.append(str(ma_id))

    # No materials assigned - use default material
    if len(mtls_list) == 0:
        bus['node']['material'] = bus['defaults']['material']

    # Only one material - no need for Multi-material
    elif len(mtls_list) == 1:
        bus['node']['material'] = mtls_list[0]

    # Several materials assigned - use Mutli-material
    else:
        bus['node']['material'] = mtl_name

        ofile.write("\nMtlMulti %s {" % mtl_name)
        ofile.write("\n\tmtls_list=List(%s);" % ','.join(mtls_list))
        ofile.write("\n\tids_list=ListInt(%s);" % ','.join(ids_list))
        ofile.write("\n}\n")

    return bus['node']['material']


##          ###    ##    ## ######## ########  ######## ########
##         ## ##    ##  ##  ##       ##     ## ##       ##     ##
##        ##   ##    ####   ##       ##     ## ##       ##     ##
##       ##     ##    ##    ######   ########  ######   ##     ##
##       #########    ##    ##       ##   ##   ##       ##     ##
##       ##     ##    ##    ##       ##    ##  ##       ##     ##
######## ##     ##    ##    ######## ##     ## ######## ########

def WriteVRayNodeTexLayered(bus, nodetree, node):
    ofile = bus['files']['nodetree']
    scene = bus['scene']

    pluginName = clean_string("nt%sn%s" % (nodetree.name, node.name))

    textures    = []
    blend_modes = []
    
    for inputSocket in node.inputs:
        if not inputSocket.is_linked:
            continue

        texNode = GetConnectedNode(nodetree, inputSocket)
        if not texNode:
            continue

        textures.append(WriteNode(bus, nodetree, texNode))
        blend_modes.append(inputSocket.value)

    ofile.write("\nTexLayered %s {" % pluginName)
    ofile.write("\n\ttextures=List(%s);" % ','.join(reversed(textures)))
    ofile.write("\n\tblend_modes=List(%s);" % ','.join(reversed(blend_modes)))
    ofile.write("\n}\n")

    return pluginName


def WriteVRayNodeBRDFLayered(bus, nodetree, node):
    ofile = bus['files']['nodetree']
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
            
            weightColor = mathutils.Color([node.inputs[weightSocket].value]*3)

            ofile.write("\nTexAColor %s {" % (weightParam))
            ofile.write("\n\ttexture=%s;" % LibUtils.AnimatedValue(scene, weightColor))
            ofile.write("\n}\n")
            
            weights.append(weightParam)

    ofile.write("\nBRDFLayered %s {" % pluginName)
    ofile.write("\n\tbrdfs=List(%s);" % ','.join(brdfs))
    ofile.write("\n\tweights=List(%s);" % ','.join(weights))
    ofile.write("\n\tadditive_mode=%s;" % LibUtils.FormatValue(node.additive_mode))
    ofile.write("\n}\n")

    return pluginName


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##

def WriteConnectedNode(bus, nodetree, nodeSocket, returnDefault=True):
    Debug("Processing socket: %s [%s]" % (nodeSocket.name, nodeSocket.vray_attr))

    if not nodeSocket.is_linked:
        if returnDefault:
            return nodeSocket.value
        else:
            return None
    
    connectedNode   = GetConnectedNode(nodetree, nodeSocket)
    connectedSocket = GetConnectedSocket(nodetree, nodeSocket)
    if connectedNode:
        vrayPlugin = WriteNode(bus, nodetree, connectedNode, returnDefault=returnDefault)

        if connectedSocket.vray_attr:
            # XXX: use as a workaround
            # TODO: get plugin desc and check if the attr is output,
            # but skip uvwgen anyway.
            #
            if connectedSocket.vray_attr not in {'uvwgen'}:
                vrayPlugin = "%s::%s" % (vrayPlugin, connectedSocket.vray_attr)

        return vrayPlugin
    
    return None


def WriteNode(bus, nodetree, node, returnDefault=False):
    Debug("Processing node: %s..." % node.name)

    # Write some nodes in a special way
    if node.bl_idname == 'VRayNodeBRDFLayered':
        return WriteVRayNodeBRDFLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeTexLayered':
        return WriteVRayNodeTexLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeSelectObject':
        return WriteVRayNodeSelectObject(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeSelectGroup':
        return WriteVRayNodeSelectGroup(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeBlenderOutputGeometry':
        return WriteVRayNodeBlenderOutputGeometry(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeBlenderOutputMaterial':
        return WriteVRayNodeBlenderOutputMaterial(bus, nodetree, node)

    vrayType   = node.vray_type
    vrayPlugin = node.vray_plugin

    if vrayType == 'NONE' or vrayPlugin == 'NONE':
        return None

    pluginName = clean_string("NT%sN%s" % (nodetree.name, node.name))

    if pluginName in bus['cache']['plugins']:
        return pluginName
    bus['cache']['plugins'].add(pluginName)

    Debug("Generating plugin \"%s\" [%s, %s]" % (pluginName, vrayType, vrayPlugin), msgType='INFO')

    dataPointer = getattr(node, vrayPlugin)

    socketParams = {}

    for nodeSocket in node.inputs:
        vrayAttr = nodeSocket.vray_attr

        socketParams[vrayAttr] = WriteConnectedNode(bus, nodetree, nodeSocket, returnDefault=returnDefault)

    result     = None
    pluginDesc = PLUGINS[vrayType][vrayPlugin]

    # XXX: Used to access 'image' pointer for BitmapBuffer
    # and 'texture' for TexGradRamp
    #
    bus['context']['node'] = node

    if hasattr(pluginDesc, 'writeDatablock'):
        result = pluginDesc.writeDatablock(bus, pluginName, PLUGINS[vrayType][vrayPlugin].PluginParams, dataPointer, socketParams)
    else:
        result = ExportUtils.WriteDatablock(bus, vrayPlugin, pluginName, PLUGINS[vrayType][vrayPlugin].PluginParams, dataPointer, socketParams)

    return result


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

def WriteVRayMaterialNodeTree(bus, nodetree):
    outputNode = GetNodeByType(nodetree, 'VRayNodeOutputMaterial')
    if not outputNode:
        Debug("Output node not found!", msgType='ERROR')
        return bus['defaults']['material']

    materialSocket = outputNode.inputs['Material']
    if not materialSocket.is_linked:
        Debug("NodeTree: %s" % nodetree.name, msgType='ERROR')
        Debug("  Node: %s" % outputNode.name, msgType='ERROR')
        Debug("  Error: Material socket is not connected!", msgType='ERROR')
        return bus['defaults']['material']

    return WriteConnectedNode(bus, nodetree, materialSocket)

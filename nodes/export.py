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
import mathutils

import _vray_for_blender

from vb30.lib     import ExportUtils, LibUtils
from vb30.plugins import PLUGINS
from vb30         import debug

from .utils import *


##     ## ######## #### ##       #### ######## #### ########  ######
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##
##     ##    ##     ##  ##        ##     ##     ##  ######    ######
##     ##    ##     ##  ##        ##     ##     ##  ##             ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
 #######     ##    #### ######## ####    ##    #### ########  ######

def GetOutputNode(ntree):
    NtreeToOutputNodeType = {
        'VRayNodeTreeScene'    : 'VRayNodeRenderChannels',
        'VRayNodeTreeWorld'    : 'VRayNodeEnvironment',
        'VRayNodeTreeMaterial' : 'VRayNodeOutputMaterial',
        'VRayNodeTreeObject'   : 'VRayNodeObjectOutput',
        'VRayNodeTreeLight'    : 'VRayNodeTreeLight',
    }

    outputNodeType = NtreeToOutputNodeType.get(ntree.bl_idname)
    if not outputNodeType:
        return None

    return GetNodeByType(ntree, outputNodeType)


 ######  ######## ##       ########  ######  ########  #######  ########   ######
##    ## ##       ##       ##       ##    ##    ##    ##     ## ##     ## ##    ##
##       ##       ##       ##       ##          ##    ##     ## ##     ## ##
 ######  ######   ##       ######   ##          ##    ##     ## ########   ######
      ## ##       ##       ##       ##          ##    ##     ## ##   ##         ##
##    ## ##       ##       ##       ##    ##    ##    ##     ## ##    ##  ##    ##
 ######  ######## ######## ########  ######     ##     #######  ##     ##  ######

def WriteVRayNodeSelectObject(bus, nodetree, node):
    if not node.objectName:
        return []
    scene = bpy.context.scene
    if node.objectName not in scene.objects:
        return []
    return [scene.objects[node.objectName]]


def WriteVRayNodeSelectGroup(bus, nodetree, node):
    if not node.groupName:
        return []
    if node.groupName not in bpy.data.groups:
        return []
    return bpy.data.groups[node.groupName].objects


def WriteVRayNodeSelectNodeTree(bus, nodetree, node):
    if not node.ntree:
        return None

    # XXX: Finish this...

    return node.ntree.name


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
    o     = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    meshName = bus['node']['geometry']

    if not VRayExporter.auto_meshes:
        return meshName

    if meshName not in bus['cache']['mesh']:
        bus['cache']['mesh'].add(meshName)

        propGroup = node.GeomStaticMesh if node else ob.data.vray.GeomStaticMesh
        dynamic_geometry = propGroup.dynamic_geometry

        if bus['engine'] == 'VRAY_RENDER_RT' and VRayScene.RTEngine.use_opencl == '4':
            setattr(propGroup, 'dynamic_geometry', True)

        try:
            _vray_for_blender.exportMesh(
                bpy.context.as_pointer(),   # Context
                ob.as_pointer(),            # Object
                meshName,                   # Result plugin name
                propGroup,                  # PropertyGroup
                o.fileManager.getFileByPluginType('GEOMETRY') # Output file
            )
        except Exception as e:
            debug.ExceptionInfo(e)
            debug.Debug("Error exporting geometry for object '%s'" % ob.name, msgType='ERROR')
        finally:
            meshName = None

        if bus['engine'] == 'VRAY_RENDER_RT' and VRayScene.RTEngine.use_opencl == '4':
            setattr(propGroup, 'dynamic_geometry', dynamic_geometry)

    return meshName


def WriteVRayNodeBlenderOutputMaterial(bus, nodetree, node):
    scene = bus['scene']
    ob    = bus['node']['object']
    o     = bus['output']

    if not len(ob.material_slots):
        bus['node']['material'] = bus['defaults']['material']
        return bus['node']['material']

    VRayScene = scene.vray

    VRayExporter    = VRayScene.Exporter
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

        o.set('MATERIAL', 'MtlMulti', mtl_name)
        o.writeHeader()
        o.writeAttibute('mtls_list', "List(%s)" % ','.join(mtls_list))
        o.writeAttibute('ids_list', "ListInt(%s)" % ','.join(ids_list))
        if node:
            id_generator = WriteConnectedNode(bus, nodetree, node.inputs["ID Generator"])
            o.writeAttibute('wrap_id', node.wrap_id)
            o.writeAttibute('mtlid_gen_float', id_generator)
        o.writeFooter()

    return bus['node']['material']


##          ###    ##    ## ######## ########  ######## ########
##         ## ##    ##  ##  ##       ##     ## ##       ##     ##
##        ##   ##    ####   ##       ##     ## ##       ##     ##
##       ##     ##    ##    ######   ########  ######   ##     ##
##       #########    ##    ##       ##   ##   ##       ##     ##
##       ##     ##    ##    ##       ##    ##  ##       ##     ##
######## ##     ##    ##    ######## ##     ## ######## ########

def WriteVRayNodeTexLayered(bus, nodetree, node):
    scene = bus['scene']
    o     = bus['output']

    pluginName = LibUtils.CleanString("nt%sn%s" % (nodetree.name, node.name))

    textures    = []
    blend_modes = []

    for inputSocket in node.inputs:
        if not inputSocket.is_linked:
            continue

        tex = WriteConnectedNode(bus, nodetree, inputSocket)

        # XXX: For some reason TexLayered doesn't like ::out_smth
        semiPos = tex.find("::")
        if semiPos != -1:
            tex = tex[:semiPos]

        textures.append(tex)
        blend_modes.append(inputSocket.value)

    alpha        = WriteConnectedNode(bus, nodetree, node.inputs['Alpha'])
    alpha_mult   = WriteConnectedNode(bus, nodetree, node.inputs['Alpha Mult'])
    alpha_offset = WriteConnectedNode(bus, nodetree, node.inputs['Alpha Offset'])
    nouvw_color  = WriteConnectedNode(bus, nodetree, node.inputs['No UV Color'])
    color_mult   = WriteConnectedNode(bus, nodetree, node.inputs['Color Mult'])
    color_offset = WriteConnectedNode(bus, nodetree, node.inputs['Color Offset'])

    o.set('TEXTURE', 'TexLayered', pluginName)
    o.writeHeader()
    o.writeAttibute('textures', "List(%s)" % ','.join(reversed(textures)))
    o.writeAttibute('blend_modes', "ListInt(%s)" % ','.join(reversed(blend_modes)))
    o.writeAttibute('alpha_from_intensity', node.alpha_from_intensity)
    o.writeAttibute('invert', node.invert)
    o.writeAttibute('invert_alpha', node.invert_alpha)
    o.writeAttibute('alpha', alpha)
    o.writeAttibute('alpha_mult', alpha_mult)
    o.writeAttibute('alpha_offset', alpha_offset)
    o.writeAttibute('nouvw_color', nouvw_color)
    o.writeAttibute('color_mult', color_mult)
    o.writeAttibute('color_offset', color_offset)
    o.writeFooter()

    return pluginName


def WriteVRayNodeBRDFLayered(bus, nodetree, node):
    scene = bus['scene']
    o     = bus['output']

    pluginName = LibUtils.CleanString("nt%sn%s" % (nodetree.name, node.name))

    brdfs   = []
    weights = []

    transparency = WriteConnectedNode(bus, nodetree, node.inputs["Transparency"])

    for i in range(int(len(node.inputs) / 2)):
        layer = i+1
        brdfSocket   = "BRDF %i"   % layer
        weightSocket = "Weight %i" % layer

        if not node.inputs[brdfSocket].is_linked:
            continue

        brdfs.append(WriteConnectedNode(bus, nodetree, node.inputs[brdfSocket]))

        if node.inputs[weightSocket].is_linked:
            weights.append(WriteConnectedNode(bus, nodetree, node.inputs[weightSocket]))
        else:
            weightParam = "%sW%sI%i"%(pluginName, brdfs[i], i)

            weightColor = mathutils.Color([node.inputs[weightSocket].value]*3)

            o.set('TEXTURE', 'TexAColor', weightParam)
            o.writeHeader()
            o.writeAttibute('texture', weightColor)
            o.writeFooter()

            weights.append(weightParam)

    o.set('BRDF', 'BRDFLayered', pluginName)
    o.writeHeader()
    o.writeAttibute('brdfs', "List(%s)" % ','.join(brdfs))
    o.writeAttibute('weights', "List(%s)" % ','.join(weights))
    o.writeAttibute('additive_mode', node.additive_mode)
    o.writeAttibute('transparency_tex', transparency)
    o.writeFooter()

    return pluginName


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##

def WriteConnectedNode(bus, nodetree, nodeSocket, linkedOnly=False):
    # Debug("Processing socket: %s [%s]" % (nodeSocket.name, nodeSocket.vray_attr))

    if not nodeSocket.is_linked:
        if linkedOnly:
            return None
        else:
            if hasattr(nodeSocket, 'value'):
                return nodeSocket.value
            return None

    connectedNode   = GetConnectedNode(nodetree, nodeSocket)
    connectedSocket = GetConnectedSocket(nodetree, nodeSocket)
    if connectedNode:
        vrayPlugin = WriteNode(bus, nodetree, connectedNode, fromSocket=nodeSocket, linkedOnly=linkedOnly)

        if connectedSocket.vray_attr and connectedSocket.vray_attr not in {'NONE'}:
            # XXX: use as a workaround
            # TODO: get plugin desc and check if the attr is output,
            # but skip uvwgen anyway.
            #
            if connectedSocket.vray_attr not in {'uvwgen', 'bitmap'}:
                vrayPlugin = "%s::%s" % (vrayPlugin, connectedSocket.vray_attr)

                if connectedNode.bl_idname == 'VRayNodeTexMayaFluid':
                    vrayPlugin = vrayPlugin.replace("::out_flame",   "@Flame")
                    vrayPlugin = vrayPlugin.replace("::out_density", "@Density")
                    vrayPlugin = vrayPlugin.replace("::out_fuel",    "@Fuel")

        return vrayPlugin

    return None


def WriteNodePy(bus, nodetree, node, linkedOnly=False):
    # Debug("Processing node: %s..." % node.name)

    # Write some nodes in a special way
    if node.bl_idname == 'VRayNodeBRDFLayered':
        return WriteVRayNodeBRDFLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeTexLayered':
        return WriteVRayNodeTexLayered(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeSelectObject':
        return WriteVRayNodeSelectObject(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeSelectGroup':
        return WriteVRayNodeSelectGroup(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeSelectNodeTree':
        return WriteVRayNodeSelectNodeTree(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeBlenderOutputGeometry':
        return WriteVRayNodeBlenderOutputGeometry(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeBlenderOutputMaterial':
        return WriteVRayNodeBlenderOutputMaterial(bus, nodetree, node)
    elif node.bl_idname == 'VRayNodeTransform':
        return node.getTransform()
    elif node.bl_idname == 'VRayNodeMatrix':
        return node.getMatrix()
    elif node.bl_idname == 'VRayNodeVector':
        return node.getVector()

    pluginName = LibUtils.CleanString("NT%sN%s" % (nodetree.name, node.name))
    if pluginName in bus['cache']['plugins']:
        return pluginName
    bus['cache']['plugins'].add(pluginName)

    vrayType   = node.vray_type
    vrayPlugin = node.vray_plugin

    if vrayType == 'NONE' or vrayPlugin == 'NONE':
        return None

    # Debug("Generating plugin \"%s\" [%s, %s]" % (pluginName, vrayType, vrayPlugin), msgType='INFO')

    propGroup = getattr(node, vrayPlugin)

    socketParams = {}

    for nodeSocket in node.inputs:
        vrayAttr = nodeSocket.vray_attr

        socketParams[vrayAttr] = WriteConnectedNode(bus, nodetree, nodeSocket)

    pluginModule = PLUGINS[vrayType][vrayPlugin]

    # XXX: Used to access 'image' pointer for BitmapBuffer
    # and 'texture' for TexGradRamp and TexRemap
    #
    bus['context']['node'] = node

    result = ExportUtils.WritePlugin(
        bus,
        pluginModule,
        pluginName,
        propGroup,
        socketParams
    )

    return result


def WriteNodeCpp(bus, nodetree, node, fromSocket=None, _linkedOnly_=False):
    return _vray_for_blender.exportNode(
        nodetree.as_pointer(),
        node.as_pointer(),
        fromSocket.as_pointer()
    )


def WriteNode(bus, nodetree, node, fromSocket=None, linkedOnly=False):
    if True:
        WriteNodeCpp(bus, nodetree, node, fromSocket)
    else:
        WriteNodePy(bus, nodetree, node, linkedOnly)


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

def WriteVRayMaterialNodeTree(bus, ntree, force=False):
    scene = bus['scene']

    VRayScene = scene.vray
    SettingsOptions = VRayScene.SettingsOptions

    outputNode = GetNodeByType(ntree, 'VRayNodeOutputMaterial')
    if not outputNode:
        debug.Debug("Output node not found!", msgType='ERROR')
        return bus['defaults']['material']

    # Check global material override
    #
    if 'material_override' in bus:
        if bus['material_override'] is not None and outputNode.dontOverride == False:
            return bus['material_override']

    # Check connection
    #
    materialSocket = outputNode.inputs['Material']
    if not materialSocket.is_linked:
        debug.Debug("NodeTree: %s" % ntree.name, msgType='ERROR')
        debug.Debug("  Node: %s" % outputNode.name, msgType='ERROR')
        debug.Debug("  Error: Material socket is not connected!", msgType='ERROR')
        return bus['defaults']['material']

    return WriteConnectedNode(bus, ntree, materialSocket)

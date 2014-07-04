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

import base64
import os

import bpy
import mathutils

from vb30.plugins import PLUGINS_ID

from vb30.nodes import tools as NodesTools
from vb30.nodes import importing as NodesImport
from vb30.nodes import export as NodesExport
from vb30.nodes import utils as NodesUtils

from vb30.nodes.sockets import AddInput, AddOutput

from vb30.lib import BlenderUtils
from vb30.lib import AttributeUtils

from vb30 import debug
from pprint import pprint


class ConvertException(Exception):
    pass


######## ##    ## ########  ########  ######
   ##     ##  ##  ##     ## ##       ##    ##
   ##      ####   ##     ## ##       ##
   ##       ##    ########  ######    ######
   ##       ##    ##        ##             ##
   ##       ##    ##        ##       ##    ##
   ##       ##    ##        ########  ######

TexTypes = {'IMAGE', 'VRAY'}

OverrideInputSocket = {
    'MtlRenderStats' : "Base Mtl",
    'MtlWrapper'     : "Base Material",
    'MtlOverride'    : "Base",
}

ObjectMaterialOverrides = (
    'MtlOverride',
)

OutputToSocket = {
    'TEXTURE'       : "Output",
    'FLOAT_TEXTURE' : "Out Intensity",
}

BlendModeToIndex = {
    'NONE' : '0',
    'OVER' : '1',
    'IN' : '2',
    'OUT' : '3',
    'ADD' : '4',
    'SUBTRACT' : '5',
    'MULTIPLY' : '6',
    'DIFFERENCE' : '7',
    'LIGHTEN' : '8',
    'DARKEN' : '9',
    'SATURATE' : '10',
    'DESATUREATE' : '11',
    'ILLUMINATE' : '12',
}


def _getBrdfInfluence(ma):
    VRayMaterial = ma.vray

    brdfType = VRayMaterial.type
    BRDF = getattr(VRayMaterial, brdfType)

    if brdfType == 'BRDFVRayMtl':
        return {
            'diffuse' : {
                'value' : mathutils.Color(BRDF.diffuse),
                'type'  : 'TEXTURE',
            },
            'opacity' : {
                'value' : ma.alpha,
                'type'  : 'FLOAT_TEXTURE',
            },
            'roughness' : {
                'value' : BRDF.roughness,
                'type'  : 'FLOAT_TEXTURE',
            },
            'reflect_glossiness' : {
                'value' : BRDF.reflect_glossiness,
                'type'  : 'FLOAT_TEXTURE',
            },
            'hilight_glossiness' : {
                'value' : BRDF.hilight_glossiness,
                'type'  : 'FLOAT_TEXTURE',
            },
            'reflect' : {
                'value' : mathutils.Color(BRDF.reflect_color),
                'type'  : 'TEXTURE',
            },
            'anisotropy' : {
                'value' : BRDF.anisotropy,
                'type'  : 'FLOAT_TEXTURE',
            },
            'anisotropy_rotation' : {
                'value' : BRDF.anisotropy_rotation,
                'type'  : 'FLOAT_TEXTURE',
            },
            'refract' : {
                'value' : mathutils.Color(BRDF.refract_color),
                'type'  : 'TEXTURE',
            },
            'refract_glossiness' : {
                'value' : BRDF.refract_glossiness,
                'type'  : 'FLOAT_TEXTURE',
            },
            'translucency_color' : {
                'value' : mathutils.Color(BRDF.translucency_color),
                'type'  : 'TEXTURE',
            },
            'fresnel_ior' : {
                'value' : 0.0,
                'type'  : 'FLOAT_TEXTURE',
            },
            'refract_ior' : {
                'value' : 0.0,
                'type'  : 'TEXTURE',
            },
            'normal' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type'  : 'TEXTURE',
            },
            'displacement' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type'  : 'TEXTURE',
            },
        }

    elif brdfType == 'BRDFSSS2Complex':
        return {
            'overall_color' : {
                'value' : mathutils.Color(ma.diffuse_color),
                'type' : 'TEXTURE',
            },
            'sub_surface_color' : {
                'value' : mathutils.Color(BRDF.sub_surface_color),
                'type' : 'TEXTURE',
            },
            'scatter_radius' : {
                'value' : mathutils.Color(BRDF.scatter_radius),
                'type' : 'TEXTURE',
            },
            'diffuse_color' : {
                'value' : mathutils.Color(BRDF.diffuse_color),
                'type' : 'TEXTURE',
            },
            'diffuse_amount' : {
                'value' : BRDF.diffuse_amount,
                'type' : 'FLOAT_TEXTURE',
            },
            'specular_color' : {
                'value' : mathutils.Color(BRDF.specular_color),
                'type' : 'TEXTURE',
            },
            'specular_amount' : {
                'value' : 0.0,
                'type' : 'FLOAT_TEXTURE',
            },
            'specular_glossiness' : {
                'value' : 0.0,
                'type' : 'FLOAT_TEXTURE',
            },
            'normal' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type' : 'TEXTURE',
            },
            'displacement' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type' : 'TEXTURE',
            },
        }

    elif brdfType == 'BRDFCarPaint':
        return {
            'normal' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type'  : 'TEXTURE',
            },
            'displacement' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type'  : 'TEXTURE',
            },
        }

    elif brdfType == 'BRDFLight':
        return {
            'diffuse' : {
                'value' : mathutils.Color(BRDF.color),
                'type'  : 'TEXTURE',
            },

            'displacement' : {
                'value' : mathutils.Color((0.0,0.0,0.0)),
                'type' : 'TEXTURE',
            },
        }

    return {}


##     ## ######## #### ##        ######
##     ##    ##     ##  ##       ##    ##
##     ##    ##     ##  ##       ##
##     ##    ##     ##  ##        ######
##     ##    ##     ##  ##             ##
##     ##    ##     ##  ##       ##    ##
 #######     ##    #### ########  ######

def CopyRamp(nodeRamp, vrayRamp):
    elementsToCreate = len(nodeRamp.elements) - 2
    for i in range(elementsToCreate):
        vrayRamp.elements.new(0.0)

    for i,rampElement in enumerate(nodeRamp.elements):
        el = vrayRamp.elements[i]
        el.color    = rampElement.color
        el.position = rampElement.position


def convert_bi():
    CONVERT_BLEND_TYPE= {
        'MIX':          'OVER',
        'SCREEN':       'OVER',
        'DIVIDE':       'OVER',
        'HUE':          'OVER',
        'VALUE':        'OVER',
        'COLOR':        'OVER',
        'SOFT LIGHT':   'OVER',
        'LINEAR LIGHT': 'OVER',
        'OVERLAY':      'OVER',
        'ADD':          'ADD',
        'SUBTRACT':     'SUBTRACT',
        'MULTIPLY':     'MULTIPLY',
        'DIFFERENCE':   'DIFFERENCE',
        'DARKEN':       'DARKEN',
        'LIGHTEN':      'LIGHTEN',
        'SATURATION':   'SATURATE',
    }

    for ma in bpy.data.materials:
        debug.PrintInfo("Converting from Blender Internal: %s" % ma.name)

        rm = ma.raytrace_mirror
        rt = ma.raytrace_transparency

        VRayMaterial = ma.vray
        BRDFVRayMtl  = VRayMaterial.BRDFVRayMtl

        BRDFVRayMtl.diffuse = ma.diffuse_color

        if ma.emit > 0.0:
            VRayMaterial.type= 'BRDFLight'

        if rm.use:
            BRDFVRayMtl.reflect_color = tuple([rm.reflect_factor]*3)
            BRDFVRayMtl.reflect_glossiness = rm.gloss_factor
            BRDFVRayMtl.reflect_subdivs = rm.gloss_samples
            BRDFVRayMtl.reflect_depth = rm.depth
            BRDFVRayMtl.option_cutoff = rm.gloss_threshold
            BRDFVRayMtl.anisotropy = 1.0 - rm.gloss_anisotropic

            if rm.fresnel > 0.0:
                BRDFVRayMtl.fresnel = True
                BRDFVRayMtl.fresnel_ior = rm.fresnel

        for slot in ma.texture_slots:
            if slot and slot.texture and slot.texture.type in TexTypes:
                VRaySlot = slot.texture.vray_slot
                VRayTexture = slot.texture.vray

                VRaySlot.blend_mode = CONVERT_BLEND_TYPE[slot.blend_type]

                if slot.use_map_emit:
                    VRayMaterial.type = 'BRDFLight'

                    VRaySlot.map_diffuse = True

                if slot.use_map_normal:
                    VRaySlot.map_normal = True
                    VRaySlot.BRDFBump.bump_tex_mult = slot.normal_factor

                if slot.use_map_color_diffuse:
                    VRaySlot.map_diffuse  = True
                    VRaySlot.diffuse_mult = slot.diffuse_color_factor

                if slot.use_map_raymir:
                    VRaySlot.map_reflect  = True
                    VRaySlot.reflect_mult = slot.raymir_factor

                if slot.use_map_alpha:
                    VRaySlot.map_opacity  = True
                    VRaySlot.opacity_mult = slot.alpha_factor


def _getTextureFromTextures(textures, key):
    # XXX: Check why it could be list
    return textures[key][0] if type(textures[key]) is list else textures[key]


def _getParamString(*args):
    return "".join([str(s) for s in args])


# Very simple stupid short name hash
def _getStringHash(s):
    s = bytes(str(int(hash(s) / -(10000000000))), 'ascii')
    s = base64.b64encode(s, altchars=b'pS')
    return s.decode('ascii').replace('=','')


def _findSocketCaseInsensitive(node, socketName, fromInputs=True):
    sockets = node.inputs if fromInputs else node.outputs
    for socket in sockets:
        if socket.name.lower() == socketName.lower():
            return socket
    return None


def _createGroupMaterial(ntree, ma):
    if not ma.vray.ntree:
        return None

    maOutput = NodesUtils.GetNodeByType(ma.vray.ntree, 'VRayNodeOutputMaterial')
    if not maOutput:
        return None

    mtlNode = NodesUtils.GetConnectedNode(ma.vray.ntree, maOutput.inputs['Material'])
    if not mtlNode:
        return None

    # Create group node
    maGroupNode = ntree.nodes.new('ShaderNodeGroup')
    maGroupNode.node_tree = ma.vray.ntree

    # Add output to material tree
    maGroupOutput = maGroupNode.node_tree.nodes.new('NodeGroupOutput')
    maGroupOutput.location.x += NodesTools.NODE_LEVEL_WIDTH
    maGroupOutput.location.y += 50

    # Create and link output material socket
    maGroupNode.node_tree.outputs.new('VRaySocketMtl', 'Material')
    maGroupNode.node_tree.links.new(
        mtlNode.outputs['Material'],
        maGroupOutput.inputs['Material']
    )

    return maGroupNode


def _createVRayTree(name, vrayTreeType):
    nt = bpy.data.node_groups.new(name, type='VRayNodeTree%s' % vrayTreeType)
    nt.use_fake_user = True
    return nt


def _createVRayNode(ntree, vrayNodeType, nodeName=None):
    if nodeName is not None:
        if nodeName in ntree.nodes:
            return ntree.nodes[nodeName]
    node = ntree.nodes.new('VRayNode%s' % vrayNodeType)
    if nodeName is not None:
        node.name = nodeName
    return node


def _connectNodes(ntree, outputNode, outputSocketName, inputNode, inputSocketName):
    outSockName = None
    outSock     = _findSocketCaseInsensitive(outputNode, outputSocketName, fromInputs=False)
    if outSock:
        outSockName = outSock.name
    else:
        # Fallback to some default output socket name
        outSockName = NodesImport.getOutputSocket(outputNode.vray_plugin)

    if inputSocketName not in inputNode.inputs:
        debug.PrintError("Can't find input socket: %s.%s" % (inputNode.name, inputSocketName))
        return

    ntree.links.new(
        outputNode.outputs[outSockName],
        inputNode.inputs[inputSocketName]
    )


def TransferProperties(node, pluginID, oldPropGroup, skipAttrs={}):
    pluginDesc = PLUGINS_ID[pluginID]
    propGroup  = getattr(node, pluginID)

    for attrDesc in pluginDesc.PluginParams:
        attrName = attrDesc['attr']

        if attrName in skipAttrs:
            continue

        attrValue = getattr(oldPropGroup, attrName)

        if attrDesc['type'] in AttributeUtils.InputTypes:
            attrSockName = AttributeUtils.GetNameFromAttr(attrName)

            inputSock = _findSocketCaseInsensitive(node, attrSockName)
            if not inputSock:
                debug.PrintError("Can't find socket to attribute: %s.%s" % (pluginID, attrName))
            else:
                inputSock.value = attrValue

        else:
            setattr(propGroup, 'attrName', attrValue)


def _getBumpAmount(ma):
    for ts in ma.texture_slots:
        if not (ts and ts.texture):
            continue
        tex = ts.texture
        if tex.type not in TexTypes:
            continue
        if tex.vray_slot.map_normal:
            return tex.vray_slot.BRDFBump.bump_tex_mult
    return 0.05


def _getDisplacementAmount(ob):
    for ms in ob.material_slots:
        if not (ms and ms.material):
            continue
        ma = ms.material
        for ts in ma.texture_slots:
            if not (ts and ts.texture):
                continue
            tex = ts.texture
            if tex.type not in TexTypes:
                continue
            if tex.vray_slot.map_displacement:
                return tex.vray_slot.GeomDisplacedMesh.displacement_amount
    return 0.05


######## ######## ##     ## ######## ##     ## ########  ########
   ##    ##        ##   ##     ##    ##     ## ##     ## ##
   ##    ##         ## ##      ##    ##     ## ##     ## ##
   ##    ######      ###       ##    ##     ## ########  ######
   ##    ##         ## ##      ##    ##     ## ##   ##   ##
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##
   ##    ######## ##     ##    ##     #######  ##     ## ########

class TextureToNode:
    def createNode(self, ntree):
        pass


 ######  #### ##    ##  ######   ##       ########
##    ##  ##  ###   ## ##    ##  ##       ##
##        ##  ####  ## ##        ##       ##
 ######   ##  ## ## ## ##   #### ##       ######
      ##  ##  ##  #### ##    ##  ##       ##
##    ##  ##  ##   ### ##    ##  ##       ##
 ######  #### ##    ##  ######   ######## ########

class SingleTexture(TextureToNode):
    def __init__(self, texture, output='TEXTURE', slot=None, blend_mode='NONE', stencil=False, mult=1.0, invert=False):
        self.texture    = texture
        self.output     = output
        self.blend_mode = blend_mode
        self.stencil    = stencil
        self.slot       = slot
        self.mult       = mult
        self.invert     = invert

    def info(self):
        print('Single Texture: %s' % self.texture)
        print('  Output: %s' % self.output)
        print('  Blend Mode: %s' % self.blend_mode)
        print('  Stencil: %s' % self.stencil)
        print('  Mult: %s' % self.mult)
        print('  Invert: %s' % self.invert)

    def __str__(self):
        return 'Single Texture'

    def createNode(self, ntree):
        tex = None

        if type(self.texture) is mathutils.Color:
            tex = _createVRayNode(ntree, "TexAColor")
            tex.inputs['Color'].value = self.texture

        elif type(self.texture) in {float, int}:
            tex = _createVRayNode(ntree, "TexFloatToColor")
            tex.inputs['Input'].value = self.texture

        else:
            VRayTexture = self.texture.vray
            VRaySlot = self.texture.vray_slot

            if self.texture.type == 'IMAGE':
                btm = _createVRayNode(ntree, "BitmapBuffer")
                tex = _createVRayNode(ntree, "TexBitmap")

                if self.texture.image and self.texture.image.filepath:
                    makeRel       = self.texture.image.filepath.startswith("//")
                    imageFilepath = bpy.path.abspath(self.texture.image.filepath)

                    NodesImport.LoadImage(
                        imageFilepath, os.path.dirname(bpy.data.filepath), btm.texture,
                        makeRelative=makeRel
                    )

                _connectNodes(ntree,
                    btm, 'Bitmap',
                    tex, 'Bitmap'
                )

            elif self.texture.type == 'VRAY':
                texType = VRayTexture.type

                oldPropGroup = getattr(VRayTexture, texType)

                tex = _createVRayNode(ntree, texType)
                skipAttrs = {}

                if texType == 'TexGradRamp':
                    # Load ramp info manually
                    skipAttrs = {'positions', 'colors'}
                    CopyRamp(self.texture.color_ramp, tex.texture.color_ramp)

                TransferProperties(tex, texType, oldPropGroup, skipAttrs)

            # Mapping
            uvwgen = None
            mappingType = self.texture.vray.texture_coords

            uvLayer = VRaySlot.uv_layer
            if not uvLayer:
                if self.slot:
                    uvLayer = slot.uv_layer

            # Always generate UV channel
            pluginHash = _getParamString(
                VRaySlot.uv_layer,
                VRaySlot.offset[0],
                VRaySlot.offset[1],
                VRaySlot.scale[0],
                VRaySlot.scale[1],
                VRaySlot.texture_rot,
                VRayTexture.mirror_u,
                VRayTexture.mirror_v,
                VRayTexture.tile_u,
                VRayTexture.tile_v,
            )

            name = "UV@%s" % _getStringHash(pluginHash)

            uvwgen = _createVRayNode(ntree, "UVWGenMayaPlace2dTexture", nodeName=name)
            uvwgen.UVWGenMayaPlace2dTexture.uv_set_name = VRaySlot.uv_layer
            uvwgen.UVWGenMayaPlace2dTexture.mirror_u = VRayTexture.mirror_u
            uvwgen.UVWGenMayaPlace2dTexture.mirror_v = VRayTexture.mirror_v
            uvwgen.inputs['Repeat U'].value = VRayTexture.tile_u
            uvwgen.inputs['Repeat V'].value = VRayTexture.tile_v
            uvwgen.inputs['Rotate UV'].value = VRaySlot.texture_rot
            uvwgen.inputs['Translate Frame U Tex'].value = VRaySlot.offset[0]
            uvwgen.inputs['Translate Frame V Tex'].value = VRaySlot.offset[1]

            # Add additional generators
            uvwgenAdd = None
            if mappingType == 'ORCO':
                pass

            elif mappingType == 'WORLD':
                pass

            if uvwgen:
                _connectNodes(ntree,
                    uvwgen, 'Mapping',
                    tex,    'Mapping'
                )

                if uvwgenAdd:
                    _connectNodes(ntree,
                        uvwgenAdd, 'Mapping',
                        uvwgen,    'Mapping'
                    )

        return tex


##     ## #### ##     ##
###   ###  ##   ##   ##
#### ####  ##    ## ##
## ### ##  ##     ###
##     ##  ##    ## ##
##     ##  ##   ##   ##
##     ## #### ##     ##

class MixTexture(TextureToNode):
    def __init__(self, color1, color2, mix_map, blend_mode='NONE', output='TEXTURE'):
        self.color1  = color1
        self.color2  = color2
        self.mix_map = mix_map
        self.blend_mode = blend_mode
        self.output  = output

    def info(self):
        print('Mix Texture:')
        print('  Color1: %s' % self.color1)
        print('  Color2: %s' % self.color2)
        print('  Mix: %s' % self.mix_map)
        print('  Output: %s' % self.output)

    def __str__(self):
        return 'Mix Texture'

    def createNode(self, ntree):
        texMix = _createVRayNode(ntree, "TexMix")

        color1  = self.color1.createNode(ntree)
        color2  = self.color2.createNode(ntree)
        mix_map = self.mix_map.createNode(ntree)

        _connectNodes(ntree,
            color1, OutputToSocket[self.color1.output],
            texMix, 'Source A'
        )

        _connectNodes(ntree,
            color2, OutputToSocket[self.color2.output],
            texMix, 'Source B'
        )

        _connectNodes(ntree,
            mix_map, OutputToSocket[self.mix_map.output],
            texMix, 'Mix Map'
        )

        return texMix


##          ###    ##    ## ######## ########  ######## ########
##         ## ##    ##  ##  ##       ##     ## ##       ##     ##
##        ##   ##    ####   ##       ##     ## ##       ##     ##
##       ##     ##    ##    ######   ########  ######   ##     ##
##       #########    ##    ##       ##   ##   ##       ##     ##
##       ##     ##    ##    ##       ##    ##  ##       ##     ##
######## ##     ##    ##    ######## ##     ## ######## ########

class LayeredTexture(TextureToNode):
    def __init__(self, textures, blend_modes, output='TEXTURE'):
        self.textures    = textures
        self.blend_modes = blend_modes
        self.output      = output

    def info(self):
        print('Layered Texture')
        for i in range(len(self.textures)):
            print('  Texture: %s'    % self.textures[i])
            print('  Blend Mode: %s' % self.blend_modes[i])

    def __str__(self):
        return 'Layered Texture'

    def createNode(self, ntree):
        texLayeredNode = _createVRayNode(ntree, "TexLayered")

        for i,tex in enumerate(reversed(self.textures)):
            # Get and/or create layered socket
            humanIndex = i + 1
            texSockName = "Texture %i" % humanIndex
            if not texSockName in texLayeredNode.inputs:
                AddInput(texLayeredNode, 'VRaySocketTexLayered', texSockName)

            # Create node
            texNode = tex.createNode(ntree)

            # Connect to layered
            _connectNodes(ntree,
                texNode, OutputToSocket[tex.output],
                texLayeredNode, texSockName
            )

            # Set blend mode
            texLayeredNode.inputs[texSockName].value = BlendModeToIndex[tex.blend_mode]

        return texLayeredNode


def CreateTextureNodes(ntree, node, textures):
    pluginID = node.vray_plugin

    pluginDesc = PLUGINS_ID[pluginID]

    for attrDesc in pluginDesc.PluginParams:
        attrName = attrDesc['attr']
        attrSockName = AttributeUtils.GetNameFromAttr(attrName)

        inputSocket = _findSocketCaseInsensitive(node, attrSockName)

        if attrDesc['type'] not in AttributeUtils.InputTypes:
            continue

        if attrName in textures:
            tex = textures[attrName]
            debug.PrintInfo('Found texture "%s" for attr "%s"' % (tex, attrName))

            texNode = tex.createNode(ntree)

            _connectNodes(
                ntree,
                texNode, OutputToSocket[tex.output],
                node,    inputSocket.name
            )


def PreprocessTextures(ma, influence):
    textures = {}

    for ts in ma.texture_slots:
        if not (ts and ts.texture):
            continue

        tex = ts.texture
        if tex.type not in TexTypes:
            continue

        VRayTexture = tex.vray
        VRaySlot    = tex.vray_slot

        # Convert mapping here if needed
        # This will support both vb25's 'master' and 'dev/animation'
        if not VRaySlot.uv_layer:
            VRaySlot.uv_layer = ts.uv_layer

        debug.PrintInfo('  Texture "%s" {%s:%s}' % (tex.name, tex.type, VRayTexture.type))

        for inf in influence:
            slotUse    = "map_%s"  % inf
            slotMult   = "%s_mult" % inf
            slotInvert = "%s_invert" % slotUse

            if not getattr(VRaySlot, slotUse):
                continue

            # NOTE: Adding default color value to blend over
            if not inf in textures:
                textures[inf] = [SingleTexture(
                    output=influence[inf]['type'],
                    texture=influence[inf]['value'],
                )]

            textures[inf].append(SingleTexture(
                texture=tex,
                slot=ts,
                output=influence[inf]['type'],
                blend_mode=VRaySlot.blend_mode,
                mult=getattr(VRaySlot, slotMult, 1.0),
                invert=getattr(VRaySlot, slotInvert, False),
                stencil=ts.use_stencil,
            ))

    return textures


def ProcessTextures(ma):
    def _hasStencil(slotTextures):
        for i,texDesc in enumerate(slotTextures):
            if texDesc.stencil:
                return i
        return None

    if ma.node_tree:
        return {}

    processedTextures = {}

    influence = _getBrdfInfluence(ma)

    textures  = PreprocessTextures(ma, influence)
    if textures:
        # print("Raw texture list:")
        # pprint(textures)

        # First check simple situations
        #
        for slotType in textures.keys():
            slotTextures = textures[slotType]

            hasStencil     = _hasStencil(slotTextures)
            slotOutputType = influence[slotType]['type']

            # We have only 2 entries:
            # 0. color from mappable value
            # 1. texture
            if len(slotTextures) == 2:
                valColor = slotTextures[0]
                valTex   = slotTextures[1]

                # If blend mode is 'NONE' we could use just the texture
                if valTex.blend_mode == 'NONE':
                    textures[slotType] = valTex

            # Now check for stencils
            # NOTE: Support only one stencil by now
            elif hasStencil:
                texOne = slotTextures[hasStencil-1]
                texMix = slotTextures[hasStencil]
                texTwo = slotTextures[hasStencil+1]

                slotTextures[hasStencil] = MixTexture(
                    color1=texOne,
                    color2=texTwo,
                    mix_map=texMix,
                    blend_mode=texMix.blend_mode,
                    output=slotOutputType,
                )

                del slotTextures[hasStencil-1]
                del slotTextures[hasStencil]

        # print("Raw texture list after prepass:")
        # pprint(textures)

        # Finally blend into texlayered
        for slotType in textures.keys():
            slotTextures = textures[slotType]
            if type(slotTextures) is not list:
                processedTextures[slotType] = [slotTextures]
                continue

            layered_tex = []
            layered_bm  = []
            for i,tex in enumerate(slotTextures):
                layered_tex.append(tex)
                layered_bm.append(tex.blend_mode)

            processedTextures[slotType] = LayeredTexture(
                textures=layered_tex,
                blend_modes=layered_bm,
                output=slotOutputType,
            )

        # print("Grouped texture list:")
        # print(processedTextures)

    return processedTextures


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

def _ShaderTreeHasBump(nt):
    return False


def _ShaderTreeHasDisplace(nt):
    return False

def _ConvertToTexSampler(maNode, n):
    pass


NodeTypeMapping = {
    'ShaderNodeOutputMaterial' : {
        'type' : 'OutputMaterial',
        'sockets' : {},
    },

    # BRDF
    # XXX: Or use BRDFVRayMtl for all?
    'ShaderNodeBsdfDiffuse' : {
        'type' : 'BRDFDiffuse',
        'sockets' : {
            'Color' : 'Color',
            'Roughness' : 'Roughness',
        }
    },
    'ShaderNodeBsdfGlass' : {
        'type' : 'BRDFGlass',
        'sockets' : {
            'Color' : 'Color Tex',
            'IOR'   : 'Ior Tex',
        }
    },
    'ShaderNodeBsdfAnisotropic' : {
        'type' : 'BRDFVRayMtl',
        'sockets' : {
            'Color'      : 'Diffuse',
            'Roughness'  : 'Roughness',
            'Anisotropy' : 'Anisotropy',
            'Rotation'   : 'Anisotropy Rotation',
        }
    },
    'ShaderNodeBsdfGlossy' : {
        'type' : 'BRDFVRayMtl',
        'sockets' : {
            'Color' : 'Diffuse',
            'Roughness' : 'Roughness',
        }
    },
    'ShaderNodeMixShader' : {
        'type' : 'BRDFLayered',
        'sockets' : {
            'Fac',
            'Shader'
        },
    },

    # Textures
    'ShaderNodeTexChecker' : {
        'type' : 'TexChecker',
        'sockets' : {},
    },
    'ShaderNodeValToRGB'   : {
        'type' : 'TexRemap',
        'sockets' : {
            'Color',
        },
    },
    'ShaderNodeTangent' : {
        'type' : 'TexSampler',
        'sockets' : {},
        'convert' : _ConvertToTexSampler,
    },
}

SocketOutputMapping = {
    'NodeSocketShader' : {
        'type' : 'VRaySocketBRDF',
        'name' : 'BRDF',
    },
    'NodeSocketColor' : {
        'type' : 'VRaySocketColor',
        'name' : 'Output',
    },
    'NodeSocketFloatFactor' : {
        'type' : 'VRaySocketFloat',
        'name' : 'Output',
    },
    'NodeSocketFloat' : {
        'type' : 'VRaySocketFloat',
        'name' : 'Output',
    },
    'NodeSocketVector' : {
        'type' : 'VRaySocketVector',
        'name' : 'Output',
    },
}


def ExportSocket(maNtree, maNode, inSock, vrayNode, nt, connect=True):
    debug.PrintInfo("Input socket '%s' type is '%s'." %
        (inSock.name, inSock.bl_idname))

    if inSock.name not in NodeTypeMapping[maNode.bl_idname]['sockets']:
        debug.PrintError("Input socket '%s' of type '%s' is not supported!" %
            (inSock.name, inSock.bl_idname))
        return None

    if not inSock.is_linked:
        vrayInSock = vrayNode.inputs[NodeTypeMapping[maNode.bl_idname]['sockets'][inSock.name]]
        value      = maNode.inputs[inSock.name].default_value

        # NOTE: We don't support 4 value color
        if hasattr(value, '__len__') and len(value) == 4:
            vrayInSock.value = (value[0],value[1],value[2])
        else:
            vrayInSock.value = value

    else:
        conNode = NodesUtils.GetConnectedNode(maNtree, inSock)
        conSock = NodesUtils.GetConnectedSocket(maNtree, inSock)

        if conSock.bl_idname not in SocketOutputMapping:
            debug.PrintError("Input socket '%s' of type '%s' can't be converted!" %
                (inSock.name, inSock.bl_idname))
            return None

        conVRayNode = ConvertNode(maNtree, conNode, nt)

        if connect:
            _connectNodes(nt,
                conVRayNode, SocketOutputMapping[conSock.bl_idname]['name'],
                vrayNode,    NodeTypeMapping[maNode.bl_idname]['sockets'][inSock.name],
            )

        return conVRayNode


def ConvertNode(maNtree, maNode, nt):
    if maNode.bl_idname not in NodeTypeMapping:
        debug.PrintError("Node '%s' of type '%s' is not supported!" %
            (maNode.name, maNode.bl_idname))
        return None

    vrayNodeType = NodeTypeMapping[maNode.bl_idname]['type']
    vrayNode = _createVRayNode(nt, vrayNodeType)

    convertFunc = NodeTypeMapping[maNode.bl_idname].get('convert')

    if maNode.bl_idname == 'ShaderNodeMixShader':
        # NOTE: If current node is 'ShaderNodeMixShader' and
        # we have a 'Fac' socket linked - connect 'out_intensity'
        # attribute of the correspondent node

        facNode   = ExportSocket(maNtree, maNode, maNode.inputs[0], None, nt, False)
        brdf1Node = ExportSocket(maNtree, maNode, maNode.inputs[1], None, nt, False)
        brdf2Node = ExportSocket(maNtree, maNode, maNode.inputs[2], None, nt, False)

        if facNode:
            _connectNodes(nt,
                facNode, 'Out Intensity',
                vrayNode, 'Weight 1'
            )

        if brdf1Node:
            _connectNodes(nt,
                brdf1Node, 'BSDF',
                vrayNode, 'BRDF 1'
            )

        if brdf2Node:
            _connectNodes(nt,
                brdf2Node, 'BSDF',
                vrayNode, 'BRDF 2'
            )

    elif convertFunc:
        convertFunc(maNode, nt)

    else:
        for inSock in maNode.inputs:
            ExportSocket(maNtree, maNode, inSock, vrayNode, nt)

    if maNode.bl_idname == 'ShaderNodeValToRGB':
        CopyRamp(maNode.color_ramp, vrayNode.texture.color_ramp)

        # vrayNode.inputs['Input Value'].value = nodeRamp.inputs['']

    return vrayNode


def ConvertNodeMaterial(scene, ob, ma):
    debug.PrintInfo("Converting node material: %s" % ma.name)

    materialNode = None

    maNtree = ma.node_tree
    nt      = _createVRayTree(ma.name, 'Material')

    ntOutput   = _createVRayNode(nt, 'OutputMaterial')
    ntMaterial = _createVRayNode(nt, 'MtlSingleBRDF')
    _connectNodes(nt, ntMaterial, 'Material', ntOutput, 'Material')

    maNtreeOutput = NodesUtils.GetNodeByType(maNtree, 'ShaderNodeOutputMaterial')
    maShader      = NodesUtils.GetConnectedNode(maNtree, maNtreeOutput.inputs['Surface'])

    vrayNode = ConvertNode(maNtree, maShader, nt)
    _connectNodes(nt, vrayNode, 'BRDF', ntMaterial, 'BRDF')

    NodesTools.rearrangeTree(nt, ntOutput)
    NodesTools.deselectNodes(nt)

    ma.vray.ntree = nt

    return ntMaterial


def ConvertMaterial(scene, ob, ma, textures):
    VRayMaterial = ma.vray
    VRayConverter = scene.vray.VRayConverter

    # This is the last node of the material
    # NOT the output, but the last Mtl node
    materialNode = None

    if VRayMaterial.ntree:
        outputNode = NodesUtils.GetNodeByType(VRayMaterial.ntree, 'VRayNodeOutputMaterial')
        materialNode = NodesUtils.GetConnectedNode(VRayMaterial.ntree, outputNode.inputs['Material'])

    else:
        if ma.node_tree:
            if not VRayConverter.convert_from_internal:
                return None
            return ConvertNodeMaterial(scene, ob, ma)

        debug.PrintInfo("Converting material: %s" % ma.name)

        nt = _createVRayTree(ma.name, 'Material')

        outputNode = _createVRayNode(nt, 'OutputMaterial')

        materialTop = _createVRayNode(nt, 'MtlSingleBRDF')
        brdfTo      = materialTop
        mainBRDF    = None

        if VRayMaterial.round_edges:
            mtlRoundEdges = _createVRayNode(nt, 'MtlRoundEdges')
            mtlRoundEdges.inputs['Radius'].value = VRayMaterial.radius

            _connectNodes(nt,
                materialTop,   'Material',
                mtlRoundEdges, 'Base Mtl')

            materialTop = mtlRoundEdges

        if VRayMaterial.material_id_number:
            mtlMaterialID = _createVRayNode(nt, 'MtlMaterialID')
            mtlMaterialID.MtlMaterialID.material_id_number  = VRayMaterial.material_id_number
            mtlMaterialID.inputs['Material Id Color'].value = VRayMaterial.material_id_color

            _connectNodes(nt,
                materialTop,   'Material',
                mtlMaterialID, 'Base Mtl')

            materialTop = mtlMaterialID

        if VRayMaterial.Mtl2Sided.use:
            mtl2Sided = _createVRayNode(nt, 'Mtl2Sided')
            mtl2Sided.Mtl2Sided.force_1sided = VRayMaterial.Mtl2Sided.force_1sided
            mtl2Sided.inputs['Translucency'].value = [VRayMaterial.Mtl2Sided.translucency_slider]*3

            backMat = None
            if VRayMaterial.Mtl2Sided.back:
                backMaName = VRayMaterial.Mtl2Sided.back
                if backMaName in bpy.data.materials:
                    backMa  = bpy.data.materials[backMaName]
                    backTex = ProcessTextures(backMa)

                    ConvertMaterial(scene, ob, backMa, backTex)

                    backMat = _createGroupMaterial(nt, backMa)

            _connectNodes(nt,
                materialTop, 'Material',
                mtl2Sided,   'Front')

            if backMat:
                _connectNodes(nt,
                    backMat,   'Material',
                    mtl2Sided, 'Back')
            else:
                _connectNodes(nt,
                    materialTop, 'Material',
                    mtl2Sided,   'Back')

            materialTop = mtl2Sided

        if VRayMaterial.MtlOverride.use:
            pass

        for ovrName in {'MtlWrapper', 'MtlRenderStats'}:
            ovrPropGroup = getattr(VRayMaterial, ovrName)
            ovrUse = getattr(ovrPropGroup, 'use')
            if not ovrUse:
                continue
            debug.PrintInfo("  Found override: %s" % ovrName)

            ovrNode = _createVRayNode(nt, ovrName)

            _connectNodes(nt,
                materialTop, 'Material',
                ovrNode,     OverrideInputSocket[ovrName])

            materialTop = ovrNode

        # Connect last material to the output
        materialNode = materialTop
        _connectNodes(nt,
            materialTop, 'Material',
            outputNode,  'Material')

        # BRDFs
        #
        if 'normal' in textures:
            norTex = _getTextureFromTextures(textures, 'normal')

            mainBRDF = _createVRayNode(nt, 'BRDFBump')
            mainBRDF.inputs['Bump Amount Texture'].value = _getBumpAmount(ma)

            bumpTexNode = norTex.createNode(nt)

            _connectNodes(nt,
                bumpTexNode, 'Color',
                mainBRDF,    'Color Texture'
            )
            _connectNodes(nt,
                bumpTexNode, 'Out Intensity',
                mainBRDF,    'Float Texture'
            )

        # Finally generate main BRDF node and connect top brdf
        # if needed
        brdfType = VRayMaterial.type

        baseBRDF = _createVRayNode(nt, brdfType)

        oldPropGroup = getattr(VRayMaterial, brdfType)

        TransferProperties(baseBRDF, brdfType, oldPropGroup)

        CreateTextureNodes(nt, baseBRDF, textures)

        if brdfType == 'BRDFVRayMtl':
            if 'reflect' not in textures:
                baseBRDF.inputs['Reflect'].value = oldPropGroup.reflect_color
            if 'refract' not in textures:
                baseBRDF.inputs['Refract'].value = oldPropGroup.refract_color
            baseBRDF.inputs['Fog Color'].value = oldPropGroup.fog_color

        if not mainBRDF:
            mainBRDF = baseBRDF
        else:
            _connectNodes(nt,
                baseBRDF, 'BRDF',
                mainBRDF, 'Base Brdf')

        # Connect last BRDF to the last material
        _connectNodes(nt,
            mainBRDF, 'BRDF',
            brdfTo,   'BRDF')

        NodesTools.rearrangeTree(nt, outputNode)
        NodesTools.deselectNodes(nt)

        VRayMaterial.ntree = nt

    return materialNode


 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##

def ConvertObject(scene, ob):
    debug.PrintInfo("Converting object: %s" % ob.name)

    VRayObject = ob.vray
    VRayData   = ob.data.vray

    needNodeTree    = False
    hasDisplacement = None

    for ms in ob.material_slots:
        if not (ms and ms.material):
            continue

        ma = ms.material

        textures = ProcessTextures(ma)

        ConvertMaterial(scene, ob, ma, textures)

        if 'displacement' in textures:
            debug.PrintInfo("  Found displacement")
            hasDisplacement = textures['displacement']

    # Check if we need node tree from override materials
    for ovrName in ObjectMaterialOverrides:
        ovrPropGroup = getattr(VRayObject, ovrName)
        ovrUse = getattr(ovrPropGroup, 'use')
        if ovrUse:
            debug.PrintInfo("  Found override: %s" % ovrName)
            needNodeTree = True
            break

    needNodeTree = needNodeTree or hasDisplacement or VRayData.override

    if not VRayObject.ntree and needNodeTree:
        nt = _createVRayTree(ob.name, 'Object')

        outputNode = _createVRayNode(nt, 'ObjectOutput')

        # MATERIAL
        #
        blenderMaterial = _createVRayNode(nt, 'BlenderOutputMaterial')

        for ovrName in ObjectMaterialOverrides:
            ovrPropGroup = getattr(VRayObject, ovrName)
            ovrUse = getattr(ovrPropGroup, 'use')

            # NOTE: MtlWrapper and MtlOverride could be left on node
            # as is
            if not ovrUse:
                continue
            pass

        _connectNodes(nt,
            blenderMaterial, 'Material',
            outputNode,      'Material'
        )

        # GEOMETRY
        #

        # Infinite plane or VRayProxy
        if VRayData.override:
            debug.PrintInfo("  Found geometry override '%s'" % VRayData.override_type)

            if VRayData.override_type == 'VRAYPLANE':
                blenderGeometry = _createVRayNode(nt, 'GeomPlane')
            else:
                blenderGeometry = _createVRayNode(nt, 'GeomMeshFile')
                blenderGeometry.GeomMeshFile.file = VRayData.GeomMeshFile.file

        # Displacemnt and / or subdivision
        else:
            blenderGeometry = _createVRayNode(nt, 'BlenderOutputGeometry')

            if hasDisplacement:
                displaceNodeType = 'GeomDisplacedMesh'
                if VRayObject.GeomStaticSmoothedMesh.use:
                    displaceNodeType = 'GeomStaticSmoothedMesh'

                dispTex    = hasDisplacement
                dispAmount = _getDisplacementAmount(ob)

                displaceNode = _createVRayNode(nt, displaceNodeType)

                displacePropGroup = getattr(displaceNode, displaceNodeType)
                setattr(displacePropGroup, 'displacement_amount', dispAmount)

                dispTexNode = dispTex.createNode(nt)

                # Connect textures
                _connectNodes(nt,
                    dispTexNode,  'Color',
                    displaceNode, 'Color'
                )
                _connectNodes(nt,
                    dispTexNode,  'Out Intensity',
                    displaceNode, 'Float'
                )

                # Connect geometry
                _connectNodes(nt,
                    blenderGeometry,  'Geometry',
                    displaceNode,     'Mesh'
                )

                # Set displace as last geometry node
                blenderGeometry = displaceNode

            else:
                if VRayObject.GeomStaticSmoothedMesh.use:
                    pass

        if blenderGeometry:
            _connectNodes(nt,
                blenderGeometry, 'Geometry',
                outputNode,      'Geometry'
            )

        NodesTools.rearrangeTree(nt, outputNode)

        VRayObject.ntree = nt


 ######   ######  ######## ##    ## ########
##    ## ##    ## ##       ###   ## ##
##       ##       ##       ####  ## ##
 ######  ##       ######   ## ## ## ######
      ## ##       ##       ##  #### ##
##    ## ##    ## ##       ##   ### ##
 ######   ######  ######## ##    ## ########

def ConvertScene(scene):
    for ob in scene.objects:
        if ob.type in BlenderUtils.NonGeometryTypes:
            continue
        ConvertObject(scene, ob)


##     ## #### 
##     ##  ##  
##     ##  ##  
##     ##  ##  
##     ##  ##  
##     ##  ##  
 #######  #### 

class VRayConverter(bpy.types.PropertyGroup):
    convert_from_internal = bpy.props.BoolProperty(
        name = "From Internal",
        default = False
    )


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayConverter,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    setattr(bpy.types.VRayScene, 'VRayConverter', bpy.props.PointerProperty(
        type = VRayConverter,
    ))


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

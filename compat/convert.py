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
#
# TODO:
#
# Material:
#   [ ] Basic material types
#   [ ] Bump
#   [ ] Textures
#   [ ] Texture blend / stencil
#   [ ] Detect displacement
#   [ ]
#
# Object:
#   [ ] Displacement
#   [ ] Geometry override
#   [ ] Material override
#

import bpy
import mathutils

from vb30.nodes import tools as NodeTools
from vb30.lib import BlenderUtils

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

MaterialOverrides = (
    'MtlOverride',
    'MtlWrapper',
    'MtlRenderStats',
)

OverrideInputSocket = {
    'MtlRenderStats' : "Base Mtl",
    'MtlWrapper'     : "Base Material",
    'MtlOverride'    : "Base",
}

ObjectMaterialOverrides = (
    'MtlRenderStats',
    'MtlWrapper',
    'MtlOverride',
)


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

def _createVRayTree(name, vrayTreeType):
    nt = bpy.data.node_groups.new(name, type='VRayNodeTree%s' % vrayTreeType)
    nt.use_fake_user = True
    return nt


def _createVRayNode(ntree, vrayNodeType):
    return ntree.nodes.new('VRayNode%s' % vrayNodeType)


def _connectNodes(ntree, outputNode, outputSocket, inputNode, inputSocket):
    ntree.links.new(outputNode.outputs[outputSocket], inputNode.inputs[inputSocket])


######## ######## ##     ## ######## ##     ## ########  ######## 
   ##    ##        ##   ##     ##    ##     ## ##     ## ##       
   ##    ##         ## ##      ##    ##     ## ##     ## ##       
   ##    ######      ###       ##    ##     ## ########  ######   
   ##    ##         ## ##      ##    ##     ## ##   ##   ##       
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##       
   ##    ######## ##     ##    ##     #######  ##     ## ######## 

class TextureToNode:
    def createNode(self, ntree, fromNode, fromSocket):
        pass


class SingleTexture(TextureToNode):
    def __init__(self, texture, output='TEXTURE', blend_mode='NONE', stencil=False, mult=1.0, invert=False):
        self.texture    = texture
        self.output     = output
        self.blend_mode = blend_mode
        self.stencil    = stencil
        self.mult       = mult
        self.invert     = invert

    def __str__(self):
        print('Single Texture: %s' % self.texture)
        print('  Output: %s' % self.output)
        print('  Blend Mode: %s' % self.blend_mode)
        print('  Stencil: %s' % self.stencil)
        print('  Mult: %s' % self.mult)
        print('  Invert: %s' % self.invert)


class MixTexture(TextureToNode):
    def __init__(self, color1, color2, mix_map, blend_mode='NONE', output='TEXTURE'):
        self.color1  = color1
        self.color2  = color2
        self.mix_map = mix_map
        self.blend_mode = blend_mode
        self.output  = output

    def __str__(self):
        print('Mix Texture:')
        print('  Color1: %s' % self.color1)
        print('  Color2: %s' % self.color2)
        print('  Mix: %s' % self.mix_map)
        print('  Output: %s' % self.output)


class LayeredTexture(TextureToNode):
    def __init__(self, textures, blend_modes, output='TEXTURE'):
        self.textures    = textures
        self.blend_modes = blend_modes
        self.output      = output

    def __str__(self):
        print('Layered Texture')
        for i in range(self.textures):
            print('  Texture: %s'    % self.textures[i])
            print('  Blend Mode: %s' % self.blend_modes[i])

    def createNode(self, ntree, fromNode, fromSocket):
        n = _createVRayNode(ntree, "TexLayered")
        pass


def PreprocessTextures(ma, influence):
    textures = {}

    for ts in ma.texture_slots:
        if not (ts and ts.texture):
            continue

        tex = ts.texture
        if tex.type not in {'IMAGE', 'VRAY'}:
            continue

        VRayTexture = tex.vray
        VRaySlot    = tex.vray_slot

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

    processedTextures = {}

    influence = _getBrdfInfluence(ma)

    textures  = PreprocessTextures(ma, influence)
    if textures:
        print("Raw texture list:")
        pprint(textures)

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

        print("Raw texture list after prepass:")
        pprint(textures)

        # Finally blend into texlayered
        for slotType in textures.keys():
            slotTextures = textures[slotType]
            if type(slotTextures) is not list:
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

        print("Grouped texture list:")
        pprint(processedTextures)

    return processedTextures


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

def ConvertMaterial(scene, ob, ma, textures):
    VRayMaterial = ma.vray

    # This is the last node of the material
    # NOT the output, but the last Mtl node
    materialNode = None

    if not VRayMaterial.ntree:
        debug.PrintInfo("Converting material: %s" % ma.name)

        nt = _createVRayTree(ma.name, 'Material')

        outputNode = _createVRayNode(nt, 'OutputMaterial')

        materialTop = _createVRayNode(nt, 'MtlSingleBRDF')
        brdfTo      = materialTop

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
            pass

        for ovrName in MaterialOverrides:
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

        # Connect last to the output
        _connectNodes(nt,
            materialTop, 'Material',
            outputNode,  'Material')

        if 'normal' in textures:
            bumpNode = _createVRayNode(nt, 'BRDFBump')

            topBRDF = bumpNode

        # Finally generate main BRDF node
        mainBRDF = _createVRayNode(nt, VRayMaterial.type)

        # Connect last BRDF to last material
        _connectNodes(nt,
            mainBRDF, 'BRDF',
            brdfTo,   'BRDF')

        NodeTools.rearrangeTree(nt, outputNode)
        NodeTools.deselectNodes(nt)

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
    hasDisplacement = False

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

        outputNode      = _createVRayNode(nt, 'ObjectOutput')
        blenderMaterial = _createVRayNode(nt, 'BlenderOutputMaterial')

        blenderGeometry = None
        if not VRayData.override:
            blenderGeometry = _createVRayNode(nt, 'BlenderOutputGeometry')
        else:
            debug.PrintInfo("  Found geometry override '%s'" % VRayData.override_type)

        for ovrName in ObjectMaterialOverrides:
            ovrPropGroup = getattr(VRayObject, ovrName)
            ovrUse = getattr(ovrPropGroup, 'use')
            if not ovrUse:
                continue
            pass

        if hasDisplacement:
            displaceNodeType = 'GeomDisplacedMesh'
            if VRayObject.GeomStaticSmoothedMesh.use:
                displaceNodeType = 'GeomStaticSmoothedMesh'

            displaceNode = _createVRayNode(nt, displaceNodeType)

            pass

        NodeTools.rearrangeTree(nt, outputNode)

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

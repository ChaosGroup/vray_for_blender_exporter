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

import bpy
import bpy_extras

from pprint import pprint

from vb30.plugins import PLUGINS, PLUGINS_ID

from vb30.nodes import importing as NodesImport
from vb30.nodes import tools     as NodesTools

from vb30.vray_tools.VRaySceneParser import ParseVrscene
from vb30.vray_tools.VrmatParser     import ParseVrmat

from vb30 import debug


def CreateMaterial(maName, ntree, use_fake_user=True):
    ma = bpy.data.materials.new(maName)
    ma.use_fake_user = use_fake_user
    ma.vray.ntree = ntree


def ImportMaterialWithDisplacement(context, filePath, use_fake_user=True):
    debug.PrintInfo('Importing materials from "%s"' % filePath)

    vrsceneDict = {}

    if filePath.endswith(".vrscene"):
        vrsceneDict = ParseVrscene(filePath)
    else:
        vrsceneDict = ParseVrmat(filePath)

    nodeNames = []
    for pluginDesc in vrsceneDict:
        pluginID    = pluginDesc['ID']
        pluginName  = pluginDesc['Name']

        if pluginID == 'Node':
            nodeNames.append(pluginName)

    for nodeName in nodeNames:
        debug.PrintInfo("Importing material from Node: %s" % nodeName)

        nodePluginDesc = NodesImport.getPluginByName(vrsceneDict, nodeName)

        # Import material
        #
        maName = nodePluginDesc['Attributes']['material']
        if maName in bpy.data.node_groups:
            continue

        maPluginDesc = NodesImport.getPluginByName(vrsceneDict, maName)
        if not maPluginDesc:
            continue

        maNtree = bpy.data.node_groups.new(maName, type='VRayNodeTreeMaterial')
        maNtree.use_fake_user = True

        maOutputNode = maNtree.nodes.new('VRayNodeOutputMaterial')

        maNode = NodesImport.createNode(maNtree, maOutputNode, vrsceneDict, maPluginDesc)

        maNtree.links.new(
            maNode.outputs['Material'],
            maOutputNode.inputs['Material']
        )

        NodesTools.rearrangeTree(maNtree, maOutputNode)

        # Check geometry for displacement
        #
        geomName = nodePluginDesc['Attributes']['geometry']

        geomPluginDesc = NodesImport.getPluginByName(vrsceneDict, geomName)

        if geomPluginDesc and geomPluginDesc['ID'] == 'GeomDisplacedMesh':
            colorTexName = geomPluginDesc['Attributes'].get("displacement_tex_color")
            floatTexName = geomPluginDesc['Attributes'].get("displacement_tex_float")

            if colorTexName or floatTexName:
                # Create node tree with displace name
                dispNtree = bpy.data.node_groups.new(geomPluginDesc['Name'], type='VRayNodeTreeMaterial')
                dispNtree.use_fake_user = True

                # Add group output to displace tree
                dispGroupOutput = dispNtree.nodes.new('NodeGroupOutput')

                # Import texture nodes
                colorTexNode = NodesImport.FindAndCreateNode(vrsceneDict, colorTexName, dispNtree, dispGroupOutput)
                floatTexNode = NodesImport.FindAndCreateNode(vrsceneDict, floatTexName, dispNtree, dispGroupOutput)

                # Add/connect output sockets
                if colorTexName:
                    dispNtree.outputs.new('VRaySocketColor', 'Color')
                    dispNtree.links.new(
                        colorTexNode.outputs['Output'],
                        dispGroupOutput.inputs['Color']
                    )
                if floatTexName:
                    dispNtree.outputs.new('VRaySocketFloat', 'Float')
                    dispNtree.links.new(
                        floatTexNode.outputs['Output'],
                        dispGroupOutput.inputs['Float']
                    )

                NodesTools.rearrangeTree(dispNtree, dispGroupOutput)

                # Create a group node in current material tree
                # to show user that we have displacement
                dispGroupNode = maNtree.nodes.new('ShaderNodeGroup')
                dispGroupNode.node_tree = dispNtree
                dispGroupNode.location.x = 0
                dispGroupNode.location.y = 100

        # Finally create a material
        CreateMaterial(maName, maNtree, use_fake_user)

    return {'FINISHED'}


def ImportMaterials(context, filePath, baseMaterial, use_fake_user=True):
    debug.PrintInfo('Importing materials from "%s"' % filePath)

    vrsceneDict = {}

    if filePath.endswith(".vrscene"):
        vrsceneDict = ParseVrscene(filePath)
    else:
        vrsceneDict = ParseVrmat(filePath)

    MaterialTypeFilter = {
        'STANDARD' : {
            'MtlSingleBRDF',
            'MtlVRmat',
            'MtlDoubleSided',
            'MtlGLSL',
            'MtlLayeredBRDF',
            'MtlDiffuse',
            'MtlBump',
            'Mtl2Sided',
        },
        'MULTI' : {
            'MtlMulti'
        },
        'WRAPPED' : {
            'MtlWrapper',
            'MtlWrapperMaya',
            'MayaMtlMatte',
            'MtlMaterialID',
            'MtlMayaRamp',
            'MtlObjBBox',
            'MtlOverride',
            'MtlRenderStats',
            'MtlRoundEdges',
            'MtlStreakFade',
        },
    }

    # Collect material names based on selected
    # base material type
    #
    materialNames = []
    for pluginDesc in vrsceneDict:
        pluginID    = pluginDesc['ID']
        pluginName  = pluginDesc['Name']

        if pluginID in MaterialTypeFilter[baseMaterial]:
            materialNames.append(pluginName)

    for maName in materialNames:
        debug.PrintInfo("Importing material: %s" % maName)

        pluginDesc = NodesImport.getPluginByName(vrsceneDict, maName)

        ntree = bpy.data.node_groups.new(maName, type='VRayNodeTreeMaterial')
        ntree.use_fake_user = True

        outputNode = ntree.nodes.new('VRayNodeOutputMaterial')

        maNode = NodesImport.createNode(ntree, outputNode, vrsceneDict, pluginDesc)

        ntree.links.new(maNode.outputs['Material'], outputNode.inputs['Material'])

        NodesTools.rearrangeTree(ntree, outputNode)

        # Finally create a material
        CreateMaterial(maName, ntree, use_fake_user)

    return {'FINISHED'}


def ImportSettings(context, filePath, pluginFilter=None):
    debug.PrintInfo('Importing settings from "%s"' % filePath)

    vrsceneDict = ParseVrscene(filePath)

    for pluginDesc in vrsceneDict:
        pluginID    = pluginDesc['ID']
        pluginName  = pluginDesc['Name']
        pluginAttrs = pluginDesc['Attributes']

        if pluginID not in PLUGINS['SETTINGS']:
            continue

        pluginModule = PLUGINS_ID.get(pluginID)
        if pluginModule is None:
            continue

        if not hasattr(context.scene.vray, pluginID):
            continue

        propGroup = getattr(context.scene.vray, pluginID)

        for attrName in pluginAttrs:
            attrDesc  = NodesImport.getParamDesc(pluginModule.PluginParams, attrName)
            if attrDesc is None:
                continue

            attrValue = pluginAttrs[attrName]
            if attrDesc['type'] == 'ENUM':
                attrValue = str(attrValue)

            setattr(propGroup, attrName, attrValue)

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
#
class VRayOperatorImportMaterials(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname      = "vray.import_materials"
    bl_label       = "Import Materials"
    bl_description = "Import materials from *.vrscene or *.vismat file"

    # ImportHelper class uses this
    filename_ext = ".vrscene;.vismat;.vrmat"

    filter_glob = bpy.props.StringProperty(
        default = "*.vrscene;*.vismat;*.vrmat",
        options = {'HIDDEN'},
    )

    # Custom properties
    base_material = bpy.props.EnumProperty(
        name        ="Base Type",
        description ="Material type to use as material base",
        items = (
            ('STANDARD', "Standart", "Use \"VRayMtl\", \"VRMat\" as base"),
            ('MULTI',    "Multi",    "Use \"Multi\" as base"),
            ('WRAPPED',  "Wrapped",  "Use \"Wrapper\", \"Render Stats\", etc. as base"),
            ('NODE',     "Node",     "Use \"Node\" as base (will also create displacement texture groups)"),
        ),
        default = 'STANDARD',
    )

    use_fake_user = bpy.props.BoolProperty(
        name    = 'Set "Fake User" Flag',
        default = True,
    )

    def execute(self, context):
        if self.base_material == 'NODE':
            return ImportMaterialWithDisplacement(context, self.filepath, self.use_fake_user)
        return ImportMaterials(context, self.filepath, self.base_material, self.use_fake_user)


class VRayOperatorImportSettings(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname      = "vray.import_settings"
    bl_label       = "Import Settings"
    bl_description = "Import settings from *.vrscene"

    filename_ext = ".vrscene"

    filter_glob = bpy.props.StringProperty(
        default = "*.vrscene",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        return ImportSettings(context, self.filepath)


def VRayMenuItems(self, context):
    self.layout.operator(VRayOperatorImportMaterials.bl_idname, text="V-Ray: Import Materials (.vrscene/.vismat/.vrmat)")
    self.layout.operator(VRayOperatorImportSettings.bl_idname,  text="V-Ray: Import Settings (.vrscene)")


def GetRegClasses():
    return (
        VRayOperatorImportMaterials,
        VRayOperatorImportSettings,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.INFO_MT_file_import.append(VRayMenuItems)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.INFO_MT_file_import.remove(VRayMenuItems)

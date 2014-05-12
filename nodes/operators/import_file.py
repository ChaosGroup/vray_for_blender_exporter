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

from vb30.nodes import importing as NodesImport
from vb30.nodes import tools     as NodesTools

from vb30.vray_tools.VRaySceneParser import ParseVrscene


def ImportMaterials(context, filePath, baseMaterial):
    vrsceneDict = ParseVrscene(filePath)

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
        pluginDesc = NodesImport.getPluginByName(vrsceneDict, maName)

        ntree = bpy.data.node_groups.new(maName, type='VRayNodeTreeMaterial')

        outputNode = ntree.nodes.new('VRayNodeOutputMaterial')

        maNode = NodesImport.createNode(ntree, outputNode, vrsceneDict, pluginDesc)

        ntree.links.new(maNode.outputs['Material'], outputNode.inputs['Material'])

        NodesTools.rearrangeTree(ntree, outputNode)

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
#
class VRayOperatorImportMaterials(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname      = "vray.import_materials"
    bl_label       = "Import Materials"
    bl_description = "Import materials from *.vrscene or *.vismat file"

    # ImportHelper class uses this
    filename_ext = ".vrscene;.vismat"

    filter_glob = bpy.props.StringProperty(
        default = "*.vrscene;*.vismat",
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
        ),
        default = 'STANDARD',
    )

    def execute(self, context):
        return ImportMaterials(context, self.filepath, self.base_material)


def VRayMenuItemImportMaterials(self, context):
    self.layout.operator(VRayOperatorImportMaterials.bl_idname, text="V-Ray: Import Materials (.vrscene/.vismat)")


def GetRegClasses():
    return (
        VRayOperatorImportMaterials,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.INFO_MT_file_import.append(VRayMenuItemImportMaterials)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.INFO_MT_file_import.remove(VRayMenuItemImportMaterials)

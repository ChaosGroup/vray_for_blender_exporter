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


class VRAY_OT_add_world_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_world_nodetree"
    bl_label       = "Add World Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayWorld = context.world.vray

        nt = bpy.data.node_groups.new("World", type='VRayWorldNodeTree')
        nt.use_fake_user = False

        outputNode = nt.nodes.new('VRayNodeWorldOutput')
        
        VRayWorld.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_material_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_material_nodetree"
    bl_label       = "Use Nodes"
    bl_description = ""

    def execute(self, context):
        idblock = context.material

        nt = bpy.data.node_groups.new(idblock.name, type='VRayShaderTreeType')
        nt.use_fake_user = False

        outputNode = nt.nodes.new('VRayNodeOutput')

        singleMaterial = nt.nodes.new('VRayNodeMtlSingleBRDF')
        singleMaterial.location.x  = outputNode.location.x - 250
        singleMaterial.location.y += 50

        brdfVRayMtl = nt.nodes.new('VRayNodeBRDFVRayMtl')
        brdfVRayMtl.location.x  = singleMaterial.location.x - 250
        brdfVRayMtl.location.y += 100

        nt.links.new(brdfVRayMtl.outputs['BRDF'], singleMaterial.inputs['BRDF'])
                
        nt.links.new(singleMaterial.outputs['Material'], outputNode.inputs['Material'])

        idblock.vray.ntree = nt
        
        return {'FINISHED'}


class VRAY_OT_node_add_brdf_layered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_add_brdf_layered_sockets'
    bl_label       = "Add BRDFLayered Socket"
    bl_description = "Adds BRDFLayered sockets"

    def execute(self, context):
        node = context.node
        
        newIndex = int(len(node.inputs) / 2) + 1

        # BRDFLayered sockets are always in pairs
        #
        brdfSockName   = "BRDF %i" % newIndex
        weightSockName = "Weight %i" % newIndex

        node.inputs.new('VRaySocketBRDF',  brdfSockName)
        node.inputs.new('VRaySocketFloatColor', weightSockName)

        node.inputs[weightSockName].value = 1.0

        return {'FINISHED'}


class VRAY_OT_node_del_brdf_layered_sockets(bpy.types.Operator):
    bl_idname      = 'vray.node_del_brdf_layered_sockets'
    bl_label       = "Remove BRDFLayered Socket"
    bl_description = "Removes BRDFLayered socket (only not linked sockets will be removed)"

    def execute(self, context):
        node = context.node

        nSockets = len(node.inputs)

        if not nSockets:
            return {'FINISHED'}

        for i in range(nSockets-1, -1, -1):
            s = node.inputs[i]
            if not s.is_linked:
                index = re.findall(r'\d+', s.name)[0]

                brdfSockName   = "BRDF %s" % index
                weightSockName = "Weight %s" % index

                if not node.inputs[brdfSockName].is_linked and not node.inputs[weightSockName].is_linked:          
                    node.inputs.remove(node.inputs[brdfSockName])
                    node.inputs.remove(node.inputs[weightSockName])
                    break

        return {'FINISHED'}



########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ## 
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ## 
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ## 
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  #### 
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ## 

def GetRegClasses():
    return (
        VRAY_OT_node_add_brdf_layered_sockets,
        VRAY_OT_node_del_brdf_layered_sockets,
        
        VRAY_OT_add_material_nodetree,
        VRAY_OT_add_world_nodetree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

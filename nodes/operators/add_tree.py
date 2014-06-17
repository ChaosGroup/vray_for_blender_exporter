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

import os

import bpy

from .. import tree_defaults

class VRAY_OT_add_nodetree_light(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_light"
    bl_label       = "Add Light Nodetree"
    bl_description = ""

    lightType = bpy.props.StringProperty(
        name = "Light Type",
        description = "Light type",
        default = ""
    )

    def execute(self, context):
        if not self.lightType:
            return {'CANCELLED'}

        VRayLight = context.object.data.vray

        nt = bpy.data.node_groups.new(context.object.name, type='VRayNodeTreeLight')
        nt.nodes.new('VRayNode%s' % self.lightType)
        nt.use_fake_user = True

        VRayLight.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_nodetree_scene(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_scene"
    bl_label       = "Add Scene Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayScene = context.scene.vray

        nt = bpy.data.node_groups.new(context.scene.name, type='VRayNodeTreeScene')
        nt.nodes.new('VRayNodeRenderChannels')
        nt.use_fake_user = True

        VRayScene.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_nodetree_object(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_object"
    bl_label       = "Add Object Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayObject = context.object.vray

        nt = bpy.data.node_groups.new(context.object.name, type='VRayNodeTreeObject')
        nt.use_fake_user = True

        outputNode = nt.nodes.new('VRayNodeObjectOutput')

        blenderGeometry = nt.nodes.new('VRayNodeBlenderOutputGeometry')
        blenderMaterial = nt.nodes.new('VRayNodeBlenderOutputMaterial')

        blenderMaterial.location.x = outputNode.location.x - 200
        blenderMaterial.location.y = outputNode.location.y + 30

        blenderGeometry.location.x = outputNode.location.x - 200
        blenderGeometry.location.y = outputNode.location.y - 150

        nt.links.new(blenderMaterial.outputs['Material'], outputNode.inputs['Material'])
        nt.links.new(blenderGeometry.outputs['Geometry'], outputNode.inputs['Geometry'])

        VRayObject.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_world_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_world_nodetree"
    bl_label       = "Add World Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayWorld = context.world.vray

        nt = bpy.data.node_groups.new("World", type='VRayNodeTreeWorld')
        nt.use_fake_user = True

        outputNode = nt.nodes.new('VRayNodeWorldOutput')
        envNode = nt.nodes.new('VRayNodeEnvironment')

        envNode.location.x = outputNode.location.x - 200
        envNode.location.y = outputNode.location.y + 200

        nt.links.new(envNode.outputs['Environment'], outputNode.inputs['Environment'])

        VRayWorld.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_material_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_material_nodetree"
    bl_label       = "Use Nodes"
    bl_description = ""

    def execute(self, context):
        tree_defaults.AddMaterialNodeTree(context.material)

        return {'FINISHED'}


class VRAY_OT_del_nodetree(bpy.types.Operator):
    bl_idname      = "vray.del_nodetree"
    bl_label       = "Delete Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayExporter = context.scene.vray.Exporter

        selectedNodeTree = VRayExporter.ntreeListIndex
        if selectedNodeTree == -1:
            return {'CANCELLED'}

        ntree = bpy.data.node_groups[selectedNodeTree]
        ntree.use_fake_user = False
        ntree.user_clear()
        bpy.data.node_groups.remove(ntree)

        VRayExporter.ntreeListIndex -= 1
        if VRayExporter.ntreeListIndex == -1 and len(bpy.data.node_groups):
            VRayExporter.ntreeListIndex = 0

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
        VRAY_OT_add_nodetree_scene,
        VRAY_OT_add_nodetree_light,
        VRAY_OT_add_nodetree_object,
        VRAY_OT_add_material_nodetree,
        VRAY_OT_add_world_nodetree,

        VRAY_OT_del_nodetree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

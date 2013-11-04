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

import os

import bpy
from bl_operators import node as BlNode


class VRAY_OT_open_image(bpy.types.Operator):
    bl_idname      = "vray.open_image"
    bl_label       = "Open Image File"
    bl_description = "Open image file"

    filepath = bpy.props.StringProperty(
        subtype = 'FILE_PATH',
    )

    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        node = context.active_node

        if not self.filepath:
            return {'CANCELLED'}

        if not os.path.exists(self.filepath):
            return {'CANCELLED'}

        filapath, filename = os.path.split(self.filepath)
        fname, fext = os.path.splitext(filename)

        node.image = bpy.data.images.load(self.filepath)
        node.image.name = fname

        return {'FINISHED'}


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

        ntree = bpy.data.node_groups.new(context.object.name, type='VRayNodeTreeLight')
        ntree.nodes.new('VRayNode%s' % self.lightType)
        
        VRayLight.ntree = ntree

        return {'FINISHED'}


class VRAY_OT_add_nodetree_scene(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_scene"
    bl_label       = "Add Scene Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayScene = context.scene.vray

        ntree = bpy.data.node_groups.new(context.scene.name, type='VRayNodeTreeScene')
        ntree.nodes.new('VRayNodeRenderChannels')
       
        VRayScene.ntree = ntree

        return {'FINISHED'}


class VRAY_OT_add_nodetree_object(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_object"
    bl_label       = "Add Object Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayObject = context.object.vray

        nt = bpy.data.node_groups.new(context.object.name, type='VRayNodeTreeObject')

        outputNode = nt.nodes.new('VRayNodeObjectOutput')

        blenderGeometry = nt.nodes.new('VRayNodeBlenderOutputGeometry')
        blenderMaterial = nt.nodes.new('VRayNodeBlenderOutputMaterial')

        blenderGeometry.location.x = outputNode.location.x - 200
        blenderGeometry.location.y = outputNode.location.y - 50

        blenderMaterial.location.x = outputNode.location.x - 200
        blenderMaterial.location.y = outputNode.location.y + 50

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
        VRayMaterial = context.material.vray

        nt = bpy.data.node_groups.new(context.material.name, type='VRayNodeTreeMaterial')

        outputNode = nt.nodes.new('VRayNodeOutputMaterial')

        singleMaterial = nt.nodes.new('VRayNodeMtlSingleBRDF')
        singleMaterial.location.x  = outputNode.location.x - 250
        singleMaterial.location.y += 50

        brdfVRayMtl = nt.nodes.new('VRayNodeBRDFVRayMtl')
        brdfVRayMtl.location.x  = singleMaterial.location.x - 250
        brdfVRayMtl.location.y += 100

        nt.links.new(brdfVRayMtl.outputs['BRDF'], singleMaterial.inputs['BRDF'])

        nt.links.new(singleMaterial.outputs['Material'], outputNode.inputs['Material'])

        VRayMaterial.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_node(BlNode.NodeAddOperator, bpy.types.Operator):
    bl_idname      = "vray.add_node"
    bl_label       = "Add World Nodetree"
    bl_description = ""

    def create_node(self, context, node_type=None):
        node = super(VRAY_OT_add_node, self).create_node(context, node_type)

        if node.bl_idname == 'VRayNodeTexGradRamp':
            if not node.texture:
                node.texture = bpy.data.textures.new("Ramp_%s" % node.name, 'NONE')
                node.texture.use_color_ramp = True
        elif node.bl_idname == 'VRayNodeBitmapBuffer':
            if not node.texture:
                node.texture = bpy.data.textures.new("Bitmap_%s" % node.name, 'IMAGE')


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_OT_open_image,

        VRAY_OT_add_node,

        VRAY_OT_add_nodetree_scene,
        VRAY_OT_add_nodetree_light,
        VRAY_OT_add_nodetree_object,
        VRAY_OT_add_material_nodetree,
        VRAY_OT_add_world_nodetree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

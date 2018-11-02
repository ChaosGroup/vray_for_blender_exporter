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

from vb30.lib import BlenderUtils
from vb30 import debug

from ..sockets import DYNAMIC_SOCKET_CLASSES, DYNAMIC_SOCKET_OVERRIDES
from ..sockets import AddInput, AddOutput

def _redrawNodeEditor():
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            area.tag_redraw()


def SelectNtreeInEditor(context, ntreeName):
    VRayExporter = context.scene.vray.Exporter
    VRayExporter.ntreeListIndex = bpy.data.node_groups.find(ntreeName)

    _redrawNodeEditor()


class VRayOpSelectNtreeInEditor(bpy.types.Operator):
    bl_idname      = "vray.select_ntree_in_editor"
    bl_label       = "Select Node Tree In Editor"
    bl_description = "Select node tree in global editor"

    # XXX: Segfault in WM_operator_properties_default()
    # ntree = bpy.props.PointerProperty(
    #     type = bpy.types.NodeTree,
    # )
    ntree = bpy.props.StringProperty()

    def execute(self, context):
        if not self.ntree:
            return {'CANCELLED'}

        SelectNtreeInEditor(context, self.ntree)

        return {'FINISHED'}


class VRayOpShowNtree(bpy.types.Operator):
    bl_idname = "vray.show_ntree"
    bl_label = "Show Node Tree"

    data = bpy.props.EnumProperty(
        items = (
            ('MATERIAL', "Material", ""),
            ('OBJECT',   "Object",   ""),
            ('LAMP',     "Lamp",     ""),
            ('WORLD',    "World",    ""),
            ('SCENE',    "Scene",    ""),
        ),
        default = 'MATERIAL'
    )

    ntree_name = bpy.props.StringProperty()

    def execute(self, context):
        ntree = None

        ob = None
        if hasattr(context, 'active_object'):
            ob = context.active_object
        elif hasattr(context, 'object'):
            ob = context.object

        if not ob:
            return {'CANCELLED'}

        if self.data == 'MATERIAL':
            if not ob:
                self.report({'ERROR_INVALID_CONTEXT'}, "No active object!")
                return {'CANCELLED'}
            if ob.type in BlenderUtils.NonGeometryTypes:
                self.report({'ERROR_INVALID_CONTEXT'}, "Selected object type doesn't support materials!")
                return {'CANCELLED'}
            if not len(ob.material_slots):
                self.report({'ERROR_INVALID_CONTEXT'}, "Object doesn't have any material slots!")
                return {'CANCELLED'}
            ma = ob.material_slots[ob.active_material_index].material
            if ma:
                ntree = ma.vray.ntree

        elif self.data == 'OBJECT':
            if ob.type in BlenderUtils.NonGeometryTypes:
                if ob.type == 'LAMP':
                    ntree = ob.data.vray.ntree
            else:
                ntree = ob.vray.ntree

        elif self.data == 'WORLD':
            ntree = context.scene.world.vray.ntree

        elif self.data == 'SCENE':
            ntree = context.scene.vray.ntree

        if not ntree:
            if self.ntree_name and self.ntree_name in bpy.data.node_groups:
                ntree = bpy.data.node_groups[self.ntree_name]

        if not ntree:
            self.report({'ERROR'}, "Node tree not found!")
            return {'CANCELLED'}

        SelectNtreeInEditor(context, ntree.name)

        return {'FINISHED'}


def ShowNtreeItems(layout):
    layout.operator("vray.show_ntree", text="Material",        icon='MATERIAL'   ).data = 'MATERIAL'
    layout.operator("vray.show_ntree", text="Object / Lamp",   icon='OBJECT_DATA').data = 'OBJECT'
    layout.operator("vray.show_ntree", text="Environment",     icon='WORLD'      ).data = 'WORLD'
    layout.operator("vray.show_ntree", text="Render Channels", icon='SCENE_DATA' ).data = 'SCENE'


class VRayMenuShowNtree(bpy.types.Menu):
    bl_label = "Show Node Tree In Editor"
    bl_idname = "VRAY_MT_ShowNtreeMenu"

    def draw(self, context):
        ShowNtreeItems(self.layout)


class VRayPieShowNtree(bpy.types.Menu):
    bl_label = "Show Node Tree In Editor"
    bl_idname = "VRAY_MT_ShowNtreePie"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'VRayNodeTreeEditor'

    def draw(self, context):
        ShowNtreeItems(self.layout.menu_pie())


class VRayPieAddNtree(bpy.types.Menu):
    bl_label = "Add Node Tree"
    bl_idname = "VRAY_MT_AddNtreePie"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'VRayNodeTreeEditor'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("vray.add_nodetree_material",    text="Material",        icon='MATERIAL')
        pie.operator("vray.add_nodetree_object_lamp", text="Object / Lamp",   icon='OBJECT_DATA')
        pie.operator("vray.add_nodetree_world",       text="Environment",     icon='WORLD')
        pie.operator("vray.add_nodetree_scene",       text="Render Channels", icon='SCENE_DATA')


class VRayOpBitmapBufferToImageEditor(bpy.types.Operator):
    bl_idname = "vray.show_node_image"
    bl_label = "Show Bitmap Buffer Image"
    bl_options = {'UNDO'}

    def execute(self, context):
        node = context.active_node
        ob   = context.active_object
        material = ob.active_material

        if not (node and hasattr(node, 'texture') and node.texture):
            return {'CANCELLED'}

        image = node.texture.image
        update_objects = [ob]
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == material:
                    update_objects.append(obj)

        if node.bl_idname in {'VRayNodeBitmapBuffer', 'VRayNodeMetaImageTexture'}:
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = image
                    break

        for obj in update_objects:
            mesh = obj.data
            if hasattr(mesh, 'uv_textures') and mesh.uv_textures:
                for uv_face in mesh.uv_textures.active.data:
                    uv_face.image = image

        return {'FINISHED'}


class VRayOpRestoreNtreeTextures(bpy.types.Operator):
    bl_idname = "vray.restore_ntree_textures"
    bl_label = "Restore Textures"

    def execute(self, context):
        for nt in bpy.data.node_groups:
            debug.PrintInfo("Checking tree: %s..." % nt.name)
            for n in nt.nodes:
                if not hasattr(n, 'texture'):
                    continue
                if n.texture:
                    debug.PrintInfo("Texture presents: %s [\"%s\"]" % (n.texture.name, n.name))
                    continue
                if not n.texture_name:
                    debug.PrintError("Outdated node version: %s" % n.name)
                    continue
                texName = n.texture_name
                if texName not in bpy.data.textures:
                    debug.PrintInfo("Texture not found: %s" % texName)
                    continue
                n.texture = bpy.data.textures[texName]
                debug.PrintInfo("Texture restored: %s [\"%s\"]" % (texName, n.name))

        return {'FINISHED'}


class VRayOpRestoreNtreeMaterials(bpy.types.Operator):
    bl_idname = "vray.restore_ntree_materials"
    bl_label = "Restore Materials"

    def execute(self, context):
        for ma in bpy.data.materials:
            VRayMaterial = ma.vray
            if VRayMaterial.ntree:
                continue
            if ma.name in bpy.data.node_groups:
                VRayMaterial.ntree = bpy.data.node_groups[ma.name]

        return {'FINISHED'}


class VRayOpRemoveFakeTextures(bpy.types.Operator):
    bl_idname = "vray.remove_fake_textures"
    bl_label = "Clean Up Fake Data"

    def execute(self, context):
        node_textures = []
        for nt in bpy.data.node_groups:
            debug.PrintInfo("Checking tree: %s..." % nt.name)
            for n in nt.nodes:
                if not hasattr(n, 'texture'):
                    continue

                if n.texture:
                    debug.PrintInfo("Texture found: %s [\"%s\"]" % (n.texture.name, n.name))

                    if not n.texture_name:
                        debug.PrintInfo("Restoring texture name: %s [\"%s\"]" % (n.texture.name, n.name))
                        n.texture_name = n.texture.name

                    node_textures.append(n.texture)

        textures_to_remove = []
        for tex in bpy.data.textures:
            if not tex.name.startswith((".Ramp@", ".Bitmap@", ".VRayFakeTexture@")):
                continue
            if tex not in node_textures:
                tex.use_fake_user = False
                textures_to_remove.append(tex)

        for tex in textures_to_remove:
            debug.PrintInfo("Removing: %s..." % tex.name)
            bpy.data.textures.remove(tex)

        return {'FINISHED'}


class VRayOpNtreeNodeMute(bpy.types.Operator):
    bl_idname = "vray.ntree_node_mute"
    bl_label = "Toggle Mute"

    def execute(self, context):
        if hasattr(context, 'active_node'):
            node = context.active_node
            if node:
                node.mute = not node.mute
                _redrawNodeEditor()
        return {'FINISHED'}


class VRayOpNtreeSyncName(bpy.types.Operator):
    bl_label = "Sync Node Tree Name"
    bl_idname = "vray.sync_ntree_name"

    material = bpy.props.PointerProperty(type=bpy.types.Material)

    def execute(self, context):
        if self.material:
            self.material.vray.ntree.name = self.material.name
        return {'FINISHED'}


class VRayOpConvertStaticSockets(bpy.types.Operator):
    bl_idname = "vray.convert_static_sockets"
    bl_label = "Converts old style sockets with wrong min max, to the imporved new ones"

    def execute(self, context):
        for ntree in bpy.data.node_groups:
            for node in ntree.nodes:
                # custom node or not vray node
                if not hasattr(node, 'vray_plugin') and not hasattr(node, 'vray_plugins'):
                    continue

                # not a plugin node
                if node.vray_plugin == 'NONE':
                    continue

                updatedTree = False
                # get all sockets of this node, so we can re-add them to get dynamic types
                sockets = []
                for socket in node.inputs:
                    if hasattr(socket, 'vray_socket_base_type'):
                        updatedTree = True
                        break

                    value = None
                    if hasattr(socket, 'value'):
                        if socket.bl_idname in {'VRaySocketColor', 'VRaySocketVector'}:
                            value = (socket.value[0], socket.value[1], socket.value[2])
                        else:
                            value = socket.value

                    sockets.append({
                        'socketType': socket.bl_idname,
                        'socketName': socket.identifier,
                        'attrName': socket.vray_attr,
                        'default': value
                    })
                    # socket does not have dynamic type
                    if socket.bl_idname not in DYNAMIC_SOCKET_OVERRIDES:
                        continue

                if updatedTree:
                    continue

                # get all links to this node
                to_links = {}
                for link in ntree.links:
                    if link.to_node == node:
                        to_links[link.to_socket.identifier] = link.from_socket

                node.inputs.clear()

                for socket in sockets:
                    # re-create socket
                    AddInput(node, **socket)
                    # re-create links to this node's sockets
                    if socket['socketName'] in to_links:
                        ntree.links.new(
                            to_links[socket['socketName']],
                            node.inputs[socket['socketName']]
                        )
        return {'FINISHED'}



def GetRegClasses():
    return (
        VRayOpConvertStaticSockets,
        VRayOpRemoveFakeTextures,
        VRayOpRestoreNtreeTextures,
        VRayOpRestoreNtreeMaterials,

        VRayOpBitmapBufferToImageEditor,
        VRayOpSelectNtreeInEditor,

        VRayOpShowNtree,
        VRayMenuShowNtree,
        VRayPieShowNtree,
        VRayPieAddNtree,

        VRayOpNtreeNodeMute,
        VRayOpNtreeSyncName,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

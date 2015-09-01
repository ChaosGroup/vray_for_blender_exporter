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

from vb30 import proxy as ProxyUtils
from vb30.lib import BlenderUtils
from vb30.nodes import tools as NodesTools

import os

import bpy


class VRayOpSetView(bpy.types.Operator):
    bl_idname = "vray.set_view"
    bl_label = "Set View"

    view_type = bpy.props.StringProperty(default='TOP')

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type=self.view_type, align_active=False)
        return {'FINISHED'}


class VRayOpSetCamera(bpy.types.Operator):
    bl_idname = "vray.set_camera"
    bl_label = "Set Active Camera"

    camera = bpy.props.PointerProperty(type=bpy.types.Object)

    def execute(self, context):
        if self.camera:
            context.scene.camera = self.camera
            if context.area.spaces[0].region_3d.view_perspective not in {'CAMERA'}:
                bpy.ops.view3d.viewnumpad(type='CAMERA')
        return {'FINISHED'}


class VRayOpSelectCamera(bpy.types.Operator):
    bl_idname = "vray.select_camera"
    bl_label = "Select Active Camera"

    def execute(self, context):
        if context.scene.camera:
            bpy.ops.object.select_camera()
        return {'FINISHED'}


class VRayMenuActiveCamera(bpy.types.Menu):
    bl_idname = "vray.active_camera"
    bl_label = "Camera Tools"

    def draw(self, context):
        self.layout.operator('vray.flip_resolution', icon='FILE_REFRESH')
        self.layout.separator()

        self.layout.operator('vray.select_camera', text="Select Active Camera", icon='CAMERA_DATA')
        self.layout.separator()

        self.layout.operator('vray.set_view', text="Top", icon='MESH_CUBE').view_type='TOP'
        self.layout.operator('vray.set_view', text="Left", icon='MESH_CUBE').view_type='LEFT'
        self.layout.operator('vray.set_view', text="Front", icon='MESH_CUBE').view_type='FRONT'
        self.layout.separator()

        if context.active_object and context.active_object.type in {'CAMERA'}:
            self.layout.operator('vray.set_camera', text="Selected", icon='CAMERA_DATA').camera = context.active_object
            self.layout.separator()

        haveCameras = False
        for ob in context.scene.objects:
            if not ob.type in {'CAMERA'}:
                continue
            haveCameras = True
            menuItemName = ob.name
            if ob == context.scene.camera:
                menuItemName += " *"
            self.layout.operator('vray.set_camera', text=menuItemName, icon='CAMERA_DATA').camera = ob
        if not haveCameras:
            self.layout.label("No camera objects found...")


class VRayOpAddObjectProxy(bpy.types.Operator):
    bl_idname = "vray.add_object_proxy"
    bl_label = "Add V-Ray Proxy"

    filepath = bpy.props.StringProperty(name="Filepath (*.vrmesh)", subtype="FILE_PATH")
    relpath = bpy.props.BoolProperty(name="Relative Path", default=True)

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.filepath:
            return {'CANCELLED'}

        filepath = os.path.normpath(self.filepath)
        if not os.path.exists(filepath):
            self.report({'ERROR'}, "File not found!")
            return {'CANCELLED'}

        # Add new mesh object
        name = 'VRayProxy@%s' % os.path.splitext(os.path.basename(filepath))[0]

        mesh = bpy.data.meshes.new(name)
        ob = bpy.data.objects.new(name, mesh)

        context.scene.objects.link(ob)

        # Add proxy
        node_filepath = bpy.path.relpath(filepath) if self.relpath and bpy.data.filepath else filepath

        ProxyUtils.CreateProxyNodetree(ob, node_filepath)

        err = ProxyUtils.LoadProxyPreviewMesh(ob, filepath, 0, 0.0, 1.0, 0.0)
        if err is not None:
            self.report({'ERROR'}, "Error loading VRayProxy: %s!" % err)
            return {'CANCELLED'}

        BlenderUtils.SelectObject(ob)

        return {'FINISHED'}


class VRayOpAddObjectPlane(bpy.types.Operator):
    bl_idname = "vray.add_object_plane"
    bl_label = "Add V-Ray Plane"

    def execute(self, context):
        # Add simple plane
        bpy.ops.mesh.primitive_plane_add()

        ob = context.active_object
        ob.name = "VRayInfinitePlane"

        # Add V-Ray node tree
        VRayObject = ob.vray

        nt = bpy.data.node_groups.new(ob.name, type='VRayNodeTreeObject')
        nt.use_fake_user = True

        outputNode = nt.nodes.new('VRayNodeObjectOutput')

        planeGeometry   = nt.nodes.new('VRayNodeGeomPlane')
        blenderMaterial = nt.nodes.new('VRayNodeBlenderOutputMaterial')

        blenderMaterial.location.x = outputNode.location.x - 200
        blenderMaterial.location.y = outputNode.location.y + 30

        planeGeometry.location.x = outputNode.location.x - 200
        planeGeometry.location.y = outputNode.location.y - 150

        nt.links.new(blenderMaterial.outputs['Material'], outputNode.inputs['Material'])
        nt.links.new(planeGeometry.outputs['Geometry'],   outputNode.inputs['Geometry'])

        NodesTools.deselectNodes(nt)

        VRayObject.ntree = nt

        return {'FINISHED'}


class VRayMenuMesh(bpy.types.Menu):
    bl_idname = "VRayMenuMesh"
    bl_label = "V-Ray"

    def draw(self, context):
        self.layout.operator(VRayOpAddObjectProxy.bl_idname, text="V-Ray Proxy", icon='VRAY_OBJECT')
        self.layout.operator(VRayOpAddObjectPlane.bl_idname, text="V-Ray Infinite Plane", icon='VRAY_OBJECT')


def VRayMenuMeshAdd(self, context):
    self.layout.menu(VRayMenuMesh.bl_idname, icon='VRAY_LOGO_MONO')


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayOpSetCamera,
        VRayOpSetView,
        VRayOpAddObjectProxy,
        VRayOpAddObjectPlane,
        VRayOpSelectCamera,
        VRayMenuMesh,
        VRayMenuActiveCamera,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)

    bpy.types.INFO_MT_mesh_add.append(VRayMenuMeshAdd)

def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

    bpy.types.INFO_MT_mesh_add.remove(VRayMenuMeshAdd)

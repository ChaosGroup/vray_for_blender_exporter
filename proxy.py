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

import math
import os
import subprocess
import sys
import tempfile
import time

import bpy
import bmesh

from vb30.lib import BlenderUtils, PathUtils, LibUtils, SysUtils
from vb30.lib import VRayStream

from vb30.nodes import tools as NodesTools

from vb30.vray_tools import VRayProxy
from vb30 import debug
from vb30 import export as ExportTools

import _vray_for_blender_rt


def LaunchPly2Vrmesh(vrsceneFilepath, vrmeshFilepath=None, nodeName=None, frames=None, applyTm=False, useVelocity=False, previewFaces=10000):
    ply2vrmeshBin  = "ply2vrmesh{ext}"

    if sys.platform == 'win32':
        ply2vrmeshExt = ".exe"
    elif sys.platform == 'linux':
        ply2vrmeshExt = ".bin"
    else:
        ply2vrmeshExt = ".mach"

    ply2vrmeshBin = ply2vrmeshBin.format(ext=ply2vrmeshExt)

    exporterPath = SysUtils.GetAppsdkPath()
    if not exporterPath:
        return "Exporter path is not found!"

    ply2vrmesh = os.path.join(exporterPath, "bin", ply2vrmeshBin)
    if not os.path.exists(ply2vrmesh):
        return "ply2vrmesh binary not found!"

    cmd = [ply2vrmesh]
    cmd.append(vrsceneFilepath)
    if not vrmeshFilepath:
        vrmeshFilepath = vrsceneFilepath.replace('.vrscene', '.vrmesh')
    cmd.append(vrmeshFilepath)

    if previewFaces:
        cmd.append('-previewFaces')
        cmd.append('%i' % previewFaces)

    if nodeName:
        cmd.append('-vrsceneNodeName')
        cmd.append(nodeName)
    else:
        cmd.append('-vrsceneWholeScene')

    if useVelocity:
        cmd.append('-vrsceneVelocity')
    if applyTm:
        cmd.append('-vrsceneApplyTm')
    if frames is not None:
        cmd.append('-vrsceneFrames')
        cmd.append('%i-%i' % (frames[0], frames[1]))

    debug.PrintInfo("Calling: %s" % " ".join(cmd))

    err = subprocess.call(cmd)
    if err:
        return "Error generating vrmesh file!"

    return None


def LoadProxyPreviewMesh(ob, filepath, anim_type, anim_offset, anim_speed, anim_frame):
    meshFile = VRayProxy.MeshFile(filepath)

    result = meshFile.readFile()
    if result is not None:
        return "Error parsing VRayProxy file!"

    meshData = meshFile.getPreviewMesh(
        anim_type,
        anim_offset,
        anim_speed,
        anim_frame
    )

    if meshData is None:
        return "Can't find preview voxel!"

    mesh = bpy.data.meshes.new("VRayProxyPreview")
    mesh.from_pydata(meshData['vertices'], [], meshData['faces'])
    mesh.update()

    if meshData['uv_sets']:
        for uvName in meshData['uv_sets']:
            mesh.uv_textures.new(uvName)

    # Replace object mesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.to_mesh(ob.data)
    ob.data.update()

    # Remove temp
    bm.free()
    bpy.data.meshes.remove(mesh)


def CreateProxyNodetree(ob, proxyFilepath, isRelative=False):
    VRayObject = ob.vray
    if VRayObject.ntree:
        return "Node tree already exists!"

    nt = bpy.data.node_groups.new(ob.name, type='VRayNodeTreeObject')
    nt.use_fake_user = True

    outputNode = nt.nodes.new('VRayNodeObjectOutput')

    proxyGeometry   = nt.nodes.new('VRayNodeGeomMeshFile')
    blenderMaterial = nt.nodes.new('VRayNodeBlenderOutputMaterial')

    blenderMaterial.location.x = outputNode.location.x - 200
    blenderMaterial.location.y = outputNode.location.y + 30

    proxyGeometry.location.x = outputNode.location.x - 200
    proxyGeometry.location.y = outputNode.location.y - 150

    nt.links.new(blenderMaterial.outputs['Material'], outputNode.inputs['Material'])
    nt.links.new(proxyGeometry.outputs['Geometry'],   outputNode.inputs['Geometry'])

    NodesTools.deselectNodes(nt)

    proxyGeometry.GeomMeshFile.file = bpy.path.relpath(proxyFilepath) if isRelative and bpy.data.filepath else proxyFilepath

    VRayObject.ntree = nt


 #######  ########   ##        ########  ########  ######## ##     ## #### ######## ##      ##
##     ## ##     ## ####       ##     ## ##     ## ##       ##     ##  ##  ##       ##  ##  ##
##     ## ##     ##  ##        ##     ## ##     ## ##       ##     ##  ##  ##       ##  ##  ##
##     ## ########             ########  ########  ######   ##     ##  ##  ######   ##  ##  ##
##     ## ##         ##        ##        ##   ##   ##        ##   ##   ##  ##       ##  ##  ##
##     ## ##        ####       ##        ##    ##  ##         ## ##    ##  ##       ##  ##  ##
 #######  ##         ##        ##        ##     ## ########    ###    #### ########  ###  ###

def LoadVRayScenePreviewMesh(vrsceneFilepath, scene, ob):
    sceneFilepath = bpy.path.abspath(vrsceneFilepath)
    if not os.path.exists(sceneFilepath):
        return "Scene file doesn't exists!"

    sceneDirpath, sceneFullFilename = os.path.split(sceneFilepath)

    sceneFileName, sceneFileExt = os.path.splitext(sceneFullFilename)

    proxyFilepath = os.path.join(sceneDirpath, "%s.vrmesh" % sceneFileName)
    if not os.path.exists(proxyFilepath):
        return "Preview proxy file doesn't exists!"

    err = LoadProxyPreviewMesh(
        ob,
        proxyFilepath,
        '0', # TODO
        0,   # TODO
        1.0, # TODO
        scene.frame_current-1
    )

    return err


class VRayOpRotateToFlip(bpy.types.Operator):
    bl_idname      = "vray.rotate_to_flip"
    bl_label       = "Rotate Object"
    bl_description = "Rotate object to flip axis"

    def execute(self, context):
        ob = context.object

        bpy.ops.transform.rotate(value=1.5708,
            axis=(1, 0, 0),
            constraint_axis=(True, False, False),
            constraint_orientation='GLOBAL',
            mirror=False,
            proportional='DISABLED'
        )

        return {'FINISHED'}


class VRayOpVRayScenePreviewLoad(bpy.types.Operator):
    bl_idname      = "vray.vrayscene_load_preview"
    bl_label       = "Load VRayScene Preview"
    bl_description = "Loads *.vrscene preview from vrmesh file"

    def execute(self, context):
        ob = context.object
        filepath = ob.vray.VRayAsset.sceneFilepath

        err = LoadVRayScenePreviewMesh(filepath, context.scene, ob)

        if err is not None:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        return {'FINISHED'}


class VRAY_OT_proxy_load_preview(bpy.types.Operator):
    bl_idname      = "vray.proxy_load_preview"
    bl_label       = "Load Preview"
    bl_description = "Loads mesh preview from vrmesh file"

    def execute(self, context):
        GeomMeshFile  = context.node.GeomMeshFile
        proxyFilepath = bpy.path.abspath(GeomMeshFile.file)

        if not proxyFilepath:
            self.report({'ERROR'}, "Proxy filepath is not set!")
            return {'FINISHED'}

        if not os.path.exists(proxyFilepath):
            return {'FINISHED'}

        err = LoadProxyPreviewMesh(
            context.object,
            proxyFilepath,
            GeomMeshFile.anim_type,
            GeomMeshFile.anim_offset,
            GeomMeshFile.anim_speed,
            context.scene.frame_current-1
        )

        if err is not None:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        return {'FINISHED'}


 #######  ########   ##         ######  ########  ########    ###    ######## ########
##     ## ##     ## ####       ##    ## ##     ## ##         ## ##      ##    ##
##     ## ##     ##  ##        ##       ##     ## ##        ##   ##     ##    ##
##     ## ########             ##       ########  ######   ##     ##    ##    ######
##     ## ##         ##        ##       ##   ##   ##       #########    ##    ##
##     ## ##        ####       ##    ## ##    ##  ##       ##     ##    ##    ##
 #######  ##         ##         ######  ##     ## ######## ##     ##    ##    ########

class VRayOpVRayScenePreviewGenerate(bpy.types.Operator):
    bl_idname      = "vray.vrayscene_generate_preview"
    bl_label       = "Generate VRayScene Preview"
    bl_description = "Generate *.vrscene preview into vrmesh file"

    def execute(self, context):
        sce = context.scene
        ob  = context.object

        sceneFilepath = bpy.path.abspath(ob.vray.VRayAsset.sceneFilepath)
        if not sceneFilepath:
            self.report({'ERROR'}, "Scene filepath is not set!")
            return {'FINISHED'}

        LaunchPly2Vrmesh(sceneFilepath, previewFaces=ob.vray.VRayAsset.maxPreviewFaces)
        LoadVRayScenePreviewMesh(sceneFilepath, context.scene, ob)

        return {'FINISHED'}


class VRAY_OT_create_proxy(bpy.types.Operator):
    bl_idname      = "vray.create_proxy"
    bl_label       = "Create proxy"
    bl_description = "Creates proxy from selection"

    def execute(self, context):
        sce = context.scene

        # Use current active object UI for initial settings
        ob        = bpy.context.object
        selection = bpy.context.selected_objects
        oneObject = len(selection) == 1

        GeomMeshFile = ob.data.vray.GeomMeshFile

        # Create output path
        outputIsRelative = BlenderUtils.IsPathRelative(GeomMeshFile.dirpath)

        outputDirpath = BlenderUtils.GetFullFilepath(GeomMeshFile.dirpath)
        outputDirpath = PathUtils.CreateDirectory(outputDirpath)

        isDebug = debug.IsDebugMode()

        # Create tmp export file
        if isDebug:
            vrsceneOutputDir = os.path.join(outputDirpath)
        else:
            vrsceneOutputDir = os.path.join(tempfile.gettempdir())

        # Settings
        frames = None
        useAnimation = False
        if GeomMeshFile.animation != 'NONE':
            useAnimation = True
            if GeomMeshFile.animation == 'MANUAL':
                frames = (GeomMeshFile.frame_start, GeomMeshFile.frame_end)
            else:
                frames = (sce.frame_start, sce.frame_end)

        applyTm     = GeomMeshFile.apply_transforms
        useVelocity = GeomMeshFile.add_velocity

        # generate .vrmesh files
        for selectedObject in selection:
            obName = selectedObject.name
            vrsceneFilepath = os.path.join(vrsceneOutputDir, LibUtils.CleanString(obName) + '.vrscene')
            exportResult = ExportTools.nonRenderVrsceneExport(
                vrscene=vrsceneFilepath,
                useAnimation=useAnimation,
                frames=frames,
                onlySelected=True,
                objectName=obName)

            if not exportResult:
                err = 'Failed to export .vrscene for object \"%s\"' % obName
                break

            vrmeshName = LibUtils.CleanString(obName)
            if oneObject and GeomMeshFile.filename:
                vrmeshName = GeomMeshFile.filename

            if '.vrmesh' not in vrmeshName:
                vrmeshName += '.vrmesh'
            vrmeshFilepath = os.path.join(outputDirpath, vrmeshName)

            err = LaunchPly2Vrmesh(
                vrsceneFilepath=vrsceneFilepath,
                vrmeshFilepath=vrmeshFilepath,
                frames=frames,
                applyTm=applyTm,
                useVelocity=useVelocity)

            if err:
                break

            # TODO: proxy_attach_mode == THIS is not implemented
            if GeomMeshFile.proxy_attach_mode == 'NONE':
                # nothing to do with the exported .vrmesh
                continue

            attachOb = selectedObject

            if GeomMeshFile.proxy_attach_mode == 'NEW':
                newName = '%s@VRayProxy' % ob.name
                newMesh = bpy.data.meshes.new(newName)
                attachOb = bpy.data.objects.new(newName, newMesh)

                context.scene.objects.link(attachOb)

            BlenderUtils.SelectObject(attachOb)
            debug.PrintError("Replacing ob [%s] with proxy [%s]" % (obName, vrmeshFilepath))

            if GeomMeshFile.proxy_attach_mode == 'NEW':
                for slot in ob.material_slots:
                    if slot and slot.material:
                        attachOb.data.materials.append(slot.material)
                        attachOb.material_slots[-1].link     = 'OBJECT'
                        attachOb.material_slots[-1].material = slot.material

            if GeomMeshFile.apply_transforms:
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            else:
                attachOb.matrix_world = ob.matrix_world

            CreateProxyNodetree(attachOb, vrmeshFilepath, outputIsRelative)

            if GeomMeshFile.proxy_attach_mode in {'NEW', 'REPLACE'}:
                LoadProxyPreviewMesh(
                    attachOb,
                    vrmeshFilepath,
                    GeomMeshFile.anim_type,
                    GeomMeshFile.anim_offset,
                    GeomMeshFile.anim_speed,
                    context.scene.frame_current-1
                )

            # Remove temp export file
            if not isDebug:
                os.remove(vrsceneFilepath)

        if err:
            self.report({'ERROR'}, "Error generating VRayProxy! Check system console!")
            debug.PrintError(err)
            return {'CANCELLED'}

        self.report({'INFO'}, "Done creating proxy!")

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
        VRAY_OT_proxy_load_preview,
        VRAY_OT_create_proxy,

        VRayOpVRayScenePreviewLoad,
        VRayOpVRayScenePreviewGenerate,
        VRayOpRotateToFlip,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

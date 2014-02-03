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

import math
import os
import subprocess
import sys
import tempfile
import time

import bpy
import bmesh

from vb30.lib   import VRayProxy
from vb30.utils import *


def write_mesh_hq(ofile, sce, ob):
	timer= time.clock()

	debug(sce, "Generating HQ file (Frame: %i; File: %s)..." % (sce.frame_current,ofile.name))

	GeomMeshFile= ob.data.vray.GeomMeshFile

	me=  ob.to_mesh(sce, True, 'RENDER')
	dme= None

	if GeomMeshFile.animation and GeomMeshFile.add_velocity:
		if sce.frame_current != sce.frame_end:
			sce.frame_set(sce.frame_current+1)
			dme= ob.to_mesh(sce, True, 'RENDER')

	if GeomMeshFile.apply_transforms:
		me.transform(ob.matrix_world)
		if dme:
			dme.transform(ob.matrix_world)

	if dme:
		for v,dv in zip(me.vertices,dme.vertices):
			ofile.write("v=%.6f,%.6f,%.6f\n" % tuple(v.co))
			ofile.write("l=%.6f,%.6f,%.6f\n" % tuple([dc-c for c,dc in zip(v.co,dv.co)]))
	else:
		for vertex in me.vertices:
			ofile.write("v=%.6f,%.6f,%.6f\n" % tuple(vertex.co))
			ofile.write("l=0.0,0.0,0.0\n")

	face_attr = 'faces' if 'faces' in dir(me) else 'polygons'

	k= 0
	for face in getattr(me, face_attr):
		vert_order= (0,1,2,2,3,0)
		if len(face.vertices) == 4:
			ofile.write("f=%d,%d,%d;%d\n" % (face.vertices[0], face.vertices[1], face.vertices[2], face.material_index + 1))
			ofile.write("f=%d,%d,%d;%d\n" % (face.vertices[2], face.vertices[3], face.vertices[0], face.material_index + 1))
			ofile.write("fn=%i,%i,%i\n" % (k,k+1,k+2))
			ofile.write("fn=%i,%i,%i\n" % (k+3,k+4,k+5))
			k+= 6
		else:
			vert_order= (0,1,2)
			ofile.write("f=%d,%d,%d;%d\n" % (face.vertices[0], face.vertices[1], face.vertices[2], face.material_index + 1))
			ofile.write("fn=%i,%i,%i\n" % (k,k+1,k+2))
			k+= 3
		for v in vert_order:
			if face.use_smooth:
				ofile.write("n=%.6f,%.6f,%.6f\n" % tuple(me.vertices[face.vertices[v]].normal))
			else:
				ofile.write("n=%.6f,%.6f,%.6f\n" % tuple(face.normal))

	uv_textures = me.tessface_uv_textures if 'tessface_uv_textures' in dir(me) else me.uv_textures
	if len(uv_textures):
		uv_layer= uv_textures[0]
		k= 0
		for face in uv_layer.data:
			for i in range(len(face.uv)):
				ofile.write("uv=%.6f,%.6f,0.0\n" % (face.uv[i][0], face.uv[i][1]))
			if len(face.uv) == 4:
				ofile.write("uf=%i,%i,%i\n" % (k,k+1,k+2))
				ofile.write("uf=%i,%i,%i\n" % (k+2,k+3,k))
				k+= 4
			else:
				ofile.write("uf=%i,%i,%i\n" % (k,k+1,k+2))
				k+= 3
	ofile.write("\n")

	debug(sce, "Generating HQ file done [%.2f]" % (time.clock() - timer))


def generate_proxy(sce, ob, vrmesh, append=False):
	hq_file= tempfile.NamedTemporaryFile(mode='w', suffix=".hq", delete=False)
	write_mesh_hq(hq_file, sce, ob)
	hq_file.close()
	proxy_creator(hq_file.name, vrmesh, append)
	os.remove(hq_file.name)


########  ########   #######  ##     ## ##    ##
##     ## ##     ## ##     ##  ##   ##   ##  ##
##     ## ##     ## ##     ##   ## ##     ####
########  ########  ##     ##    ###       ##
##        ##   ##   ##     ##   ## ##      ##
##        ##    ##  ##     ##  ##   ##     ##
##        ##     ##  #######  ##     ##    ##

class VRAY_OT_proxy_load_preview(bpy.types.Operator):
	bl_idname      = "vray.proxy_load_preview"
	bl_label       = "Load Preview"
	bl_description = "Loads mesh preview from vrmesh file"

	def execute(self, context):
		proxyFilepath = bpy.path.abspath(context.node.GeomMeshFile.file)

		if not proxyFilepath:
			self.report({'ERROR'}, "Proxy filepath is not set!")
			return {'FINISHED'}

		if not os.path.exists(proxyFilepath):
			self.report({'ERROR'}, "Proxy filepath does not exist!")
			return {'FINISHED'}

		meshFile = VRayProxy.MeshFile(proxyFilepath)
		result = meshFile.readFile()

		if result is not None:
			self.report({'ERROR'}, "Error parsing VRayProxy file!")
			return {'FINISHED'}

		previewVoxel = meshFile.getVoxelByType(VRayProxy.MVF_PREVIEW_VOXEL)

		if not previewVoxel:
			self.report({'ERROR'}, "Can't find preview voxel!")
			return {'FINISHED'}

		vertices = previewVoxel.getVertices()
		faces    = previewVoxel.getFaces()

		mesh = bpy.data.meshes.new("VRayProxyPreview")
		mesh.from_pydata(vertices, [], faces)
		mesh.update()

		# Replace object mesh
		bm = bmesh.new()
		bm.from_mesh(mesh)
		bm.to_mesh(context.object.data)

		context.object.data.update()

		# Remove temp
		bm.free()
		bpy.data.meshes.remove(mesh)

		return {'FINISHED'}


class VRAY_OT_create_proxy(bpy.types.Operator):
	bl_idname      = "vray.create_proxy"
	bl_label       = "Create proxy"
	bl_description = "Creates proxy from selection"

	def execute(self, context):
		sce = context.scene

		VRayScene    = sce.vray
		VRayExporter = VRayScene.Exporter

		def _create_proxy(ob):
			if ob.type in ('LAMP','CAMERA','ARMATURE','LATTICE','EMPTY'):
				return

			timer= time.clock()

			GeomMeshFile= ob.data.vray.GeomMeshFile

			vrmesh_filename= GeomMeshFile.filename if GeomMeshFile.filename else clean_string(ob.name)
			vrmesh_filename+= ".vrmesh"

			vrmesh_dirpath= bpy.path.abspath(GeomMeshFile.dirpath)
			if not os.path.exists(vrmesh_dirpath):
				os.mkdir(vrmesh_dirpath)
			vrmesh_filepath= os.path.join(vrmesh_dirpath,vrmesh_filename)

			if GeomMeshFile.animation:
				selected_frame= sce.frame_current

				frame_start= sce.frame_start
				frame_end= sce.frame_end
				if GeomMeshFile.animation_range == 'MANUAL':
					frame_start= GeomMeshFile.frame_start
					frame_end= GeomMeshFile.frame_end

				# Export first frame to create file
				frame= frame_start
				sce.frame_set(frame)
				generate_proxy(sce,ob,vrmesh_filepath)
				frame+= 1
				# Export all other frames
				while(frame <= frame_end):
					sce.frame_set(frame)
					generate_proxy(sce,ob,vrmesh_filepath,append=True)
					frame+= 1
				sce.frame_set(selected_frame)

			else:
				if VRayExporter.experimental:
					bpy.ops.vray.generate_vrayproxy(
						filepath = vrmesh_filepath,
					)
				else:
					generate_proxy(sce,ob,vrmesh_filepath)

			# ob_name= ob.name
			# ob_data_name= ob.data.name

			# VRayMesh= ob.data.vray

			# if GeomMeshFile.mode != 'NONE':
			# 	if GeomMeshFile.mode in ('THIS','REPLACE'):
			# 		if GeomMeshFile.add_suffix:
			# 			ob.name+= '_proxy'
			# 			ob.data.name+= '_proxy'

			# 	if GeomMeshFile.mode == 'THIS':
			# 		VRayMesh.override= True
			# 		VRayMesh.override_type= 'VRAYPROXY'
			# 		GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)

			# 	bbox_faces= ((0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7))
			# 	bbox_mesh= bpy.data.meshes.new(ob_data_name+'_proxy')
			# 	bbox_mesh.from_pydata(ob.bound_box, [], bbox_faces)
			# 	bbox_mesh.update()

			# 	if GeomMeshFile.mode in ('NEW','REPLACE'):
			# 		for slot in ob.material_slots:
			# 			if slot and slot.material:
			# 				bbox_mesh.materials.append(slot.material)

			# 	if GeomMeshFile.mode == 'NEW':
			# 		new_ob= bpy.data.objects.new(ob_name+'_proxy', bbox_mesh)
			# 		sce.objects.link(new_ob)
			# 		new_ob.matrix_world= ob.matrix_world
			# 		new_ob.draw_type= 'WIRE'
			# 		bpy.ops.object.select_all(action='DESELECT')
			# 		new_ob.select= True
			# 		sce.objects.active= new_ob

			# 		if GeomMeshFile.apply_transforms:
			# 			ob.select= True
			# 			sce.objects.active= ob
			# 			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

			# 		VRayMesh= new_ob.data.vray
			# 		VRayMesh.override= True
			# 		VRayMesh.override_type= 'VRAYPROXY'

			# 		GeomMeshFile= VRayMesh.GeomMeshFile
			# 		GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)

			# 	elif GeomMeshFile.mode == 'REPLACE':
			# 		bm = bmesh.new()
			# 		bm.from_mesh(bbox_mesh)
			# 		bm.to_mesh(ob.data)
			# 		bm.free()

			# 		ob.draw_type = 'WIRE'
			# 		for md in ob.modifiers: ob.modifiers.remove(md)

			# 		if GeomMeshFile.apply_transforms:
			# 			ob.select= True
			# 			sce.objects.active= ob
			# 			bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

			# 		VRayMesh= ob.data.vray
			# 		VRayMesh.override= True
			# 		VRayMesh.override_type= 'VRAYPROXY'

			# 		GeomMeshFile= VRayMesh.GeomMeshFile
			# 		GeomMeshFile.file= bpy.path.relpath(vrmesh_filepath)
			debug(context.scene, "Proxy generation total time: %.2f\n" % (time.clock() - timer))

		if len(bpy.context.selected_objects):
			for ob in bpy.context.selected_objects:
				_create_proxy(ob)
		else:
			_create_proxy(context.object)

		return {'FINISHED'}


def GetRegClasses():
	return (
		VRAY_OT_proxy_load_preview,
		VRAY_OT_create_proxy,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

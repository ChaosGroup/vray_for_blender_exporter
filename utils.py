'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Python modules  '''
import filecmp
import math
import os
import random
import shutil
import string
import socket
import subprocess
import sys
import time
import tempfile

''' Blender modules '''
import bpy
import mathutils

''' vb modules '''
from vb25.plugins import *

PLATFORM= sys.platform
HOSTNAME= socket.gethostname()

TEX_TYPES= ('IMAGE', 'VRAY')

try:
	none_matrix= mathutils.Matrix(((0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0)))
except:
	none_matrix= mathutils.Matrix((0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0))

def color(text, color=None):
	if not color or not PLATFORM == 'linux2':
		return text
	if color == 'green':
		return "\033[0;32m%s\033[0m" % text
	elif color == 'red':
		return "\033[0;31m%s\033[0m" % text
	elif color == 'yellow':
		return "\033[0;33m%s\033[0m" % text
	else:
		return text

def get_plugin_property(rna_pointer, property):
	return rna_pointer.get(property, getattr(rna_pointer, property))

# The most powerfull unique name generator =)
def get_random_string():
	return ''.join([random.choice(string.ascii_letters) for x in range(16)])

def debug(scene, message, newline= True, cr= True, error= False):
	# sys.stdout.write("[%s] V-Ray/Blender: %s%s%s" % (
	# 	time.strftime("%Y/%b/%d|%H:%m:%S"),
	# 	color("Error! ", 'red') if error else '',
	# 	message,
	# 	'\n' if newline else '\r' if cr else '')
	# )
	sys.stdout.write("V-Ray/Blender: %s%s%s" % (
		color("Error! ", 'red') if error else '',
		message,
		'\n' if newline else '\r' if cr else '')
	)
	if not newline:
		sys.stdout.flush()

def p(t):
	if type(t) == bool:
		return "%i"%(t)
	elif type(t) == int:
		return "%i"%(t)
	elif type(t) == float:
		return "%.6f"%(t)
	elif type(t) == mathutils.Vector:
		return "Vector(%.3f,%.3f,%.3f)"%(t.x,t.y,t.z)
	elif type(t) == mathutils.Color:
		return "Color(%.3f,%.3f,%.3f)"%(t.r,t.g,t.b)
	elif type(t) == str:
		if t == "True":
			return "1"
		elif t == "False":
			return "0"
		else:
			return t
	else:
		return "%s"%(t)

def a(scene, t):
	if scene.vray.exporter.animation:
		return "interpolate((%i,%s))" % (scene.frame_current, p(t))
	else:
		return p(t)

def transform(m):
	return "Transform(\n\t\tMatrix(\n\t\t\tVector(%f, %f, %f),\n\t\t\tVector(%f, %f, %f),\n\t\t\tVector(%f, %f, %f)\n\t\t),\n\t\tVector(%f, %f, %f))"\
            %(m[0][0], m[0][1], m[0][2],\
              m[1][0], m[1][1], m[1][2],\
              m[2][0], m[2][1], m[2][2],\
              m[3][0], m[3][1], m[3][2])

def clean_string(s):
	s= s.replace("+", "p")
	s= s.replace("-", "m")
	for i in range(len(s)):
		c= s[i]
		if not ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')):
			s= s.replace(c, "_")
	return s

def get_uv_layer_id(uv_layers, uv_layer_name):
	if uv_layer_name == "":
		return 1
	return uv_layers[uv_layer_name] if uv_layer_name in uv_layers else 1

def get_uv_layers(sce):
	uv_layers= {}
	uv_id= 1
	for ma in bpy.data.materials:
		for slot in ma.texture_slots:
			if slot and slot.texture:
				if slot.texture.vray.texture_coords == 'UV':
					if slot.uv_layer and slot.uv_layer not in uv_layers:
						uv_layers[slot.uv_layer]= uv_id
						uv_id+= 1

	if sce.vray.exporter.debug:
		for uv_layer in uv_layers:
			debug(sce, "UV layer name map: \"%s\" => %i" % (uv_layer, uv_layers[uv_layer]))

	return uv_layers

def get_uv_layers_map(sce):
	uv_layers= {}
	uv_id= 1
	for ma in bpy.data.materials:
		for slot in ma.texture_slots:
			if slot and slot.texture:
				if slot.texture.vray.texture_coords == 'UV':
					if slot.uv_layer and slot.uv_layer not in uv_layers:
						uv_layers[slot.uv_layer]= uv_id
						uv_id+= 1

	if sce.vray.exporter.debug:
		for uv_layer in uv_layers:
			debug(sce, "UV layer name map: \"%s\" => %i" % (uv_layer, uv_layers[uv_layer]))

	return uv_layers

def generate_object_list(object_names_string= None, group_names_string= None):
	object_list= []

	if object_names_string:
		ob_names= object_names_string.split(';')
		for ob_name in ob_names:
			if ob_name in bpy.data.objects:
				object_list.append(bpy.data.objects[ob_name])

	if group_names_string:
		gr_names= group_names_string.split(';')
		for gr_name in gr_names:
			if gr_name in bpy.data.groups:
				object_list.extend(bpy.data.groups[gr_name].objects)

	return object_list

# def get_name(data, bus):
# 	name= data.name
# 	if bus['object']['particle'].get('name'):
# 		name= "%s_%s" % (bus['object']['particle']['name'], name)
# 	if bus['object']['dupli'].get('name'):
# 		name= "%s_%s" % (bus['object']['dupli']['name'], name)
# 	if issubclass(type(data), bpy.types.Lamp):
# 		name= 'LA'+name
# 	elif issubclass(type(data), bpy.types.Texture):
# 		name= 'TE'+name
# 	elif type(data) == bpy.types.Material:
# 		name= 'MA'+name
# 	else:
# 		name= 'OB'+name
# 	if data.library:
# 		name+= "%s%s" % ('LI', get_filename(data.library.filepath))
# 	return clean_string(name)

def get_name(ob, prefix= None):
	name= ob.name
	if prefix:
		name= prefix+name
	if ob.library:
		name+= "%s%s" % ('LI', get_filename(ob.library.filepath))
	return clean_string(name)

def get_data_by_name(sce, data_type, name):
	if data_type == 'objects':
		if name in sce.objects:
			return sce.objects[name]
	elif data_type in ('textures','materials','meshes'):
		if name in bpy.data[data_type]:
			return bpy.data[data_type][name]
	return None

def get_filename(filepath):
	return os.path.split(bpy.path.abspath(filepath))[1]

def get_full_filepath(sce,ob,filepath):
	def rel_path(filepath):
		if filepath[:2] == "//":
			return True
		else:
			return False

	VRayDR= sce.vray.VRayDR

	if ob.library and filepath[:2] == '//':
		lib_path= os.path.dirname(bpy.path.abspath(ob.library.filepath))
		filepath= os.path.normpath(os.path.join(lib_path,filepath[2:]))

	src_file= os.path.normpath(bpy.path.abspath(filepath))

	if PLATFORM != 'win32':
		src_file= src_file.replace('\\','/')

	src_filename= os.path.split(src_file)[1]

	if VRayDR.on:
		dest_path= os.path.normpath(bpy.path.abspath(VRayDR.shared_dir))

		if dest_path == "":
			return src_file
		
		blendfile_name= os.path.split(bpy.data.filepath)[1][:-6]

		dest_path= os.path.join(dest_path, blendfile_name + os.sep)
		if not os.path.exists(dest_path):
			os.mkdir(dest_path)

		dest_file= os.path.join(dest_path,src_filename)
		if os.path.isfile(src_file):
			if os.path.exists(dest_file):
				if not filecmp.cmp(dest_file,src_file):
					debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
					shutil.copy(src_file,dest_path)
			else:
				debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
				shutil.copy(src_file,dest_path)

		if VRayDR.type == 'UU':
			return dest_file
		elif VRayDR.type == 'WU':
			return "..%s%s%s%s"%(os.sep, blendfile_name, os.sep, src_filename)
		else:
			return "//%s/%s"%(HOSTNAME, rel_path)

	return src_file

def get_render_file_format(VRayExporter, file_format):
	if VRayExporter.image_to_blender:
		return 'exr'
	if file_format in ('JPEG','JPEG2000'):
		file_format= 'jpg'
	elif file_format in ('OPEN_EXR','IRIS','CINEON'):
		file_format= 'exr'
	elif file_format == 'MULTILAYER':
		file_format= 'vrimg'
	elif file_format in ('TARGA', 'TARGA_RAW'):
		file_format= 'tga'
	else:
		file_format= 'png'
	return file_format.lower()
	
def object_on_visible_layers(sce,ob):
	for l in range(20):
		if ob.layers[l] and sce.layers[l]:
			return True
	return False

def get_distance(ob1, ob2):
	p1= ob1.matrix_world[3]
	p2= ob2.matrix_world[3]
	vec= p1 - p2
	return vec.length

def proxy_creator(hq_filepath, vrmesh_filepath, append= False):
	pc_binary= "vb_proxy"
	if PLATFORM == 'win32':
		pc_binary+= ".exe"
	if get_vray_exporter_path():
		p= os.path.join(get_vray_exporter_path(),pc_binary)
		if os.path.exists(p):
			pc_binary= p

	params= []
	params.append(pc_binary)
	if append:
		params.append('--append')
	params.append(hq_filepath)
	params.append(vrmesh_filepath)

	os.system(' '.join(params))

def get_vray_exporter_path():
	for vb_path in bpy.utils.script_paths(os.path.join('io','vb25')):
		if vb_path:
			return vb_path
	return ''

def get_vray_standalone_path(sce):
	VRayExporter= sce.vray.exporter

	vray_bin= "vray"
	if PLATFORM == 'win32':
		vray_bin+= ".exe"

	def get_env_paths(var):
		split_char= ':'
		if PLATFORM == 'win32':
			split_char= ';'
		env_var= os.getenv(var)
		if env_var:
			return env_var.replace('\"','').split(split_char)
		return []

	def find_vray_binary(paths):
		if paths:
			for p in paths:
				if p:
					vray_path= os.path.join(p,vray_bin)
					if os.path.exists(vray_path):
						debug(sce, "V-Ray found in: %s" % (vray_path))
						return vray_path
		return None

	if not VRayExporter.detect_vray and VRayExporter.vray_binary:
		return bpy.path.abspath(VRayExporter.vray_binary)

	vray_standalone_paths= get_env_paths('VRAY_PATH')
	if vray_standalone_paths:
		vray_standalone= find_vray_binary(vray_standalone_paths)
		if vray_standalone:
			return vray_standalone

	search_paths= []
	for maya in ('2011','2010','2009','2008'):
		for arch in ('x64','x86'):
			env_var= "VRAY_FOR_MAYA%s_MAIN_%s"%(maya,arch)
			debug(sce, "Searching in: %s" % (env_var))
			vray_maya= find_vray_binary([os.path.join(p,'bin') for p in get_env_paths(env_var)])
			if vray_maya:
				return vray_maya

	debug(sce, "V-Ray not found! Trying to start \"%s\" command from $PATH..." % (vray_bin), True)

	return vray_bin

def get_filenames(scene, filetype):
	def create_dir(directory):
		if not os.path.exists(directory):
			debug(scene, "Path \"%s\" doesn't exist, trying to create... " % directory)
			try:
				os.mkdir(directory)
				debug(scene, "Path \"%s\" doesn't exist, trying to create... done." % directory)
			except:
				directory= tempfile.gettempdir()
				debug(scene, "Directory creation failed!")
				debug(scene, "Using default exporting path: %s" % directory)
		return directory

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter
	VRayDR=       VRayScene.VRayDR
	
	(blendfile_path, blendfile_name)= os.path.split(bpy.data.filepath)

	# Blend-file name without extension
	blendfile_name= blendfile_name[:-6]

	# Default export directory is system's %TMP%
	default_dir= tempfile.gettempdir()

	# Export directory
	export_dir= default_dir
	export_file= blendfile_name if VRayExporter.output_unique else 'scene'

	if VRayDR.on:
		export_dir= os.path.join(
			bpy.path.abspath(VRayDR.shared_dir),
			blendfile_name + os.sep
		)
	else:
		if VRayExporter.output == 'USER':
			if VRayExporter.output_dir:
				export_dir= bpy.path.abspath(VRayExporter.output_dir)
			else:
				export_dir= default_dir
		elif VRayExporter.output == 'SCENE':
			export_dir= blendfile_path

		if VRayExporter.output != 'USER':
			export_dir= os.path.join(export_dir,"vb25")

	filepath=  default_dir if blendfile_name == 'startup' else export_dir

	if filetype in ('scene', 'materials', 'lights', 'nodes', 'camera', 'environment'):
		filepath= os.path.join(create_dir(export_dir), "%s_%s.vrscene" % (export_file,filetype))

	elif filetype == 'geometry':
		filepath= os.path.join(create_dir(export_dir), "%s_geometry_00.vrscene" % (export_file))

	elif filetype == 'lightmaps':
		filepath= create_dir(os.path.join(export_dir,filetype))

	elif filetype == 'output':
		if blendfile_name == 'startup':
			filepath= create_dir(export_dir)
		else:
			filepath= create_dir(bpy.path.abspath(scene.render.filepath))

	# debug(scene, "%s: %s" % (filetype.capitalize(), filepath))

	return filepath


def print_dict(scene, title, params):
	debug(scene, "%s:" % title)
	for key in params:
		if type(params[key]) == dict:
			print_dict(scene, key, params[key])
		elif type(params[key]) in (list,tuple):
			debug(scene, "    %s" % (key))
			for item in params[key]:
				debug(scene, item)
		else:
			debug(scene, "  %s: %s" % (key, params[key]))

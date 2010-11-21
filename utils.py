'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Python modules  '''
import os
import sys
import tempfile
import math
import subprocess
import time
import shutil
import filecmp
import socket

''' Blender modules '''
import bpy
import mathutils


PLATFORM= sys.platform
HOSTNAME= socket.gethostname()

none_matrix= mathutils.Matrix(
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0]
)

def	debug(sce, s):
	ve= sce.vray.exporter
	if ve.debug:
		print("V-Ray/Blender: %s"%(s))

def p(t):
	if type(t) == type(True):
		return "%i"%(t)
	elif type(t) == type(1):
		return "%i"%(t)
	elif type(t) == type(1.0):
		return "%.6f"%(t)
	elif str(type(t)) == "<class 'color'>":
		return "Color(%.3f,%.3f,%.3f)"%(tuple(t))
	elif str(type(t)) == "<class 'vector'>":
		return "Color(%.3f,%.3f,%.3f)"%(tuple(t))
	elif type(t) == type(""):
		if(t == "True"):
			return "1"
		elif(t == "False"):
			return "0"
		else:
			return t
	else:
		return "%s"%(t)

def a(sce,t):
	return "interpolate((%i,%s))"%(sce.frame_current,p(t))

def transform(m):
	return "Transform(Matrix(Vector(%f, %f, %f),Vector(%f, %f, %f),Vector(%f, %f, %f)),Vector(%f, %f, %f))"\
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

def rel_path(filepath):
	if filepath[:2] == "//":
		return True
	else:
		return False

def get_filename(fn):
	(filepath, filename)= os.path.split(bpy.path.abspath(fn))
	return filename

def get_full_filepath(sce,filepath):
	VRayDR= sce.vray.VRayDR

	src_file= os.path.normpath(bpy.path.abspath(filepath))
	src_filename= os.path.split(src_file)[1]

	if VRayDR.on:
		dest_path= bpy.path.abspath(VRayDR.shared_dir)
		if dest_path == "":
			return src_file
		blendfile_name= os.path.split(bpy.data.filepath)[1][:-6]

		dest_path= os.path.join(dest_path, blendfile_name + os.sep)
		if not os.path.exists(dest_path):
			os.mkdir(dest_path)

		rel_path= blendfile_name + os.sep + src_filename

		dest_file= os.path.join(dest_path,src_filename)
		if os.path.isfile(src_file):
			if os.path.exists(dest_file):
				if not filecmp.cmp(dest_file,src_file):
					debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
					shutil.copy(src_file,dest_path)
			else:
				debug(sce,"Copying \"%s\" to \"%s\"..."%(src_filename,dest_path))
				shutil.copy(src_file,dest_path)

		if VRayDR.type in ('UU','WU'):
			return "..%s%s"%(os.sep,rel_path)
		else:
			return "//%s/%s"%(HOSTNAME,rel_path)

	return src_file

def get_render_file_format(ve,file_format):
	if ve.image_to_blender:
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
	
def get_name(data, prefix= None, dupli_name= None):
	name= data.name
	if dupli_name:
		name= "%s_%s"%(dupli_name,name)
	if prefix:
		name= "%s_%s"%(prefix,name)
	if data.library:
		name+= "_%s"%(get_filename(data.library.filepath))
	return clean_string(name)

def object_on_visible_layers(sce,ob):
	for l in range(20):
		if ob.layers[l] and sce.layers[l]:
			return True
	return False

def vb_script_path():
	for vb_path in bpy.utils.script_paths(os.path.join('io','vb25')):
		if vb_path:
			return vb_path
	return ''

def proxy_creator(hq_filepath, vrmesh_filepath, append= False):
	pc_binary= "proxy_converter"
	if PLATFORM == 'win32':
		pc_binary+= ".exe"
	if vb_script_path():
		p= os.path.join(vb_script_path(),'bin',pc_binary)
		if os.path.exists(p):
			pc_binary= p

	params= []
	params.append(pc_binary)
	if append:
		params.append('--append')
	params.append(hq_filepath)
	params.append(vrmesh_filepath)

	os.system(' '.join(params))

def vb_binary_path(sce):
	vray_bin= "vray"
	if PLATFORM == 'win32':
		vray_bin+= ".exe"
	vray_path= vray_bin

	VRayExporter= sce.vray.exporter
	if not VRayExporter.detect_vray:
		if VRayExporter.vray_binary == "":
			debug(sce,"V-Ray binary is not set!")
			return vray_bin
		else:
			return bpy.path.abspath(VRayExporter.vray_binary)
	
	vray_env_path= os.getenv('VRAY_PATH')

	if vray_env_path is None:
		for maya in ('2011','2010','2009','2008'):
			for arch in ('x64','x86'):
				vray_env_path= os.getenv("VRAY_FOR_MAYA%s_MAIN_%s"%(maya,arch))
				if vray_env_path:
					break
			if vray_env_path:
				break
		if vray_env_path:
			vray_env_path= os.path.join(vray_env_path,'bin')

	if vray_env_path:
		if PLATFORM == "win32":
			if vray_env_path[0:1] == ";":
				vray_env_path= vray_env_path[1:]
			if vray_env_path[0:1] == "\"":
				vray_env_path= vray_env_path[1:-1]
		else:
			if vray_env_path[0:1] == ":":
				vray_env_path= vray_env_path[1:]
		vray_path=  os.path.join(vray_env_path, vray_bin)

	return vray_path

def get_plugin(plugins, plugin_id):
	for plugin in plugins:
		if plugin.ID == plugin_id:
			return plugin
	return None

def get_filenames(sce, filetype):
	def create_dir(directory):
		if not os.path.exists(directory):
			print("V-Ray/Blender: Path doesn't exist, trying to create...")
			print("V-Ray/Blender: Creating directory: %s"%(directory))
			try:
				os.mkdir(directory)
			except:
				print("V-Ray/Blender: Creating directory \"%s\" failed!"%(directory))
				directory= tempfile.gettempdir()
				print("V-Ray/Blender: Using default exporting path: \"%s\""%(directory))
		return directory

	ve= sce.vray.exporter
	VRayDR= sce.vray.VRayDR
	
	(blendfile_path, blendfile_name)= os.path.split(bpy.data.filepath)
	blendfile_name= blendfile_name[:-6]

	default_dir= tempfile.gettempdir()
	export_dir= default_dir

	export_file= 'scene'
	if ve.output_unique:
		export_file= blendfile_name

	if VRayDR.on:
		export_dir= os.path.join(bpy.path.abspath(VRayDR.shared_dir), blendfile_name + os.sep)
	else:
		if ve.output == 'USER':
			if ve.output_dir == "":
				export_dir= default_dir
			else:
				export_dir= bpy.path.abspath(ve.output_dir)
		elif ve.output == 'SCENE':
			export_dir= blendfile_path

		if ve.output != 'USER':
			export_dir= os.path.join(export_dir,"vb25")

	filepath= export_dir

	if filetype in ('scene', 'geometry', 'materials', 'lights', 'nodes', 'camera'):
		filepath= os.path.join(create_dir(export_dir), "%s_%s.vrscene" % (export_file,filetype))

	elif filetype == 'lightmaps':
		filepath= create_dir(os.path.join(export_dir,filetype))

	elif filetype == 'output':
		if blendfile_name == 'startup.blend':
			filepath= create_dir(export_dir)
		else:
			filepath= create_dir(bpy.path.abspath(sce.render.filepath))

	debug(sce,"Filepath (%s): %s" % (filetype,filepath))

	return filepath

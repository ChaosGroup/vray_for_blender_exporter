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


TEX_TYPES= ('IMAGE', 'VRAY')


MODULES= {
	'SettingsRaycaster': (
		'maxLevels',
		'minLeafSize',
		'faceLevelCoef',
		'dynMemLimit',
	),
	
	'SettingsUnitsInfo': (
		'meters_scale',
		'photometric_scale'
	),

	'SettingsDMCSampler': (
		'time_dependent',
		'adaptive_amount',
		'adaptive_threshold',
		'adaptive_min_samples',
		'subdivs_mult'
	),

	'SettingsImageSampler': (
		'fixed_subdivs',
		'dmc_minSubdivs',
		'dmc_threshold',
		'dmc_show_samples',
		'subdivision_minRate',
		'subdivision_maxRate',
		'subdivision_threshold',
		'subdivision_edges',
		'subdivision_normals',
		'subdivision_normals_threshold',
		'subdivision_jitter',
		'subdivision_show_samples'
	),

	'SettingsColorMapping': (
		'affect_background',
		'dark_mult',
		'bright_mult',
		'gamma',
		'subpixel_mapping',
		'clamp_output',
		'clamp_level',
		'adaptation_only',
		'linearWorkflow'
	),

	'SettingsDefaultDisplacement': (
		'override_on',
		'edgeLength',
		'viewDependent',
		'maxSubdivs',
		'tightBounds',
		'amount',
		'relative'
	),
	
	'SettingsRegionsGenerator': (
        'xc',
        'yc',
        # 'xymeans',
        # 'seqtype',
        'reverse'
	)
}


PLATFORM= sys.platform
HOSTNAME= socket.gethostname()

none_matrix= mathutils.Matrix(
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0],
	[0.0,0.0,0.0]
)

def color(text, color=None):
	if not color or PLATFORM == 'win32':
		return text
	if color == 'green':
		return "\033[0;32m%s\033[0m" % text
	elif color == 'red':
		return "\033[0;31m%s\033[0m" % text
	elif color == 'yellow':
		return "\033[0;33m%s\033[0m" % text
	else:
		return text

# The most powerfull unique name generator =)
def get_random_string():
	return ''.join([random.choice(string.ascii_letters) for x in range(16)])

def	debug(sce, s, error= False):
	if sce.vray.exporter.debug:
		out= color("V-Ray/Blender: ", 'green')
		if error: out+= color("Error! ", 'red')
		out+= "%s"%(s)
		print("%s"%(out))

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

def a(sce,t):
	return "interpolate((%i,%s))"%(sce.frame_current,p(t))

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

def rel_path(filepath):
	if filepath[:2] == "//":
		return True
	else:
		return False

def get_uv_layer_id(sce, uv_layers, uv_layer_name):
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
			print("UV Layer: %s => %i" % (uv_layer, uv_layers[uv_layer]))

	return uv_layers

def get_data_by_name(sce, data, name):
	if data == 'objects':
		if name in sce.objects:
			return sce.objects[name]
	elif data in ('textures','materials','meshes'):
		if name in bpy.data[data]:
			return bpy.data[data][name]
	return None

def get_filename(fn):
	(filepath, filename)= os.path.split(bpy.path.abspath(fn))
	return filename

def get_full_filepath(sce,ob,filepath):
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
	pc_binary= "vb_proxy"
	if PLATFORM == 'win32':
		pc_binary+= ".exe"
	if vb_script_path():
		p= os.path.join(vb_script_path(),pc_binary)
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

def get_plugin(plugins, plugin_id):
	for plugin in plugins:
		if plugin.ID == plugin_id:
			return plugin
	return None

def get_filenames(sce, filetype):
	def create_dir(directory):
		if PLATFORM != 'win32':
			directory= directory.replace('\\','/')
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

	if filetype in ('scene', 'materials', 'lights', 'nodes', 'camera'):
		filepath= os.path.join(create_dir(export_dir), "%s_%s.vrscene" % (export_file,filetype))

	elif filetype == 'geometry':
		filepath= os.path.join(create_dir(export_dir), "%s_geometry_00.vrscene" % (export_file))

	elif filetype == 'lightmaps':
		filepath= create_dir(os.path.join(export_dir,filetype))

	elif filetype == 'output':
		if blendfile_name == 'startup.blend':
			filepath= create_dir(export_dir)
		else:
			filepath= create_dir(bpy.path.abspath(sce.render.filepath))

	debug(sce,"Filepath (%s): %s" % (filetype,filepath))

	return filepath


CONVERT_BLEND_TYPE= {
	'MIX':          'OVER',
	'SCREEN':       'OVER',
	'DIVIDE':       'OVER',
	'HUE':          'OVER',
	'VALUE':        'OVER',
	'COLOR':        'OVER',
	'SOFT LIGHT':   'OVER',
	'LINEAR LIGHT': 'OVER',
	'OVERLAY':      'OVER',
	'ADD':          'ADD',
	'SUBTRACT':     'SUBTRACT',
	'MULTIPLY':     'MULTIPLY',
	'DIFFERENCE':   'DIFFERENCE',
	'DARKEN':       'DARKEN',
	'LIGHTEN':      'LIGHTEN',
	'SATURATION':   'SATURATE',
}


def preprocess_textures(sce):
	for tex in bpy.data.textures:
		tex.vray.name= get_random_string()
		debug(sce,"Texture: {0} [type: {1}; id: {2}]".format(tex.name,tex.type,tex.vray.name))


class VRAY_OT_convert_scene(bpy.types.Operator):
	bl_idname = "vray.convert_scene"
	bl_label  = "Convert materials"
	bl_description = "Convert scene materials from Blender Internal to V-Ray."

	def invoke(self, context, event):
		for ma in bpy.data.materials:
			print("V-Ray/Blender: Processing material: %s" % ma.name)
			
			rm= ma.raytrace_mirror
			rt= ma.raytrace_transparency
			
			VRayMaterial= ma.vray
			BRDFVRayMtl=  VRayMaterial.BRDFVRayMtl

			if ma.emit > 0.0:
				VRayMaterial.type= 'EMIT'

			if rm.use:
				BRDFVRayMtl.reflect_color= tuple([rm.reflect_factor]*3)
				BRDFVRayMtl.reflect_glossiness= rm.gloss_factor
				BRDFVRayMtl.reflect_subdivs= rm.gloss_samples
				BRDFVRayMtl.reflect_depth= rm.depth
				BRDFVRayMtl.option_cutoff= rm.gloss_threshold
				BRDFVRayMtl.anisotropy= 1.0 - rm.gloss_anisotropic

				if rm.fresnel > 0.0:
					BRDFVRayMtl.fresnel= True
					BRDFVRayMtl.fresnel_ior= rm.fresnel
			
			for slot in ma.texture_slots:
				if slot and slot.texture and slot.texture.type in TEX_TYPES:
					VRaySlot=    slot.texture.vray_slot
					VRayTexture= slot.texture.vray

					VRaySlot.blend_mode= CONVERT_BLEND_TYPE[slot.blend_type]
					
					if slot.use_map_emit:
						VRayMaterial.type= 'EMIT'

			if ma.type == 'VOLUME':
				VRayMaterial.type= 'VOL'
				
		return{'FINISHED'}


class VRAY_OT_flip_resolution(bpy.types.Operator):
	bl_idname = "vray.flip_resolution"
	bl_label  = "Flip resolution"
	bl_description = "Flip render resolution."

	def invoke(self, context, event):
		rd= context.scene.render

		rd.resolution_x, rd.resolution_y = rd.resolution_y, rd.resolution_x
		rd.pixel_aspect_x, rd.pixel_aspect_y = rd.pixel_aspect_y, rd.pixel_aspect_x
		
		return{'FINISHED'}

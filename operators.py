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
import subprocess
import tempfile
import time
import zipfile
import urllib.request
import sys

import bpy

import bmesh
from bpy.props import *

import vb25.render
import vb25.proxy

from vb25.lib     import VRaySocket, VRayProxy
from vb25.utils   import *
from vb25.plugins import PLUGINS


##     ## ########  ########     ###    ######## ########
##     ## ##     ## ##     ##   ## ##      ##    ##
##     ## ##     ## ##     ##  ##   ##     ##    ##
##     ## ########  ##     ## ##     ##    ##    ######
##     ## ##        ##     ## #########    ##    ##
##     ## ##        ##     ## ##     ##    ##    ##
 #######  ##        ########  ##     ##    ##    ########

class VRAY_OT_update(bpy.types.Operator):
	bl_idname      = "vray.update"
	bl_label       = "Update Exporter"
	bl_description = "Update exporter from github"

	def execute(self, context):
		update_dir = create_dir(os.path.join(tempfile.gettempdir(), "vb25_update"))

		# Downloading file
		self.report({'INFO'}, "Downloading 'master' branch archive...")

		GIT_MASTER_URL = "https://github.com/bdancer/vb25/zipball/master"

		# devnote: urllib2 not available, urllib's fancyurlopener returns errors anyways (when connection is not available)
		# so this is a working 'ugly fix' that at leasts works. Sorry the ghetto fix.
		try:
			(filename, headers) = urllib.request.urlretrieve(GIT_MASTER_URL)
		except urllib.error.URLError:
			self.report({'ERROR'}, "Error retrieving the files. Check your connection.")
			return {'CANCELLED'}

		# Extracting archive
		ziparchive = zipfile.ZipFile(filename)
		ziparchive.extractall(update_dir)
		ziparchive.close()

		# Check update dir
		cur_vb25_dirpath = get_vray_exporter_path()
		new_vb25_dirpath = ""

		dirnames = os.listdir(update_dir)
		for dirname in dirnames:
			if dirname.startswith("bdancer-vb25-"):
				new_vb25_dirpath = os.path.join(update_dir, dirname)
				break

		if not new_vb25_dirpath:
			self.report({'ERROR'}, "Update files not found!")
			return {'CANCELLED'}

		# Copying new files
		debug(context.scene, "Copying new files...")
		if os.path.exists(cur_vb25_dirpath):
			if sys.platform == 'win32':
				for item in os.listdir(cur_vb25_dirpath):
					s = os.path.join(cur_vb25_dirpath, item)
					if os.path.isdir(s):
						os.system("rmdir /Q /S %s" % s)
					else:
						os.system("del /Q /F %s" % s)
			else:
				shutil.rmtree(cur_vb25_dirpath)

		copytree(new_vb25_dirpath, cur_vb25_dirpath)

		if os.path.exists(filename):
			self.report({'INFO'}, "Removing update archive: %s"%(filename))
			os.remove(filename)

		if os.path.exists(update_dir):
			self.report({'INFO'}, "Removing update unpack directory: %s"%(update_dir))
			shutil.rmtree(update_dir)

		self.report({'INFO'}, "V-Ray/Blender exporter updated!")

		return {'FINISHED'}


 ######     ###    ##     ## ######## ########     ###
##    ##   ## ##   ###   ### ##       ##     ##   ## ##
##        ##   ##  #### #### ##       ##     ##  ##   ##
##       ##     ## ## ### ## ######   ########  ##     ##
##       ######### ##     ## ##       ##   ##   #########
##    ## ##     ## ##     ## ##       ##    ##  ##     ##
 ######  ##     ## ##     ## ######## ##     ## ##     ##

class VRAY_OT_lens_shift(bpy.types.Operator):
	bl_idname=      'vray.lens_shift'
	bl_label=       "Get lens shift"
	bl_description= "Calculate lens shift"

	@classmethod
	def poll(cls, context):
		return (context.camera)

	def execute(self, context):
		VRayCamera=     context.camera.vray
		CameraPhysical= VRayCamera.CameraPhysical

		CameraPhysical.lens_shift= PLUGINS['CAMERA']['CameraPhysical'].get_lens_shift(context.object)

		return {'FINISHED'}


######## ######## ######## ########  ######  ########  ######
##       ##       ##       ##       ##    ##    ##    ##    ##
##       ##       ##       ##       ##          ##    ##
######   ######   ######   ######   ##          ##     ######
##       ##       ##       ##       ##          ##          ##
##       ##       ##       ##       ##    ##    ##    ##    ##
######## ##       ##       ########  ######     ##     ######

class VRAY_OT_effect_add(bpy.types.Operator):
	bl_idname=      'vray.effect_add'
	bl_label=       "Add Effect"

	bl_description= "Add effect"

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects
		VRayEffects.effects.add()
		VRayEffects.effects[-1].name= "Effect"

		return {'FINISHED'}


class VRAY_OT_effect_remove(bpy.types.Operator):
	bl_idname=      'vray.effect_remove'
	bl_label=       "Remove Effect"
	bl_description= "Remove effect"

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		if VRayEffects.effects_selected >= 0:
			VRayEffects.effects.remove(VRayEffects.effects_selected)
			VRayEffects.effects_selected-= 1

		return {'FINISHED'}


class VRAY_OT_effect_up(bpy.types.Operator):
	bl_idname=      'vray.effect_up'
	bl_label=       "Move effect up"
	bl_description= "Move effect up"

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		if VRayEffects.effects_selected <= 0:
			return {'CANCELLED'}

		VRayEffects.effects.move(VRayEffects.effects_selected,
								 VRayEffects.effects_selected - 1)
		VRayEffects.effects_selected-= 1

		return {'FINISHED'}


class VRAY_OT_effect_down(bpy.types.Operator):
	bl_idname=      'vray.effect_down'
	bl_label=       "Move effect down"
	bl_description= "Move effect down"

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		if VRayEffects.effects_selected == len(VRayEffects.effects) - 1:
			return {'CANCELLED'}

		VRayEffects.effects.move(VRayEffects.effects_selected,
								 VRayEffects.effects_selected + 1)
		VRayEffects.effects_selected+= 1

		return {'FINISHED'}


#### ##    ##  ######  ##       ##     ## ########  ######## ########
 ##  ###   ## ##    ## ##       ##     ## ##     ## ##       ##     ##
 ##  ####  ## ##       ##       ##     ## ##     ## ##       ##     ##
 ##  ## ## ## ##       ##       ##     ## ##     ## ######   ########
 ##  ##  #### ##       ##       ##     ## ##     ## ##       ##   ##
 ##  ##   ### ##    ## ##       ##     ## ##     ## ##       ##    ##
#### ##    ##  ######  ########  #######  ########  ######## ##     ##

class VRAY_OT_includer_add(bpy.types.Operator):
	bl_idname=      'vray.includer_add'
	bl_label=       "Add Include"
	bl_description= "Add Include *.vrsene"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.Includer

		module.nodes.add()
		module.nodes[-1].name= "Include Scene"

		return {'FINISHED'}


class VRAY_OT_includer_remove(bpy.types.Operator):
	bl_idname=      'vray.includer_remove'
	bl_label=       "Remove Include"
	bl_description= "Remove Include *.vrsene"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.Includer

		if module.nodes_selected >= 0:
		   module.nodes.remove(module.nodes_selected)
		   module.nodes_selected-= 1

		return {'FINISHED'}


class VRAY_OT_includer_up(bpy.types.Operator):
	bl_idname=      'vray.includer_up'
	bl_label=       "Up Include"
	bl_description= "Up Include *.vrsene"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.Includer

		if module.nodes_selected <= 0:
			return {'CANCELLED'}

		module.nodes.move(module.nodes_selected,
								 module.nodes_selected - 1)
		module.nodes_selected-= 1

		return {'FINISHED'}


class VRAY_OT_includer_down(bpy.types.Operator):
	bl_idname=      'vray.includer_down'
	bl_label=       "Down Include"
	bl_description= "Down Include *.vrsene"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.Includer

		if module.nodes_selected <= 0:
			return {'CANCELLED'}

		module.nodes.move(module.nodes_selected,
								 module.nodes_selected + 1)
		module.nodes_selected+= 1

		return {'FINISHED'}


######## ##       ######## ##     ## ######## ##    ## ########  ######
##       ##       ##       ###   ### ##       ###   ##    ##    ##    ##
##       ##       ##       #### #### ##       ####  ##    ##    ##
######   ##       ######   ## ### ## ######   ## ## ##    ##     ######
##       ##       ##       ##     ## ##       ##  ####    ##          ##
##       ##       ##       ##     ## ##       ##   ###    ##    ##    ##
######## ######## ######## ##     ## ######## ##    ##    ##     ######

class VRAY_OT_channel_add(bpy.types.Operator):
	bl_idname=      'vray.render_channels_add'
	bl_label=       "Add Render Channel"
	bl_description= "Add render channel"

	def execute(self, context):
		sce= context.scene
		vsce= sce.vray

		render_channels= vsce.render_channels

		render_channels.add()
		render_channels[-1].name= "RenderChannel"

		return {'FINISHED'}


class VRAY_OT_channel_del(bpy.types.Operator):
	bl_idname=      'vray.render_channels_remove'
	bl_label=       "Remove Render Channel"
	bl_description= "Remove render channel"

	def execute(self, context):
		sce= context.scene
		vsce= sce.vray

		render_channels= vsce.render_channels

		if vsce.render_channels_index >= 0:
		   render_channels.remove(vsce.render_channels_index)
		   vsce.render_channels_index-= 1

		return {'FINISHED'}


########  ########
##     ## ##     ##
##     ## ##     ##
##     ## ########
##     ## ##   ##
##     ## ##    ##
########  ##     ##

class VRAY_OT_node_add(bpy.types.Operator):
	bl_idname=      'vray.render_nodes_add'
	bl_label=       "Add Render Node"
	bl_description= "Add render node"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.VRayDR

		module.nodes.add()
		module.nodes[-1].name= "Render Node"

		return {'FINISHED'}



class VRAY_OT_node_del(bpy.types.Operator):
	bl_idname=      'vray.render_nodes_remove'
	bl_label=       "Remove Render Node"
	bl_description= "Remove render node"

	def execute(self, context):
		vs= context.scene.vray
		module= vs.VRayDR

		if module.nodes_selected >= 0:
		   module.nodes.remove(module.nodes_selected)
		   module.nodes_selected-= 1

		return {'FINISHED'}


########  #######     ######## ######## ##     ## ########
   ##    ##     ##       ##    ##        ##   ##     ##
   ##    ##     ##       ##    ##         ## ##      ##
   ##    ##     ##       ##    ######      ###       ##
   ##    ##     ##       ##    ##         ## ##      ##
   ##    ##     ##       ##    ##        ##   ##     ##
   ##     #######        ##    ######## ##     ##    ##

class VRAY_OT_settings_to_text(bpy.types.Operator):
	bl_idname      = 'vray.settings_to_text'
	bl_label       = "Settings to Text"
	bl_description = "Export settings to Text"

	bb_code = BoolProperty(
		name = "Use BB-code",
		description = "Use BB-code formatting",
		default = True
	)

	def execute(self, context):
		text = bpy.data.texts.new(name="Settings")

		bus = {}
		bus['scene'] = context.scene
		bus['preview'] = False
		bus['files'] = {}
		bus['files']['scene'] = text
		bus['filenames'] = {}
		bus['plugins'] = PLUGINS
		bus['effects'] = {}
		bus['effects']['fog']  = {}
		bus['effects']['toon'] = {}
		bus['effects']['toon']['effects'] = []
		bus['effects']['toon']['objects'] = []

		text.write("V-Ray/Blender 2.0 | Scene: %s | %s\n" % (context.scene.name, time.strftime("%d %b %Y %H:%m:%S")))

		for key in PLUGINS['SETTINGS']:
			if key in ('BakeView', 'RenderView', 'SettingsEnvironment'):
				# Skip some plugins
				continue

			plugin = PLUGINS['SETTINGS'][key]
			if hasattr(plugin, 'write'):
				plugin.write(bus)

		return {'FINISHED'}


########  ########  ######   #######  ##       ##     ## ######## ####  #######  ##    ##
##     ## ##       ##    ## ##     ## ##       ##     ##    ##     ##  ##     ## ###   ##
##     ## ##       ##       ##     ## ##       ##     ##    ##     ##  ##     ## ####  ##
########  ######    ######  ##     ## ##       ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##             ## ##     ## ##       ##     ##    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ## ##     ## ##       ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   #######  ########  #######     ##    ####  #######  ##    ##

class VRAY_OT_flip_resolution(bpy.types.Operator):
	bl_idname      = "vray.flip_resolution"
	bl_label       = "Flip resolution"
	bl_description = "Flip render resolution"

	def execute(self, context):
		scene = context.scene
		rd    = scene.render

		VRayScene = scene.vray

		if VRayScene.image_aspect_lock:
			VRayScene.image_aspect = 1.0 / VRayScene.image_aspect

		rd.resolution_x, rd.resolution_y = rd.resolution_y, rd.resolution_x
		rd.pixel_aspect_x, rd.pixel_aspect_y = rd.pixel_aspect_y, rd.pixel_aspect_x

		return {'FINISHED'}


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##


class VRAY_OT_write_scene(bpy.types.Operator):
	bl_idname      = "vray.write_scene"
	bl_label       = "Export scene"
	bl_description = "Export scene to a \"vrscene\" file"

	def execute(self, context):
		bus = {}
		bus['plugins'] = PLUGINS
		bus['scene'] = context.scene
		bus['preview'] = False
		bus['files']     = {}
		bus['filenames'] = {}

		init_files(bus)

		vb25.render.write_scene(bus)

		return {'FINISHED'}


class VRAY_OT_write_geometry(bpy.types.Operator):
	bl_idname      = "vray.write_geometry"
	bl_label       = "Export meshes"
	bl_description = "Export meshes into vrscene file"

	dialog_width = 180

	def draw(self, context):
		layout = self.layout
		split = layout.split()
		col = split.column()
		col.label(text = "Animation mode is active!")
		col.label(text = "Are you sure to export meshes?")

	def invoke(self, context, event):
		wm    = context.window_manager
		scene = context.scene

		VRayScene    = scene.vray
		VRayExporter = VRayScene.exporter

		if not bpy.app.background:
			if VRayExporter.animation and VRayExporter.animation_type == 'FULL':
				return wm.invoke_props_dialog(self, self.dialog_width)

		return self.execute(context)

	def execute(self, context):
		bus = {}
		bus['plugins'] = PLUGINS
		bus['scene'] = context.scene
		bus['preview'] = False
		bus['files']     = {}
		bus['filenames'] = {}

		init_files(bus, skipGeom=True)

		vb25.render.write_geometry(bus)

		return {'FINISHED'}


########  ######## ##    ## ########  ######## ########
##     ## ##       ###   ## ##     ## ##       ##     ##
##     ## ##       ####  ## ##     ## ##       ##     ##
########  ######   ## ## ## ##     ## ######   ########
##   ##   ##       ##  #### ##     ## ##       ##   ##
##    ##  ##       ##   ### ##     ## ##       ##    ##
##     ## ######## ##    ## ########  ######## ##     ##

class VRAY_OT_render(bpy.types.Operator):
	bl_idname      = "vray.render"
	bl_label       = "V-Ray Renderer"
	bl_description = "Render operator"

	def execute(self, context):
		scene = context.scene

		VRayScene    = scene.vray
		VRayExporter = VRayScene.exporter

		vb25.render.render(None, scene)

		return {'FINISHED'}



########  ##     ## ##    ##
##     ## ##     ## ###   ##
##     ## ##     ## ####  ##
########  ##     ## ## ## ##
##   ##   ##     ## ##  ####
##    ##  ##     ## ##   ###
##     ##  #######  ##    ##

class VRAY_OT_run(bpy.types.Operator):
	bl_idname      = "vray.run"
	bl_label       = "Run V-Ray"
	bl_description = "Run V-Ray renderer"

	def execute(self, context):
		vb25.render.run(None, context.scene)
		return {'FINISHED'}


class VRAY_OT_terminate(bpy.types.Operator):
	bl_idname      = "vray.terminate"
	bl_label       = "Terminate VRayRT"
	bl_description = "Terminates running VRayRT instance"

	def execute(self, context):
		s = VRaySocket()
		s.connect()
		s.send("stop", result=False)
		s.send("quit", result=False)
		s.disconnect()

		return {'FINISHED'}


 ######   #######  ##        #######  ########
##    ## ##     ## ##       ##     ## ##     ##
##       ##     ## ##       ##     ## ##     ##
##       ##     ## ##       ##     ## ########
##       ##     ## ##       ##     ## ##   ##
##    ## ##     ## ##       ##     ## ##    ##
 ######   #######  ########  #######  ##     ##

class VRAY_OT_set_kelvin_color(bpy.types.Operator):
	bl_idname      = "vray.set_kelvin_color"
	bl_label       = "Kelvin color"
	bl_description = "Set color temperature"

	data_path= StringProperty(
		name= "Data",
		description= "Data path",
		maxlen= 1024,
		default= ""
	)

	d_color= EnumProperty(
		name= "Illuminant series D",
		description= "Illuminant series D",
		items= (
			('D75',  "D75",  "North sky Daylight"),
			('D65',  "D65",  "Noon Daylight"),
			('D55',  "D55",  "Mid-morning / Mid-afternoon Daylight"),
			('D50',  "D50",  "Horizon Light"),
		),
		default= 'D50'
	)

	use_temperature= BoolProperty(
		name= "Use temperature",
		description= "Use temperature",
		default= False
	)

	temperature= IntProperty(
		name= "Temperature",
		description= "Kelvin temperature",
		min= 1000,
		max= 40000,
		step= 100,
		default= 5000
	)

	dialog_width= 150

	def draw(self, context):
		layout= self.layout

		if 0:
			row= layout.split().row(align= True)
			row.prop(self, 'use_temperature', text= "")
			if self.use_temperature:
				row.prop(self, 'temperature', text= "K")
			else:
				row.prop(self, 'd_color', text= "Type")
		else:
			split= layout.split()
			col= split.column()
			col.prop(self, 'd_color', text= "Type")
			sub= col.row(align= True)
			sub.prop(self, 'use_temperature', text= "")
			sub.prop(self, 'temperature', text= "K")

	def invoke(self, context, event):
		wm= context.window_manager
		return wm.invoke_props_dialog(self, self.dialog_width)

	def execute(self, context):
		D_COLOR= {
			'D75': 7500,
			'D65': 6500,
			'D55': 5500,
			'D50': 5000,
		}

		def recursive_attr(data, attrs):
			if not attrs:
				return data
			attr= attrs.pop()
			return recursive_attr(getattr(data, attr), attrs)

		if self.data_path:
			attrs= self.data_path.split('.')
			attr= attrs.pop() # Attribute to set
			attrs.reverse()

			data_pointer= recursive_attr(context, attrs)

			temperature= D_COLOR[self.d_color]

			if self.use_temperature:
				temperature= self.temperature

			setattr(data_pointer, attr, tuple(kelvin_to_rgb(temperature)))

		return {'FINISHED'}


######## ######## ##     ## ######## ##     ## ########  ########  ######
   ##    ##        ##   ##     ##    ##     ## ##     ## ##       ##    ##
   ##    ##         ## ##      ##    ##     ## ##     ## ##       ##
   ##    ######      ###       ##    ##     ## ########  ######    ######
   ##    ##         ## ##      ##    ##     ## ##   ##   ##             ##
   ##    ##        ##   ##     ##    ##     ## ##    ##  ##       ##    ##
   ##    ######## ##     ##    ##     #######  ##     ## ########  ######

class VRAY_OT_add_sky(bpy.types.Operator):
	bl_idname      = "vray.add_sky"
	bl_label       = "Add Sky texture"
	bl_description = "Add Sky texture to the background"

	def execute(self, context):
		scene= context.scene

		try:
			for i,slot in enumerate(scene.world.texture_slots):
				if not slot:
					tex= bpy.data.textures.new(name= 'VRaySky',
											   type= 'VRAY')
					tex.vray.type= 'TexSky'
					new_slot= scene.world.texture_slots.create(i)
					new_slot.texture= tex
					break
		except:
			debug(scene,
				  "Sky texture only availble in \"%s\"!" % color("Special build",'green'),
				  error= True)

		return {'FINISHED'}


##       #### ##    ## ##    ## #### ##    ##  ######
##        ##  ###   ## ##   ##   ##  ###   ## ##    ##
##        ##  ####  ## ##  ##    ##  ####  ## ##
##        ##  ## ## ## #####     ##  ## ## ## ##   ####
##        ##  ##  #### ##  ##    ##  ##  #### ##    ##
##        ##  ##   ### ##   ##   ##  ##   ### ##    ##
######## #### ##    ## ##    ## #### ##    ##  ######

class VRAY_OT_copy_linked_materials(bpy.types.Operator):
	bl_idname      = "vray.copy_linked_materials"
	bl_label       = "Copy linked materials"
	bl_description = "Copy linked materials"

	def execute(self, context):
		scene=  context.scene
		object= context.active_object

		if not object:
			debug(scene, "No object selected!", error= True)
			return {'CANCELLED'}

		if object.type == 'EMPTY':
			debug(scene, "Empty object type is not supported! Use simple mesh instead.", error= True)
			return {'CANCELLED'}

		if object.dupli_type == 'GROUP':
			object.dupli_list_create(scene)

			for dup_ob in object.dupli_list:
				ob= dup_ob.object
				for slot in ob.material_slots:
					ma= slot.material
					if ma:
						materials= [slot.material for slot in object.material_slots]
						if ma not in materials:
							debug(scene, "Adding material: %s" % (ma.name))
							object.data.materials.append(ma)

			object.dupli_list_clear()

			return {'FINISHED'}

		debug(scene, "Object \"%s\" has no dupli-group assigned!" % (object.name), error= True)
		return {'CANCELLED'}


def GetRegClasses():
	return (
		VRAY_OT_update,
		VRAY_OT_lens_shift,
		VRAY_OT_effect_add,
		VRAY_OT_effect_remove,
		VRAY_OT_effect_up,
		VRAY_OT_effect_down,
		VRAY_OT_includer_add,
		VRAY_OT_includer_remove,
		VRAY_OT_includer_up,
		VRAY_OT_includer_down,
		VRAY_OT_channel_add,
		VRAY_OT_channel_del,
		VRAY_OT_node_add,
		VRAY_OT_node_del,
		VRAY_OT_settings_to_text,
		VRAY_OT_flip_resolution,
		VRAY_OT_write_scene,
		VRAY_OT_write_geometry,
		VRAY_OT_render,
		VRAY_OT_run,
		VRAY_OT_terminate,
		VRAY_OT_set_kelvin_color,
		VRAY_OT_add_sky,
		VRAY_OT_copy_linked_materials,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

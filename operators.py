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
import subprocess
import tempfile
import time
import sys
import shutil

import bpy

import bmesh
from bpy.props import *

import vb30.proxy

from vb30.lib     import LibUtils, BlenderUtils, PathUtils, SysUtils
from vb30.lib     import ColorUtils
from vb30.plugins import PLUGINS, PLUGINS_ID
from vb30 import debug


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
		# Check if target dir is writable
		exporterDir = SysUtils.GetExporterPath()
		if not os.access(exporterDir, os.W_OK):
			self.report({'ERROR'}, "Exporter directory is not writable!")
			return {'CANCELLED'}

		git = shutil.which("git")
		if not git:
			if sys.platform == 'win32':
				# Try default path
				git = "C:/Program Files (x86)/Git/bin/git.exe"
				if not os.path.exists(git):
					self.report({'ERROR'}, "Git is not found!")
					return {'CANCELLED'}
			else:
				self.report({'ERROR'}, "Git is not found!")
				return {'CANCELLED'}

		if sys.platform == 'win32':
			git = '"%s"' % git

		cmds = (
			"%s fetch" % git,
			"%s reset --hard origin/master" % git,
			"%s submodule foreach git fetch" % git,
			"%s submodule foreach git reset --hard origin/master" % git
		)

		os.chdir(exporterDir)

		err = 0
		for cmd in cmds:
			debug.PrintInfo("Executing: %s" % cmd)
			err += os.system(cmd)

		if err:
			self.report({'WARNING'}, "V-Ray For Blender: Git update warning! Check system console!")
			return {'CANCELLED'}

		self.report({'INFO'}, "V-Ray For Blender: Exporter is now updated! Please, restart Blender!")

		return {'FINISHED'}


 ######     ###    ##     ## ######## ########     ###
##    ##   ## ##   ###   ### ##       ##     ##   ## ##
##        ##   ##  #### #### ##       ##     ##  ##   ##
##       ##     ## ## ### ## ######   ########  ##     ##
##       ######### ##     ## ##       ##   ##   #########
##    ## ##     ## ##     ## ##       ##    ##  ##     ##
 ######  ##     ## ##     ## ######## ##     ## ##     ##

class VRAY_OT_lens_shift(bpy.types.Operator):
	bl_idname      = 'vray.lens_shift'
	bl_label       = "Get lens shift"
	bl_description = "Calculate lens shift"

	@classmethod
	def poll(cls, context):
		return (context.camera)

	def execute(self, context):
		VRayCamera = context.camera.vray

		CameraPhysical = VRayCamera.CameraPhysical

		CameraPhysical.lens_shift = PLUGINS_ID['CameraPhysical'].GetLensShift(context.object)

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


class VRAY_OT_dr_nodes_load(bpy.types.Operator):
	bl_idname      = "vray.dr_nodes_load"
	bl_label       = "Load DR Nodes"
	bl_description = "Load distributed rendering nodes list"

	def execute(self, context):
		VRayScene = context.scene.vray
		VRayDR = VRayScene.VRayDR

		nodesFilepath = os.path.join(SysUtils.GetUserConfigDir(), "render_nodes.txt")

		if not os.path.exists(nodesFilepath):
			return {'CANCELLED'}

		with open(nodesFilepath, 'r') as nodesFile:
			VRayDR.nodes.clear()

			for line in nodesFile.readlines():
				l = line.strip()
				if not l:
					continue

				item = VRayDR.nodes.add()

				nodeSetup = l.split(":")

				# Initial format
				if len(nodeSetup) == 2:
					item.name, item.address = nodeSetup
				# "Use" added
				elif len(nodeSetup) == 3:
					item.name    = nodeSetup[0]
					item.address = nodeSetup[1]
					item.use     = int(nodeSetup[2])
				# Port override added
				elif len(nodeSetup) == 5:
					item.name = nodeSetup[0]
					item.address = nodeSetup[1]
					item.use = int(nodeSetup[2])
					item.port_override = int(nodeSetup[3])
					item.port = int(nodeSetup[4])

		VRayDR.nodes_selected = 0

		return {'FINISHED'}


class VRAY_OT_dr_nodes_save(bpy.types.Operator):
	bl_idname      = "vray.dr_nodes_save"
	bl_label       = "Save DR Nodes"
	bl_description = "Save distributed rendering nodes list"

	def execute(self, context):
		VRayScene = context.scene.vray
		VRayDR = VRayScene.VRayDR

		nodesFilepath = os.path.join(SysUtils.GetUserConfigDir(), "render_nodes.txt")

		with open(nodesFilepath, 'w') as nodesFile:
			for item in VRayDR.nodes:
				item_data = "{item.name}:{item.address}:{item.use:d}:{item.port_override:d}:{item.port:d}".format(item=item)
				nodesFile.write("%s\n" % item_data)

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

		rd.resolution_x, rd.resolution_y = rd.resolution_y, rd.resolution_x
		rd.pixel_aspect_x, rd.pixel_aspect_y = rd.pixel_aspect_y, rd.pixel_aspect_x

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
		min= 800,
		max= 12000,
		default= 5000
	)

	dialog_width = 150

	def draw(self, context):
		layout = self.layout

		split = layout.split()
		col = split.column()
		col.prop(self, 'd_color', text="Type")
		sub = col.row(align=True)
		sub.prop(self, 'use_temperature', text="")
		sub.prop(self, 'temperature', text="K")

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

			setattr(data_pointer, attr, tuple(ColorUtils.KelvinToRBG(temperature)))

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
		# TODO: Create noded version
		#
		return {'FINISHED'}


##     ## ####  ######   ######
###   ###  ##  ##    ## ##    ##
#### ####  ##  ##       ##
## ### ##  ##   ######  ##
##     ##  ##        ## ##
##     ##  ##  ##    ## ##    ##
##     ## ####  ######   ######

class VRayOpSwitchSlotsObject(bpy.types.Operator):
	bl_idname      = "vray.switch_material_slot"
	bl_label       = "Switch Material Slots"
	bl_description = "Switch all object's material slots to DATA / OBJECT"

	def execute(self, context):
		VRayExporter = context.scene.vray.Exporter

		switch_to = VRayExporter.op_switch_slots_switch_to

		from_slot = 'OBJECT' if switch_to == 'DATA' else 'DATA'

		for ob in context.scene.objects:
			if not ob.type == 'MESH':
				continue
			for s in ob.material_slots:
				ma = s.material
				if s.link == from_slot:
					s.link = switch_to
					s.material = ma

		return {'FINISHED'}


def GetRegClasses():
	return (
		VRAY_OT_update,
		VRAY_OT_lens_shift,
		VRAY_OT_node_add,
		VRAY_OT_node_del,
		VRAY_OT_dr_nodes_load,
		VRAY_OT_dr_nodes_save,
		VRAY_OT_settings_to_text,
		VRAY_OT_flip_resolution,
		VRAY_OT_set_kelvin_color,
		VRAY_OT_add_sky,

		VRayOpSwitchSlotsObject,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

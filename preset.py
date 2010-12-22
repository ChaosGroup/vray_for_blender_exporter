'''

	V-Ray/Blender 2.5

	http://vray.cgdo.ru

	Author: Andrey M. Izrantsev (aka bdancer)
	E-Mail: izrantsev@cgdo.ru

	This plugin is protected by the GNU General Public License v.2

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


''' Blender modules '''
import bpy

''' vb modules '''
from vb25.utils import *


class VBPresetBase():
	bl_options = {'REGISTER'}

	name= bpy.props.StringProperty(
		name= "Name",
		description= "Name of the preset, used to make the path name",
		maxlen= 64,
		default= "")

	remove_active= bpy.props.BoolProperty(
		default= False,
		options= {'HIDDEN'})

	@staticmethod
	def as_filename(name):
		for char in " !@#$%^&*(){}:\";'[]<>,.\\/?":
			name= name.replace(char, '_')
		return name.lower().strip()

	def execute(self, context):
		import os
		
		if hasattr(self, "pre_cb"):
			self.pre_cb(context)
		
		preset_menu_class = getattr(bpy.types, self.preset_menu)

		if not self.remove_active:		  
			if not self.name:
				return {'FINISHED'}

			filename= self.as_filename(self.name)
			
			target_path= os.path.normpath(os.path.join(vb_script_path(), "presets", self.preset_subdir))

			filepath= os.path.join(target_path, filename) + ".py"
			
			if hasattr(self, "add"):
				self.add(context, filepath)
			else:
				file_preset = open(filepath, 'w')
				file_preset.write("import bpy\n")

				for rna_path in self.preset_values:
					value = eval(rna_path)
					# convert thin wrapped sequences to simple lists to repr()
					try:
						value = value[:]
					except:
						pass

					file_preset.write("%s = %r\n" % (rna_path, value))

				file_preset.close()

			preset_menu_class.bl_label = bpy.path.display_name(filename)

		else:
			preset_active = preset_menu_class.bl_label

			filepath= os.path.join(vb_script_path(), "presets", self.preset_subdir, preset_active+".py")

			if not os.path.exists(filepath):
				return {'CANCELLED'}

			if hasattr(self, "remove"):
				self.remove(context, filepath)
			else:
				try:
					os.remove(filepath)
				except:
					import traceback
					traceback.print_exc()

			# XXX, stupid!
			preset_menu_class.bl_label = "Presets"

		if hasattr(self, "post_cb"):
			self.post_cb(context)

		return {'FINISHED'}

	def check(self, context):
		self.name = self.as_filename(self.name)

	def invoke(self, context, event):
		if not self.remove_active:
			wm = context.window_manager
			return wm.invoke_props_dialog(self)
		else:
			return self.execute(context)


class vb_preset_global_render(VBPresetBase, bpy.types.Operator):
	'''Add a V-Ray global preset'''
	bl_idname = "vray.preset_add"
	bl_label  = "Add V-Ray Global Preset"

	preset_menu   = "VRAY_MT_global_preset"
	preset_subdir = "render"

	preset_values= []
	# "bpy.context.scene.vray.SettingsGI.SettingsIrradianceMap.min_rate",
	

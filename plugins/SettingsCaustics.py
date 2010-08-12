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

TYPE= 'SETTINGS'

ID=   'SETTINGSCAUSTICS'
NAME= 'Caustics'
PLUG= 'SettingsCaustics'
DESC= "Caustics settings."

PARAMS= (
	'on',
	'max_photons',
	'search_distance',
	'max_density',
	'multiplier',
	'mode',
	'file',
	# 'dont_delete',
	'auto_save',
	'auto_save_file',
	'show_calc_phase'
)


import bpy

from vb25.utils import *


class SettingsCaustics(bpy.types.IDPropertyGroup):
	pass

def add_properties(parent_struct):
	parent_struct.PointerProperty(
		attr= 'SettingsCaustics',
		type= SettingsCaustics,
		name= "Caustics",
		description= "Caustics settings."
	)

	SettingsCaustics.BoolProperty(
		attr= 'on',
		name= "On",
		description= "Enable caustics computation.",
		default= False
	)

	SettingsCaustics.IntProperty(
		attr= 'max_photons',
		name= "Max photons",
		description= "TODO.",
		min= 0,
		max= 10000,
		soft_min= 0,
		soft_max= 1000,
		default= 30
	)

	SettingsCaustics.FloatProperty(
		attr= 'search_distance',
		name= "Search distance",
		description= "TODO.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 1.0,
		precision= 3,
		default= 0.1
	)

	SettingsCaustics.FloatProperty(
		attr= 'max_density',
		name= "Max density",
		description= "TODO.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	SettingsCaustics.FloatProperty(
		attr= 'multiplier',
		name= "Multiplier",
		description= "TODO.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	SettingsCaustics.EnumProperty(
		attr= 'mode',
		name= "Mode",
		description= "Caustics computaion mode.",
		items=(
			('FILE', "From file",      ""),
			('NEW',   "New",           "")
		),
		default= 'NEW'
	)

	SettingsCaustics.StringProperty(
		attr= 'file',
		name= "File",
		subtype= 'FILE_PATH',
		description= "TODO."
	)

	# SettingsCaustics.BoolProperty(
	# 	attr= 'dont_delete',
	# 	name= "Don\'t delete",
	# 	description= "TODO.",
	# 	default= False
	# )

	SettingsCaustics.BoolProperty(
		attr= 'auto_save',
		name= "Auto save",
		description= "TODO.",
		default= False
	)

	SettingsCaustics.StringProperty(
		attr= 'auto_save_file',
		name= "Auto save file",
		subtype= 'FILE_PATH',
		description= "TODO."
	)

	SettingsCaustics.BoolProperty(
		attr= 'show_calc_phase',
		name= "Show calc phase",
		description= "TODO.",
		default= False
	)



'''
  OUTPUT
'''
def write(ofile, sce, rna_pointer):
	MODE= {
		'FILE': 1,
		'NEW':  0
	}
	
	ofile.write("\n%s {" % PLUG)
	for param in PARAMS:
		if param in ('file','auto_save_file'):
			value= "\"%s\"" % getattr(rna_pointer,param)
		elif param == 'mode':
			value= MODE[rna_pointer.mode]
		else:
			value= getattr(rna_pointer,param)
		ofile.write("\n\t%s= %s;"%(param, p(value)))
	ofile.write("\n}\n")



'''
  GUI
'''
narrowui= 200


class SettingsCausticsPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render'


class RENDER_PT_SettingsCaustics(SettingsCausticsPanel, bpy.types.Panel):
	bl_label = NAME

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		sce= context.scene
		rd= sce.render
		show= sce.vray_scene.SettingsCaustics.on
		return (rd.use_game_engine == False) and (rd.engine in cls.COMPAT_ENGINES) and (show)
	
	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		vsce= context.scene.vray_scene
		vmodule= getattr(vsce, PLUG)

		layout.prop(vmodule,'mode')

		if vmodule.mode == 'FILE':
			layout.prop(vmodule,'file')
		else:
			split= layout.split()
			col= split.column()
			col.prop(vmodule,'multiplier')
			col.prop(vmodule,'search_distance')
			if wide_ui:
				col = split.column()
			col.prop(vmodule,'max_photons')
			col.prop(vmodule,'max_density')
			col.prop(vmodule,'show_calc_phase')

			split= layout.split()
			split.label(text="Files:")
			split= layout.split(percentage=0.25)
			colL= split.column()
			colR= split.column()
			if wide_ui:
				colL.prop(vmodule,"auto_save", text="Auto save")
			else:
				colL.prop(vmodule,"auto_save", text="")
			colR.active= vmodule.auto_save
			colR.prop(vmodule,"auto_save_file", text="")

		
		
		
bpy.types.register(RENDER_PT_SettingsCaustics)


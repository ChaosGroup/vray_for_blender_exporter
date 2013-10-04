import bpy

from vb25.plugins import PLUGINS, gen_material_menu_items


TYPE= 'MATERIAL'
ID=   'Material'

NAME= 'General material setings'
DESC= "General V-Ray material settings"


def add_properties(rna_pointer):
	material_types = gen_material_menu_items(PLUGINS['BRDF'])
	
	# rna_pointer.type = bpy.props.EnumProperty(
	# 	name = "Type",
	# 	description  = "Material type",
	# 	items = material_types,
	# 	default = material_types[0][0]
	# )

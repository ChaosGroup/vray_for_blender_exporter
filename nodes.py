'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 15 March 2011 [17:03]"

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


''' Blender modules '''
import bpy
import mathutils
import sys

''' vb modules '''
from vb25.uvwgen  import *
from vb25.texture import *
from vb25.plugins import *
from vb25.utils   import *


# def get_node_name(nt, node):
# 	return "%s_%s" % (get_name(nt, prefix= 'NT'),
# 					  clean_string(node.name))


# # Find node connected to socket
# # @ nt - NodeTree
# # @ ns - NodeSocket
# def find_connected_node(nt, ns):
# 	for n in nt.links:
# 		if n.to_socket == ns:
# 			return n.from_node
# 	return None


# def write_node_old(bus):
# 	global material_name
	
# 	ofile= bus['files']['materials']
# 	scene= bus['scene']

# 	ma= bus['material']

# 	nt= bus['node_material']['node_tree']
# 	no= bus['node_material']['node']
	
# 	debug(scene,"  Writing node: %s [%s]"%(no.name, no.type))

# 	if no.type == 'OUTPUT':
# 		brdf_name= "BRDFDiffuse_no_material"

# 		for ns in no.inputs:
# 			if ns.name == 'Color':
# 				color= find_connected_node(nt, ns)
# 				brdf_name= "%s_%s_%s"%(ma.name, nt.name, color.name)

# 		material_name= get_name(ma, prefix='MA')

# 		ofile.write("\nMtlSingleBRDF %s {"  % material_name)
# 		ofile.write("\n\tbrdf= %s;" % clean_string(brdf_name))
# 		ofile.write("\n}\n")

# 	elif no.type in ('MATERIAL','MATERIAL_EXT'):
# 		bus['textures']= {}
# 		bus['material']= no.material

# 		brdf= PLUGINS['BRDF'][no.material.vray.type].write(bus)

# 		bus['material']= ma

# 	elif no.type == 'MIX_RGB':
# 		color1= "BRDFDiffuse_no_material"
# 		color2= "BRDFDiffuse_no_material"
# 		fac= "Color(0.5,0.5,0.5)"

# 		brdf_name= "%s_%s_%s"%(ma.name, nt.name, no.name)

# 		for ns in no.inputs:
# 			if ns.name == 'Color1':
# 				node_color1= find_connected_node(nt, ns)
# 			elif ns.name == 'Color2':
# 				node_color2= find_connected_node(nt, ns)
# 			else:
# 				fac= "Color(1.0,1.0,1.0)*%.3f"%(1.0 - ns.default_value[0])
# 				node_fac= find_connected_node(nt, ns)

# 		if node_color1:
# 			if node_color1.type in ('MATERIAL','MATERIAL_EXT'):
# 				color1= "%s_MA%s" % (node_color1.material.vray.type,
# 									 clean_string(node_color1.material.name))

# 		if node_color2:
# 			if node_color2.type in ('MATERIAL','MATERIAL_EXT'):
# 				color2= "%s_MA%s" % (node_color2.material.vray.type,
# 									 clean_string(node_color2.material.name))

# 		if node_fac:
# 			if node_fac.type == 'TEXTURE':
# 				bus['mtex']= {}
# 				bus['mtex']['mapto']=   'node'
# 				bus['mtex']['slot']=    None
# 				bus['mtex']['texture']= node_fac.texture
# 				bus['mtex']['factor']=  1.0
# 				bus['mtex']['name']=    clean_string("NT%sNO%sTE%s" % (nt.name,
# 																	   no.name,
# 																	   node_fac.texture.name))

# 				# Write texture
# 				weights= write_texture(bus)

# 		else:
# 			weights= "weights_%s"%(clean_string(brdf_name))
# 			ofile.write("\nTexAColor %s {"%(weights))
# 			ofile.write("\n\tuvwgen= %s;" % bus['defaults']['uvwgen'])
# 			ofile.write("\n\ttexture= %s;" % fac)
# 			ofile.write("\n}\n")

# 		ofile.write("\nBRDFLayered %s {"%(clean_string(brdf_name)))
# 		ofile.write("\n\tbrdfs= List(%s, %s);"%(color1, color2))
# 		ofile.write("\n\tweights= List(%s, TEDefaultBlend);"%(weights))
# 		ofile.write("\n\tadditive_mode= 0;") # Shellac
# 		ofile.write("\n}\n")


# 	elif no.type == 'INVERT':
# 		pass


# def write_node_material_old(bus):
# 	ofile= bus['files']['materials']
# 	scene= bus['scene']

# 	ob=    bus['node']['object']
# 	base=  bus['node']['base']

# 	ma=    bus['material']

# 	bus['node_material']= {}
# 	bus['node_material']['material']=  ma
# 	bus['node_material']['node_tree']= ma.node_tree

# 	debug(scene, "Writing node material: %s" % (ma.name))

# 	node_tree= ma.node_tree
# 	for node in node_tree.nodes:
# 		if node.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT'):
# 			bus['node_material']['node']= node

# 			write_node_old(bus)

# 		else:
# 			debug(scene, "Node: %s (unsupported node type: %s)" % (node.name, node.type))

# 	return material_name

'''
  NODES
'''
def write_BRDFDiffuse(bus, name, node, color):
	ofile= bus['files']['materials']
	scene= bus['scene']

	return "BRDFDiffuse%s" % str(color)


def write_TexAColor(bus, name, node, color):
	ofile= bus['files']['materials']
	scene= bus['scene']

	tex_name= "TAC%sNO%s" % (name, clean_string(node.name))

	ofile.write("\nTexAColor %s {" % tex_name)
	ofile.write("\n\ttexture= %s;" % a(scene, color))
	ofile.write("\n}\n")

	return tex_name


def write_ShaderNodeTexture(bus, node, input_params):
	node_tree= bus['nodes']['node_tree']

	bus['mtex']= {}
	bus['mtex']['mapto']=   'node'
	bus['mtex']['slot']=     None
	bus['mtex']['texture']=  node.texture
	bus['mtex']['factor']=   1.0
	bus['mtex']['name']=     clean_string("NT%sNO%sTE%s" % (node_tree.name,
														   node.name,
														   node.texture.name))

	return write_texture(bus)


def write_ShaderNodeMaterial(bus, node, input_params):
	ma=    bus['material']

	bus['textures']= {}
	bus['material']= node.material

	node_name= PLUGINS['BRDF'][node.material.vray.type].write(bus)

	bus['material']= ma

	return node_name


def write_ShaderNodeOutput(bus, node, input_params):
	ofile= bus['files']['materials']
	scene= bus['scene']

	ma=    bus['material']

	params= {
		'Color': "",
		'Alpha': "",
	}

	for key in params:
		# Key is mapped in input_params
		if key in input_params:
			params[key]= input_params[key]

		else:
			if key == 'Color':
				params[key]= write_BRDFDiffuse(bus, key, node,
											   mathutils.Color(node.inputs[key].default_value))
			elif key == 'Alpha':
				params[key]= write_TexAColor(bus, key, node,
											 mathutils.Color([node.inputs[key].default_value[0]]*3))

	node_name= get_name(ma, prefix='MA')

	ofile.write("\nMtlSingleBRDF %s {"  % node_name)
	ofile.write("\n\tbrdf= %s;" % params['Color'])
	ofile.write("\n}\n")

	return node_name

	
def write_ShaderNodeMixRGB(bus, node, input_params):
	ofile= bus['files']['materials']
	scene= bus['scene']

	node_tree= bus['nodes']['node_tree']

	params= {
		'Color1': "",
		'Color2': "",
		'Fac':    "",
	}
	
	for key in params:
		# Key is mapped in input_params
		if key in input_params:
			params[key]= input_params[key]

		else:
			if key == 'Color1':
				params[key]= write_BRDFDiffuse(bus, key, node, node.inputs[key])
			elif key == 'Color2':
				params[key]= write_BRDFDiffuse(bus, key, node, node.inputs[key])
			elif key == 'Fac':
				params[key]= write_TexAColor(bus, key, node,
											 mathutils.Color([node.inputs[key].default_value[0]]*3))

	node_name= get_node_name(node_tree, node)

	ofile.write("\nBRDFLayered %s {" % node_name)
	ofile.write("\n\tbrdfs= List(%s, %s);" % (params['Color1'], params['Color2']))
	ofile.write("\n\tweights= List(%s, TEDefaultBlend);" % params['Fac'])
	ofile.write("\n}\n")

	return node_name

	
		

'''
  MATERIAL
'''
def get_node_name(node_tree, node):
	return "%s%s" % (get_name(node_tree, prefix='NT'),
					 clean_string(node.name))


def get_output_node(node_tree):
	for node in node_tree.nodes:
		if node.type == 'OUTPUT':
			return node
	return None


def connected_node(node_tree, node_socket):
	for node in node_tree.links:
		if node.to_socket == node_socket:
			return node.from_node
	return None


def write_node(bus, node_tree, node):
	ofile= bus['files']['materials']
	scene= bus['scene']

	node_params= {}

	for input_socket in node.inputs:
		input_node= connected_node(node_tree, input_socket)

		if not input_node:
			continue

		node_params[input_socket.name]= write_node(bus, node_tree, input_node)

	print_dict(scene, "Node \"%s\"" % (node.name), node_params)

	if node.type == 'MIX_RGB':
		return write_ShaderNodeMixRGB(bus, node, node_params)

	elif node.type == 'OUTPUT':
		return write_ShaderNodeOutput(bus, node, node_params)

	elif node.type in {'MATERIAL','MATERIAL_EXT'}:
		return write_ShaderNodeMaterial(bus, node, node_params)

	elif node.type == 'TEXTURE':
		return write_ShaderNodeTexture(bus, node, node_params)


def write_node_material(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']

	ob=    bus['node']['object']
	base=  bus['node']['base']

	ma=    bus['material']

	node_tree= ma.node_tree
	
	output_node= get_output_node(node_tree)

	if output_node:
		bus['nodes']= {}
		bus['nodes']['node_tree']= node_tree
		
		return write_node(bus, node_tree, output_node)

	return bus['defaults']['material']


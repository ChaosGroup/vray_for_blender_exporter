'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 15 March 2011 [19:34]"

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


'''
  NODES
'''
def write_BRDFDiffuse(bus, name, node, color):
	ofile= bus['files']['materials']
	scene= bus['scene']

	comp_name= "BRDFDiffuse%s" % (name)
	
	ofile.write("\nBRDFDiffuse %s {" % comp_name)
	ofile.write("\n\tcolor= %s;" % a(scene, color))
	ofile.write("\n}\n")

	return comp_name


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
				c= node.inputs[key].default_value
				params[key]= write_BRDFDiffuse(bus, key, node,
											   mathutils.Color((c[0],c[1],c[2])))
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
				c= node.inputs[key].default_value
				params[key]= write_BRDFDiffuse(bus, key, node,
											   mathutils.Color((c[0],c[1],c[2])))
			elif key == 'Color2':
				c= node.inputs[key].default_value
				params[key]= write_BRDFDiffuse(bus, key, node,
											   mathutils.Color((c[0],c[1],c[2])))
			elif key == 'Fac':
				params[key]= write_TexAColor(bus, key, node,
											 mathutils.Color([node.inputs[key].default_value[0]]*3))

	node_name= get_node_name(node_tree, node)

	ofile.write("\nBRDFLayered %s {" % node_name)
	ofile.write("\n\tbrdfs= List(%s, %s);" % (params['Color2'], params['Color1']))
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


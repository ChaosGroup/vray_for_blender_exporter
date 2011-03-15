'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Tuesday, 15 March 2011 [14:08]"

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

''' vb modules '''
from vb25.uvwgen  import *
from vb25.texture import *
from vb25.plugins import *
from vb25.utils   import *


material_name= None


def get_node_name(nt, node):
	return "%s_%s" % (get_name(nt, prefix= 'NT'),
					  clean_string(node.name))


# Find node connected to socket
# @ nt - NodeTree
# @ ns - NodeSocket
def find_connected_node(nt, ns):
	for n in nt.links:
		if n.to_socket == ns:
			return n.from_node
	return None


def write_node(bus):
	global material_name
	
	ofile= bus['files']['materials']
	scene= bus['scene']

	ma= bus['material']

	nt= bus['node_material']['node_tree']
	no= bus['node_material']['node']
	
	debug(scene,"  Writing node: %s [%s]"%(no.name, no.type))

	if no.type == 'OUTPUT':
		brdf_name= "BRDFDiffuse_no_material"

		for ns in no.inputs:
			if ns.name == 'Color':
				color= find_connected_node(nt, ns)
				brdf_name= "%s_%s_%s"%(ma.name, nt.name, color.name)

		material_name= get_name(ma, prefix='MA')

		ofile.write("\nMtlSingleBRDF %s {"  % material_name)
		ofile.write("\n\tbrdf= %s;" % clean_string(brdf_name))
		ofile.write("\n}\n")

	elif no.type in ('MATERIAL','MATERIAL_EXT'):
		bus['textures']= {}
		bus['material']= no.material

		brdf= PLUGINS['BRDF'][no.material.vray.type].write(bus)

		bus['material']= ma

	elif no.type == 'MIX_RGB':
		color1= "BRDFDiffuse_no_material"
		color2= "BRDFDiffuse_no_material"
		fac= "Color(0.5,0.5,0.5)"

		brdf_name= "%s_%s_%s"%(ma.name, nt.name, no.name)

		for ns in no.inputs:
			if ns.name == 'Color1':
				node_color1= find_connected_node(nt, ns)
			elif ns.name == 'Color2':
				node_color2= find_connected_node(nt, ns)
			else:
				fac= "Color(1.0,1.0,1.0)*%.3f"%(1.0 - ns.default_value[0])
				node_fac= find_connected_node(nt, ns)

		if node_color1:
			if node_color1.type in ('MATERIAL','MATERIAL_EXT'):
				color1= "%s_MA%s" % (node_color1.material.vray.type,
									 clean_string(node_color1.material.name))

		if node_color2:
			if node_color2.type in ('MATERIAL','MATERIAL_EXT'):
				color2= "%s_MA%s" % (node_color2.material.vray.type,
									 clean_string(node_color2.material.name))

		if node_fac:
			if node_fac.type == 'TEXTURE':
				bus['mtex']= {}
				bus['mtex']['mapto']=   'node'
				bus['mtex']['slot']=    None
				bus['mtex']['texture']= node_fac.texture
				bus['mtex']['factor']=  1.0
				bus['mtex']['name']=    clean_string("NT%sNO%sTE%s" % (nt.name,
																	   no.name,
																	   node_fac.texture.name))

				# Write texture
				weights= write_texture(bus)

		else:
			weights= "weights_%s"%(clean_string(brdf_name))
			ofile.write("\nTexAColor %s {"%(weights))
			ofile.write("\n\tuvwgen= UVWGenChannel_default;")
			ofile.write("\n\ttexture= %s;"%(fac))
			ofile.write("\n}\n")

		ofile.write("\nBRDFLayered %s {"%(clean_string(brdf_name)))
		ofile.write("\n\tbrdfs= List(%s,%s);"%(color1, color2))
		ofile.write("\n\tweights= List(%s,TEDefaultBlend);"%(weights))
		ofile.write("\n\tadditive_mode= 0;") # Shellac
		ofile.write("\n}\n")

	elif no.type == 'TEXTURE':
		bus['mtex']= {}
		bus['mtex']['mapto']=   'node'
		bus['mtex']['slot']=    None
		bus['mtex']['texture']= no.texture
		bus['mtex']['factor']=  1.0
		bus['mtex']['name']=    clean_string("NT%sNO%sTE%s" % (nt.name,
															   no.name,
															   no.texture.name))

		# Write texture
		tex_name= write_texture(bus)

	elif no.type == 'INVERT':
		pass


def write_node_material(bus):
	ofile= bus['files']['materials']
	scene= bus['scene']

	ob=    bus['node']['object']
	base=  bus['node']['base']

	ma=    bus['material']

	bus['node_material']= {}
	bus['node_material']['material']=  ma
	bus['node_material']['node_tree']= ma.node_tree

	debug(scene, "Writing node material: %s" % (ma.name))

	node_tree= ma.node_tree
	for node in node_tree.nodes:
		if node.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT'):
			bus['node_material']['node']= node

			write_node(bus)

		else:
			debug(scene, "Node: %s (unsupported node type: %s)" % (node.name, node.type))

	return material_name

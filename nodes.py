'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

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
from vb25.utils import *
from vb25.textures import *
from vb25.plugins import *


def get_brdf_type(ma):
	vma= ma.vray
	if vma.type == 'MTL':
		if sce.vray.exporter.compat_mode:
			return 'BRDFLayered'
		else:
			return 'BRDFVRayMtl'
	elif vma.type == 'SSS':
		return 'BRDFSSS2Complex'
	elif vma.type == 'EMIT':
		return 'BRDFLight'
	else:
		return ''

def get_node_name(nt, node):
	nt_name= get_name(nt,"NodeTree")
	node_name= "%s_%s"%(nt_name, clean_string(node.name))
	return node_name

def find_connected_node(nt, ns):
	for n in nt.links:
		if n.to_socket == ns:
			return n.from_node
	return None

def write_node(ofile, ma, nt, no):
	debug(sce,"  Writing node: %s [%s]"%(no.name, no.type))

	if no.type == 'OUTPUT':
		brdf_name= "BRDFDiffuse_no_material"

		for ns in no.inputs:
			if ns.name == 'Color':
				color= find_connected_node(nt, ns)
				brdf_name= "%s_%s_%s"%(ma.name, nt.name, color.name)

		ofile.write("\nMtlSingleBRDF %s {"%(get_name(ma,'Material')))
		ofile.write("\n\tbrdf= %s;"%(clean_string(brdf_name)))
		ofile.write("\n}\n")

	elif no.type in ('MATERIAL','MATERIAL_EXT'):
		write_material(no.material, filters, object_params, ofile)

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
				color1= get_name(node_color1.material,'%s_Material' % get_brdf_type(node_color1.material))

		if node_color2:
			if node_color2.type in ('MATERIAL','MATERIAL_EXT'):
				color2= get_name(node_color2.material,'%s_Material' % get_brdf_type(node_color2.material))

		if node_fac:
			if node_fac.type == 'TEXTURE':
				weights= write_texture(ofile, sce, {'material': ma,
													'texture': node_fac.texture})
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
		tex_name= write_texture(ofile, sce, {'material': ma,
											 'texture': no.texture})

	elif no.type == 'INVERT':
		debug(sce,"Node type \"%s\" is currently not implemented."%(no.type))

	else:
		debug(sce,"Node: %s (unsupported node type: %s)"%(no.name,no.type))


def write_node_material(params):
	ofile= params['file']
	ob=    params['object']
	ma=    params['material']
	uvs=   params['object']['uv_ids']

	params['node_tree']= node_tree


	debug(sce,"Writing node material: %s"%(ma.name))
	node_tree= ma.node_tree
	for node in node_tree.nodes:
		params['node']= node

		if n.type in ('OUTPUT', 'MATERIAL', 'MIX_RGB', 'TEXTURE', 'MATERIAL_EXT', 'INVERT'):
			write_node(ofile, ma, nt, n)
		else:
			debug(sce,"Node: %s (unsupported node type: %s)"%(n.name, n.type))


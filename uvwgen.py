'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Friday, 29 April 2011 [08:58]"

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

''' vb modules '''
from vb25.utils import *
from vb25.plugins import *


def write_UVWGenProjection(bus):
	TYPE= {
		'NONE':   0,
		'FLAT':   1,
		'SPHERE': 2,
		'TUBE':   3,
		'BALL':   4,
		#'CUBE':   5, # cubic
		'CUBE':   6,  # triplanar (looks like Cube actually)
		'TRI':    6,  # triplanar
		'PERS':   8,
	}

	scene= bus['scene']
	ofile= bus['files']['textures']

	texture= bus['mtex']['texture']

	VRayTexture= texture.vray
	VRaySlot=    texture.vray_slot

	uvwgen= "UVP%s" % (bus['mtex']['name'])

	ob= get_orco_object(scene, bus['node']['object'], VRayTexture)

	ofile.write("\nUVWGenProjection %s {" % uvwgen)
	ofile.write("\n\ttype= %d;" % TYPE[VRayTexture.mapping])
	if ob:
		uvw_transform= mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X') # To match Blender mapping
		uvw_transform*= ob.matrix_world.copy().inverted()                    # To remove object transfrom
		ofile.write("\n\tuvw_transform= %s; // Object: %s" % (a(scene, transform(uvw_transform)), ob.name))
	# Add:
	#  - camera_settings
	#  - camera_view
	ofile.write("\n}\n")

	return uvwgen


def write_UVWGenChannel(bus):
	ofile= bus['files']['textures']
	sce=   bus['scene']

	texture= bus['mtex']['texture']
	slot=    bus['mtex'].get('slot')

	uvw_name= "UVC%s" % (bus['mtex']['name'])

	VRaySlot=    texture.vray_slot
	VRayTexture= texture.vray
	
	uvw_channel= 1
	uvwgen=      None

	if VRayTexture.texture_coords == 'ORCO':
		uvwgen= write_UVWGenProjection(bus)

	else:
		if slot and hasattr(slot, 'uv_layer'):
			uvw_channel= get_uv_layer_id(bus['uvs'], slot.uv_layer)

	ofile.write("\nUVWGenChannel %s {" % uvw_name)
	ofile.write("\n\tuvw_channel= %i;" % uvw_channel)
	if slot:
		scale_x= 0.001 if abs(slot.scale[0]) < 0.001 else abs(slot.scale[0])
		scale_y= 0.001 if abs(slot.scale[1]) < 0.001 else abs(slot.scale[1])
		scale_z= 0.001 if abs(slot.scale[2]) < 0.001 else abs(slot.scale[2])

		uvw_transform= mathutils.Matrix.Rotation(VRaySlot.texture_rot, 3, 'Z')

		ofile.write("\n\tuvw_transform= interpolate((%i, Transform(" % sce.frame_current)
		ofile.write("\n\t\tMatrix(")
		ofile.write("\n\t\t\tVector(%.6f, %.6f, %.6f)*%.3f," % (uvw_transform[0][0], uvw_transform[0][1], uvw_transform[0][2],
																(VRayTexture.tile_u if VRayTexture.tile in ('TILEUV','TILEU') else 1.0) / scale_x))

		ofile.write("\n\t\t\tVector(%.6f, %.6f, %.6f)*%.3f," % (uvw_transform[1][0], uvw_transform[1][1], uvw_transform[1][2],
																(VRayTexture.tile_v if VRayTexture.tile in ('TILEUV','TILEV') else 1.0) / scale_y))

		ofile.write("\n\t\t\tVector(%.6f, %.6f, %.6f)*%.3f"  % (uvw_transform[2][0], uvw_transform[2][1], uvw_transform[2][2],
																1.0  / scale_z))
		ofile.write("\n\t\t),")
		ofile.write("\n\t\tVector(%.6f, %.6f, %.6f)" % (slot.offset[0], slot.offset[1], slot.offset[2]))
		ofile.write("\n\t)));")

		ofile.write("\n\twrap_u= %d;" % (2 if (VRayTexture.mirror_u or slot.scale[0] < 0) else 0))
		ofile.write("\n\twrap_v= %d;" % (2 if (VRayTexture.mirror_v or slot.scale[1] < 0) else 0))
		ofile.write("\n\twrap_w= %d;" % (2 if                          slot.scale[2] < 0  else 0))
	else:
		ofile.write("\n\twrap_u= %d;" % (2 if VRayTexture.mirror_u else 0))
		ofile.write("\n\twrap_v= %d;" % (2 if VRayTexture.mirror_v else 0))

	# Optional UVWGen from which the initial uvw coordinates
	# will be taken, instead of the surface point
	if uvwgen:
		ofile.write("\n\tuvwgen= %s;" % uvwgen)
	ofile.write("\n}\n")

	return uvw_name


def write_UVWGenEnvironment(bus):
	MAPPING_TYPE= {
		'SPHERE':  'spherical',
		'ANGULAR': 'angular',
		'SCREEN':  'screen',
		'TUBE':    'max_cylindrical',
		'CUBIC':   'cubic',
		'MBALL':   'mirror_ball',
	}

	scene= bus['scene']
	ofile= bus['files']['textures']

	slot=     bus['mtex']['slot']
	texture=  bus['mtex']['texture']
	tex_name= bus['mtex']['name']

	uvw_name= "UVE%s" % (tex_name)

	VRayTexture= texture.vray
	VRaySlot=    texture.vray_slot

	uvw_matrix= mathutils.Matrix.Rotation(VRaySlot.texture_rotation_h, 4, 'Z')
	if VRayTexture.environment_mapping not in ('SCREEN'):
		uvw_matrix*= mathutils.Matrix.Rotation(VRaySlot.texture_rotation_v, 4, 'Y')

	ofile.write("\nUVWGenEnvironment %s {" % uvw_name)
	ofile.write("\n\tmapping_type= \"%s\";" % MAPPING_TYPE[VRayTexture.environment_mapping])
	ofile.write("\n\tuvw_transform= %s;" % transform(uvw_matrix))
	ofile.write("\n}\n")
	
	return uvw_name


def write_uvwgen(bus):
	slot=    bus['mtex']['slot']
	texture= bus['mtex']['texture']

	if type(slot) is bpy.types.WorldTextureSlot:
		return write_UVWGenEnvironment(bus)

	else:
		VRayTexture= texture.vray

		uvwgen= write_UVWGenChannel(bus)

		# Cache uvwgen under texture name
		bus['cache']['uvwgen'][ bus['mtex']['name'] ]= uvwgen

		# We need to pass normal uvwgen to BRDFBump
		if 'material' in bus and bus['mtex']['mapto'] == 'normal':
			bus['material']['normal_uvwgen']= uvwgen
		
		return uvwgen

	


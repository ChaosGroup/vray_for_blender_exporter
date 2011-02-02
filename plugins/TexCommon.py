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


TYPE= 'TEXTURE'

ID=   'TEXCOMMON'
NAME= 'General texture setings'
DESC= "Common V-Ray Texture settings."
PID=   100

PARAMS= (
)


''' Blender modules '''
import bpy
from bpy.props import *


def add_properties(rna_pointer):
	rna_pointer.name= StringProperty(
		name= "V-Ray Texture name",
		description= "V-Ray texture name for internal usage.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

	rna_pointer.placement_type= EnumProperty(
		name= "Placement type",
		description= "Image texure placement type.",
		items= (
			('FULL', "Full",  "The whole texture is valid."),
			('CROP', "Crop",  "Crop texture."),
			('PLACE',"Place", "Place texture."),
		),
		default= 'FULL'
	)

	rna_pointer.texture_coords= EnumProperty(
		name= "Coords",
		description= "Image texure placement type.",
		items= (
			('ORCO', "Object", "Generated coordinates."),
			('UV',   "UV",     "Mesh UV coordinates."),
		),
		default= 'UV'
	)

	rna_pointer.tile= EnumProperty(
		name= "Tile",
		description= "Tile type.",
		items= (
			('NOTILE', "No tile", "No tiling."),
			('TILEUV', "Tile UV", "Tile in UV."),
			('TILEU',  "Tile U",  "Tile in U."),
			('TILEV',  "Tile V",  "Tile in V."),
		),
		default= 'TILEUV'
	)

	rna_pointer.mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('FLAT',   "Flat",        "Planar projection."),
			('CUBE',   "Cube",        "Cubic projection."),
			('SPHERE', "Sphere",      "Spherical projection."),
			('TUBE',   "Tube",        "Cylindrical projection."),
			('BALL',   "Ball",        "Ball projection."),
			('TRI',    "Triplanar",   "Triplanar projection."),
			('PERS',   "Perspective", "Perspective projection."),
		),
		default= 'FLAT'
	)

	rna_pointer.environment_mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('SCREEN',  "Screen",      "Planar projection."),
			('CUBIC',   "Cube",        "Cubic projection."),
			('SPHERE',  "Sphere",      "Spherical projection."),
			('TUBE',    "Tube",        "Cylindrical projection."),
			('ANGULAR', "Angular",     "Angular projection."),
			('MBALL',   "Mirror ball", "Mirror ball projection."),
		),
		default= 'SPHERE'
	)

	rna_pointer.object= StringProperty(
		name= "Mapping Object",
		description= "Object to use for mapping generation.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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

import bpy


TYPE = 'GEOMETRY'
ID   = 'GeomStaticMesh'
NAME = 'Mesh'
DESC = "Mesh settings"


def add_properties(rna_pointer):
	class GeomStaticMesh(bpy.types.PropertyGroup):
		dynamic_geometry = bpy.props.BoolProperty(
			name        = "Dynamic geometry",
			description = "Instead of copying the mesh many times in the BSP tree, only the bounding box will be present many times and ray intersections will occur in a separate object space BSP tree",
			default     =  False
		)
		use_for_ptex = bpy.props.BoolProperty(
			name        = "Use For PTex",
			description = "Turn this option on if this object will be used with PTex",
			default     =  False
		)
	bpy.utils.register_class(GeomStaticMesh)

	rna_pointer.GeomStaticMesh = bpy.props.PointerProperty(
		name        = "V-Ray Satic Mesh",
		type        =  GeomStaticMesh,
		description = "V-Ray static mesh settings"
	)

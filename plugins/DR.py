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

from bpy.props import *


TYPE= 'SETTINGS'

ID=   'DR'
NAME= 'Distributed render'
DESC= "Distributed render options"

PARAMS= (
)


def add_properties(rna_pointer):
	class VRayDR(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(VRayDR)

	rna_pointer.VRayDR= PointerProperty(
		name= "Distributed rendering",
		type=  VRayDR,
		description= "Distributed rendering settings"
	)

	VRayDR.on= BoolProperty(
		name= "Distributed rendering",
		description= "Distributed rendering",
		default= False
	)

	VRayDR.port= IntProperty(
		name= "Distributed rendering port",
		description= "Distributed rendering port",
		min= 0,
		max= 65535,
		default= 20204
	)

	VRayDR.shared_dir= StringProperty(
		name= "Shared directory",
		subtype= 'DIR_PATH',
		description= "Distributed rendering shader directory"
	)

	VRayDR.share_name= StringProperty(
		name= "Share name",
		default= "VRAYDR",
		description= "Share name"
	)

	VRayDR.type= EnumProperty(
		name= "Type",
		description= "Distributed rendering network type",
		items= (
			('WW', "Windows - Windows", "Window master & Windows nodes"),
			('WU', "Windows - Unix (TODO)", "Window master & Unix nodes"),
			('UU', "Unix - Unix",       "Unix master & Unix nodes"),
			('UW', "Unix - Windows (TODO)", "Unix master & Windows nodes"),
		),
		default= 'WW'
	)


	class VRayRenderNode(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(VRayRenderNode)

	VRayDR.nodes= CollectionProperty(
		name= "Render Nodes",
		type=  VRayRenderNode,
		description= "V-Ray render nodes"
	)

	VRayDR.nodes_selected= IntProperty(
		name= "Render Node Index",
		default= -1,
		min= -1,
		max= 100
	)

	VRayRenderNode.address= StringProperty(
		name= "IP/Hostname",
		description= "Render node IP or hostname"
	)

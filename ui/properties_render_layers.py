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

from pynodes_framework import idref

from vb25.ui import classes


class VRayPanelRenderElements(classes.VRayRenderLayersPanel):
	bl_label   = "Render Elements"
	bl_options = {'HIDE_HEADER'}

	def draw(self, context):
		layout = self.layout

		VRayScene = context.scene.vray
		
		split = layout.split()
		row = split.row(align=True)
		idref.draw_idref(row, VRayScene, 'ntree', text="Node Tree")
		row.operator("vray.add_nodetree_scene", icon='ZOOMIN', text="")


def GetRegClasses():
	return (
		VRayPanelRenderElements,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

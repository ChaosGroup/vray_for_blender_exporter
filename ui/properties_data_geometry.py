#
# V-Ray For Blender
#
# http://chaosgroup.com
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

from vb30.ui import classes


def GetContextData(context):
	if context.active_object.type == 'MESH':
		return context.mesh
	else:
		return context.curve
	return data


class VRAY_DP_tools(classes.VRayGeomPanel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}

	def draw_header(self, context):
		self.layout.label(text="", icon='VRAY_LOGO_MONO')

	def draw(self, context):
		wide_ui= context.region.width > classes.narrowui

		layout= self.layout

		data = GetContextData(context)

		VRayMesh = data.vray
		GeomMeshFile= VRayMesh.GeomMeshFile

		layout.label(text="Generate VRayProxy:")

		split= layout.split()
		col= split.column()
		col.prop(GeomMeshFile, 'dirpath')
		col.prop(GeomMeshFile, 'filename')
		col.separator()
		col.prop(GeomMeshFile, 'proxy_attach_mode', text="Attach mode")

		split= layout.split()
		col= split.column()
		col.prop(GeomMeshFile, 'animation')
		sub= col.column()
		sub.active= GeomMeshFile.animation
		sub.prop(GeomMeshFile, 'add_velocity')
		sub.prop(GeomMeshFile, 'animation_range', text="Range")
		if GeomMeshFile.animation_range == 'MANUAL':
			sub= sub.column(align=True)
			sub.prop(GeomMeshFile, 'frame_start')
			sub.prop(GeomMeshFile, 'frame_end')
		if wide_ui:
			col= split.column()
		col.prop(GeomMeshFile, 'add_suffix')
		col.prop(GeomMeshFile, 'apply_transforms')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.operator('vray.create_proxy', icon='OUTLINER_OB_MESH')


def GetRegClasses():
	return (
		VRAY_DP_tools,
	)


def register():
	from bl_ui import properties_data_mesh
	for member in dir(properties_data_mesh):
		subclass = getattr(properties_data_mesh, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.add(compatEngine)
		except:
			pass
	del properties_data_mesh

	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	from bl_ui import properties_data_mesh
	for member in dir(properties_data_mesh):
		subclass = getattr(properties_data_mesh, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.remove(compatEngine)
		except:
			pass
	del properties_data_mesh

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

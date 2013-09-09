'''

  V-Ray/Blender

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

''' vb modules '''
from vb25.ui.ui import *


from bl_ui import properties_data_mesh
for member in dir(properties_data_mesh):
	subclass= getattr(properties_data_mesh, member)
	try:
		subclass.COMPAT_ENGINES.add('VRAY_RENDER')
		subclass.COMPAT_ENGINES.add('VRAY_RENDER_PREVIEW')
	except:
		pass
del properties_data_mesh


class VRAY_DP_override(VRayDataPanel, bpy.types.Panel):
	bl_label   = "Options"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDERER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return (context.mesh and engine_poll(__class__, context))

	def draw(self, context):
		wide_ui = context.region.width > narrowui
		layout  = self.layout

		VRayMesh = context.mesh.vray
		GeomStaticMesh = VRayMesh.GeomStaticMesh

		layout.prop(VRayMesh, 'override')

		if VRayMesh.override:
			split = layout.split()
			row = split.row()
			row.prop(VRayMesh, 'override_type', expand=True)

			if VRayMesh.override_type == 'VRAYPROXY':
				GeomMeshFile = VRayMesh.GeomMeshFile

				split = layout.split()
				col = split.column()
				col.prop(GeomMeshFile, 'file')
				col.prop(GeomMeshFile, 'anim_type')

				split = layout.split()
				col = split.column(align=True)
				col.prop(GeomMeshFile, 'anim_speed')
				if wide_ui:
					col = split.column()
				col.prop(GeomMeshFile, 'anim_offset')

				layout.separator()
				layout.operator('vray.proxy_load_preview', icon='OUTLINER_OB_MESH', text="Load Preview Mesh")

		else:
			layout.prop(GeomStaticMesh, 'dynamic_geometry')


class VRAY_DP_tools(VRayDataPanel, bpy.types.Panel):
	bl_label   = "Tools"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDERER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return (context.mesh and engine_poll(__class__, context))

	def draw(self, context):
		wide_ui= context.region.width > narrowui

		layout= self.layout

		VRayMesh=     context.mesh.vray
		GeomMeshFile= VRayMesh.GeomMeshFile

		layout.label(text="Generate VRayProxy:")

		split= layout.split()
		col= split.column()
		col.prop(GeomMeshFile, 'dirpath')
		col.prop(GeomMeshFile, 'filename')
		col.separator()
		col.prop(GeomMeshFile, 'mode', text="Attach mode")

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

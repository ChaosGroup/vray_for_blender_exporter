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


narrowui= 200


def base_poll(cls, context):
	rd= context.scene.render
	return (rd.engine in cls.COMPAT_ENGINES)

class VRayDataPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'

class VRayMaterialPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'material'

class VRayObjectPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'object'

class VRayRenderPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render'

class VRayScenePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'scene'

class VRayTexturePanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'

class VRayWorldPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'world'

	@classmethod
	def poll(cls, context):
		rd= context.scene.render
		return (context.world) and (rd.engine in cls.COMPAT_ENGINES)


def factor_but(layout, rna_pointer, use, factor, label= None):
	row= layout.row(align=True)
	row.prop(rna_pointer,
			 use,
			 text= "")
	sub= row.row()
	sub.active= getattr(rna_pointer, use)
	sub.prop(rna_pointer,
			 factor,
			 slider=True,
			 text= label if label else "")


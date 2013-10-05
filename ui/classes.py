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


VRayEngines = {
	'VRAY_RENDER',
	'VRAY_RENDER_PREVIEW',
	'VRAY_RENDER_RT',
	'VRAY_RENDERER'
}

narrowui = 200


def GetContextType(context):
	if hasattr(context, 'node'):
		return 'NODE'

	if hasattr(context, 'material'):
		return 'MATERIAL'
	
	return None


def GetRegionWidthFromContext(context):
	contextType = GetContextType(context)
	if contextType == 'NODE':
		return context.node.width
	elif hasattr(context, 'region'):
		return context.region.width
	# Assume wide region width
	return 1024


def context_tex_datablock(context):
	idblock = context.material
	if idblock:
		return idblock

	idblock = context.lamp
	if idblock:
		return idblock

	idblock = context.world
	if idblock:
		return idblock

	idblock = context.brush
	if idblock:
		return idblock

	if context.particle_system:
		idblock = context.particle_system.settings

	return idblock


def PollEngine(cls, context):
	rd = context.scene.render
	return rd.engine in cls.COMPAT_ENGINES


class VRayPanel(bpy.types.Panel):
	COMPAT_ENGINES = VRayEngines


class VRayDataPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'

	@classmethod
	def poll(cls, context):
		return PollEngine(cls, context)


class VRayGeomPanel(VRayDataPanel):
	incompatTypes  = {'LAMP', 'CAMERA', 'ARMATURE', 'EMPTY'}

	@classmethod
	def poll(cls, context):
		return context.object and context.object.type not in cls.incompatTypes and PollEngine(cls, context)


class VRayLampPanel(VRayDataPanel):
	@classmethod
	def poll(cls, context):
		return context.lamp and PollEngine(cls, context)


class VRayMaterialPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'material'

	@classmethod
	def poll(cls, context):
		return context.material and PollEngine(cls, context)


class VRayObjectPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'object'

	incompatTypes  = {'LAMP', 'CAMERA', 'ARMATURE', 'EMPTY'}

	@classmethod
	def poll(cls, context):
		return context.object and context.object.type not in cls.incompatTypes and PollEngine(cls, context)


class VRayParticlePanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'particle'

	@classmethod
	def poll(cls, context):
		return context.particle_system and PollEngine(cls, context)


class VRayRenderPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render'

	@classmethod
	def poll(cls, context):
		return PollEngine(cls, context)


class VRayRenderLayersPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'render_layer'

	@classmethod
	def poll(cls, context):
		return PollEngine(cls, context)


class VRayScenePanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'scene'

	@classmethod
	def poll(cls, context):
		return PollEngine(cls, context)


class VRayTexturePanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'texture'

	@classmethod
	def poll(cls, context):
		return context.texture and PollEngine(cls, context)


class VRayWorldPanel(VRayPanel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'world'
	
	@classmethod
	def poll(cls, context):
		return context.world and PollEngine(cls, context)


# List item:
#  <item name> <item use-flag>
#
class VRayListUse(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		layout.label(item.name)
		layout.prop(item, 'use')


class VRayList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		layout.label(item.name)


def GetRegClasses():
	return (
		VRayListUse,
		VRayList,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)


def unregister():
	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

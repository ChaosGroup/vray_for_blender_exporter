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


''' Python modules '''
import os

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui import *


class VRAY_OT_effect_add(bpy.types.Operator):
	bl_idname=      'vray.effect_add'
	bl_label=       "Add Effect"
	bl_description= "Add effect."

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		VRayEffects.effects.add()
		VRayEffects.effects[-1].name= "Effect"

		return{'FINISHED'}


class VRAY_OT_effect_remove(bpy.types.Operator):
	bl_idname=      'vray.effect_remove'
	bl_label=       "Remove Effect"
	bl_description= "Remove effect."

	def execute(self, context):
		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects
				
		if VRayEffects.effects_selected >= 0:
			VRayEffects.effects.remove(VRayEffects.effects_selected)
			VRayEffects.effects_selected-= 1

		return{'FINISHED'}

'''
  GUI
'''
class VRAY_SP_effects(VRayScenePanel, bpy.types.Panel):
	bl_label   = "Effects"
	bl_options = {'DEFAULT_CLOSED'}
	
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		wide_ui= context.region.width > narrowui

		VRayScene= context.scene.vray

		VRayEffects= VRayScene.VRayEffects

		split= layout.split()
		row= split.row()
		row.template_list(VRayEffects, 'effects',
						  VRayEffects, 'effects_selected',
						  rows= 3)
		col= row.column(align=True)
		col.operator('vray.effect_add',    text="", icon="ZOOMIN")
		col.operator('vray.effect_remove', text="", icon="ZOOMOUT")

		if VRayEffects.effects_selected >= 0:
			layout.separator()

			effect= VRayEffects.effects[VRayEffects.effects_selected]

			split= layout.split()
			col= split.column()
			col.prop(effect, 'name')
			col.prop(effect, 'type')

			layout.separator()

			if effect.type == 'FOG':
				EnvironmentFog= effect.EnvironmentFog

				split= layout.split()
				col= split.column()
				col.prop(EnvironmentFog, 'color')
				if wide_ui:
					col= split.column()
				col.prop(EnvironmentFog, 'emission')

				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop(EnvironmentFog, 'distance')
				col.prop(EnvironmentFog, 'density')
				col.prop(EnvironmentFog, 'subdivs')
				col.prop(EnvironmentFog, 'scatter_gi')
				if EnvironmentFog.scatter_gi:
					col.prop(EnvironmentFog, 'scatter_bounces')
				col.prop(EnvironmentFog, 'use_height')
				if EnvironmentFog.use_height:
					col.prop(EnvironmentFog, 'height')
				if wide_ui:
					col= split.column()
				#col.prop(EnvironmentFog, 'fade_out_type')
				col.prop(EnvironmentFog, 'fade_out_radius')
				col.prop(EnvironmentFog, 'affect_background')
				col.prop(EnvironmentFog, 'use_shade_instance')
				col.prop(EnvironmentFog, 'simplify_gi')

				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop(EnvironmentFog, 'light_mode')
				col.prop(EnvironmentFog, 'fade_out_mode')

				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop(EnvironmentFog, 'step_size')
				col.prop(EnvironmentFog, 'max_steps')
				if wide_ui:
					col= split.column()
				col.prop(EnvironmentFog, 'tex_samples')
				col.prop(EnvironmentFog, 'cutoff_threshold')

				#col.prop(EnvironmentFog, 'per_object_fade_out_radius')
				#col.prop(EnvironmentFog, 'yup')

				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop_search(EnvironmentFog, 'objects',
								context.scene, 'objects', text="Objects")
				col.prop_search(EnvironmentFog, 'groups',
								bpy.data, 'groups', text="Groups")

			elif effect.type == 'TOON':
				VolumeVRayToon= effect.VolumeVRayToon

				split= layout.split()
				col= split.column()
				col.prop(VolumeVRayToon, 'lineColor', text="")
				col.prop(VolumeVRayToon, 'widthType')
				col.prop(VolumeVRayToon, 'lineWidth')
				col.prop(VolumeVRayToon, 'opacity')
				if wide_ui:
					col= split.column()
				col.prop(VolumeVRayToon, 'normalThreshold')
				col.prop(VolumeVRayToon, 'overlapThreshold')
				col.prop(VolumeVRayToon, 'hideInnerEdges')
				col.prop(VolumeVRayToon, 'doSecondaryRays')
				col.prop(VolumeVRayToon, 'traceBias')

				layout.separator()

				split= layout.split()
				col= split.column()
				col.prop(VolumeVRayToon, 'excludeType', text="")
				col.prop_search(VolumeVRayToon, 'excludeList_objects',
								context.scene, 'objects', text="Objects")
				col.prop_search(VolumeVRayToon, 'excludeList_groups',
								bpy.data, 'groups', text="Groups")

				# col.prop(VolumeVRayToon, 'lineColor_tex')
				# col.prop(VolumeVRayToon, 'lineWidth_tex')
				# col.prop(VolumeVRayToon, 'opacity_tex')
				# col.prop(VolumeVRayToon, 'distortion_tex')

			else:
				split= layout.split()
				col= split.column()
				col.label(text="Strange, but this effect type doesn\'t exist...")

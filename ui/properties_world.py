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

from vb25.ui      import classes
from vb25.plugins import PLUGINS


class VRAY_WP_context_world(classes.VRayWorldPanel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
        
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        world = context.world
        space = context.space_data
        rd = context.scene.render

        texture_count = world and len(world.texture_slots.keys())

        split = layout.split(percentage=0.85)
        if scene:
            split.template_ID(scene, "world", new="world.new")
        elif world:
            split.template_ID(space, "pin_id")

        VRayWorld = context.world.vray

        layout.separator()
        layout.prop(VRayWorld, 'global_light_level', slider=True)

        layout.separator()
        if VRayWorld.nodetree:
            layout.prop_search(VRayWorld, "nodetree", bpy.data, "node_groups")
        else:
            layout.operator("vray.add_world_nodetree", icon='NODETREE', text="Add Node Tree")


class VRAY_WP_effects(classes.VRayWorldPanel):
    bl_label   = "Effects"
    bl_options = {'DEFAULT_CLOSED'}

    
    def draw_header(self, context):
        VRayScene= context.scene.vray
        self.layout.prop(VRayScene.VRayEffects, 'use', text="")

    def draw(self, context):
        layout= self.layout

        wide_ui= context.region.width > classes.narrowui

        VRayScene= context.scene.vray
        VRayEffects= VRayScene.VRayEffects

        layout.active= VRayEffects.use

        split= layout.split()
        row= split.row()
        row.template_list("VRayListUse", "",
                          VRayEffects, 'effects',
                          VRayEffects, 'effects_selected',
                          rows= 4)
        col= row.column()
        sub= col.row()
        subsub= sub.column(align=True)
        subsub.operator('vray.effect_add',    text="", icon="ZOOMIN")
        subsub.operator('vray.effect_remove', text="", icon="ZOOMOUT")
        sub= col.row()
        subsub= sub.column(align=True)
        subsub.operator("vray.effect_up",   icon='MOVE_UP_VEC',   text="")
        subsub.operator("vray.effect_down", icon='MOVE_DOWN_VEC', text="")

        if VRayEffects.effects_selected >= 0:
            layout.separator()

            effect= VRayEffects.effects[VRayEffects.effects_selected]

            if wide_ui:
                split= layout.split(percentage=0.2)
            else:
                split= layout.split()
            col= split.column()
            col.label(text="Name:")
            if wide_ui:
                col= split.column()
            row= col.row(align=True)
            row.prop(effect, 'name', text="")

            if wide_ui:
                split= layout.split(percentage=0.2)
            else:
                split= layout.split()
            col= split.column()
            col.label(text="Type:")
            if wide_ui:
                col= split.column()
            col.prop(effect, 'type', text="")

            layout.separator()

            # Box border
            box = layout.box()
            box.active = effect.use

            if effect.type == 'FOG':
                PLUGINS['SETTINGS']['SettingsEnvironment'].draw_EnvironmentFog(context, box, effect)

            elif effect.type == 'TOON':
                PLUGINS['SETTINGS']['SettingsEnvironment'].draw_VolumeVRayToon(context, box, effect)


def GetRegClasses():
    return (
        VRAY_WP_context_world,
        VRAY_WP_effects,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

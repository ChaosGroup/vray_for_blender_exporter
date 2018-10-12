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

from vb30.ui      import classes
from vb30.lib     import DrawUtils
from vb30.plugins import PLUGINS



class VRayPanelWorldPreview(classes.VRayWorldPanel):
    bl_label = "Preview"
    bl_options = {'HIDE_HEADER'}

    COMPAT_ENGINES = {'VRAY_RENDER_RT'}

    def draw(self, context):
        self.layout.template_preview(context.world)


class VRAY_WP_context_world(classes.VRayPanel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = 'world'
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        world = context.world
        space = context.space_data

        if scene:
            layout.template_ID(scene, "world", new="world.new")
        elif world:
            layout.template_ID(space, "pin_id")

        if context.world:
            VRayWorld = context.world.vray

            layout.separator()
            layout.prop(VRayWorld, 'global_light_level', slider=True)

            classes.NtreeWidget(layout, VRayWorld, "World Tree", "vray.add_nodetree_world", 'WORLD')

            if not classes.TreeHasNodes(VRayWorld.ntree):
                return

            activeNode = VRayWorld.ntree.nodes[-1]

            layout.separator()
            classes.DrawNodePanel(context, self.layout, activeNode, PLUGINS)


def GetRegClasses():
    return (
        VRayPanelWorldPreview,
        VRAY_WP_context_world,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

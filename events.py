#
# V-Ray/Blender
#
# http://www.chaosgroup.com
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

from .lib import BlenderUtils

from .nodes.tree_defaults import AddMaterialNodeTree
from . import engine
import _vray_for_blender_rt

@bpy.app.handlers.persistent
def dr_nodes_store(e):
    bpy.ops.vray.dr_nodes_save()


@bpy.app.handlers.persistent
def dr_nodes_restore(e):
    bpy.ops.vray.dr_nodes_load()


@bpy.app.handlers.persistent
def event_shutdown(e):
    engine.shutdown()


@bpy.app.handlers.persistent
def new_material_ntree(ma):
    AddMaterialNodeTree(ma)
    bpy.ops.object.material_slot_add()
    bpy.ops.vray.show_ntree(data='MATERIAL', ntree_name=ma.vray.ntree.name)


@bpy.app.handlers.persistent
def update_world_preview(ob):
    if not hasattr(ob, 'type'):
        return
    if not ob.type == 'CAMERA':
        return
    sce = bpy.context.scene
    world = sce.world
    if not world:
        return
    ntree = world.vray.ntree
    if not ntree:
        return

    _vray_for_blender_rt.updatePreview(bpy.context.as_pointer(), BlenderUtils.NC_WORLD)


@bpy.app.handlers.persistent
def update_material_preview(sce):
    pass
    _vray_for_blender_rt.updatePreview(bpy.context.as_pointer(), BlenderUtils.NC_MATERIAL)


def register():
    BlenderUtils.AddEvent(bpy.app.handlers.save_post, dr_nodes_store)
    BlenderUtils.AddEvent(bpy.app.handlers.load_post, dr_nodes_restore)
    BlenderUtils.AddEvent(bpy.app.handlers.exit,      event_shutdown)

    BlenderUtils.AddEvent(bpy.app.handlers.new_material, new_material_ntree)

    BlenderUtils.AddEvent(bpy.app.handlers.object_update, update_world_preview)

    BlenderUtils.AddEvent(bpy.app.handlers.frame_change_post, update_material_preview)


def unregister():
    BlenderUtils.DelEvent(bpy.app.handlers.save_post, dr_nodes_store)
    BlenderUtils.DelEvent(bpy.app.handlers.load_post, dr_nodes_restore)
    BlenderUtils.DelEvent(bpy.app.handlers.exit,      event_shutdown)

    BlenderUtils.DelEvent(bpy.app.handlers.new_material, new_material_ntree)

    BlenderUtils.DelEvent(bpy.app.handlers.object_update, update_world_preview)

    BlenderUtils.DelEvent(bpy.app.handlers.frame_change_post, update_material_preview)

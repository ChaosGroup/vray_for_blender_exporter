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

import random
import bpy

from vb30.nodes import utils as NodeUtils


class VRayOpGenRandomMtlId(bpy.types.Operator):
    bl_idname      = "vray.gen_random_mtl_ids"
    bl_label       = "Randomize Material IDs"
    bl_description = "Randomize material IDs"

    def execute(self, context):
        for nt in bpy.data.node_groups:
            for n in nt.nodes:
                if n.bl_idname in {'VRayNodeMetaStandardMaterial'}:
                    sock = NodeUtils.getInputSocketByVRayAttr(n, 'material_id_color')
                    if sock:
                        m_id_color = (random.random(), random.random(), random.random())
                        sock.value = m_id_color
        return {'FINISHED'}


def GetRegClasses():
    return (
        VRayOpGenRandomMtlId,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

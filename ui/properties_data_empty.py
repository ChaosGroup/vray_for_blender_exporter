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

from vb25.ui import classes


class VRAY_DP_empty(classes.VRayDataPanel):
    bl_label   = "Override"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'EMPTY' and classes.VRayDataPanel.poll(context)

    def draw(self, context):
        wide_ui = context.region.width > classes.narrowui
        layout  = self.layout
        
        VRayObject = context.object.vray

        box = layout.box()

        box.prop(VRayObject, 'overrideWithScene')

        if VRayObject.overrideWithScene:
            split = box.split()
            col = split.column()
            col.prop(VRayObject, 'sceneFilepath')
            col.prop(VRayObject, 'sceneDirpath')
            
            split = box.split()
            col = split.column()
            col.prop(VRayObject, 'sceneReplace')
            col.prop(VRayObject, 'sceneUseTransform')
            
            split = box.split()
            col = split.column()
            col.prop(VRayObject, 'sceneAddNodes')
            col.prop(VRayObject, 'sceneAddMaterials')
            col.prop(VRayObject, 'sceneAddLights')
            if wide_ui:
                col = split.column()
            col.prop(VRayObject, 'sceneAddCameras')
            col.prop(VRayObject, 'sceneAddEnvironment')


def register():
    bpy.utils.register_class(VRAY_DP_empty)


def unregister():
    bpy.utils.unregister_class(VRAY_DP_empty)

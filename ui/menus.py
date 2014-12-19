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


class VRayOpSetCamera(bpy.types.Operator):
    bl_idname = "vray.set_camera"
    bl_label = "Set Active Camera"

    camera = bpy.props.PointerProperty(type=bpy.types.Object)

    def execute(self, context):
        if self.camera:
            context.scene.camera = self.camera
        return {'FINISHED'}


class VRayMenuActiveCamera(bpy.types.Menu):
    bl_idname = "vray.active_camera"
    bl_label = "Set Active Camera"

    def draw(self, context):
        self.layout.operator('vray.flip_resolution', icon='FILE_REFRESH')
        self.layout.separator()

        haveCameras = False
        for ob in context.scene.objects:
            if not ob.type in {'CAMERA'}:
                continue
            haveCameras = True
            menuItemName = ob.name
            if ob == context.scene.camera:
                menuItemName += " *"
            self.layout.operator('vray.set_camera', text=menuItemName, icon='CAMERA_DATA').camera = ob
        if not haveCameras:
            self.layout.label("No camera objects found...")



########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayOpSetCamera,
        VRayMenuActiveCamera,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

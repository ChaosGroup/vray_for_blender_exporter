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

from vb30.ui import classes


# Based on SCENE_PT_scene
#
class VRayPanelScene(classes.VRayScenePanel):
	bl_label = "Scene"

	def draw(self, context):
		layout = self.layout

		scene = context.scene
		VRayScene = scene.vray

		layout.prop(scene, "camera")
		layout.prop(scene, "background_set", text="Background")
		layout.prop(scene, "active_clip", text="Active Clip")

		classes.NtreeWidget(layout, VRayScene, "Channels Tree", "vray.add_nodetree_scene", 'SCENE')


def GetRegClasses():
	return (
		VRayPanelScene,
	)


def register():
	for regClass in GetRegClasses():
		bpy.utils.register_class(regClass)

	from bl_ui import properties_scene
	for member in dir(properties_scene):
		if member in {'SCENE_PT_scene'}:
			continue
		subclass = getattr(properties_scene, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.add(compatEngine)
		except:
			pass
	del properties_scene



def unregister():
	from bl_ui import properties_scene
	for member in dir(properties_scene):
		subclass = getattr(properties_scene, member)
		try:
			for compatEngine in classes.VRayEngines:
				subclass.COMPAT_ENGINES.remove(compatEngine)
		except:
			pass
	del properties_scene

	for regClass in GetRegClasses():
		bpy.utils.unregister_class(regClass)

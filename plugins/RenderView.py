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
from bpy.props import *

from vb25.utils import *


TYPE= 'SETTINGS'
ID=   'RenderView'

NAME= 'Render view'
DESC= "Render view settings"

PARAMS= (
)


def add_properties(rna_pointer):
	pass


def write(bus):
	ofile  = bus['files']['camera']
	scene  = bus['scene']
	camera = bus['camera']

	VRayScene = scene.vray
	VRayBake  = VRayScene.VRayBake
	RTEngine  = VRayScene.RTEngine

	VRayCamera     = camera.data.vray
	SettingsCamera = VRayCamera.SettingsCamera

	if not VRayBake.use:
		fov = VRayCamera.fov if VRayCamera.override_fov else camera.data.angle

		aspect = float(scene.render.resolution_x) / float(scene.render.resolution_y)

		if aspect < 1.0:
			fov = fov * aspect

		ofile.write("\n// Camera: %s" % (camera.name))
		ofile.write("\nRenderView CameraView {")
		ofile.write("\n\ttransform=%s;" % a(scene, transform(camera.matrix_world)))
		ofile.write("\n\tfov=%s;" % a(scene, fov))
		if SettingsCamera.type not in ('SPHERIFICAL','BOX'):
			ofile.write("\n\tclipping=1;")
			ofile.write("\n\tclipping_near=%s;" % a(scene, camera.data.clip_start))
			ofile.write("\n\tclipping_far=%s;" % a(scene, camera.data.clip_end))
		if camera.data.type == 'ORTHO':
			ofile.write("\n\torthographic=1;")
			ofile.write("\n\torthographicWidth=%s;" % a(scene, camera.data.ortho_scale))
		ofile.write("\n}\n")

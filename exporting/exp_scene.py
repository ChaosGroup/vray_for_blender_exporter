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

from vb30 import debug

from . import exp_lights
from . import exp_camera
from . import exp_environment
from . import exp_objects


def ExportScene(bus, exportNodes=True, exportMeshes=None):
    debug.Debug("ExportScene()")

    err = None

    err = exp_environment.ExportEnvironment(bus)
    err = exp_lights.ExportLights(bus)
    err = exp_camera.ExportCamera(bus)
    err = exp_objects.ExportObjects(bus, exportNodes, exportMeshes)

    return err

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

from vb30.lib     import ExportUtils
from vb30.plugins import PLUGINS_ID

from vb30 import debug


@debug.TimeIt
def ExportCamera(bus):
    scene  = bus['scene']
    camera = bus['camera']

    VRayScene  = scene.vray
    VRayCamera = camera.data.vray

    # NOTE: Order is vital here
    cameraPlugins = (
        'SettingsMotionBlur',
        'SettingsCameraDof',
        'SettingsCamera',
        'CameraPhysical',
        'RenderView',
        'CameraStereoscopic',
        'VRayStereoscopicSettings',
    )

    for pluginName in cameraPlugins:
        propGroup      = None
        overrideParams = {}

        if pluginName == 'VRayStereoscopicSettings':
            propGroup = getattr(VRayScene, pluginName)
        elif pluginName == 'CameraStereoscopic':
            PLUGINS_ID['CameraStereoscopic'].write(bus)
            continue
        else:
            propGroup = getattr(VRayCamera, pluginName)

        if not propGroup:
            continue

        enabled = True
        for enableAttr in {'use', 'on'}:
            if hasattr(propGroup, enableAttr):
                enabled = getattr(propGroup, enableAttr)
        if not enabled:
            continue

        pluginModule = PLUGINS_ID[pluginName]

        ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

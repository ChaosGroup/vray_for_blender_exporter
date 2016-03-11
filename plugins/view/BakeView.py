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

import mathutils

from vb30.debug import Debug
from vb30.lib import ExportUtils
from vb30.lib import BlenderUtils
from vb30.lib import PluginUtils


PluginUtils.loadPluginOnModule(globals(), __name__)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    if not propGroup.use:
        return

    if not propGroup.bake_node:
        Debug("Bake object is not set!", msgType='ERROR')
        return

    bakeObject = BlenderUtils.GetSceneObject(scene, propGroup.bake_node)
    if not bakeObject:
        Debug("Bake object \"%s\" not found!" % propGroup.bake_node, msgType='ERROR')
        return

    o.set('SETTINGS', 'UVWGenChannel', 'UVWbakeView')
    o.writeHeader()
    o.writeAttibute('uvw_channel', propGroup.uv_channel)
    o.writeAttibute('uvw_transform', mathutils.Matrix.Identity(4))
    o.writeFooter()

    overrideParams.update({
        'bake_node' : BlenderUtils.GetObjectName(bakeObject),
        'bake_uvwgen' : "UVWbakeView",
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

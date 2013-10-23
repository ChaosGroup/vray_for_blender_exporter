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

from pprint import pprint

from vb25.debug import Debug

from . import utils
from . import AttributeUtils
from . import VRaySocket


def WriteFile(bus, filetype, data):
    if bus['mode'] == 'SOCKET':
        return
    ofile = bus['files'][filetype]
    ofile.write(data)


def WritePluginParams(bus, ofile, pluginType, pluginName, dataPointer, mappedParams, PluginParams):
    scene      = None
    vraySocket = None

    if bus['mode'] == 'VRSCENE':
        scene = bus['scene']
        if ofile is None:
            if 'files' in bus:
                ofile = bus['files']['nodetree']

    if bus['mode'] == 'SOCKET':
        vraySocket = VRaySocket.VRaySocket()

    for attrDesc in sorted(PluginParams, key=lambda t: t['attr']):
        attr  = attrDesc['attr']
        skip  = attrDesc.get('skip', False)

        if skip:
            continue

        # Skip output attributes
        if attrDesc['type'] in AttributeUtils.OutputTypes:
            continue

        # Type could be skipped, but mappedParams could contain a manually defined value for it
        if attrDesc['type'] in AttributeUtils.SkippedTypes and attrDesc['attr'] not in mappedParams:
            continue

        # Skip attibutes that should be mapped, but are not mapped, we will use parameter value then
        if attrDesc['type'] in AttributeUtils.InputTypes and attrDesc['attr'] not in mappedParams:
            continue

        value = None

        if attr in mappedParams:
            value = mappedParams[attr]

        if value is None:
            value = getattr(dataPointer, attr)

        if value is None:
            Debug("%s.%s value is None!" % (pluginName, attr), msgType='ERROR')
            continue

        if attrDesc['type'] in AttributeUtils.PluginTypes and not value:
            continue

        if attrDesc['type'] in {'STRING'}:
            if not value:
                continue
            else:
                value = '"%s"' % value

        if bus['mode'] == 'VRSCENE' and ofile is not None:
            ofile.write("\n\t%s=%s;" % (attr, utils.AnimatedValue(scene, value)))

        if bus['mode'] == 'SOCKET' and vraySocket:
            vraySocket.send("set %s.%s=%s" % (pluginName, attr, utils.FormatValue(value)))

    if vraySocket:
        vraySocket.send("render")
        vraySocket.disconnect()


def WriteDatablock(bus, pluginType, pluginName, PluginParams, dataPointer, mappedParams):
    WriteFile(bus, 'nodetree', "\n%s %s {" % (pluginType, pluginName))
    WritePluginParams(bus, None, pluginType, pluginName, dataPointer, mappedParams, PluginParams)
    WriteFile(bus, 'nodetree', "\n}\n")

    return pluginName

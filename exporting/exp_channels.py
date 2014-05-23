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

from vb30.nodes import export as NodesExport


def ExportRenderElements(bus):
    scene = bus['scene']
    o     = bus['output']

    ntree = scene.vray.ntree
    if not ntree:
        return

    outputNode = NodesExport.GetNodeByType(ntree, 'VRayNodeRenderChannels')
    if not outputNode:
        return

    for socket in outputNode.inputs:
        if socket.is_linked and socket.use:
            NodesExport.WriteConnectedNode(bus, ntree, socket)

    o.set('RENDERCHANNEL', 'SettingsRenderChannels', 'SettingsRenderChannels')
    o.writeHeader()
    o.writeAttibute('unfiltered_fragment_method', outputNode.unfiltered_fragment_method)
    o.writeAttibute('deep_merge_mode', outputNode.deep_merge_mode)
    o.writeAttibute('deep_merge_coeff', outputNode.deep_merge_coeff)
    o.writeFooter()

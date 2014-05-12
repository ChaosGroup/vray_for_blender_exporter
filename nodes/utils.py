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


def GetNodeName(ntree, node):
    return clean_string("NT%sN%s" % (ntree.name, node.name))


def GetConnectedNode(ntree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_node:
            return l.from_node
    return None


def GetConnectedSocket(ntree, nodeSocket):
    for l in nodeSocket.links:
        if l.from_socket:
            return l.from_socket
    return None


def GetNodesByType(ntree, nodeType):
    for n in ntree.nodes:
        if n.bl_idname == nodeType:
            yield n


def GetNodeByType(ntree, nodeType):
    if not ntree:
        return None
    for n in ntree.nodes:
        if n.bl_idname == nodeType:
            return n
    return None

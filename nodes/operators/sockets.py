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

from ..sockets import AddInput, AddOutput


class VRayNodeAddCustomSocket:
    vray_socket_type    = None
    vray_socket_name    = None

    def execute(self, context):
        node = context.node

        nSockets = 0
        for sock in node.inputs:
            if sock.name.startswith(self.vray_socket_name):
                nSockets += 1

        newIndex = nSockets + 1
        sockName = "%s %i" % (self.vray_socket_name, newIndex)

        AddInput(node, self.vray_socket_type, sockName)

        if hasattr(self, 'set_value'):
            self.set_value(node.inputs[sockName], newIndex)

        return {'FINISHED'}


class VRayNodeDelCustomSocket:
    vray_socket_type    = None
    vray_socket_name    = None

    def execute(self, context):
        node     = context.node

        nSockets = 0
        for sock in node.inputs:
            if sock.name.startswith(self.vray_socket_name):
                nSockets += 1

        if not nSockets:
            return {'FINISHED'}

        for i in range(nSockets, 0, -1):
            sockName   = "%s %i" % (self.vray_socket_name, i)
            if sockName not in node.inputs:
                break
            s = node.inputs[sockName]
            if not s.is_linked:
                node.inputs.remove(s)
                break

        return {'FINISHED'}

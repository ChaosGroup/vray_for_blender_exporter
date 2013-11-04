#
# V-Ray/Blender
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

__all__ = [ 'export' ]


def register():
    from . import sockets
    from . import specials
    from . import nodes
    from . import operators
    from . import tree
    from . import templates

    operators.register()

    tree.register()
    sockets.register()

    specials.register()
    nodes.register()

    templates.register()


def unregister():
    from . import sockets
    from . import specials
    from . import nodes
    from . import operators
    from . import tree
    from . import templates

    templates.unregister()

    nodes.unregister()
    specials.unregister()
    
    sockets.unregister()
    tree.unregister()

    operators.unregister()

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

if "bpy" in locals():
    import imp
    imp.reload(lib)
    imp.reload(plugins)
    imp.reload(preset)
    imp.reload(operators)
    imp.reload(proxy)
    imp.reload(nodes)
    imp.reload(ui)
    imp.reload(engine)
    imp.reload(realtime)
    imp.reload(keymap)
else:
    import bpy
    from vb25 import lib
    from vb25 import plugins
    from vb25 import preset
    from vb25 import operators
    from vb25 import proxy
    from vb25 import nodes
    from vb25 import ui
    from vb25 import engine
    from vb25 import realtime
    from vb25 import keymap


def register():
    plugins.register()
    operators.register()
    ui.register()
    engine.register()
    nodes.register()
    proxy.register()
    realtime.register()
    keymap.register()


def unregister():
    plugins.unregister()
    operators.unregister()
    engine.unregister()
    nodes.unregister()
    proxy.unregister()
    realtime.unregister()
    ui.unregister()
    keymap.unregister()

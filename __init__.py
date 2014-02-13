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

bl_info = {
    "name" : "V-Ray For Blender 3.0",
    "author" : "",
    "blender" : (2, 67, 0),
    "location" : "Info header, render engine menu",
    "description" : "Exporter to the V-Ray Standalone file format",
    "warning" : "",
    "wiki_url" : "https://github.com/bdancer/vb30/wiki",
    "tracker_url" : "https://github.com/bdancer/vb30/issues",
    "support" : 'COMMUNITY',
    "category" : "Render"
}


if "bpy" in locals():
    import imp
    imp.reload(plugins)
    imp.reload(preset)
    imp.reload(operators)
    imp.reload(proxy)
    imp.reload(nodes)
    imp.reload(engine)
    imp.reload(realtime)
    imp.reload(keymap)
    imp.reload(ui)
else:
    import bpy
    from vb30 import plugins
    from vb30 import preset
    from vb30 import operators
    from vb30 import proxy
    from vb30 import nodes
    from vb30 import engine
    from vb30 import realtime
    from vb30 import keymap
    from vb30 import ui


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

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
    imp.reload(nodes)
    imp.reload(proxy)
    imp.reload(ui)
    imp.reload(engine)
    imp.reload(realtime)
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


def register():
    plugins.register()

    proxy.register()
    nodes.register()
    ui.register()
    operators.register()
    engine.register()

    realtime.register()

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new('Screen', space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new('vray.render', 'F10', 'PRESS')


def unregister():
    plugins.unregister()

    proxy.unregister()
    nodes.unregister()
    ui.unregister()
    operators.unregister()
    engine.unregister()    

    realtime.unregister()

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Screen']
        for kmi in km.keymap_items:
            if kmi.idname == 'vray.render':
                km.keymap_items.remove(kmi)
                break

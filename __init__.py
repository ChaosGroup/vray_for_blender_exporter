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
    "name"        : "V-Ray For Blender 3.5",
    "author"      : "Andrei Izrantcev <andrei.izrantcev@chaosgroup.com>",
    "blender"     : (2, 70, 0),
    "location"    : "Info header, render engine menu",
    "description" : "Exporter to the V-Ray Standalone file format",
    "warning"     : "",
    "wiki_url"    : "https://github.com/bdancer/vb30/wiki",
    "tracker_url" : "https://github.com/bdancer/blender-for-vray/issues",
    "category"    : "Render"
}

from vb30 import plugins
from vb30 import preset
from vb30 import operators
from vb30 import proxy
from vb30 import nodes
from vb30 import engine
from vb30 import keymap
from vb30 import ui
from vb30 import events
from vb30 import compat
from vb30 import utils

def engineExit():
    import _vray_for_blender_rt
    _vray_for_blender_rt.exit()

def register():
    import atexit
    atexit.unregister(engineExit)
    atexit.register(engineExit)

    engine.init()

    plugins.register()
    operators.register()
    ui.register()
    nodes.register()
    proxy.register()
    keymap.register()
    events.register()
    preset.register()
    utils.register()
    compat.register()

    # NOTE: Register engine at the end,
    # to be sure all used data is registered.
    engine.register()


def unregister():
    engine.shutdown()

    # Remove events first
    events.unregister()

    plugins.unregister()
    operators.unregister()
    nodes.unregister()
    proxy.unregister()
    ui.unregister()
    keymap.unregister()
    preset.unregister()
    utils.unregister()
    compat.unregister()

    engine.unregister()

'''

	V-Ray/Blender

	http://vray.cgdo.ru

	Author: Andrey M. Izrantsev (aka bdancer)
	E-Mail: izrantsev@cgdo.ru

	This program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

	All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


if "bpy" in locals():
	import imp
	imp.reload(lib)
	imp.reload(plugins)
	imp.reload(ui)
	imp.reload(preset)
	imp.reload(render_ops)
else:
	import bpy
	from vb25 import lib
	from vb25 import plugins
	from vb25 import ui
	from vb25 import preset
	from vb25 import render_ops


def register():
	bpy.utils.register_module(__name__)

	plugins.add_properties()

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		km = kc.keymaps.new('Screen', space_type='EMPTY', region_type='WINDOW')
		kmi = km.keymap_items.new('vray.render', 'F10', 'PRESS')


def unregister():
	bpy.utils.unregister_module(__name__)

	plugins.remove_properties()

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		km = kc.addon.keymaps['Screen']
		for kmi in km.keymap_items:
			if kmi.idname == 'vray.render':
				km.keymap_items.remove(kmi)
				break

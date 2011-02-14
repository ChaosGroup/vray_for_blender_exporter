'''

  V-Ray/Blender 2.5

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

# TODO: move to Add-ons
# bl_info= {
# 	"name":        "V-Ray (git)",
# 	"author":      "Andrey M. Izrantsev",
# 	"version":     (2, 0, 0),
# 	"blender":     (2, 5, 6),
# 	"api":         34812,
# 	"location":    "Info Header",
# 	"description": "V-Ray Standalone 2.0 integration.",
# 	"warning":     "",
# 	"wiki_url":    "http://github.com/bdancer/vb25/wiki",
# 	"tracker_url": "http://github.com/bdancer/vb25/issues",
# 	"category":    "Render"
# }

if "bpy" in locals():
	import imp
	imp.reload(plugins)
	imp.reload(ui)
	imp.reload(preset)
	imp.reload(render_ops)
else:
	import bpy
	from vb25 import plugins
	from vb25 import ui
	from vb25 import preset
	from vb25 import render_ops


def register():
	plugins.add_properties()


def unregister():
	plugins.remove_properties()

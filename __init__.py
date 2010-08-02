'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''

try:
	init_data

	reload(properties_camera)
	reload(properties_lamp)
	reload(properties_material)
	reload(properties_texture)
	reload(properties_world)
	reload(properties_object)
	reload(properties_data)
	reload(properties_render)
	reload(render)
except:
	from vb25 import properties_camera
	from vb25 import properties_lamp
	from vb25 import properties_material
	from vb25 import properties_texture
	from vb25 import properties_world
	from vb25 import properties_object
	from vb25 import properties_data
	from vb25 import properties_render
	from vb25 import render

def register():
    pass

def unregister():
    pass

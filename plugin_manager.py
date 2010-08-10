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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


import bpy

import sys
import os
import imp

from vb25.utils import *


TEX_PLUGINS= []
TEX_PLUGINS_TYPES= []


base_dir= vb_script_path()
if base_dir is not None:
	plugins_dir= os.path.join(base_dir,"plugins")
	
	if not plugins_dir in sys.path:
		sys.path.append(plugins_dir)

	plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname.endswith(".py")]
	plugins= [__import__(fname) for fname in plugins_files]

	for plugin in plugins:
		sys.stdout.write("V-Ray/Blender: Loading module: %s         \r"%(plugin.__name__))
		if plugin.TYPE == 'TEXTURE':
			TEX_PLUGINS.append(plugin)
			TEX_PLUGINS_TYPES.append(plugin.ID)
		sys.stdout.flush()
	sys.stdout.write("V-Ray/Blender: Loading modules... done.          \n")


class VRayTexture(bpy.types.IDPropertyGroup):
    pass


def add_properties():
	bpy.types.Texture.PointerProperty(
		attr= 'vray_texture',
		type= VRayTexture,
		name= "V-Ray Texture Settings",
		description= "V-Ray texture settings"
	)

	tex_enum_items= []
	for plugin in TEX_PLUGINS:
		plugin_desc= []

		plugin.add_properties(VRayTexture)

		plugin_desc.append(plugin.ID)
		plugin_desc.append(plugin.NAME)
		plugin_desc.append(plugin.DESC)

		tex_enum_items.append(tuple(plugin_desc))

	tex_enum_items.append(('NONE',"None",""))
		
	VRayTexture.EnumProperty(
		attr= 'type',
		name= "Texture type",
		description= "V-Ray texture type",
		items= (tuple(tex_enum_items)),
		default= 'NONE'
	)


def remove_properties():
	bpy.types.Texture.RemoveProperty('vray_texture')

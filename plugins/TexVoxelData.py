#
# V-Ray/Blender
#
# http://vray.cgdo.ru
#
# Author: Andrey M. Izrantsev (aka bdancer)
# E-Mail: izrantsev@cgdo.ru
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


# Blender modules
import bpy
from bpy.props import *

# V-Ray/Blender modules
from vb25.utils   import *
from vb25.ui.ui   import *
from vb25.plugins import *
from vb25.texture import *
from vb25.uvwgen  import *


TYPE = 'TEXTURE'

ID   = 'TexVoxelData'
NAME = 'Voxel Data'
PLUG = 'TexVoxelData'
DESC = "VoxelData texture."
PID  =  15

PARAMS = (
	'debug',
	'test_color',
	'filepath',
)


def add_properties(VRayTexture):
	class TexVoxelData(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(TexVoxelData)
	
	VRayTexture.TexVoxelData= PointerProperty(
		name        = "TexVoxelData",
		type        =  TexVoxelData,
		description = "V-Ray TexVoxelData settings"
	)

	TexVoxelData.test_color = FloatVectorProperty(
		name        = "Test Color",
		description = "Color for testing output",
		subtype     = 'COLOR',
		min         =  0.0,
		max         =  1.0,
		soft_min    =  0.0,
		soft_max    =  1.0,
		default     = (1.0,1.0,1.0)
	)

	TexVoxelData.filepath = StringProperty(
		name        = "Filepath",
		description = "Voxel data filepath",
		subtype     = 'FILE_PATH',
		default     = ""
	)

	TexVoxelData.debug = BoolProperty(
		name        = "Debug",
		description = "Debug output",
		default     = True
	)

#
# Export
#
def write(bus):
	scene = bus['scene']
	ofile = bus['files']['textures']

	slot     = bus['mtex']['slot']
	texture  = bus['mtex']['texture']
	tex_name = bus['mtex']['name']

	uvwgen = write_uvwgen(bus)

	TexVoxelData = getattr(texture.vray, PLUG)

	# Write output
	ofile.write("\n%s %s {" % (PLUG, tex_name))
	for param in PARAMS:
		if param == 'filepath':
			ofile.write("\n\tfilepath=\"%s\";" % bpy.path.abspath(TexVoxelData.filepath))
		else:
			ofile.write("\n\t%s=%s;"%(param, a(scene, getattr(TexVoxelData, param))))
	ofile.write("\n\tuvwgen=%s;" % uvwgen)
	ofile.write("\n}\n")

	return tex_name


#
# GUI
#
class VRAY_TP_TexVoxelData(VRayTexturePanel, bpy.types.Panel):
	bl_label = NAME

	@classmethod
	def poll(cls, context):
		return texture_type_poll(cls, context, context.texture, ID)
	
	def draw(self, context):
		tex = context.texture

		TexVoxelData = getattr(tex.vray, PLUG)
		
		wide_ui = context.region.width > narrowui

		layout = self.layout

		layout.prop(TexVoxelData, 'filepath')
		layout.separator()
		layout.prop(TexVoxelData, 'test_color')
		layout.prop(TexVoxelData, 'debug')


## Registration
#
bpy.utils.register_class(VRAY_TP_TexVoxelData)

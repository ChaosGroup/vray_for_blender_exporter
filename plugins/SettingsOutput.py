'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Time-stamp: "Monday, 14 March 2011 [08:47]"

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


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'SETTINGS'

ID=   'SettingsOutput'

NAME= 'Output'
DESC= "Output options."

PARAMS= (
)


def add_properties(rna_pointer):
	class SettingsOutput(bpy.types.PropertyGroup):
		img_noAlpha= BoolProperty(
			name= "No alpha",
			description= "Don't write the alpha channel to the final image.",
			default= False
		)

		img_separateAlpha= BoolProperty(
			name= "Separate alpha",
			description= "Write the alpha channel to a separate file.",
			default= False
		)

		img_file= StringProperty(
			name= "File name",
			description= "Render file name (Variables: %C - camera name; %S - scene name).",
			default= "render_%C"
		)

		img_dir= StringProperty(
			name= "Path",
			description= "Render file directory.",
			subtype= 'DIR_PATH',
			default= "//render/"
		)

		img_file_needFrameNumber= BoolProperty(
			name= "Add frame number",
			description= "Add frame number to the image file name.",
			default= True
		)

		relements_separateFolders= BoolProperty(
			name= "Separate folders",
			description= "Save render channels in separate folders.",
			default= False
		)
	bpy.utils.register_class(SettingsOutput)

	rna_pointer.SettingsOutput= PointerProperty(
		name= NAME,
		type= SettingsOutput,
		description= DESC
	)



def write(bus):
	COMPRESSION= {
		'NONE':  1,
		'PXR24': 6,
		'ZIP':   4,
		'PIZ':   5,
		'RLE':   2,
	}

	ofile=  bus['files']['scene']
	scene=  bus['scene']

	VRayScene=      scene.vray
	VRayExporter=   VRayScene.exporter
	VRayDR=         VRayScene.VRayDR
	SettingsOutput= VRayScene.SettingsOutput

	wx= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	wy= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

	file_format= get_render_file_format(VRayExporter, scene.render.file_format)

	ofile.write("\nSettingsOutput SettingsOutput {")
	ofile.write("\n\timg_noAlpha= %d;" % SettingsOutput.img_noAlpha)
	ofile.write("\n\timg_separateAlpha= %d;" % SettingsOutput.img_separateAlpha)
	ofile.write("\n\timg_width= %s;" % wx)
	ofile.write("\n\timg_height= %s;" % (wx if VRayScene.VRayBake.use else wy))
	ofile.write("\n\timg_file= \"%s\";" % bus['filenames']['output_filename'])
	ofile.write("\n\timg_dir= \"%s\";" % bus['filenames']['output'])
	ofile.write("\n\timg_file_needFrameNumber= %d;" % SettingsOutput.img_file_needFrameNumber)
	ofile.write("\n\tanim_start= %d;" % scene.frame_start)
	ofile.write("\n\tanim_end= %d;" % scene.frame_end)
	ofile.write("\n\tframe_start= %d;" % scene.frame_start)
	ofile.write("\n\tframes_per_second= %.3f;" % 1.0)
	ofile.write("\n\tframes= %d-%d;" % (scene.frame_start, scene.frame_end))
	ofile.write("\n\tframe_stamp_enabled= %d;" % 0)
	ofile.write("\n\tframe_stamp_text= \"%s\";" % ("V-Ray/Blender 2.0 | V-Ray Standalone %%vraycore | %%rendertime"))
	ofile.write("\n\trelements_separateFolders= %d;" % SettingsOutput.relements_separateFolders)
	ofile.write("\n\trelements_divider= \".\";")
	ofile.write("\n}\n")

	ofile.write("\nSettingsEXR SettingsEXR {")
	ofile.write("\n\tcompression= %i;" % COMPRESSION[scene.render.exr_codec])
	ofile.write("\n\tbits_per_channel= %d;" % (16 if scene.render.use_exr_half else 32))
	ofile.write("\n}\n")

	ofile.write("\nSettingsTIFF SettingsTIFF {")
	ofile.write("\n\tbits_per_channel= %d;" % (16 if scene.render.use_tiff_16bit else 32))
	ofile.write("\n}\n")

	ofile.write("\nSettingsJPEG SettingsJPEG {")
	ofile.write("\n\tquality= %d;" % scene.render.file_quality)
	ofile.write("\n}\n")

	ofile.write("\nSettingsPNG SettingsPNG {")
	ofile.write("\n\tcompression= %d;" % (int(scene.render.file_quality / 10) if scene.render.file_quality < 90 else 90))
	ofile.write("\n\tbits_per_channel= 16;")
	ofile.write("\n}\n")

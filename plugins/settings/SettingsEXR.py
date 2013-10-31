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

TYPE = 'SETTINGS'
ID   = 'SettingsEXR'
NAME = 'SettingsEXR'
DESC = ""

PluginParams = (
    {
        'attr' : 'compression',
        'desc' : "Compression for OpenEXR output",
        'type' : 'ENUM',
        'items' : (
            ('0', "Default", ""),
            ('1', "No Compression", ""),
            ('2', "RLE", ""),
            ('3', "ZIPS", ""),
            ('4', "ZIP", ""),
            ('5', "PIZ", ""),
            ('6', "pxr24", ""),
        ),
        'default' : '3',
    },
    {
        'attr' : 'bits_per_channel',
        'desc' : "Bits per channel",
        'type' : 'ENUM',
        'items' : (
            ('16', "16", ""),
            ('32', "32", ""),
        ),
        'default' : '16',
    },
    {
        'attr' : 'extra_attributes',
        'desc' : "Extra attributes to write in the header",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'auto_data_window',
        'desc' : "true to enable auto data window based on the alpha channel when writing scanline-based multichannel OpenEXR files",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'write_integer_ids',
        'desc' : "true to write integer elemnt ids when using Image Format exr",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""


# wx= int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
# wy= int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)

# ofile.write("\nSettingsOutput SettingsOutput {")
# if VRayExporter.auto_save_render:
#   ofile.write("\n\timg_file= \"%s\";" % bus['filenames']['output_filename'])
#   ofile.write("\n\timg_dir= \"%s/\";" % bus['filenames']['output'])
# ofile.write("\n\timg_noAlpha=%d;" % SettingsOutput.img_noAlpha)
# ofile.write("\n\timg_separateAlpha=%d;" % SettingsOutput.img_separateAlpha)
# ofile.write("\n\timg_width=%s;" % wx)
# ofile.write("\n\timg_height=%s;" % (wx if VRayScene.VRayBake.use else wy))
# ofile.write("\n\timg_file_needFrameNumber=%d;" % SettingsOutput.img_file_needFrameNumber)
# ofile.write("\n\tanim_start=%d;" % scene.frame_start)
# ofile.write("\n\tanim_end=%d;" % scene.frame_end)
# ofile.write("\n\tframe_start=%d;" % scene.frame_start)
# ofile.write("\n\tframes_per_second=%.3f;" % 1.0)
# ofile.write("\n\tframes=%d-%d;" % (scene.frame_start, scene.frame_end))
# ofile.write("\n\tframe_stamp_enabled=%d;" % 0)
# ofile.write("\n\tframe_stamp_text= \"%s\";" % ("V-Ray/Blender 2.0 | V-Ray Standalone %%vraycore | %%rendertime"))
# ofile.write("\n\trelements_separateFolders=%d;" % SettingsOutput.relements_separateFolders)
# ofile.write("\n\trelements_divider= \".\";")
# ofile.write("\n}\n")

# ofile.write("\nSettingsEXR SettingsEXR {")
# ofile.write("\n\tcompression=%i;" % COMPRESSION[scene.render.image_settings.exr_codec])
# ofile.write("\n\tbits_per_channel=%s;" % SettingsOutput.color_depth)
# ofile.write("\n}\n")

# ofile.write("\nSettingsTIFF SettingsTIFF {")
# ofile.write("\n\tbits_per_channel=%s;" % SettingsOutput.color_depth)
# ofile.write("\n}\n")

# ofile.write("\nSettingsSGI SettingsSGI {")
# ofile.write("\n\tbits_per_channel=%s;" % SettingsOutput.color_depth)
# ofile.write("\n}\n")

# ofile.write("\nSettingsJPEG SettingsJPEG {")
# ofile.write("\n\tquality=%d;" % scene.render.image_settings.quality)
# ofile.write("\n}\n")

# ofile.write("\nSettingsPNG SettingsPNG {")
# ofile.write("\n\tcompression=%d;" % (int(scene.render.image_settings.quality / 10) if scene.render.image_settings.quality < 90 else 9))
# ofile.write("\n\tbits_per_channel=%s;" % (SettingsOutput.color_depth if SettingsOutput.color_depth in ['8','16'] else '16'))
# ofile.write("\n}\n")

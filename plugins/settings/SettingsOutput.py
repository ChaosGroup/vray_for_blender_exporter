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

from vb25.lib import ExportUtils


TYPE = 'SETTINGS'
ID   = 'SettingsOutput'
NAME = 'Output'
DESC = ""

PluginParams = (
    {
        'attr' : 'img_width',
        'desc' : "Output image width",
        'type' : 'INT',
        'default' : 640,
    },
    {
        'attr' : 'img_height',
        'desc' : "Output image height",
        'type' : 'INT',
        'default' : 480,
    },
    {
        'attr' : 'img_pixelAspect',
        'desc' : "Output image pixel aspect",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'img_file',
        'desc' : "Render file name (Variables: %C - camera name; %S - scene name; %F - blendfile name)",
        'type' : 'STRING',
        'default' : "%F_%C",
    },
    {
        'attr' : 'img_dir',
        'desc' : "Render file directory (Variables: %C - camera name; %S - scene name; %F - blendfile name)",
        'type' : 'STRING',
        'subtype' : 'DIR_PATH',
        'default' : "//render/%F/",
    },
    {
        'attr' : 'img_file_needFrameNumber',
        'desc' : "Add frame number to the image file name",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_separateAlpha',
        'desc' : "Write the alpha channel to a separate file",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_noAlpha',
        'desc' : "Don't write the alpha channel to the final image",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_dontSaveRgbChannel',
        'desc' : "If true, the RGB channel will not be saved to disk",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_deepFile',
        'desc' : "If true, V-Ray will will generate deep image file (valid for vrst and exr)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_rawFile',
        'desc' : "If true, V-Ray will render to a tiled file format (.vrimg or .exr). This is automatically turned on for file formats that only support tiled writing (like .vrimg)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'img_rawFileVFB',
        'desc' : "If writing to a tiled file format, specifies whether a memory VFB window should be displayed (0 - no memory VFB, 1 - full memory VFB, 2 - preview)",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'anim_start',
        'desc' : "Start of animation range in time units",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'anim_end',
        'desc' : "End of animation range in time units",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'anim_frame_padding',
        'desc' : "Animation Frame Name Padding",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'anim_renumber_on',
        'desc' : "If true, frame renumbering is used",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'anim_renumber_start',
        'desc' : "Start number for renumber frames",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'anim_renumber_step',
        'desc' : "Renumber frames step",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'anim_ren_frame_start',
        'desc' : "First frame of animation range",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'frame_start',
        'desc' : "The frame number at the start of the animation range",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'frames_per_second',
        'desc' : "Number of frames per unit time",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'frames',
        'desc' : "List of frames to be rendered. May contain intervals in the form of lists with start and end frame",
        'type' : 'LIST',
        'default' : "",
    },
    {
        'attr' : 'rgn_left',
        'desc' : "Image output region left coord",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'rgn_width',
        'desc' : "Image output region width",
        'type' : 'FLOAT',
        'default' : 640,
    },
    {
        'attr' : 'rgn_top',
        'desc' : "Image output region top coord",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'rgn_height',
        'desc' : "Image output region height",
        'type' : 'FLOAT',
        'default' : 480,
    },
    {
        'attr' : 'bmp_width',
        'desc' : "Output bitmap width",
        'type' : 'INT',
        'default' : 640,
    },
    {
        'attr' : 'bmp_height',
        'desc' : "Output bitmap height",
        'type' : 'INT',
        'default' : 480,
    },
    {
        'attr' : 'r_left',
        'desc' : "Bitmap output region left coord",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'r_width',
        'desc' : "Bitmap output region width",
        'type' : 'INT',
        'default' : 640,
    },
    {
        'attr' : 'r_top',
        'desc' : "Bitmap output region top coord",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'r_height',
        'desc' : "Bitmap output region height",
        'type' : 'INT',
        'default' : 480,
    },
    {
        'attr' : 'frame_stamp_enabled',
        'desc' : "true to enable the VFB frame stamp",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'frame_stamp_text',
        'desc' : "Frame stamp text",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'relements_separateFolders',
        'desc' : "Save render channels in separate folders",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'relements_separate_rgba',
        'desc' : "true to save the main RGBA elment in a separate folder too, if relements_separateFolders is specified",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'relements_divider',
        'desc' : "Render elements name separator",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'film_offset_x',
        'desc' : "Horizontal film offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'film_offset_y',
        'desc' : "Vertical film offset",
        'type' : 'FLOAT',
        'default' : 0,
    },

    {
        'attr' : 'img_format',
        'name' : "Image Format",
        'desc' : "Output image format",
        'type' : 'ENUM',
        'items' : (
            ('SettingsPNG',  "PNG",       ""),
            ('SettingsJPEG', "JPEG",      ""),
            ('SettingsTIFF', "TIFF",      ""),
            ('SettingsTGA',  "TGA",       ""),
            ('SettingsSGI',  "SGI",       ""),
            ('SettingsEXR',  "OpenEXR",   ""),
            ('SettingsVRST', "VRayImage", "V-Ray Image Format"),
        ),
        'skip' : True,
        'default' : 'SettingsJPEG',
    },
)

PluginWidget = """
{ "widgets": [
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene  = bus['scene']

    VRayScene = scene.vray

    img_width = int(scene.render.resolution_x * scene.render.resolution_percentage * 0.01)
    img_height = int(scene.render.resolution_y * scene.render.resolution_percentage * 0.01)
    
    if VRayScene.RTEngine.enabled or scene.render.engine == 'VRAY_RENDER_RT':
        if VRayScene.SettingsRTEngine.stereo_mode:
            img_width *= 2.0

    overrideParams.update({
        'img_width'  : img_width,
        'img_height' : img_height,
        'bmp_width'  : img_width,
        'bmp_height' : img_height,
        'rgn_width'  : img_width,
        'rgn_height' : img_height,
        'r_width'    : img_width,
        'r_height'   : img_height,

        'img_file' : "",
        'img_dir' : "",
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

# ofile.write("\nSettingsOutput SettingsOutput {")
# if VRayExporter.auto_save_render:
#   ofile.write("\n\timg_file= \"%s\";" % bus['filenames']['output_filename'])
#   ofile.write("\n\timg_dir= \"%s/\";" % bus['filenames']['output'])
# ofile.write("\n\timg_noAlpha=%d;" % SettingsOutput.img_noAlpha)
# ofile.write("\n\timg_separateAlpha=%d;" % SettingsOutput.img_separateAlpha)
# ofile.write("\n\timg_width=%s;" % wx)
# ofile.write("\n\timg_height=%s;" % (wx if VRayScene.BakeView.use else wy))
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

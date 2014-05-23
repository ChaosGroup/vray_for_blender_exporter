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

TYPE = 'SETTINGS'
ID   = 'VRayStereoscopicSettings'
NAME = 'Stereo Render'
DESC = ""

PluginParams = (
    {
        'attr' : 'eye_distance',
        'desc' : "The eye distance for which the stereoscopic image will be rendered",
        'type' : 'FLOAT',
        'default' : 6.5,
    },
    {
        'attr' : 'specify_focus',
        'desc' : "If on then the focus is determined by focus_method and focus_distance. Otherwise it is determined from the camera target distance",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'focus_distance',
        'desc' : "The focus distance when specify_focus is enabled",
        'type' : 'FLOAT',
        'default' : 200,
    },
    {
        'attr' : 'focus_method',
        'desc' : "Specifies the focus method for the two views",
        'type' : 'ENUM',
        'items' : (
            ('0', "None",     "Both cameras have their focus points directly in front of them"),
            ('1', "Rotation", "The stereoscopy is achieved by rotating the left and right views so that their focus points coincide at the distance from the eyes where the lines of sight for each eye converge called fusion distance"),
            ('2', "Shear",    "The orientation of both views remain the same but each eyes view is sheared along Z so that the two frustums converge at the fusion distance"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'interocular_method',
        'desc' : "Specifies how the two virtual cameras will be placed in relation to the real camera in the scene",
        'type' : 'ENUM',
        'items' : (
            ('0', "Shift Both",  "Both virtual cameras will be shifted in opposite directions at a distance equal to half of the eye distance"),
            ('1', "Shift Left",  "The virtual cameras are shifted to the left so that the right camera takes the position of the original camera. The left camera is shifted to the left at a distance equal to the 'Eye Distance'"),
            ('2', "Shift Right", "The virtual cameras are shifted to the right so that the left camera takes the position of the original camera. The right camera is shifted to the right at a distance equal to the 'Eye Distance'")
        ),
        'default' : '0',
    },
    {
        'attr' : 'view',
        'desc' : "Specifies which of the stereoscopic views will be rendered",
        'type' : 'ENUM',
        'items' : (
            ('0', "Both",  "Both views will be rendered side by side"),
            ('1', "Left",  "Only the left view will be rendered"),
            ('2', "Right", "Only the right view will be rendered")
        ),
        'default' : '0',
    },
    {
        'attr' : 'adjust_resolution',
        'desc' : "When on this option will automatically adjust the resolution for the final image rendered",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'sm_mode',
        'desc' : "Allows us to specify the mode of operation for the shade map",
        'type' : 'ENUM',
        'items' : (
            ('0', "Disabled",         "No shade map will be used during rendering"),
            ('1', "Render shade map", "In this mode a shade map will be created and saved in the file specified in the Shademap file field"),
            ('2', "Use shade map",    "In this mode V-Ray will render the image using information from the file specified in the Shademap file field")
        ),
        'default' : '0',
    },
    {
        'attr' : 'reuse_threshold',
        'desc' : "Lower values will make V-Ray use less of the shade map and more real shading",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'shademap_file',
        'desc' : "The name of the file in which the shade map information is stored",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'float_colors_mode',
        'desc' : "Store 32 bit (single precision) color channels in the shade map. When off 16 bit (half precision) values are stored",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'vrst_compression',
        'desc' : "Compression type for the .vrst files",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Compression",  ""),
            ('1', "ZLIB Compression", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'exr_compression',
        'desc' : "Compression type for the .exr files",
        'type' : 'ENUM',
        'items' : (
            ('0', "No Compression",  ""),
            ('1', "RLE Compression", ""),
            ('2', "ZIPS Compression", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'exclude_list',
        'desc' : "A list of plugins for which the shade map won't be used",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'left_camera',
        'desc' : "A camera plugin for the left eye; if not specified, the left camera is computed based on the scene camera",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'right_camera',
        'desc' : "A camera plugin for the right eye; if not specified, the right camera is computed based on the scene camera",
        'type' : 'PLUGIN',
        'default' : "",
    },

    {
        'attr' : 'use',
        'name' : 'Stereo Render',
        'desc' : "Use Stereoscopic",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

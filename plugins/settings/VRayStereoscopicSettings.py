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
ID   = 'VRayStereoscopicSettings'
NAME = 'VRayStereoscopicSettings'
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
        'desc' : "Specifies the focus method for the two views (0 - none/parallel; 1 - rotation; 2 - shear)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'interocular_method',
        'desc' : "Specifies how the two virtual cameras will be placed in relation to the real camera in the scene (0 - symmetric/shift both; 1 - shift left; 2 - shift right)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'view',
        'desc' : "Specifies which of the stereoscopic views will be rendered (0 - both; 1 - left; 2 - right)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'adjust_resolution',
        'desc' : "When on this option will automatically adjust the resolution for the final image rendered",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'sm_mode',
        'desc' : "Allows us to specify the mode of operation for the shade map (0 - disabled; 1 - render shade map; 2 - use shade map)",
        'type' : 'INT',
        'default' : 0,
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
        'desc' : "Compression type for the .vrst files (0 - no compression, 1 - ZLIB compression)",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'exr_compression',
        'desc' : "Compression type for the .exr files (0 - no compression, 1 - RLE compression, 2 - ZIPS compression)",
        'type' : 'INT',
        'default' : 2,
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
)

PluginWidget = """
{ "widgets": [
]}
"""

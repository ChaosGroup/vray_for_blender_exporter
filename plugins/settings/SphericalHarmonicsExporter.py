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
ID   = 'SphericalHarmonicsExporter'
NAME = 'Spherical Harmonics Exporter'
DESC = "Spherical harmonics exporter settings"

PluginParams = (
    {
        'attr' : 'anim_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mode',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "Occlusion (Selected)", ""),
            ('1', "Occlusion", ""),
            ('2', "Interreflection (Selected)", ""),
            ('3', "Interreflection", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'bands',
        'desc' : "",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'subdivs',
        'desc' : "Controls the number of samples taken in order to create the spherical harmonics. Higher values produce better results but take longer to render",
        'type' : 'INT',
        'default' : 50,
    },
    {
        'attr' : 'bounces',
        'desc' : "This option is only available when one of the interreflection methods is selected. It controls the number of secondary bounces that are going to be traced",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'ray_bias',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'file_name',
        'desc' : "This is the name of the *.vrsh file which contains the precomputed SH for this scene",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/spherical_harmonics.vrsh",
    },
    {
        'attr' : 'file_format',
        'desc' : "This is the output file format. It could be *.xml for general purposes, V-Ray internal format *.vrsh designed to be used in \"Spherical Harmoics\" GI engine or both of them",
        'type' : 'ENUM',
        'items' : (
            ('xml',  "*.xml",  ""),
            ('vrsh', "*.vrsh", ""),
        ),
        'default' : 'vrsh'
    },
    {
        'attr' : 'per_normal',
        'desc' : "Spherical harmonics can be created either for each vertex of the geometry or for each normal, this option allows you to choose between those two modes. For round objects it is better to use per Vertex mode while for objects with large flat surfaces the per Normal mode is better and faster",
        'type' : 'ENUM',
        'items' : (
            ('0', "Per normal", ""),
            ('1', "Per vertex", ""),
        ),
        'default' : '0'
    },
    {
        'attr' : 'hit_recording',
        'desc' : "Enabling it speeds up the calculations by storing a lot of information in the RAM",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'max_mem_usage',
        'desc' : "",
        'type' : 'INT',
        'default' : 2000,
    },
    {
        'attr' : 'object_space',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "World Space",  ""),
            ('1', "Object Space", ""),
        ),
        'default' : '0'
    },
    {
        'attr' : 'adaptive_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adaptive_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'adaptive_depth',
        'desc' : "",
        'type' : 'INT',
        'default' : 3,
    },
    {
        'attr' : 'adaptive_edge',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'save_obj',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'node',
        'desc' : "Node of the mesh",
        'type' : 'PLUGIN',
        'default' : "",
    },
)

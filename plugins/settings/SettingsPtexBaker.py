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
ID   = 'SettingsPtexBaker'
NAME = 'Ptex Baker'
DESC = ""

PluginParams = (
    {
        'attr' : 'objects',
        'desc' : "A list of SceneNodes that will be baked",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'texture_name',
        'desc' : "The base name for the Ptex files",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'res_u',
        'desc' : "The resolution in the U direction in texture space is 2 ^ res_u",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'res_v',
        'desc' : "The resolution in the V direction in texture space is 2 ^ res_v",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'force_quads',
        'desc' : "If true the textures will be quadrangular even if the mesh is purely triangular",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'data_format',
        'desc' : "Type of texel data: 0 - 8 bit int, 1 - 16 bit int, 2 - 16 bit float, 3 - 32 bit float",
        'type' : 'INT',
        'default' : 3,
    },
    {
        'attr' : 'write_faces_degrees',
        'desc' : "If true then meta data containing the degree of each mesh polygon will be included in the Ptex files",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'write_faces_vertices',
        'desc' : "If true then meta data containing the vertices of each mesh polygon will be included in the Ptex files",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'write_vertex_positions',
        'desc' : "If true then meta data containing the positions of all vertices will be included in the Ptex files",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'generate_mipmaps',
        'desc' : "True to generate mipmaps and false otherwise",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'border_mode_u',
        'desc' : "Type of border mode in U direction: 0 - clamp, 1 - black, 2 - periodic",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'border_mode_v',
        'desc' : "Type of border mode in V direction: 0 - clamp, 1 - black, 2 - periodic",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'samplers_per_texel',
        'desc' : "The number of samples shaded for each texel will be the square of this number",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'multichannel_file',
        'desc' : "If this is true then all render elements will be baked into one Ptex file",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'surface_offset',
        'desc' : "An offset along the geometric surface normal at which to perform shading in order to avoid surface acne",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'world_space_res',
        'desc' : "If true then the resolution for each texture will be calculated adaptively, based on the size of the corresponding geometry",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'length_u',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'length_v',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'resolution_multiplier',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'projection_baking',
        'desc' : "0 - normal baking, 1 - projection baking",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'mode',
        'desc' : "0 - outside, 1 - inside, 2 - outside first, the inside, 3 - inside first, the outside, 4 - closest",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'normal',
        'desc' : "0 - Smooth normal, 1 - Geometry normal",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'ray_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'max_depth',
        'desc' : "Geometry that is intersected further than this value along the ray will be ignored. If the value is zero then no geometry will be ignored",
        'type' : 'FLOAT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

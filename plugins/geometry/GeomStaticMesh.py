#
# V-Ray/Blender
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

import bpy


TYPE = 'GEOMETRY'
ID   = 'GeomStaticMesh'
NAME = "Mesh"
DESC = "Mesh settings"

PluginParams = (
    # Exported from _vray_for_blender
    #
    # {
    #     'attr' : 'vertices',
    #     'desc' : "",
    #     'type' : 'VECTOR',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'faces',
    #     'desc' : "",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'normals',
    #     'desc' : "",
    #     'type' : 'VECTOR',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'faceNormals',
    #     'desc' : "",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'map_channels',
    #     'desc' : "A list of mapping channels; each channel itself is a list of 3 elements - the channel index, the channel vertices and the channel faces",
    #     'type' : 'LIST',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'map_channels_names',
    #     'desc' : "A list containing the names of the mapping channels",
    #     'type' : 'STRING',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'edge_visibility',
    #     'desc' : "A list of edge visibility flags, each integer in the list has edge visibility information for 10 consecutive faces",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'face_mtlIDs',
    #     'desc' : "Material IDs for each face",
    #     'type' : 'INT',
    #     'default' : "",
    # },

    # TODO: Export from _vray_for_blender
    #
    # {
    #     'attr' : 'edge_creases_vertices',
    #     'desc' : "The indices of the vertices of the creased edges. Contains two indices per edge",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'edge_creases_sharpness',
    #     'desc' : "Sharpness values for each creased edge",
    #     'type' : 'FLOAT',
    #     'default' : "",
    # },    
    # {
    #     'attr' : 'vertex_creases_vertices',
    #     'desc' : "A list of creased vertices",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'vertex_creases_sharpness',
    #     'desc' : "The sharpness values of the creased vertices",
    #     'type' : 'FLOAT',
    #     'default' : "",
    # },

    # {
    #     'attr' : 'smooth_derivs',
    #     'desc' : "A list of mapping channels with smooth derivs; this can also be a single boolean value to specify whether all channels are smooth",
    #     'type' : 'LIST',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'velocities',
    #     'desc' : "Per vertex velocities, taken from a ColorSet in Maya",
    #     'type' : 'VECTOR',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'first_poly_vertices',
    #     'desc' : "A list of indices of the first vertices of the polygons of degree greater than 4",
    #     'type' : 'INT',
    #     'default' : "",
    # },

    # {
    #     'attr' : 'reference_mesh',
    #     'desc' : "The reference mesh which is used to calculate the uvw coordinates when a 3d placement is used",
    #     'type' : 'PLUGIN',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'reference_transform',
    #     'desc' : "The transform of the reference mesh",
    #     'type' : 'TRANSFORM',
    #     'default' : None,
    # },

    {
        'attr' : 'weld_threshold',
        'desc' : "If this parameter is present, the vertices of the mesh which are within the given threshold of one another will be welded. If absent or negative, no welding is performed",
        'type' : 'FLOAT',
        'default' : -1,
    },
    {
        'attr' : 'primary_visibility',
        'desc' : "If off shading an intersection with this mesh will not generate a gbuffer",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'dynamic_geometry',
        'desc' : "When this flag is true V-Ray will use dynamic geometry for this mesh(instead of copying the mesh many times in the BSP tree, only the bounding box will be present many times and ray intersections will occur in a separate object space BSP tree)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'environment_geometry',
        'desc' : "When this flag is true V-Ray will use this geometry as part of the background(for example, this will be included in matte objects",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'smooth_uv_borders',
        'name' : "Smooth UV Borders",
        'desc' : "true to smooth UVs at mesh borders when rendering this mesh as a subdivision surface",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'smooth_uv',
        'name' : "Smooth UV",
        'desc' : "true to smooth UVs when rendering this mesh as a subdivision surface",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'osd_subdiv_level',
        'name' : "Subdiv. Level",
        'desc' : "Level of OpenSubdiv subdivision",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'osd_subdiv_type',
        'name' : "Subdiv. Type",
        'desc' : "Type of OpenSubdiv subdivision",
        'type' : 'ENUM',
        'items' : (
            ('0', "Catmull-Clark", ""),
            ('1', "Loop", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'osd_preserve_map_borders',
        'name' : 'Preserve Map Borders',
        'desc' : "Different modes for subdividing the uv boundaries with OpenSubdiv",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('1', "Internal", ""),
            ('1', "All", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'osd_preserve_geometry_borders',
        'name' : 'Preserve Geometry Borders',
        'desc' : "Keep the geometry boundaries in place while subdividing the mesh with OpenSubdiv",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'osd_subdiv_uvs',
        'name' : 'Subdivide UV',
        'desc' : "Smooth UVs when applying subdivision with OpenSubdiv",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "primary_visibility" },
            { "name" : "dynamic_geometry" },
            { "name" : "environment_geometry" }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "OpenSubdiv" },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "osd_subdiv_type" },
            { "name" : "osd_subdiv_level", "label" : "Level" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "osd_preserve_map_borders" },
            { "name" : "osd_preserve_geometry_borders" },
            { "name" : "osd_subdiv_uvs" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "smooth_uv" },
            { "name" : "smooth_uv_borders" }
        ]
    }
]}
"""

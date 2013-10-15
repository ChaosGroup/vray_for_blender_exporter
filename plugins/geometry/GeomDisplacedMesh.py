#
# V-Ray/Blender
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

import bpy

from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'GEOMETRY'
ID   = 'GeomDisplacedMesh'
NAME = "Displacement"
DESC = "Displacement settings"


PluginParams = (
    {
        'attr' : 'mesh',
        'desc' : "The triangle mesh that will be displaced",
        'type' : 'GEOMETRY',
        'default' : "",
    },
    {
        'attr' : 'displacement_tex_color',
        'name' : "Vector Texture",
        'desc' : "The displacement texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'displacement_tex_float',
        'name' : "Float Texture",
        'desc' : "The displacement texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'displacement_amount',
        'desc' : "Determines the displacement amount for white areas in the displacement map; if use_globals is true this is multiplied by the global displacement amount option",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'displacement_shift',
        'desc' : "This constant value is added to the displacement map",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'use_globals',
        'desc' : "If true, the global displacement quality settings will be used",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'view_dep',
        'desc' : "If use_globals is false, this determines if view-dependent tesselation is used",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'edge_length',
        'desc' : "If use_globals is false, this determines the approximate edge length for the sub-triangles",
        'type' : 'FLOAT',
        'default' : 4,
    },
    {
        'attr' : 'max_subdivs',
        'desc' : "If use_globals is false, this determines the maximum subdivisions for a triangle of the original mesh",
        'type' : 'INT',
        'default' : 256,
    },
    {
        'attr' : 'keep_continuity',
        'desc' : "If true, the plugin will attempt to keep the continuity of the displaced surface",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'water_level',
        'desc' : "Geometry below this displacement level will be clipped away",
        'type' : 'FLOAT',
        'default' : -1e+30,
    },
    {
        'attr' : 'map_channel',
        'desc' : "The mapping channel to use for vector and 2d displacement",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'static_displacement',
        'desc' : "If true, the resulting triangles of the displacement algorithm will be inserted into the rayserver as static geometry",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'image_width',
        'desc' : "This parameter overrides the imgWidth paramter from VRayFrameData during the calculation of the subdivision depth",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'cache_normals',
        'desc' : "If this option is equal to 1 then the normals of the generated triangles are cached",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_bounds',
        'desc' : "If true, the min/max values for the displacement texture are specified by the min_bound and max_bound parameters; if false, these are calculated automatically",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'min_bound',
        'desc' : "The lowest value for the displacement texture",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'max_bound',
        'desc' : "The biggest value for the displacement texture",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'resolution',
        'desc' : "Resolution at which to sample the displacement map for 2d displacement",
        'type' : 'INT',
        'default' : 256,
    },
    {
        'attr' : 'precision',
        'desc' : "Increase for curved surfaces to avoid artifacts",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'tight_bounds',
        'desc' : "When this is on, initialization will be slower, but tighter bounds will be computed for the displaced triangles making rendering faster",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'filter_texture',
        'desc' : "Filter the texture for 2d displacement",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'filter_blur',
        'desc' : "The amount of UV space to average for filtering purposes. A value of 1.0 will average thw whole texture",
        'type' : 'FLOAT',
        'default' : 0.001,
    },

    # {
    #     'attr' : 'displace_2d',
    #     'desc' : "Use to enable 2d displacement. Overrides the vector_displacement flag",
    #     'type' : 'BOOL',
    #     'default' : False,
    # },
    # {
    #     'attr' : 'vector_displacement',
    #     'desc' : "When this is 1, the red, green and blue channels of displacement_tex_color will be used to perform vector displacement with base 0.5; if this is 2, then the map matches the Mudbox displacement maps",
    #     'type' : 'INT',
    #     'default' : 0,
    # },
    {
        'attr' : 'type',
        'desc' : "Displacement type",
        'type' : 'ENUM',
        'items' : (
            ('NOR', "Normal", "Normal displacement"),
            ('2D',  "2D",     "2D displacement"),
            ('3D',  "Vector", "Vector displacement"),
        ),
        'skip' : True,
        'default' : 'NOR',
    },
)


def nodeDraw(context, layout, GeomDisplacedMesh):
    layout.prop(GeomDisplacedMesh, 'type')
    layout.prop(GeomDisplacedMesh, 'displacement_amount', text="Amount")


def gui(context, layout, GeomDisplacedMesh):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    split = layout.split()
    col = split.column()
    col.prop(GeomDisplacedMesh, 'displacement_shift', slider=True)
    col.prop(GeomDisplacedMesh, 'water_level', slider=True)
    col.prop(GeomDisplacedMesh, 'resolution')
    col.prop(GeomDisplacedMesh, 'precision')
    if wide_ui:
        col = split.column()
    col.prop(GeomDisplacedMesh, 'type')
    col.prop(GeomDisplacedMesh, 'keep_continuity')
    col.prop(GeomDisplacedMesh, 'filter_texture')
    if GeomDisplacedMesh.filter_texture:
        col.prop(GeomDisplacedMesh, 'filter_blur')
    col.prop(GeomDisplacedMesh, 'use_bounds')
    if GeomDisplacedMesh.use_bounds:
        sub = col.column(align= True)
        sub.prop(GeomDisplacedMesh, 'min_bound', text="Min", slider= True)
        sub.prop(GeomDisplacedMesh, 'max_bound', text="Max", slider= True)

    split = layout.split()
    col = split.column()
    col.prop(GeomDisplacedMesh, 'use_globals')
    if not GeomDisplacedMesh.use_globals:
        split = layout.split()
        col = split.column()
        col.prop(GeomDisplacedMesh, 'edge_length')
        col.prop(GeomDisplacedMesh, 'max_subdivs')
        if wide_ui:
            col = split.column()
        col.prop(GeomDisplacedMesh, 'view_dep')
        col.prop(GeomDisplacedMesh, 'tight_bounds')


def writeDatablock(bus, pluginName, PluginParams, GeomDisplacedMesh, mappedParams):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ofile.write("\n%s %s {" % (ID, pluginName))

    if GeomDisplacedMesh.type == '2D':
        ofile.write("\n\tdisplace_2d=1;")
        ofile.write("\n\tvector_displacement=0;")
    elif GeomDisplacedMesh.type == '3D':
        ofile.write("\n\tdisplace_2d=0;")
        ofile.write("\n\tvector_displacement=1;")
    else:
        ofile.write("\n\tdisplace_2d=0;")
        ofile.write("\n\tvector_displacement=0;")

    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, GeomDisplacedMesh, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName

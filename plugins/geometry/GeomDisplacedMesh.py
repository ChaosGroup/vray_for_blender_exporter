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
import mathutils

from vb30.lib   import ExportUtils
from vb30.debug import Debug


TYPE = 'GEOMETRY'
ID   = 'GeomDisplacedMesh'
NAME = "Displacement"
DESC = "Displacement settings"

PluginParams = (
    {
        'attr' : 'mesh',
        'desc' : "The triangle mesh that will be displaced",
        'type' : 'GEOMETRY',
        'skip' : True,
        'default' : "",
    },
    {
        'attr' : 'displacement_tex_color',
        'name' : "Color",
        'desc' : "The displacement texture",
        'type' : 'TEXTURE',
        'skip' : True,
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'displacement_tex_float',
        'name' : "Float",
        'desc' : "The displacement texture",
        'type' : 'FLOAT_TEXTURE',
        'skip' : True,
        'default' : 0.0,
    },
    {
        'attr' : 'displacement_amount',
        'name' : "Amount",
        'desc' : "Determines the displacement amount for white areas in the displacement map; if use_globals is true this is multiplied by the global displacement amount option",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'displacement_shift',
        'name' : "Shift",
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
        'name' : "Mode",
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

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "type" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "displacement_amount" },
                    { "name" : "displacement_shift" },
                    { "name" : "water_level" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "resolution" },
                    { "name" : "precision" },
                    { "name" : "keep_continuity" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "use_globals" }
        ]
    },

    {   "layout" : "SPLIT",
        "active" : { "prop" : "use_globals" },
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "edge_length" },
                    { "name" : "max_subdivs" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "view_dep" },
                    { "name" : "tight_bounds" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "use_bounds" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "active" : { "prop" : "use_bounds" },
                "attrs" : [
                    { "name" : "min_bound" }
                ]
            },
            {   "layout" : "COLUMN",
                "active" : { "prop" : "use_bounds" },
                "attrs" : [
                    { "name" : "max_bound" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "static_displacement" },
            { "name" : "cache_normals" },
            { "name" : "filter_texture" },
            { "name" : "filter_blur", "active" : { "prop" : "filter_texture" } }
        ]
    }
]}
"""


def nodeDraw(context, layout, GeomDisplacedMesh):
    layout.prop(GeomDisplacedMesh, 'type')
    layout.prop(GeomDisplacedMesh, 'displacement_amount', text="Amount")


def writeDatablock(bus, pluginModule, pluginName, propGroup, mappedParams):
    scene = bus['scene']
    ob    = bus['node']['object']
    o     = bus['output']

    mesh = mappedParams.get('mesh', None)

    texture_float = mappedParams.get('displacement_tex_float', None)
    texture_color = mappedParams.get('displacement_tex_color', None)

    if not mesh:
        Debug("Object \"%s\" Displacement: 'mesh' is not connected!" % ob.name, msgType='ERROR')
        return None

    if propGroup.type == '3D':
        if not texture_color or type(texture_color) == mathutils.Color:
            Debug("Object \"%s\" Displacement: 'Color' texture is not connected!" % ob.name, msgType='ERROR')
            return mesh
    else:
        if not texture_float or type(texture_float) == mathutils.Color:
            Debug("Object \"%s\" Displacement: 'Float' texture is not connected!" % ob.name, msgType='ERROR')
            return mesh

    o.set('OBJECT', pluginModule.ID, pluginName)
    o.writeHeader()

    o.writeAttibute("mesh", mesh)
    if propGroup.type == '2D':
        o.writeAttibute("displace_2d", "1")
        o.writeAttibute("vector_displacement", "0")
        o.writeAttibute("displacement_tex_float", texture_float)
    elif propGroup.type == '3D':
        o.writeAttibute("displace_2d", "0")
        o.writeAttibute("vector_displacement", "1")
        o.writeAttibute("displacement_tex_color", texture_color)
    else:
        o.writeAttibute("displace_2d", "0")
        o.writeAttibute("vector_displacement", "0")
        o.writeAttibute("displacement_tex_float", texture_float)

    ExportUtils.WritePluginParams(bus, pluginModule, pluginName, propGroup, mappedParams)

    o.writeFooter()

    return pluginName

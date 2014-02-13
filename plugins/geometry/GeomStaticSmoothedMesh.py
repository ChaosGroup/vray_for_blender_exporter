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
ID   = 'GeomStaticSmoothedMesh'
NAME = "Subdivision"
DESC = "Subdivision surface settings"

PluginParams = (
    {
        'attr' : 'mesh',
        'desc' : "The triangle mesh that will be displaced",
        'type' : 'GEOMETRY',
        'default' : "",
    },
    {
        'attr' : 'displacement_tex_color',
        'name' : "Color",
        'desc' : "The displacement texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'displacement_tex_float',
        'name' : "Float",
        'desc' : "The displacement texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
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
        'desc' : "The mapping channel to use for vector displacement",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'image_width',
        'desc' : "This parameter overrides the imgWidth paramter from VRayFrameData during the calculation of the subdivision depth",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'cache_normals',
        'desc' : "If this option is equal to 1 then the normals of the generated triangles are cached. It has effect only if the surface is displaced",
        'type' : 'BOOL',
        'default' : 0,
    },
    {
        'attr' : 'use_globals',
        'desc' : "If true, the global displacement quality settings will be used",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'static_subdiv',
        'desc' : "True if the resulting triangles of the subdivision algorithm will be inserted into the rayserver as static geometry",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'view_dep',
        'desc' : "If use_globals is false, this determines if view-dependent tesselation is used",
        'type' : 'INT',
        'default' : 1,
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
        'attr' : 'preserve_map_borders',
        'desc' : "The valid values",
        'type' : 'ENUM',
        'items' : (
            ('-1', "Not Set", ""),
            ('0', "None", ""),
            ('1', "Internal", ""),
            ('2', "All", ""),
        ),
        'default' : '-1',
    },
    {
        'attr' : 'classic_catmark',
        'desc' : "If equal to 1 then the classical Catmull-Clark masks will be used for meshes which contain only quadrangles",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'vector_displacement',
        'name' : "Mode",
        'desc' : "Mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Normal", "Normal displacement"),
            ('1', "Vector", "The red, green and blue channels of \"Texture (Color)\" will be used to perform vector displacement with base 0.5"),
            ('2', "Absolute Tangent", "Mudbox displacement maps in absolute tangent space"),
            ('3', "Vector (Object Space)", "Vector displacement in object space"),
        ),
        'default' : '0',
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "vector_displacement" }
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
                    { "name" : "keep_continuity" },
                    { "name" : "cache_normals" }
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
                    { "name" : "view_dep" }
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
        "active" : { "prop" : "use_bounds" },
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "min_bound" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "max_bound" }
                ]
            }
        ]
    }
]}
"""


def writeDatablock(bus, pluginName, PluginParams, GeomStaticSmoothedMesh, mappedParams):
    scene = bus['scene']
    ob    = bus['node']['object']

    mesh = mappedParams.get('mesh', None)

    if not mesh:
        Debug("Object \"%s\" Displacement: 'mesh' is not connected!" % ob.name, msgType='ERROR')
        return None

    ofile.write("\n%s %s {" % (ID, pluginName))
    ofile.write("\n\tmesh=%s;" % mesh)
    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, GeomStaticSmoothedMesh, mappedParams, PluginParams)
    ofile.write("\n}\n")

    return pluginName

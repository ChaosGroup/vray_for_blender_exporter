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

import bpy
import mathutils

from vb30.lib import ExportUtils
from vb30.lib import utils as LibUtils
from vb30.debug import Debug


TYPE = 'SETTINGS'
ID   = 'BakeView'
NAME = 'Bake'
DESC = "Bake settings"

PluginParams = (
    {
        'attr' : 'bake_node',
        'desc' : "The node to bake",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'target_nodes',
        'desc' : "The target objects for projection baking",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bake_uvwgen',
        'desc' : "The uvw generator",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'dilation',
        'desc' : "Number of pixels to expand around geometry",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'flip_derivs',
        'desc' : "true to flip the texture direction derivatives (reverses bump mapping)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'u_min',
        'desc' : "The minimum u value to bake",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'v_min',
        'desc' : "The minimum v value to bake",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'u_max',
        'desc' : "The maximum u value to bake",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'v_max',
        'desc' : "The maximum v value to bake",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'fov',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.785398,
    },
    {
        'attr' : 'projection_baking',
        'desc' : "Projection baking",
        'type' : 'ENUM',
        'items' : (
            ('0', "Normal", ""),
            ('1', "Projection", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'mode',
        'desc' : "Bake mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Outside", ""),
            ('1', "Inside", ""),
            ('2', "Outside - Inside", ""),
            ('3', "Inside - Outside", ""),
            ('4', "Closest", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'normal',
        'desc' : "Normal mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Smooth", ""),
            ('1', "Geometry", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'max_depth',
        'desc' : "Geometry that is intersected further than this value along the ray will be ignored. If the value is zero then no geometry will be ignored",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ray_offset',
        'desc' : "The ray's beginning will be offseted this much along the normal",
        'type' : 'FLOAT',
        'default' : 0,
    },

    {
        'attr' : 'use',
        'desc' : "Use texture baking",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
    {
        'attr' : 'uv_channel',
        'desc' : "UV channel to use",
        'type' : 'INT',
        'ui' : {
            'min' : 0,
        },
        'skip' : True,
        'default' : False,
    },
    {
        'attr' : 'bake_material',
        'desc' : "Material for \"Bake By Material\"",
        'type' : 'STRING',
        'skip' : True,
        'default' : "",
    },
)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    if not propGroup.use:
        return

    if not propGroup.bake_node:
        Debug("Bake object is not set!", msgType='ERROR')
        return

    bakeObject = LibUtils.GetSceneObject(scene, propGroup.bake_node)
    if not bakeObject:
        Debug("Bake object \"%s\" not found!" % propGroup.bake_node, msgType='ERROR')
        return

    o.set('SETTINGS', 'UVWGenChannel', 'UVWbakeView')
    o.writeHeader()
    o.writeAttribute('uvw_channel', propGroup.uv_channel)
    o.writeAttribute('uvw_transform', mathutils.Matrix.Identity(4))
    o.writeFooter()

    overrideParams.update({
        'bake_node' : LibUtils.GetObjectName(bakeObject),
        'bake_uvwgen' : "UVWbakeView",
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

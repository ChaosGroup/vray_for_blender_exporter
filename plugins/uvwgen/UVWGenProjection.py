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

import math

import bpy
import mathutils

from vb30.lib import ExportUtils
from vb30.lib import utils


TYPE = 'UVWGEN'
ID   = 'UVWGenProjection'
NAME = 'Projection'
DESC = "Projection mapping"

PluginParams = (
    {
        'attr' : 'uvw_transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : "",
    },
    {
        'attr' : 'uvw_transform_tex',
        'desc' : "",
        'type' : 'TRANSFORM_TEXTURE',
        'default' : "",
    },
    {
        'attr' : 'tex_transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : "",
    },
    {
        'attr' : 'camera_settings',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'camera_view',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bitmap',
        'desc' : "If we are projecting a bitmap, this is the bitmap's buffer, we need it to implement vertical/horizontal fit",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'type',
        'desc' : "Mapping type",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('1', "Planar", ""),
            ('2', "Spherical", ""),
            ('3', "Cylindrical", ""),
            ('4', "Ball", ""),
            ('5', "Cubic", ""),
            ('6', "Triplanar", ""),
            ('8', "Perspective", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'fitfill',
        'name' : 'Fit Fill',
        'desc' : "Fit fill",
        'type' : 'ENUM',
        'items' : (
            ('0', "Fit Fill", ""),
            ('1', "Horizontal", ""),
            ('2', "Vertical", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'fittype',
        'name' : 'Fit Type',
        'desc' : "Fit type",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('1', "Match camera film gate", ""),
            ('2', "Match camera resolution", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'u_angle',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 3.14159,
    },
    {
        'attr' : 'v_angle',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.5708,
    },
    {
        'attr' : 'film_gate_w',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'film_gate_h',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'hide_backface',
        'desc' : "Determine whether to project on back faces of polygons when in perspective mode",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'hide_occluded',
        'desc' : "Determine whether to project on occluded points when in perspective mode",
        'type' : 'BOOL',
        'default' : False,
    },
)


def writeDatablock(bus, pluginModule, pluginName, propGroup, mappedParams):
    scene = bus['scene']

    # XXX: Temporary fix for RT callback
    if 'node' not in bus:
        return pluginName

    ob = bus['node'].get('object', None)
    
    o = bus['output']
    o.set(pluginModule.TYPE, pluginModule.ID, pluginName)

    o.writeHeader()

    if ob is not None:
        o.writeAttibute("uvw_transform", utils.AnimatedValue(scene, ob.matrix_world.copy().inverted()))

    ExportUtils.WritePluginParams(bus, pluginModule, pluginName, propGroup, mappedParams)

    o.writeFooter()

    return pluginName


def nodeDraw(context, layout, UVWGenProjection):
    layout.prop(UVWGenProjection, 'type')


def gui(context, layout, UVWGenProjection):
    layout.prop(UVWGenProjection, 'type')
    layout.prop(UVWGenProjection, 'fitfill')
    layout.prop(UVWGenProjection, 'fittype')

    layout.separator()

    split = layout.split()
    row = split.row(align=True)
    row.prop(UVWGenProjection, 'u_angle')
    row.prop(UVWGenProjection, 'v_angle')
    
    split = layout.split()
    row = split.row(align=True)
    row.prop(UVWGenProjection, 'film_gate_w')
    row.prop(UVWGenProjection, 'film_gate_h')

    split = layout.split()
    row = split.row()
    row.prop(UVWGenProjection, 'hide_backface')
    row.prop(UVWGenProjection, 'hide_occluded')

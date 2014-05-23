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

import re

import bpy

from vb30.lib import ExportUtils, LibUtils


TYPE = 'EFFECT'
ID   = 'SphereFade'
NAME = 'Sphere Fade'
DESC = ""

PluginParams = (
    {
        'attr' : 'gizmos',
        'name' : "Gizmo 1",
        'desc' : "List of gizmos",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'empty_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'affect_alpha',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'falloff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
)


def nodeDraw(context, layout, propGroup):
    split = layout.split()
    col = split.column()
    col.prop(propGroup, 'empty_color', text="")
    col.prop(propGroup, 'falloff')
    col.prop(propGroup, 'affect_alpha')

    layout.separator()

    split = layout.split()
    row = split.row(align=True)

    addOp = row.operator('vray.node_list_socket_add', icon="ZOOMIN", text="Add")
    addOp.socketType = 'VRaySocketObject'
    addOp.socketName = 'Gizmo'
    addOp.vray_attr  = "gizmos"

    row.operator('vray.node_list_socket_del', icon="ZOOMOUT", text="")


def gui(context, layout, SphereFade):
    split = layout.split()
    col = split.column()
    col.prop(SphereFade, 'empty_color')
    col.prop(SphereFade, 'affect_alpha')
    col.prop(SphereFade, 'falloff')


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams): 
    gizmos = LibUtils.GetAsList(overrideParams['gizmos'])

    for key in overrideParams:
        if re.match("^gizmos\d+", key):
            gizmos.append(overrideParams[key])

    gizmos = filter(None, gizmos)

    overrideParams['gizmos'] = "List(%s)" % ",".join(gizmos)

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

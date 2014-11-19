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


TYPE = 'EFFECT'
ID   = 'SphereFadeGizmo'
NAME = 'Sphere Fade Gizmo'
DESC = ""

PluginParams = (
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'radius',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'invert',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },

    {
        'attr' : 'object',
        'desc' : "",
        'type' : 'STRING',
        'skip' :  True,
        'default' : "",
    },
)

PluginWidget = '{ "widgets": [] }'


def nodeDraw(context, layout, SphereFadeGizmo):
    layout.prop_search(SphereFadeGizmo,   'object',
                       bpy.context.scene, 'objects',
                       text="")

    ob = None
    if SphereFadeGizmo.object:
        if SphereFadeGizmo.object in bpy.context.scene.objects:
            ob = bpy.context.scene.objects[SphereFadeGizmo.object]

    if ob and not ob.type == 'EMPTY':
        layout.prop(SphereFadeGizmo, 'radius')

    layout.prop(SphereFadeGizmo, 'invert')

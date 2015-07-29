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

import math

import bpy
import bgl
import mathutils

from bpy_extras.view3d_utils import location_3d_to_region_2d

from vb30.lib import LibUtils


handlers = []


CircleShape = (
    (0.000,1.000,0.000),
    (-0.195,0.981,0.000),
    (-0.383,0.924,0.000),
    (-0.556,0.831,0.000),
    (-0.707,0.707,0.000),
    (-0.831,0.556,0.000),
    (-0.924,0.383,0.000),
    (-0.981,0.195,0.000),
    (-1.000,0.000,0.000),
    (-0.981,-0.195,0.000),
    (-0.924,-0.383,0.000),
    (-0.831,-0.556,0.000),
    (-0.707,-0.707,0.000),
    (-0.556,-0.831,0.000),
    (-0.383,-0.924,0.000),
    (-0.195,-0.981,0.000),
    (0.000,-1.000,0.000),
    (0.195,-0.981,0.000),
    (0.383,-0.924,0.000),
    (0.556,-0.831,0.000),
    (0.707,-0.707,0.000),
    (0.831,-0.556,0.000),
    (0.924,-0.383,0.000),
    (0.981,-0.195,0.000),
    (1.000,0.000,0.000),
    (0.981,0.195,0.000),
    (0.924,0.383,0.000),
    (0.831,0.556,0.000),
    (0.707,0.707,0.000),
    (0.556,0.831,0.000),
    (0.383,0.924,0.000),
    (0.195,0.981,0.000),
)

RectangleShape = (
    ( 1.0,  1.0, 0.0),
    ( 1.0, -1.0, 0.0),
    (-1.0, -1.0, 0.0),
    (-1.0,  1.0, 0.0),
)

RectangleShape2 = (
    (0.0,  1.0, 0.0),
    (0.0, -1.0, 0.0),
    ( 1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
)


ui_theme   = bpy.context.user_preferences.themes[0]
lamp_color = ui_theme.view_3d.lamp
lamp_color_off = (0.0,0.0,0.0,1.0)


def vray_draw_point(p, mult, tm=mathutils.Matrix.Identity(4)):
    _p = mathutils.Vector((p[0], p[1], p[2])) * mult
    _p3d = tm * _p
    _p2d = location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, _p3d)
    bgl.glVertex2f(*_p2d)


def vray_draw_shape(shape, mult, tm=mathutils.Matrix.Identity(4)):
    bgl.glBegin(bgl.GL_LINES)
    i = 0
    while i < len(shape):
        ci = i
        ni = 0 if i == len(shape) - 1 else i + 1
        vray_draw_point(shape[ci], mult, tm)
        vray_draw_point(shape[ni], mult, tm)
        i += 1
    bgl.glEnd()


def vray_draw_light_sphere_shape(ob):
    r = ob.data.vray.LightSphere.radius

    vray_draw_shape(CircleShape, r, ob.matrix_world)
    vray_draw_shape(CircleShape, r, ob.matrix_world * mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X'))
    vray_draw_shape(CircleShape, r, ob.matrix_world * mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y'))


def vray_draw_light_direct_shape(ob):
    r = ob.data.vray.LightDirectMax.fallsize

    top_tm    = ob.matrix_world
    bottom_tm = ob.matrix_world * mathutils.Matrix.Translation((0.0, 0.0, -ob.data.distance))

    if ob.data.vray.LightDirectMax.shape_type == '0':
        vray_draw_shape(CircleShape, r, top_tm)
        vray_draw_shape(CircleShape, r, bottom_tm)

        bgl.glBegin(bgl.GL_LINES)
        vray_draw_point(RectangleShape2[0], r, top_tm)
        vray_draw_point(RectangleShape2[0], r, bottom_tm)
        vray_draw_point(RectangleShape2[1], r, top_tm)
        vray_draw_point(RectangleShape2[1], r, bottom_tm)
        vray_draw_point(RectangleShape2[2], r, top_tm)
        vray_draw_point(RectangleShape2[2], r, bottom_tm)
        vray_draw_point(RectangleShape2[3], r, top_tm)
        vray_draw_point(RectangleShape2[3], r, bottom_tm)
        bgl.glEnd()
    else:
        vray_draw_shape(RectangleShape, r, top_tm)
        vray_draw_shape(RectangleShape, r, bottom_tm)

        bgl.glBegin(bgl.GL_LINES)
        vray_draw_point(RectangleShape[0], r, top_tm)
        vray_draw_point(RectangleShape[0], r, bottom_tm)
        vray_draw_point(RectangleShape[1], r, top_tm)
        vray_draw_point(RectangleShape[1], r, bottom_tm)
        vray_draw_point(RectangleShape[2], r, top_tm)
        vray_draw_point(RectangleShape[2], r, bottom_tm)
        vray_draw_point(RectangleShape[3], r, top_tm)
        vray_draw_point(RectangleShape[3], r, bottom_tm)
        bgl.glEnd()


def vray_draw_light_shape():
    if not bpy.context:
        return
    ob = bpy.context.active_object
    if not ob:
        return
    if ob.type not in {'LAMP'}:
        return

    la = ob.data

    VRayLight = LibUtils.GetLightPropGroup(la)

    bgl.glEnable(bgl.GL_POINT_SMOOTH)
    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

    col = lamp_color if VRayLight.enabled else lamp_color_off
    bgl.glColor4f(*col)

    if la.type == 'POINT':
        if la.vray.omni_type == 'SPHERE':
            vray_draw_light_sphere_shape(ob)
    elif la.type == 'SUN':
        if la.vray.direct_type == 'DIRECT':
            vray_draw_light_direct_shape(ob)

    # Reset draw
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


RegClasses = ()


def register():
    global handlers

    def vray_draw_handler_add(cb):
        handlers.append(bpy.types.SpaceView3D.draw_handler_add(cb, (), 'WINDOW', 'POST_PIXEL'))

    for regClass in RegClasses:
        bpy.utils.register_class(regClass)

    vray_draw_handler_add(vray_draw_light_shape)


def unregister():
    global handlers

    for regClass in RegClasses:
        bpy.utils.unregister_class(regClass)

    for handle in handlers:
        bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
    handlers = []

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

import bpy

from vb25.lib import ExportUtils


TYPE = 'CAMERA'
ID   = 'RenderView'
NAME = 'Render view'
DESC = "Render view settings"

PluginParams = (
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
        'attr' : 'focalDistance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'aperture',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'lens_rotation',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'frame_samples',
        'desc' : "Number of samples per frame for the transformation",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'clipping',
        'desc' : "true to enable clipping planes",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'clipping_near',
        'desc' : "The near clipping plane",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'clipping_far',
        'desc' : "The far clipping plane",
        'type' : 'FLOAT',
        'default' : 1e+18,
    },
    {
        'attr' : 'zoom',
        'desc' : "Zoom factor",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'orthographic',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'orthographicWidth',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'dont_affect_settings',
        'desc' : "This is here so we can suppress a RenderView node from affecting the main VRayRenderer sequence and frame data",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'use_scene_offset',
        'desc' : "If true, the scene will be internally translated relative to the render view",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mayaFocalLength',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'mayaApperture',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
)


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    ca    = bus['camera']

    VRayScene = scene.vray
    VRayBake  = VRayScene.BakeView

    if VRayBake.use:
        return

    VRayCamera = ca.data.vray

    fov = VRayCamera.fov if VRayCamera.override_fov else ca.data.angle
    
    aspect = float(scene.render.resolution_x) / float(scene.render.resolution_y)

    if aspect < 1.0:
        fov = fov * aspect

    overrideParams = {
        'fov' : fov,
        'orthographic' : ca.data.type == 'ORTHO',
        'use_scene_offset' : False if bus["engine"] == 'VRAY_RENDER_RT' else True,
        'clipping_near' : ca.data.clip_start,
        'clipping_far' : ca.data.clip_end,
        'transform' : ca.matrix_world,
    }

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

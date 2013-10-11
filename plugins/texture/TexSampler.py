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


TYPE = 'TEXTURE'
ID   = 'TexSampler'
NAME = 'Sampler'
DESC = ""

PluginParams = (
    {
        'attr' : 'point',
        'desc' : "The shading point in world space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'pointReference',
        'desc' : "The shading point in reference space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'pointObject',
        'desc' : "The shading point in object space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'pointCamera',
        'desc' : "The shading point in camera space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'normal',
        'desc' : "The smooth normal in world space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'normalReference',
        'desc' : "The smooth normal in reference space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'normalCamera',
        'desc' : "The smooth normal in camera space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'normalObject',
        'desc' : "The smooth normal in object space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'bumpNormal',
        'desc' : "The bump normal in world space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'bumpNormalCamera',
        'desc' : "The bump map normal in camera space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'bumpNormalObject',
        'desc' : "The bump map normal in object space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'gnormal',
        'desc' : "The geometric normal in world space",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'camToWorld',
        'desc' : "The transformation from camera to world space",
        'type' : 'OUTPUT_TRANSFORM_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'view_dir',
        'desc' : "The viewing direction",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'frame_time',
        'desc' : "The current frame (image) time",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'ray_time',
        'desc' : "The ray time within the motion blur interval",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'facing_ratio',
        'desc' : "The cosine of the angle between the normal and the viewing direction",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'material_id',
        'desc' : "The surface material id, if the surface supports it",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'flipped_normal',
        'desc' : "Zero if the face is front facing and one if it is backfacing the camera",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'cameraNearClipPlane',
        'desc' : "The camera near clipping plane, calculated from the scene bounding box and the camera transform in the frame data",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'cameraFarClipPlane',
        'desc' : "The camera far clipping plane, calculated from the scene bounding box and the camera transform in the frame data",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'uvCoord',
        'desc' : "The uvw coordinates of the point being shaded. These are the coordinates of channel 0",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'rayDirection',
        'desc' : "The viewing direction in camera space. Used for the samplerInfo node in Maya",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'pixelCenter',
        'desc' : "The current sample image coordinates. Used for the samplerInfo node in Maya",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'tangentUCamera',
        'desc' : "The U axis of the currently shaded point's UVW space, transformed in camera space. UV channel 0 is used",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'tangentVCamera',
        'desc' : "The V axis of the currently shaded point's UVW space, transformed in camera space. UV channel 0 is used",
        'type' : 'OUTPUT_VECTOR_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'ray_depth',
        'desc' : "The ray depth",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'path_length',
        'desc' : "The path length",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
)


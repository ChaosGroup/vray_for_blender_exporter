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


TYPE = 'EFFECT'
ID   = 'VolumeVRayToon'
NAME = 'Toon'
DESC = ""

PluginParams = (
    {
        'attr' : 'lineColor',
        'desc' : "The color of cartoon line",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'widthType',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'lineWidth',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.5,
    },
    {
        'attr' : 'opacity',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'hideInnerEdges',
        'desc' : "true : show outlines and not interior edges, false : show all edges",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'normalThreshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.7,
    },
    {
        'attr' : 'overlapThreshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.95,
    },
    {
        'attr' : 'traceBias',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'doSecondaryRays',
        'desc' : "true : show toon lines in reflections",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'excludeType',
        'desc' : "true : apply toon effect only to objects in excludeList; false : apply toon effect to all objects out of excludeList",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'compensateExposure',
        'desc' : "Compensate VRay physical camera exposure",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'excludeList',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'lineColor_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'lineWidth_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'opacity_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'distortion_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
)

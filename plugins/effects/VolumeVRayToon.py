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
from vb25.lib import utils as LibUtils


TYPE = 'EFFECT'
ID   = 'VolumeVRayToon'
NAME = 'Toon'
DESC = ""

PluginParams = (
    # {
    #     'attr' : 'lineColor',
    #     'desc' : "The color of cartoon line",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'lineColor_tex',
        'name' : "Color",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'lineWidth',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1.5,
    # },
    {
        'attr' : 'lineWidth_tex',
        'name' : "Width",
        'desc' : "",
        'skip' : True,
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    # {
    #     'attr' : 'opacity',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },
    {
        'attr' : 'opacity_tex',
        'name' : "Opacity",
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'distortion_tex',
        'name' : "Distortion",
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.0,
    },
    {
        'attr' : 'widthType',
        'name' : 'Width Type',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "Pixels", ""),
            ('1', "World", ""),
        ),
        'default' : '0',
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
        'name' : 'List Type',
        'desc' : "Exclude list behavior",
        'type' : 'ENUM',
        'items' : (
            ('0', "Exclude", ""),
            ('1', "Include", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'compensateExposure',
        'desc' : "Compensate VRay physical camera exposure",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'excludeList',
        'name' : "List",
        'desc' : "",        
        'type' : 'PLUGIN',
        'skip' : True,
        'default' : "",
    },
)


def nodeDraw(context, layout, VolumeVRayToon):
    layout.prop(VolumeVRayToon, 'widthType', text="Width")
    layout.prop(VolumeVRayToon, 'excludeType', text="List")


def gui(context, layout, VolumeVRayToon):
    split = layout.split()
    col = split.column()
    col.prop(VolumeVRayToon, 'normalThreshold')
    col.prop(VolumeVRayToon, 'overlapThreshold')
    col.prop(VolumeVRayToon, 'traceBias')
    col.prop(VolumeVRayToon, 'hideInnerEdges')
    col.prop(VolumeVRayToon, 'doSecondaryRays')
    col.prop(VolumeVRayToon, 'compensateExposure')


def writeDatablock(bus, pluginName, PluginParams, VolumeVRayToon, mappedParams):
    ofile = bus['files']['environment']
    scene = bus['scene']

    excludeList = [ LibUtils.GetObjectName(ob) for ob in mappedParams['excludeList'] ]
    
    ofile.write("\n%s %s {" % (ID, pluginName))
    ofile.write("\n\texcludeList=List(%s);" % ",".join(excludeList))

    # XXX: When size is in pixels lineWidth_tex value is ignored
    #
    if type(mappedParams['lineWidth_tex']) is str:
        ofile.write("\n\tlineWidth_tex=%s;" % mappedParams['lineWidth_tex'])
    else:
        ofile.write("\n\tlineWidth=%s;" % LibUtils.AnimatedValue(scene, mappedParams['lineWidth_tex']))
    
    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, VolumeVRayToon, mappedParams, PluginParams)

    ofile.write("\n}\n")

    bus['volumes'].add(pluginName)
    
    return pluginName

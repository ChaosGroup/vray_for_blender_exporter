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

import _vray_for_blender

from vb30.lib import ExportUtils, BlenderUtils
from vb30.lib import LibUtils


TYPE = 'EFFECT'
ID   = 'EnvFogMeshGizmo'
NAME = 'Fog Gizmo'
DESC = "Simulation domain"

PluginParams = (
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'skip' : True,
        'default' : None,
    },
    {
        'attr' : 'geometry',
        'name' : "Object",
        'desc' : "",
        'skip' : True,
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'lights',
        'desc' : "",
        'skip' : True,
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'fade_out_radius',
        'desc' : "fade out effect for the edges",
        'type' : 'FLOAT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "fade_out_radius" }
        ]
    }
]}
"""


def writeEnvFogMeshGizmo(bus, ob, lights, pluginName):
    scene = bus['scene']
    o     = bus['output']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    geomName = BlenderUtils.GetObjectName(ob, prefix='ME')
    if geomName in bus['cache']['mesh']:
        return

    bus['cache']['mesh'].add(geomName)

    if VRayExporter.auto_meshes:
        _vray_for_blender.exportMesh(
            bpy.context.as_pointer(),   # Context
            ob.as_pointer(),            # Object
            geomName,                   # Result plugin name
            None,                       # propGroup
            o.fileManager.getFileByPluginType('GEOMETRY') # Output file
        )

    o.set(TYPE, ID, pluginName)
    o.writeHeader()
    o.writeAttibute('geometry', geomName)
    o.writeAttibute('transform', ob.matrix_world)
    if lights:
        o.writeAttibute('lights', "List(%s)" % lights)
    o.writeFooter()

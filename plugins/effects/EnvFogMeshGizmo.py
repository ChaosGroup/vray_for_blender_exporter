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

import _vray_for_blender

from vb25.lib import ExportUtils
from vb25.lib import utils as LibUtils
from vb25     import utils


TYPE = 'EFFECT'
ID   = 'EnvFogMeshGizmo'
NAME = 'Fog Mesh Gizmo'
DESC = ""

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


def writeDatablock(bus, pluginName, PluginParams, EnvFogMeshGizmo, mappedParams):
    ofile = bus['files']['environment']
    scene = bus['scene']

    domainName = mappedParams.get('geometry', None)
    if domainName is None:
        return None

    if not domainName or not domainName in scene.objects:
        return None

    domainObject = scene.objects[domainName]

    # Write smoke domain
    domainPluginName = utils.get_name(domainObject, prefix='MG')

    _vray_for_blender.exportMesh(
        bpy.context.as_pointer(),  # Context
        domainObject.as_pointer(), # Object
        domainPluginName,          # Result plugin name
        ofile                      # Output file
    )

    ofile.write("\n%s %s {" % (ID, pluginName))
    ofile.write("\n\tgeometry=%s;" % domainPluginName)
    ofile.write("\n\ttransform=%s;" % LibUtils.AnimatedValue(scene, domainObject.matrix_world))
    
    ExportUtils.WritePluginParams(bus, ofile, ID, pluginName, EnvFogMeshGizmo, mappedParams, PluginParams)

    ofile.write("\n}\n")

    bus['object_exclude'].add(domainName)

    return pluginName

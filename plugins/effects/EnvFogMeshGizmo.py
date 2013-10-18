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
import mathutils

import _vray_for_blender

from vb25.lib import ExportUtils
from vb25.lib import utils as LibUtils
from vb25     import utils


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


def writeDatablock(bus, pluginName, PluginParams, EnvFogMeshGizmo, mappedParams):
    ofile = bus['files']['environment']
    scene = bus['scene']

    lights = mappedParams.get('lights', "")

    domainObject = mappedParams.get('geometry', None)
    if domainObject is None:
        return None
    
    if type(domainObject) is list:
        domainObject = domainObject[0]

    if not domainObject:
        return None

    smd = LibUtils.GetSmokeModifier(domainObject)
    if not smd:
        return None

    pluginName = LibUtils.GetObjectName(domainObject, prefix='MG')

    _vray_for_blender.exportSmokeDomain(
        bpy.context.as_pointer(),   # Context
        domainObject.as_pointer(),  # Object
        smd.as_pointer(),           # SmokeModifierData
        pluginName,                 # Result plugin name
        lights,                     # Lights (string)
        ofile                       # Output file
    )

    bus['object_exclude'].add(domainObject.name)

    return pluginName

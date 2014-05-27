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

import _vray_for_blender

from vb30.lib import ExportUtils, LibUtils, BlenderUtils


TYPE = 'TEXTURE'
ID   = 'TexMayaFluid'
NAME = 'Phoenix Fluid'
DESC = "Fluid data texture for Phoenix shader"

PluginParams = (
    {
        'attr' : 'interpolation_type',
        'desc' : "Interpolation type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Linear",    "Linear interpolation"),
            ('1', "Quadratic", "Quadratic interpolation"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'mb_type',
        'name' : "Motion Blur",
        'desc' : "Motion blur type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Disabled", ""),
            ('1', "Blend", ""),
            ('2', "Velocity", ""),
            ('3', "Velocity + Blend", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'frame_duration',
        'desc' : "The frame duration in sec",
        'type' : 'FLOAT',
        'default' : 0.0416667,
    },
    {
        'attr' : 'cache_frame',
        'desc' : "Converts the current frame number to cache frame number",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'out_flame',
        'desc' : "Flame",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'out_fuel',
        'desc' : "Fuel",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'out_density',
        'desc' : "Density",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },

    {
        'attr' : 'domain',
        'name' : "Domain",
        'desc' : "Simulation domain",
        'type' : 'GEOMETRY',
        'skip' : True,
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "interpolation_type" },
            { "name" : "mb_type" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    domainObject = overrideParams.get('domain', None)
    if domainObject is None:
        return None
    
    if type(domainObject) is list:
        domainObject = domainObject[0]

    if not domainObject:
        return None

    smd = BlenderUtils.GetSmokeModifier(domainObject)
    if not smd:
        return None

    _vray_for_blender.exportFluid(
        bpy.context.as_pointer(),     # Context
        domainObject.as_pointer(),    # Object
        smd.as_pointer(),             # SmokeModifierData
        propGroup,                    # Property group
        pluginName,                   # Result plugin name
        o.fileManager.getFileByPluginType('GEOMETRY'),  # Output file
    )

    return pluginName

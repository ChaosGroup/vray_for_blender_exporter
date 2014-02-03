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

from vb30.lib import ExportUtils
from vb30.lib import utils as LibUtils


TYPE = 'TEXTURE'
ID   = 'TexSky'
NAME = 'Sky'
DESC = ""

PluginParams = (
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'target_transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'turbidity',
        'desc' : "Determines the amount of dust in the air and affects the color of the sun and sky. Smaller values produce a clear/blue sky, larger values yellow and orange",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 2.0,
        },
        'default' : 3,
    },
    {
        'attr' : 'ozone',
        'desc' : "Affects the color of the sun light (between 0.0 and 1.0). Smaller values make the sunlight more yellow, larger values make it blue",
        'type' : 'FLOAT',
        'default' : 0.35,
    },
    {
        'attr' : 'water_vapour',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'intensity_multiplier',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'size_multiplier',
        'desc' : "Controls the visible size of the sun. Affects the appearance of the sun disc as seen by the camera and reflections, as well as the blurriness of the sun shadows",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'filter_color',
        'desc' : "Sunlight color. Used to add user control to light color definition",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'invisible',
        'desc' : "When on, this option makes the sun invisible, both to the camera and to reflections",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'horiz_illum',
        'desc' : "Specifies the intensity (in Lx) of the illumination on horizontal surfaces coming from the sky",
        'type' : 'FLOAT',
        'default' : 25000,
    },
    {
        'attr' : 'sky_model',
        'desc' : "Selects the procedural model used to simulate the TexSky texture",
        'type' : 'ENUM',
        'items' : (
            ('0', "Preetham et al.", ""),
            ('1', "CIE Clear", ""),
            ('2', "CIE Overcast", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'sun_dir_only',
        'desc' : "Use only direction of the specified sun (don't inherit all other parameters)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'auto_sun',
        'name' : "Find Sun Automatically",
        'desc' : "Attach Sun automatically and take settings from it",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True,
    },
    {
        'attr' : 'sun',
        'desc' : "If specified, all parameters are taken from the sun; otherwise, the sky parameters are used",
        'type' : 'PLUGIN',
        'skip' : True,
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "align" : false,
        "attrs" : [
            { "name" : "auto_sun" },
            { "name" : "invisible", "label" : "Sun Invisible" }
        ]
    },

    {   "layout" : "ROW",
        "align" : false,
        "attrs" : [
            { "name" : "sky_model" }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "turbidity" },
                    { "name" : "ozone" },
                    { "name" : "intensity_multiplier" },
                    { "name" : "size_multiplier" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "horiz_illum" },
                    { "name" : "water_vapour" }
                ]
            }
        ]
    }
]}
"""


def FindSun(scene):
    for ob in [ob for ob in scene.objects if ob.type == 'LAMP']:
        if ob.data.type == 'SUN' and ob.data.vray.direct_type == 'SUN':
            return ob
    return None


def writeDatablock(bus, pluginModule, pluginName, propGroup, mappedParams):
    scene = bus['scene']
    o     = bus['output']
    
    sunObject = mappedParams.get('sun', None)
    if sunObject:      
        if type(sunObject) is list:
            sunObject = sunObject[0]
    else:
        if propGroup.auto_sun:
            sunObject = FindSun(scene)

    o.set(pluginModule.TYPE, pluginModule.ID, pluginName)

    o.writeHeader()

    if sunObject:
        o.writeAttibute("sun", LibUtils.GetObjectName(sunObject))

    ExportUtils.WritePluginParams(bus, pluginModule, pluginName, propGroup, mappedParams)

    o.writeFooter()

    return pluginName

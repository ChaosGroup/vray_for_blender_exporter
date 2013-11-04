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


TYPE = 'BRDF'
ID   = 'BRDFLight'
NAME = 'Light'
DESC = ""

PluginParams = (
    {
        'attr' : 'color',
        'desc' : "The self-illumination color",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'colorMultiplier',
        'desc' : "Color Multiplier",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'transparency',
        'desc' : "Transparency of the BRDF",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'doubleSided',
        'desc' : "If false, the light color is black for back-facing surfaces",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'emitOnBackSide',
        'desc' : "Emit on back side",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'channels',
        'desc' : "Render channels the result of this BRDF will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'compensateExposure',
        'desc' : "Compensate camera exposure",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'multiplyByOpacity',
        'desc' : "When enabled the color of the light brdf is multiplied by the brdf's opacity (inverse of the brdf's transparency)",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "doubleSided" },
                    { "name" : "emitOnBackSide" }
                ]
            },
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "compensateExposure" },
                    { "name" : "multiplyByOpacity" }
                ]
            }
        ]
    }
]}
"""

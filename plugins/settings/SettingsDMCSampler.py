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

from vb30.lib import ExportUtils


TYPE = 'SETTINGS'
ID   = 'SettingsDMCSampler'
NAME = 'DMC Sampler'
DESC = ""

PluginParams = (
    {
        'attr' : 'time_dependent',
        'desc' : "This make the samping pattern change with time",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adaptive_amount',
        'desc' : "A value of 1.0 means full adaptation; a value of 0.0 means no adaptation",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 0.0,
            'max' : 1.0,
        },
        'default' : 0.85,
    },
    {
        'attr' : 'adaptive_threshold',
        'desc' : "Controls V-Ray's judgement of when a blurry value is \"good enough\" to be used",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 0.0,
            'max' : 1.0,
        },
        'default' : 0.01,
    },
    {
        'attr' : 'adaptive_min_samples',
        'desc' : "The minimum number of samples that must be made before the early termination algorithm is used",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'subdivs_mult',
        'desc' : "This will multiply all subdivs values everywhere during rendering",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'path_sampler_type',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "0", ""),
            ('1', "1", ""),
            ('2', "2", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'div_shade_subdivs',
        'name' : "Divide Shading Subdivs",
        'desc' : "Allow VRay to divide the number of samples for lights, materials etc by the number of AA samples in order to achieve roughly the same quality and number of rays when changing AA settings",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "adaptive_amount", "slider" : true },
                    { "name" : "adaptive_threshold", "label" : "Noise Thresh." },
                    { "name" : "subdivs_mult" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "adaptive_min_samples", "label" : "Min. Samples" },
                    { "name" : "time_dependent" },
                    { "name" : "div_shade_subdivs" }
                ]
            }
        ]
    }
]}
"""

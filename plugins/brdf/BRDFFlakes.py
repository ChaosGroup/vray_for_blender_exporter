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


TYPE = 'BRDF'
ID   = 'BRDFFlakes'
NAME = 'Flakes'
DESC = ""

PluginParams = (
    {
        'attr' : 'flake_color',
        'name' : "Color",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.3, 0.4, 0.8),
    },
    {
        'attr' : 'flake_glossiness',
        'name' : "Glossiness",
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'flake_orientation',
        'name' : "Orientation",
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.3,
    },
    {
        'attr' : 'flake_density',
        'name' : "Density",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_scale',
        'name' : "Scale",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'flake_size',
        'name' : "Size",
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_map_size',
        'name' : "Map Size",
        'desc' : "The size of the internal flakes map",
        'type' : 'INT',
        'default' : 1024,
    },
    {
        'attr' : 'flake_filtering_mode',
        'name' : 'Filtering Mode',
        'desc' : "Flake filtering mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Simple", ""),
            ('1', "Directional", ""),

        ),
        'default' : '1',
    },
    {
        'attr' : 'flake_seed',
        'name' : 'Seed',
        'desc' : "The random seed for the flakes",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'flake_uvwgen',
        'name' : 'Uvwgen',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'traceReflections',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'doubleSided',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'cutoff_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'mapping_type',
        'desc' : "The mapping method for the flakes",
        'type' : 'ENUM',
        'items' : (
            ('0', "Explicit",  "Explicit mapping channel"),
            ('1', "Triplanar", "Triplanar projection in object space"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'mapping_channel',
        'desc' : "The mapping channel when the mapping_type is 0",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'environment_override',
        'desc' : "Environment override texture",
        'type' : 'TEXTURE',
        'options' : ['LINKED_ONLY'],
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_density" },
                    { "name" : "flake_scale" },
                    { "name" : "flake_size" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "flake_filtering_mode", "label" : "" },
                    { "name" : "flake_map_size" },
                    { "name" : "flake_seed" },
                    { "name" : "traceReflections" }
                ]
            }
        ]
    },

    {   "layout" : "SEPARATOR",
        "label" : "Options" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "subdivs" },
                    { "name" : "cutoff_threshold", "label" : "Cutoff" },
                    { "name" : "doubleSided" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "mapping_type", "label" : "" },
                    { "name" : "mapping_channel" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "environment_priority" }
        ]
    }
]}
"""

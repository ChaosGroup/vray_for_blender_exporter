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

from vb30.lib import ExportUtils


TYPE = 'BRDF'
ID   = 'BRDFBump'
NAME = 'Bump'
DESC = ""

PluginParams = (
    {
        'attr' : 'base_brdf',
        'desc' : "Base BRDF",
        'type' : 'BRDF',
        'default' : "",
    },
    {
        'attr' : 'bump_tex_float',
        'name' : "Bump Texture",
        'desc' : "Bump texture",
        'type' : 'FLOAT_TEXTURE',
        'options' : ['LINKED_ONLY'],
        'default' : 1.0,
    },
    {
        'attr' : 'bump_tex_color',
        'name' : "Normal Texture",
        'desc' : "Normal texture",
        'type' : 'TEXTURE',
        'options' : ['LINKED_ONLY'],
        'default' : (0.0, 0.0, 0.0),
    },
    {
        'attr' : 'bump_tex_mult',
        'name' : "Bump Amount",
        'desc' : "Bump amount",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'bump_tex_mult_tex',
        'name' : "Bump Amount",
        'desc' : "Bump amount",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.1,
    },
    {
        'attr' : 'bump_shadows',
        'desc' : "true to offset the surface shading point, in addition to the normal",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'map_type',
        'name' : "Type",
        'desc' : "The type of the map",
        'type' : 'ENUM',
        'items' : (
            ('0', "Bump",              ""),
            ('1', "Normal (Tangent)" , ""),
            ('2', "Normal (Object)",   ""),
            ('3', "Normal (Camera)",   ""),
            ('4', "Normal (World)",    ""),
            ('5', "From Bump",         ""),
            ('6', "Explicit Normal",   ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'normal_uvwgen',
        'desc' : "The uvw generator for the normal map texture when \"Type\" is \"Normal (Tangent)\"",
        'type' : 'UVWGEN',
        'default' : "",
    },
    {
        'attr' : 'maya_compatible',
        'desc' : "When this is true the BRDFBump will try to match the Maya bump/normal mapping",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'compute_bump_for_shadows',
        'desc' : "true to compute bump mapping for shadow rays in case the material is transparent; false to skip the bump map for shadow rays (faster rendering)",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'bump_delta_scale',
        'desc' : "Scale for sampling the bitmap when map_type is 0. Normally this is tied to the ray differentials, but can be changed if necessary",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "bump_delta_scale" },
            { "name" : "bump_shadows" },
            { "name" : "compute_bump_for_shadows" },
            { "name" : "maya_compatible" }
        ]
    }
]}
"""


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'map_type')


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    overrideParams.update({
        'bump_tex_mult' : 1.0,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

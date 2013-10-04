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

from vb25.lib   import ExportUtils
from vb25.ui.ui import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'MATERIAL'
ID   = 'MtlBump'
NAME = 'MtlBump'
DESC = ""

PluginParams = (
    {
        'attr' : 'base_mtl',
        'desc' : "Base material",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bump_tex_color',
        'desc' : "Bump texture",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'bump_tex_float',
        'desc' : "Bump texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'bump_tex_mult',
        'desc' : "Bump amount",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'bump_tex_mult_tex',
        'desc' : "Bump amount texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'bump_tex',
        'desc' : "Bump texture; this is deprecated, use bump_tex_color or bump_tex_float instead",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bump_shadows',
        'desc' : "true to offset the surface shading point, in addition to the normal",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bump_delta_scale',
        'desc' : "Scale for sampling the bitmap when map_type is 0. Normally this is tied to the ray differentials, but can be changed if necessary",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'maya_compatible',
        'desc' : "When this is true the BRDFBump will try to match the Maya bump/normal mapping",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'map_type',
        'desc' : "The type of the map (0 - from regular texture output, 1 - normal map in tangent space, 2 - normal map in object space, 3 - normal map in camera space, 4 - normal map in world space, 5 - from texture bump output, 6 - explicit normal)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'normal_uvwgen',
        'desc' : "The uvw generator for the normal map texture when map_type is 1",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'compute_bump_for_shadows',
        'desc' : "true to compute bump mapping for shadow rays in case the material is transparent; false to skip the bump map for shadow rays (faster rendering)",
        'type' : 'BOOL',
        'default' : True,
    },
)

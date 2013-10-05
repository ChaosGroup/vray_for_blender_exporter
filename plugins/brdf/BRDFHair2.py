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
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'BRDF'
ID   = 'BRDFHair2'
NAME = 'Hair2'
DESC = ""

PluginParams = (
    {
        'attr' : 'diffuse_color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'refraction_index',
        'desc' : "Index of refraction for the hair",
        'type' : 'FLOAT',
        'default' : 1.55,
    },
    {
        'attr' : 'absorption',
        'desc' : "Absorption coeficient, controls the color of the hair",
        'type' : 'TEXTURE',
        'default' : (0.2, 0.2, 0.2, 1),
    },
    {
        'attr' : 'r_long_shift',
        'desc' : "Longitudinal shift for the R lobe",
        'type' : 'FLOAT',
        'default' : -10,
    },
    {
        'attr' : 'tt_long_shift',
        'desc' : "Longitudinal shift for the TT lobe",
        'type' : 'FLOAT',
        'default' : 5,
    },
    {
        'attr' : 'trt_long_shift',
        'desc' : "Longitudinal shift for the TRT lobe",
        'type' : 'FLOAT',
        'default' : 15,
    },
    {
        'attr' : 'r_long_width',
        'desc' : "Longitudinal width (stddev.) for the R lobe",
        'type' : 'FLOAT',
        'default' : 5,
    },
    {
        'attr' : 'tt_long_width',
        'desc' : "Longitudinal width (stddev.) for the TT lobe",
        'type' : 'FLOAT',
        'default' : 2.5,
    },
    {
        'attr' : 'trt_long_width',
        'desc' : "Longitudinal width (stddev.) for the TRT lobe",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'glint_scale',
        'desc' : "Glint scale factor 0.5 to 5.0",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'azimuthal_width',
        'desc' : "Azimuthal width of the caustic from 10 to 25 degrees",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'fade_range',
        'desc' : "Fade range for caustic merge (0.2 to 0.4)",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'caustic_limit',
        'desc' : "Caustic intensity limit",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'r_mult',
        'desc' : "Multiplier for the R lobe",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'tt_mult',
        'desc' : "Multiplier for the TT lobe",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'trt_mult',
        'desc' : "Multiplier for the TRT lobe",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'diffuse_mult',
        'desc' : "Multiplier for the Diffuse component",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

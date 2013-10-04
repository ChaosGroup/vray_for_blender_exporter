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


TYPE = 'BRDF'
ID   = 'BRDFGlassGlossy'
NAME = 'BRDFGlassGlossy'
DESC = ""

PluginParams = (
    {
        'attr' : 'color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'color_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'transparency',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'transparency_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ior',
        'desc' : "IOR for the glass; this is ignored if the surface has a volume shader (the volume IOR is used)",
        'type' : 'FLOAT',
        'default' : 1.55,
    },
    {
        'attr' : 'cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'affect_shadows',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_alpha',
        'desc' : "Specifies how render channels are propagated through the glass (0 - only the color channel; 1 - color and alpha; 2 - all channels",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'trace_refractions',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'trace_depth',
        'desc' : "The maximum refraction bounces (-1 is controlled by the global options)",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'exit_color_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reflect_exit_color',
        'desc' : "The color to use when the maximum depth is reached",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'refract_exit_color',
        'desc' : "The color to use when maximum depth is reached when exit_color_on is true",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'volume',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'ior_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'glossiness',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.8,
    },
    {
        'attr' : 'glossiness_tex',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'glossiness_tex_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'dispersion_on',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'dispersion',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'interpolation_on',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'imap_min_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'imap_max_rate',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'imap_color_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'imap_norm_thresh',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.4,
    },
    {
        'attr' : 'imap_samples',
        'desc' : "",
        'type' : 'INT',
        'default' : 20,
    },
)

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
ID   = 'BRDFSampled'
NAME = 'Sampled'
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
        'default' : (0.5, 0.5, 0.5),
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
        'attr' : 'cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'back_side',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'brdf_bitmap',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'brdf_nsamples_d_theta',
        'desc' : "Number of d_theta samples",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'brdf_nsamples_d_phi',
        'desc' : "Number of d_phi samples (1 means isotropic BRDF)",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'brdf_importance_sampling_on',
        'desc' : "true to use importance sampling for the reflections",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'brdf_importance_sampling_resolution',
        'desc' : "Resolution for the resampling of the BRDF used for importance sampling of reflections",
        'type' : 'INT',
        'default' : 32,
    },
    {
        'attr' : 'brdf_importance_sampling_view_terms',
        'desc' : "Number of terms to decompose the view-dependent portion of the resampling matrix",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'brdf_importance_sampling_half_terms',
        'desc' : "Number of terms to decompose the half-angle portion of the resampling matrix",
        'type' : 'INT',
        'default' : 2,
    },
)

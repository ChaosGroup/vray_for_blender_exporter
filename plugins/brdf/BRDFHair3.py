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
ID   = 'BRDFHair3'
NAME = 'Hair3'
DESC = ""

PluginParams = (
    {
        'attr' : 'overall_color',
        'desc' : "Overall color multiplier",
        'type' : 'TEXTURE',
        'default' : (0.9, 0.9, 0.9, 1),
    },
    {
        'attr' : 'transparency',
        'desc' : "Transparency",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'diffuse_color',
        'desc' : "Diffuse hair color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'diffuse_amount',
        'desc' : "Multiplier for the diffuse color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'primary_specular',
        'desc' : "Primary specular color",
        'type' : 'TEXTURE',
        'default' : (0.2, 0.2, 0.2, 1),
    },
    {
        'attr' : 'primary_specular_amount',
        'desc' : "Multiplier for the primary specular color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'primary_glossiness',
        'desc' : "Primary glossiness",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'secondary_specular',
        'desc' : "Secondary specular color",
        'type' : 'TEXTURE',
        'default' : (0.2, 0.2, 0.2, 1),
    },
    {
        'attr' : 'secondary_specular_amount',
        'desc' : "Multiplier for the secondary specular color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'secondary_glossiness',
        'desc' : "Secondary glossiness",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'secondary_lock_to_transmission',
        'desc' : "true to derive the secondary specular color from the transmission color",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'transmission',
        'desc' : "Transmission color",
        'type' : 'TEXTURE',
        'default' : (0.2, 0.2, 0.2, 1),
    },
    {
        'attr' : 'transmission_amount',
        'desc' : "Multiplier for the transmission color",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'transmission_glossiness_length',
        'desc' : "Transmission glossiness along strand length",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'transmission_glossiness_width',
        'desc' : "Transmission glossiness across strand width",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'opaque_for_shadows',
        'desc' : "true to always compute the material as opaque for shadow rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'opaque_for_gi',
        'desc' : "true to always compute the material as opaque for GI rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'simplify_for_gi',
        'desc' : "true to use a simpler and less precise representation of the BRDF for GI rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'use_cached_gi',
        'desc' : "true to use the light cache/irradiance map; false to always use brute force GI for the hair",
        'type' : 'BOOL',
        'default' : True,
    },
)

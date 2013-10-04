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
ID   = 'MtlMulti'
NAME = 'MtlMulti'
DESC = ""

PluginParams = (
    # {
    #     'attr' : 'mtls_list',
    #     'desc' : "A list of the materials",
    #     'type' : 'PLUGIN',
    #     'default' : "",
    # },
    # {
    #     'attr' : 'ids_list',
    #     'desc' : "A list of material IDs",
    #     'type' : 'INT',
    #     'default' : "",
    # },
    {
        'attr' : 'mtlid_gen',
        'desc' : "An integer texture that generates material ids; if not present, neither mtlid_gen_float is present then surface material id will be used",
        'type' : 'INT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'mtlid_gen_float',
        'desc' : "A float texture that generates material ids; if not present, neither mtlid_gen is present then surface material id will be used",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'wrap_id',
        'desc' : "true to wrap the material ID's to the largest specified ID for the material",
        'type' : 'BOOL',
        'default' : False,
    },
)

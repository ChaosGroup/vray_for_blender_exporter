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
ID   = 'BRDFFlakes'
NAME = 'BRDFFlakes'
DESC = ""

PluginParams = (
    {
        'attr' : 'flake_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.3, 0.4, 0.8, 1),
    },
    {
        'attr' : 'flake_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.8,
    },
    {
        'attr' : 'flake_orientation',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.3,
    },
    {
        'attr' : 'flake_density',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_scale',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'flake_size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'flake_map_size',
        'desc' : "The size of the internal flakes map",
        'type' : 'INT',
        'default' : 1024,
    },
    {
        'attr' : 'flake_filtering_mode',
        'desc' : "Flake filtering mode (0 - simple; 1 - directional)",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'flake_seed',
        'desc' : "The random seed for the flakes",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'flake_uvwgen',
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
        'desc' : "The mapping method for the flakes (0 - explicit mapping channel, 1 - triplanar projection in object space)",
        'type' : 'INT',
        'default' : 0,
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
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
)

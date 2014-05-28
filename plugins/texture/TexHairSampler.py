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


TYPE = 'TEXTURE'
ID   = 'TexHairSampler'
NAME = 'Hair Sampler'
DESC = "Hair Sampler"

PluginParams = (
    {
        'attr' : 'distance_along_strand',
        'name' : "Distance",
        'desc' : "Distance along the hair strand where the intersection occurred, in the [0,1] range",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'hair_color',
        'name' : "Color",
        'desc' : "Color from hair primitive (if present)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'hair_incandescence',
        'name' : "Incandescence",
        'desc' : "Incandescence from hair primitive (if present)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'hair_transparency',
        'name' : "Transparency",
        'desc' : "Transparency from hair primitive (if present)",
        'type' : 'OUTPUT_TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr' : 'random_by_strand',
        'name' : "Random Distance",
        'desc' : "Random by the hair strand where the intersection occurred, in the [0,1] range",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
)

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


TYPE = 'MATERIAL'
ID   = 'MtlOverride'
NAME = 'Override'
DESC = "MtlOverride settings"

PluginParams = (
    {
        'attr' : 'base_mtl',
        'name' : 'Base',
        'desc' : "The normal material (visible to the camera)",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'gi_mtl',
        'name' : 'GI',
        'desc' : "The gi material",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'reflect_mtl',
        'name' : 'Reflection',
        'desc' : "The reflection material",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'refract_mtl',
        'name' : 'Refraction',
        'desc' : "The refraction material",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'shadow_mtl',
        'name' : 'Shadow',
        'desc' : "The shadow material",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'environment_override',
        'name' : 'Environment',
        'desc' : "Environment override texture",
        'type' : 'TEXTURE',
        'options' : ['LINKED_ONLY'],
        'default' : (1.0,1.0,1.0),
    },
    {
        'attr' : 'environment_priority',
        'desc' : "Environment override priority (used when several materials override it along a ray path)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'use',
        'name' : "Use",
        'desc' : "Use Override material",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)

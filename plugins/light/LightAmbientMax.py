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


TYPE = 'LIGHT'
ID   = 'LightAmbientMax'
NAME = 'Ambient (3ds max)'
DESC = ""

PluginParams = (
    {
        'attr' : 'enabled',
        'desc' : "true if the light is enabled",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mode',
        'desc' : "light mode",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'gi_min_distance',
        'desc' : "minimal distance for gi rays",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'color',
        'desc' : "The ambient color",
        'type' : 'COLOR',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'compensate_exposure',
        'desc' : "true to compensate for camera exposure",
        'type' : 'BOOL',
        'default' : True,
    },
)

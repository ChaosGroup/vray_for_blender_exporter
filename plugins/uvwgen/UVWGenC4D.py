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


TYPE = 'UVWGEN'
ID   = 'UVWGenC4D'
NAME = 'C4D'
DESC = ""

PluginParams = (
    {
        'attr' : 'uvw_channel',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'len_x',
        'desc' : "X length of the texture",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'len_y',
        'desc' : "Y length of the texture",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'proj_type',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'tex_transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'ox',
        'desc' : "X offset of the texture",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'oy',
        'desc' : "Y offset of the texture",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'texflag',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'repetitionx',
        'desc' : "Repetition x",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'repetitiony',
        'desc' : "Repetition y",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'pixel_aspect',
        'desc' : "Pixel Aspect",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'film_aspect',
        'desc' : "Film Aspect",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

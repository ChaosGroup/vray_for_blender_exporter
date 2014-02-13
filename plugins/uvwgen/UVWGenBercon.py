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
ID   = 'UVWGenBercon'
NAME = 'Bercon'
DESC = ""

PluginParams = (
    {
        'attr' : 'offset_x',
        'desc' : "the X offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'offset_y',
        'desc' : "the Y offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'offset_z',
        'desc' : "the Z offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'size_x',
        'desc' : "X size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'size_y',
        'desc' : "Y size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'size_z',
        'desc' : "Z size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'angle_x',
        'desc' : "X angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'angle_y',
        'desc' : "Y angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'angle_z',
        'desc' : "Z angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'tile_x',
        'desc' : "X tiles",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'tile_y',
        'desc' : "Y tiles",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'tile_z',
        'desc' : "Z tiles",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'offset_x2',
        'desc' : "second X offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'offset_y2',
        'desc' : "second Y offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'offset_z2',
        'desc' : "second Z offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'size_x2',
        'desc' : "second X size",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'size_y2',
        'desc' : "second Y size",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'size_z2',
        'desc' : "second Z size",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'angle_x2',
        'desc' : "second X angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'angle_y2',
        'desc' : "second Y angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'angle_z2',
        'desc' : "second Z angle",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'xyz_lock',
        'desc' : "XYZ Lock",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'seed',
        'desc' : "Seed",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'rand_mat',
        'desc' : "Random by material",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'rand_obj',
        'desc' : "Random by object",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'rand_par',
        'desc' : "Random by particle",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'map',
        'desc' : "Mapping type",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'channel',
        'desc' : "Mapping channel",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'filtering',
        'desc' : "filtering",
        'type' : 'FLOAT',
        'default' : 1,
    },
)

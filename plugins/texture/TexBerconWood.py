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

import TexCommonParams


TYPE = 'TEXTURE'
ID   = 'TexBerconWood'
NAME = 'BerconWood'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'noise_color1',
        'desc' : "noise color 1",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'noise_color2',
        'desc' : "noise color 2",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'noise_color3',
        'desc' : "noise color 3",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'noise_map1',
        'desc' : "noise map 1",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'noise_map2',
        'desc' : "noise map 2",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'noise_map3',
        'desc' : "noise map 3",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'wood_size',
        'desc' : "wood size",
        'type' : 'FLOAT',
        'default' : 3,
    },
    {
        'attr' : 'low_tresh',
        'desc' : "low treshold",
        'type' : 'FLOAT',
        'default' : 0.3,
    },
    {
        'attr' : 'high_tresh',
        'desc' : "high treshold",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'wood_type',
        'desc' : "0:Radial wood, 1:Perlin wood, 2:Simplex wood, 3:Linear wood",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'trunk_str',
        'desc' : "trunk strength",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'trunk_freq',
        'desc' : "trunk frequency",
        'type' : 'FLOAT',
        'default' : 0.04,
    },
    {
        'attr' : 'radial_str',
        'desc' : "radial strength",
        'type' : 'FLOAT',
        'default' : 0.25,
    },
    {
        'attr' : 'radial_freq',
        'desc' : "radial frequency",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'radial_z',
        'desc' : "radial Z frequency",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'angle_str',
        'desc' : "angle strength",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'angle_freq',
        'desc' : "angle frequency",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'angle_rad',
        'desc' : "angle radius",
        'type' : 'FLOAT',
        'default' : 15,
    },
    {
        'attr' : 'grain_str',
        'desc' : "grain strength",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'grain_freq',
        'desc' : "grain frequency",
        'type' : 'FLOAT',
        'default' : 5,
    },
    {
        'attr' : 'grain_lock',
        'desc' : "grain lock",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'width_var',
        'desc' : "width variation",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'gain_var',
        'desc' : "gain variation",
        'type' : 'FLOAT',
        'default' : 0.75,
    },
    {
        'attr' : 'rand_seed',
        'desc' : "random seed",
        'type' : 'FLOAT',
        'default' : 12.345,
    },
    {
        'attr' : 'wood_skew',
        'desc' : "wood skew",
        'type' : 'FLOAT',
        'default' : 0.75,
    },
    {
        'attr' : 'samples',
        'desc' : "samples",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'dist_map',
        'desc' : "distortion map",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'dist_map2',
        'desc' : "distortion map 2",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'dist_str',
        'desc' : "distortion strength",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'use_dist',
        'desc' : "use distortion",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'tex_size',
        'desc' : "texture for the size",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_low',
        'desc' : "texture for low treshhold",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_high',
        'desc' : "texture for high greshhold",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_skew',
        'desc' : "texture for skew",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_width_var',
        'desc' : "texture for width variation",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_gain_var',
        'desc' : "texture for gain variation",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_trunk_str',
        'desc' : "texture for trunk strength",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_trunk_freq',
        'desc' : "texture for trunk frequency",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_radial_str',
        'desc' : "texture for radial strength",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_radial_freq',
        'desc' : "texture for radial frequency",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_z_str',
        'desc' : "texture for radial z strength",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_ang_str',
        'desc' : "texture for angular strength",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_ang_freq',
        'desc' : "texture for angular frequency",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_ang_rad',
        'desc' : "texture for angular radius",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_grain_str',
        'desc' : "texture for grain strength",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'tex_grain_freq',
        'desc' : "texture for grain frequency",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'use_curve_input',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'curve_output',
        'desc' : "Calculated blend amount to be tranformed by the bezier curve!",
        'type' : 'OUTPUT_FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'curve_input',
        'desc' : "If curve is used the output value will be taken from this texture",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
])

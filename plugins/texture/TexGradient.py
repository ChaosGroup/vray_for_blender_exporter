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
ID   = 'TexGradient'
NAME = 'Gradient'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'color1',
        'desc' : "First color",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 1),
    },
    {
        'attr' : 'color2',
        'desc' : "Middle color",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5, 1),
    },
    {
        'attr' : 'color3',
        'desc' : "End color",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'has_textures',
        'desc' : "This affects bump mapping, following a peculiarity in the 3ds Max implementation",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'middle',
        'desc' : "Middle color position",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'type',
        'desc' : "Gradient type (0 - linear, 1 - radial)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'noise_amount',
        'desc' : "Noise amount",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_size',
        'desc' : "Noise size",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'noise_type',
        'desc' : "Noise type (0 - regular, 1 - fractal, 2 - turbulence)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'noise_iterations',
        'desc' : "Noise iterations",
        'type' : 'FLOAT',
        'default' : 4,
    },
    {
        'attr' : 'noise_phase',
        'desc' : "Noise phase",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_low',
        'desc' : "Noise low threshold",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_high',
        'desc' : "Noise high threshold",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'noise_smooth',
        'desc' : "Threshold smoothing",
        'type' : 'FLOAT',
        'default' : 0,
    },
])

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
ID   = 'TexGradRamp'
NAME = 'GradRamp'
DESC = ""

PluginParams = list(TexCommonParams.PluginTextureCommonParams)

PluginParams.extend([
    {
        'attr' : 'positions',
        'desc' : "positions of the given colors",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    # {
    #     'attr' : 'colors',
    #     'desc' : "the given colors",
    #     'type' : 'TEXTURE',
    #     'default' : "",
    # },
    {
        'attr' : 'texture_map',
        'desc' : "the texture used for mapped gradient ramp",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0, 1.0),
    },
    {
        'attr' : 'gradient_type',
        'desc' : "0:four corner, 1:box, 2:diagonal, 3:lighting, 4:linear, 5:mapped, 6:normal, 7:pong, 8:radial, 9:spiral, 10:sweep, 11:tartan",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'interpolation',
        'desc' : "0:none, 1:linear, 2:expUp, 3:expDown, 4:smooth, 5:bump, 6:spike",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'noise_amount',
        'desc' : "Distortion noise amount",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_type',
        'desc' : "0:regular, 1:fractal, 2:turbulence",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'noise_size',
        'desc' : "default = 1.0",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'noise_phase',
        'desc' : "default = 0.0",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_levels',
        'desc' : "default = 4.0",
        'type' : 'FLOAT',
        'default' : 4,
    },
    {
        'attr' : 'noise_treshold_low',
        'desc' : "default = 0.0f",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_treshold_high',
        'desc' : "default = 1.0f",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'noise_smooth',
        'desc' : "default = 0.0f",
        'type' : 'FLOAT',
        'default' : 0,
    },
])

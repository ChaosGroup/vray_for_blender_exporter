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

from vb25.lib        import ExportUtils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'BRDF'
ID   = 'BRDFDiffuse'
NAME = 'Diffuse'
DESC = ""

PluginParams = (
    # {
    #     'attr' : 'color',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (1, 1, 1),
    # },
    {
        'attr' : 'color_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'color_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },

    # {
    #     'attr' : 'transparency',
    #     'desc' : "",
    #     'type' : 'COLOR',
    #     'default' : (0, 0, 0),
    # },
    {
        'attr' : 'transparency_tex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },
    # {
    #     'attr' : 'transparency_tex_mult',
    #     'desc' : "",
    #     'type' : 'FLOAT',
    #     'default' : 1,
    # },

    {
        'attr' : 'roughness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1.0,
    },
    {
        'attr' : 'use_irradiance_map',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
)


# def writeDatablock(bus, pluginName, PluginParams, BRDFDiffuse, mappedParams):
#     ExportUtils.WriteFile(bus, 'nodetree', "\n%s %s {" % (ID, pluginName))
#     ExportUtils.WriteFile(bus, 'nodetree', "\n\tcolor=Color(0.0,0.0,0.0);")
#     ExportUtils.WriteFile(bus, 'nodetree', "\n\tcolor_tex_mult=1.0;")
#     ExportUtils.WriteFile(bus, 'nodetree', "\n\ttransparency=Color(0.0,0.0,0.0);")
#     ExportUtils.WriteFile(bus, 'nodetree', "\n\ttransparency_tex_mult=1.0;")

#     ExportUtils.WritePluginParams(bus, bus['files']['nodetree'], ID, pluginName, BRDFDiffuse, mappedParams, PluginParams)

#     ExportUtils.WriteFile(bus, 'nodetree', "\n}\n")

#     return pluginName

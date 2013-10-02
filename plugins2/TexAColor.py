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
from bpy.props import *

from vb25.lib   import ExportUtils
from vb25.lib   import AttributeUtils
from vb25.ui.ui import *


TYPE = 'TEXTURE'
ID   = 'TexAColor'
PLUG = 'TexAColor'
PID  =  100

NAME = 'Color'
DESC = "Just a color"

PluginParams = (
    {
        'attr'    : 'texture',
        'name'    : "Color",
        'desc'    : "Color",
        'type'    : 'TEXTURE',
        'default' :  (1,1,1,1),
    },
)


def add_properties(rna_pointer):
    class TexAColor(bpy.types.PropertyGroup):
        pass
    bpy.utils.register_class(TexAColor)

    for param in PluginParams:
        AttributeUtils.GenerateAttribute(TexAColor, param)

    rna_pointer.TexAColor = PointerProperty(
        name        = "TexAColor",
        type        =  TexAColor,
        description = "V-Ray TexAColor settings"
    )


def writeDatablock(bus, TexAColor, pluginName, mappedParams):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ofile.write("\nTexAColor %s {" % pluginName)
    ExportUtils.WritePluginParams(bus, ofile, TexAColor, mappedParams, PluginParams)
    ofile.write("\n}\n")

    return pluginName


def gui(context, layout, TexAColor):
    layout.prop(TexAColor, 'texture', text="Color")

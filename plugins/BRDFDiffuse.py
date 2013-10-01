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

from vb25.ui.ui import *
from vb25.lib   import ExportUtils
from vb25.lib   import AttributeUtils


TYPE = 'BRDF'
ID   = 'BRDFDiffuse'
PID  =  5

NAME = 'Diffuse'
DESC = "BRDFDiffuse."

# For node sockets generation
#
MAPPED_PARAMS = {
    'color_tex'        : 'TEXTURE',
    'transparency_tex' : 'FLOAT_TEXTURE',
    'roughness'        : 'FLOAT_TEXTURE',
}

PluginParams = (
    {
        'attr'    : 'color_tex',
        'name'    : "Color",
        'desc'    : "Diffuse color",
        'type'    : 'TEXTURE',
        'default' : (1.0, 1.0, 1.0),
    },
    {
        'attr'    : 'transparency_tex',
        'name'    : "Transparency",
        'desc'    : "Transparency of the BRDF",
        'type'    : 'FLOAT_TEXTURE',
        'default' :  0.0,
    },
    {
        'attr'    : 'roughness',
        'name'    : "Roughness",
        'desc'    : "Roughness",
        'type'    : 'FLOAT_TEXTURE',
        'default' :  0.0,
        'ui' : {
            'min' : 0.0,
            'max' : 1.0,
        }
    },
    {
        'attr'    : 'use_irradiance_map',
        'name'    : "Use Irradiance Map",
        'desc'    : "Use Irradiance Map, use Brute Force otherwise",
        'type'    : 'BOOL',
        'default' :  True,  
    }
)


def add_properties(rna_pointer):
    class BRDFDiffuse(bpy.types.PropertyGroup):
        pass
    bpy.utils.register_class(BRDFDiffuse)

    for param in PluginParams:
        AttributeUtils.GenerateAttribute(BRDFDiffuse, param)

    rna_pointer.BRDFDiffuse = PointerProperty(
        name        = "BRDFDiffuse",
        type        =  BRDFDiffuse,
        description = "V-Ray BRDFDiffuse settings"
    )


def writeDatablock(bus, BRDFDiffuse, pluginName, mappedParams):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ofile.write("\nBRDFDiffuse %s {" % pluginName)

    # Treat some params in a special way
    #
    ofile.write("\n\tcolor=Color(0.0,0.0,0.0);")
    ofile.write("\n\tcolor_tex_mult=1.0;")
    ofile.write("\n\ttransparency=Color(0.0,0.0,0.0);")
    ofile.write("\n\ttransparency_tex_mult=1.0;")

    # Export all the rest in an automated manner
    #
    ExportUtils.WritePluginParams(bus, ofile, BRDFDiffuse, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName


def write(bus, baseName=None):
    print("This shouldn't happen!")


def gui(context, layout, BRDFDiffuse):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    split = layout.split()
    col = split.column(align=True)
    col.prop(BRDFDiffuse, 'color_tex', text="")
    if wide_ui:
        col = split.column(align=True)
    col.prop(BRDFDiffuse, 'transparency_tex')

    layout.separator()

    split = layout.split()
    col = split.column()
    sub = col.column(align=True)
    sub.prop(BRDFDiffuse, 'roughness')
    if wide_ui:
        col= split.column()
    col.prop(BRDFDiffuse, 'use_irradiance_map')

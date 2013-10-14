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

from vb25.lib import ExportUtils


TYPE = 'MATERIAL'
PLUG = 'Mtl2Sided'
ID   =  PLUG
NAME = 'Two Sided'
DESC = "Mtl2Sided settings"


PluginParams = (
    {
        'attr' : 'front',
        'desc' : "The material for the surface on the same side as the normal",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'back',
        'desc' : "The material for the side that is opposite the surface normal",
        'type' : 'MATERIAL',
        'default' : "",
    },
    {
        'attr' : 'translucency_tex',
        'name' : "Translucency",
        'desc' : "Translucency texture",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'force_1sided',
        'name' : "Force Single Sided",
        'desc' : "True to make the sub-materials one-sided",
        'type' : 'BOOL',
        'default' : True,
    },

    # TODO: channel selection node
    # {
    #   'attr' : 'channels',
    #   'desc' : "Render channels the result of this BRDF will be written to",
    #   'type' : 'STRING',
    #   'default' : "",
    # },
    
    {
        'attr' : 'use',
        'name' : "Use",
        'desc' : "Use Two Sided material",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False,
    },
)


def nodeDraw(context, layout, Mtl2Sided):
    layout.prop(Mtl2Sided, 'force_1sided')


def writeDatablock(bus, pluginName, PluginParams, Mtl2Sided, mappedParams):
    ofile = bus['files']['materials']
    scene = bus['scene']

    ofile.write("\nMtl2Sided %s {" % pluginName)
    ofile.write("\n\ttranslucency=Color(0.0,0.0,0.0);")
    ofile.write("\n\ttranslucency_tex_mult=1.0;")

    ExportUtils.WritePluginParams(bus, ofile, Mtl2Sided, mappedParams, PluginParams)

    ofile.write("\n}\n")

    return pluginName

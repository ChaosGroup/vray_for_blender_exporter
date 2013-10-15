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

from vb25.lib import utils


TYPE = 'TEXTURE'
ID   = 'TexMeshVertexColorChannel'
NAME = 'Mesh Vertex Channel'
DESC = ""

PluginParams = (
    {
        'attr' : 'channelIndex',
        'name' : "Channel Index",
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'channel_name',
        'desc' : "Name of the channel to use",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'default_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.0, 0.0, 0.0),
    },

    {
        'attr' : 'data_select',
        'desc' : "Use UV",
        'type' : 'ENUM',
        'items' : (
            ('0', "UV", "Use UV channels"),
            ('1', "Color", "Use Color channels"),
        ),
        'skip' : True,
        'default' : '1',
    },
)


def nodeDraw(context, layout, TexMeshVertexColorChannel):
    ob = context.object

    layout.prop(TexMeshVertexColorChannel, 'channelIndex')

    layout.prop(TexMeshVertexColorChannel, 'data_select', expand=True)

    if TexMeshVertexColorChannel.data_select == '0':
        layout.prop_search(TexMeshVertexColorChannel, 'channel_name',
                           ob.data, 'uv_textures',
                           text="")
    else:
        layout.prop_search(TexMeshVertexColorChannel, 'channel_name',
                           ob.data, 'vertex_colors',
                           text="")


# def writeDatablock(bus, pluginName, PluginParams, TexMeshVertexColorChannel, mappedParams):
#     ofile = bus['files']['nodetree']
#     scene = bus['scene']

#     ofile.write("\n%s %s {" % (ID, pluginName))

#     if TexMeshVertexColorChannel.channel_name:
#         ofile.write('\n\tchannel_name="%s";' % TexMeshVertexColorChannel.channel_name)
#     else:
#         ofile.write("\n\tchannelIndex=%i;" % TexMeshVertexColorChannel.channelIndex)
#     ofile.write("\n\tdefault_color=Color(%.3f,%.3f,%.3f);" % TexMeshVertexColorChannel.default_color)
#     ofile.write("\n}\n")

#     return pluginName

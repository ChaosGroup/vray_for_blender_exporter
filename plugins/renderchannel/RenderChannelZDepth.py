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

TYPE = 'RENDERCHANNEL'
ID   = 'RenderChannelZDepth'
NAME = 'Z-Depth'
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "Channel name",
        'type' : 'STRING',
        'default' : NAME,
    },
    {
        'attr' : 'depth_from_camera',
        'desc' : "From camera",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'depth_clamp',
        'desc' : "Clamp",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'filtering',
        'desc' : "Filtering",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'depth_black',
        'desc' : "Black distance",
        'type' : 'FLOAT',
        'default' : 0.0,
    },
    {
        'attr' : 'depth_white',
        'desc' : "White distance",
        'type' : 'FLOAT',
        'default' : 1000.0,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')

    split = layout.split()
    col = split.column(align=True)
    col.prop(propGroup, 'depth_black', text="Black Distance")
    col.prop(propGroup, 'depth_white', text="White Distance")

    split = layout.split()
    col = split.column()
    col.prop(propGroup, 'depth_from_camera')
    col.prop(propGroup, 'depth_clamp')
    col.prop(propGroup, 'filtering')

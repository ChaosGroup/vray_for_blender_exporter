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
ID   = 'RenderChannelMultiMatte'
NAME = 'MultiMatte'
DESC = "MultiMatte"

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "",
        'type' : 'STRING',
        'default' : NAME,
    },
    {
        'attr' : 'red_id',
        'desc' : "The object ID that will be written as the red channel (0 to disable the red channel)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'green_id',
        'desc' : "The object ID that will be written as the green channel (0 to disable the green channel)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'blue_id',
        'desc' : "The object ID that will be written as the blue channel (0 to disable the blue channel)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'use_mtl_id',
        'desc' : "Use the material IDs instead of the object IDs",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_matte_objects',
        'desc' : "Don't affect Matte Objects",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'consider_for_aa',
        'desc' : "Consider this render element for antialiasing (may slow down rendering)",
        'type' : 'BOOL',
        'default' : False,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')
    
    layout.prop(propGroup, 'red_id')
    layout.prop(propGroup, 'green_id')
    layout.prop(propGroup, 'blue_id')
    layout.prop(propGroup, 'use_mtl_id')
    layout.prop(propGroup, 'affect_matte_objects')

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

TYPE = 'RENDERCHANNEL'
ID   = 'RenderChannelObjectSelect'
NAME = "Object Select"
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "",
        'type' : 'STRING',
        'default' : NAME,
    },
    {
        'attr' : 'id',
        'desc' : "The object/material ID that will be extracted",
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
        'desc' : "AA",
        'type' : 'BOOL',
        'default' : False,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')

    layout.prop(propGroup, 'use_mtl_id')
    
    text = "Material ID" if propGroup.use_mtl_id else"Object ID"
    layout.prop(propGroup, 'id', text=text)

    layout.prop(propGroup, 'affect_matte_objects')
    layout.prop(propGroup, 'consider_for_aa')

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
ID   = 'RenderChannelVelocity'
NAME = 'Velocity'
DESC = ""

PluginParams = (
    {
        'attr' : 'name',
        'desc' : "",
        'type' : 'STRING',
        'default' : "Velocity",
    },
    {
        'attr' : 'clamp_velocity',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'max_velocity',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'max_velocity_last_frame',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ignore_z',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'filtering',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
)


def nodeDraw(context, layout, propGroup):
    layout.prop(propGroup, 'name')
    
    layout.prop(propGroup, 'max_velocity')
    layout.prop(propGroup, 'max_velocity_last_frame', text="Max. Last")
    layout.prop(propGroup, 'clamp_velocity')
    layout.prop(propGroup, 'ignore_z')
    layout.prop(propGroup, 'filtering')

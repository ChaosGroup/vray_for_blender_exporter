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
PLUG = 'MtlSingleBRDF'
ID   =  PLUG
NAME = 'Single'
DESC = "MtlSingleBRDF settings"

PluginParams = (
    {
        'attr' : 'filter',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'brdf',
        'name' : "BRDF",
        'desc' : "",
        'type' : 'BRDF',
        'default' : "",
    },
    {
        'attr' : 'double_sided',
        'desc' : "1 to make the material double-sided",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'allow_negative_colors',
        'desc' : "true to allow negative color components; otherwise they will be clamped to 0",
        'type' : 'BOOL',
        'default' : False,
    },
)


def nodeDraw(context, layout, MtlSingleBRDF):
    layout.prop(MtlSingleBRDF, 'double_sided')
    layout.prop(MtlSingleBRDF, 'allow_negative_colors')

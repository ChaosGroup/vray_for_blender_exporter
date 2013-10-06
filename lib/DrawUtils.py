#
# V-Ray/Blender
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

from . import AttributeUtils

from pynodes_framework import idref


def Draw(context, layout, dataPointer, PluginParams):
    for attrDesc in PluginParams:
        if attrDesc['type'] in AttributeUtils.SkippedTypes:
            continue
        if attrDesc['type'] in AttributeUtils.OutputTypes:
            continue
        if attrDesc['type'] in AttributeUtils.InputTypes:
            continue

        if attrDesc['type'] in {'IMAGE'}:
            if 0:
                idref.draw_idref(layout, dataPointer, attrDesc['attr'])
        else:
            layout.prop(dataPointer, attrDesc['attr'])

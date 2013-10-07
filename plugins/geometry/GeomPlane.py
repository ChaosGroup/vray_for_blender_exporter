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


TYPE = 'GEOMETRY'
ID   = 'GeomPlane'
NAME = 'Infinite Plane'
DESC = "Procedural infinite plane"

PluginParams = ()


def writeDatablock(bus, pluginName, PluginParams, GeomDisplacedMesh, mappedParams):
    ofile = bus['files']['nodes']

    ofile.write("\nGeomPlane %s {}\n" % (ID, pluginName))

    return pluginName

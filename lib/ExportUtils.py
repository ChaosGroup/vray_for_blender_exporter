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

from . import utils


def WriteParamsBlock(bus, ofile, dataPointer, mappedParams, DEF_PARAMS, DEF_MAPPED_PARAMS):
    scene = bus['scene']

    for param in DEF_PARAMS:
        value = getattr(dataPointer, param)

        if param in DEF_MAPPED_PARAMS:
            if param in mappedParams:
                value = mappedParams[param]

            if DEF_MAPPED_PARAMS[param] == 'FLOAT_TEXTURE':
                if type(value) is str:
                    value = "%s::out_intensity" % value

        ofile.write("\n\t%s=%s;" % (param, utils.AnimatedValue(scene, value)))


def WritePluginParams(bus, ofile, dataPointer, mappedParams, PluginParams):
    scene = bus['scene']
    
    for attrDesc in PluginParams:
        value = None
        attr  = attrDesc['attr']

        if attr in mappedParams:
            value = mappedParams[attr]

            if attrDesc['type'] == 'FLOAT_TEXTURE':
                if type(value) is str:
                    value = "%s::out_intensity" % value
        else:
            value = getattr(dataPointer, attr)
        
        if value is not None:
            ofile.write("\n\t%s=%s;" % (attr, utils.AnimatedValue(scene, value)))

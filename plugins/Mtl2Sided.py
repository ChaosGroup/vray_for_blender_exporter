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

from bpy.props import *


TYPE = 'MATERIAL'
ID   = 'Mtl2Sided'

NAME = 'Mtl2Sided'
UI   = "Two-sided"
DESC = "Mtl2Sided settings."

PARAMS = (
)

MAPPED_PARAMS = {
	'front' : 'MATERIAL',
	'back'  : 'MATERIAL',

	'translucency'     : 'COLOR',
	'translucency_tex' : 'TEXTURE',
}


def add_properties(rna_pointer):
	class Mtl2Sided(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(Mtl2Sided)

	rna_pointer.Mtl2Sided= PointerProperty(
		name = "Mtl2Sided",
		type = Mtl2Sided,
		description = "V-Ray Mtl2Sided settings"
	)

	Mtl2Sided.use = BoolProperty(
		name = "Two sided material",
		description = "Simple \"Two sided\" material. Use nodes for advanced control",
		default = False
	)

	Mtl2Sided.front= StringProperty(
		name = "Front Material",
		description = "The material for the surface on the same side as the normal",
		default = ""
	)

	Mtl2Sided.back = StringProperty(
		name = "Back Material",
		description = "The material for the side that is opposite the surface normal. Same as \"Front Material\" if nothing is set",
		default = ""
	)

	Mtl2Sided.translucency_tex= StringProperty(
		name = "Translucency Texture",
		description = "Translucency texture",
		default = ""
	)

	Mtl2Sided.control= EnumProperty(
		name        = "Control",
		description = "Translucency type",
		items = (
			('SLIDER',  "Slider",  "."),
			('COLOR',   "Color",   "."),
			('TEXTURE', "Texture", ".")
		),
		default = 'SLIDER'
	)

	Mtl2Sided.translucency_tex_mult= FloatProperty(
		name = "Translucency texture multiplier",
		description = "Translucency texture multiplier",
		min = 0.0,
		max = 1.0,
		soft_min = 0.0,
		soft_max = 1.0,
		precision = 3,
		default = 1.0
	)

	Mtl2Sided.translucency_color= FloatVectorProperty(
		name = "Translucency color",
		description = "Translucency between front and back",
		subtype = 'COLOR',
		min = 0.0,
		max = 1.0,
		soft_min = 0.0,
		soft_max = 1.0,
		default = (0.5,0.5,0.5)
	)

	Mtl2Sided.translucency_slider= FloatProperty(
		name = "Translucency",
		description = "Translucency between front and back",
		min = 0.0,
		max = 1.0,
		soft_min = 0.0,
		soft_max = 1.0,
		precision = 3,
		default = 0.5
	)

	Mtl2Sided.force_1sided= BoolProperty(
		name = "Force one-sided",
		description = "Make the sub-materials one-sided",
		default = True
	)


def writeDatablock(bus, Mtl2Sided, pluginName, mappedParams):
	ofile = bus['files']['materials']

	ofile.write("\nMtl2Sided %s {" % pluginName)
	ofile.write("\n\tfront=%s;" % mappedParams['front'])

	back = mappedParams['back']
	if back == 'MANOMATERIALISSET':
		back = mappedParams['front']	
	ofile.write("\n\tback=%s;" % back)

	ofile.write("\n\tforce_1sided=%i;" % Mtl2Sided.force_1sided)
	ofile.write("\n}\n")

	return pluginName

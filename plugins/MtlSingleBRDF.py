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


TYPE = 'MATERIAL'
ID   = 'MtlSingleBRDF'

NAME = 'Single BRDF'
DESC = "MtlSingleBRDF settings."

PARAMS = ()

MAPPED_PARAMS = {
	'brdf' : 'BRDF',
}


def add_properties(rna_pointer):
	class MtlSingleBRDF(bpy.types.PropertyGroup):
		brdf = bpy.props.StringProperty(
			name        = "BRDF",
			description = "BRDF",
			default     = ""
		)

		double_sided = bpy.props.BoolProperty(
			name        = "Double sided",
			description = "Make the material double-sided",
			default     = True
		)

		allow_negative_colors = bpy.props.BoolProperty(
			name        = "Allow negative colors",
			description = "If false negative colors will be clamped",
			default     = True
		)

	bpy.utils.register_class(MtlSingleBRDF)

	rna_pointer.MtlSingleBRDF = bpy.props.PointerProperty(
		name        = "MtlSingleBRDF",
		type        =  MtlSingleBRDF,
		description = "V-Ray MtlSingleBRDF settings"
	)


def gui(context, layout, MtlSingleBRDF):
	split = layout.split()
	col = split.column()
	col.prop(MtlSingleBRDF, 'double_sided')
	col.prop(MtlSingleBRDF, 'allow_negative_colors')


def writeDatablock(bus, MtlSingleBRDF, pluginName, mappedParams):
	ofile = bus['files']['materials']

	ofile.write("\nMtlSingleBRDF %s {" % pluginName)
	ofile.write("\n\tbrdf=%s;" % mappedParams['brdf'])
	ofile.write("\n\tdouble_sided=%i;" % MtlSingleBRDF.double_sided)
	ofile.write("\n\tallow_negative_colors=%i;" % MtlSingleBRDF.allow_negative_colors)
	ofile.write("\n}\n")

	return pluginName

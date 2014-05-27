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

import bpy

from vb30.lib import ExportUtils


TYPE = 'SETTINGS'
ID   = 'SettingsDMCSampler'
NAME = 'DMC Sampler'
DESC = ""

PluginParams = (
    {
        'attr' : 'time_dependent',
        'desc' : "This make the samping pattern change with time",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'adaptive_amount',
        'desc' : "A value of 1.0 means full adaptation; a value of 0.0 means no adaptation",
        'type' : 'FLOAT',
        'default' : 0.85,
    },
    {
        'attr' : 'adaptive_threshold',
        'desc' : "Controls V-Ray's judgement of when a blurry value is \"good enough\" to be used",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'adaptive_min_samples',
        'desc' : "The minimum number of samples that must be made before the early termination algorithm is used",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'subdivs_mult',
        'desc' : "This will multiply all subdivs values everywhere during rendering",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'path_sampler_type',
        'desc' : "",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'div_shade_subdivs',
        'name' : "Divide Shading Subdivs",
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

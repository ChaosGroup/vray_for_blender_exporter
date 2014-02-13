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

TYPE = 'SETTINGS'
ID   = 'SettingsDefaultDisplacement'
NAME = 'Default Displacement'
DESC = ""

PluginParams = (
    {
        'attr' : 'override_on',
        'desc' : "Override settings globally",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'edgeLength',
        'desc' : "Max. height",
        'type' : 'FLOAT',
        'default' : 4,
    },
    {
        'attr' : 'viewDependent',
        'desc' : "Determines if view-dependent tesselation is used",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'maxSubdivs',
        'desc' : "Determines the maximum subdivisions for a triangle of the original mesh",
        'type' : 'INT',
        'default' : 256,
    },
    {
        'attr' : 'tightBounds',
        'desc' : "When this is on, initialization will be slower, but tighter bounds will be computed for the displaced triangles making rendering faster",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'amount',
        'desc' : "Determines the displacement amount for white areas in the displacement map",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'relative',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

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

TYPE = 'CAMERA'
ID   = 'SettingsCameraDof'
NAME = 'SettingsCameraDof'
DESC = ""

PluginParams = (
    {
        'attr' : 'on',
        'name' : "Use Depth Of Field",
        'desc' : "Use depth of field",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'aperture',
        'desc' : "The size of the virtual camera aperture, in world units",
        'type' : 'FLOAT',
        'default' : 5,
    },
    {
        'attr' : 'center_bias',
        'desc' : "This determines the uniformity of the DOF effect",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'focal_dist',
        'desc' : "Determines the distance from the camera at which objects will be in perfect focus",
        'type' : 'FLOAT',
        'default' : 200,
    },
    {
        'attr' : 'sides_on',
        'desc' : "This option allows you to simulate the polygonal shape of the aperture of real-world cameras",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'sides_num',
        'desc' : "Number of sides",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'rotation',
        'desc' : "Specifies the orientation of the aperture shape",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'anisotropy',
        'desc' : "This allows the stretching of the bokeh effect horizontally or vertically",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'subdivs',
        'desc' : "Controls the quality of the DOF effect",
        'type' : 'INT',
        'default' : 8,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

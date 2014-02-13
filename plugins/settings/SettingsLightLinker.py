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
ID   = 'SettingsLightLinker'
NAME = 'Settings Light Linker'
DESC = ""

PluginParams = (
    {
        'attr' : 'ignored_lights',
        'desc' : "List containing lists of plugins. Every sub list contains a light plugin (always the first element) and some node plugins the light is not illuminating",
        'type' : 'LIST',
        'default' : "",
    },
    {
        'attr' : 'ignored_shadow_lights',
        'desc' : "List containing list of plugins. Every sub list contains a light plugin (always the first element) and some node plugins, which do not cast shadows from this light",
        'type' : 'LIST',
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

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
ID   = 'SettingsRaycaster'
NAME = 'Raycaster'
DESC = "Raycaster options"

PluginParams = (
    {
        'attr' : 'maxLevels',
        'desc' : "Max. tree depth",
        'type' : 'INT',
        'default' : 60,
    },
    {
        'attr' : 'minLeafSize',
        'desc' : "Min. voxel size",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'faceLevelCoef',
        'desc' : "Balance coefficient between depth and faces per voxel",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'dynMemLimit',
        'desc' : "Limit for dynamic geometry, in megabytes",
        'type' : 'INT',
        'default' : 4000,
    },
    {
        'attr' : 'embreeUse',
        'desc' : "Enable/Disable using the embree ray caster",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'embreeUseMB',
        'desc' : "Enable/disable using the embree ray caster for motion blur",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'embreeHair',
        'desc' : "Enable/disable the Embree ray caster for hair",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'embreeLowMemory',
        'desc' : "Try to conserve memory, using potentially slower algorithms",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'embreeRayPackets',
        'desc' : "Turn on the packet ray casting",
        'type' : 'BOOL',
        'default' : False,
    },
)

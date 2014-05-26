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
ID   = 'SettingsMotionBlur'
NAME = 'Motion Blur'
DESC = ""

PluginParams = (
    {
        'attr' : 'on',
        'name' : "Use Motion Blur",
        'desc' : "Use motion blur",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'geom_samples',
        'desc' : "This determines the number of geometry segments used to approximate motion blur",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'low_samples',
        'desc' : "This controls how many samples in time will be computed during irradiance map calculations",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'duration',
        'desc' : "Specifies the duration, in frames, during which the camera shutter is open",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'subdivs',
        'desc' : "Determines the quality of the motion blur",
        'type' : 'INT',
        'default' : 6,
    },
    {
        'attr' : 'bias',
        'desc' : "This controls the bias of the motion blur effect",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'shutter_efficiency',
        'desc' : "Shutter efficiency",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'interval_center',
        'desc' : "Specifies the middle of the motion blur interval with respect to the frame",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'camera_motion_blur',
        'desc' : "Use camera motion blur",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

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
ID   = 'SphericalHarmonicsRenderer'
NAME = 'Spherical Harmonics Renderer'
DESC = "Spherical harmonics renderer settings"

PluginParams = (
    {
        'attr' : 'file_name',
        'desc' : "This is the name of the *.vrsh file which contains the precomputed SH for this scene",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/spherical_harmonics.vrsh",
    },
    {
        'attr' : 'use_single_vrsh',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'precalc_light_per_frame',
        'desc' : "Reasonable when rendering animations. Depending on this option V-Ray calculates the lighting either once at the beginning of the rendering or precalculates it before every frame",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'sample_environment',
        'desc' : "Turns on the environment sampling to add environment light contribution",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'is_hemispherical',
        'name' : "Upper hemisphere only",
        'desc' : "Depending on this option V-Ray samples either the whole sphere or only the upper hemisphere of the environment",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'subdivs',
        'desc' : "The square of this parameter is proportional to the number of rays, sampled in the environment",
        'type' : 'INT',
        'ui' : {
            'min' : 1,
        },
        'default' : 30,
    },
    {
        'attr' : 'apply_filtering',
        'desc' : "Turns on the filtering of the spherical harmonics. This is useful to reduce the ringing artifacts (known as Gibbs phenomena in signal processing) by suppressing the high frequencies. This produces blurred SH which result in a smoother image",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'filter_strength',
        'desc' : "The strength of high frequencies' suppression. Values near 0.0 slightly change the image while values near 1.0 smooth it a lot",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 0.0,
            'max' : 1.0,
        },
        'default' : 0.5,
    },
)

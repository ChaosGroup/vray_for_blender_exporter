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

TYPE = 'SETTINGS'
ID   = 'SettingsGI'
NAME = 'Global Illumination'
DESC = "Global illumination settings"

PluginParams = (
    {
        'attr' : 'on',
        'desc' : "Enable Global Illumination",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'refract_caustics',
        'desc' : "This allows indirect lighting to pass through transparent objects (glass etc)",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'reflect_caustics',
        'desc' : "This allows indirect light to be reflected from specular objects (mirrors etc)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'saturation',
        'desc' : "Controls the saturation of the GI",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'contrast',
        'desc' : "This parameter determines the base for the contrast boost",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'contrast_base',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'primary_engine',
        'desc' : "Primary diffuse bounces engines",
        'type' : 'ENUM',
        'items' : (
            ('0', "Irradiance Map", ""),
            ('2', "Brute Force", ""),
            ('3', "Light Cache", ""),
            ('4', "Spherical Harmonics", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'primary_multiplier',
        'desc' : "This value determines how much primary diffuse bounces contribute to the final image illumination",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 0.0,
        },
        'default' : 1,
    },
    {
        'attr' : 'secondary_engine',
        'desc' : "Secondary diffuse bounces engines",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('2', "Brute Force", ""),
            ('3', "Light Cache", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'secondary_multiplier',
        'desc' : "This determines the effect of secondary diffuse bounces on the scene illumination",
        'type' : 'FLOAT',
        'ui' : {
            'min' : 0.0,
        },
        'default' : 1,
    },
    {
        'attr' : 'ray_distance_on',
        'name' : "Limit Ray Distance",
        'desc' : "Limit ray distance",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ray_distance',
        'desc' : "Maximum ray distance",
        'type' : 'FLOAT',
        'default' : 100000,
    },
    {
        'attr' : 'ao_on',
        'name' : "Use Ambient Occlusion",
        'desc' : "Use ambient occlusion",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ao_amount',
        'name' : "AO Amount",
        'desc' : "Ambient occlusion amount",
        'type' : 'FLOAT',
        'default' : 0.8,
    },
    {
        'attr' : 'ao_radius',
        'name' : 'AO Radius',
        'desc' : "Ambient occlusion radius",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'ao_subdivs',
        'name' : 'AO Subdivs',
        'desc' : "Ambient occlusion subdivs",
        'type' : 'INT',
        'default' : 8,
    },

    {
        'attr' : 'spherical_harmonics',
        'name' : 'Spherical Harmonics Mode',
        'desc' : "Bake or render spherical harmonics",
        'type' : 'ENUM',
        'items' : (
            ('BAKE',   "Bake",   ""),
            ('RENDER', "Render", ""),
        ),
        'skip' : True,
        'default' : 'BAKE',
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

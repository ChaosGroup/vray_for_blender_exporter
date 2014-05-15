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

TYPE = 'BRDF'
ID   = 'BRDFSkinComplex'
NAME = 'Skin'
DESC = "Skin shader"

PluginParams = (
    {
        'attr' : 'scale',
        'desc' : "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smaller",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'max_sss_amount',
        'desc' : "The maximum summed weight of the SSS components",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'max_reflection_amount',
        'desc' : "The maximum summed weight of the reflection components",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'opacity',
        'desc' : "Opacity",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'diffuse_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5, 1),
    },
    {
        'attr' : 'diffuse_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'shallow_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.776471, 0.603922, 0.545098, 1),
    },
    {
        'attr' : 'shallow_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'shallow_radius',
        'desc' : "The radius for shallow scattering, in cm",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.1,
    },
    {
        'attr' : 'medium_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.682353, 0.407843, 0.133333, 1),
    },
    {
        'attr' : 'medium_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'medium_radius',
        'desc' : "The radius for medium scattering, in cm",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.5,
    },
    {
        'attr' : 'deep_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.929412, 0.0784314, 0.0392157, 1),
    },
    {
        'attr' : 'deep_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'deep_radius',
        'desc' : "The radius for deep scattering, in cm",
        'type' : 'FLOAT_TEXTURE',
        'default' : 2,
    },
    {
        'attr' : 'primary_reflecton_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'primary_reflection_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'primary_reflection_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.6,
    },
    {
        'attr' : 'primary_reflection_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'primary_reflection_fresnel',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'primary_reflection_fresnel_ior',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.33,
    },
    {
        'attr' : 'secondary_reflecton_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1, 1),
    },
    {
        'attr' : 'secondary_reflection_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'secondary_reflection_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.6,
    },
    {
        'attr' : 'secondary_reflection_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'secondary_reflection_fresnel',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'secondary_reflection_fresnel_ior',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.33,
    },
    {
        'attr' : 'multiple_scattering',
        'desc' : "The algorithm used to compute multiple scattering: 0 - pre-pass based illumination map; 1 - object space illumination map; 2 - raytraced",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'scatter_gi',
        'desc' : "true to enable scattering of GI rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'raytraced_scatter_textures',
        'desc' : "true to scatter SSS textures when using raytraced scattering",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'raytraced_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'prepass_rate',
        'desc' : "Sampling density for the illumination map",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'prepass_id',
        'desc' : "0 to calculate a separate illuminataion map for this shader; otherwise all shaders with the same prepass ID will share the same illumination map",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'prepass_interpolation_accuracy',
        'desc' : "Interpolation accuracy for the illumination map; normally 1.0 is fine",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'geom_samples_per_unit_area',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 16,
    },
    {
        'attr' : 'geom_auto_density',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'geom_surface_offset',
        'desc' : "An offset along the geometric surface normal at which to perform shading in order to avoid surface acne",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'geom_preview_samples',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'geom_max_distance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'geom_background_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'geom_samples_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'option_reflections_trace',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'option_reflections_maxDepth',
        'desc' : "",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'option_reflections_cutoff',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'channels',
        'desc' : "Render channels the result of this BRDF will be written to",
        'type' : 'LIST',
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

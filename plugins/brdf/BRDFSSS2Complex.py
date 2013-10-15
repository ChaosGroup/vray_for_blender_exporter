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

from vb25.lib   import ExportUtils
from vb25.ui.classes import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'BRDF'
ID   = 'BRDFSSS2Complex'
NAME = 'SSS 2 Complex'
DESC = ""

PluginParams = (
    {
        'attr' : 'prepass_rate',
        'desc' : "Sampling density for the illumination map",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'interpolation_accuracy',
        'desc' : "Interpolation accuracy for the illumination map; normally 1.0 is fine",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'scale',
        'desc' : "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smaller",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'ior',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.5,
    },
    {
        'attr' : 'overall_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'diffuse_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'diffuse_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0,
    },
    {
        'attr' : 'sub_surface_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.5, 0.5, 0.5),
    },
    {
        'attr' : 'scatter_radius',
        'desc' : "This is measured in centimeters",
        'type' : 'TEXTURE',
        'default' : (0.92, 0.52, 0.175),
    },
    {
        'attr' : 'scatter_radius_mult',
        'desc' : "The scatter radius will be multiplied by this number",
        'type' : 'FLOAT_TEXTURE',
        'default' : 2,
    },
    {
        'attr' : 'phase_function',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'legacy_mode',
        'desc' : "true to turn on the old method for calculating volume properties from the scatter_radius",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'specular_color',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (1, 1, 1),
    },
    {
        'attr' : 'specular_amount',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 1,
    },
    {
        'attr' : 'specular_glossiness',
        'desc' : "",
        'type' : 'FLOAT_TEXTURE',
        'default' : 0.6,
    },
    {
        'attr' : 'specular_subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'cutoff_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.01,
    },
    {
        'attr' : 'trace_reflections',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'reflection_depth',
        'desc' : "",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'single_scatter',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'subdivs',
        'desc' : "Single scatter subdivisions",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'refraction_depth',
        'desc' : "",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'front_scatter',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'back_scatter',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'scatter_gi',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'prepass_blur',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1.2,
    },
    {
        'attr' : 'prepass_id',
        'desc' : "0 to calculate a separate illuminataion map for this shader; otherwise all shaders with the same prepass ID will share the same illumination map",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'channels',
        'desc' : "Render channels the result of this BRDF will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'linear_workflow',
        'desc' : "Set to true to apply the inverse of gamma correction",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'prepass_mode',
        'desc' : "Prepass mode: 0 - calculate new irradiance map for each frame (meaningless in RT); 1 - calculate and save map for each frame (meaningless in RT); 2 - load saved irradiance map for each frame; 3 - calculate and save map only for the first rendered frame; 4 - load saved irradiance map on the first rendered frame only",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'prepass_fileName',
        'desc' : "File path template for saved irradiance map files, frame number is appended for modes 1 and 2",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'geometry_based_sampling',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'samples_per_unit_area',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 16,
    },
    {
        'attr' : 'auto_density',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'surface_offset',
        'desc' : "An offset along the geometric surface normal at which to perform shading in order to avoid surface acne",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'preview_samples',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'max_distance',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'background_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'samples_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },
)

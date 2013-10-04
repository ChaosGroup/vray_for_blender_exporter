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
from vb25.ui.ui import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'BRDF'
ID   = 'BRDFSSS2'
NAME = 'BRDFSSS2'
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
        'attr' : 'diffuse_reflectance',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0.81, 0.81, 0.69, 1),
    },
    {
        'attr' : 'scatter_radius',
        'desc' : "This is measured in centimeters",
        'type' : 'TEXTURE',
        'default' : (0.92, 0.52, 0.175, 1),
    },
    {
        'attr' : 'scatter_radius_mult',
        'desc' : "The scatter radius will be multiplied by this number",
        'type' : 'FLOAT_TEXTURE',
        'default' : 2,
    },
    {
        'attr' : 'subdivs',
        'desc' : "",
        'type' : 'INT',
        'default' : 8,
    },
    {
        'attr' : 'phase_function',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'single_scatter',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
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
        'attr' : 'prepass_lod_threshold',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 4,
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
        'attr' : 'linear_workflow',
        'desc' : "Set to true to apply the inverse of gamma correction",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'legacy_mode',
        'desc' : "Turns on the old method for computing volume properties from the scatter_radius",
        'type' : 'BOOL',
        'default' : False,
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

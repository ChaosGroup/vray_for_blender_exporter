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
ID   = 'SettingsIrradianceMap'
NAME = 'SettingsIrradianceMap'
DESC = ""

PluginParams = (
    {
        'attr' : 'min_rate',
        'desc' : "This value determines the resolution for the first GI pass",
        'type' : 'INT',
        'ui' : {
            'min' : -8,
        },
        'default' : -3,
    },
    {
        'attr' : 'max_rate',
        'desc' : "This value determines the resolution of the last GI pass",
        'type' : 'INT',
        'ui' : {
            'min' : -8,
        },
        'default' : 0,
    },
    {
        'attr' : 'subdivs',
        'desc' : "This controls the quality of individual GI samples",
        'type' : 'INT',
        'default' : 80,
    },
    {
        'attr' : 'interp_samples',
        'name' : "Interpolation Samples",
        'desc' : "The number of GI samples that will be used to interpolate the indirect illumination at a given point",
        'type' : 'INT',
        'default' : 20,
    },
    {
        'attr' : 'calc_interp_samples',
        'name' : "Calc. Pass Interpolation Samples",
        'desc' : "The number of already computed samples that will be used to guide the sampling algorithm",
        'type' : 'INT',
        'default' : 15,
    },
    {
        'attr' : 'interp_frames',
        'name' : "Interpolation Frames",
        'desc' : "The number of frames that will be used to interpolate GI when the \"Mode\" is set to \"Animation (rendering)\"",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'color_threshold',
        'desc' : "This parameter controls how sensitive the irradiance map algorithm is to changes in indirect lighting",
        'type' : 'FLOAT',
        'default' : 0.3,
    },
    {
        'attr' : 'normal_threshold',
        'desc' : "This parameter controls how sensitive the irradiance map is to changes in surface normals and small surface details",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'distance_threshold',
        'desc' : "This parameter controls how sensitive the irradiance map is to distance between surfaces",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'detail_enhancement',
        'name' : "Detail Enhancement",
        'desc' : "Detail enhancement is a method for bringing additional detail to the irradiance map in the case where there are small details in the image",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'detail_radius',
        'name' : "Detail Enhancement Radius",
        'desc' : "This determines the radius for the detail enhancement effect",
        'type' : 'FLOAT',
        'default' : 0.2,
    },
    {
        'attr' : 'detail_subdivs_mult',
        'name' : "Detail Enhancement Subdivs Mult",
        'desc' : "The number of samples taken for the high-precision sampling as a percentage of the irradiance map Hemispheric subdivs",
        'type' : 'FLOAT',
        'default' : 60,
    },
    {
        'attr' : 'detail_scale',
        'desc' : "Detail enhancement scale",
        'type' : 'ENUM',
        'items' : (
            ('0', "Screen", "Radius in pixels"),
            ('1', "World",  "Radius in world units")
        ),
        'default' : '0',
    },
    {
        'attr' : 'randomize_samples',
        'desc' : "When it is checked, the image samples will be randomly jittered",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'interpolation_mode',
        'desc' : "Method for interpolating the GI value from the samples in the irradiance map",
        'type' : 'ENUM',
        'items' : (
            ('0', "Least squares with Voronoi weights", ""),
            ('1', "Delone triangulation",  ""),
            ('2', "Least squares fit", ""),
            ('3', "Weighted average", "")
        ),
        'default' : '2',
    },
    {
        'attr' : 'lookup_mode',
        'desc' : "Method of choosing suitable points from the irradiance map to be used as basis for the interpolation",
        'type' : 'ENUM',
        'items' : (
            ('0',"Quad-Balanced",""),
            ('1',"Nearest",""),
            ('2',"Overlapping",""),
            ('3',"Density-Based","")
        ),
        'default' : '3',
    },
    {
        'attr' : 'mode',
        'desc' : "Irradiance map mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Single Frame",                   "A new irradiance map is created for each frame"),
            ('1', "Multiframe Incremental",         "At the start of the rendering, the irradiance map is deleted, and then each frame incrementally adds to the irradiance map in memory"),
            ('2', "From File",                      "The irradiance map is loaded from a file"),
            ('3', "Add To Current Map",             "A new irradiance map is created and added to the one in memory"),
            ('4', "Incremental Add To Current Map", "Each frame adds incrementally to the irradiance map in memory; the old map is not deleted"),
            ('5', "Bucket Mode",                    "Each render region (bucket) calculates its own irradiance map independently of the rest"),
            ('6', "Animation (Prepass)",            "Separate irradiance map is rendered and saved with a different name for each frame; no final image is rendered"),
            ('7', "Animation (Rendering)",          "Final rendering of animation using saved per-frame irradiance maps")
        ),
        'default' : '0',
    },
    {
        'attr' : 'dont_delete',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'file',
        'desc' : "Irradiance map file name",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/irradiance_map.vrmap",
    },
    {
        'attr' : 'show_samples',
        'desc' : "Show Irradiance Map samples",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'show_calc_phase',
        'desc' : "Show Irradiance Map calculation process",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'show_direct_light',
        'desc' : "Show direct light when showing calculation process",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'multiple_views',
        'desc' : "When this option is on, V-Ray will calculate the irradiance map samples for the entire camera path, instead of just the current view",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'multipass',
        'desc' : "When checked, this will cause V-Ray to use all irradiance map samples computed so far",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'check_sample_visibility',
        'desc' : "This will cause V-Ray to use only those samples from the irradiance map, which are directly visible from the interpolated point",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'auto_save',
        'desc' : "Automatically save the irradiance map to the specified file at the end of the rendering",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'auto_save_file',
        'desc' : "Irradiance map auto save file",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "//lightmaps/irradiance_map.vrmap",
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

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

from vb25.lib import ExportUtils


TYPE = 'SETTINGS'
ID   = 'SettingsRTEngine'
NAME = 'Realtime Engine Settings'
DESC = "Realtime Engine settings"

PluginParams = (
    {
        'attr' : 'cpu_bundle_size',
        'desc' : "Number of samples to transfer over the network for RT-CPU",
        'type' : 'INT',
        'default' : 128,
    },
    {
        'attr' : 'cpu_samples_per_pixel',
        'desc' : "Number of samples per pixel for RT-CPU",
        'type' : 'INT',
        'default' : 4,
    },
    {
        'attr' : 'gpu_bundle_size',
        'desc' : "Number of samples to transfer over the network for RT-GPU",
        'type' : 'INT',
        'default' : 192,
    },
    {
        'attr' : 'gpu_samples_per_pixel',
        'desc' : "Number of samples per pixel for RT-GPU",
        'type' : 'INT',
        'default' : 16,
    },
    {
        'attr' : 'trace_depth',
        'desc' : "Maximum trace depth for reflections/refractions etc",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'gi_depth',
        'desc' : "Maximum trace depth for GI",
        'type' : 'INT',
        'default' : 3,
    },
    {
        'attr' : 'coherent_tracing',
        'desc' : "true to enable coherent tracing of gi/reflections/refractions etc",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'stereo_mode',
        'desc' : "Enable side-by-side stereo rendering",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'stereo_eye_distance',
        'desc' : "Distance between the two cameras for stereo mode",
        'type' : 'FLOAT',
        'precision' : 4,
        'default' : 0.065,
    },
    {
        'attr' : 'stereo_focus',
        'desc' : "Focus mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", ""),
            ('1', "Rotation", ""),
            ('2', "Shear", ""),
        ),
        'default' : '2',
    },
    {
        'attr' : 'opencl_texsize',
        'desc' : "OpenCL Single Kernel maximum texture size - bigger textures are scaled to fit this size",
        'type' : 'INT',
        'default' : 512,
    },
    {
        'attr' : 'opencl_resizeTextures',
        'desc' : "true to resize textures for the GPU based on opencl_texsize; false to use full resolution textures",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'opencl_textureFormat',
        'desc' : "Format for the textures on the GPU",
        'type' : 'ENUM',
        'items' : (
            ('0', "32-Bit Float", ""),
            ('1', "16-Bit Half Float", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'progressive_samples_per_pixel',
        'desc' : "Progressive increase for samples_per_pixel (from 1 to real value). Use this for faster feadback",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'undersampling',
        'desc' : "Use undersampling",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'disable_render_elements',
        'desc' : "Produce only RGBA",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'max_render_time',
        'desc' : "Max render time (0 = inf)",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'max_sample_level',
        'desc' : "Max sample level (0 = inf)",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'noise_threshold',
        'desc' : "Noise threshold for the image sampler (0 = inf)",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'enable_mask',
        'desc' : "Show AA mask",
        'type' : 'BOOL',
        'default' : False,
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "align" : true,
        "attrs" : [
            { "name" : "trace_depth" },
            { "name" : "gi_depth" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "ROW",
        "align" : true,
        "attrs" : [
            { "name" : "cpu_bundle_size" },
            { "name" : "cpu_samples_per_pixel" }
        ]
    },

    {   "layout" : "SEPARATOR" },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "opencl_texsize" },
                    { "name" : "opencl_textureFormat", "label" : "" },
                    { "name" : "opencl_resizeTextures" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "gpu_bundle_size" },
                    { "name" : "gpu_samples_per_pixel" }
                ]
            }
        ]
    },

    {   "layout" : "COLUMN",
        "align" : true,
        "attrs" : [
            { "name" : "max_render_time" },
            { "name" : "max_sample_level" },
            { "name" : "noise_threshold" }
        ]
    },

    {   "layout" : "COLUMN",
        "attrs" : [
            { "name" : "progressive_samples_per_pixel" },
            { "name" : "coherent_tracing" },
            { "name" : "undersampling" },
            { "name" : "disable_render_elements" },
            { "name" : "enable_mask" }
        ]
    },

    {   "layout" : "COLUMN",
        "align" : true,
        "attrs" : [
            { "name" : "stereo_mode" }
        ]
    },

    {   "layout" : "COLUMN",
        "active" : { "prop" : "stereo_mode" },
        "attrs" : [
            { "name" : "stereo_focus" },
            { "name" : "stereo_eye_distance" }
        ]
    }
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']

    overrideParams.update({
        'noise_threshold' : 0.0 if scene.render.engine == 'VRAY_RENDER_RT' else propGroup.noise_threshold,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

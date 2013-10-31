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
ID   = 'SettingsRTEngine'
NAME = 'SettingsRTEngine'
DESC = ""

PluginParams = (
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
        'attr' : 'coherent_tracing',
        'desc' : "true to enable coherent tracing of gi/reflections/refractions etc",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'stereo_mode',
        'desc' : "Non-zero to enable side-by-side stereo rendering",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'stereo_eye_distance',
        'desc' : "Distance between the two cameras for stereo mode",
        'type' : 'FLOAT',
        'default' : 6.5,
    },
    {
        'attr' : 'stereo_focus',
        'desc' : "Focus mode (0 - none, 1 - rotation, 2 - shear)",
        'type' : 'INT',
        'default' : 2,
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
        'desc' : "Format for the textures on the GPU (0 - 32-bit float; 1 - 16-bit half float)",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'progressive_samples_per_pixel',
        'desc' : "Progressive increase for samples_per_pixel (from 1 to real value). Use this for faster feadback",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'undersampling',
        'desc' : "1 to use undersampling, 0 otherwise. Default is 1",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'disable_render_elements',
        'desc' : "if 1, RT will produce only RGBA. Default is 0",
        'type' : 'INT',
        'default' : 0,
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
        'desc' : "Show aa mask",
        'type' : 'INT',
        'default' : 0,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""

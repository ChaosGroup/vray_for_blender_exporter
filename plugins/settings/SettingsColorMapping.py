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
ID   = 'SettingsColorMapping'
NAME = 'Color Mapping'
DESC = ""


PluginParams = (
    {
        'attr' : 'type',
        'desc' : "",
        'type' : 'ENUM',
        'items' : (
            ('0', "Linear", ""),
            ('1', "Exponential", ""),
            ('2', "HSV Exponential", ""),
            ('3', "Intensity Exponential", ""),
            ('4', "Gamma Correction", ""),
            ('5', "Intensity Gamma", ""),
            ('6', "Reinhard", "")
        ),
        'default' : '0',
    },
    {
        'attr' : 'affect_background',
        'desc' : "Affect colors belonging to the background",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'dark_mult',
        'name' : "Dark multiplier",
        'desc' : "Multiplier for dark colors",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'bright_mult',
        'name' : "Bright multiplier",
        'desc' : "Multiplier for bright colors",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'gamma',
        'desc' : "Gamma correction for the output image regardless of the color mapping mode",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'subpixel_mapping',
        'desc' : "This option controls whether color mapping will be applied to the final image pixels, or to the individual sub-pixel samples",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'clamp_output',
        'desc' : "Clamp colors",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'clamp_level',
        'desc' : "The level at which colors will be clamped",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'adaptation_only',
        'desc' : "When this parameter is on, the color mapping will not be applied to the final image, however V-Ray will proceed with all its calculations as though color mapping is applied (e.g. the noise levels will be corrected accordingly)",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'linearWorkflow',
        'desc' : "When this option is checked V-Ray will automatically apply the inverse of the Gamma correction that you have set in the Gamma field to all materials in scene",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'exposure',
        'desc' : "Additional image exposure",
        'type' : 'COLOR',
        'default' : (1, 1, 1),
    },

    {
        'attr' : 'input_gamma',
        'desc' : "Input gamma for textures",
        'type' : 'FLOAT',
        'skip' : True,
        'default' : 1,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    import bpy
    from vb30.lib import ExportUtils

    if bus['preview']:
        # Use color mapping settings from current scene not from preview scene
        propGroup = bpy.context.scene.vray.SettingsColorMapping

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

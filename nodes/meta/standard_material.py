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

import bpy

from vb30 import plugins as PluginUtils
from vb30.ui import classes
from vb30.nodes import utils as NodeUtils
from vb30.nodes import sockets as SocketUtils


class VRayNodeMetaStandardMaterial(bpy.types.Node):
    bl_idname = 'VRayNodeMetaStandardMaterial'
    bl_label  = 'Standard Material'
    bl_icon   = 'MATERIAL'

    vray_plugins = ('BRDFVRayMtl',
                    'BRDFBump',
                    'MtlSingleBRDF',
                    'MtlMaterialID')

    vray_type   = bpy.props.StringProperty(default='MATERIAL')
    vray_plugin = bpy.props.StringProperty(default='MtlSingleBRDF')

    def init(self, context):
        attr_filter = {
            'BRDFVRayMtl': {
            },
            'BRDFBump': {
                'base_brdf',
            },
            'MtlSingleBRDF': {
                'brdf',
            },
            'MtlMaterialID': {
                'base_mtl',
            },
        }

        for pluginID in self.vray_plugins:
            NodeUtils.AddDefaultInputs(self, PluginUtils.PLUGINS_ID[pluginID], attrFilter=attr_filter[pluginID])

        SocketUtils.AddOutput(self, 'VRaySocketMtl', "Material")

    def copy(self, node):
        pass

    def draw_buttons(self, context, layout):
        layout.prop(self.BRDFVRayMtl, 'brdf_type', text="BRDF")

    def draw_buttons_ext(self, context, layout):
        plugin_labels = {
            'BRDFVRayMtl': "BRDF",
            'BRDFBump': "Bump / Normal Mapping",
            'MtlSingleBRDF': "Material",
            'MtlMaterialID': "Material ID",
        }

        for pluginID in self.vray_plugins:
            box = layout.box()

            label = plugin_labels[pluginID]
            if label:
                box.label("%s:" % label)

            classes.DrawPluginUI(
                context,
                box,
                self,
                getattr(self, pluginID),
                pluginID,
                PluginUtils.PLUGINS_ID[pluginID]
            )


def GetRegClasses():
    return (
        VRayNodeMetaStandardMaterial,
   )


def register():
    for pluginID in VRayNodeMetaStandardMaterial.vray_plugins:
        pluginDesc = PluginUtils.PLUGINS_ID[pluginID]
        PluginUtils.AddAttributes(pluginDesc, VRayNodeMetaStandardMaterial)

    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

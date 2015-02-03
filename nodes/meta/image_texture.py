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

from .. import utils as NodeUtils
from .. import sockets as SocketUtils


class VRayNodeMetaImageTexture(bpy.types.Node):
    bl_idname = 'VRayNodeMetaImageTexture'
    bl_label  = 'Image File Texture'
    bl_icon   = 'TEXTURE'

    vray_type   = bpy.props.StringProperty(default='TEXTURE')
    vray_plugin = bpy.props.StringProperty(default='TexBitmap')

    mapping_type = bpy.props.EnumProperty(
        items = (
            ('UV',         "UV",         "UV mapping"),
            ('PROJECTION', "Projection", "Generated mapping"),
            ('OBJECT',     "Object",     "Object mapping"),
        ),
        default = 'UV'
    )

    def init(self, context):
        NodeUtils.CreateBitmapTexture(self)
        NodeUtils.AddDefaultInputs(self, PluginUtils.PLUGINS_ID['UVWGenMayaPlace2dTexture'])
        NodeUtils.AddDefaultOutputs(self, PluginUtils.PLUGINS_ID['TexBitmap'])
        SocketUtils.AddOutput(self, 'VRaySocketColor', "Output")


    def draw_buttons(self, context, layout):
        box = layout.box()
        box.label("Image Settings:")
        bitmapPluginDesc = PluginUtils.PLUGINS_ID['BitmapBuffer']
        bitmapPluginDesc.nodeDraw(context, box, self)

        box = layout.box()
        box.label("Mapping Settings:")
        box.row().prop(self, 'mapping_type', expand=True)

        mappingPluginID = None
        if self.mapping_type == 'UV':
            mappingPluginID = 'UVWGenMayaPlace2dTexture'
        elif self.mapping_type == 'PROJECTION':
            mappingPluginID = 'UVWGenProjection'
        elif self.mapping_type == 'OBJECT':
            mappingPluginID = 'UVWGenObject'

        if mappingPluginID:
            mapPluginDesc = PluginUtils.PLUGINS_ID[mappingPluginID]
            if hasattr(mapPluginDesc, 'nodeDraw'):
                mapPluginDesc.nodeDraw(context, box, getattr(self, mappingPluginID))


    def draw_buttons_ext(self, context, layout):
        box = layout.box()
        box.label("Bitmap Settings:")
        bitmapPluginDesc = PluginUtils.PLUGINS_ID['BitmapBuffer']
        classes.DrawPluginUI(
            context,
            box,
            self,
            self.BitmapBuffer,
            'BitmapBuffer',
            bitmapPluginDesc
        )

        box = layout.box()
        box.label("Mapping Settings:")
        uvPluginDesc = PluginUtils.PLUGINS_ID['UVWGenMayaPlace2dTexture']
        classes.DrawPluginUI(
            context,
            box,
            self.UVWGenMayaPlace2dTexture,
            self.UVWGenMayaPlace2dTexture,
            'UVWGenMayaPlace2dTexture',
            uvPluginDesc
        )


def GetRegClasses():
    return (
        VRayNodeMetaImageTexture,
   )


def register():
    for pluginID in {'BitmapBuffer', 'TexBitmap', 'UVWGenMayaPlace2dTexture', 'UVWGenProjection'}:
        pluginDesc = PluginUtils.PLUGINS_ID[pluginID]

        PluginUtils.AddAttributes(pluginDesc, VRayNodeMetaImageTexture)

    NodeUtils.CreateFakeTextureAttribute(VRayNodeMetaImageTexture)

    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

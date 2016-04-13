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

from vb30.lib import PluginUtils

PluginUtils.loadPluginOnModule(globals(), __name__)


def nodeDraw(context, layout, node):
    if not node.texture:
        layout.label("Missing texture!")
    else:
        layout.template_ID(node.texture, 'image', open='image.open')
        col = layout.column(align=True)
        col.label("Double click to show in editor")
        col.label("and on object's active UV Map.")


def gui(context, layout, BitmapBuffer, node):
    if node.texture:
        if node.texture.image:
            if not context.scene.render.engine == 'VRAY_RENDER_PREVIEW':
                layout.template_preview(node.texture)
            layout.separator()
            layout.template_image(node.texture, 'image', node.texture.image_user)
        else:
            layout.template_ID(node.texture, 'image', open='image.open')
        layout.separator()

    # NOTE: PluginWidget will go after
    layout.label("V-Ray Settings:")

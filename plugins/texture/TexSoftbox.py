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


def gui(context, layout, TexSoftbox, node):
    box = layout.box()
    box.prop(TexSoftbox, 'grad_vert_on', text="V Vignette")
    if TexSoftbox.grad_vert_on:
        col = box.column()
        col.prop(TexSoftbox, 'grad_vert_flip')
        col.template_color_ramp(node.ramp_grad_vert, 'color_ramp', expand=True)

    box = layout.box()
    box.prop(TexSoftbox, 'grad_horiz_on', text="U Vignette")
    if TexSoftbox.grad_horiz_on:
        col = box.column()
        col.prop(TexSoftbox, 'grad_horiz_flip')
        col.template_color_ramp(node.ramp_grad_horiz, 'color_ramp', expand=True)

    box = layout.box()
    box.prop(TexSoftbox, 'grad_rad_on', text="Radial Vignette")
    if TexSoftbox.grad_rad_on:
        col = box.column()
        col.prop(TexSoftbox, 'grad_rad_flip')
        col.template_color_ramp(node.ramp_grad_rad, 'color_ramp', expand=True)

    box = layout.box()
    box.prop(TexSoftbox, 'frame_on', text="Frame Vignette")
    if TexSoftbox.frame_on:
        col = box.column()
        col.prop(TexSoftbox, 'frame_flip')
        col.template_color_ramp(node.ramp_frame, 'color_ramp', expand=True)

        col = box.column()
        col.prop(TexSoftbox, 'frame_tint_on', text="Frame Tint")
        if TexSoftbox.frame_tint_on:
            row = col.row(align=True)
            row.prop(TexSoftbox, 'frame_tint', text="")
            row.prop(TexSoftbox, 'frame_tint_strength', text="Strength")

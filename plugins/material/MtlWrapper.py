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

from vb30.lib import PluginUtils
from vb30.lib import ExportUtils
from vb30.lib.DrawUtils import GetContextType, GetRegionWidthFromContext
from vb30.ui.classes    import narrowui


PluginUtils.loadPluginOnModule(globals(), __name__)


def gui(context, layout, MtlWrapper, node):
    contextType = GetContextType(context)
    regionWidth = GetRegionWidthFromContext(context)

    wide_ui = regionWidth > narrowui

    split= layout.split()
    col= split.column()
    col.prop(MtlWrapper, 'generate_gi')
    col.prop(MtlWrapper, 'receive_gi')
    if wide_ui:
        col= split.column()
    col.prop(MtlWrapper, 'generate_caustics')
    col.prop(MtlWrapper, 'receive_caustics')

    split= layout.split()
    col= split.column()
    col.prop(MtlWrapper, 'gi_quality_multiplier')

    split= layout.split()
    col= split.column()
    col.label(text="Matte properties")

    split= layout.split()
    colL= split.column()
    colL.prop(MtlWrapper, 'matte_surface')
    if wide_ui:
        colR= split.column()
    else:
        colR= colL
    colR.prop(MtlWrapper, 'alpha_contribution')
    if MtlWrapper.matte_surface:
        colR.prop(MtlWrapper, 'reflection_amount')
        colR.prop(MtlWrapper, 'refraction_amount')
        colR.prop(MtlWrapper, 'gi_amount')
        colR.prop(MtlWrapper, 'no_gi_on_other_mattes')

        colL.prop(MtlWrapper, 'affect_alpha')
        colL.prop(MtlWrapper, 'shadows')
        if MtlWrapper.shadows:
            colL.prop(MtlWrapper, 'shadow_tint_color')
            colL.prop(MtlWrapper, 'shadow_brightness')

    split= layout.split()
    col= split.column()
    col.label(text="Miscellaneous")

    split= layout.split()
    col= split.column()
    col.prop(MtlWrapper, 'gi_surface_id')
    col.prop(MtlWrapper, 'trace_depth')
    if wide_ui:
        col= split.column()
    col.prop(MtlWrapper, 'matte_for_secondary_rays')

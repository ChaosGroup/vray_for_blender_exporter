#
# V-Ray/Blender
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

import json

from . import AttributeUtils

from pynodes_framework import idref


def GetContextType(context):
    if hasattr(context, 'node'):
        return 'NODE'
    if hasattr(context, 'material'):
        return 'MATERIAL'
    return None


def GetRegionWidthFromContext(context):
    contextType = GetContextType(context)
    if contextType == 'NODE':
        return context.node.width
    elif hasattr(context, 'region'):
        return context.region.width
    # Assume wide region width
    return 1024


def IsRegionWide(context):
    regionWidth = GetRegionWidthFromContext(context)
    if regionWidth > 200:
        return True
    return False


def DrawAttr(layout, propGroup, attr, text=None):
    if not hasattr(propGroup, attr):
        return    
    if text is not None:    
        layout.prop(propGroup, attr, text=text)
    else:
        layout.prop(propGroup, attr)


def Draw(context, layout, dataPointer, PluginParams):
    for attrDesc in PluginParams:
        if attrDesc['type'] in AttributeUtils.SkippedTypes:
            continue
        if attrDesc['type'] in AttributeUtils.OutputTypes:
            continue
        if attrDesc['type'] in AttributeUtils.InputTypes:
            continue

        if attrDesc['type'] in {'IMAGE', 'NODETREE', 'MTEX'}:
            idref.draw_idref(layout, dataPointer, attrDesc['attr'])
        else:
            DrawAttr(layout, dataPointer, attrDesc['attr'])


def RenderItem(dataPointer, layout, attr, text=None, expand=False):
    if text is not None:
        layout.prop(dataPointer, attr, expand=expand, text=text)
    else:
        layout.prop(dataPointer, attr, expand=expand)


def RenderContainer(context, layout, item, align=False, label=None):
    if item == 'SPLIT':
        return layout.split()
    elif item == 'COLUMN':
        return layout.column(align=align)
    elif item == 'ROW':
        if not IsRegionWide(context):
            return layout.column(align=align)
        return layout.row(align=align)
    elif item == 'SEPARATOR':
        if label is not None:
            layout.label(text=label)
        else:
            layout.separator()
        return layout
    elif item == 'BOX':
        return layout.box()
    return layout


def RenderWidget(context, dataPointer, layout, widget):
    # Layout
    containerType = widget['layout']

    if containerType == 'SPLIT':
        subLayout = layout
        
        if IsRegionWide(context):
            subLayout = RenderContainer(context, layout, 'SPLIT')

        for w in widget['splits']:
            RenderWidget(context, dataPointer, subLayout, w)

    # Optional stuff
    containerAlign = widget.get('align', False)
    containerLabel = widget.get('label', None)

    container = RenderContainer(context, layout, containerType, containerAlign, containerLabel)

    widgetAttributes = widget.get('attrs', {})

    for item in widgetAttributes:
        # Attribute name
        attr = item['name']

        # Optional stuff
        label        = item.get('label', None)
        drawExpanded = IsRegionWide(context) and item.get('expand', False)

        RenderItem(dataPointer, container, attr, text=label, expand=drawExpanded)


def RenderTemplate(context, layout, dataPointer, pluginModule):
    jsonTemplate = pluginModule.PluginWidget

    widgetDesc = json.loads(jsonTemplate)

    for widget in widgetDesc['widgets']:
        RenderWidget(context, dataPointer, layout, widget)

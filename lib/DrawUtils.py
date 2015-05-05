#
# V-Ray/Blender
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

import json

from . import AttributeUtils


def GetContextType(context):
    if hasattr(context, 'node') and context.node:
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


def Draw(context, layout, propGroup, PluginParams):
    for attrDesc in sorted(PluginParams, key=lambda x: x['attr']):
        if attrDesc['type'] in AttributeUtils.SkippedTypes:
            continue
        if attrDesc['type'] in AttributeUtils.OutputTypes:
            continue
        if attrDesc['type'] in AttributeUtils.InputTypes:
            continue

        DrawAttr(layout, propGroup, attrDesc['attr'])


def EvalUiState(item, propGroup):
    cond_prop   = item.get('prop')
    cond_type   = item.get('condition', 'equal')
    cond_value  = item.get('value', True)

    prop_value = getattr(propGroup, cond_prop)

    if type(cond_value) is int:
        prop_value = int(prop_value)
    elif type(cond_value) is bool:
        prop_value = bool(prop_value)

    cond = True
    if cond_type == 'equal':
        cond = prop_value == cond_value
    elif cond_type == 'not_equal':
        cond = prop_value != cond_value
    elif cond_type == 'greater':
        cond = prop_value > cond_value
    elif cond_type == 'less':
        cond = prop_value < cond_value
    elif cond_type == 'greater_or_equal':
        cond = prop_value >= cond_value
    elif cond_type == 'less_or_equal':
        cond = prop_value <= cond_value

    # print("%s == %s:%s => %s" % (
    #     cond_prop,
    #     cond_value,
    #     prop_value,
    #     cond
    # ))

    return cond


def ShowContainer(layout, show, propGroup):
    if show is not None:
        return EvalUiState(show, propGroup)
    return True


def SetActive(layout, active, propGroup):
    if active is not None:
        layout.active = EvalUiState(active, propGroup)


def RenderItem(propGroup, layout, attr, text=None, slider=False, expand=False, active=None):
    container = layout

    if active is not None:
        container = layout.row()
        container.active = EvalUiState(active, propGroup)

    if text is not None:
        container.prop(propGroup, attr, slider=slider, expand=expand, text=text)
    else:
        container.prop(propGroup, attr, slider=slider, expand=expand)


def RenderContainer(context, layout, item, align=False, label=None, propGroup=None, active=None):
    container = layout

    if item == 'SPLIT':
        container = layout.split()
    elif item == 'COLUMN':
        container = layout.column(align=align)
    elif item == 'ROW':
        if not IsRegionWide(context):
            container = layout.column(align=align)
        else:
            container = layout.row(align=align)
    elif item == 'SEPARATOR':
        if label is not None:
            layout.separator()
            layout.label(text="%s:" % label)
        else:
            layout.separator()
        container = layout
    elif item == 'BOX':
        container = layout.box()

    SetActive(container, active, propGroup)

    return container


def RenderWidget(context, propGroup, layout, widget):
    # Layout
    containerType   = widget.get('layout', 'COLUMN')
    containerActive = widget.get('active', None)
    containerShow   = widget.get('show', None)

    if not ShowContainer(layout, containerShow, propGroup):
        return

    if containerType == 'SPLIT':
        subLayout = layout

        if IsRegionWide(context):
            subLayout = RenderContainer(
                context,
                layout,
                'SPLIT',
                propGroup=propGroup,
                active=containerActive
            )
        else:
            if containerActive is not None:
                subLayout = layout.split()
                SetActive(subLayout, containerActive, propGroup)

        for w in widget['splits']:
            RenderWidget(context, propGroup, subLayout, w)

    # Optional stuff
    containerAlign  = widget.get('align', False)
    containerLabel  = widget.get('label', None)
    containerActive = widget.get('active', None)

    container = RenderContainer(
        context,
        layout,
        containerType,
        containerAlign,
        containerLabel,
        propGroup=propGroup,
        active=containerActive
    )

    widgetAttributes = widget.get('attrs', {})

    for item in widgetAttributes:
        # Attribute name
        attr = item['name']

        # Optional stuff
        label  = item.get('label', None)
        active = item.get('active', None)
        expand = IsRegionWide(context) and item.get('expand', False)
        slider = item.get('slider', False)

        RenderItem(propGroup, container, attr, text=label, slider=slider, expand=expand, active=active)


def RenderTemplate(context, layout, propGroup, pluginModule):
    jsonTemplate = pluginModule.PluginWidget

    widgetDesc = jsonTemplate if type(jsonTemplate) is dict else json.loads(jsonTemplate)

    for widget in widgetDesc['widgets']:
        RenderWidget(context, propGroup, layout, widget)

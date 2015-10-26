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

import re

import bpy

from vb30.debug import Debug, PrintDict

from . import CallbackUI


PluginTypes = {
    'BRDF',
    'MATERIAL',
    'PLUGIN',
    'TEXTURE',
    'UVWGEN',
}

SkippedTypes = {
    'LIST',
    'INT_LIST',
    'FLOAT_LIST',
    'VECTOR_LIST',
    'COLOR_LIST',
    'MAPCHANNEL_LIST',
    'TRANSFORM_LIST',
    'TRANSFORM_TEXTURE',
}

InputTypes = {
    'BRDF',
    'FLOAT_TEXTURE',
    'VECTOR_TEXTURE',
    'GEOMETRY',
    'MATERIAL',
    'PLUGIN',
    'TEXTURE',
    'UVWGEN',
    'VECTOR',
    'TRANSFORM',
    'MATRIX',
}

OutputTypes = {
    'OUTPUT_PLUGIN',
    'OUTPUT_COLOR',
    'OUTPUT_FLOAT_TEXTURE',
    'OUTPUT_VECTOR_TEXTURE',
    'OUTPUT_TRANSFORM_TEXTURE',
    'OUTPUT_TEXTURE',
}

TypeToSocket = {
    'COLOR'  : 'VRaySocketColor',
    'VECTOR' : 'VRaySocketVector',
    'FLOAT'  : 'VRaySocketFloat',
    'INT'    : 'VRaySocketInt',

    'TRANSFORM' : 'VRaySocketTransform',
    'MATRIX'    : 'VRaySocketTransform',

    'BRDF'     : 'VRaySocketBRDF',
    'GEOMETRY' : 'VRaySocketGeom',
    'MATERIAL' : 'VRaySocketMtl',
    'PLUGIN'   : 'VRaySocketObject',
    'UVWGEN'   : 'VRaySocketCoords',

    'TEXTURE'       : 'VRaySocketColor',
    'FLOAT_TEXTURE' : 'VRaySocketFloatColor',
    'INT_TEXTURE'   : 'VRaySocketFloatColor',
    'VECTOR_TEXTURE' : 'VRaySocketVector',

    'OUTPUT_COLOR'             : 'VRaySocketColor',
    'OUTPUT_PLUGIN'            : 'VRaySocketObject',
    'OUTPUT_FLOAT_TEXTURE'     : 'VRaySocketFloatColor',
    'OUTPUT_TEXTURE'           : 'VRaySocketColor',
    'OUTPUT_VECTOR_TEXTURE'    : 'VRaySocketVector',
    'OUTPUT_TRANSFORM_TEXTURE' : 'VRaySocketTransform',
}

TypeToSocketNoValue = dict(TypeToSocket)
for key in TypeToSocketNoValue:
    if TypeToSocketNoValue[key] == 'VRaySocketColor':
        TypeToSocketNoValue[key] = 'VRaySocketColorNoValue'
    elif TypeToSocketNoValue[key] in {'VRaySocketFloat', 'VRaySocketFloatColor'}:
        TypeToSocketNoValue[key] = 'VRaySocketFloatNoValue'

TypeToProp = {
    'BOOL'   : bpy.props.BoolProperty,
    'COLOR'  : bpy.props.FloatVectorProperty,
    'ACOLOR' : bpy.props.FloatVectorProperty,
    'VECTOR' : bpy.props.FloatVectorProperty,
    'ENUM'   : bpy.props.EnumProperty,
    'FLOAT'  : bpy.props.FloatProperty,
    'INT'    : bpy.props.IntProperty,
    'STRING' : bpy.props.StringProperty,

    'TRANSFORM' : bpy.props.StringProperty,
    'MATRIX'    : bpy.props.StringProperty,

    'BRDF'     : bpy.props.StringProperty,
    'GEOMETRY' : bpy.props.StringProperty,
    'MATERIAL' : bpy.props.StringProperty,
    'PLUGIN'   : bpy.props.StringProperty,
    'UVWGEN'   : bpy.props.StringProperty,

    'INT_TEXTURE'   : bpy.props.IntProperty,
    'FLOAT_TEXTURE' : bpy.props.FloatProperty,
    'TEXTURE'       : bpy.props.FloatVectorProperty,
    'VECTOR_TEXTURE' : bpy.props.FloatVectorProperty,

    'OUTPUT_COLOR'             : bpy.props.FloatVectorProperty,
    'OUTPUT_PLUGIN'            : bpy.props.StringProperty,
    'OUTPUT_FLOAT_TEXTURE'     : bpy.props.FloatProperty,
    'OUTPUT_TEXTURE'           : bpy.props.FloatVectorProperty,
    'OUTPUT_VECTOR_TEXTURE'    : bpy.props.FloatVectorProperty,
    'OUTPUT_TRANSFORM_TEXTURE' : bpy.props.FloatVectorProperty,
}


# When there is no name specified for the attribute we could "guess" the name
# from the attribute like: 'dist_near' will become "Dist Near"
#
def GetNameFromAttr(attr):
    attr_name = attr.replace("_", " ")
    attr_name = re.sub(r"\B([A-Z])", r" \1", attr_name)

    return attr_name.title()


def ValueInEnumItems(attrDesc, enumValue):
    for item in attrDesc['items']:
        if item[0] == enumValue:
            return True
    return False


# This will generate Blender's Property based on attribute description
# and add it to 'classMembers' dict.
#
def GenerateAttribute(classMembers, attrDesc):
    if attrDesc['type'] in SkippedTypes:
        return

    # TODO: Widget attributes
    if attrDesc['type'].startswith('WIDGET_'):
        return

    attrArgs = {
        'attr'        : attrDesc['attr'],
        'name'        : attrDesc.get('name', GetNameFromAttr(attrDesc['attr'])),
        'description' : attrDesc['desc'],
    }

    if 'default' in attrDesc:
        attrArgs['default'] = attrDesc['default']

    if 'update' in attrDesc:
        attrArgs['update'] = attrDesc['update']

    defUi = {
        'min'      : -1<<20,
        'max'      :  1<<20,
        'soft_min' : 0,
        'soft_max' : 64,
    }

    attrFunc = TypeToProp[attrDesc['type']]

    if attrDesc['type'] in {'STRING'}:
        pass

    elif attrDesc['type'] in {'COLOR', 'ACOLOR', 'TEXTURE'}:
        c = attrDesc['default']
        attrArgs['subtype'] = 'COLOR'
        attrArgs['default'] = (c[0], c[1], c[2])
        attrArgs['min'] = 0.0
        attrArgs['max'] = 1.0

    elif attrDesc['type'] in {'VECTOR'}:
        if 'subtype' not in attrDesc:
            attrArgs['subtype'] = 'TRANSLATION'
        attrArgs['precision'] = 3

    elif attrDesc['type'] in {'FLOAT', 'FLOAT_TEXTURE'}:
        attrArgs['precision'] = attrDesc.get('precision', 3)

    elif attrDesc['type'] in {'INT', 'INT_TEXTURE'}:
        pass

    elif attrDesc['type'] in {'TRANSFORM', 'MATRIX'}:
        # Currenlty used as fake string attribute
        # attrArgs['size']    = 16
        # attrArgs['subtype'] = 'MATRIX'
        # attrArgs['default'] = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0)
        # Override default
        attrArgs['default'] = ""

    elif attrDesc['type'] in {'ENUM'}:
        # NOTE: JSON parser returns lists but need tuples
        attrArgs['items'] = (tuple(item) for item in attrDesc['items'])

    if 'options' in attrDesc:
        options = set()
        for opt in attrDesc['options']:
            # These options are not directly mapped into the Blender prop
            # options
            if opt not in {'LINKED_ONLY', 'EXPORT_AS_IS'}:
                options.add(opt)
        attrArgs['options'] = options

    for optionalKey in {'size', 'precision', 'subtype'}:
        if optionalKey in attrDesc:
            attrArgs[optionalKey] = attrDesc[optionalKey]

    if attrDesc['type'] in {'INT', 'INT_TEXTURE', 'FLOAT', 'FLOAT_TEXTURE'}:
        if 'ui' not in attrDesc:
            attrDesc['ui'] = defUi

        attrArgs['min'] = attrDesc['ui'].get('min', defUi['min'])
        attrArgs['max'] = attrDesc['ui'].get('max', defUi['max'])
        attrArgs['soft_min'] = attrDesc['ui'].get('soft_min', attrArgs['min'])
        attrArgs['soft_max'] = attrDesc['ui'].get('soft_max', attrArgs['max'])

    classMembers[attrDesc['attr']] = attrFunc(**attrArgs)

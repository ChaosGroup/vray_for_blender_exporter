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

import bpy


InputTypes = (
    'COLOR',
    'TEXTURE',
    'FLOAT_TEXTURE',
)

OutputTypes = (
    'OUTPUT_COLOR',
    'OUTPUT_TEXTURE',
    'OUTPUT_FLOAT_TEXTURE',
)

TypeToSocket = {
    'COLOR'         : 'VRaySocketColor',
    'TEXTURE'       : 'VRaySocketColor',
    'FLOAT_TEXTURE' : 'VRaySocketFloatColor',
    'BRDF'          : 'VRaySocketBRDF',
    'MATERIAL'      : 'VRaySocketMtl',

    'OUTPUT_COLOR'         : 'VRaySocketColor',
    'OUTPUT_TEXTURE'       : 'VRaySocketColor',
    'OUTPUT_FLOAT_TEXTURE' : 'VRaySocketFloatColor',
}

TypeToProp = {
    'BOOL'          : bpy.props.BoolProperty,
    'INT'           : bpy.props.IntProperty,
    'TEXTURE'       : bpy.props.FloatVectorProperty,
    'FLOAT_TEXTURE' : bpy.props.FloatProperty,
    'ENUM'          : bpy.props.EnumProperty,

    'OUTPUT_COLOR'         : bpy.props.FloatVectorProperty,
    'OUTPUT_TEXTURE'       : bpy.props.FloatVectorProperty,
    'OUTPUT_FLOAT_TEXTURE' : bpy.props.FloatProperty,
}


def callback_match_BI_diffuse(self, context):
    if not hasattr(context, 'material'):
        return

    from bl_ui.properties_material import active_node_mat
    
    material = active_node_mat(context.material)
    
    if not context.material:
        return
    
    if not self.as_viewport_color:
        material.diffuse_color = (0.5, 0.5, 0.5)
        return

    color = self.diffuse if material.vray.type == 'BRDFVRayMtl' else self.color

    material.diffuse_color = color


def GenerateAttribute(dataPointer, attrDesc):   
    attrFunc = TypeToProp[attrDesc['type']]

    attrArgs = {
        'attr'        : attrDesc['attr'],
        'name'        : attrDesc.get('name', attrDesc['attr'].replace("_", " ").title()),
        'description' : attrDesc['desc'],
        'default'     : attrDesc['default'],
    }

    if 'options' in attrDesc:
        attrArgs['options'] = attrDesc['options']

    if attrDesc['type'] in ['COLOR', 'ACOLOR', 'TEXTURE']:
        attrArgs['subtype'] = 'COLOR'
        attrArgs['size']    = len(attrDesc['default'])

    elif attrDesc['type'] in ['FLOAT', 'FLOAT_TEXTURE']:
        defUi = {
            'min' : -1024.0,
            'max' :  1024.0,
            'soft_min' : 0.0,
            'soft_max' : 1.0,
        }

    elif attrDesc['type'] in ['INT', 'INT_TEXTURE']:
        defUi = {
            'min' : -1024,
            'max' :  1024,
            'soft_min' : 0,
            'soft_max' : 8,
        }

    if attrDesc['type'] in ['INT', 'INT_TEXTURE', 'FLOAT', 'FLOAT_TEXTURE']:
        if 'ui' not in attrDesc:
            attrDesc['ui'] = defUi

        attrArgs['min'] = attrDesc['ui'].get('min', defUi['min'])
        attrArgs['max'] = attrDesc['ui'].get('max', defUi['max'])
        attrArgs['soft_min'] = attrDesc['ui'].get('soft_min', defUi['soft_min'])
        attrArgs['soft_max'] = attrDesc['ui'].get('soft_max', defUi['soft_max'])

    setattr(dataPointer, attrDesc['attr'], attrFunc(**attrArgs))

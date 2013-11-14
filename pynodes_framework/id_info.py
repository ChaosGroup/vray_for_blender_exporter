# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy


# List of ID type identifiers
# ( identifier, bpy.types identifier, bpy.data list )
_id_types_map = [
    ('ACTION',               'Action',               'actions'),
    ('ARMATURE',             'Armature',             'armatures'),
    ('BRUSH',                'Brush',                'brushes'),
    ('CAMERA',               'Camera',               'cameras'),
    ('CURVE',                'Curve',                'curves'),
    ('FONT',                 'Font',                 'fonts'),
    ('GREASEPENCIL',         'GreasePencil',         'grease_pencil'),
    ('GROUP',                'Group',                'groups'),
    ('IMAGE',                'Image',                'images'),
    ('KEY',                  'Key',                  None),
    ('LAMP',                 'Lamp',                 'lamps'),
    ('LATTICE',              'Lattice',              'lattices'),
    ('LIBRARY',              'Library',              'libraries'),
    ('LINESTYLE',            'FreestyleLineStyle',   'linestyles'),
    ('MASK',                 'Mask',                 'masks'),
    ('MATERIAL',             'Material',             'materials'),
    ('META',                 'MetaBall',             'metaballs'),
    ('MESH',                 'Mesh',                 'meshes'),
    ('MOVIECLIP',            'MovieClip',            'movieclips'),
    ('NODETREE',             'NodeTree',             'node_groups'),
    ('OBJECT',               'Object',               'objects'),
    ('PARTICLE',             'ParticleSettings',     'particles'),
    ('SCENE',                'Scene',                'scenes'),
    ('SCREEN',               'Screen',               'screens'),
    ('SPEAKER',              'Speaker',              'speakers'),
    ('SOUND',                'Sound',                'sounds'),
    ('TEXT',                 'Text',                 'texts'),
    ('TEXTURE',              'Texture',              'textures'),
    ('WORLD',                'World',                'worlds'),
    ('WINDOWMANAGER',        'WindowManager',        'window_managers'),
]

_id_datalist_map = { identifier : datalist for identifier, _, datalist in _id_types_map }
_id_type_icon_map = { item.identifier : item.icon for item in bpy.types.DriverTarget.bl_rna.properties['id_type'].enum_items }

_id_type_identifier_map = { typename : identifier for identifier, typename, _ in _id_types_map }
def id_type_identifier(id_type):
    return _id_type_identifier_map[id_type.__name__]
def id_data_type_identifier(id_data):
    return _id_type_identifier_map[type(id_data).__name__]

def id_type_icon(id_type):
    return _id_type_icon_map[id_type]

def id_type_list(id_type):
    id_type_id = _id_type_identifier_map[id_type.__name__]
    return _id_datalist_map[id_type_id]
def id_data_type_list(id_data):
    id_type_id = _id_type_identifier_map[type(id_data).__name__]
    return _id_datalist_map[id_type_id]

def get_id_path(p):
    pid = p.id_data
    return(repr(pid))

def get_full_path(p):
    path = get_id_path(p)
    if p != p.id_data:
        path = "%s.%s" % (path, p.path_from_id())
    return path

def get_idtype_list(idtype):
    prop = _id_datalist_map[idtype]
    return lambda: getattr(bpy.data, prop, [])

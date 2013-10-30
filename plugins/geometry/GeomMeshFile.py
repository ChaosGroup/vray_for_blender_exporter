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


TYPE = 'GEOMETRY'
ID   = 'GeomMeshFile'
NAME = 'VRayProxy'
DESC = "VRayProxy geomtery"

PluginParams = (
    {
        'attr' : 'file',
        'desc' : "",
        'type' : 'STRING',
        'subtype' : 'FILE_PATH',
        'default' : "",
    },
    {
        'attr' : 'anim_type',
        'desc' : "Animated proxy playback type",
        'type' : 'ENUM',
        'items' : (
            ('0', "Loop", ""),
            ('1', "Once", ""),
            ('2', "Ping-pong", ""),
            ('3', "Still", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'anim_override',
        'desc' : "Controls if anim_start and anim_length are taken in consideration. Useful only, when the file name contains frame filter",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'anim_speed',
        'desc' : "Animated proxy playback speed",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'anim_offset',
        'desc' : "Animated proxy initial frame offset",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'anim_start',
        'desc' : "Specifies the first frame of the animation sequence",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'anim_length',
        'desc' : "Specifies the length of the animation sequence",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'primary_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'scale',
        'desc' : "Size scaling factor",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'flip_axis',
        'desc' : "Transform the proxy from Y-up to Z-up (and vice versa) coordinate system",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'smooth_uv_borders',
        'desc' : "true to smooth UVs at mesh borders when rendering this mesh as a subdivision surface",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'smooth_uv',
        'desc' : "true to smooth UVs when rendering this mesh as a subdivision surface",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'compute_normals',
        'desc' : "true to calculate smooth normals",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'smooth_angle',
        'desc' : "smooth angle in degrees",
        'type' : 'FLOAT',
        'default' : 30,
    },
    {
        'attr' : 'compute_bbox',
        'desc' : "true to compute the bounding box, false to read it from the file",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'num_preview_faces',
        'desc' : "number of faces in preview",
        'type' : 'INT',
        'default' : 10000,
    },
    {
        'attr' : 'use_face_sets',
        'desc' : "turn on/off face sets",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'use_full_names',
        'desc' : "read the full path instead of only the name",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'object_path',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'hair_width_multiplier',
        'desc' : "Hair width multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'visibility_lists_type',
        'desc' : "Specifies the type of both names and ids lists",
        'type' : 'ENUM',
        'items' : (
            ('0', "Exclude", ""),
            ('1', "Include", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'visibility_list_names',
        'desc' : "Visibility list of mesh names. Either include or exclude",
        'type' : 'LIST',
        'default' : "",
    },
    {
        'attr' : 'visibility_list_ids',
        'desc' : "Visibility list of mesh ids. Either include or exclude",
        'type' : 'INT_LIST',
        'default' : "",
    },
    {
        'attr' : 'hair_visibility_lists_type',
        'desc' : "Specifies the type of both names and ids lists",
        'type' : 'ENUM',
        'items' : (
            ('0', "Exclude", ""),
            ('1', "Include", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'hair_visibility_list_names',
        'desc' : "Visibility list of hair names. Either include or exclude",
        'type' : 'LIST',
        'default' : "",
    },
    {
        'attr' : 'hair_visibility_list_ids',
        'desc' : "Visibility list of hair ids. Either include or exclude",
        'type' : 'INT_LIST',
        'default' : "",
    },

    # Proxy Generator Settings
    #
    {
        'attr' : 'proxy_attach_mode',
        'desc' : "Proxy attach mode",
        'type' : 'ENUM',
        'items' : (
            ('NONE',    "None",        "Don\'t attach proxy"),
            ('NEW',     "New object",  "Attach proxy to new object"),
            ('THIS',    "This object", "Attach proxy to this object"),
            ('REPLACE', "Replace",     "Replace this object with proxy"),
        ),
        'skip' : True,
        'default' : 'NONE'
    },
    {
        'attr' : 'apply_transforms',
        'desc' : "Apply rotation, location and scale",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False
    },
    {
        'attr' : 'add_suffix',
        'name' : "Add suffix",
        'desc' : "Add \"_proxy\" suffix to object and mesh names",
        'type' : 'BOOL',
        'skip' : True,
        'default' : True
    },
    {
        'attr' : 'animation',
        'name' : "Animation",
        'desc' : "Animated proxy",
        'type' : 'BOOL',
        'skip' : True,
        'default' : False
    },
    {
        'attr' : 'dirpath',
        'name' : "Path",
        'subtype' : 'DIR_PATH',
        'desc' : "Proxy generation directory",
        'type' : 'STRING',
        'skip' : True,
        'default' : "//proxy"
    },
    {
        'attr' : 'add_velocity',
        'name' : "Add velocity",
        'desc' : "This makes it possible to add motion blur to the final animation. However exporting this extra information takes longer. If you are not going to need motion blur it makes sense to disable this option",
        'type' : 'BOOL',
        'skip' : True,
        'default' :  False
    },
    {
        'attr' : 'filename',
        'name' : "Name",
        'desc' : "Proxy file name. If empty object's name is used",
        'type' : 'STRING',
        'skip' : True,
        'default' :  ""
    },
    {
        'attr' : 'animation_range',
        'name' : "Animation range",
        'desc' : "Animation range type",
        'type' : 'ENUM',
        'items' : (
            ('MANUAL', "Manual", "Set manually"),
            ('SCENE',  "Scene",  "Get from scene")
        ),
        'skip' : True,
        'default' : 'SCENE'
    },
    {
        'attr' : 'frame_start',
        'name' : "Start Frame",
        'desc' : "Proxy generation start frame",
        'type' : 'INT',
        'ui' : {
            'min'      :  1,
            'soft_min' :  1,
        },
        'skip' : True,
        'default' : 1
    },
    {
        'attr' : 'frame_end',
        'name' : "End Frame",
        'desc' : "Proxy generation end frame",
        'type' : 'INT',
        'ui' : {
            'min'      :  1,
            'soft_min' :  1,
        },
        'skip' : True,
        'default' : 250
    },
)

PluginWidget = """
{ "widgets": [
    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "file" }
        ]
    },
    
    {   "layout" : "SEPARATOR" },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "scale" }
        ]
    },

    {   "layout" : "SEPARATOR" },
    
    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "anim_type", "label" : "Type" },
                    { "name" : "anim_override", "label" : "Override" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "active" : {
                    "prop" : "anim_override",
                    "condition" : true
                },
                "attrs" : [
                    { "name" : "anim_speed", "label" : "Speed" },
                    { "name" : "anim_offset", "label" : "Offset" },
                    { "name" : "anim_start", "label" : "Start" },
                    { "name" : "anim_length", "label" : "Length" }
                ]
            }
        ]
    },

    {   "layout" : "SPLIT",
        "splits" : [
            {   "layout" : "COLUMN",
                "attrs" : [
                    { "name" : "flip_axis" },
                    { "name" : "compute_bbox" },
                    { "name" : "smooth_uv" },
                    { "name" : "smooth_uv_borders" }
                ]
            },
            {   "layout" : "COLUMN",
                "align" : true,
                "attrs" : [
                    { "name" : "compute_normals" },
                    { "name" : "smooth_angle",
                      "label" : "Angle",
                      "active" : { "prop" : "compute_normals" }
                    }
                ]
            }
        ]
    },

    {   "layout" : "ROW",
        "attrs" : [
            { "name" : "primary_visibility" }
        ]
    }
]}
"""

def nodeDraw(context, layout, GeomMeshFile):
    layout.prop(GeomMeshFile, 'file')
    layout.operator('vray.proxy_load_preview', icon='OUTLINER_OB_MESH', text="Load Preview Mesh")

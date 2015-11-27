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


TYPE = 'OBJECT'
ID   = 'VRayClipper'
NAME = 'Clipper'
DESC = "Clipper settings"


PluginParams = (
    {
        'attr' : 'enabled',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'affect_light',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'only_camera_rays',
        'desc' : "The clipper will affect objects as they are directly seen by the camera, but they will appear unchanged to reflection/refraction/GI rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'clip_lights',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'use_obj_mtl',
        'name' : "Use Object Material",
        'desc' : "When enabled, the clipper will use the material of each clipped object to fill in the resulting holes. When this is off, the material applied to the clipper object itself will be used",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'set_material_id',
        'name' : 'Set Material ID',
        'desc' : "When enabled, you can specify a face material ID for the clipper object",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'material_id',
        'name' : "Material ID",
        'desc' : "The face material ID for the clipped surfaces when \"Set material\" ID is enabled",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'exclusion_mode',
        'desc' : "Exclusion Mode",
        'type' : 'ENUM',
        'items' : (
            ('0', "Include", ""),
            ('1', "Exclude", ""),
        ),
        'default' : '1',
    },
    {
        'attr' : 'exclusion_nodes',
        'desc' : "List of node plugins to consider for inclusion/exclusion",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'transform',
        'desc' : "",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'material',
        'desc' : "",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'object_id',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
)

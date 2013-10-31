#
# V-Ray For Blender
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

TYPE = 'SETTINGS'
ID   = 'SettingsVFB'
NAME = 'SettingsVFB'
DESC = ""

PluginParams = (
    {
        'attr' : 'bloom_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bloom_fill_edges',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'bloom_weight',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 20,
    },
    {
        'attr' : 'bloom_size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 20,
    },
    {
        'attr' : 'bloom_shape',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 4,
    },
    {
        'attr' : 'bloom_mode',
        'desc' : "0-image 1-image and buffer  2-buffer",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'bloom_mask_intensity_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bloom_mask_intensity',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 3,
    },
    {
        'attr' : 'bloom_mask_objid_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bloom_mask_objid',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'bloom_mask_mtlid_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'bloom_mask_mtlid',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'glare_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_fill_edges',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'glare_weight',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 50,
    },
    {
        'attr' : 'glare_size',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 20,
    },
    {
        'attr' : 'glare_type',
        'desc' : "0- from image  1 - from render camera  2 - from camera params",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'glare_mode',
        'desc' : "0-image 1-image and buffer  2-buffer",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'glare_image_path',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'glare_obstacle_image_path',
        'desc' : "",
        'type' : 'STRING',
        'default' : "",
    },
    {
        'attr' : 'glare_diffraction_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_use_obstacle_image',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_cam_blades_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'glare_cam_num_blades',
        'desc' : "",
        'type' : 'INT',
        'default' : 6,
    },
    {
        'attr' : 'glare_cam_rotation',
        'desc' : "Rotation in degrees from 0.0 - 360.0",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'glare_cam_fnumber',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 8,
    },
    {
        'attr' : 'glare_mask_intensity_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_mask_intensity',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 3,
    },
    {
        'attr' : 'glare_mask_objid_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_mask_objid',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'glare_mask_mtlid_on',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'glare_mask_mtlid',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'interactive',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
)

PluginWidget = """
{ "widgets": [
]}
"""
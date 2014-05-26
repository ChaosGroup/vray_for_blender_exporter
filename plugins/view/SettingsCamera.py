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

from vb30.lib import ExportUtils


TYPE = 'CAMERA'
ID   = 'SettingsCamera'
NAME = 'Camera'
DESC = ""

PluginParams = (
    {
        'attr' : 'type',
        'desc' : "Camera typ",
        'type' : 'ENUM',
        'items' : (
            ('0', "Default", ""),
            ('1', "Spherifical", ""),
            ('2', "Cylindrical (Point)", ""),
            ('3', "Cylindrical (Ortho)", ""),
            ('4', "Box", ""),
            ('5', "Fish-Eye", ""),
            ('6', "Warped Spherical", ""),
            ('7', "Orthogonal", ""),
            ('8', "Pinhole", ""),
        ),
        'default' : '0',
    },
    {
        'attr' : 'height',
        'desc' : "Height of the cylindrical (ortho) camera",
        'type' : 'FLOAT',
        'default' : 400,
    },
    {
        'attr' : 'dist',
        'desc' : "Applies only to fish-eye camera. Controls distance to the sphere center",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'fov',
        'desc' : "Field of view; if negative, the field of view will not be modified",
        'type' : 'FLOAT',
        'default' : 0.785398,
    },
    {
        'attr' : 'auto_fit',
        'desc' : "The auto-fit option of the fish-eye camera",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'curve',
        'desc' : "Controls the way the rendered images is warped. Applies only to fish-eye camera",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'dont_affect_settings',
        'desc' : "This is here so we can suppress a SettingsCamera node from affecting the main VRayRenderer sequence and frame data",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'image_planes',
        'desc' : "Used only to force a re-export of the image plane geometry in RT rendering",
        'type' : 'PLUGIN',
        'default' : "",
    },
)

PluginWidget = """
{ "widgets": [
]}
"""


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    ca = bus['camera']

    VRayCamera = ca.data.vray
    
    cameraType = propGroup.type
    if ca.data.type == 'ORTHO':
        cameraType = 7
    else:
        # We must set camera type to "pinhole" to make the physical camera match the fov
        if VRayCamera.CameraPhysical:
            cameraType = 8

    overrideParams.update({
        'fov'    : -1,
        'type'   : cameraType,
        'height' : ca.data.ortho_scale,
    })

    return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)

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

from . import tools as NodesTools


def AddMaterialNodeTree(ma):
    VRayMaterial = ma.vray

    if VRayMaterial.ntree:
        VRayMaterial.ntree = VRayMaterial.ntree.copy()

    else:
        nt = bpy.data.node_groups.new(ma.name, type='VRayNodeTreeMaterial')
        nt.use_fake_user = True

        outputNode = nt.nodes.new('VRayNodeOutputMaterial')

        singleMaterial = nt.nodes.new('VRayNodeMtlSingleBRDF')
        singleMaterial.location.x  = outputNode.location.x - 250
        singleMaterial.location.y += 50

        brdfVRayMtl = nt.nodes.new('VRayNodeBRDFVRayMtl')
        brdfVRayMtl.location.x  = singleMaterial.location.x - 250
        brdfVRayMtl.location.y += 100

        nt.links.new(brdfVRayMtl.outputs['BRDF'], singleMaterial.inputs['BRDF'])

        nt.links.new(singleMaterial.outputs['Material'], outputNode.inputs['Material'])

        VRayMaterial.ntree = nt

    NodesTools.deselectNodes(VRayMaterial.ntree)

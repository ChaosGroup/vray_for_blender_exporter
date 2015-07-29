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

from vb30.lib import LibUtils

from . import tools as NodesTools


def AddWorldNodeTree(world):
    VRayWorld = world.vray

    nt = bpy.data.node_groups.new("World", type='VRayNodeTreeWorld')
    nt.use_fake_user = True

    outputNode = nt.nodes.new('VRayNodeWorldOutput')
    envNode = nt.nodes.new('VRayNodeEnvironment')

    envNode.location.x = outputNode.location.x - 200
    envNode.location.y = outputNode.location.y + 200

    nt.links.new(envNode.outputs['Environment'], outputNode.inputs['Environment'])

    NodesTools.deselectNodes(nt)

    VRayWorld.ntree = nt


def AddLampNodeTree(lamp):
    VRayLight = lamp.vray

    nt = bpy.data.node_groups.new(lamp.name, type='VRayNodeTreeLight')
    nt.use_fake_user = True

    lightPluginName = LibUtils.GetLightPluginName(lamp)

    nt.nodes.new('VRayNode%s' % lightPluginName)
    NodesTools.deselectNodes(nt)

    VRayLight.ntree = nt


def AddSceneNodeTree(sce):
    VRayScene = sce.vray

    nt = bpy.data.node_groups.new(sce.name, type='VRayNodeTreeScene')
    nt.use_fake_user = True

    nt.nodes.new('VRayNodeRenderChannels')
    NodesTools.deselectNodes(nt)

    VRayScene.ntree = nt


def AddObjectNodeTree(ob):
    VRayObject = ob.vray

    nt = bpy.data.node_groups.new(ob.name, type='VRayNodeTreeObject')
    nt.use_fake_user = True

    outputNode = nt.nodes.new('VRayNodeObjectOutput')

    blenderGeometry = nt.nodes.new('VRayNodeBlenderOutputGeometry')
    blenderMaterial = nt.nodes.new('VRayNodeBlenderOutputMaterial')

    blenderMaterial.location.x = outputNode.location.x - 200
    blenderMaterial.location.y = outputNode.location.y + 30

    blenderGeometry.location.x = outputNode.location.x - 200
    blenderGeometry.location.y = outputNode.location.y - 150

    nt.links.new(blenderMaterial.outputs['Material'], outputNode.inputs['Material'])
    nt.links.new(blenderGeometry.outputs['Geometry'], outputNode.inputs['Geometry'])

    NodesTools.deselectNodes(nt)

    VRayObject.ntree = nt


def AddMaterialNodeTree(ma):
    VRayMaterial = ma.vray

    if VRayMaterial.ntree:
        VRayMaterial.ntree = VRayMaterial.ntree.copy()

    else:
        nt = bpy.data.node_groups.new(ma.name, type='VRayNodeTreeMaterial')
        nt.use_fake_user = True

        outputNode = nt.nodes.new('VRayNodeOutputMaterial')

        meta_node = nt.nodes.new('VRayNodeMetaStandardMaterial')
        meta_node.location.x  = outputNode.location.x - 250
        meta_node.location.y += 50
        meta_node.width = 185

        nt.links.new(meta_node.outputs['Material'], outputNode.inputs['Material'])

        VRayMaterial.ntree = nt

    NodesTools.deselectNodes(VRayMaterial.ntree)

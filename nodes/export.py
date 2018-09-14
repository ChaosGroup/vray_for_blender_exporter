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
import mathutils

from vb30.lib     import ExportUtils, LibUtils
from vb30.plugins import PLUGINS
from vb30         import debug

from .utils import *


##     ## ######## #### ##       #### ######## #### ########  ######
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##
##     ##    ##     ##  ##        ##     ##     ##  ######    ######
##     ##    ##     ##  ##        ##     ##     ##  ##             ##
##     ##    ##     ##  ##        ##     ##     ##  ##       ##    ##
 #######     ##    #### ######## ####    ##    #### ########  ######

def GetOutputNode(ntree):
    NtreeToOutputNodeType = {
        'VRayNodeTreeScene'    : 'VRayNodeRenderChannels',
        'VRayNodeTreeWorld'    : 'VRayNodeEnvironment',
        'VRayNodeTreeMaterial' : 'VRayNodeOutputMaterial',
        'VRayNodeTreeObject'   : 'VRayNodeObjectOutput',
        'VRayNodeTreeLight'    : 'VRayNodeTreeLight',
    }

    outputNodeType = NtreeToOutputNodeType.get(ntree.bl_idname)
    if not outputNodeType:
        return None

    return GetNodeByType(ntree, outputNodeType)


######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##

def WriteConnectedNode(_unused_, nodetree, nodeSocket):
    connectedNode = GetConnectedNode(nodetree, nodeSocket)
    if connectedNode:
        return _vray_for_blender.exportNode(
            nodetree.as_pointer(),
            connectedNode.as_pointer(),
            nodeSocket.as_pointer()
        )

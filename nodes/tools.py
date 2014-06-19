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

from .utils import GetConnectedNode


NODE_LEVEL_WIDTH = 200.0


def getNodeHeight(n):
    socketHeigth = 25
    return n.height + socketHeigth * (len(n.inputs) + len(n.outputs))


def collectLeafs(tree, ntree, n, depth):
    for inSock in n.inputs:
        if inSock.is_linked:
            inNode = GetConnectedNode(ntree, inSock)
            if not depth in tree:
                tree[depth] = []
            tree[depth].append(inNode)
            tree = collectLeafs(tree, ntree, inNode, depth+1)
    return tree


def rearrangeTree(ntree, n, depth=0):
    tree = {
        depth : [n],
    }

    tree = collectLeafs(tree, ntree, n, depth+1)

    # pprint(tree)

    for level in sorted(tree):
        if level == 0:
            continue

        levelNodes = tree[level]
        levelHeigth = 0

        # Calculate full level height
        for node in levelNodes:
            levelHeigth += getNodeHeight(node)

        levelTop        = levelHeigth
        levelHeightHalf = levelHeigth / 2.0

        for node in levelNodes:
            node.location.x = n.location.x - (level * NODE_LEVEL_WIDTH)

            node.location.y = levelTop - levelHeightHalf

            levelTop -= getNodeHeight(node)

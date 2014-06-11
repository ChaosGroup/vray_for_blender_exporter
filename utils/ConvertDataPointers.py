# This script will convert node based scene
# to the new pointers location
#

import bpy


for nt in bpy.data.node_groups:
    for n in nt.nodes:
        if not hasattr(n, 'texture'):
            continue
        if not n.texture:
            continue
        n.tex = n.texture
        n.tex.use_fake_user = False
        n.texture = None

for ma in bpy.data.materials:
    if ma.vray.ntree:
        ma.node_tree = ma.vray.ntree
        ma.node_tree.use_fake_user = False

for la in bpy.data.lamps:
    if la.vray.ntree:
        la.node_tree = la.vray.ntree
        la.node_tree.use_fake_user = False
        la.vray.ntree = None

for ob in bpy.context.scene.objects:
    if ob.vray.ntree:
        ob.node_tree = ob.vray.ntree
        ob.node_tree.use_fake_user = False
        ob.vray.ntree = None

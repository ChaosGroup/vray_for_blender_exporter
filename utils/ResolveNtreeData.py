import bpy


def ResovleNtreeData():
    texPrefix = {
        'VRayNodeTexGradRamp'  : ".Ramp_",
        'VRayNodeTexRemap'     : ".Ramp_",
        'VRayNodeBitmapBuffer' : ".Bitmap_",
    }

    for ma in bpy.data.materials:
        maName = ma.name
        if ma.vray.ntree:
            continue
        if maName in bpy.data.node_groups:
            ma.vray.ntree = bpy.data.node_groups[maName]

    for ob in bpy.context.scene.objects:
        obName = ob.name
        if ob.vray.ntree:
            continue
        if obName in bpy.data.node_groups:
            ob.vray.ntree = bpy.data.node_groups[obName]

    for nt in bpy.data.node_groups:
        for n in nt.nodes:
            if not hasattr(n, 'texture'):
                continue
            if n.texture:
                continue

            texName = texPrefix[n.bl_idname] + n.name

            if texName in bpy.data.textures:
                n.texture = bpy.data.textures[texName]


if __name__ == '__main__':
    ResovleNtreeData()

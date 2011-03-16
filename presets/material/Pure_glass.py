import bpy

def active_node_material(ma):
	ma_node= ma.active_node_material
	if ma_node:
		return ma_node
	else:
		return ma

ma= active_node_material(bpy.context.active_object.active_material)

ma.diffuse_color = 0.0,0.0,0.0

VRayMaterial= ma.vray
VRayMaterial.type= 'BRDFVRayMtl'

BRDFVRayMtl= VRayMaterial.BRDFVRayMtl

BRDFVRayMtl.fog_color= 1.0,1.0,1.0
BRDFVRayMtl.refract_color= 1.0,1.0,1.0
BRDFVRayMtl.refract_ior= 1.55
BRDFVRayMtl.refract_affect_shadows= True
BRDFVRayMtl.reflect_color= 0.95,0.95,0.95
BRDFVRayMtl.fresnel= True

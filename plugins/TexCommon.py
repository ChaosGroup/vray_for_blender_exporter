'''

  V-Ray/Blender 2.5

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *
from vb25.ui.ui import *


TYPE= 'TEXTURE'
ID=   'TexCommon'

NAME= 'Common texture setings'
DESC= "Common V-Ray Texture settings."

PARAMS= (
)


def add_properties(rna_pointer):
	rna_pointer.name= StringProperty(
		name= "V-Ray Texture name",
		description= "V-Ray texture name for internal usage.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

	rna_pointer.texture_coords= EnumProperty(
		name= "Coords",
		description= "Image texure placement type.",
		items= (
			('ORCO', "Object", "Generated coordinates."),
			('UV',   "UV",     "Mesh UV coordinates."),
		),
		default= 'UV'
	)

	rna_pointer.mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('FLAT',   "Flat",        "Planar projection."),
			('CUBE',   "Cube",        "Cubic projection."),
			('SPHERE', "Sphere",      "Spherical projection."),
			('TUBE',   "Tube",        "Cylindrical projection."),
			('BALL',   "Ball",        "Ball projection."),
			('TRI',    "Triplanar",   "Triplanar projection."),
			('PERS',   "Perspective", "Perspective projection."),
		),
		default= 'FLAT'
	)

	rna_pointer.environment_mapping= EnumProperty(
		name= "Projection",
		description= "Generated projection type.",
		items= (
			('SCREEN',  "Screen",      "Planar projection."),
			('CUBIC',   "Cube",        "Cubic projection."),
			('SPHERE',  "Sphere",      "Spherical projection."),
			('TUBE',    "Tube",        "Cylindrical projection."),
			('ANGULAR', "Angular",     "Angular projection."),
			('MBALL',   "Mirror ball", "Mirror ball projection."),
		),
		default= 'SPHERE'
	)

	rna_pointer.object= StringProperty(
		name= "Mapping Object",
		description= "Object to use for mapping generation.",
		subtype= 'NONE',
		options= {'HIDDEN'},
		default= ""
	)

	rna_pointer.tile= EnumProperty(
		name= "Tile",
		description= "Tile type.",
		items= (
			('NOTILE', "No tile", "No tiling."),
			('TILEUV', "Tile UV", "Tile in UV."),
			('TILEU',  "Tile U",  "Tile in U."),
			('TILEV',  "Tile V",  "Tile in V."),
		),
		default= 'TILEUV'
	)

	# use_3d_mapping
	rna_pointer.use_3d_mapping= BoolProperty(
		name= "Use 3D mapping",
		description= "Use 3D mapping.",
		default= True
	)

	# wrap
	rna_pointer.wrap= BoolProperty(
		name= "Wrap",
		description= "TODO: Tooltip.",
		default= True
	)

	# alpha_from_intensity
	rna_pointer.alpha_from_intensity= BoolProperty(
		name= "Alpha from intensity",
		description= "If true, the resulting alpha is the color intensity; otherwise the alpha is taken from the bitmap alpha.",
		default= False
	)

	# invert
	rna_pointer.invert= BoolProperty(
		name= "Invert",
		description= "If true, the resulting texture color will be inverted.",
		default= False
	)

	# invert_alpha
	rna_pointer.invert_alpha= BoolProperty(
		name= "Invert alpha",
		description= "If true and invert is on, the resulting texture alpha will be inverted too. If false, just the color will be inverted.",
		default= True
	)
	
	# color_mult
	rna_pointer.color_mult= FloatVectorProperty(
		name= "color mult",
		description= "A multiplier for the texture color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (1,1,1)
	)

	# color_offset
	rna_pointer.color_offset= FloatVectorProperty(
		name= "color offset",
		description= "An additional offset for the texture color.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0,0,0)
	)

	# alpha_mult
	rna_pointer.alpha_mult= FloatProperty(
		name= "alpha mult",
		description= "A multiplier for the texture alpha.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)
	
	# alpha_offset
	rna_pointer.alpha_offset= FloatProperty(
		name= "alpha offset",
		description= "An additional offset for the texture alpha.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# nouvw_color
	rna_pointer.nouvw_color= FloatVectorProperty(
		name= "nouvw color",
		description= "The color when there are no valid uvw coordinates.",
		subtype= 'COLOR',
		min= 0.0,
		max= 1.0,
		soft_min= 0.0,
		soft_max= 1.0,
		default= (0.5,0.5,0.5)
	)

	# uvwgen
	rna_pointer.uvwgen= StringProperty(
		name= "UVW generator",
		description= "UVW generator.",
		default= ""
	)

	# placement_type
	rna_pointer.placement_type= EnumProperty(
		name= "Placement type",
		description= "Image texure placement type.",
		items= (
			('FULL', "Full",  "The whole texture is valid."),
			('CROP', "Crop",  "Crop texture."),
			('PLACE',"Place", "Place texture."),
		),
		default= 'FULL'
	)

	# u
	rna_pointer.u= FloatProperty(
		name= "U",
		description= "U coordinate of the valid texture sector.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# v
	rna_pointer.v= FloatProperty(
		name= "V",
		description= "V coordinate of the valid texture sector.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# w
	rna_pointer.w= FloatProperty(
		name= "W",
		description= "Width of the valid texture sector.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# h
	rna_pointer.h= FloatProperty(
		name= "H",
		description= "Height of the valid texture sector.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# jitter
	rna_pointer.jitter= FloatProperty(
		name= "Jitter",
		description= "Amount of random placement variation.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)

	# tile_u
	rna_pointer.tile_u= IntProperty(
		name= "Tile U",
		description= "If true there is horizontal tiling.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)
	
	# tile_v
	rna_pointer.tile_v= IntProperty(
		name= "Tile V",
		description= "If true there is vertical tiling.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# uv_noise_on
	rna_pointer.uv_noise_on= BoolProperty(
		name= "Use",
		description= "If true the noise is enabled.",
		default= 0
	)
	
	# uv_noise_animate
	rna_pointer.uv_noise_animate= IntProperty(
		name= "Animate",
		description= "If true the noise is animated.",
		min= 0,
		max= 100,
		soft_min= 0,
		soft_max= 10,
		default= 0
	)

	# uv_noise_amount
	rna_pointer.uv_noise_amount= FloatProperty(
		name= "Amount",
		description= "UV noise amount.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# uv_noise_levels
	rna_pointer.uv_noise_levels= FloatProperty(
		name= "Levels",
		description= "UV noise iterations.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# uv_noise_size
	rna_pointer.uv_noise_size= FloatProperty(
		name= "Size",
		description= "UV noise size.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	# un_noise_phase
	rna_pointer.un_noise_phase= FloatProperty(
		name= "Phase",
		description= "UV noise phase.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 0
	)



'''
  OUTPUT
'''
def write(bus):
	PLACEMENT_TYPE= {
		'FULL':  0,
		'CROP':  1,
		'PLACE': 2,
	}
	TILE= {
		'NOTILE': 0,
		'TILEUV': 1,
		'TILEU':  2,
		'TILEV':  3,
	}

	ofile= bus['files']['textures']
	scene= bus['scene']

	slot=    bus['mtex']['slot']
	texture= bus['mtex']['texture']

	VRayTexture= texture.vray
	VRaySlot=    texture.vray_slot

	ofile.write("\n\tplacement_type= %i;" % PLACEMENT_TYPE[VRayTexture.placement_type])
	ofile.write("\n\ttile_u= %d;" % VRayTexture.tile_u)
	ofile.write("\n\ttile_v= %d;" % VRayTexture.tile_v)
	ofile.write("\n\tu= %s;" % a(scene, VRayTexture.u))
	ofile.write("\n\tv= %s;" % a(scene, VRayTexture.v))
	ofile.write("\n\tw= %s;" % a(scene, VRayTexture.w))
	ofile.write("\n\th= %s;" % a(scene, VRayTexture.h))
	ofile.write("\n\tjitter= %s;" % a(scene, VRayTexture.jitter))
	ofile.write("\n\tinvert= %s;" % a(scene, VRayTexture.invert))
	ofile.write("\n\tinvert_alpha= %s;" % a(scene, VRayTexture.invert_alpha))
	ofile.write("\n\talpha_from_intensity= %s;" % a(scene, VRayTexture.alpha_from_intensity))
	ofile.write("\n\tuv_noise_on= %s;" % a(scene, VRayTexture.uv_noise_on))
	ofile.write("\n\tuv_noise_animate= %s;" % a(scene, VRayTexture.uv_noise_animate))
	ofile.write("\n\tun_noise_phase= %s;" % a(scene, VRayTexture.un_noise_phase))
	ofile.write("\n\tuv_noise_amount= %s;" % a(scene, VRayTexture.uv_noise_amount))
	ofile.write("\n\tuv_noise_levels= %s;" % a(scene, VRayTexture.uv_noise_levels))
	ofile.write("\n\tuv_noise_size= %s;" % a(scene, VRayTexture.uv_noise_size))
	# ofile.write("\n\t= %s;" % a(scene, VRayTexture.))

	if hasattr(VRayTexture, VRayTexture.type):
		TexPlugin= getattr(VRayTexture, VRayTexture.type)

		if hasattr(TexPlugin, 'wrap'):
			ofile.write("\n\twrap= %s;" % a(scene, VRayTexture.wrap))

		if hasattr(TexPlugin, 'use_3d_mapping'):
			ofile.write("\n\tuse_3d_mapping= %s;" % a(scene, VRayTexture.use_3d_mapping))


class VRAY_OT_bake_procedural(bpy.types.Operator):
	bl_idname=      'vray.bake_procedural'
	bl_label=       "Bake procedural"
	bl_description= "Render procedural texture to file."

	def execute(self, context):
		debug(context.scene, "Bake procedural: In progress...")
		return {'FINISHED'}

bpy.utils.register_class(VRAY_OT_bake_procedural)


class VRAY_TP_Common(VRayTexturePanel, bpy.types.Panel):
	bl_label       = "Common"
	COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		tex= context.texture
		return tex and tex.type == 'VRAY' and tex.vray.type != 'NONE' and engine_poll(cls, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		tex= context.texture

		VRayTexture= tex.vray

		TexPlugin= getattr(VRayTexture, VRayTexture.type)

		layout.prop(VRayTexture, 'placement_type', expand= True)

		if VRayTexture.placement_type not in ('FULL'):
			split= layout.split()
			col= split.column(align= True)
			col.prop(VRayTexture, 'u')
			col.prop(VRayTexture, 'v')
			if wide_ui:
				col= split.column(align= True)
			col.prop(VRayTexture, 'w')
			col.prop(VRayTexture, 'h')

		layout.separator()

		split= layout.split()
		row= split.row(align= True)
		row.prop(VRayTexture, 'tile_u')
		row.prop(VRayTexture, 'tile_v')

		split= layout.split()
		col= split.column()
		col.prop(VRayTexture, 'jitter')

		layout.separator()

		split= layout.split()
		col= split.column()
		col.prop(VRayTexture, 'invert')
		sub= col.column()
		sub.active= VRayTexture.invert
		sub.prop(VRayTexture, 'invert_alpha')
		col.prop(VRayTexture, 'alpha_from_intensity')
		if wide_ui:
			col= split.column()
		if hasattr(TexPlugin, 'use_3d_mapping'):
			col.prop(VRayTexture, 'use_3d_mapping')
		if hasattr(TexPlugin, 'wrap'):
			col.prop(VRayTexture, 'wrap')

		layout.separator()

		box= layout.box()
		box.prop(VRayTexture, 'uv_noise_on', text= "UV noise")
		split= box.split()
		split.active= VRayTexture.uv_noise_on
		col= split.column()
		col.prop(VRayTexture, 'uv_noise_animate')
		col.prop(VRayTexture, 'un_noise_phase')
		if wide_ui:
			col= split.column()
		col.prop(VRayTexture, 'uv_noise_amount')
		col.prop(VRayTexture, 'uv_noise_levels')
		col.prop(VRayTexture, 'uv_noise_size')

		# split= layout.split()
		# col= split.column()
		# col.prop(VRayTexture, 'color_mult')
		# col.prop(VRayTexture, 'color_offset')
		# if wide_ui:
		# 	col= split.column()
		# col.prop(VRayTexture, 'alpha_mult')
		# col.prop(VRayTexture, 'alpha_offset')
		# col.prop(VRayTexture, 'nouvw_color')

		layout.separator()
		layout.operator("vray.bake_procedural", icon= 'TEXTURE')


bpy.utils.register_class(VRAY_TP_Common)



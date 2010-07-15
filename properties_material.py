'''

 V-Ray/Blender

 http://vray.cgdo.ru

 Started:       29 Aug 2009
 Last Modified: 10 Mar 2010

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''

import os
import bpy


FloatProperty= bpy.types.Material.FloatProperty
IntProperty= bpy.types.Material.IntProperty
BoolProperty= bpy.types.Material.BoolProperty
EnumProperty= bpy.types.Material.EnumProperty
VectorProperty= bpy.types.Material.FloatVectorProperty



'''
  BRDFVRayMtl
'''
VectorProperty(
	attr="vray_fog_color",
	name="Fog color",
	description="Fog color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(1.0, 1.0, 1.0)
)

VectorProperty(
	attr="vray_refract_color",
	name="Refraction color",
	description="Refraction color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

VectorProperty(
	attr="vray_reflect_color",
	name="Reflection color",
	description="Reflection color.",
	subtype="COLOR",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default=(0.0, 0.0, 0.0)
)

BoolProperty(	attr="vray_fresnel",
				name="Frensnel reflections",
				description="Enable frensnel reflections.",
				default= False)

BoolProperty(	attr="vray_fresnel_ior_lock",
				name="Frensnel reflections lock",
				description="",
				default= True)

FloatProperty(  attr="vray_fresnel_ior",
				name="Fresnel IOR",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=10.0, default= 1.6)

FloatProperty(  attr="vray_roughness",
				name="Roughness",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_hilightGlossiness",
				name="Hilight gloss",
				description="",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 1.0)

BoolProperty(	attr="vray_hilightGlossiness_lock",
				name="Hilight glossiness lock",
				description="",
				default= True)

BoolProperty(	attr="vray_double_sided",
				name="Double-sided",
				description="",
				default= True)

BoolProperty(	attr="vray_back_side",
				name="Reflect on back side",
				description="",
				default= False)

BoolProperty(	attr="vray_affect_shadows",
				name="Affect shadows",
				description="",
				default= False)

BoolProperty(	attr="vray_trace_refractions",
				name="Trace refractions",
				description="",
				default= True)

BoolProperty(	attr="vray_trace_reflections",
				name="Trace reflections",
				description="",
				default= True)

BoolProperty(	attr="vray_affect_alpha",
				name="Affect alpha",
				description="",
				default= False)

FloatProperty(  attr="vray_fog_color_mult",
				name="Fog multiplier",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 0.1)

FloatProperty(  attr="vray_fog_bias",
				name="Fog bias",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_fog_ior",
				name="Fog bias",
				description="",
				min=0.0, max=10.0, soft_min=0.0, soft_max=1.0, default= 1.0)

FloatProperty(  attr="vray_anisotropy",
				name="Anisotropy",
				description="",
				min=-1.0, max=1.0, soft_min=-1.0, soft_max=1.0, default= 0.0)

FloatProperty(  attr="vray_anisotropy_rotation",
				name="Rotation",
				description="Anisotropy rotation",
				min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default= 0.0)

EnumProperty(   attr="vray_brdf",
				name="BRDF",
				description="This determines the type of BRDF (the shape of the hilight).",
				items=(("PHONG", "Phong", "Phong hilight/reflections."),
					   ("BLINN", "Blinn", "Blinn hilight/reflections."),
					   ("WARD", "Ward",  "Ward hilight/reflections.")),
				default= "BLINN")


BoolProperty( 
	attr= "vray_mtl_emitOnBackSide", 
	name= "Emit on back side", 
	description= 'TODO.', 
	default= False
)


BoolProperty( 
	attr= "vray_mtl_compensateExposure", 
	name= "Compensate camera exposure", 
	description= 'TODO.', 
	default= False
)




'''
  BRDFSSS2Complex
'''
IntProperty( 
	attr= "vray_fsss_prepass_rate",
	name= "Prepass rate", 
	description= "Sampling density for the illumination map.", 
	min= -10, 
	max=  10, 
	default= -1
)

FloatProperty(
	attr= "vray_fsss_interpolation_accuracy", 
	name= "Interpolation accuracy", 
	description= "Interpolation accuracy for the illumination map; normally 1.0 is fine.", 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

FloatProperty(
	attr= "vray_fsss_scale", 
	name= "Scale", 
	description= "Values below 1.0 will make the object look as if it is bigger. Values above 1.0 will make it look as if it is smalle.", 
	min= 0.0, 
	max= 1000.0, 
	soft_min= 0.0, 
	soft_max= 1000.0, 
	precision= 4, 
	default= 1
)

FloatProperty(
	attr= "vray_fsss_ior", 
	name= "IOR", 
	description= 'TODO.', 
	min= 0.0, 
	max= 10.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.5
)

FloatProperty(
	attr= "vray_fsss_diffuse_amount", 
	name= "Diffuse amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 0.0
)

FloatProperty(
	attr= "vray_fsss_scatter_radius_mult", 
	name= "Scatter radius", 
	description= 'TODO.', 
	min= 0.0, 
	max= 100.0, 
	soft_min= 0.0, 
	soft_max= 10.0, 
	precision= 3, 
	default= 1.0
)

VectorProperty( 
	attr= "vray_fsss_overall_color", 
	name= "Overall color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1, 1, 1)
)

VectorProperty( 
	attr= "vray_fsss_diffuse_color", 
	name= "Diffuse color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

VectorProperty( 
	attr= "vray_fsss_sub_surface_color", 
	name= "Sub surface color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.5, 0.5, 0.5)
)

VectorProperty( 
	attr= "vray_fsss_scatter_radius", 
	name= "Scatter radius", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (0.92, 0.52, 0.175)
)

FloatProperty(
	attr= "vray_fsss_phase_function", 
	name= "Phase function", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0
)

VectorProperty( 
	attr= "vray_fsss_specular_color", 
	name= "Specular color", 
	description= 'TODO.', 
	subtype= "COLOR", 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	default= (1, 1, 1)
)

IntProperty( 
	attr= "vray_fsss_specular_subdivs", 
	name= "Specular subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

FloatProperty(
	attr= "vray_fsss_specular_amount", 
	name= "Specular amount", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 1
)

FloatProperty(
	attr= "vray_fsss_specular_glossiness", 
	name= "Specular glossiness", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.6
)

FloatProperty(
	attr= "vray_fsss_cutoff_threshold", 
	name= "Cutoff threshold", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.01
)

BoolProperty( 
	attr= "vray_fsss_trace_reflections", 
	name= "Trace reflections", 
	description= 'TODO.', 
	default= False
)

IntProperty( 
	attr= "vray_fsss_reflection_depth", 
	name= "Reflection depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

EnumProperty(
	attr="vray_fsss_single_scatter",
	name="Single scatter",
	description= 'TODO.', 
	items=(("NONE",   "None", ""),
		   ("SIMPLE", "Simple", ""),
		   ("SOLID",  "Raytraced (solid)", ""),
		   ("REFR",   "Raytraced (refractive)",  "")),
	default= "SIMPLE"
)

IntProperty( 
	attr= "vray_fsss_subdivs", 
	name= "Subdivs", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 8
)

IntProperty( 
	attr= "vray_fsss_refraction_depth", 
	name= "Refraction depth", 
	description= 'TODO.', 
	min= 0, 
	max= 10, 
	default= 5
)

BoolProperty( 
	attr= "vray_fsss_front_scatter", 
	name= "Front scatter", 
	description= 'TODO.', 
	default= True
)

BoolProperty( 
	attr= "vray_fsss_back_scatter", 
	name= "Back scatter", 
	description= 'TODO.', 
	default= True
)

BoolProperty( 
	attr= "vray_fsss_scatter_gi", 
	name= "Scatter gi", 
	description= 'TODO.', 
	default= False
)

FloatProperty(
	attr= "vray_fsss_prepass_blur", 
	name= "Prepass blur", 
	description= 'TODO.', 
	min= 0.0, 
	max= 1.0, 
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1.2
)



'''
  Material
'''
EnumProperty(
	attr='vray_mtl_emitter',
	name='Emitter type',
	description='This determines the type of BRDF (the shape of the hilight).',
	items=(('MTL',  'Material',   ''),
		   ('MESH', 'Mesh light',  '')),
	default= 'MTL'
)

EnumProperty(
	attr= 'vray_mtl_type',
	name= 'Type',
	description= 'Material type.',
	items=(
		('MTL',  'Basic', 'Basic V-Ray material.'),
		('SSS',  'SSS',   'Fast SSS material.'),
		('EMIT', 'Light', 'Light emitting material.')
	),
	default= 'MTL'
)

BoolProperty(
	attr='vray_mtl_two_sided',
	name='Two sided material',
	description='Simple \'Two sided\' material. Use nodes for advanced control.',
	default= False
)

FloatProperty(
	attr= 'vray_mtlts_translucency',
	name= 'Translucency',
	description= 'Translucency between front and back.',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0, 
	soft_max= 1.0, 
	precision= 3, 
	default= 0.5
)



'''
  Presets
'''
SSS2= {
	'Skin_brown': {
		'ior':                  1.3,
		'diffuse_color':        (169, 123, 92),
		'sub_surface_color':    (169, 123, 92),
		'scatter_radius':       (155, 94, 66),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Skin_pink': {
		'ior':                  1.3,
		'diffuse_color':        (203, 169, 149),
		'sub_surface_color':    (203, 169, 149),
		'scatter_radius':       (177, 105, 84),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Skin_yellow': {
		'ior':                  1.3,
		'diffuse_color':        (204, 165, 133),
		'sub_surface_color':    (204, 165, 133),
		'scatter_radius':       (177, 105, 84),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.5
	},
	'Milk_skimmed': {
		'ior':                  1.3,
		'diffuse_color':        (230, 230, 210),
		'sub_surface_color':    (230, 230, 210),
		'scatter_radius':       (245, 184, 107),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Milk_whole': {
		'ior':                  1.3,
		'diffuse_color':        (242, 239, 222),
		'sub_surface_color':    (242, 239, 222),
		'scatter_radius':       (188, 146,  90),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.9,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Marble_white': {
		'ior':                  1.5,
		'diffuse_color':        (238, 233, 228),
		'sub_surface_color':    (238, 233, 228),
		'scatter_radius':       (235, 190, 160),
		'scatter_radius_mult':  1.0,
		'phase_function':       -0.25,
		'specular_amount':      1.0,
		'specular_glossiness':  0.7
	},
	'Ketchup': {
		'ior':                  1.3,
		'diffuse_color':        (102, 28,  0),
		'sub_surface_color':    (102, 28,  0),
		'scatter_radius':       (176, 62, 50),
		'scatter_radius_mult':  1.0,
		'phase_function':       0.9,
		'specular_amount':      1.0,
		'specular_glossiness':  0.7
	},
	'Cream': {
		'ior':                  1.3,
		'diffuse_color':        (224, 201, 117),
		'sub_surface_color':    (224, 201, 117),
		'scatter_radius':       (215, 153,  81),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.6
	},
	'Potato': {
		'ior':                  1.3,
		'diffuse_color':        (224, 201, 117),
		'sub_surface_color':    (224, 201, 117),
		'scatter_radius':       (215, 153,  81),
		'scatter_radius_mult':  2.0,
		'phase_function':       0.8,
		'specular_amount':      1.0,
		'specular_glossiness':  0.8
	},
	'Spectration': {
		'ior':                  1.5,
		'diffuse_color':        (255, 255, 255),
		'sub_surface_color':    (255, 255, 255),
		'scatter_radius':       (  0,   0,   0),
		'scatter_radius_mult':  0.0,
		'phase_function':       0.0,
		'specular_amount':      0.0,
		'specular_glossiness':  0.0
	},
	'Water_clear': {
		'ior':                  1.3,
		'diffuse_color':        (  0,   0,   0),
		'sub_surface_color':    (  0,   0,   0),
		'scatter_radius':       (255, 255, 255),
		'scatter_radius_mult':  300.0,
		'phase_function':       0.95,
		'specular_amount':      1.0,
		'specular_glossiness':  1.0
	}
}

# def generate_preset():
# 	for preset in SSS2:
# 		ofile= open("/home/bdancer/devel/vrayblender/exporter/2.5/presets/sss/%s.py"%(preset), 'w')
# 		for param in SSS2[preset]:
# 			ps= SSS2[preset][param]
# 			if type(ps) == tuple:
# 				pss= ""
# 				for c in ps:
# 					pss+= "%.3f,"%(float(c / 255.0))
# 				ps= pss[:-1]
# 			s= "bpy.context.active_object.active_material.%s = %s\n"%("vray_fsss_%s"%(param), ps)
# 			ofile.write(s.replace(')','').replace('(',''))
# 		ofile.write('\n')
# 		ofile.close()
#generate_preset()


def active_node_mat(mat):
    if mat:
        mat_node= mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat
    return None



'''
  GUI
'''


narrowui= 200


class MATERIAL_MT_fsss_presets(bpy.types.Menu):
	bl_label= "SSS Presets"
	preset_subdir= os.path.join("..", "io", "vb25", "presets", "sss")
	preset_operator = "script.execute_preset"
	draw = bpy.types.Menu.draw_preset


class MaterialButtonsPanel(bpy.types.Panel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'material'

	def poll(self, context):
		engine = context.scene.render.engine
		return (context.material) and (engine in self.COMPAT_ENGINES)


class MATERIAL_PT_vray_context_material(MaterialButtonsPanel):
	bl_label = ""
	bl_show_header = False

	COMPAT_ENGINES = {'VRAY_RENDER'}

	def poll(self, context):
		engine = context.scene.render.engine
		return (context.material or context.object) and (engine in self.COMPAT_ENGINES)

	def draw(self, context):
		layout = self.layout

		mat= active_node_mat(context.material)
		ob= context.object
		slot= context.material_slot
		space= context.space_data
		wide_ui= context.region.width > narrowui

		if ob:
			row = layout.row()
			row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
			col = row.column(align=True)
			col.operator("object.material_slot_add", icon='ZOOMIN', text="")
			col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")
			col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")
			if ob.mode == 'EDIT':
				row = layout.row(align=True)
				row.operator("object.material_slot_assign", text="Assign")
				row.operator("object.material_slot_select", text="Select")
				row.operator("object.material_slot_deselect", text="Deselect")

		if wide_ui:
			split = layout.split(percentage=0.65)

			if ob:
				split.template_ID(ob, "active_material", new="material.new")
				row = split.row()
				if slot:
					row.prop(slot, "link", text="")
				else:
					row.label()
			elif mat:
				split.template_ID(space, "pin_id")
				split.separator()
		else:
			if ob:
				layout.template_ID(ob, "active_material", new="material.new")
			elif mat:
				layout.template_ID(space, "pin_id")

		if mat:
			layout.prop(mat, "vray_mtl_type", expand=True)


class MATERIAL_PT_vray_preview(MaterialButtonsPanel):
	bl_label = "Preview"
	bl_default_closed = False
	bl_show_header = False

	COMPAT_ENGINES= set(['VRAY_RENDER'])

	def draw(self, context):
		self.layout.template_preview(context.material)


class MATERIAL_PT_vray_basic(MaterialButtonsPanel):
	bl_label = 'Parameters'
	bl_default_closed = False
	bl_show_header = True

	COMPAT_ENGINES= set(['VRAY_RENDER'])

	def draw(self, context):
		layout= self.layout

		ob= context.object
		mat= active_node_mat(context.material)
		sce= context.scene
		wide_ui= context.region.width > narrowui

		if(mat.vray_mtl_type == 'MTL'):
			raym= mat.raytrace_mirror
			rayt= mat.raytrace_transparency

			row= layout.row()
			colL= row.column()
			colL.label(text="Diffuse")

			row= layout.row()
			colL= row.column()
			colR= row.column()
			colL.prop(mat, "diffuse_color", text="")

			colL.prop(mat, "vray_roughness")
			colR.prop(mat, "alpha")

			row= layout.row()
			colL= row.column()
			colL.label(text="Reflection")

			row= layout.row()
			colL= row.column(align=True)
			colL.prop(mat, "vray_reflect_color", text="")
			if(not mat.vray_hilightGlossiness_lock):
				colL.prop(mat, "vray_hilightGlossiness", slider=True)
			colL.prop(raym, "gloss_factor", text="Reflection gloss")
			colL.prop(raym, "gloss_samples", text="Subdivs")
			colL.prop(raym, "depth")
			colL.prop(raym, "gloss_threshold", text="Cutoff", slider=False)
			colR= row.column()
			colR.prop(mat, "vray_brdf", text="")
			colR.prop(mat, "vray_hilightGlossiness_lock")

			if(not mat.vray_brdf == 'PHONG'):
				colR.prop(mat, "vray_anisotropy")
				colR.prop(mat, "vray_anisotropy_rotation")
			colR.prop(mat, "vray_fresnel")
			if mat.vray_fresnel:
				colR.prop(mat, "vray_fresnel_ior")

			row= layout.row()
			colL= row.column()
			colL.label(text="Refraction")
			colR= row.column()
			colR.label(text="Fog")

			row= layout.row()
			colL= row.column(align=True)
			colL.prop(mat, "vray_refract_color", text="")
			colL.prop(rayt, "ior")
			colL.prop(rayt, "gloss_factor", text="Glossiness")
			colL.prop(rayt, "gloss_samples", text="Subdivs")
			colL.prop(rayt, "depth")
			colL.prop(rayt, "gloss_threshold", text="Cutoff", slider=False)

			colR= row.column(align=True)
			colR.prop(mat, "vray_fog_color", text="")
			colR.prop(mat, "vray_fog_color_mult")
			colR.prop(mat, "vray_fog_bias")
			colR.label(text="")
			colR.prop(mat, "vray_affect_alpha")
			colR.prop(mat, "vray_affect_shadows")

			row= layout.row()
			colL= row.column()
			colL.label(text="Options")

			row= layout.row()
			colL= row.column()
			colL.prop(mat, "vray_trace_reflections")
			colL.prop(mat, "vray_trace_refractions")
			colR= row.column()
			colR.prop(mat, "vray_double_sided")
			colR.prop(mat, "vray_back_side")

			row= layout.row()
			colL= row.column()
			colL.label(text="Advanced")

			row= layout.row()
			colL= row.column()
			colR= row.column()

			colL.prop(mat, "vray_mtl_two_sided")
			if(mat.vray_mtl_two_sided):
				colR.prop(mat, "vray_mtlts_translucency", slider=True)

		elif(mat.vray_mtl_type == 'EMIT'):
			row= layout.row()
			colL= row.column()
			colL.label(text="Color")

			row= layout.row()
			col= row.column()
			col.prop(mat, "diffuse_color", text="")
			if wide_ui:
				col= row.column()
			col.prop(mat, "alpha")

			row= layout.row()
			colL= row.column()
			colL.label(text="Emitter")

			row= layout.row()
			col= row.column()
			col.prop(mat, "vray_mtl_emitter", text="Type")
			if wide_ui:
				col= row.column()
			if not mat.vray_mtl_emitter == 'MESH':
				col.prop(mat, "emit", text="Intensity")

			if(mat.vray_mtl_emitter == 'MESH'):
				if(sce.vray_export_compat == 'DEMO'):
					row= layout.row()
					col= row.column()
					col.label(text='Mesh light is only available in V-Ray Standalone :(')
				else:
					split= layout.split()
					col= split.column()
					col.prop(ob, 'vray_lamp_portal_mode', text="Mode")
					if(ob.vray_lamp_portal_mode == 'NORMAL'):
						col.prop(ob, 'vray_lamp_units', text="Units")
						col.prop(ob, 'vray_lamp_intensity', text="Intensity")
					col.prop(ob, 'vray_lamp_subdivs')

					if wide_ui:
						col= split.column()
					col.prop(ob, 'vray_lamp_invisible')
					col.prop(ob, 'vray_lamp_affectDiffuse')
					col.prop(ob, 'vray_lamp_affectSpecular')
					col.prop(ob, 'vray_lamp_affectReflections')
					col.prop(ob, 'vray_lamp_noDecay')

					col.prop(ob, 'vray_lamp_doubleSided')
					col.prop(ob, 'vray_lamp_storeWithIrradianceMap')

					ob.vray_node_meshlight= True
			else:
				ob.vray_node_meshlight= False
				
				row= layout.row()
				colL= row.column()
				colL.prop(mat, "vray_mtl_emitOnBackSide")
				colL.prop(mat, "vray_mtl_compensateExposure")

		else: # SSS
			if(sce.vray_export_compat == 'STD'):
				row= layout.row()
				col= row.column()
				col.label(text='General')

				row= layout.row()
				col= row.column()
				col.menu("MATERIAL_MT_fsss_presets", text="Presets")

				row= layout.row()
				colL= row.column()
				colR= row.column()

				colL.prop(mat, 'vray_fsss_prepass_rate')
				colL.prop(mat, 'vray_fsss_scale')
				colR.prop(mat, 'vray_fsss_ior')
				colR.prop(mat, 'vray_fsss_interpolation_accuracy', text='Accuracy')


				row= layout.row()
				col= row.column()
				col.label(text='')


				row= layout.row()
				col= row.column()
				col.label(text='Overall color')
				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_overall_color', text='')
				col= row.column()
				col.prop(mat, 'vray_fsss_phase_function')

				row= layout.row()
				col= row.column()
				col.label(text='Diffuse color')
				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_diffuse_color', text='')
				col= row.column()
				col.prop(mat, 'vray_fsss_diffuse_amount')

				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_sub_surface_color')
				col= row.column()
				col.label(text='')

				row= layout.row()
				col= row.column()
				col.label(text='Scatter color')
				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_scatter_radius', text='')
				col= row.column()
				col.prop(mat, 'vray_fsss_scatter_radius_mult')


				row= layout.row()
				col= row.column()
				col.label(text='')


				row= layout.row()
				col= row.column()
				col.label(text='Specular layer')

				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_specular_color', text='')
				col.prop(mat, 'vray_fsss_specular_subdivs', text='Subdivs')
				col= row.column()
				col.prop(mat, 'vray_fsss_specular_amount', text='Amount')
				col.prop(mat, 'vray_fsss_specular_glossiness', text='Glossiness')

				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_trace_reflections')
				if(mat.vray_fsss_trace_reflections):
					col= row.column()
					col.prop(mat, 'vray_fsss_reflection_depth')


				row= layout.row()
				col= row.column()
				col.label(text='')


				row= layout.row()
				col= row.column()
				col.label(text='Options')
				row= layout.row()
				col= row.column()
				col.prop(mat, 'vray_fsss_single_scatter', text='Type')
				col.prop(mat, 'vray_fsss_subdivs')
				col.prop(mat, 'vray_fsss_refraction_depth')
				col.prop(mat, 'vray_fsss_cutoff_threshold')
				col= row.column()
				col.prop(mat, 'vray_fsss_front_scatter')
				col.prop(mat, 'vray_fsss_back_scatter')
				col.prop(mat, 'vray_fsss_scatter_gi')
				col.prop(mat, 'vray_fsss_prepass_blur')
			else:
				row= layout.row()
				col= row.column()
				col.label(text='Only available in V-Ray Standalone :(')


bpy.types.register(MATERIAL_MT_fsss_presets)
bpy.types.register(MATERIAL_PT_vray_context_material)
bpy.types.register(MATERIAL_PT_vray_preview)
bpy.types.register(MATERIAL_PT_vray_basic)


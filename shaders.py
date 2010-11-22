'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

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

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Blender modules '''
import bpy

''' vb modules '''
from vb25.utils import *


def write_TexFresnel(ofile, sce, ma, ma_name, tex_vray):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {"%(tex_name))
	if(tex_vray["reflect"]):
		ofile.write("\n\tblack_color= %s;"%(tex_vray["reflect"]))
	else:
		ofile.write("\n\tblack_color= %s;"%(a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior)))
	ofile.write("\n}\n")

	return tex_name


def write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray):
	rm= ma.raytrace_mirror

	brdf_name= "BRDFMirror_%s"%(ma_name)

	ofile.write("\nBRDFMirror %s {"%(brdf_name))
	if(tex_vray['color']):
		ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	if(tex_vray['reflect']):
		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tback_side= %d;"%(ma.vray_back_side))
	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
	ofile.write("\n\ttrace_depth= %i;"%(rm.depth))
	ofile.write("\n\tcutoff= %.6f;"%(0.01))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray):
	rm= ma.raytrace_mirror

	brdf_name= "BRDFGlossy_%s"%(ma_name)

	if(ma.vray_brdf == 'PHONG'):
		ofile.write("\nBRDFPhong %s {"%(brdf_name))
	elif(ma.vray_brdf == 'WARD'):
		ofile.write("\nBRDFWard %s {"%(brdf_name))
	else:
		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_reflect_color)))))
	ofile.write("\n\tsubdivs= %i;"%(rm.gloss_samples))

	if(tex_vray['reflect']):
		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(
			1.0 - ma.vray_reflect_color[0],
			1.0 - ma.vray_reflect_color[1],
			1.0 - ma.vray_reflect_color[2]))))

	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,rm.gloss_factor)))
	ofile.write("\n\thilightGlossiness= %s;"%(a(sce,ma.vray_hilightGlossiness)))
	if(tex_vray['reflect_glossiness']):
		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['reflect_glossiness'])))
	if(tex_vray['hilight_glossiness']):
		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['hilight_glossiness'])))
	ofile.write("\n\tback_side= %s;"%(a(sce,ma.vray_back_side)))
	ofile.write("\n\ttrace_reflections= %s;"%(p(ma.vray_trace_reflections)))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rm.depth)))
	if(not ma.vray_brdf == 'PHONG'):
		ofile.write("\n\tanisotropy= %s;"%(a(sce,ma.vray_anisotropy)))
		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,ma.vray_anisotropy_rotation)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,rm.gloss_threshold)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlass_%s"%(ma_name)

	ofile.write("\nBRDFGlass %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlassGlossy_%s"%(ma_name)

	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tglossiness= %s;"%(a(sce,rt.gloss_factor)))
	ofile.write("\n\tsubdivs= %i;"%(rt.gloss_samples))
	ofile.write("\n\tior= %s;"%(a(sce,rt.ior)))
	ofile.write("\n\taffect_shadows= %d;"%(ma.vray_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(ma.vray_trace_refractions))
	ofile.write("\n\ttrace_depth= %s;"%(a(sce,rt.depth)))
	ofile.write("\n\tcutoff= %s;"%(a(sce,0.001)))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray):
	brdf_name= "BRDFDiffuse_%s"%(ma_name)

	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	ofile.write("\n\troughness= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(ma.vray_roughness,ma.vray_roughness,ma.vray_roughness))))
	if(tex_vray['color']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['color']))
	ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency_tex= %s;"%(a(sce,tex_vray['alpha'])))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDF(ofile, sce, ma, ma_name, tex_vray):
	def bool_color(color, level):
		for c in color:
			if c > level:
				return True
		return False

	rm= ma.raytrace_mirror
	rt= ma.raytrace_transparency

	brdfs= []

	if(tex_vray['reflect']):
		tex_vray['reflect']= write_TexInvert(tex_vray['reflect'])

	if(ma.vray_fresnel):
		tex_vray['reflect']= write_TexFresnel(ofile, sce, ma, ma_name, tex_vray)

	if(tex_vray['reflect'] or bool_color(ma.vray_reflect_color, 0.0)):
		if(rm.gloss_factor < 1.0 or tex_vray['reflect_glossiness']):
			brdf_name= write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray)
		brdfs.append(brdf_name)

	if(tex_vray['refract'] or bool_color(ma.vray_refract_color, 0.0)):
		if(rt.gloss_factor < 1.0 or tex_vray['refract_glossiness']):
			brdf_name= write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray)
	else:
		brdf_name= write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray)
	brdfs.append(brdf_name)

	if(len(brdfs) == 1):
		brdf_name= brdfs[0]
	else:
		brdf_name= "BRDFLayered_%s"%(ma_name)

		ofile.write("\nBRDFLayered %s {"%(brdf_name))
		ofile.write("\n\tbrdfs= List(")
		brdfs_out= ""
		for brdf in brdfs:
			brdfs_out+= "\n\t\t%s,"%(brdf)
		ofile.write(brdfs_out[0:-1])
		ofile.write("\n\t);")
		ofile.write("\n\tadditive_mode= %s;"%(0)); # For shellac
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))
		if(tex_vray['alpha']):
			ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['alpha']))
		ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFGlossy_%s"%(ma_name)

	if BRDFVRayMtl.brdf_type == 'PHONG':
		ofile.write("\nBRDFPhong %s {"%(brdf_name))
	elif BRDFVRayMtl.brdf_type == 'WARD':
		ofile.write("\nBRDFWard %s {"%(brdf_name))
	else:
		ofile.write("\nBRDFBlinn %s {"%(brdf_name))

	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	ofile.write("\n\tsubdivs= %i;"%(BRDFVRayMtl.reflect_subdivs))

	if tex_vray['reflect']:
		ofile.write("\n\ttransparency= Color(1.0,1.0,1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))

	ofile.write("\n\treflectionGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	if BRDFVRayMtl.hilight_glossiness_lock:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.reflect_glossiness)))
	else:
		ofile.write("\n\thilightGlossiness= %s;"%(a(sce,BRDFVRayMtl.hilight_glossiness)))
	if tex_vray['reflect_glossiness']:
		ofile.write("\n\treflectionGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['reflect_glossiness'])))
	if tex_vray['hilight_glossiness']:
		ofile.write("\n\thilightGlossiness_tex= %s;"%("%s::out_intensity"%(tex_vray['hilight_glossiness'])))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	if BRDFVRayMtl.brdf_type != 'PHONG':
		ofile.write("\n\tanisotropy= %s;"%(a(sce,BRDFVRayMtl.anisotropy)))
		ofile.write("\n\tanisotropy_rotation= %s;"%(a(sce,BRDFVRayMtl.anisotropy_rotation)))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFMirror_%s"%(ma_name)

	ofile.write("\nBRDFMirror %s {"%(brdf_name))
	if tex_vray['color']:
		ofile.write("\n\tcolor= %s;"%(tex_vray['color']))
	else:
		ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.reflect_color)))))
	if tex_vray['reflect']:
		ofile.write("\n\ttransparency= Color(1.0, 1.0, 1.0);")
		ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['reflect']))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple([1.0 - c for c in BRDFVRayMtl.reflect_color])))))
	ofile.write("\n\tback_side= %d;"%(BRDFVRayMtl.option_reflect_on_back))
	ofile.write("\n\ttrace_reflections= %s;"%(p(BRDFVRayMtl.reflect_trace)))
	ofile.write("\n\ttrace_depth= %i;"%(BRDFVRayMtl.reflect_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdf_name= "BRDFGlass_%s"%(ma_name)

	ofile.write("\nBRDFGlass %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(BRDFVRayMtl.refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tior= %s;"%(a(sce,BRDFVRayMtl.refract_ior)))
	ofile.write("\n\taffect_shadows= %d;"%(BRDFVRayMtl.refract_affect_shadows))
	ofile.write("\n\taffect_alpha= %d;"%(BRDFVRayMtl.refract_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(BRDFVRayMtl.refract_trace))
	ofile.write("\n\ttrace_depth= %s;"%(BRDFVRayMtl.refract_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray):
	rt= ma.raytrace_transparency

	brdf_name= "BRDFGlassGlossy_%s"%(ma_name)

	ofile.write("\nBRDFGlassGlossy %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f,%.6f,%.6f)"%(tuple(ma.vray_refract_color)))))
	if(tex_vray['refract']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['refract']))
	ofile.write("\n\tglossiness= %s;"%(a(sce,BRDFVRayMtl.refract_glossiness)))
	ofile.write("\n\tsubdivs= %i;"%(BRDFVRayMtl.refract_subdivs))
	ofile.write("\n\tior= %s;"%(a(sce,BRDFVRayMtl.refract_ior)))
	ofile.write("\n\taffect_shadows= %d;"%(BRDFVRayMtl.refract_affect_shadows))
	ofile.write("\n\taffect_alpha= %d;"%(BRDFVRayMtl.refract_affect_alpha))
	ofile.write("\n\ttrace_refractions= %d;"%(BRDFVRayMtl.refract_trace))
	ofile.write("\n\ttrace_depth= %s;"%(BRDFVRayMtl.refract_depth))
	ofile.write("\n\tcutoff= %.6f;"%(BRDFVRayMtl.option_cutoff))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDFLight(ofile, sce, ma, ma_name, tex_vray):
	brdf_name= "BRDFLight_%s"%(ma_name)

	if(tex_vray['color']):
		color= tex_vray['color']
	else:
		color= "Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color))

	if(tex_vray['alpha']):
		alpha= write_TexInvert(ofile, sce,tex_vray['alpha'])
		color= write_TexCompMax(ofile, sce,"%s_alpha"%(brdf_name), alpha, color)

	light= ma.vray.BRDFLight

	ofile.write("\nBRDFLight %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,color)))
	ofile.write("\n\tcolorMultiplier= %s;"%(a(sce,ma.emit * 10)))
	ofile.write("\n\tcompensateExposure= %s;"%(a(sce,light.compensateExposure)))
	ofile.write("\n\temitOnBackSide= %s;"%(a(sce,light.emitOnBackSide)))
	ofile.write("\n\tdoubleSided= %s;"%(a(sce,light.doubleSided)))

	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency= %s;"%(a(sce,tex_vray['alpha'])))
	else:
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(1.0 - ma.alpha, 1.0 - ma.alpha, 1.0 - ma.alpha))))

	ofile.write("\n}\n")

	return brdf_name


def write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray):
	BRDFVRayMtl= ma.vray.BRDFVRayMtl
		
	brdf_name= "BRDFDiffuse_%s"%(ma_name)

	ofile.write("\nBRDFDiffuse %s {"%(brdf_name))
	ofile.write("\n\tcolor= %s;"%(a(sce,"Color(%.6f, %.6f, %.6f)"%(tuple(ma.diffuse_color)))))
	ofile.write("\n\troughness= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(BRDFVRayMtl.roughness))))
	if(tex_vray['color']):
		ofile.write("\n\tcolor_tex= %s;"%(tex_vray['color']))
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha))))
	if(tex_vray['alpha']):
		ofile.write("\n\ttransparency_tex= %s;"%(a(sce,tex_vray['alpha'])))
	ofile.write("\n}\n")

	return brdf_name


def write_BRDF(ofile, sce, ma, ma_name, tex_vray):
	def bool_color(color):
		for c in color:
			if c > 0.0:
				return True
		return False

	BRDFVRayMtl= ma.vray.BRDFVRayMtl

	brdfs= []

	if tex_vray['reflect']:
		tex_vray['reflect']= write_TexInvert(tex_vray['reflect'])

	if tex_vray['reflect'] or bool_color(BRDFVRayMtl.reflect_color):
		if BRDFVRayMtl.reflect_glossiness < 1.0 or tex_vray['reflect_glossiness']:
			brdf_name= write_BRDFGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFMirror(ofile, sce, ma, ma_name, tex_vray)
		brdfs.append(brdf_name)

	if tex_vray['refract'] or bool_color(BRDFVRayMtl.refract_color):
		if BRDFVRayMtl.refract_glossiness < 1.0 or tex_vray['refract_glossiness']:
			brdf_name= write_BRDFGlassGlossy(ofile, sce, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFGlass(ofile, sce, ma, ma_name, tex_vray)
	else:
		brdf_name= write_BRDFDiffuse(ofile, sce, ma, ma_name, tex_vray)
	brdfs.append(brdf_name)

	if len(brdfs) == 1:
		brdf_name= brdfs[0]
	else:
		brdf_name= "BRDFLayered_%s"%(ma_name)
		ofile.write("\nBRDFLayered %s {"%(brdf_name))
		ofile.write("\n\tbrdfs= List(%s);"%(','.join(brdfs)))
		ofile.write("\n\ttransparency= %s;"%(a(sce,"Color(1.0,1.0,1.0)*%.6f"%(1.0 - ma.alpha))))
		if tex_vray['alpha']:
			ofile.write("\n\ttransparency_tex= %s;"%(tex_vray['alpha']))
		ofile.write("\n}\n")

	return brdf_name

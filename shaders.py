def write_TexFresnel(ofile, ma, ma_name, tex_vray):
	tex_name= "TexFresnel_%s"%(ma_name)

	ofile.write("\nTexFresnel %s {"%(tex_name))
	if(tex_vray["reflect"]):
		ofile.write("\n\tblack_color= %s;"%(tex_vray["reflect"]))
	else:
		ofile.write("\n\tblack_color= %s;"%(a(sce,"AColor(%.6f, %.6f, %.6f, 1.0)"%(tuple([1.0 - c for c in ma.vray_reflect_color])))))
	ofile.write("\n\tfresnel_ior= %s;"%(a(sce,ma.vray_fresnel_ior)))
	ofile.write("\n}\n")

	return tex_name


def write_BRDFMirror(ofile, ma, ma_name, tex_vray):
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


def write_BRDFGlossy(ofile, ma, ma_name, tex_vray):
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


def write_BRDFGlass(ofile, ma, ma_name, tex_vray):
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


def write_BRDFGlassGlossy(ofile, ma, ma_name, tex_vray):
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


def write_BRDFDiffuse(ofile, ma, ma_name, tex_vray):
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


def write_BRDF(ofile, ma, ma_name, tex_vray):
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
		tex_vray['reflect']= write_TexFresnel(ofile, ma, ma_name, tex_vray)

	if(tex_vray['reflect'] or bool_color(ma.vray_reflect_color, 0.0)):
		if(rm.gloss_factor < 1.0 or tex_vray['reflect_glossiness']):
			brdf_name= write_BRDFGlossy(ofile, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFMirror(ofile, ma, ma_name, tex_vray)
		brdfs.append(brdf_name)

	if(tex_vray['refract'] or bool_color(ma.vray_refract_color, 0.0)):
		if(rt.gloss_factor < 1.0 or tex_vray['refract_glossiness']):
			brdf_name= write_BRDFGlassGlossy(ofile, ma, ma_name, tex_vray)
		else:
			brdf_name= write_BRDFGlass(ofile, ma, ma_name, tex_vray)
	else:
		brdf_name= write_BRDFDiffuse(ofile, ma, ma_name, tex_vray)
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

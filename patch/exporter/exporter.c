#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "BKE_main.h"
#include "BKE_scene.h"
#include "BKE_context.h"
#include "BKE_utildefines.h"
#include "BKE_library.h"
#include "BKE_DerivedMesh.h"
#include "BKE_fcurve.h"
#include "BKE_animsys.h"

#include "BKE_global.h"
#include "BKE_report.h"
#include "BKE_object.h"
#include "BKE_mesh.h"
#include "BKE_curve.h"
#include "BKE_bvhutils.h"

#include "BKE_customdata.h"
#include "BKE_anim.h"
#include "BKE_depsgraph.h"
#include "BKE_displist.h"
#include "BKE_font.h"
#include "BKE_mball.h"

#include "DNA_scene_types.h"
#include "DNA_object_types.h"
#include "DNA_meshdata_types.h"
#include "DNA_mesh_types.h"
#include "DNA_image_types.h"
#include "DNA_material_types.h"
#include "DNA_texture_types.h"
#include "DNA_camera_types.h"
#include "DNA_lamp_types.h"
#include "DNA_anim_types.h"
#include "DNA_action_types.h"
#include "DNA_curve_types.h"
#include "DNA_armature_types.h"
#include "DNA_modifier_types.h"

#include "BLI_fileops.h"
#include "BLI_listbase.h"
#include "BLI_math.h"
#include "BLI_path_util.h"
#include "BLI_string.h"

#include "RNA_access.h"

#include "MEM_guardedalloc.h"

#include "exporter.h"


#define TYPE_UV 5


char *clean_string(char *str)
{
    char *tmp_str;
    int i;

    tmp_str= (char*)malloc(MAX_IDPROP_NAME * sizeof(char));

    strncpy(tmp_str, str, MAX_IDPROP_NAME);

    for(i= 0; i < strlen(str); i++) {
        if(tmp_str[i]) {
            if(tmp_str[i] == '+')
                tmp_str[i]= 'p';
            else if(tmp_str[i] == '-')
                tmp_str[i]= 'm';
            else if(!((tmp_str[i] >= 'A' && tmp_str[i] <= 'Z') || (tmp_str[i] >= 'a' && tmp_str[i] <= 'z') || (tmp_str[i] >= '0' && tmp_str[i] <= '9')))
                tmp_str[i]= '_';
        }
    }
    
    return tmp_str;
}



void write_mesh_vray(FILE *gfile, Scene *sce, Object *ob, Mesh *mesh)
{
    Mesh   *me= ob->data;
    MFace  *face;
    MVert  *vert;

    CustomData *fdata;

    int    verts;
    int    fve[4];
	float *ve[4];
	float  no[3];

    int hasUV= 0;
    int maxLayer= 0;

    char *lib_file= (char*)malloc(FILE_MAX * sizeof(char));
    
    const int ft[6]= {0,1,2,2,3,0};

    unsigned long int ev= 0;

    int i, j, f, k, l;
    int u, u0;


    //printf("V-Ray/Blender: Processing object: %s\n", ob->id.name+2);
    //printf("  Mesh: %s\n", me->id.name+2);


    // Name format: Geom_<meshname>_<libname>
    fprintf(gfile,"GeomStaticMesh Geom_%s", clean_string(me->id.name+2));
    if(me->id.lib) {
        BLI_split_dirfile(me->id.lib->name+2, NULL, lib_file);
        fprintf(gfile,"_%s", clean_string(lib_file));

        printf("    Lib: %s\n", me->id.lib->name+2);
        printf("      File: %s\n", lib_file);
    }
    fprintf(gfile," {\n");


    fprintf(gfile,"\tvertices= interpolate((%d, ListVector(", sce->r.cfra);
    vert= mesh->mvert;
    for(f= 0; f < mesh->totvert; ++vert, ++f) {
        if(f) fprintf(gfile,",");
        fprintf(gfile,"Vector(%.6f,%.6f,%.6f)", vert->co[0], vert->co[1], vert->co[2]);
    }
    fprintf(gfile,")));\n");


    fprintf(gfile,"\tfaces= interpolate((%d, ListInt(", sce->r.cfra);
    face= mesh->mface;
    for(f= 0; f < mesh->totface; ++face, ++f) {
        if(f) fprintf(gfile,",");
        if(face->v4)
            fprintf(gfile,"%d,%d,%d,%d,%d,%d", face->v1, face->v2, face->v3, face->v3, face->v4, face->v1);
        else
            fprintf(gfile,"%d,%d,%d", face->v1, face->v2, face->v3);
    }
    fprintf(gfile,")));\n");


    fprintf(gfile,"\tnormals= interpolate((%d, ListVector(", sce->r.cfra);
    face= mesh->mface;
    for(f= 0; f < mesh->totface; ++face, ++f) {
        if(f) fprintf(gfile,",");

        fve[0]= face->v1;
        fve[1]= face->v2;
        fve[2]= face->v3;
        fve[3]= face->v4;
               
        // Get face normal
        for(i= 0; i < 3; i++)
            ve[i]= mesh->mvert[fve[i]].co;
        if(face->v4) {
            ve[3]= mesh->mvert[fve[3]].co;
            normal_quad_v3(no, ve[0], ve[1], ve[2], ve[3]);
        } else
            normal_tri_v3(no, ve[0], ve[1], ve[2]);
                
        if(face->v4) {
            for(i= 0; i < 6; i++) {
                if(i) fprintf(gfile,",");

                // If face is smooth get vertex normal
                if(face->flag & ME_SMOOTH)
                    for(j= 0; j < 3; j++)
                        no[j]= (float)(mesh->mvert[fve[ft[i]]].no[j]/32767.0);

                fprintf(gfile,"Vector(%.6f,%.6f,%.6f)", no[0],no[1],no[2]);
            }
        } else {
            for(i= 0; i < 3; i++) {
                if(i) fprintf(gfile,",");

                // If face is smooth get vertex normal
                if(face->flag & ME_SMOOTH)
                    for(j= 0; j < 3; j++)
                        no[j]= (float)(mesh->mvert[fve[i]].no[j]/32767.0);

                fprintf(gfile,"Vector(%.6f,%.6f,%.6f)", no[0],no[1],no[2]);
            }
        }
    }
    fprintf(gfile,")));\n");


    fprintf(gfile,"\tfaceNormals= interpolate((%d, ListInt(", sce->r.cfra);
    face= mesh->mface;
    k= 0;
    for(f= 0; f < mesh->totface; ++face, ++f) {
        if(f) fprintf(gfile,",");
        
        if(mesh->mface[f].v4)
            verts= 6;
        else
            verts= 3;

        for(i= 0; i < verts; i++) {
            if(i) fprintf(gfile,",");
            fprintf(gfile,"%d", k++);
        }
    }
    fprintf(gfile,")));\n");


    fprintf(gfile,"\tface_mtlIDs= ListInt(");
    face= mesh->mface;
    for(f= 0; f < mesh->totface; ++face, ++f) {
        if(f) fprintf(gfile,",");
        if(face->v4)
            fprintf(gfile,"%d,%d", face->mat_nr, face->mat_nr);
        else
            fprintf(gfile,"%d", face->mat_nr);
    }
    fprintf(gfile,");\n");


    fprintf(gfile,"\tedge_visibility= ListInt(");
    ev= 0;
	if(mesh->totface <= 5) {
        face= mesh->mface;
        for(f= 0; f < mesh->totface; ++face, ++f) {
            if(face->v4) {
                ev= (ev << 6) | 27;
            } else {
                ev= (ev << 3) | 7;
            }
        }
        fprintf(gfile,"%lu", ev);
    } else {
        k= 0;
        face= mesh->mface;
        for(f= 0; f < mesh->totface; ++face, ++f) {
            if(face->v4) {
                ev= (ev << 6) | 27;
                k+= 2;
            } else {
                ev= (ev << 3) | 7;
                k+= 1;
            }
            if(k == 10) {
                fprintf(gfile,"%lu", ev);
                if(f < mesh->totface - 1)
                    fprintf(gfile,",");
                ev= 0;
                k= 0;
            }
        }

        if(k) {
            fprintf(gfile,"%lu", ev);
        }
    }
    fprintf(gfile,");\n");


    fdata= &mesh->fdata;

    hasUV= 0;
    maxLayer= 0;
    for(l= 1; l < fdata->totlayer; ++l) {
        if(fdata->layers[l].type == TYPE_UV) {
            hasUV= 1;
            maxLayer= l;
        }
    }

    if(hasUV) {
        fprintf(gfile,"\tmap_channels= interpolate((%d, List(", sce->r.cfra);
        for(l= 1; l < fdata->totlayer; ++l) {
            if(fdata->layers[l].type == TYPE_UV) {
                CustomData_set_layer_active(fdata, TYPE_UV, l-1);
                mesh_update_customdata_pointers(mesh);
                
                fprintf(gfile,"\n\t\t// %s", fdata->layers[l].name);
                fprintf(gfile,"\n\t\tList(%d,ListVector(", l);

                face= mesh->mface;
                for(f= 0; f < mesh->totface; ++face, ++f) {
                    if(f) fprintf(gfile,",");

                    if(face->v4)
                        verts= 4;
                    else
                        verts= 3;
                    for(i= 0; i < verts; i++) {
                        if(i) fprintf(gfile,",");
                        
                        fprintf(gfile, "Vector(%.6f,%.6f,0.0)",
                                mesh->mtface[f].uv[i][0],
                                mesh->mtface[f].uv[i][1]);
                    }
                }

                fprintf(gfile,"),");

                fprintf(gfile,"ListInt(");
                u= -1;
                u0= -1;
                face= mesh->mface;
                for(f = 0; f < mesh->totface; ++face, ++f) {
                    if(f) fprintf(gfile,",");

                    if(face->v4) {
                        verts= 6;
                        u= u0;
                    } else {
                        if(mesh->mface[f-1].v4)
                            u= u0;
                        verts= 3;
                    }

                    for(i= 0; i < verts; i++) {
                        if(i) fprintf(gfile,",");
                            
                        if(verts == 6) {
                            if(i == 5) {
                                u0= u;
                                u-= 4;
                            }
                            if(i != 3)
                                u++;
                        } else {
                            u++;
                            u0= u;
                        }

                        fprintf(gfile,"%d", u);
                    }
                }
                fprintf(gfile,"))");

                if(l != maxLayer)
                    fprintf(gfile,",");
            }
        }
        fprintf(gfile,")));\n");
    }

    fprintf(gfile,"}\n\n");
}


Mesh *get_render_mesh(Scene *sce, Main *bmain, Object *ob)
{
    Object      *tmpobj= NULL;
    Curve       *tmpcu= NULL;
    Mesh        *mesh= NULL;
    DerivedMesh *dm;

    /* perform the mesh extraction based on type */
    switch (ob->type) {
    case OB_FONT:
    case OB_CURVE:
    case OB_SURF:
        /* copies object and modifiers (but not the data) */
        tmpobj= copy_object( ob );
        tmpcu = (Curve *)tmpobj->data;
        tmpcu->id.us--;

        /* copies the data */
        tmpobj->data = copy_curve( (Curve *) ob->data );

        /* get updated display list, and convert to a mesh */
        makeDispListCurveTypes( sce, tmpobj, 0 );
        nurbs_to_mesh( tmpobj );
		
        /* nurbs_to_mesh changes the type tp a mesh, check it worked */
        if(tmpobj->type != OB_MESH) {
            free_libblock_us( &bmain->object, tmpobj );
            return NULL;
        }

        mesh = tmpobj->data;
        free_libblock_us( &bmain->object, tmpobj );
        break;
    case OB_MBALL:
        /* metaballs don't have modifiers, so just convert to mesh */
        ob = find_basis_mball( sce, ob );
        mesh = add_mesh( "Mesh" );
        mball_to_mesh( &ob->disp, mesh );
        break;
    case OB_MESH:
        /* apply modifiers and create mesh */
        dm = mesh_create_derived_render( sce, ob, CD_MASK_MESH );
        mesh = add_mesh( "Mesh" );
        DM_to_mesh( dm, mesh );
        dm->release( dm );
        break;
    default:
        return NULL;
    }

    return mesh;
}


int export_scene(bContext *C, wmOperator *op)
{
    Scene  *sce= CTX_data_scene(C);
    Main   *bmain= CTX_data_main(C);
    Base   *base;
    Object *ob;
    Mesh   *mesh;

    FILE   *gfile= NULL;
    char    filename[FILE_MAX];

    double  time;
    char    time_str[32];

    if(RNA_property_is_set(op->ptr, "vray_geometry_file")) {
        RNA_string_get(op->ptr, "vray_geometry_file", filename);
        gfile= fopen(filename, "w");
    }

    if(gfile) {    
        base= (Base*)sce->base.first;

        time= PIL_check_seconds_timer();

        while(base) {
            ob= base->object;

            if(ob->lay & sce->lay) {
                mesh= get_render_mesh(sce, bmain, ob);

                if(mesh) {
                    printf("V-Ray/Blender: Exporting mesh: \033[0;32m%s\033[0m\r", ob->id.name+2);
                    fflush(stdout);

                    write_mesh_vray(gfile, sce, ob, mesh);

                    /* remove the temporary mesh */
                    free_mesh(mesh);
                    BLI_remlink(&bmain->mesh, mesh);
                    MEM_freeN(mesh);
                }
            }
            
            base= base->next;
        }

        BLI_timestr(PIL_check_seconds_timer()-time, time_str);
        
        printf("V-Ray/Blender: Exporting meshes done [%s]                   \n", time_str);

        fclose(gfile);
    }

    return 0;
}

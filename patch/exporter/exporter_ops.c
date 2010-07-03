#include "BKE_main.h"
#include "BKE_scene.h"
#include "BKE_context.h"

#include "DNA_windowmanager_types.h"

#include "WM_api.h"
#include "WM_types.h"

#include "exporter.h"
#include "exporter_ops.h"


void SCENE_OT_scene_export(wmOperatorType *ot)
{
    /* identifiers */
    ot->name= "Export scene";
    ot->idname= "SCENE_OT_scene_export";
    ot->description="Export scene for external renderer.";

    /* api callbacks */
    ot->exec= export_scene;

    /* flags */
    ot->flag= 0;

    RNA_def_string(ot->srna, "vray_geometry_file", "", FILE_MAX, "Geometry export file", "Geometry export file.");
}


void ED_operatortypes_exporter(void)
{
	WM_operatortype_append(SCENE_OT_scene_export);
}


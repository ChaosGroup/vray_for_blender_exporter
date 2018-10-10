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

import bpy
import sys

import os
import json

from vb30 import version
from vb30.lib import SysUtils
from vb30.lib import BlenderUtils

import _vray_for_blender_rt


TYPE = 'SYSTEM'
ID   = 'VRayExporter'
NAME = 'Exporter'
DESC = "Exporter configuration"


def _mtlEditorUpdatePreview(self, context):
    if self.materialListIndexPrev != self.materialListIndex:
        self.materialListIndexPrev = self.materialListIndex
        _vray_for_blender_rt.updatePreview(bpy.context.as_pointer(), BlenderUtils.NC_MATERIAL)


class VRayExporterSetBinary(bpy.types.Operator):
    bl_idname      = "vray.select_vray_std"
    bl_label       = "Use V-Ray Standalone"
    bl_description = "Use V-Ray Standalone"

    bin_path = bpy.props.StringProperty()

    def execute(self, context):
        VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences
        VRayPreferences.vray_binary = self.bin_path
        return {'FINISHED'}


def getVRayCloudPath():
    """
    If V-Ray Cloud is installed on the system returns the path to it, else - None.
    """

    # check whether vcloud JSON file exists
    vcloudJsonDir = '%APPDATA%/Chaos Group/vcloud/client/' if bpy.app.build_platform == b'Windows' else '$HOME/.ChaosGroup/vcloud/client/'
    vcloudJsonDir = os.path.expandvars(vcloudJsonDir)
    vcloudJsonFilename = vcloudJsonDir + 'vcloud.json'
    if not os.path.exists(vcloudJsonFilename):
        return None

    # check whether the vcloud executable file exists via the "executable" field in the JSON file
    vcloudFullPath = ''
    with open(vcloudJsonFilename, 'r') as jsonFileId:
        jsonData = json.load(jsonFileId)
        vcloudFullPath = os.path.expandvars(jsonData['executable'])
    
    return vcloudFullPath if os.path.exists(vcloudFullPath) else None


class VRayExporterPreferences(bpy.types.AddonPreferences):
    bl_idname = "vb30"

    vray_cloud_binary = getVRayCloudPath()
    detect_vray_cloud = vray_cloud_binary is not None

    detect_vray = bpy.props.BoolProperty(
        name = "Detect V-Ray",
        description = "Detect V-Ray binary location",
        default = True
    )

    vray_binary = bpy.props.StringProperty(
        name = "Path",
        subtype = 'FILE_PATH',
        description = "Path to V-Ray binary. Don\'t use relative path here - use absolute!"
    )

    def draw(self, context):
        layout = self.layout

        layout.label(text="Exporter revision: %s" % version.VERSION)

        layout.prop(self, "detect_vray")
        if not self.detect_vray:
            vrayStds = SysUtils.GetVRayStandalones()
            if vrayStds:
                pathBox = layout.box()
                pathBox.label("V-Ray Standalone is found in:")
                for vrayStd in vrayStds:
                    vrayExePath = vrayStds[vrayStd]

                    split = pathBox.split(percentage=0.3)
                    col = split.column()
                    col.label(vrayStd)

                    col = split.column()
                    op = col.operator('vray.select_vray_std', text=vrayExePath, icon='FILE_TICK')
                    op.bin_path = vrayExePath

            vrayBin = "vray.exe" if sys.platform == 'win32' else "vray"
            layout.label('You could manually select "%s" binary, please, note NOT to use relative path here:' % vrayBin)

            split = layout.split(percentage=0.2, align=True)
            split.column().label("Filepath:")
            split.column().prop(self, "vray_binary", text="")
        
        if self.detect_vray_cloud:
            layout.label(text="V-Ray Cloud binary: {0}".format(self.vray_cloud_binary))
        else:
            layout.label(text="V-Ray Cloud binary is not detected on your system!")


class VRayExporter(bpy.types.PropertyGroup):
    experimental = bpy.props.BoolProperty(
        name        = "Experimental",
        description = "Enable experimental options",
        default     = False
    )

    spherical_harmonics = bpy.props.EnumProperty(
        name = "Spherical Harmonics Mode",
        description = "Bake or render spherical harmonics",
        items = (
            ('BAKE',   "Bake",   ""),
            ('RENDER', "Render", ""),
        ),
        default = 'BAKE'
    )

    ######## ##     ## ########   #######  ########  ########
    ##        ##   ##  ##     ## ##     ## ##     ##    ##
    ##         ## ##   ##     ## ##     ## ##     ##    ##
    ######      ###    ########  ##     ## ########     ##
    ##         ## ##   ##        ##     ## ##   ##      ##
    ##        ##   ##  ##        ##     ## ##    ##     ##
    ######## ##     ## ##         #######  ##     ##    ##

    currentBakeObject = bpy.props.PointerProperty(
        name = "Current Bake object",
        type = bpy.types.Object,
        options= {'HIDDEN'},
    )

    ntreeExportDirectory = bpy.props.StringProperty(
        name = "Export Path",
        subtype = 'DIR_PATH',
        description = "Export directory",
        default = "//vrscenes/"
    )

    activeLayers = bpy.props.EnumProperty(
        name        = "Active layers",
        description = "Render objects from layers",
        items = (
            ('ACTIVE', "Active Layers", ""),
            ('ALL',    "All Layers",    ""),
            ('CUSTOM', "Custom Layers", "")
        ),
        default = 'ACTIVE'
    )

    customRenderLayers = bpy.props.BoolVectorProperty(
        subtype = 'LAYER',
        size    = 20
    )

    use_displace = bpy.props.BoolProperty(
        name = "Displace / Subdiv",
        description = "Use displace / subdivisions",
        default = True
    )

    use_still_motion_blur = bpy.props.BoolProperty(
        name        = "Still Motion Blur",
        description = "Generate data for motion blur",
        default     = False
    )

    use_hair = bpy.props.BoolProperty(
        name = "Export Hair",
        description = "Render hair",
        default = True
    )

    calculate_instancer_velocity = bpy.props.BoolProperty(
        name = "Calculate instancer velocity",
        description = "Used to calculate particles velocty when using motion blur",
        default = False
    )

    use_smoke = bpy.props.BoolProperty(
        name = "Export Smoke",
        description = "Render smoke",
        default = True
    )

    camera_loop = bpy.props.BoolProperty(
        name = "Camera Loop",
        description = "Render views from all cameras",
        default = False
    )

    auto_meshes = bpy.props.BoolProperty(
        name = "Re-Export Meshes",
        description = "Re-Export meshes",
        default = True
    )

    debug = bpy.props.BoolProperty(
        name = "Debug",
        description = "Enable script\'s debug output",
        default = False
    )

    output = bpy.props.EnumProperty(
        name = "Exporting Directory",
        description = "Exporting directory",
        items = (
            ('USER',  "Custom Directory", ""),
            ('SCENE', "Scene File Directory",   ""),
            ('TMP',   "Global TMP directory",   "")
        ),
        default = 'TMP'
    )

    currentContextObject = bpy.props.PointerProperty(
        name = "Nodetree context object",
        description = "This object will be used when exporting object nodetrees for materail and geometry context",
        type = bpy.types.Object,
    )

    ntreeListIndex = bpy.props.IntProperty(
        name        = "Node Trees List Index",
        description = "Node trees list index",
        min         = -1,
        default     = -1,
    )

    materialListIndex = bpy.props.IntProperty(
        name        = "Material List Index",
        description = "Material list index",
        min         = -1,
        default     = -1,
        update      = _mtlEditorUpdatePreview,
    )

    materialListIndexPrev = bpy.props.IntProperty(
        name        = "Material List Index Previous State",
        description = "Material list index previous state",
        min         = -1,
        default     = -1,
    )

    materialListShowPreview = bpy.props.BoolProperty(
        name        = "Show preview",
        description = "Show preview",
        default     = True
    )

    useSeparateFiles = bpy.props.BoolProperty(
        name        = "Separate Files",
        description = "Export plugins to separate files",
        default     = True
    )

    default_mapping = bpy.props.EnumProperty(
        name = "Default Mapping",
        description = "Defaul mapping type for procedural texture nodes without \"Mapping\" socket linked",
        items = (
            ('0', "Object",  "Object mapping"),
            ('1', "Box",     "Box projection"),
            ('2', "Channel", "Default channel"),
        ),
        default = '0'
    )

    ########  ######## ##    ## ########  ######## ########      ######  ######## ######## ######## #### ##    ##  ######    ######
    ##     ## ##       ###   ## ##     ## ##       ##     ##    ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
    ##     ## ##       ####  ## ##     ## ##       ##     ##    ##       ##          ##       ##     ##  ####  ## ##        ##
    ########  ######   ## ## ## ##     ## ######   ########      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
    ##   ##   ##       ##  #### ##     ## ##       ##   ##            ## ##          ##       ##     ##  ##  #### ##    ##        ##
    ##    ##  ##       ##   ### ##     ## ##       ##    ##     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
    ##     ## ######## ##    ## ########  ######## ##     ##     ######  ########    ##       ##    #### ##    ##  ######    ######

    animation_mode = bpy.props.EnumProperty(
        name = "Animation Mode",
        description = "Animation Type",
        items = (
            ('NONE',         "None",                         "Render single frame"),
            ('FULL',         "Full Range",                   "Export full animation range then render"),
            ('CAMERA',       "Full Range (Camera Only)",     "Export full animation of camera motion"),
            ('NOTMESHES',    "Full Range (Except Geometry)", "Export full animation range then render (meshes are not animated)"),
            ('CAMERA_LOOP',  "Camera Loop",                  "Render all scene cameras"),
            ('FRAMEBYFRAME', "Frame By Frame",               "Export and render frame by frame"),
        ),
        default = 'NONE'
    )

    draft = bpy.props.BoolProperty(
        name = "Draft Render",
        description = "Render with low settings",
        default = False
    )

    select_node_preview = bpy.props.BoolProperty(
        name = "Selected node preview",
        description = "Enable material preview of selected node in node editor",
        default = False
    )

    image_to_blender = bpy.props.BoolProperty(
        name = "Image To Blender",
        description = "Pass image to Blender on render end (EXR file format is used)",
        default = False
    )

    ########  ########   #######   ######  ########  ######   ######
    ##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ##
    ##     ## ##     ## ##     ## ##       ##       ##       ##
    ########  ########  ##     ## ##       ######    ######   ######
    ##        ##   ##   ##     ## ##       ##             ##       ##
    ##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ##
    ##        ##     ##  #######   ######  ########  ######   ######

    autorun = bpy.props.BoolProperty(
        name = "Autorun",
        description = "Start V-Ray automatically after export",
        default = True
    )

    verboseLevel = bpy.props.EnumProperty(
        name = "Log Level",
        description = "Specifies the verbose level of information printed to the standard output",
        items = (
            ('0', "No information", "No information printed"),
            ('1', "Only errors",    "Only errors"),
            ('2', "Warnings",       "Errors and warnings"),
            ('3', "Progress",       "Errors, warnings and informational messages"),
            ('4', "All",            "All output"),
        ),
        default = '3'
    )

    showProgress = bpy.props.EnumProperty(
        name = "Show Progress",
        description = "Specifies whether calculations progress should be printed to the standard output",
        items = (
            ('0', "None",                 ""),
            ('1', "Verbose > Only Erros", 'Display progress only if "Verbose Level" is > "Only errors"'),
            ('2', "Always",               "Errors and warnings"),
        ),
        default = '1'
    )

    autoclose = bpy.props.BoolProperty(
        name = "Auto Close",
        description = "Stop render and close VFB on Esc",
        default = False
    )

    log_window = bpy.props.BoolProperty(
        name = "Show Log Window",
        description = "Show log window (Linux)",
        default = False
    )

    log_window_type = bpy.props.EnumProperty(
        name = "Log Window Type",
        description = "Log window type",
        items = (
            ('DEFAULT', "Default",        ""),
            ('XTERM',   "XTerm",          ""),
            ('GNOME',   "Gnome Terminal", ""),
            ('KDE',     "Konsole",        ""),
            ('CUSTOM',  "Custom",         "")
        ),
        default = 'DEFAULT'
    )

    log_window_term = bpy.props.StringProperty(
        name = "Custom Terminal",
        description = "Custom log window terminal command",
        default = "x-terminal-emulator"
    )

    display = bpy.props.BoolProperty(
        name = "Display VFB",
        description = "Display VFB",
        default = True
    )

    display_vfb_in_batch = bpy.props.BoolProperty(
        name = "Display VFB In Batch Mode",
        description = "Display VFB in background mode",
        default = False
    )

    display_vfb_on_top = bpy.props.BoolProperty(
        name = "Display Always On Top",
        description = "Display VFB on top of the other windows",
        default = True
    )

    detect_vray = bpy.props.BoolProperty(
        name = "Detect V-Ray",
        description = "Detect V-Ray binary location",
        default = True
    )

    vray_binary = bpy.props.StringProperty(
        name = "Path",
        subtype = 'FILE_PATH',
        description = "Path to V-Ray binary. Don\'t use relative path here - use absolute!"
    )

    output_dir = bpy.props.StringProperty(
        name = "Directory",
        subtype = 'DIR_PATH',
        description = "User-defined output directory"
    )

    output_unique = bpy.props.BoolProperty(
        name = "Use Unique Filename",
        description = "Use unique file name",
        default = False
    )

    auto_save_render = bpy.props.BoolProperty(
        name = "Save Render",
        description = "Save render automatically",
        default = False
    )

    wait = bpy.props.BoolProperty(
        name        = "Wait Proccess Exit",
        description = "Wait for V-Ray to complete rendering",
        options     = {'HIDDEN'},
        default     = False
    )

    gen_run_file = bpy.props.BoolProperty(
        name        = "Generate Run File",
        description = "Generate script for render",
        default     = False
    )

    ui_render_grouping = bpy.props.BoolProperty(
        name = "Group Render Panels",
        default = True
    )

    ui_render_context = bpy.props.EnumProperty(
        name = "Render Context Panels",
        description = "Show render panels group",
        items = (
            ('0', "Render", ""),
            ('1', "Globals", ""),
            ('2', "GI", ""),
            ('3', "Sampler", ""),
            ('4', "System", ""),
        ),
        default = '0'
    )

    op_switch_slots_switch_to = bpy.props.EnumProperty(
        items = (
            ('OBJECT', "Object", ""),
            ('DATA',   "Data",   ""),
        ),
        default = 'OBJECT'
    )

    subsurf_to_osd = bpy.props.BoolProperty(
        name        = "Subsurf To OpenSubdiv",
        description = "Automatically convert Subsurf modifier (if last in stack) to V-Ray's OpenSubdiv subdivision",
        default     = False
    )

    data_format = bpy.props.EnumProperty(
        name = "Export Format",
        description = "Export data format",
        items = (
            ('ZIP',   "ZIP",        "Compress list data"),
            ('HEX',   "HEX",        "Export list data in hex format"),
            ('ASCII', "Plain Text", "Export as plain text"),
        ),
        default = 'ZIP'
    )

    backend = bpy.props.EnumProperty(
        name = "V-Ray Backend",
        description = "V-Ray backend",
        items = SysUtils.getExporterBackendList(),
    )

    work_mode = bpy.props.EnumProperty(
        name = "Render Mode",
        description = "Render mode",
        items = (
            ('RENDER',        "Render", ""),
            ('RENDER_EXPORT', "Render & Export", ""),
            ('EXPORT_ONLY',   "Export Only", ""),
        ),
        default = 'RENDER'
    )

    backend_worker = bpy.props.EnumProperty(
        name = "Server Mode",
        description = "Server mode",
        items = (
            ('LOCAL',   "Local",  ""),
            ('NETWORK', "Remote", ""),
        ),
        default = 'LOCAL'
    )

    zmq_address = bpy.props.StringProperty(
        name = "Server Address",
        description = "Server address",
        default = ""
    )

    zmq_port = bpy.props.IntProperty(
        name = "Server Port",
        description = "Server port",
        min = 1000,
        max = 65535,
        default = 5555
    )

    zmq_log_level = bpy.props.EnumProperty(
        name = "ZMQ log level",
        description = "ZMQ log level",
        items = (
            ('ERROR', 'Error', ''),
            ('WARNING', 'Warning', ''),
            ('DEBUG', 'Debug', ''),
            ('INFO', 'Info', ''),
        ),
        default = 'ERROR'
    )

    vfb_global_preset_file_use = bpy.props.BoolProperty(
        name = "Use Global Preset File",
        description = "Use VFB global preset file",
        default = False
    )

    vfb_global_preset_file = bpy.props.StringProperty(
        name = "Global Preset File",
        subtype = 'FILE_PATH',
        description = "VFB global preset file",
    )

    viewport_image_type = bpy.props.EnumProperty(
        name = "Viewport Image Type",
        description = "Viewport Image Type",
        items = (
            ( "1", "RAW", "Full Color + Alpha" ),
            ( "4", "JPEG", "JPEG compressed"   )
        ),
        default = '1'
    )

    viewport_jpeg_quality = bpy.props.IntProperty(
        name = "Image quality",
        description = "JPEG image quality",
        min = 10,
        max = 100,
        subtype = 'PERCENTAGE',
        default = 60
    )

    viewport_resolution = bpy.props.IntProperty(
        name = "Viewport Resolution",
        description = "Viewport resolution",
        min = 10,
        max = 100,
        subtype = 'PERCENTAGE',
        default = 100
    )

    viewport_alpha = bpy.props.BoolProperty(
        name = "Show Alpha",
        description = "Show Alpha",
        default = False
    )

    submit_to_vray_cloud = bpy.props.BoolProperty(
        name = "Submit to V-Ray Cloud",
        description = "Submits current scene as a render job to the V-Ray Cloud",
        default = False
    )

    vray_cloud_project_name = bpy.props.StringProperty(
        name = "Project",
        description = "V-Ray Cloud Project Name",
        default = "Blender for V-Ray"
    )

    vray_cloud_job_name = bpy.props.StringProperty(
        name = "Job",
        description = "V-Ray Cloud Job Name",
        default = "$F"
    )

    device_type = bpy.props.EnumProperty(
        name = "Device Type",
        description = "Rendering device",
        items = (
            ('CPU', "CPU", ""),
            ('GPU', "GPU", ""),
        ),
        default = 'CPU'
    )

    device_gpu_type = bpy.props.EnumProperty(
        name = "GPU Device Type",
        description = "GPU device type",
        items = (
            ('CUDA', "CUDA", ""),
            ('OPENCL', "OpenCL", ""),
        ),
        default = 'CUDA'
    )

def GetRegClasses():
    return (
        VRayExporter,
        VRayExporterPreferences,
        VRayExporterSetBinary,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

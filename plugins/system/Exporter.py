#
# V-Ray For Blender
#
# http://vray.cgdo.ru
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


TYPE = 'SYSTEM'
ID   = 'VRayExporter'
NAME = 'Exporter'
DESC = "Exporter configuration"


class VRayExporter(bpy.types.PropertyGroup):
    experimental = bpy.props.BoolProperty(
        name        = "Experimental",
        description = "Enable experimental options",
        default     = False
    )

    backend = bpy.props.EnumProperty(
        name        = "Renderer",
        description = "V-Ray type",
        items = (
                ('STD', "V-Ray Standalone", ""),
                ('VB',  "V-Ray For Blender", ""),
        ),
        default = 'STD'
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

    ##    ##  #######  ########  ########  ######  
    ###   ## ##     ## ##     ## ##       ##    ## 
    ####  ## ##     ## ##     ## ##       ##       
    ## ## ## ##     ## ##     ## ######    ######  
    ##  #### ##     ## ##     ## ##             ## 
    ##   ### ##     ## ##     ## ##       ##    ## 
    ##    ##  #######  ########  ########  ######  
    
    nodesUseSidePanel = bpy.props.BoolProperty(
        name = "Side Panel",
        description = "Draw node properties in editors's side panel",
        default = False
    )

    ######## ##     ## ########   #######  ########  ######## 
    ##        ##   ##  ##     ## ##     ## ##     ##    ##    
    ##         ## ##   ##     ## ##     ## ##     ##    ##    
    ######      ###    ########  ##     ## ########     ##    
    ##         ## ##   ##        ##     ## ##   ##      ##    
    ##        ##   ##  ##        ##     ## ##    ##     ##    
    ######## ##     ## ##         #######  ##     ##    ##    
    
    use_fast_dupli_export = bpy.props.BoolProperty(
        name = "Fast Dupli / Particles Export",
        description = "Use fast dupli export",
        default = False
    )

    activeLayers = bpy.props.EnumProperty(
        name        = "Active layers",
        description = "Render objects from layers",
        items = (
                ('ACTIVE', "Active", ""),
                ('ALL',    "All",    ""),
                ('CUSTOM', "Custom", "")
        ),
        default = 'ACTIVE'
    )

    customRenderLayers = bpy.props.BoolVectorProperty(
        subtype = 'LAYER',
        size    = 20
    )

    use_displace = bpy.props.BoolProperty(
        name = "Displace / subdiv",
        description = "Use displace / subdivisions",
        default = True
    )

    check_animated = bpy.props.BoolProperty(
        name = "Check animated",
        description = "Detect animated meshes",
        default = False
    )

    customFrame = bpy.props.IntProperty(
        name        = "Custom Frame",
        description = "Custom frame number",
        options     = {'HIDDEN'},
        min         = 0,
        max         = 1024,
        default     = 0
    )

    use_hair = bpy.props.BoolProperty(
        name = "Hair",
        description = "Render hair",
        default = True
    )

    use_still_motion_blur = bpy.props.BoolProperty(
        name        = "Still Motion Blur",
        description = "Generate data for still motion blur",
        default     = False
    )

    use_smoke = bpy.props.BoolProperty(
        name = "Smoke",
        description = "Render smoke",
        default = True
    )

    use_smoke_hires = bpy.props.BoolProperty(
        name = "Smoke High Resolution",
        description = "Render high resolution smoke",
        default = True
    )

    use_instances = bpy.props.BoolProperty(
        name = "Instances",
        description = "Use instances (Alt+D meshes will be the same; saves memory and faster export)",
        default = False
    )

    camera_loop = bpy.props.BoolProperty(
        name = "Camera loop",
        description = "Render views from all cameras",
        default = False
    )

    auto_meshes = bpy.props.BoolProperty(
        name = "Auto export meshes",
        description = "Export meshes automatically before render",
        default = True
    )

    debug = bpy.props.BoolProperty(
        name = "Debug",
        description = "Enable script\'s debug output",
        default = False
    )

    mesh_debug = bpy.props.BoolProperty(
        name = "Debug",
        description = "Enable build debug output",
        default = False
    )

    output = bpy.props.EnumProperty(
        name = "Exporting directory",
        description = "Exporting directory",
        items = (
            ('USER',"User-defined directory",""),
            ('SCENE',"Scene file directory",""),
            ('TMP',"Global TMP directory","")
        ),
        default = 'TMP'
    )

    ntreeListIndex = bpy.props.IntProperty(
        name        = "Node Trees List Index",
        description = "Node trees list index",
        min         = -1,
        default     = -1,
    )

    useSeparateFiles = bpy.props.BoolProperty(
        name        = "Separate Files",
        description = "Export plugins to separate files",
        default     = True
    )

    checkAnimated = bpy.props.BoolProperty(
        name        = "Check Animated",
        description = "Check 'is_animated' attribute when exporting animation",
        default     = False
    )


    ########  ######## ##    ## ########  ######## ########      ######  ######## ######## ######## #### ##    ##  ######    ######  
    ##     ## ##       ###   ## ##     ## ##       ##     ##    ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ## 
    ##     ## ##       ####  ## ##     ## ##       ##     ##    ##       ##          ##       ##     ##  ####  ## ##        ##       
    ########  ######   ## ## ## ##     ## ######   ########      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######  
    ##   ##   ##       ##  #### ##     ## ##       ##   ##            ## ##          ##       ##     ##  ##  #### ##    ##        ## 
    ##    ##  ##       ##   ### ##     ## ##       ##    ##     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ## 
    ##     ## ######## ##    ## ########  ######## ##     ##     ######  ########    ##       ##    #### ##    ##  ######    ######  

    animation = bpy.props.BoolProperty(
        name = "Animation",
        description = "Render animation",
        default = False
    )

    animation_type = bpy.props.EnumProperty(
        name = "Animation Mode",
        description = "Animation Type",
        items = (
            ('FRAMEBYFRAME', "Frame-By-Frame", "Export and render frame by frame"),
            ('FULL',         "Full Range",     "Export full animation range then render"),
            ('NOTMESHES',    "All But Meshes", "Export full animation range then render (meshes are not animated)")
        ),
        default = 'FRAMEBYFRAME'
    )

    draft = bpy.props.BoolProperty(
        name = "Draft render",
        description = "Render with low settings",
        default = False
    )

    image_to_blender = bpy.props.BoolProperty(
        name = "Image to Blender",
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
        name = "Log level",
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

    autoclose = bpy.props.BoolProperty(
        name = "Auto close",
        description = "Stop render and close VFB on Esc",
        default = False
    )

    log_window = bpy.props.BoolProperty(
        name = "Show log window",
        description = "Show log window (Linux)",
        default = False
    )

    use_feedback = bpy.props.BoolProperty(
        name        = "Render feedback",
        description = "Catch and show rendering progress",
        default     = False
    )

    use_progress = bpy.props.BoolProperty(
        name        = "Show progress",
        description = "Catch and show calculations progress",
        default     = False
    )

    wait = bpy.props.BoolProperty(
        name        = "Wait",
        description = "Wait for V-Ray to complete rendering",
        options     = {'HIDDEN'},
        default     = False
    )

    log_window_type = bpy.props.EnumProperty(
        name = "Log window type",
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
        name = "Log window terminal",
        description = "Log window terminal command",
        default = "x-terminal-emulator"
    )

    display = bpy.props.BoolProperty(
        name = "Display VFB",
        description = "Display VFB",
        default = True
    )

    detect_vray = bpy.props.BoolProperty(
        name = "Detect V-Ray",
        description = "Detect V-Ray binary location",
        default = True
    )

    display_srgb = bpy.props.BoolProperty(
        name = "Display in sRGB",
        description = "Display colors on Vray Framebuffer in sRGB space",
        default = False
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
        name = "Use unique file name",
        description = "Use unique file name",
        default = False
    )

    auto_save_render = bpy.props.BoolProperty(
        name = "Save render",
        description = "Save render automatically",
        default = False
    )

    socket_address = bpy.props.StringProperty(
        name        = "Socket address",
        description = "V-Ray Standalone socket interface address",
        default     = "localhost"
    )


def GetRegClasses():
    return (
        VRayExporter,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

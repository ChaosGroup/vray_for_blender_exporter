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

import math
import os
import string
import subprocess
import sys
import tempfile
import time

import bpy
import mathutils

import _vray_for_blender

from vb30.plugins import PLUGINS, PLUGINS_ID

from vb30.lib     import utils as LibUtils
from vb30.lib     import ExportUtils
from vb30.nodes   import export as NodesExport
from vb30.debug   import Debug, PrintDict
from vb30.lib.VRayStream import VRayStream
from vb30         import utils
from vb30.utils   import get_name, a, p


##     ## ######## #### ##        ######  
##     ##    ##     ##  ##       ##    ## 
##     ##    ##     ##  ##       ##       
##     ##    ##     ##  ##        ######  
##     ##    ##     ##  ##             ## 
##     ##    ##     ##  ##       ##    ## 
 #######     ##    #### ########  ######  

def GetObjects(bus, checkAnimated=False, checkUpdated=False):
    scene = bus['scene']

    for ob in scene.objects:
        if checkAnimated and not ob.is_animated:
            continue
        if checkUpdated and not (ob.is_updated or ob.is_updated_data):
            continue
        if ob.type in {'ARMATURE', 'LATTICE', 'SPEAKER'}:
            continue
        if ob.name in bus['gizmos']:
            continue
        if not utils.object_visible(bus, ob):
            continue
        yield ob


 ######  ######## ######## ######## #### ##    ##  ######    ######
##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##       ##          ##       ##     ##  ####  ## ##        ##
 ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
      ## ##          ##       ##     ##  ##  #### ##    ##        ##
##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
 ######  ########    ##       ##    #### ##    ##  ######    ######

def ExportRenderPasses(bus):
    scene = bus['scene']
    o     = bus['output']

    ntree = scene.vray.ntree
    if not ntree:
        return

    outputNode = NodesExport.GetNodeByType(ntree, 'VRayNodeRenderChannels')
    if not outputNode:
        return

    for socket in outputNode.inputs:
        if socket.is_linked and socket.use:
            NodesExport.WriteConnectedNode(bus, ntree, socket)

    o.set('RENDERCHANNEL', 'SettingsRenderChannels', 'SettingsRenderChannels')
    o.writeHeader()
    o.writeAttibute('unfiltered_fragment_method', outputNode.unfiltered_fragment_method)
    o.writeAttibute('deep_merge_mode', outputNode.deep_merge_mode)
    o.writeAttibute('deep_merge_coeff', outputNode.deep_merge_coeff)
    o.writeFooter()


def ExportSettings(bus):
    """
    Exports global render settings
    Must be called once before the object export
    """

    scene = bus['scene']
    ca    = bus['camera']

    VRayCamera = ca.data.vray
    VRayScene  = scene.vray

    Includer       = VRayScene.Includer
    VRayExporter   = VRayScene.Exporter
    VRayDR         = VRayScene.VRayDR

    SettingsOutput = VRayScene.SettingsOutput
    SettingsGI     = VRayScene.SettingsGI

    for pluginType in {'SETTINGS', 'CAMERA'}:
        for pluginName in PLUGINS[pluginType]:
            if pluginName in {'BakeView',
                              'SettingsLightLinker',
                              'VRayStereoscopicSettings',
                              'SettingsPtexBaker',
                              'SettingsVertexBaker',
                              'SettingsCurrentFrame',
                              'SettingsLightTree',
                              'SettingsVRST',
                              'CameraStereoscopic',
                              'SettingsEnvironment'}:
                continue

            if pluginName in {'SettingsEXR',
                              'SettingsVFB'}:
                continue

            pluginModule = PLUGINS[pluginType][pluginName]

            propGroup      = None
            overrideParams = {}
            
            if pluginName == 'SettingsRegionsGenerator':
                propGroup = getattr(VRayScene, pluginName)

                overrideParams = {
                    'xc' : propGroup.xc,
                    'yc' : propGroup.xc if propGroup.lock_size else propGroup.yc,
                }
            elif pluginName.startswith('Filter'):
                continue
            elif pluginName in {'SphericalHarmonicsExporter', 'SphericalHarmonicsRenderer'}:
                propGroup = getattr(VRayScene, pluginName)
                
                if SettingsGI.primary_engine != '4':
                    continue

                if VRayExporter.spherical_harmonics == 'BAKE':
                    if pluginName == 'SphericalHarmonicsRenderer':
                        continue
                else:
                    if pluginName == 'SphericalHarmonicsExporter':
                        continue
            elif pluginName == 'SettingsCamera':
                propGroup = getattr(VRayCamera, pluginName)
            elif pluginName == 'CameraPhysical':
                propGroup = getattr(VRayCamera, pluginName)
            elif pluginName == 'RenderView':
                propGroup = getattr(VRayCamera, pluginName)
            else:
                propGroup = getattr(VRayScene, pluginName)
            
            if not propGroup:
                continue

            ExportUtils.WritePlugin(bus, pluginModule, pluginName, propGroup, overrideParams)

    PLUGINS_ID['SettingsEnvironment'].write(bus)

    ExportRenderPasses(bus)


 ######     ###    ##     ## ######## ########     ###    
##    ##   ## ##   ###   ### ##       ##     ##   ## ##   
##        ##   ##  #### #### ##       ##     ##  ##   ##  
##       ##     ## ## ### ## ######   ########  ##     ## 
##       ######### ##     ## ##       ##   ##   ######### 
##    ## ##     ## ##     ## ##       ##    ##  ##     ## 
 ######  ##     ## ##     ## ######## ##     ## ##     ## 

def ExportCamera(scene, camera):
    """
    Exports camera
    Mainly used from ExportObjects()
    This could be called separately for "Camera Loop" feature
    """
    pass


##       ####  ######   ##     ## ########  ######  
##        ##  ##    ##  ##     ##    ##    ##    ## 
##        ##  ##        ##     ##    ##    ##       
##        ##  ##   #### #########    ##     ######  
##        ##  ##    ##  ##     ##    ##          ## 
##        ##  ##    ##  ##     ##    ##    ##    ## 
######## ####  ######   ##     ##    ##     ######  

def write_lamp(bus):
    scene = bus['scene']
    ob    = bus['node']['object']

    lamp     = ob.data
    VRayLamp = lamp.vray

    lamp_name   = get_name(ob, prefix='LA')
    lamp_matrix = ob.matrix_world

    if 'dupli' in bus['node'] and 'name' in bus['node']['dupli']:
        lamp_name  += bus['node']['dupli']['name']
        lamp_matrix = bus['node']['dupli']['matrix']

    if 'particle' in bus['node'] and 'name' in bus['node']['particle']:
        lamp_name  += bus['node']['particle']['name']
        lamp_matrix = bus['node']['particle']['matrix']

    lightPluginName = LibUtils.GetLightPluginName(lamp)

    lightPropGroup = getattr(VRayLamp, lightPluginName)

    # Check if we have a node tree and export it
    #
    socketParams = {
        'transform' : lamp_matrix,
    }

    if VRayLamp.ntree:
        lightNode = NodesExport.GetNodeByType(VRayLamp.ntree, 'VRayNode%s' % lightPluginName)
        if lightNode:
            for nodeSocket in lightNode.inputs:
                vrayAttr = nodeSocket.vray_attr
                value = NodesExport.WriteConnectedNode(bus, VRayLamp.ntree, nodeSocket, returnDefault=False)
                if value is not None:
                    socketParams[vrayAttr] = value

    if lamp.type == 'AREA':
        if lamp.shape == 'RECTANGLE':
            socketParams['u_size'] = lamp.size   / 2.0
            socketParams['v_size'] = lamp.size_y / 2.0
        else:
            socketParams['u_size'] = lamp.size / 2.0
            socketParams['v_size'] = lamp.size / 2.0
    
    # Check 'Render Elements' and add light to channels
    #
    if scene.vray.ntree:
        passesNode = NodesExport.GetNodeByType(scene.vray.ntree, 'VRayNodeRenderChannels')
        if passesNode:
            listRenderElements = {
                'channels_raw'      : [],
                'channels_diffuse'  : [],
                'channels_specular' : [],
            }

            for socket in passesNode.inputs:
                if not socket.is_linked or not socket.use:
                    continue

                lightSelectNode = NodesExport.GetConnectedNode(scene.vray.ntree, socket)
                if not lightSelectNode or not lightSelectNode.bl_idname == 'VRayNodeRenderChannelLightSelect':
                    continue

                lightsSocket = lightSelectNode.inputs['Lights']
                if not lightsSocket.is_linked:
                    continue

                lightSelectChannelName = NodesExport.GetNodeName(scene.vray.ntree, lightSelectNode)

                lightGroup = NodesExport.WriteConnectedNode(bus, scene.vray.ntree, lightsSocket)
                for l in lightGroup:
                    if not l.type == 'LAMP':
                        continue
                    if not l == ob:
                        continue

                    lightChannelType = lightSelectNode.RenderChannelLightSelect.type

                    if lightChannelType == 'RAW':
                        listRenderElements['channels_raw'].append(lightSelectChannelName)
                    elif lightChannelType == 'DIFFUSE':
                        listRenderElements['channels_diffuse'].append(lightSelectChannelName)
                    elif lightChannelType == 'SPECULAR':
                        listRenderElements['channels_specular'].append(lightSelectChannelName)

            for key in listRenderElements:
                socketParams[key] = "List(%s)" % ",".join(listRenderElements[key])

    # Write light
    ExportUtils.WritePlugin(
        bus,
        PLUGINS['LIGHT'][lightPluginName],
        lamp_name,
        lightPropGroup,
        socketParams
    )


 #######  ########        ## ########  ######  ########  ######  
##     ## ##     ##       ## ##       ##    ##    ##    ##    ## 
##     ## ##     ##       ## ##       ##          ##    ##       
##     ## ########        ## ######   ##          ##     ######  
##     ## ##     ## ##    ## ##       ##          ##          ## 
##     ## ##     ## ##    ## ##       ##    ##    ##    ##    ## 
 #######  ########   ######  ########  ######     ##     ######  

def write_node(bus):
    scene = bus['scene']
    o     = bus['output']

    ob         = bus['node']['object']
    visibility = bus['visibility']

    if not bus['node']['geometry']:
        return

    if not bus['node']['material']:
        bus['node']['material'] = bus['defaults']['material']

    VRayScene = scene.vray
    SettingsOptions = VRayScene.SettingsOptions

    # TODO: Use LightLinker instead of Node's 'lights' attribute
    #
    lights = []
    for lamp in [o for o in scene.objects if o.type == 'LAMP']:
        if lamp.data is None:
            continue

        VRayLamp = lamp.data.vray

        lamp_name = get_name(lamp, prefix='LA')

        if not utils.object_visible(bus, lamp) or lamp.hide_render:
            if not SettingsOptions.light_doHiddenLights:
                continue

        if not VRayLamp.use_include_exclude:
            utils.append_unique(lights, lamp_name)
        else:
            object_list = utils.generate_object_list(VRayLamp.include_objects, VRayLamp.include_groups)
            if VRayLamp.include_exclude == 'INCLUDE':
                if ob in object_list:
                    utils.append_unique(lights, lamp_name)
            else:
                if ob not in object_list:
                    utils.append_unique(lights, lamp_name)

    node_name = bus['node']['name']
    matrix    = bus['node']['matrix']
    base_mtl  = bus['node']['material']

    if 'dupli' in bus['node'] and 'name' in bus['node']['dupli']:
        node_name = bus['node']['dupli']['name']
        matrix    = bus['node']['dupli']['matrix']

    if 'particle' in bus['node'] and 'name' in bus['node']['particle']:
        node_name = bus['node']['particle']['name']
        matrix    = bus['node']['particle']['matrix']

    if bus['node'].get('hair', False):
        node_name += 'HAIR'

    material = base_mtl

    if not (VRayScene.RTEngine.enabled or bus['engine'] == 'VRAY_RENDER_RT'):
        material = "RS%s" % node_name

        o.set('MATERIAL', 'MtlRenderStats', material)
        o.writeHeader()
        o.writeAttibute('base_mtl', base_mtl)
        o.writeAttibute('visibility', a(scene, (0 if ob in visibility['all'] or bus['node']['visible'] == False else 1)))
        o.writeAttibute('camera_visibility', a(scene, (0 if ob in visibility['camera']  else 1)))
        o.writeAttibute('gi_visibility', a(scene, (0 if ob in visibility['gi']      else 1)))
        o.writeAttibute('reflections_visibility', a(scene, (0 if ob in visibility['reflect'] else 1)))
        o.writeAttibute('refractions_visibility', a(scene, (0 if ob in visibility['refract'] else 1)))
        o.writeAttibute('shadows_visibility', a(scene, (0 if ob in visibility['shadows'] else 1)))
        o.writeFooter()

    o.set('OBJECT', 'Node', node_name)
    o.writeHeader()
    o.writeAttibute('objectID', bus['node'].get('objectID', ob.pass_index))
    o.writeAttibute('geometry', bus['node']['geometry'])
    o.writeAttibute('material', material)
    if 'particle' in bus['node'] and 'visible' in bus['node']['particle']:
        o.writeAttibute('visible', a(scene, bus['node']['particle']['visible']))
    o.writeAttibute('transform', LibUtils.AnimatedValue(scene, matrix))
    o.writeFooter()

    # TODO: Use Light Linker
    # if not bus['preview']:
    #     ofile.write("\n\tlights=List(%s);" % (','.join(lights)))


def write_object(bus):
    scene = bus['scene']
    ob    = bus['node']['object']

    # Skip if object is just dupli-group holder
    if ob.dupli_type == 'GROUP':
        return

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    VRayObject   = ob.vray
    VRayData     = ob.data.vray

    bus['node']['name']     = get_name(ob, prefix='OB')
    bus['node']['geometry'] = get_name(ob.data if VRayExporter.use_instances else ob, prefix='ME')
    bus['node']['matrix']   = ob.matrix_world

    # If this is hair we already have all needed data in the bus
    #
    if bus['node'].get('hair', False):
        write_node(bus)
        return

    # Check if this is a particle holder and skip if needed
    if len(ob.particle_systems):
        for ps in ob.particle_systems:
            if not ps.settings.use_render_emitter:
                return

    # Export nodetree
    socketParams = {}
    if VRayObject.ntree:
        vrayOuputNode = NodesExport.GetNodeByType(VRayObject.ntree, 'VRayNodeObjectOutput')
        if vrayOuputNode:
            for nodeSocket in vrayOuputNode.inputs:
                vrayAttr = nodeSocket.vray_attr
                value = NodesExport.WriteConnectedNode(bus, VRayObject.ntree, nodeSocket)
                if value is not None:
                    socketParams[vrayAttr] = value
    else:
        socketParams['material'] = NodesExport.WriteVRayNodeBlenderOutputMaterial(bus, None, None)
        socketParams['geometry'] = NodesExport.WriteVRayNodeBlenderOutputGeometry(bus, None, None)

    PrintDict("Object \"%s\"" % ob.name, socketParams)

    bus['node']['geometry'] = socketParams.get('geometry', None)
    bus['node']['material'] = socketParams.get('material', None)

    # TODO: If 'geometry' is None, we need to check if LightMesh node was used
    # and export as Light

    write_node(bus)


def _write_object_particles_hair(bus):
    scene = bus['scene']
    o     = bus['output']
    ob    = bus['node']['object']

    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    if not VRayExporter.use_hair:
        return

    if not len(ob.particle_systems):
        return

    for ps in ob.particle_systems:
        if not (ps.settings.type == 'HAIR' and ps.settings.render_type == 'PATH'):
            continue

        ps_material = None
        ps_material_idx = ps.settings.material
        if len(ob.material_slots) >= ps_material_idx:
            if ob.material_slots[ps_material_idx - 1].material:
                ps_material = NodesExport.GetOutputName(ob.material_slots[ps_material_idx - 1].material.vray.ntree)

        hair_geom_name = LibUtils.CleanString("HAIR%s%s" % (ps.name, ps.settings.name))
        hair_node_name = "Node"+hair_geom_name

        _vray_for_blender.exportHair(
            bpy.context.as_pointer(),   # Context
            ob.as_pointer(),            # Object
            ps.as_pointer(),            # ParticleSystem
            hair_geom_name,             # Result plugin name
            o.getFileByType('GEOMETRY') # Output file
        )

        bus['node']['hair']     = True
        bus['node']['name']     = hair_node_name
        bus['node']['geometry'] = hair_geom_name
        bus['node']['material'] = ps_material

        write_node(bus)

        bus['node']['hair'] = False


def _write_object_dupli(bus):
    scene = bus['scene']
    o     = bus['output']
    ob    = bus['node']['object']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    dupli_from_particles = False
    if len(ob.particle_systems):
        for ps in ob.particle_systems:
            if ps.settings.render_type in {'OBJECT', 'GROUP'}:
                dupli_from_particles = True
                break

    if dupli_from_particles or ob.dupli_type in {'VERTS', 'FACES', 'GROUP'}:
        if VRayExporter.use_fast_dupli_export:
            _vray_for_blender.exportDupli(
                bpy.context.as_pointer(),    # Context
                ob.as_pointer(),             # Object
                o.getFileByType('OBJECT'),   # Nodes file
                o.getFileByType('GEOMETRY'), # Geometry file
            )
        else:
            ob.dupli_list_create(scene)

            for dup_id,dup_ob in enumerate(ob.dupli_list):
                parent_dupli = ""

                bus['node']['object'] = dup_ob.object
                bus['node']['base']   = ob

                # Currently processed dupli name
                dup_node_name = LibUtils.CleanString("OB%sDO%sID%i" % (ob.name,
                                                               dup_ob.object.name,
                                                               dup_id))
                dup_node_matrix = dup_ob.matrix

                # For case when dupli is inside other dupli
                if 'dupli' in bus['node'] and 'name' in bus['node']['dupli']:
                    # Store parent dupli name
                    parent_dupli   = bus['node']['dupli']['name']
                    dup_node_name += parent_dupli

                bus['node']['dupli'] =  {}
                bus['node']['dupli']['name']   = dup_node_name
                bus['node']['dupli']['matrix'] = dup_node_matrix

                _write_object(bus)

                bus['node']['object'] = ob
                bus['node']['base']   = ob

                bus['node']['dupli'] = {}
                bus['node']['dupli']['name'] = parent_dupli

            ob.dupli_list_clear()


def _write_object(bus):
    ob = bus['node']['object']

    if ob.type in {'CAMERA', 'ARMATURE', 'LATTICE'}:
        return

    # Export LAMP
    if ob.type == 'LAMP':
        write_lamp(bus)

    elif ob.type == 'EMPTY':
        # writeSceneInclude(bus)
        _write_object_dupli(bus)

    else:
        write_object(bus)
        _write_object_particles_hair(bus)

        # Parent dupli_list_create() call create all duplicates
        # even for sub duplis, so no need to process dupli again
        if 'dupli' in bus['node'] and 'matrix' not in bus['node']['dupli']:
            _write_object_dupli(bus)


def ExportObjects(bus, checkAnimated=False, checkUpdated=False):
    scene = bus['scene']

    for ob in GetObjects(bus, checkAnimated=checkAnimated, checkUpdated=checkUpdated):
        # Node struct
        bus['node'] = {
            # Currently processes object
            'object' : ob,

            # Object visibility
            'visible' : ob,

            # Attributes for particle / dupli export
            'base' : ob,
            'dupli' : {},
            'particle' : {},
        }

        _write_object(bus)


######## ########     ###    ##     ## ######## 
##       ##     ##   ## ##   ###   ### ##       
##       ##     ##  ##   ##  #### #### ##       
######   ########  ##     ## ## ### ## ######   
##       ##   ##   ######### ##     ## ##       
##       ##    ##  ##     ## ##     ## ##       
##       ##     ## ##     ## ##     ## ######## 

def ExportFrame(bus, frame=None, camera=None, checkAnimated=False, checkUpdated=False, is_preview=False):
    """
    Exports data for the specified frame
    @scene - scene
    @checkAnimated - will check for object's attr "is_animated" (TODO)
    """

    timer = time.clock()

    scene = bus['scene']

    bus.update({
        # Current frame
        'frame' : frame if frame is not None else scene.frame_current,

        # Active camera
        'camera' : camera if camera is not None else scene.camera,

        # Set of environment effects objects
        'volumes' : set(),

        # Set of fog gizmos, to exclude from 'Node' creation
        'gizmos' : set(),

        # Prevents export data duplication
        'cache' : {
            'plugins' : set(),
            'mesh'    : set(),
            'nodes'   : set(),
        },
    })

    # Should go before object export, because of 'gizmos'
    ExportSettings(bus)

    ExportObjects(bus)

    _vray_for_blender.clearCache()

    print("Frame export done in [%.2f]" % (time.clock() - timer))


def ExportAnimation(bus):
    """
    Exports scene animation
    Only works in 'VRSCENE' work
    """
    scene = bus['scene']

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    if VRayExporter.animation_type == 'FRAMEBYFRAME':
        if VRayExporter.use_still_motion_blur:
            pass
    else:
        # Store current frame
        selected_frame = scene.frame_current

        f = scene.frame_start
        while(f <= scene.frame_end):
            scene.frame_set(f)

            ExportFrame(bus, checkAnimated=VRayExporter.checkAnimated)

            f += scene.frame_step

            # Clear names cache
            _vray_for_blender.clearCache()

        # Restore selected frame
        scene.frame_set(selected_frame)


def Export(data, scene, engine, is_preview=False, is_viewport=False):
    """
    Exports scene
    Only works in 'VRSCENE' work
    """

    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    _vray_for_blender.initCache(int(VRayExporter.animation), int(VRayExporter.check_animated))

    bus = {
        # Data exporter
        'output' : VRayStream,

        # We always need to access scene data
        'scene' : scene,

        # We will override some params in case of preview
        'preview' : is_preview,

        # We need to know render engine type
        'engine' : engine,

        # Some storage
        'context' : {},

        # Visibility lists for "Hide From View"
        'visibility' : utils.get_visibility_lists(scene.camera),

        # Fail safe defaults
        'defaults' : {
            'brdf' : "BRDFNOBRDFISSET",
            'material' : "MANOMATERIALISSET",
            'texture' : "TENOTEXTUREIESSET",
            'uvwgen' : "DEFAULTUVWC",
            'blend' : "TEDefaultBlend",
        },
    }

    # If running upload scene before export
    # to free files
    #
    if VRayStream.process.is_running():
        VRayStream.socket.send("stop", result=True)
        VRayStream.socket.send("unload", result=True)

    # Set 'VRSCENE' mode to export to files
    VRayStream.setMode('VRSCENE')
    
    VRayStream.overwriteGeometry = VRayExporter.auto_meshes

    # Init output files
    # XXX: Refactor this
    err = utils.init_files(bus)
    if err:
        return err

    if VRayExporter.animation:
        ExportAnimation(bus)
    else:
        if VRayExporter.use_still_motion_blur:
            frameCurrent = scene.frame_current

            # Export current frame
            ExportFrame(bus)

            # Export next frame
            scene.frame_set(frameCurrent + 1.0)
            ExportFrame(bus, checkAnimated=VRayExporter.checkAnimated)

            # Restore frame
            scene.frame_set(frameCurrent)

        else:
            if VRayExporter.camera_loop:
                for i,ca in enumerate([ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]):
                    ExportFrame(bus, frame=i, camera=ca, checkAnimated=True)
            else:
                ExportFrame(bus, is_preview=is_preview)

    VRayStream.write('MAIN', utils.get_vrscene_template("defaults.vrscene"))

    VRayStream.closeFiles()

    _vray_for_blender.clearFrames()
    _vray_for_blender.clearCache()


def Run(scene, engine):
    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    reloadScene = VRayStream.process.is_running()

    VRayStream.initProcess(utils.get_vray_standalone_path(scene))

    if engine == 'VRAY_RENDER_RT':
        VRayStream.setProcessMode('CMD')
    else:
        VRayStream.setProcessMode('NORMAL')

    VRayStream.process.verboseLevel = int(VRayExporter.verboseLevel)
    VRayStream.process.displaySRGB = VRayExporter.display_srgb

    if not VRayExporter.autorun:
        print("V-Ray Standalone Command line:\n  %s" % ' '.join(VRayStream.process.getCommandLine()))
        return

    VRayStream.startProcess()
    if reloadScene:
        VRayStream.reload_scene()
        VRayStream.render()


def Stop():
    # Stop process
    VRayStream.stopProcess()

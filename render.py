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

from vb25.plugins import PLUGINS

from vb25.debug   import Debug, PrintDict
from vb25.lib     import utils  as LibUtils
from vb25.lib     import ExportUtils
from vb25.nodes   import export as NodesExport
from vb25.utils   import *


 ######  ######## ######## ######## #### ##    ##  ######    ######
##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##       ##          ##       ##     ##  ####  ## ##        ##
 ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
      ## ##          ##       ##     ##  ##  #### ##    ##        ##
##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
 ######  ########    ##       ##    #### ##    ##  ######    ######

def write_settings(bus):
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
                              'SettingsOutput',
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
    
    # if VRayExporter.draft:
    #     bus['files']['scene'].write("\n")
    #     bus['files']['scene'].write(get_vrscene_template("draft.vrscene"))
    
    # bus['files']['scene'].write("\n")
    # bus['files']['scene'].write(get_vrscene_template("defaults.vrscene"))

    # for key in bus['filenames']:
    #     if key in ('output', 'output_filename', 'output_loadfile', 'lightmaps', 'scene', 'DR'):
    #         # Skip some files
    #         continue

    #     if VRayDR.on:
    #         if key == 'geometry':
    #             for t in range(threadCount):
    #                 if VRayDR.type == 'WW':
    #                     ofile.write("\n#include \"//%s/%s/%s/%s_%.2i.vrscene\"" % (HOSTNAME, VRayDR.share_name, bus['filenames']['DR']['sub_dir'], os.path.basename(bus['filenames']['geometry'][:-11]), t))
    #                 else:
    #                     ofile.write("\n#include \"%s_%.2i.vrscene\"" % (bus['filenames']['DR']['prefix'] + os.sep + os.path.basename(bus['filenames']['geometry'][:-11]), t))
    #         else:
    #             if VRayDR.type == 'WW':
    #                 ofile.write("\n#include \"//%s/%s/%s/%s\"" % (HOSTNAME, VRayDR.share_name, bus['filenames']['DR']['sub_dir'], os.path.basename(bus['filenames'][key])))
    #             else:
    #                 ofile.write("\n#include \"%s\"" % (bus['filenames']['DR']['prefix'] + os.sep + os.path.basename(bus['filenames'][key])))
    #     else:
    #         if key == 'geometry':
    #             if bus['preview']:
    #                 ofile.write("\n#include \"%s\"" % os.path.join(get_vray_exporter_path(), "preview", "preview_geometry.vrscene"))
    #             else:
    #                 ofile.write("\n#include \"%s.vrscene\"" % (os.path.basename(bus['filenames']['geometry'][:-11]), t))
    #         else:
    #             if bus['preview'] and key == 'colorMapping':
    #                 if os.path.exists(bus['filenames'][key]):
    #                     ofile.write("\n#include \"%s\"" % bus['filenames'][key])
    #             else:
    #                 ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames'][key]))
    # ofile.write("\n")

    # if Includer.use:
    #     ofile.write("\n// Include additional *.vrscene files")
    #     for includeNode in Includer.nodes:
    #         if includeNode.use == True:
    #             ofile.write("\n#include \"" + bpy.path.abspath(includeNode.scene) + "\"\t\t // " + includeNode.name)


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
    # XXX: Resolve!
    #
    if False:
        listRenderElements = {
            'channels_raw'      : [],
            'channels_diffuse'  : [],
            'channels_specular' : [],
        }

        for channel in scene.vray.render_channels:
            if channel.type == 'LIGHTSELECT' and channel.use:
                channelData = channel.RenderChannelLightSelect
                channelName = "LightSelect_%s" % clean_string(channel.name)

                lampList = generateDataList(channelData.lights, 'lamps')

                if lamp in lampList:
                    key = 'channels_%s' % channelData.lower()
                    listRenderElements[key].append(channelName)

        for key in listRenderElements:
            renderChannelArray = listRenderElements[key]

            if not len(renderChannelArray):
                continue

            ofile.write("\n\t%s=List(%s);" % (key, ",".join(renderChannelArray)))

    # Write light
    ExportUtils.WritePlugin(
        bus,
        PLUGINS['LIGHT'][lightPluginName],
        lamp_name,
        lightPropGroup,
        socketParams
    )


 #######  ########        ## ########  ######  ########  ######       ###    ##    ##  #######  ########  ########  ######     ###
##     ## ##     ##       ## ##       ##    ##    ##    ##    ##     ##      ###   ## ##     ## ##     ## ##       ##    ##      ##
##     ## ##     ##       ## ##       ##          ##    ##          ##       ####  ## ##     ## ##     ## ##       ##             ##
##     ## ########        ## ######   ##          ##     ######     ##       ## ## ## ##     ## ##     ## ######    ######        ##
##     ## ##     ## ##    ## ##       ##          ##          ##    ##       ##  #### ##     ## ##     ## ##             ##       ##
##     ## ##     ## ##    ## ##       ##    ##    ##    ##    ##     ##      ##   ### ##     ## ##     ## ##       ##    ##      ##
 #######  ########   ######  ########  ######     ##     ######       ###    ##    ##  #######  ########  ########  ######     ###

def write_node(bus):
    scene = bus['scene']
    o     = bus['output']

    ob         = bus['node']['object']
    visibility = bus['visibility']

    if not bus['node']['material'] or not bus['node']['geometry']:
        return

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

        if not object_on_visible_layers(scene, lamp) or lamp.hide_render:
            if not SettingsOptions.light_doHiddenLights:
                continue

        if not VRayLamp.use_include_exclude:
            append_unique(lights, lamp_name)
        else:
            object_list = generate_object_list(VRayLamp.include_objects, VRayLamp.include_groups)
            if VRayLamp.include_exclude == 'INCLUDE':
                if ob in object_list:
                    append_unique(lights, lamp_name)
            else:
                if ob not in object_list:
                    append_unique(lights, lamp_name)

    node_name = bus['node']['name']
    matrix    = bus['node']['matrix']
    base_mtl  = bus['node']['material']

    if 'dupli' in bus['node'] and 'name' in bus['node']['dupli']:
        node_name = bus['node']['dupli']['name']
        matrix    = bus['node']['dupli']['matrix']

    if 'particle' in bus['node'] and 'name' in bus['node']['particle']:
        node_name = bus['node']['particle']['name']
        matrix    = bus['node']['particle']['matrix']

    if 'hair' in bus['node'] and bus['node']['hair'] == True:
        node_name += 'HAIR'

    material = base_mtl

    if not VRayScene.RTEngine.enabled:
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
    o.writeAttibute('transform', a(scene, transform(matrix)))
    o.writeFooter()

    # TODO: check why this was needed.
    #if not (('dupli' in bus['node'] and 'name' in bus['node']['dupli']) or ('particle' in bus['node'] and 'name' in bus['node']['particle'])):
    #   ofile.write("\n\tlights=List(%s);" % (','.join(lights)))

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

    # If 'geometry' is None, we need to check if LightMesh node was used
    # and export as Light
    #
    # TODO

    write_node(bus)


##     ##    ###    #### ########
##     ##   ## ##    ##  ##     ##
##     ##  ##   ##   ##  ##     ##
######### ##     ##  ##  ########
##     ## #########  ##  ##   ##
##     ## ##     ##  ##  ##    ##
##     ## ##     ## #### ##     ##

def _write_object_particles_hair(bus):
    scene = bus['scene']
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

        ps_material = bus['defaults']['material']
        ps_material_idx = ps.settings.material
        if len(ob.material_slots) >= ps_material_idx:
            if ob.material_slots[ps_material_idx - 1].material:
                ps_material = NodesExport.GetOutputName(ob.material_slots[ps_material_idx - 1].material.vray.ntree)

        hair_geom_name = clean_string("HAIR%s%s" % (ps.name, ps.settings.name))
        hair_node_name = "Node"+hair_geom_name

        _vray_for_blender.exportHair(
            bpy.context.as_pointer(), # Context
            ob.as_pointer(),          # Object
            ps.as_pointer(),          # ParticleSystem
            hair_geom_name,           # Result plugin name
            bus['files']['geom']      # Output file
        )

        bus['node']['hair']     = True
        bus['node']['name']     = hair_node_name
        bus['node']['geometry'] = hair_geom_name
        bus['node']['material'] = ps_material

        write_node(bus)

        bus['node']['hair'] = False


########  ##     ## ########  ##       ####          ##    ######## ##     ## #### ######## ######## ######## ########
##     ## ##     ## ##     ## ##        ##          ##     ##       ###   ###  ##     ##       ##    ##       ##     ##
##     ## ##     ## ##     ## ##        ##         ##      ##       #### ####  ##     ##       ##    ##       ##     ##
##     ## ##     ## ########  ##        ##        ##       ######   ## ### ##  ##     ##       ##    ######   ########
##     ## ##     ## ##        ##        ##       ##        ##       ##     ##  ##     ##       ##    ##       ##   ##
##     ## ##     ## ##        ##        ##      ##         ##       ##     ##  ##     ##       ##    ##       ##    ##
########   #######  ##        ######## ####    ##          ######## ##     ## ####    ##       ##    ######## ##     ##

def _write_object_dupli(bus):
    scene = bus['scene']
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
        ob.dupli_list_create(scene)

        for dup_id,dup_ob in enumerate(ob.dupli_list):
            parent_dupli = ""

            bus['node']['object'] = dup_ob.object
            bus['node']['base']   = ob

            # Currently processed dupli name
            dup_node_name = clean_string("OB%sDO%sID%i" % (ob.name,
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


##     ## ########     ###    ##    ##    ###     ######   ######  ######## ########
##     ## ##     ##   ## ##    ##  ##    ## ##   ##    ## ##    ## ##          ##        ##   ##
##     ## ##     ##  ##   ##    ####    ##   ##  ##       ##       ##          ##         ## ##
##     ## ########  ##     ##    ##    ##     ##  ######   ######  ######      ##       #########
 ##   ##  ##   ##   #########    ##    #########       ##       ## ##          ##         ## ##
  ## ##   ##    ##  ##     ##    ##    ##     ## ##    ## ##    ## ##          ##        ##   ##
   ###    ##     ## ##     ##    ##    ##     ##  ######   ######  ########    ##

def writeSceneInclude(bus):
    o   = bus['output']
    ob  = bus['node']['object']

    VRayObject = ob.vray

    if not VRayObject.overrideWithScene:
        return

    if VRayObject.sceneFilepath == "" and VRayObject.sceneDirpath == "":
        return

    vrsceneFilelist = []
    if VRayObject.sceneFilepath:
        vrsceneFilelist.append(bpy.path.abspath(VRayObject.sceneFilepath))

    if VRayObject.sceneDirpath:
        vrsceneDirpath = bpy.path.abspath(VRayObject.sceneDirpath)

        for dirname, dirnames, filenames in os.walk(vrsceneDirpath):
            for filename in filenames:
                if not filename.endswith(".vrscene"):
                    continue
                vrsceneFilelist.append(os.path.join(dirname, filename))

    # sceneFile.write("\nSceneInclude %s {" % get_name(ob, prefix='SI'))
    # sceneFile.write("\n\tfilepath=\"%s\";" % ";".join(vrsceneFilelist))
    # sceneFile.write("\n\tprefix=\"%s\";" % get_name(ob, prefix='SI'))
    # sceneFile.write("\n\ttransform=%s;" % transform(ob.matrix_world))
    # sceneFile.write("\n\tuse_transform=%s;" % p(VRayObject.sceneUseTransform))
    # sceneFile.write("\n\treplace=%s;" % p(VRayObject.sceneReplace))
    # sceneFile.write("\n\tadd_nodes=%s;" % p(VRayObject.sceneAddNodes))
    # sceneFile.write("\n\tadd_materials=%s;" % p(VRayObject.sceneAddMaterials))
    # sceneFile.write("\n\tadd_lights=%s;" % p(VRayObject.sceneAddLights))
    # sceneFile.write("\n\tadd_cameras=%s;" % p(VRayObject.sceneAddCameras))
    # sceneFile.write("\n\tadd_environment=%s;" % p(VRayObject.sceneAddEnvironment))
    # sceneFile.write("\n}\n")


def _write_object(bus):
    ob = bus['node']['object']

    if ob.type in {'CAMERA', 'ARMATURE', 'LATTICE'}:
        return

    # Export LAMP
    if ob.type == 'LAMP':
        write_lamp(bus)

    elif ob.type == 'EMPTY':
        writeSceneInclude(bus)
        _write_object_dupli(bus)

    else:
        write_object(bus)
        _write_object_particles_hair(bus)

        # Parent dupli_list_create() call create all duplicates
        # even for sub duplis, so no need to process dupli again
        if 'dupli' in bus['node'] and 'matrix' not in bus['node']['dupli']:
            _write_object_dupli(bus)


 ######   ######  ######## ##    ## ########
##    ## ##    ## ##       ###   ## ##
##       ##       ##       ####  ## ##
 ######  ##       ######   ## ## ## ######
      ## ##       ##       ##  #### ##
##    ## ##    ## ##       ##   ### ##
 ######   ######  ######## ##    ## ########

def write_scene(bus):
    scene = bus['scene']

    VRayScene = scene.vray

    VRayExporter = VRayScene.Exporter
    SettingsOptions = VRayScene.SettingsOptions

    bus['material_override'] = None

    # Fail-safe defaults
    bus['defaults'] = {}
    bus['defaults']['brdf'] = "BRDFNOBRDFISSET"
    bus['defaults']['material'] = "MANOMATERIALISSET"
    bus['defaults']['texture'] = "TENOTEXTUREIESSET"
    bus['defaults']['uvwgen'] = "DEFAULTUVWC"
    bus['defaults']['blend'] = "TEDefaultBlend"

    # if bus['preview']:
    #     bus['files']['scene'].write(get_vrscene_template("preview.vrscene"))

    # Write override material     
    if SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
        overrideMaterial = get_data_by_name(scene, 'materials', SettingsOptions.mtl_override)
        overrideNtree = overrideMaterial.vray.ntree
        if overrideNtree:
            bus['material_override'] = NodesExport.WriteVRayMaterialNodeTree(bus, overrideNtree, force=True)

    def write_frame(bus):
        timer = time.clock()
        scene = bus['scene']

        debug(scene, "Writing frame %i..." % scene.frame_current)

        VRayScene       = scene.vray
        VRayExporter    = VRayScene.Exporter
        SettingsOptions = VRayScene.SettingsOptions

        # Prepare exclude for effects
        bus['object_exclude'] = set()

        # Cache names to prevent multiple export
        bus['cache']['nodes'] = set()
        bus['cache']['mesh'] = set()
        bus['cache']['plugins'] = set()

        # Write environment and effects
        PLUGINS['SETTINGS']['SettingsEnvironment'].write(bus)

        # Prepare objects
        bus['objects']= []
        for ob in scene.objects:
            if ob.type in {'CAMERA', 'ARMATURE', 'LATTICE'}:
                continue
            if ob.name not in bus['object_exclude']:
                bus['objects'].append(ob)
                # if LibUtils.IsAnimated(ob):
                #     print("Object %s is animated!" % ob.name)

        # Camera
        bus['camera']= scene.camera

        # Visibility list for "Hide from view" and "Camera loop" features
        bus['visibility']= get_visibility_lists(bus['camera'])

        # "Hide from view" debug data
        if VRayExporter.debug:
            print_dict(scene, "Hide from view", bus['visibility'])

        for ob in bus['objects']:
            if not object_visible(bus, ob):
                continue

            debug(scene, "{0}: {1:<32}".format(ob.type, color(ob.name, 'green')), VRayExporter.debug)

            # Node struct
            bus['node']= {}

            # Currently processes object
            bus['node']['object']= ob

            # Object visibility
            bus['node']['visible']= ob

            # We will know if object has displace
            # only after material export
            bus['node']['displace']= {}

            # We will know if object is mesh light
            # only after material export
            bus['node']['meshlight']= {}

            # If object has particles or dupli
            bus['node']['base']= ob
            bus['node']['dupli']= {}
            bus['node']['particle']= {}

            _write_object(bus)

        # PLUGINS['SETTINGS']['BakeView'].write(bus)
        # PLUGINS['SETTINGS']['RenderView'].write(bus)

        # PLUGINS['CAMERA']['CameraPhysical'].write(bus)
        # PLUGINS['CAMERA']['CameraStereoscopic'].write(bus)

        debug(scene, "Writing frame {0}... done {1:<64}".format(scene.frame_current, "[%.2f]"%(time.clock() - timer)))

    timer= time.clock()

    debug(scene, "Writing scene...")

    if bus['preview']:
        write_frame(bus)
        return False

    if VRayExporter.animation and VRayExporter.animation_type in {'FULL', 'NOTMESHES'}:
        selected_frame= scene.frame_current
        f= scene.frame_start
        while(f <= scene.frame_end):
            scene.frame_set(f)
            write_frame(bus)
            f+= scene.frame_step
        scene.frame_set(selected_frame)
    else:
        if VRayExporter.camera_loop:
            if bus['cameras']:
                for i,camera in enumerate(bus['cameras']):
                    bus['camera'] = camera
                    bus['camera_index'] = i
                    VRayExporter.customFrame = i+1
                    write_frame(bus)
            else:
                debug(scene, "No cameras selected for \"Camera loop\"!", error= True)
                return True

        else:
            write_frame(bus)

    debug(scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))

    return None


########  ##     ## ##    ##
##     ## ##     ## ###   ##
##     ## ##     ## ####  ##
########  ##     ## ## ## ##
##   ##   ##     ## ##  ####
##    ##  ##     ## ##   ###
##     ##  #######  ##    ##

def run(bus):
    scene = bus['scene']

    VRayScene = scene.vray

    VRayExporter = VRayScene.Exporter
    VRayDR       = VRayScene.VRayDR
    RTEngine     = VRayScene.RTEngine

    vray_exporter=   get_vray_exporter_path()
    vray_standalone= get_vray_standalone_path(scene)

    resolution_x= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
    resolution_y= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

    params = []
    params.append(vray_standalone)
    params.append('-sceneFile=%s' % Quotes(bus['output'].getSceneFilepath()))

    preview_file     = os.path.join(tempfile.gettempdir(), "preview.jpg")
    preview_loadfile = os.path.join(tempfile.gettempdir(), "preview.0000.jpg")
    image_file = os.path.join(bus['filenames']['output'], bus['filenames']['output_filename'])
    load_file  = preview_loadfile if bus['preview'] else os.path.join(bus['filenames']['output'], bus['filenames']['output_loadfile'])

    if scene.render.threads_mode == 'FIXED':
        params.append('-numThreads=%i' % scene.render.threads)

    if bus['preview']:
        params.append('-imgFile=%s' % Quotes(preview_file))
        params.append('-showProgress=0')
        params.append('-display=0')
        params.append('-autoclose=1')
        params.append('-verboseLevel=0')

    else:
        if RTEngine.enabled or scene.render.engine == 'VRAY_RENDER_RT':
            params.append('-cmdMode=1')

        if scene.render.engine == 'VRAY_RENDER_RT':
            params.append('-autoclose=1')
            params.append('-display=1')
            params.append('-setfocus=0')
            params.append('-showProgress=0')
            params.append('-verboseLevel=0')
        else:
            params.append('-display=%i' % VRayExporter.display)
            params.append('-verboseLevel=%s' % VRayExporter.verboseLevel)

            if VRayExporter.image_to_blender and VRayExporter.auto_save_render:
                params.append('-autoclose=1')
        
        if scene.render.use_border:
            x0 = resolution_x * scene.render.border_min_x
            y0 = resolution_y * (1.0 - scene.render.border_max_y)
            x1 = resolution_x * scene.render.border_max_x
            y1 = resolution_y * (1.0 - scene.render.border_min_y)

            region = 'crop' if scene.render.use_crop_to_border else 'region'
            params.append("-%s=%i;%i;%i;%i" % (region, x0, y0, x1, y1))

        if VRayExporter.use_still_motion_blur:
            params.append("-frames=%d" % scene.frame_end)
        else:
            if VRayExporter.animation:
                params.append("-frames=")
                if VRayExporter.animation_type == 'FRAMEBYFRAME':
                    params.append("%d" % scene.frame_current)
                else:
                    params.append("%d-%d,%d" % (scene.frame_start, scene.frame_end, int(scene.frame_step)))
            elif VRayExporter.camera_loop:
                if bus['cameras']:
                    params.append("-frames=1-%d,1" % len(bus['cameras']))
            # else:
            #   params.append("%d" % scene.frame_current)

        if VRayDR.on:
            if len(VRayDR.nodes):
                params.append('-distributed=1')
                params.append('-portNumber=%i' % VRayDR.port)
                params.append('-renderhost=%s' % Quotes(';'.join([n.address for n in VRayDR.nodes])))
                params.append('-include=%s' % Quotes(bus['filenames']['DR']['shared_dir'] + os.sep))

        if VRayExporter.auto_save_render or VRayExporter.image_to_blender:
            params.append('-imgFile=%s' % Quotes(image_file))

    if PLATFORM == "linux":
        if VRayExporter.log_window:
            LOG_TERMINAL = {
                'DEFAULT' : 'xterm',
                'XTERM'   : 'xterm',
                'GNOME'   : 'gnome-terminal',
                'KDE'     : 'konsole',
                'CUSTOM'  : VRayExporter.log_window_term,
            }

            log_window = []
            if VRayExporter.log_window_type in ['DEFAULT', 'XTERM']:
                log_window.append("xterm")
                log_window.append("-T")
                log_window.append("VRAYSTANDALONE")
                log_window.append("-geometry")
                log_window.append("90x10")
                log_window.append("-e")
                log_window.extend(params)
            else:
                log_window.extend(LOG_TERMINAL[VRayExporter.log_window_type].split(" "))
                log_window.append("-e")
                if VRayExporter.log_window_type == "GNOME":
                    log_window.append("\"%s\"" % (" ".join(params)))
                else:
                    log_window.extend(params)
            params = log_window

    if (VRayExporter.autoclose
        or (VRayExporter.animation and VRayExporter.animation_type == 'FRAMEBYFRAME')
        or (VRayExporter.animation and VRayExporter.animation_type == 'FULL' and VRayExporter.use_still_motion_blur)):
        params.append('-autoclose=1')

    engine = bus['engine']

    if VRayExporter.display_srgb:
        params.append('-displaySRGB=1')

    # If this is a background task, wait until render end
    # and no VFB is required
    if bpy.app.background or VRayExporter.wait:
        if bpy.app.background:
            params.append('-display=0')   # Disable VFB (TODO: add configuration option)
            params.append('-autoclose=1') # Exit on render end
        subprocess.call(params)
        return

    if VRayExporter.use_feedback:
        if scene.render.use_border:
            return

        proc = VRayProcess()
        proc.sceneFile = bus['filenames']['scene']
        proc.imgFile   = image_file
        proc.scene     = scene

        proc.set_params()
        proc.run()

        feedback_image = os.path.join(get_ram_basedir(), "vrayblender_%s_stream.jpg"%(get_username()))

        proc_interrupted = False

        render_result_image = None

        if engine is None:
            return

            # TODO: try finish this
            if RTEngine.enabled:
                render_result_name = "VRay Render"

                if render_result_name not in bpy.data.images:
                    bpy.ops.image.new(name=render_result_name, width=resolution_x, height=resolution_y, color=(0.0, 0.0, 0.0), alpha=True, generated_type='BLANK', float=False)
                    render_result_image.source   = 'FILE'
                    render_result_image.filepath = feedback_image

                render_result_image = bpy.data.images[render_result_name]

                def task():
                    global proc

                    if not proc.is_running():
                        return

                    err = proc.recieve_image(feedback_image)

                    if err is None:
                        try:
                            render_result_image.reload()

                            for window in bpy.context.window_manager.windows:
                                for area in window.screen.areas:
                                    if area.type == 'IMAGE_EDITOR':
                                        for space in area.spaces:
                                            if space.type == 'IMAGE_EDITOR':
                                                if space.image.name == render_result_name:
                                                    area.tag_redraw()
                                                    return
                        except:
                            return

                def my_timer():
                    t = Timer(0.25, my_timer)
                    t.start()
                    task()

                my_timer()

        else:
            while True:
                time.sleep(0.25)

                if engine.test_break():
                    proc_interrupted = True
                    debug(None, "Process is interrupted by the user")
                    break

                err = proc.recieve_image(feedback_image)
                if VRayExporter.debug:
                    debug(None, "Recieve image error: %s"%(err))
                if err is None:
                    load_result(engine, resolution_x, resolution_y, feedback_image)

                if proc.exit_ready:
                    break

                if VRayExporter.use_progress:
                    msg, prog = proc.get_progress()
                    if prog is not None and msg is not None:
                        engine.update_stats("", "V-Ray: %s %.0f%%"%(msg, prog*100.0))
                        engine.update_progress(prog)

                if proc.exit_ready:
                    break

            proc.kill()

            # Load final result image to Blender
            if VRayExporter.image_to_blender and not proc_interrupted:
                if load_file.endswith('vrimg'):
                    # VRayImage (.vrimg) loaing is not supported
                    debug(None, "VRayImage loading is not supported. Final image will not be loaded.")
                else:
                    debug(None, "Loading final image: %s"%(load_file))
                    load_result(engine, resolution_x, resolution_y, load_file)

    else:
        if not VRayExporter.autorun:
            debug(scene, "Command: %s" % ' '.join(params))
            return

        process = subprocess.Popen(params)

        if VRayExporter.animation and (VRayExporter.animation_type == 'FRAMEBYFRAME' or (VRayExporter.animation_type == 'FULL' and VRayExporter.use_still_motion_blur)):
            process.wait()
            return

        if not isinstance(engine, bpy.types.RenderEngine):
            return

        if engine is not None and (bus['preview'] or VRayExporter.image_to_blender) and not scene.render.use_border:
            while True:
                if engine.test_break():
                    try:
                        process.kill()
                    except:
                        pass
                    break

                if process.poll() is not None:
                    try:
                        if not VRayExporter.animation:
                            result= engine.begin_result(0, 0, resolution_x, resolution_y)
                            layer= result.layers[0]
                            layer.load_from_file(load_file)
                            engine.end_result(result)
                    except:
                        pass
                    break

                time.sleep(0.1)


def export_and_run(bus):
    err = write_scene(bus)

    write_settings(bus)

    if not err:
        run(bus)


#### ##    ## #### ########
 ##  ###   ##  ##     ##
 ##  ####  ##  ##     ##
 ##  ## ## ##  ##     ##
 ##  ##  ####  ##     ##
 ##  ##   ###  ##     ##
#### ##    ## ####    ##

def init_bus(engine, scene, preview=False):
    VRayScene = scene.vray
    VRayExporter = VRayScene.Exporter

    bus = {}
    bus['mode'] = 'VRSCENE'
    bus['scene']   = scene
    bus['preview'] = preview
    bus['files']     = {}
    bus['filenames'] = {}

    bus['volumes'] = set()
    bus['context'] = {}
    bus['cache'] = {
        'plugins' : set(),
        'mesh'    : set(),
        'nodes'   : set(),
    }

    init_files(bus)

    # Camera loop
    bus['cameras'] = None
    if VRayExporter.camera_loop:
        bus['cameras'] = [ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]

    # Render engine
    bus['engine']= engine

    return bus


########  ######## ##    ## ########  ######## ########
##     ## ##       ###   ## ##     ## ##       ##     ##
##     ## ##       ####  ## ##     ## ##       ##     ##
########  ######   ## ## ## ##     ## ######   ########
##   ##   ##       ##  #### ##     ## ##       ##   ##
##    ##  ##       ##   ### ##     ## ##       ##    ##
##     ## ######## ##    ## ########  ######## ##     ##

def render(engine, scene, preview= None):
    VRayScene    = scene.vray
    VRayExporter = VRayScene.Exporter

    if preview:
        export_and_run(init_bus(engine, scene, True))
        return None

    if VRayExporter.use_still_motion_blur:
        # Store current settings
        e_anim_state = VRayExporter.animation
        e_anim_type  = VRayExporter.animation_type
        frame_start = scene.frame_start
        frame_end   = scene.frame_end

        # Run export
        if e_anim_state:
            if e_anim_type not in ['FRAMEBYFRAME']:
                return "\"Still Motion Blur\" feature works only in \"Frame-By-Frame\" animation mode!"

            VRayExporter.animation_type = 'FULL'

            f = frame_start
            while(f <= frame_end):
                scene.frame_start = f - 1
                scene.frame_end   = f

                export_and_run(init_bus(engine, scene))

                f += scene.frame_step

        else:
            VRayExporter.animation = True
            VRayExporter.animation_type = 'FULL'

            scene.frame_start = scene.frame_current - 1
            scene.frame_end   = scene.frame_current

            export_and_run(init_bus(engine, scene))

        # Restore settings
        VRayExporter.animation = e_anim_state
        VRayExporter.animation_type = e_anim_type
        scene.frame_start = frame_start
        scene.frame_end   = frame_end

    else:
        if VRayExporter.animation:
            if VRayExporter.animation_type == 'FRAMEBYFRAME':
                selected_frame = scene.frame_current

                f = scene.frame_start
                while(f <= scene.frame_end):
                    scene.frame_set(f)
                    export_and_run(init_bus(engine, scene))
                    f += scene.frame_step

                scene.frame_set(selected_frame)
            else:
                export_and_run(init_bus(engine, scene))
        else:
            export_and_run(init_bus(engine, scene))

    return None

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
import mathutils

from vb30.lib import ExportUtils
from vb30.lib import LibUtils


TYPE = 'EFFECT'
ID   = 'PhxShaderSim'
NAME = 'Phoenix Data'
DESC = ""

PluginParams = (
    {
        'attr' : 'cache',
        'desc' : "The phoenix cache that will be used with this simulator",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'play_speed',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'enabled',
        'desc' : "set to false to disable. ",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'render',
        'desc' : "set to false to disable rendering. The data is still loaded and Phoenix textures and emissive lights will still work",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'contentTime',
        'desc' : "force using an externally set content time",
        'type' : 'INT',
        'default' : -1,
    },
    {
        'attr' : 'node_transform',
        'desc' : "The transformation matrix for the instance that uses this simulator",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'wind_from_movement',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'unit_scale',
        'desc' : "The scaling between simulation and scene units",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'frame_duration',
        'desc' : "Override the frame duration in the cache",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'sarg',
        'desc' : "0-texture; 1-T; 2-Sm; 3-V; 10-fuel",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'stex',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'surflevel',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1000,
    },
    {
        'attr' : 'solidbelow',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'displacement',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'displ2d',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'displmul',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'displ0',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'displ1',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'displ2',
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'rendstep',
        'desc' : "",
        'type' : 'INT',
        'default' : 50,
    },
    {
        'attr' : 'lightcache',
        'desc' : "if true, a light cache will be used for diffuse lighting",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'lightcachesr',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'pmbounces',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'heathaze',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'hhfactor',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'rendsolid',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'geommode',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'left_handed_coord',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'jitter',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'softb',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'difmul',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'sampler',
        'desc' : "0-trunc; 1-linear; 2-spherical",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'smoketransp',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'stoptransp',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.99,
    },
    {
        'attr' : 'skiptransp',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'play_speed',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'noscatter',
        'desc' : "0-enabled; 1-disabled; 2-analytic; 3-analytic+shadows",
        'type' : 'INT',
        'default' : 2,
    },
    {
        'attr' : 'transpmode',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'bias',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'usebias',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'wrapx',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'wrapy',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'wrapz',
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'lightlinks',
        'desc' : "light linking list used in volumetric mode",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bounces',
        'desc' : "max GI bounces",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'velocity_mult',
        'desc' : "Velocity multiplier for the volume renderer",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'velocities_from_uvw',
        'desc' : "Create velocity channel from uvw movement",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mesher',
        'desc' : "If true, use mesher to generate runtime vray static mesh",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'smoothmesh',
        'desc' : "Mesh smoothing iterations",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'meshsubdiv',
        'desc' : "Mesh skyline subdivisions",
        'type' : 'FLOAT',
        'default' : 2,
    },
    {
        'attr' : 'darksky',
        'desc' : "Mesh skyline darkening",
        'type' : 'FLOAT',
        'default' : 0.5,
    },
    {
        'attr' : 'ocean',
        'desc' : "If true, generate 'ocean' geometry outisde the simulator",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'oceanlevel',
        'desc' : "Mesh 'ocean' level",
        'type' : 'FLOAT',
        'default' : 50,
    },
    {
        'attr' : 'mod_e',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'earg',
        'desc' : "0-disabled; 1-T; 2-Sm; 3-V; 4-texture; 10-fuel",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'etex',
        'name' : "Emission",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'ecolor',
        'desc' : "raw emissive table",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'ecolor_positions',
        'desc' : "positions of the emission color ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'ecolor_colors',
        'desc' : "colors of the emission color ramp",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'ecolor_interpolations',
        'desc' : "0: none, 1: linear, 2: smooth, 3: spline",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'elum_positions',
        'desc' : "positions of the luminance ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'elum_values',
        'desc' : "values of the luminance ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'elum_interpolations',
        'desc' : "0: none, 1: linear, 2: smooth, 3: spline",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'ecolor_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'ecolor_scale',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'emult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'no_alpha_e',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'mod_d',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'darg',
        'desc' : "0-disabled; 1-T; 2-Sm; 3-V; 4-texture; 5-simple color; 10-fuel",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'dtex',
        'name' : "Diffuse",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'dcolor',
        'desc' : "raw diffuse table",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'dcolor_positions',
        'desc' : "positions of the diffuse color ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'dcolor_colors',
        'desc' : "colors of the diffuse color ramp",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'dcolor_interpolations',
        'desc' : "0: none, 1: linear, 2: smooth, 3: spline",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'dcolor_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'dcolor_scale',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'simple_color',
        'desc' : "",
        'type' : 'COLOR',
        'default' : (0.2, 0.2, 0.2),
    },
    {
        'attr' : 'mod_t',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'targ',
        'desc' : "0-simple smoke; 1-T; 2-Sm; 3-V; 4-texture; 10-fuel",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'ttex',
        'name' : "Transparency",
        'desc' : "",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'transp',
        'desc' : "raw transparency table",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'transp_positions',
        'desc' : "positions of the transparency ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'transp_values',
        'desc' : "values of the transparency ramp",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'transp_interpolations',
        'desc' : "0: none, 1: linear, 2: smooth, 3: spline",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'transp_offset',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'transp_scale',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'transp_power',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'shadow_opacity',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'cell_aspect',
        'desc' : "Cell stretch aspect for the 3 axis",
        'type' : 'FLOAT',
        'default' : 1.0,
    },
    {
        'attr' : 'varg',
        'desc' : "0-normal velocity; 2-texture",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'vtex',
        'desc' : "velocity texture",
        'type' : 'TEXTURE',
        'default' : (0, 0, 0, 0),
    },
    {
        'attr' : 'mod_v',
        'desc' : "",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'velocities',
        'desc' : "Specify directly the velocities in distance per frame",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'usegizmo',
        'desc' : "enable using of gizmos",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'invgizmo',
        'desc' : "invert meaning of gizmos",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'gizmo',
        'desc' : "geometry to define the rendering volume",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'gizmo_transform',
        'desc' : "world transformation of the gizmo",
        'type' : 'TRANSFORM',
        'default' : None,
    },
    {
        'attr' : 'al_enable',
        'desc' : "enable the additional emissive lights",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'lights',
        'desc' : "additional number of emissive lights",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'al_placing',
        'desc' : "emissive lights placement type, 0-simple, 1-inside",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'al_sampling',
        'desc' : "sampling type, 0-simple, 1-DMC",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'al_subdivs',
        'desc' : "number of subdivision for the DMC light sampling",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'al_csubdivs',
        'desc' : "number of caustics subdivision for lights",
        'type' : 'INT',
        'default' : 1000,
    },
    {
        'attr' : 'persistlights',
        'desc' : "if true, the emissive lights will be created, even the volume is not renderable",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'selfshadow',
        'desc' : "if 1, the emission lights will cast raytraced shadows to the volume. if 2, a grid map will be used to determine illumination",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'gridreduct',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 10,
    },
    {
        'attr' : 'lightsmult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'lightscut',
        'desc' : "cut off threshold for the lights",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'radmult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'self_illum_map_min_pow',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 0.1,
    },
    {
        'attr' : 'generate_gi',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'receive_gi',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'gen_gi_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'rec_gi_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'generate_caust',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'receive_caust',
        'desc' : "",
        'type' : 'INT',
        'default' : 1,
    },
    {
        'attr' : 'caust_mult',
        'desc' : "",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'camera_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'reflections_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'refractions_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'gi_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'shadows_visibility',
        'desc' : "",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'use_progressive',
        'desc' : "Use progressive rendering, instead of single sample",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'channels',
        'desc' : "Render channels the result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_raw',
        'desc' : "Render channels the raw diffuse result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_diffuse',
        'desc' : "Render channels the diffuse result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'channels_specular',
        'desc' : "Render channels the specular result of this light will be written to",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'material_id',
        'desc' : "Material ID",
        'type' : 'COLOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'volnorm',
        'desc' : "if true, write to normals in volume mode",
        'type' : 'INT',
        'default' : 0,
    },
    {
        'attr' : 'volzdepth',
        'desc' : "if true, write to the z-depth render element",
        'type' : 'INT',
        'default' : 0,
    },
)


def writePhxShaderTexAlpha(bus, ttex=""):
    scene = bus['scene']
    o     = bus['output']

    texName = "%s@Alpha" % ttex.replace("::","")

    o.set('EFFECT', 'PhxShaderTexAlpha', texName)
    o.writeHeader()
    o.writeAttibute('ttex', ttex)
    o.writeAttibute('transparency', 'AColor(0.5,0.5,0.5,1.0)')
    o.writeFooter()

    return texName


def writeTexMayaFluidTransformed(bus, fluid_tex="", fluid_value_scale=1.0):
    scene = bus['scene']
    o     = bus['output']

    texName = "%s@Tm" % fluid_texc

    o.set('EFFECT', 'TexMayaFluidTransformed', texName)
    o.writeHeader()
    o.writeAttibute('fluid_tex', fluid_tex)
    o.writeAttibute('fluid_value_scale', 1.0)
    o.writeAttibute('dynamic_offset_x', 0)
    o.writeAttibute('dynamic_offset_y', 0)
    o.writeAttibute('dynamic_offset_z', 0)
    o.writeFooter()

    return texName


def writeDatablock(bus, pluginModule, pluginName, propGroup, overrideParams):
    scene = bus['scene']
    o     = bus['output']

    cache = overrideParams.get('cache')
    if cache is None:
        return None
    if type(cache) is list:
        cache = cache[0]
    if not cache:
        return None

    smd = LibUtils.GetSmokeModifier(cache)
    if not smd:
        return None

    cachePluginName = "%s@Cache" % pluginName

    o.set('EFFECT', 'PhxShaderCache', cachePluginName)
    o.writeHeader()
    o.writeAttibute('grid_size_x', smd.domain_settings.domain_resolution[0])
    o.writeAttibute('grid_size_y', smd.domain_settings.domain_resolution[1])
    o.writeAttibute('grid_size_z', smd.domain_settings.domain_resolution[2])
    o.writeFooter()

    for key in {'dtex', 'etex', 'ttex'}:
        if type(overrideParams[key]) is not str:
            continue
        overrideParams[key] = overrideParams[key].replace("::out_density", "@Density")
        overrideParams[key] = overrideParams[key].replace("::out_flame",   "@Flame")
        overrideParams[key] = overrideParams[key].replace("::out_fuel",    "@Fuel")

    ttex = overrideParams.get('ttex')
    ttex = writePhxShaderTexAlpha(bus, ttex)

    # To match Phoenix container
    #
    node_transform = cache.matrix_world.copy()
    sca_tm = mathutils.Matrix.Identity(4)
    sca_tm[0][0], sca_tm[1][1], sca_tm[2][2] = 2.0,2.0,2.0
    node_transform = node_transform * sca_tm

    overrideParams.update({
        'node_transform' : node_transform,
        'cache' : cachePluginName,
        'darg' : 4,
        'earg' : 4,
        'targ' : 4,
        'ttex' : ttex,
    })

    if False:
        return ExportUtils.WritePluginCustom(bus, pluginModule, pluginName, propGroup, overrideParams)
    else:
        o.set(pluginModule.TYPE, pluginModule.ID, pluginName)
        o.writeHeader()
        o.writeAttibute('node_transform', node_transform);
        o.writeAttibute('cache', cachePluginName)
        o.writeAttibute('darg', 4)
        o.writeAttibute('dtex', overrideParams['dtex'])
        o.writeAttibute('earg', 4)
        o.writeAttibute('etex', overrideParams['etex'])
        o.writeAttibute('targ', 4)
        o.writeAttibute('ttex', overrideParams['ttex'])
        o.writeAttibute('camera_visibility', 1)
        o.writeAttibute('cell_aspect', 'ListFloat(1.0,1.0,1.0)')
        o.writeAttibute('enabled', 1)
        o.writeAttibute('jitter', 1)
        o.writeAttibute('rendstep', propGroup.rendstep)
        o.writeAttibute('shadow_opacity', 0.5)
        o.writeAttibute('shadows_visibility', 1)
        o.writeAttibute('transpmode', 1)
        o.writeAttibute('no_alpha_e', 0)
        o.writeAttibute('lightcache', 1)
        o.writeAttibute('noscatter', 1)
        o.writeAttibute('bounces', 1)
        o.writeFooter()

    # To exclude object from Node creation
    #
    bus['gizmos'].add(cache.name)

    return pluginName

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

import os
import sys
import math

import bpy
from bpy.props import *

from vb30.compat.utils import *


# PLUGINS = {
#     'BRDF':          {},
#     'CAMERA':        {},
#     'GEOMETRY':      {},
#     'LIGHT':         {},
#     'MATERIAL':      {},
#     'OBJECT':        {},
#     'RENDERCHANNEL': {},
#     'SETTINGS':      {},
#     'SLOT':          {},
#     'TEXTURE':       {},
#     'WORLD':         {},
#
#     'NODE':          {},
# }
#
#
# plugins_dir = os.path.dirname(__file__)
# if not plugins_dir in sys.path:
#     sys.path.append(plugins_dir)
#
# plugins_files= [fname[:-3] for fname in os.listdir(plugins_dir) if fname and fname.endswith(".py") and not fname == "__init__.py"]
# plugins= [__import__(fname) for fname in plugins_files]
#
# for plugin in plugins:
#     PLUGINS[plugin.TYPE][plugin.ID]= plugin


class VRaySlot(bpy.types.PropertyGroup):
    uv_layer = StringProperty(
        name        = "UV Map",
        description = "UV map to use",
        default     = ""
    )

    offset = FloatVectorProperty(
        subtype = 'TRANSLATION',
        size = 2,
        default = (0.0,0.0),
    )

    scale = FloatVectorProperty(
        name = "Coverage",
        subtype = 'TRANSLATION',
        size = 2,
        default = (1.0,1.0),
    )

    # Move to Slot plugin
    uvwgen= StringProperty(
        name= "UVW Generator",
        subtype= 'NONE',
        options= {'HIDDEN'},
        description= "UVW generator name",
        default= "UVWGenChannel_default"
    )

    blend_mode= EnumProperty(
        name= "Blend mode",
        description= "Blend mode",
        items= (
            ('NONE',        "None",       ""),
            ('OVER',        "Over",       ""),
            ('IN',          "In",         ""),
            ('OUT',         "Out",        ""),
            ('ADD',         "Add",        ""),
            ('SUBTRACT',    "Subtract",   ""),
            ('MULTIPLY',    "Multiply",   ""),
            ('DIFFERENCE',  "Difference", ""),
            ('LIGHTEN',     "Lighten",    ""),
            ('DARKEN',      "Darken",     ""),
            ('SATURATE',    "Saturate",   ""),
            ('DESATUREATE', "Desaturate", ""),
            ('ILLUMINATE',  "Illuminate", ""),
        ),
        default= 'OVER'
    )

    texture_rot= FloatProperty(
        name= "Rotation",
        description= "Texture rotation",
        subtype= 'ANGLE',
        min= -2.0 * math.pi,
        max=  2.0 * math.pi,
        soft_min= -math.pi,
        soft_max=  math.pi,
        default= 0.0
    )

    texture_rotation_h= FloatProperty(
        name= "Horiz. rotation",
        description= "Horizontal rotation",
        subtype= 'ANGLE',
        min= -2.0 * math.pi,
        max=  2.0 * math.pi,
        soft_min= -math.pi,
        soft_max=  math.pi,
        default= 0.0
    )

    texture_rotation_v= FloatProperty(
        name= "Vert. rotation",
        description= "Vertical rotation",
        subtype= 'ANGLE',
        min= -2.0 * math.pi,
        max=  2.0 * math.pi,
        soft_min= -math.pi,
        soft_max=  math.pi,
        default= 0.0
    )

    texture_rotation_w= FloatProperty(
        name= "W rotation",
        description= "W rotation",
        subtype= 'ANGLE',
        min= -2.0 * math.pi,
        max=  2.0 * math.pi,
        soft_min= -math.pi,
        soft_max=  math.pi,
        default= 0.0
    )

    '''
      MAPTO
    '''
    map_diffuse= BoolProperty(
        name= "Diffuse",
        description= "Diffuse texture",
        default= True
    )

    map_diffuse_invert= BoolProperty(
        name= "Invert diffuse",
        description= "Invert diffuse texture",
        default= False
    )

    diffuse_mult= FloatProperty(
        name= "Diffuse texture multiplier",
        description= "Diffuse texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_displacement= BoolProperty(
        name= "Displacement",
        description= "Displacement texture",
        default= False
    )

    map_displacement_invert= BoolProperty(
        name= "Invert displacement texture",
        description= "Invert displacement texture",
        default= False
    )

    displacement_mult= FloatProperty(
        name= "Displacement texture multiplier",
        description= "Displacement texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_normal= BoolProperty(
        name= "Normal",
        description= "Normal texture",
        default= False
    )

    map_normal_invert= BoolProperty(
        name= "Invert normal texture",
        description= "Invert normal texture",
        default= False
    )

    normal_mult= FloatProperty(
        name= "Normal texture multiplier",
        description= "Normal texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_opacity= BoolProperty(
        name= "Opacity",
        description= "Opacity texture",
        default= False
    )

    map_opacity_invert= BoolProperty(
        name= "Invert opacity texture",
        description= "Invert opacity texture",
        default= False
    )

    opacity_mult= FloatProperty(
        name= "Opacity texture multiplier",
        description= "Opacity texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_roughness= BoolProperty(
        name= "Roughness",
        description= "Roughness texture",
        default= False
    )

    map_roughness_invert= BoolProperty(
        name= "Invert roughness texture",
        description= "Invert roughness texture",
        default= False
    )

    roughness_mult= FloatProperty(
        name= "Roughness texture multiplier",
        description= "Roughness texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_reflect= BoolProperty(
        name= "Reflection",
        description= "Reflection texture",
        default= False
    )

    map_reflect_invert= BoolProperty(
        name= "Invert reflection texture",
        description= "Invert reflection texture",
        default= False
    )

    map_reflect_invert= BoolProperty(
        name= "Invert reflection",
        description= "Invert reflection texture",
        default= False
    )

    reflect_mult= FloatProperty(
        name= "Reflection texture multiplier",
        description= "Reflection texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_reflect_glossiness= BoolProperty(
        name= "Reflection glossiness",
        description= "Reflection glossiness texture",
        default= False
    )

    map_reflect_glossiness_invert= BoolProperty(
        name= "Invert reflection glossiness texture",
        description= "Invert reflection glossiness texture",
        default= False
    )

    reflect_glossiness_mult= FloatProperty(
        name= "Reflection glossiness texture multiplier",
        description= "Reflection glossiness texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_hilight_glossiness= BoolProperty(
        name= "Hilight glossiness",
        description= "Hilight glossiness texture",
        default= False
    )

    map_hilight_glossiness_invert= BoolProperty(
        name= "Invert hilight_glossiness texture",
        description= "Invert hilight_glossiness texture",
        default= False
    )

    hilight_glossiness_mult= FloatProperty(
        name= "Hilight glossiness texture multiplier",
        description= "Hilight glossiness texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_anisotropy= BoolProperty(
        name= "Anisotropy",
        description= "Anisotropy texture",
        default= False
    )

    map_anisotropy_invert= BoolProperty(
        name= "Invert anisotropy texture",
        description= "Invert anisotropy texture",
        default= False
    )

    anisotropy_mult= FloatProperty(
        name= "Anisotropy texture multiplier",
        description= "Anisotropy texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_anisotropy_rotation= BoolProperty(
        name= "Anisotropy rotation",
        description= "Anisotropy rotation texture",
        default= False
    )

    map_anisotropy_rotation_invert= BoolProperty(
        name= "Invert anisotropy rotation texture",
        description= "Invert anisotropy rotation texture",
        default= False
    )

    anisotropy_rotation_mult= FloatProperty(
        name= "Anisotropy rotation texture multiplier",
        description= "Anisotropy rotation texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_fresnel_ior= BoolProperty(
        name= "Fresnel IOR",
        description= "Fresnel IOR texture",
        default= False
    )

    map_fresnel_ior_invert= BoolProperty(
        name= "Invert fresnel IOR texture",
        description= "Invert fresnel IOR texture",
        default= False
    )

    fresnel_ior_mult= FloatProperty(
        name= "Fresnel IOR texture multiplier",
        description= "Fresnel IOR texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_refract= BoolProperty(
        name= "Refraction",
        description= "Refraction texture",
        default= False
    )

    map_refract_invert= BoolProperty(
        name= "Invert refraction texture",
        description= "Invert refraction texture",
        default= False
    )

    refract_mult= FloatProperty(
        name= "Refraction texture multiplier",
        description= "Refraction texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_refract_ior= BoolProperty(
        name= "Refraction IOR",
        description= "Refraction IOR texture",
        default= False
    )

    map_refract_ior_invert= BoolProperty(
        name= "Invert refraction IOR texture",
        description= "Invert refraction IOR texture",
        default= False
    )

    refract_ior_mult= FloatProperty(
        name= "Refraction IOR texture multiplier",
        description= "Refraction IOR texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_refract_glossiness= BoolProperty(
        name= "Refraction glossiness",
        description= "Refraction glossiness texture",
        default= False
    )


    map_refract_glossiness_invert= BoolProperty(
        name= "Invert refraction glossiness texture",
        description= "Invert refraction glossiness texture",
        default= False
    )

    refract_glossiness_mult= FloatProperty(
        name= "Refraction glossiness texture multiplier",
        description= "Refraction glossiness texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_translucency_color= BoolProperty(
        name= "Translucency",
        description= "Translucency texture",
        default= False
    )

    map_translucency_color_invert= BoolProperty(
        name= "Invert translucency texture",
        description= "Invert translucency texture",
        default= False
    )

    translucency_color_mult= FloatProperty(
        name= "Translucency texture multiplier",
        description= "Translucency texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )


    '''
      BRDFCarPaint
    '''
    map_coat= BoolProperty(
        name= "Overall color",
        description= "Overall color",
        default= False
    )

    coat_mult= FloatProperty(
        name= "Coat texture multiplier",
        description= "Coat texture multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_flake= BoolProperty(
        name= "Overall color",
        description= "Overall color",
        default= False
    )

    flake_mult= FloatProperty(
        name= "Flake texture multiplier",
        description= "Flake texture multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_base= BoolProperty(
        name= "Overall color",
        description= "Overall color",
        default= False
    )

    base_mult= FloatProperty(
        name= "Base texture multiplier",
        description= "Base texture multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )


    '''
      BRDFSSS2Complex
    '''
    map_overall_color= BoolProperty(
        name= "Overall color",
        description= "Overall color",
        default= False
    )

    overall_color_mult= FloatProperty(
        name= "Overall color multiplier",
        description= "Overall color multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_diffuse_color= BoolProperty(
        name= "Diffuse color",
        description= "Diffuse color",
        default= False
    )

    diffuse_color_mult= FloatProperty(
        name= "Diffuse color multiplier",
        description= "Diffuse color multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_diffuse_amount= BoolProperty(
        name= "Diffuse amount",
        description= "Diffuse amount",
        default= False
    )

    diffuse_amount_mult= FloatProperty(
        name= "Diffuse amount multiplier",
        description= "Diffuse amount multiplie",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_sub_surface_color= BoolProperty(
        name= "Sub-surface color",
        description= "Sub-surface color",
        default= False
    )

    sub_surface_color_mult= FloatProperty(
        name= "Sub-surface color multiplier",
        description= "Sub-surface color multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_scatter_radius= BoolProperty(
        name= "Scatter radius",
        description= "Scatter radius",
        default= False
    )

    scatter_radius_mult= FloatProperty(
        name= "Scatter radius multiplier",
        description= "Scatter radius multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_specular_color= BoolProperty(
        name= "Specular color",
        description= "Specular color",
        default= False
    )

    specular_color_mult= FloatProperty(
        name= "Specular color multiplier",
        description= "Specular color multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_specular_amount= BoolProperty(
        name= "Specular amount",
        description= "Specular amoun",
        default= False
    )

    specular_amount_mult= FloatProperty(
        name= "Specular amount multiplier",
        description= "Specular amount multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )

    map_specular_glossiness= BoolProperty(
        name= "Specular glossiness",
        description= "Specular glossiness",
        default= False
    )

    specular_glossiness_mult= FloatProperty(
        name= "Specular glossiness multiplier",
        description= "Specular glossiness multiplier",
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=1.0,
        default=1.0
    )


    '''
      EnvironmentFog
    '''
    map_emission_tex= BoolProperty(
        name= "Emission",
        description= "Emission texture",
        default= False
    )

    emission_tex_mult= FloatProperty(
        name= "Emission texture multiplier",
        description= "Emission texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_color_tex= BoolProperty(
        name= "Color",
        description= "Color texture",
        default= False
    )

    color_tex_mult= FloatProperty(
        name= "Color texture multiplier",
        description= "Color texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_density_tex= BoolProperty(
        name= "Density",
        description= "Density texture",
        default= False
    )

    density_tex_mult= FloatProperty(
        name= "Density texture multiplier",
        description= "Density texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    map_fade_out_tex= BoolProperty(
        name= "Fade out",
        description= "Fade out texture",
        default= False
    )

    fade_out_tex_mult= FloatProperty(
        name= "Fade out texture multiplier",
        description= "Fade out texture multiplier",
        min= 0.0,
        max= 100.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= 1.0
    )

    use_map_env_bg= BoolProperty(
        name= "Background",
        description= "Background",
        default= True
    )

    use_map_env_bg_invert= BoolProperty(
        name= "Invert background texture",
        description= "Invert background texture",
        default= False
    )

    env_bg_factor= FloatProperty(
        name= "Background texture multiplier",
        description= "Background texture multiplier",
        min= 0.0,
        max= 10000.0,
        soft_min= 0.0,
        soft_max= 2.0,
        precision= 3,
        default= 1.0
    )

    use_map_env_gi= BoolProperty(
        name= "GI",
        description= "Override for GI",
        default= False
    )

    use_map_env_gi_invert= BoolProperty(
        name= "Invert GI texture",
        description= "Invert GI texture",
        default= False
    )

    env_gi_factor= FloatProperty(
        name= "GI texture multiplier",
        description= "GI texture multiplier",
        min= 0.0,
        max= 10000.0,
        soft_min= 0.0,
        soft_max= 2.0,
        precision= 3,
        default= 1.0
    )

    use_map_env_reflection= BoolProperty(
        name= "Reflection",
        description= "Override for Reflection",
        default= False
    )

    use_map_env_reflection_invert= BoolProperty(
        name= "Invert reflection texture",
        description= "Invert reflection texture",
        default= False
    )

    env_reflection_factor= FloatProperty(
        name= "Reflection texture multiplier",
        description= "Reflection texture multiplier",
        min= 0.0,
        max= 10000.0,
        soft_min= 0.0,
        soft_max= 2.0,
        precision= 3,
        default= 1.0
    )

    use_map_env_refraction= BoolProperty(
        name= "Refraction",
        description= "Override for Refraction",
        default= False
    )

    use_map_env_refraction_invert= BoolProperty(
        name= "Invert refraction texture",
        description= "Invert refraction texture",
        default= False
    )

    env_refraction_factor= FloatProperty(
        name= "Refraction texture multiplier",
        description= "Refraction texture multiplier",
        min= 0.0,
        max= 10000.0,
        soft_min= 0.0,
        soft_max= 2.0,
        precision= 3,
        default= 1.0
    )


def add_properties():
    bpy.utils.register_class(VRaySlot)

    setattr(bpy.types.VRayMesh, 'override', bpy.props.BoolProperty(
        name        = "Override",
        description = "Override mesh",
        default     = False
    ))

    setattr(bpy.types.VRayMesh, 'override_type', bpy.props.EnumProperty(
        name        = "Override",
        description = "Override geometry type",
        items = (
            ('VRAYPROXY', "VRayProxy", ""),
            ('VRAYPLANE', "VRayPlane", ""),
        ),
        default = 'VRAYPROXY'
    ))

    setattr(bpy.types.VRayMaterial, 'type', bpy.props.EnumProperty(
        name = "Type",
        description = "Material type",
        items = (
            ('BRDFVRayMtl', 'VRayMtl', 'BRDFVRayMtl settings'),
            ('BRDFSSS2Complex', 'SSS', 'Fast SSS 2 BRDF settings'),
            ('BRDFLight', 'Light', 'V-Ray light shader'),
            ('BRDFCarPaint', 'Car', 'BRDFCarPaint'),
            ('BRDFHair3', 'Hair', 'Hair material'),
            ('MtlVRmat', 'VRmat', 'MtlVRmat settings'),
            ('BRDFLayered', 'Layered', 'BRDFLayered')
        ),
        default = 'BRDFVRayMtl'
    ))

    setattr(bpy.types.VRayMaterial, 'material_id_number', bpy.props.IntProperty(
        name= "Material ID",
        description= "Material ID",
        min= 0,
        max= 1024,
        soft_min= 0,
        soft_max= 10,
        default= 0
    ))

    setattr(bpy.types.VRayMaterial, 'material_id_color', bpy.props.FloatVectorProperty(
        name= "Color",
        description= "Material ID color",
        subtype= 'COLOR',
        min= 0.0,
        max= 1.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= (1.0,1.0,1.0)
    ))

    setattr(bpy.types.VRayMaterial, 'round_edges', bpy.props.BoolProperty(
        name        = "Round edges",
        description = "Round edges",
        default     = False
    ))

    setattr(bpy.types.VRayMaterial, 'radius', bpy.props.FloatProperty(
        name        = "Rounding radius",
        description = "Rounding radius",
        precision   = 3,
        min         = 0.0,
        max         = 100.0,
        soft_min    = 0.0,
        soft_max    = 1.0,
        default     = 0.0
    ))

    setattr(bpy.types.VRayTexture, 'type', bpy.props.EnumProperty(
        name = "Texture Type",
        description = "V-Ray texture type",
        items = (
            ('NONE', 'None', ''),
            ('TexDirt', 'Dirt', ''),
            ('TexFalloff', 'Falloff', ''),
            ('TexFresnel', 'Fresnel', ''),
            ('TexSky', 'Sky', 'Sky texture'),
            ('TexEdges', 'Edge', 'Wire frame texture'),
            ('TexNoiseMax', 'Noise', '3ds max like noise texture'),
            ('TexGradRamp', 'Gradient Ramp', 'TexGradRamp'),
            ('TexGradient', 'Gradient', 'TexGradient'),
            ('TexTiles', 'Tiles', 'TexTiles'),
            ('TexMarbleMax', 'Marble', 'TexMarbleMax'),
            ('TexSplat', 'Splat', 'TexSplat'),
            ('TexWood', 'Wood', 'TexWood'),
            ('TexRock', 'Rock', 'TexRock'),
            ('TexCloth', 'Cloth', 'TexCloth'),
            ('TexChecker', 'Checker', 'TexChecker'),
            ('TexSwirl', 'Swirl', 'TexSwirl'),
            ('TexCellular', 'Cellular', 'TexCellular'),
            ('TexGranite', 'Granite', 'TexGranite'),
            ('TexBulge', 'Bulge', 'TexBulge'),
            ('TexGrid', 'Grid', 'TexGrid'),
            ('TexStucco', 'Stucco', 'TexStucco'),
            ('TexSpeckle', 'Speckle', 'TexSpeckle'),
            ('TexSmoke', 'Smoke', 'TexSmoke'),
            ('TexLeather', 'Leather', 'TexLeather'),
            ('TexSnow', 'Snow', 'TexSnow'),
            ('TexMeshVertexColorChannel', 'Vertex Color', 'TexMeshVertexColorChannel'),
            ('TexInvert', 'Invert', 'Invert'),
            ('TexWater', 'Water', 'Water'),
            ('TexMayaContrast', 'Maya Contrast', 'Maya Contrast'),
            ('TexMaskMax', 'Mask Max', 'Mask Max'),
            ('TexMix', 'Mix', 'Mix'),
            ('TexCompMax', 'Comp Max', 'Comp Max'),
            ('TexBerconWood', 'Bercon Wood', 'Bercon Wood'),
            ('TexDistance', 'Distance', ''),
            ('TexPtex', 'Ptex', 'VRay TexPtex texture')
        ),
        default = 'NONE'
    ))

    setattr(bpy.types.Texture, 'vray_slot', bpy.props.PointerProperty(
        name = "V-Ray Material Texture Slot",
        type = VRaySlot,
        description = "V-Ray material texture slot settings"
    ))


    setattr(bpy.types.BRDFVRayMtl, 'refract_color', FloatVectorProperty(
        name= "Refraction color",
        description= "Refraction color",
        subtype= 'COLOR',
        min= 0.0,
        max= 1.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= (0.0,0.0,0.0)
    ))

    setattr(bpy.types.BRDFVRayMtl, 'reflect_color', FloatVectorProperty(
        name= "Reflection color",
        description= "Reflection color",
        subtype= 'COLOR',
        min= 0.0,
        max= 1.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= (0.0,0.0,0.0)
    ))

    setattr(bpy.types.BRDFVRayMtl, 'translucency_color', FloatVectorProperty(
        name= "Translucency_color",
        description= "Filter color for the translucency effect",
        subtype= 'COLOR',
        min= 0.0,
        max= 1.0,
        soft_min= 0.0,
        soft_max= 1.0,
        default= (1.0,1.0,1.0)
    ))

    setattr(bpy.types.VRayObject, 'MtlRenderStats', PointerProperty(
        type = bpy.types.MtlRenderStats,
    ))

    setattr(bpy.types.VRayObject, 'MtlWrapper', PointerProperty(
        type = bpy.types.MtlWrapper,
    ))

    setattr(bpy.types.VRayObject, 'MtlRenderStats', PointerProperty(
        type = bpy.types.MtlRenderStats,
    ))

    setattr(bpy.types.VRayObject, 'MtlOverride', PointerProperty(
        type = bpy.types.MtlOverride,
    ))


def remove_properties():
    bpy.utils.unregister_class(VRaySlot)

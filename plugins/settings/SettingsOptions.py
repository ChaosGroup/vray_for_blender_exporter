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

TYPE = 'SETTINGS'
ID   = 'SettingsOptions'
NAME = 'Options'
DESC = ""

PluginParams = (
    {
        'attr' : 'geom_displacement',
        'name' : "Use Displacement",
        'desc' : "Render displacement",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'geom_doHidden',
        'name' : "Render Hidden",
        'desc' : "Render hidden geometry",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'light_doLights',
        'name' : "Use Lights",
        'desc' : "Use lights",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'light_doDefaultLights',
        'name' : "Default Lights",
        'desc' : "Use default lights (when no lights are presented in a scene)",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'light_doHiddenLights',
        'name' : "Hidden Lights",
        'desc' : "Render hidden lights",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'light_doShadows',
        'name' : "Shadows",
        'desc' : "Render shadows",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'light_onlyGI',
        'name' : "Produce GI Only",
        'desc' : "Use only GI from lights",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'light_disableSelfIllumination',
        'name' : "Self Illumination",
        'desc' : "self-Illumination",
        'type' : 'BOOL',
        'ui' : {
            'inverted' : True,
        },
        'default' : True,
    },
    {
        'attr' : 'gi_dontRenderImage',
        'name' : "Calculate GI Only",
        'desc' : "Don't render final image",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mtl_reflectionRefraction',
        'name' : "Render Reflection / Refraction",
        'desc' : "Render reflections / refractions",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mtl_limitDepth',
        'name' : "Limit Depth",
        'desc' : "Limit max depth",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mtl_maxDepth',
        'name' : "Max Ray Depth",
        'desc' : "Max. ray depth for reflections and refractions",
        'type' : 'INT',
        'default' : 5,
    },
    {
        'attr' : 'mtl_doMaps',
        'name' : "Use Textures",
        'desc' : "Render textures",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mtl_filterMaps',
        'name' : "Filter Textures",
        'desc' : "Filter textures",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mtl_filterMapsForSecondaryRays',
        'name' : "Filter Textures For GI",
        'desc' : "false to turn off filtering for glossy and GI rays",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mtl_transpMaxLevels',
        'name' : "Max Transp. Levels",
        'desc' : "Max. transparency levels",
        'type' : 'INT',
        'default' : 50,
    },
    {
        'attr' : 'mtl_transpCutoff',
        'name' : "Transp. Cutoff",
        'desc' : "Transparency cutoff",
        'type' : 'FLOAT',
        'default' : 0.001,
    },
    {
        'attr' : 'mtl_override_on',
        'name' : "Override Material",
        'desc' : "Override material",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'mtl_glossy',
        'name' : "Render Glossy",
        'desc' : "Render glossy",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'mtl_uninvertedNormalBump',
        'name' : 'Uninverted Normal Bump',
        'desc' : "If true the normal bump in tangent space will not be inverted on flipped UVs",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'geom_backfaceCull',
        'name' : "Force Back Face Culling",
        'desc' : "If true, back faces will be invisible to camera and shadow rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ray_bias',
        'name' : "Sec. Ray Bias",
        'desc' : "Secondary ray bias",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'misc_lowThreadPriority',
        'name' : "Low Thread Priority",
        'desc' : "Low thread priority",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'gi_texFilteringMultiplier',
        'desc' : "GI texturing multiplier",
        'type' : 'FLOAT',
        'default' : 1,
    },
    {
        'attr' : 'misc_abortOnMissingAsset',
        'name' : "Abort On Missing Asset",
        'desc' : "",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'misc_transferAssets',
        'name' : 'Transfer Assets',
        'desc' : "Transfer missing assets on DR",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'misc_useCachedAssets',
        'name' : 'Use Cached Assets',
        'desc' : "Use cached assets on DR",
        'type' : 'BOOL',
        'default' : True,
    },
    {
        'attr' : 'dr_assetsCacheLimitType',
        'name' : "Cache Limit Type",
        'desc' : "Type of the assets cache limit",
        'type' : 'ENUM',
        'items' : (
            ('0', "None", "Assets are never deleted from the cache folder"),
            ('1', "Age (Hours)", "Assets that have been transferred before the specified period of time are deleted; the specified value is in hours"),
            ('2', "Size (GB)", "Assets are deleted from oldest to freshly received until the cache folder is below the specified size in gigabytes"),
        ),
        'default' : '0',
    },
    {
        'attr' : 'dr_assetsCacheLimitValue',
        'name' : "Cache Limit",
        'desc' : "Value of the assets cache limit",
        'type' : 'FLOAT',
        'default' : 0,
    },
    {
        'attr' : 'dr_overwriteLocalCacheSettings',
        'name' : "Overwrite Cache Settings",
        'desc' : "If is true the client's cache settings will overwrite server settings",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ray_max_intensity_on',
        'name' : "Limit Ray Intensity",
        'desc' : "Enable clamping of secondary rays",
        'type' : 'BOOL',
        'default' : False,
    },
    {
        'attr' : 'ray_max_intensity',
        'name' : "Max Ray Intensity",
        'desc' : "The max secondary ray intensity when ray_max_intensity_on is enabled",
        'type' : 'FLOAT',
        'default' : 20,
    },

    {
        'attr' : 'mtl_override',
        'desc' : "Override material",
        'type' : 'STRING',
        'skip' : True,
        'default' : "",
    },
)


# TODO: Resolve draft / preview
#
# ofile.write("\n\tmtl_limitDepth= 1;")
# ofile.write("\n\tmtl_maxDepth= 5;")
# ofile.write("\n\tmtl_transpMaxLevels= 10;")
# ofile.write("\n\tmtl_transpCutoff= 0.1;")
# ofile.write("\n\tmtl_glossy= 1;")

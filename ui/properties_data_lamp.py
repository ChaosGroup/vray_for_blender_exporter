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

from pynodes_framework import idref

from vb25.ui      import classes
from vb25.lib     import utils as LibUtils
from vb25.lib     import DrawUtils
from vb25.plugins import PLUGINS


##     ## ######## #### ##        ######  
##     ##    ##     ##  ##       ##    ## 
##     ##    ##     ##  ##       ##       
##     ##    ##     ##  ##        ######  
##     ##    ##     ##  ##             ## 
##     ##    ##     ##  ##       ##    ## 
 #######     ##    #### ########  ######  

def LightIsSun(lamp):
    if lamp.type == 'SUN' and lamp.vray.direct_type == 'SUN':
        return True
    return False


def LightIsPortal(lamp):
    if lamp.type == 'AREA' and int(lamp.vray.LightRectangle.lightPortal):
        return True
    return False


def LightIsAmbient(lamp):
    if LibUtils.GetLightPluginName(lamp) in {'LightAmbientMax'}:
        return True
    return False


 ######   #######  ##    ## ######## ######## ##     ## ######## 
##    ## ##     ## ###   ##    ##    ##        ##   ##     ##    
##       ##     ## ####  ##    ##    ##         ## ##      ##    
##       ##     ## ## ## ##    ##    ######      ###       ##    
##       ##     ## ##  ####    ##    ##         ## ##      ##    
##    ## ##     ## ##   ###    ##    ##        ##   ##     ##    
 ######   #######  ##    ##    ##    ######## ##     ##    ##    

class VRAY_DP_context_lamp(classes.VRayLampPanel):
    bl_label   = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout

        ob    = context.object
        lamp  = context.lamp
        space = context.space_data

        if ob:
            layout.template_ID(ob, 'data')
        elif lamp:
            layout.template_ID(space, 'pin_id')

        VRayLight = lamp.vray

        layout.separator()      
        layout.prop(lamp, 'type', expand=True)

        lightSubTypeAttr = LibUtils.LampSubType[lamp.type]
        if lightSubTypeAttr is not None:
            layout.prop(VRayLight, lightSubTypeAttr, expand=True)

        lightPluginName = LibUtils.GetLightPluginName(lamp)
        lightPropGroup = getattr(VRayLight, lightPluginName)

        layout.separator()
        split = self.layout.split()
        row = split.row(align=True)
        idref.draw_idref(row, VRayLight, 'ntree', text="Node Tree")
        row.operator("vray.add_nodetree_light", icon='ZOOMIN', text="").lightType=lightPluginName

        # if not classes.TreeHasNodes(VRayLight.ntree):
        #     return

        # activeNode = VRayLight.ntree.nodes[-1]

        # layout.separator()
        # classes.DrawNodePanel(context, self.layout, activeNode, PLUGINS)


 ######   ######## ##    ## ######## ########     ###    ##       
##    ##  ##       ###   ## ##       ##     ##   ## ##   ##       
##        ##       ####  ## ##       ##     ##  ##   ##  ##       
##   #### ######   ## ## ## ######   ########  ##     ## ##       
##    ##  ##       ##  #### ##       ##   ##   ######### ##       
##    ##  ##       ##   ### ##       ##    ##  ##     ## ##       
 ######   ######## ##    ## ######## ##     ## ##     ## ######## 

class VRAY_DP_light(classes.VRayLampPanel):
    bl_label = "Lamp"

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp
        VRayLamp = lamp.vray

        lightPluginName = LibUtils.GetLightPluginName(lamp)
        lightPropGroup = getattr(VRayLamp, lightPluginName)

        layout.prop(lightPropGroup, 'enabled')

        # Color
        #
        if not (LightIsPortal(lamp) or LightIsSun(lamp)):
            split = layout.split(percentage=0.4)
            row = split.row()
            row.prop(VRayLamp, 'color_type', expand=True)

            if VRayLamp.color_type == 'RGB':
                row = split.row()
                row.prop(lightPropGroup, 'color_tex', text="")
                row.operator('vray.set_kelvin_color', text="", icon='COLOR', emboss=False).data_path="object.data.vray.%s.color_tex" % lightPluginName
            else:
                row = split.row()
                row.prop(VRayLamp, 'temperature', text="K")

            DrawUtils.DrawAttr(layout, lightPropGroup, 'invisible')

            layout.separator()

        # Intensity
        #
        split = layout.split()
        col = split.column()
        DrawUtils.DrawAttr(col, lightPropGroup, 'lightPortal', text="Mode")
        if not (LightIsPortal(lamp) or LightIsSun(lamp)):
            DrawUtils.DrawAttr(col, lightPropGroup, 'units', text="Units")
        
        if LightIsSun(lamp):
            DrawUtils.DrawAttr(col, lightPropGroup, 'intensity', text="Intensity")
        else:
            DrawUtils.DrawAttr(col, lightPropGroup, 'intensity_multiplier')

        split = layout.split()
        col = split.column()
        DrawUtils.DrawAttr(col, lightPropGroup, 'subdivs')
        DrawUtils.DrawAttr(col, lightPropGroup, 'causticSubdivs')
        DrawUtils.DrawAttr(col, lightPropGroup, 'noDecay')
        DrawUtils.DrawAttr(col, lightPropGroup, 'doubleSided')
        DrawUtils.DrawAttr(col, lightPropGroup, 'storeWithIrradianceMap')

        split = layout.split()
        col = split.column()
        DrawUtils.DrawAttr(col, lightPropGroup, 'affectDiffuse')
        DrawUtils.DrawAttr(col, lightPropGroup, 'affectSpecular')
        DrawUtils.DrawAttr(col, lightPropGroup, 'affectReflections')

        DrawUtils.DrawAttr(col, lightPropGroup, 'intensity_tex', text="Intensity")

        DrawUtils.Draw(context, layout, lightPropGroup, PLUGINS['LIGHT'][lightPluginName].PluginParams)


 ######  ##     ##    ###    ########  ######## 
##    ## ##     ##   ## ##   ##     ## ##       
##       ##     ##  ##   ##  ##     ## ##       
 ######  ######### ##     ## ########  ######   
      ## ##     ## ######### ##        ##       
##    ## ##     ## ##     ## ##        ##       
 ######  ##     ## ##     ## ##        ######## 

class VRAY_DP_light_shape(classes.VRayLampPanel):
    bl_label = "Shape"

    def draw(self, context):
        layout = self.layout

        lamp      = context.lamp
        VRayLight = lamp.vray
        VRayScene = context.scene.vray

        lightPluginName = LibUtils.GetLightPluginName(lamp)

        lightPropGroup = getattr(VRayLight, lightPluginName)

        if lamp.type == 'AREA':
            layout.prop(lamp, 'shape', expand=True)
            split = layout.split()
            if lamp.shape == 'SQUARE':
                col = split.column()
                col.prop(lamp, 'size')
            else:
                row = split.row(align=True)
                row.prop(lamp, 'size', text="Size X")
                row.prop(lamp, 'size_y')

        if lamp.type == 'SPOT':
            split = layout.split()
            col = split.column()
            if VRayLight.spot_type == 'SPOT':
                col.prop(lamp, 'spot_size', text="Size")
                col.prop(lamp, 'spot_blend', text="Blend")
            else:
                col.prop(lightPropGroup, 'ies_file', text="File")


######## ##     ##  ######  ##       ##     ## ########  ######## 
##        ##   ##  ##    ## ##       ##     ## ##     ## ##       
##         ## ##   ##       ##       ##     ## ##     ## ##       
######      ###    ##       ##       ##     ## ##     ## ######   
##         ## ##   ##       ##       ##     ## ##     ## ##       
##        ##   ##  ##    ## ##       ##     ## ##     ## ##       
######## ##     ##  ######  ########  #######  ########  ######## 

class VRAY_DP_include_exclude(classes.VRayLampPanel):
    bl_label   = "Include / Exclude"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        VRayLamp = context.lamp.vray
        self.layout.prop(VRayLamp, 'use_include_exclude', text="")

    def draw(self, context):
        layout = self.layout

        VRayLamp = context.lamp.vray

        layout.active = VRayLamp.use_include_exclude

        split= layout.split()
        col= split.column()
        col.prop(VRayLamp, 'include_exclude', text="")
        col.prop_search(VRayLamp, 'include_objects', context.scene, 'objects', text="Objects")
        col.prop_search(VRayLamp, 'include_groups',  bpy.data,      'groups',  text="Groups")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_DP_context_lamp,
        VRAY_DP_light,
        # VRAY_DP_light_shape,
        VRAY_DP_include_exclude,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

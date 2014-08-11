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

from vb30.ui      import classes
from vb30.lib     import LibUtils
from vb30.lib     import DrawUtils
from vb30.plugins import PLUGINS


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
        split = layout.split(percentage=0.3)
        col = split.column()
        col.label("Lamp Tree:")
        col = split.column()
        row = col.row(align=True)
        if VRayLight.ntree:
            renameOp = row.operator("vray.nodetree_rename_to", icon='SYNTAX_OFF', text="")
            renameOp.to_data = 'LAMP'
        row.prop_search(VRayLight, 'ntree', bpy.data, 'node_groups', text="")
        if not VRayLight.ntree:
            row.operator("vray.add_nodetree_light", icon='ZOOMIN', text="").lightType=lightPluginName

        layout.separator()
        classes.DrawPluginUI(context, layout, VRayLight, lightPropGroup, lightPluginName, PLUGINS['LIGHT'][lightPluginName])


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
                row.prop(lamp, 'size',   text="X")
                row.prop(lamp, 'size_y', text="Y")

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

    COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDERER','VRAY_RENDER_PREVIEW'}

    def draw(self, context):
        wide_ui= context.region.width > classes.narrowui
        layout= self.layout

        VRayLamp= context.lamp.vray

        layout.prop(VRayLamp, 'include_exclude', text="Type")

        split = layout.split()
        split.active = VRayLamp.include_exclude != '0'
        col = split.column()
        col.prop(VRayLamp, 'illumination_shadow', text="From")
        col.prop_search(VRayLamp, 'exclude_objects',  context.scene, 'objects', text="Object")
        col.prop_search(VRayLamp, 'exclude_groups',   bpy.data,      'groups',  text="Group")


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
        VRAY_DP_light_shape,
        VRAY_DP_include_exclude,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

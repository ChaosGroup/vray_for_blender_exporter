#
# V-Ray/Blender
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

from vb30.ui import classes

from ..        import tree
from ..sockets import AddInput, AddOutput


 #######  ########        ## ########  ######  ########
##     ## ##     ##       ## ##       ##    ##    ##
##     ## ##     ##       ## ##       ##          ##
##     ## ########        ## ######   ##          ##
##     ## ##     ## ##    ## ##       ##          ##
##     ## ##     ## ##    ## ##       ##    ##    ##
 #######  ########   ######  ########  ######     ##

class VRayNodeObjectOutput(bpy.types.Node, tree.VRayObjectNode):
    bl_idname = 'VRayNodeObjectOutput'
    bl_label  = 'Object Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    nsamples = bpy.props.IntProperty(
        name        = "Samples",
        description = "Number of transform samples",
        default     =  0
    )

    def draw_buttons(self, context, layout):
        ob = context.active_object

        layout.prop(ob, 'hide_render', text="Visible")
        layout.prop(ob, 'pass_index', text="Object ID")
        layout.prop(self, 'nsamples')

    def init(self, context):
        AddInput(self, 'VRaySocketMtl',  "Material", 'material')
        AddInput(self, 'VRaySocketGeom', "Geometry", 'geometry')


class VRayNodeBlenderOutputGeometry(bpy.types.Node, tree.VRayObjectNode):
    bl_idname = 'VRayNodeBlenderOutputGeometry'
    bl_label  = 'Blender Object Geometry'
    bl_icon   = 'MESH_DATA'

    vray_type   = bpy.props.StringProperty(default='NONE')
    vray_plugin = bpy.props.StringProperty(default='NONE')

    GeomStaticMesh = bpy.props.PointerProperty(
        name = "GeomStaticMesh",
        type =  bpy.types.GeomStaticMesh,
        description = "GeomStaticMesh settings"
    )

    def draw_buttons(self, context, layout):
        classes.DrawPluginUIAuto(context, layout, self.GeomStaticMesh, 'GeomStaticMesh')

    def init(self, context):
        AddOutput(self, 'VRaySocketGeom', "Geometry")


class VRayNodeBlenderOutputMaterial(bpy.types.Node, tree.VRayObjectNode):
    bl_idname = 'VRayNodeBlenderOutputMaterial'
    bl_label  = 'Blender Object Materials'
    bl_icon   = 'MATERIAL'

    vray_type   = bpy.props.StringProperty(default='NONE')
    vray_plugin = bpy.props.StringProperty(default='NONE')

    wrap_id = bpy.props.BoolProperty(
        name        = "Wrap ID",
        description = "Wrap the material ID's to the largest specified ID for the material",
        default     =  False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, 'wrap_id')

    def init(self, context):
        AddInput(self, 'VRaySocketFloatNoValue', "ID Generator", attrName='mtlid_gen_float')

        AddOutput(self, 'VRaySocketMtl', "Material")


##     ##    ###    ######## ######## ########  ####    ###    ##
###   ###   ## ##      ##    ##       ##     ##  ##    ## ##   ##
#### ####  ##   ##     ##    ##       ##     ##  ##   ##   ##  ##
## ### ## ##     ##    ##    ######   ########   ##  ##     ## ##
##     ## #########    ##    ##       ##   ##    ##  ######### ##
##     ## ##     ##    ##    ##       ##    ##   ##  ##     ## ##
##     ## ##     ##    ##    ######## ##     ## #### ##     ## ########

class VRayNodeOutputMaterial(bpy.types.Node, tree.VRayTreeNode):
    bl_idname = 'VRayNodeOutputMaterial'
    bl_label  = 'Material Output'
    bl_icon   = 'VRAY_LOGO'

    vray_type   = 'NONE'
    vray_plugin = 'NONE'

    dontOverride = bpy.props.BoolProperty(
        name        = "Don't Override",
        description = "Don't override material",
        default     = False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, 'dontOverride')

    def init(self, context):
        AddInput(self, 'VRaySocketMtl', "Material")


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRayNodeBlenderOutputMaterial,
        VRayNodeBlenderOutputGeometry,

        VRayNodeOutputMaterial,
        VRayNodeObjectOutput,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

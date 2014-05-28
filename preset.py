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

import bpy


class VRAY_MT_preset_global(bpy.types.Menu):
    bl_label        = "Global Presets"
    preset_subdir   = os.path.join("..", "startup", "vb30", "presets", "render")
    preset_operator = "script.execute_preset"
    draw            = bpy.types.Menu.draw_preset


class VRAY_MT_preset_gi(bpy.types.Menu):
    bl_label        = "GI Presets"
    preset_subdir   = os.path.join("..", "startup", "vb30", "presets", "gi")
    preset_operator = "script.execute_preset"
    draw            = bpy.types.Menu.draw_preset


class VRAY_MT_preset_im(bpy.types.Menu):
    bl_label        = "Irradiance Map Presets"
    preset_subdir   = os.path.join("..", "startup", "vb30", "presets", "im")
    preset_operator = "script.execute_preset"
    draw            = bpy.types.Menu.draw_preset


########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_MT_preset_global,
        VRAY_MT_preset_gi,
        VRAY_MT_preset_im,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)

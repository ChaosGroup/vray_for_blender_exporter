'''

  V-Ray/Blender

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
  
'''

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.ui.ui import *

TYPE= 'SETTINGS'

ID=   'SETTINGSCENE'
NAME= 'Scene settings'
DESC= "Misc. scene settings"

PARAMS= (
)


def image_aspect_lock(self, context):
	scene= context.scene
	rd=    scene.render
	VRayScene= scene.vray
		
	if VRayScene.image_aspect_lock:
		rd.resolution_y= rd.resolution_x / VRayScene.image_aspect
	
	return None


def add_properties(rna_pointer):
	rna_pointer.image_aspect_lock= BoolProperty(
		name= "Lock aspect",
		description= "Lock image aspect",
		default= False
	)

	rna_pointer.image_aspect= FloatProperty(
		update= image_aspect_lock,
		name= "Image aspect",
		description= "Image aspect",
		min= 0.1,
		max= 100.0,
		soft_min= 0.1,
		soft_max= 10.0,
		precision= 3,
		default= 1.333
	)

	class VRayStereoscopicSettings(bpy.types.PropertyGroup):
		pass
	bpy.utils.register_class(VRayStereoscopicSettings)

	rna_pointer.VRayStereoscopicSettings= PointerProperty(
		name= "VRayStereoscopicSettings",
		type=  VRayStereoscopicSettings,
		description= "V-Ray VRayStereoscopicSettings settings"
	)

	VRayStereoscopicSettings.use= BoolProperty(
		name= "Stereoscopic",
		description= "Use stereoscopic render",
		default= False
	)

	
	VRayStereoscopicSettings.left_camera= StringProperty(
		name= "Left Camera",
		description= "Left camera",
		default= ""
	)
	
	VRayStereoscopicSettings.right_camera= StringProperty(
		name= "Right Camera",
		description= "Right camera",
		default= ""
	)

	VRayStereoscopicSettings.eye_distance= FloatProperty(
		name= "Eye Distance",
		description= "The eye distance for which the stereoscopic image will be rendered",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 6.5
	)

	VRayStereoscopicSettings.specify_focus= BoolProperty(
		name= "Specify Focus",
		description= "If on then the focus is determined by 'Focus' and 'Focus Distance'",
		default= False
	)

	VRayStereoscopicSettings.focus_distance= FloatProperty(
		name= "Focus Distance",
		description= "Focus distance",
		min= 0.0,
		max= 100000.0,
		soft_min= 0.0,
		soft_max= 1000.0,
		precision= 3,
		default= 200
	)

	VRayStereoscopicSettings.focus_method= EnumProperty(
		name= "Focus Method",
		description= "Specifies the focus method for the two views",
		items= (
			('NONE',  "None",     "Both cameras have their focus points directly in front of them"),
			('ROT',   "Rotation", "The stereoscopy is achieved by rotating the left and right views so that their focus points coincide at the distance from the eyes where the lines of sight for each eye converge called fusion distance"),
			('SHEAR', "Shear",    "The orientation of both views remain the same but each eyes view is sheared along Z so that the two frustums converge at the fusion distance"),
		),
		default= 'NONE'
	)

	VRayStereoscopicSettings.interocular_method= EnumProperty(
		name= "Interocular Method",
		description= "Specifies how the two virtual cameras will be placed in relation to the real camera in the scene",
		items= (		
			('BOTH',  "Both",  "Both virtual cameras will be shifted in opposite directions at a distance equal to half of the eye distance"),
			('LEFT',  "Left",  "The virtual cameras are shifted to the left so that the right camera takes the position of the original camera. The left camera is shifted to the left at a distance equal to the 'Eye Distance'"),
			('RIGHT', "Right", "The virtual cameras are shifted to the right so that the left camera takes the position of the original camera. The right camera is shifted to the right at a distance equal to the 'Eye Distance'")
		),
		default= 'BOTH'
	)

	VRayStereoscopicSettings.view= EnumProperty(
		name= "View",
		description= "Specifies which of the stereoscopic views will be rendered",
		items= (		
			('BOTH',  "Both",  "Both views will be rendered side by side"),
			('LEFT',  "Left",  "Only the left view will be rendered"),
			('RIGHT', "Right", "Only the right view will be rendered")
		),
		default= 'BOTH'
	)

	VRayStereoscopicSettings.adjust_resolution= BoolProperty(
		name= "Adjust Resolution",
		description= "When on this option will automatically adjust the resolution for the final image rendered",
		default= False
	)


	VRayStereoscopicSettings.reuse_threshold= FloatProperty(
		name= "Reuse Threshold",
		description= "Lower values will make V-Ray use less of the shade map and more real shading",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1
	)

	VRayStereoscopicSettings.sm_mode= EnumProperty(
		name= "Shademap Mode",
		description= "Allows us to specify the mode of operation for the shade map",
		items= (
			('DISABLED', "Disabled",         "No shade map will be used during rendering"),
			('RENDER',   "Render shade map", "In this mode a shade map will be created and saved in the file specified in the Shademap file field"),
			('USE',      "Use shade map",    "In this mode V-Ray will render the image using information from the file specified in the Shademap file field")
		),
		default='DISABLED'
	)

	VRayStereoscopicSettings.shademap_file= StringProperty(
		name= "Shademap File",
		subtype= 'FILE_PATH',
		description= "The name of the file in which the shade map information is stored",
		default= "//lightmaps/shade.vrmap"
	)

	VRayStereoscopicSettings.exclude_list= StringProperty(
		name= "Exclude",
		description= "Allows the user to exclude some of the objects in the scene from being rendered with the shade map [';' separated list of objects and groups]",
		default= ""
	)

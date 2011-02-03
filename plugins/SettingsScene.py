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
DESC= "Misc. scene settings."

PARAMS= (
)


def add_properties(rna_pointer):
	rna_pointer.use_hidden_lights= BoolProperty(
		name= "Hidden lights",
		description= "Render hidden lights.",
		default= False
	)

	rna_pointer.image_aspect= FloatProperty(
		name= "Image aspect",
		description= "Image aspect.",
		min= 0.0,
		max= 100.0,
		soft_min= 0.0,
		soft_max= 10.0,
		precision= 3,
		default= 1.333
	)

	rna_pointer.image_aspect_lock= BoolProperty(
		name= "Lock aspect",
		description= "Lock image aspect.",
		default= False
	)


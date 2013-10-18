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
from bpy.props import *

from vb25.ui      import classes
from vb25.plugins import *
from vb25.utils   import *
from vb25.nodes   import export as NodesExport


TYPE = 'SETTINGS'
ID   = 'SettingsEnvironment'
NAME = 'Environment & Effects'
DESC = "Environment and effects"


######## ######## ######## ########  ######  ########  ######  
##       ##       ##       ##       ##    ##    ##    ##    ## 
##       ##       ##       ##       ##          ##    ##       
######   ######   ######   ######   ##          ##     ######  
##       ##       ##       ##       ##          ##          ## 
##       ##       ##       ##       ##    ##    ##    ##    ## 
######## ##       ##       ########  ######     ##     ######  

def WriteEffects(bus, ntree, node):
	scene = bus['scene']
	ofile = bus['files']['environment']

	for nodeSocket in node.inputs:
		NodesExport.WriteConnectedNode(bus, ntree, nodeSocket)


######## ##    ## ##     ## #### ########   #######  ##    ## ##     ## ######## ##    ## ######## 
##       ###   ## ##     ##  ##  ##     ## ##     ## ###   ## ###   ### ##       ###   ##    ##    
##       ####  ## ##     ##  ##  ##     ## ##     ## ####  ## #### #### ##       ####  ##    ##    
######   ## ## ## ##     ##  ##  ########  ##     ## ## ## ## ## ### ## ######   ## ## ##    ##    
##       ##  ####  ##   ##   ##  ##   ##   ##     ## ##  #### ##     ## ##       ##  ####    ##    
##       ##   ###   ## ##    ##  ##    ##  ##     ## ##   ### ##     ## ##       ##   ###    ##    
######## ##    ##    ###    #### ##     ##  #######  ##    ## ##     ## ######## ##    ##    ##    

def WriteEnvironment(bus, ntree, node):
	scene = bus['scene']
	ofile = bus['files']['environment']

	volumes = bus.get('volumes', ())

	VRayWorld = scene.world.vray

	if node is None:
		ofile.write("\nSettingsEnvironment settingsEnvironment {")
		ofile.write("\n\tglobal_light_level=%s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayWorld.global_light_level))
		ofile.write("\n\tenvironment_volume=List(%s);" % (','.join(volumes)))
		ofile.write("\n}\n")
		return

	socketParams = {}
	for nodeSocket in node.inputs:
		vrayAttr = nodeSocket.vray_attr
		socketParams[vrayAttr] = NodesExport.WriteConnectedNode(bus, ntree, nodeSocket)

	ofile.write("\nSettingsEnvironment settingsEnvironment {")
	ofile.write("\n\tglobal_light_level=%s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayWorld.global_light_level))
	ofile.write("\n\tenvironment_volume=List(%s);" % (','.join(volumes)))
	ofile.write("\n\tbg_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\tbg_tex_mult=1.0;")
	ofile.write("\n\tgi_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\tgi_tex_mult=1.0;")
	ofile.write("\n\treflect_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\treflect_tex_mult=1.0;")
	ofile.write("\n\trefract_color=Color(0.0,0.0,0.0);")
	ofile.write("\n\trefract_tex_mult=1.0;")

	ofile.write("\n\tbg_tex=%s;" % a(scene, socketParams.get('bg_tex', node.inputs['Background'].value)))

	for override in {'gi_tex', 'reflect_tex', 'refract_tex'}:
		value = None

		if override in socketParams and getattr(node, override):
			value = socketParams[override]
		else:
			value = socketParams.get('bg_tex', None)

		if value:
			ofile.write("\n\t%s=%s;" % (override, a(scene, value)))

	ofile.write("\n}\n")


def write(bus):
	scene = bus['scene']

	ntree = scene.world.vray.ntree
	if not ntree:
		return 

	outputNode = NodesExport.GetNodeByType(ntree, 'VRayNodeWorldOutput')
	if not outputNode:
		return

	# Effects must always be exported before Environment
	#
	effectsSocket = outputNode.inputs['Effects']
	if effectsSocket.is_linked:
		effectsNode = NodesExport.GetConnectedNode(ntree, effectsSocket)
		if effectsNode:
			WriteEffects(bus, ntree, effectsNode)

	environmentSocket = outputNode.inputs['Environment']
	if environmentSocket.is_linked:
		environmentNode = NodesExport.GetConnectedNode(ntree, environmentSocket)
		if environmentNode:
			WriteEnvironment(bus, ntree, environmentNode)
	else:
		WriteEnvironment(bus, ntree, None)


def write_VolumeVRayToon_from_material(bus):
	WIDTHTYPE= {
		'PIXEL': 0,
		'WORLD': 1,
	}

	ofile= bus['files']['environment']
	scene= bus['scene']

	ob= bus['node']['object']
	ma= bus['material']['material']

	VRayMaterial= ma.vray

	VolumeVRayToon= VRayMaterial.VolumeVRayToon

	toon_name= clean_string("MT%s%s" % (ob.name, ma.name))

	ofile.write("\nVolumeVRayToon %s {" % toon_name)
	ofile.write("\n\tcompensateExposure= 1;")
	for param in PARAMS['VolumeVRayToon']:
		if param == 'excludeType':
			value= 1
		elif param == 'excludeList':
			value= "List(%s)" % get_name(ob, prefix='OB')
		elif param == 'widthType':
			value= WIDTHTYPE[VolumeVRayToon.widthType]
		else:
			value= getattr(VolumeVRayToon, param)
		ofile.write("\n\t%s=%s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return toon_name



def write_SphereFadeGizmo(bus, ob):
	vray = ob.vray
	name= "MG%s" % get_name(ob, prefix='EMPTY')
	ofile.write("\nSphereFadeGizmo %s {" % name)
	ofile.write("\n\ttransform=%s;" % a(scene, transform(ob.matrix_world)))
	if ob.type == 'EMPTY':
		ofile.write("\n\tradius=%s;" % ob.empty_draw_size)
	elif vray.MtlRenderStats.use:
		ofile.write("\n\tradius=%s;" % vray.fade_radius)
	ofile.write("\n\tinvert=0;")
	ofile.write("\n}\n")
	return name


def write_SphereFade(bus, effect, gizmos):
	scene= bus['scene']
	name= "ESF%s" % clean_string(effect.name)

	ofile.write("\nSphereFade %s {" % name)
	print(gizmos)
	ofile.write("\n\tgizmos= List(%s);" % ','.join(gizmos))
	for param in PARAMS['SphereFade']:
		value= getattr(effect.SphereFade, param)
		ofile.write("\n\t%s=%s;"%(param, a(scene,value)))

	ofile.write("\n}\n")


def write_VolumeVRayToon(bus, effect, objects):
	EXCLUDETYPE= {
		'EXCLUDE': 0,
		'INCLUDE': 1,
	}
	WIDTHTYPE= {
		'PIXEL': 0,
		'WORLD': 1,
	}

	VolumeVRayToon= effect.VolumeVRayToon

	name= "EVT%s" % clean_string(effect.name)

	ofile.write("\nVolumeVRayToon %s {" % name)
	ofile.write("\n\tcompensateExposure= 1;")
	for param in PARAMS['VolumeVRayToon']:
		if param == 'excludeType':
			value= EXCLUDETYPE[VolumeVRayToon.excludeType]
		elif param == 'widthType':
			value= WIDTHTYPE[VolumeVRayToon.widthType]
		elif param == 'excludeList':
			value= "List(%s)" % ','.join(objects)
		else:
			value= getattr(VolumeVRayToon, param)
		ofile.write("\n\t%s=%s;"%(param, a(scene, value)))
	ofile.write("\n}\n")

	return name

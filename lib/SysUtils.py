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

import getpass
import os
import socket
import sys

import bpy

from . import BlenderUtils


def GetUsername():
    if sys.platform == 'win32':
        return "standalone"
    else:
        return getpass.getuser()


def GetHostname():
    return socket.gethostname()


def GetVRayStandalonePath():
	VRayPreferences = bpy.context.user_preferences.addons['vb30'].preferences

	vray_bin = "vray"
	if sys.platform == 'win32':
		vray_bin += ".exe"

	def get_env_paths(var):
		split_char= ';' if sys.platform == 'win32' else ":"
		env_var= os.getenv(var)
		if env_var:
			return env_var.replace('\"','').split(split_char)
		return []

	def find_vray_std_osx_official():
		vrayPath = "/Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/bin/snow_leopard_x86/gcc-4.2/vray"
		if os.path.exists(vrayPath):
			return vrayPath
		return None

	def find_vray_std_osx():
		import glob
		instLogFilepath = "/var/log/chaos_installs"
		if not os.path.exists(instLogFilepath):
			return None
		instLog = open(instLogFilepath, 'r').readlines()
		for l in instLog:
			# Example path:
			#  /Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/uninstall/linuxinstaller.app/Contents
			#
			if 'V-Ray Standalone' in l and '[UN]' not in l:
				_tmp_, path = l.strip().split('=')

				# Going up to /Applications/ChaosGroup/V-Ray/Standalone_for_snow_leopard_x86/bin
				path = os.path.normpath(os.path.join(path.strip(), '..', '..', '..', "bin"))

				possiblePaths = glob.glob('%s/*/*/vray' % path)
				if len(possiblePaths):
					return possiblePaths[0]
				return None
		return None

	def find_vray_binary(paths):
		if paths:
			for p in paths:
				if p:
					vray_path= os.path.join(p,vray_bin)
					if os.path.exists(vray_path):
						return vray_path
		return None

	if not VRayPreferences.detect_vray and VRayPreferences.vray_binary:
		manualVRayPath = bpy.path.abspath(VRayPreferences.vray_binary)
		if os.path.exists(manualVRayPath):
			return manualVRayPath

	# Check 'VRAY_PATH' environment variable
	#
	vray_standalone_paths= get_env_paths('VRAY_PATH')
	if vray_standalone_paths:
		vray_standalone= find_vray_binary(vray_standalone_paths)
		if vray_standalone:
			return vray_standalone

	# On OS X check default path and install log
	#
	if sys.platform in {'darwin'}:
		path = find_vray_std_osx_official()
		if path is not None:
			return path
		path = find_vray_std_osx()
		if path is not None:
			return path

	# Try to find Standalone in V-Ray For Maya
	#
	for var in reversed(sorted(os.environ.keys())):
		if var.startswith('VRAY_FOR_MAYA'):
			if var.find('MAIN') != -1:
				debug(sce, "Searching in: %s" % (var))
				vray_maya= find_vray_binary([os.path.join(path, 'bin') for path in get_env_paths(var)])
				if vray_maya:
					debug(sce, "V-Ray found in: %s" % (vray_maya))
					return vray_maya

	# Try to find vray binary in %PATH%
	debug(sce, "V-Ray not found! Trying to start \"%s\" command from $PATH..." % (vray_bin), True)

	return shutil.which(vray_bin)


def GetExporterPath():
	for path in bpy.utils.script_paths(os.path.join('addons','vb30')):
		if path:
			return path
	return None


def GetVRsceneTemplate(filename):
	templatesDir = os.path.join(GetExporterPath(), "templates")
	templateFilepath = os.path.join(templatesDir, filename)

	templateFilepathUser = os.path.join(BlenderUtils.GetUserConfigDir(), "templates", "%s.user" % filename)

	if os.path.exists(templateFilepathUser):
		templateFilepath = templateFilepathUser

	if not os.path.exists(templateFilepath):
		return ""

	return open(templateFilepath, 'r').read()

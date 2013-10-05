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

import os
import re
import socket
import subprocess
import sys
import tempfile
import time

from vb25                import utils
from vb25.lib.VRaySocket import VRaySocket
from vb25.debug          import Debug


# V-Ray process
PROC     = None
RUN_FILE = os.path.join(tempfile.gettempdir(), "vray_%s.run" % (utils.get_username()))


# Subprocess on Windows prefer <path>, on unix "<path>"
def format_path(path):
	return path if utils.PLATFORM == 'win32' else '"%s"'%(path)


# Process management
def run(params, engine='VRAY_RENDER_RT'):
	global PROC
	
	# if engine == 'VRAY_RENDER_RT':
	# 	PROC = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# else:
	# 	PROC = subprocess.Popen(params)
	PROC = subprocess.Popen(params)

	# Create pid file
	open(RUN_FILE, 'w')


def kill():
	global PROC
	
	if PROC is not None and PROC.poll() is None:
		# XXX: Zombie is still there
		PROC.kill()
	
	PROC = None
	if os.path.exists(RUN_FILE):
		os.remove(RUN_FILE)


def is_running():
	cmd_socket = VRaySocket()
	sock = cmd_socket.socket
	cmd_socket.disconnect()

	isRunning = None

	if sock is None:
		if os.path.exists(RUN_FILE):
			os.remove(RUN_FILE)
		isRunning = False
	else:		
		isRunning = True

	Debug("VRayProcess: is_running = %i" % isRunning)
	
	return isRunning


def reload_scene(scene_file):
	if scene_file is None:
		utils.debug(None, "Scene file is None!", error=True)
		return {'FAIL'}
	
	cmd_socket = VRaySocket()
	cmd_socket.send("stop")
	cmd_socket.send("unload")
	cmd_socket.send("load %s" % scene_file)
	cmd_socket.send("render")
	cmd_socket.disconnect()

	return None


def stop_render():
	cmd_socket = VRaySocket()
	cmd_socket.send("stop")
	cmd_socket.disconnect()

	return None

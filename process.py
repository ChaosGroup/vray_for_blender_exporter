#
# V-Ray/Blender
#
# http://vray.cgdo.ru
#
# Author: Andrey M. Izrantsev (aka bdancer)
# E-Mail: izrantsev@cgdo.ru
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


# Python modules
import os
import re
import socket
import subprocess
import sys
import tempfile
import time

# V-Ray/Blender modules
import vrayblender

from vrayblender.lib.VRaySocket import VRaySocket


# V-Ray process
PROC     = None
RUN_FILE = os.path.join(tempfile.gettempdir(), "vray_%s.run" % (vrayblender.utils.get_username()))


# Subprocess on Windows prefer <path>, on unix "<path>"
def format_path(path):
	return path if vrayblender.utils.PLATFORM == 'win32' else '"%s"'%(path)


# Process management
def run(params, pipe=False):
	global PROC

	if pipe:
		PROC = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
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

	if sock is None:
		if os.path.exists(RUN_FILE):
			os.remove(RUN_FILE)
		return False

	return True


def get_progress():
	global PROC

	if not PROC:
		return None

	if not PROC.stdout:
		return None

	msg  = None
	prog = None

	if PROC is not None and PROC.poll() is None:
		stdout_lines = PROC.stdout.read(512).decode('UTF-8').split('\n')
		for line in stdout_lines:

			if line.find("Building light cache") != -1:
				msg = "Light cache"
			elif line.find("Prepass") != -1:
				msg = "Irradiance map"
			elif line.find("Rendering image") != -1:
				msg = "Render"

			if msg is None:
				continue

			s = re.search('[-+]?([0-9]*\.[0-9]+|[0-9]+)', line)
			if s:
				f = s.group(0)
				if f is not None:
					prog = float(f) / 100.0
					break

	return prog


def reload_scene(scene_file):
	if scene_file is None:
		vrayblender.utils.debug(None, "Scene file is None!", error=True)
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


def grab_image(filepath):
	cmd_socket = VRaySocket()

	if not cmd_socket.connect():
		return {'SOCKET_FAIL'}

	# JPEG stream
	jpeg_image   = bytes()

	recv_stream  = True
	store_jpeg   = False
	recv_max_cnt = 20
	recv_cnt     = 0

	buff         = []

	cmd_socket.send("getImage 90 1")

	while(recv_stream):
		if not len(buff):
			# If buffer is empty - fill it
			# and check for fail
			b = cmd_socket.recv(1)
			if b is None:
				return {'SOCKET_FAIL'}
			buff.append( b )

			b = cmd_socket.recv(1)
			if b is None:
				return {'SOCKET_FAIL'}
			buff.append( b )

			if(buff[0] == b'f' and buff[1] == b'a'):
				return {'RENDER_STOPPED'}

		else:
			# If buffer is not empty - delete first element
			# and append new to the end
			buff = buff[1:]

			b = cmd_socket.recv(1)
			if b is None:
				return {'SOCKET_FAIL'}

			buff.append( b )

		if store_jpeg:
			jpeg_image += buff[-1]

		if(buff[0] == b'\xff' and buff[1] == b'\xd8'): # Start sig: FF D8
			store_jpeg = True

			jpeg_image += buff[0]
			jpeg_image += buff[1]

		if(buff[0] == b'\xff' and buff[1] == b'\xd9'): # End sig: FF D9
			# Terminate only if we recieve END SIGNATURE
			# while getting JPEG
			if store_jpeg:
				recv_stream = False

		if not store_jpeg:
			if recv_cnt > recv_max_cnt:
				return {'NO_JPEG_SIG'}

		recv_cnt += 1

	cmd_socket.disconnect()

	# Write stream to file
	jpeg_file = open(filepath, 'wb')
	jpeg_file.write(jpeg_image)
	jpeg_file.close()

	return None

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
import signal
import sys
import tempfile
import time

# V-Ray/Blender modules
import vb25
from vb25.lib import VRaySocket


# V-Ray process
PROC     = None
RUN_FILE = os.path.join(tempfile.gettempdir(), "vray_%s.run" % (vb25.utils.get_username()))


# Subprocess on Windows prefer <path>, on unix "<path>"
def format_path(path):
	return path if vb25.utils.PLATFORM == 'win32' else '"%s"'%(path)


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
		PROC.terminate()

	PROC = None
	if os.path.exists(RUN_FILE):
		os.remove(RUN_FILE)


def is_running():
	global PROC
	if PROC.poll() is None:
		return True
	return False


def get_progress():
	global PROC

	msg  = None
	prog = None

	if PROC is not None and PROC.poll() is None:
		stdout_lines = PROC.stdout.read(256).decode('UTF-8').split('\n')

		for line in stdout_lines:
			if line.find("Building light cache") != -1:
				msg = "Light cache"
			elif line.find("Prepass") != -1:
				prepass_num = line[line.find("Prepass")+7:line.find("of")].strip()
				msg = "Irradiance map (prepass %s)" % (prepass_num)
			elif line.find("Rendering image") != -1:
				msg = "Rendering"
			elif line.find("Building caustics photon map") != -1:
				msg = "Caustics"

			if msg is None:
				continue

			p_start = line.find("...: ") + 5
			p_end   = line.find("%")

			if p_start != -1 and p_end != -1 and p_end > p_start:
				p_str = line[p_start:p_end].strip()
				if len(p_str):
					prog = float(p_str) / 100.0
					break

		PROC.stdout.flush()

	return msg, prog


def reload_scene(scene_file):
	if scene_file is None:
		vb25.utils.debug(None, "Scene file is None!", error=True)
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


def exit():
	cmd_socket = VRaySocket()
	cmd_socket.send("quit")
	cmd_socket.disconnect()

	return None


def grab_image(filepath):
	cmd_socket = VRaySocket()

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

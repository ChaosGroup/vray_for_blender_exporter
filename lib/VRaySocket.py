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

# VRay Standalone communication socket

# Python modules
import socket


class VRaySocket():
	socket  = None
	address = "localhost"
	port    = 4368

	def __init__(self, address):
		self.address = address
		self.connect()

	def __init__(self):
		self.connect()

	def __del__(self):
		self.disconnect()

	def connect(self):
		self.disconnect()

		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.address, self.port))
		except socket.error:
			self.socket = None

		if self.socket is None:
			return False

		return True

	def disconnect(self):
		if self.socket is not None:
			self.socket.close()
			self.socket = None

	def send(self, cmd):
		if self.socket is None:
			self.connect()

		if self.socket is not None:
			try:
				self.socket.send(bytes(cmd+'\0','UTF-8'))
			except socket.error:
				self.connect()

	def recv(self, size):
		b = None
		try:
			b = self.socket.recv(size)
		except:
			pass
		return b

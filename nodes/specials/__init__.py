#
# V-Ray/Blender
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

__all__ = []


def register():
    from . import outputs
    from . import selector
    from . import environment
    from . import brdf
    from . import texture
    from . import effects
    from . import renderchannels

    outputs.register()
    selector.register()
    environment.register()
    brdf.register()
    texture.register()
    effects.register()
    renderchannels.register()

def unregister():
    from . import outputs
    from . import selector
    from . import environment
    from . import brdf
    from . import texture
    from . import effects
    from . import renderchannels

    outputs.unregister()
    selector.unregister()
    environment.unregister()
    brdf.unregister()
    texture.unregister()
    effects.unregister()
    renderchannels.unregister()

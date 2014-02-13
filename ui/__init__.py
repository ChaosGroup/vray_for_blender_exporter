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

__all__ = [ 'classes' ]


def register():
    from vb30.ui import classes
    from vb30.ui import properties_data_geometry
    from vb30.ui import properties_data_camera
    from vb30.ui import properties_data_lamp
    from vb30.ui import properties_data_empty
    from vb30.ui import properties_material
    from vb30.ui import properties_object
    from vb30.ui import properties_particles
    from vb30.ui import properties_render
    from vb30.ui import properties_render_layers
    from vb30.ui import properties_scene
    from vb30.ui import properties_texture
    from vb30.ui import properties_world

    classes.register()

    properties_data_geometry.register()
    properties_data_camera.register()
    properties_data_lamp.register()
    properties_data_empty.register()
    properties_material.register()
    properties_object.register()
    properties_particles.register()
    properties_render.register()
    properties_render_layers.register()
    properties_scene.register()
    properties_texture.register()
    properties_world.register()


def unregister():
    from vb30.ui import classes
    from vb30.ui import properties_data_geometry
    from vb30.ui import properties_data_camera
    from vb30.ui import properties_data_lamp
    from vb30.ui import properties_data_empty
    from vb30.ui import properties_material
    from vb30.ui import properties_object
    from vb30.ui import properties_particles
    from vb30.ui import properties_render
    from vb30.ui import properties_render_layers
    from vb30.ui import properties_scene
    from vb30.ui import properties_texture
    from vb30.ui import properties_world
    
    classes.unregister()

    properties_data_geometry.unregister()
    properties_data_camera.unregister()
    properties_data_lamp.unregister()
    properties_data_empty.unregister()
    properties_material.unregister()
    properties_object.unregister()
    properties_particles.unregister()
    properties_render.unregister()
    properties_render_layers.unregister()
    properties_scene.unregister()
    properties_texture.unregister()
    properties_world.unregister()

'''

 V-Ray/Blender 2.5

 http://vray.cgdo.ru

 Started:       29 Aug 2009
 Last Modified: 19 Jul 2010

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


import bpy


FloatProperty= bpy.types.Object.FloatProperty
IntProperty= bpy.types.Object.IntProperty
BoolProperty= bpy.types.Object.BoolProperty
StringProperty= bpy.types.Object.StringProperty
EnumProperty= bpy.types.Object.EnumProperty

BoolProperty(	attr="vray_proxy",
				name="Proxy",
				description="",
				default= False)

StringProperty( attr="vray_proxy_file",
				name="File",
				subtype= 'FILE_PATH',
				description="Proxy file.")

EnumProperty(   attr="vray_proxy_anim_type",
				name="Animation type",
				description="This determines the type of BRDF (the shape of the hilight).",
				items=(("LOOP",     "Loop",      "TODO."),
					   ("ONCE",     "Once",      "TODO."),
					   ("PINGPONG", "Ping-pong", "TODO."),
					   ("STILL",    "Still",     "TODO.")),
				default= "LOOP")

FloatProperty(  attr="vray_proxy_anim_speed",
				name="Speed",
				description="Animated proxy playback speed.",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=1.0, default= 1.0)

FloatProperty(  attr="vray_proxy_anim_offset",
				name="Offset",
				description="Animated proxy initial frame offset.",
				min=0.0, max=1000.0, soft_min=0.0, soft_max=1.0, default= 0.0)


class DataButtonsPanel(bpy.types.Panel):
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'

	def poll(self, context):
		engine = context.scene.render.engine
		return (context.object and context.object.type == 'EMPTY') and (engine in self.COMPAT_ENGINES)


class DATA_PT_vray_proxy(DataButtonsPanel):
	bl_label = "Proxy"
	bl_default_closed = True
	
	COMPAT_ENGINES = set(['VRAY_RENDER'])

	def draw_header(self, context):
		ob= context.object
		self.layout.prop(ob, "vray_proxy", text="")

	def draw(self, context):
		layout= self.layout
		
		ob= context.object

		layout.active= ob.vray_proxy

		split= layout.split()
		colL= split.column()
		colL.prop(ob, "vray_proxy_file")

		split= layout.split()
		colL= split.column()
		colL.label(text="Animation:")
		colR= split.column(align=True)
		colR.prop(ob, "vray_proxy_anim_type")
		colR.prop(ob, "vray_proxy_anim_speed")
		colR.prop(ob, "vray_proxy_anim_offset")

bpy.types.register(DATA_PT_vray_proxy)

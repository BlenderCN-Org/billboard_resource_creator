'''
Created by GameSolids

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>
	or write to the Free Software Foundation,
	Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

'''

import bpy, os
from os import path
from operator import itemgetter
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty

#bpy.ops.mesh.quads_convert_to_tris()

class gs_export_options(bpy.types.PropertyGroup):
	'''Items that will be created at export'''
	
	# diffuse texture atlas
	diffuse = bpy.props.BoolProperty(
		name="Diffuse",
		default=True
		)
	# normals map texture atlas
	normal = bpy.props.BoolProperty(
		name="Normals",
		default=True
		)
	# ambient occlusion texture atlas
	ambio = bpy.props.BoolProperty(
		name="AmbientOcclusion",
		default=False
		)
	# Unity3D component for assembling the billboard
	# as a Unity BillboardAsset
	unityComponent = bpy.props.BoolProperty(
		name="Unity3D Component",
		default=True
		)
	# Unity3D shader for displaying the 
	# BillboardAsset in Unity
	unityShader = bpy.props.BoolProperty(
		name="Unity3D Shader",
		default=False
		)
	# Unreal Engine Script for assembling the 
	# billboard in Unreal
	unrealComponent = bpy.props.BoolProperty(
		name="Unreal Component",
		default=False
		)


class gs_template_objects(bpy.types.PropertyGroup):
	'''Items that are stored as blender objects'''

	file = bpy.props.StringProperty(
		name="File",
		default=""
		)

	section = bpy.props.StringProperty(
		name="Section",
		default=""
		)

	billboard_object = bpy.props.StringProperty(
		name="Billboard",
		default=""
		)

	billboard_cage = bpy.props.StringProperty(
		name="Cage",
		default=""
		)

class RenderAtlasButton(bpy.types.Operator):
	''' Bake the textures, and write the files '''
	bl_idname = "gs_billboard.render_atlas"
	bl_label = "Render Atlas"
	bl_description = ""
	bl_options = {"REGISTER"}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		return {"FINISHED"}


class CheckSetupButton(bpy.types.Operator):
	''' Checks current Scene for Billboard Mesh and Cage,
		add them if not found. '''
	bl_idname = "gs_billboard.check_settings"
	bl_label = "Setup Billboard Rig"
	bl_description = ""
	bl_options = {"REGISTER"}

	@classmethod
	def poll(cls, context):
		return True

	def appendObject(self,context,name):
		
		return

	def appendMaterial(self, context, name):
		
		return

	def appendFromTemplate(self,context,typePath):
		'''opens addon template items'''
		script_file = os.path.realpath(__file__)
		directory = os.path.dirname(script_file)

		t = bpy.context.scene.gs_template

		t.file = os.path.join(directory, "template.blend")
		t.section = "\\"+typePath[0]+"\\"

		if typePath[1] is "Billboard":
			t.billboard_object = "Billboard"

		t_filepath  = t.file + t.section + typePath[1]
		t_directory = t.file + t.section
		t_filename  = typePath[1]

		bpy.ops.wm.append(
			filepath=t_filepath, 
			filename=t_filename,
			directory=t_directory
			)

	def execute(self, context):
		#find our active 3dView port
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						#move cursor to Interest point, update view port
						context_override = bpy.context.copy()
						context_override['area'] = area
						context_override['region'] = region
						# context_override now refferrs to the Active View3D

		print(bpy.context.scene.objects.active.name)

		#only link template items if we haven't assigned them already
		if bpy.context.scene.gs_template.billboard_object is "":
			self.appendFromTemplate(context,("Object","Billboard"))
			self.appendFromTemplate(context,("Object","BillboardCage"))
			self.appendFromTemplate(context,("Material","Billboard_material"))
		else:
			print("doyle")

		return {"FINISHED"}


def initSceneProperties():
	# File path matches the Unity Example
	bpy.types.Scene.gs_billboard_path = bpy.props.StringProperty(
		name = "Export Path", 
		default = "./",
		subtype='DIR_PATH'
		)

	bpy.types.Scene.gs_billboard_mesh = bpy.props.StringProperty(
		name = "Billboard"
		) #?

	bpy.types.Scene.gs_settings = bpy.props.PointerProperty(
		type=gs_export_options
		)

	bpy.types.Scene.gs_template = bpy.props.PointerProperty(
		type=gs_template_objects
		)

	return


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

import bpy, os, logging
from os import path
from operator import itemgetter
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

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

	billboard_cage_material = bpy.props.StringProperty(
		name="Cage.Material",
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

		# check objects are selected
		if len(scene.objects) > 0:
			if scene.objects.active is not None:
				logging.info(scene.objects.active.name)

		return {"FINISHED"}


class CheckSetupButton(bpy.types.Operator):
	''' Checks current Scene for Billboard Mesh and Cage,
		add them if not found. '''
	bl_idname = "gs_billboard.template_setup"
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
		t = bpy.context.scene.gs_template
		# get template file in Addon directory
		t.file = os.path.join(SCRIPT_DIR, "template.blend")
		t.section = "\\"+typePath[0]+"\\"

		# append Bleder necessary blender objects
		t_filepath  = t.file + t.section + typePath[1]
		t_directory = t.file + t.section
		t_filename  = typePath[1]

		bpy.ops.wm.append(
			filepath=t_filepath, 
			filename=t_filename,
			directory=t_directory
			)

		logging.info(typePath[1]+" loaded from template")

		return typePath[1]

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
		
		logging.info("Starting setup helper...")

		scene = bpy.context.scene
		t = scene.gs_template

		''' only link template items if we haven't assigned them already
			check1 is to see if anything has been assigned
			check2 is to see if user-defined objects has been assigned 
		'''
		gs_bb_check1 = t.billboard_object is ""
		gs_bb_check2 = t.billboard_object not in scene.objects
		if gs_bb_check1 and gs_bb_check2 :
			t.billboard_object = self.appendFromTemplate(
				context,("Object","Billboard")
				)
		else:
			logging.info("Using current Billboard: name here")

		gs_bc_check1 = t.billboard_cage is ""
		gs_bc_check2 = t.billboard_cage not in scene.objects
		if gs_bc_check1 and gs_bc_check2 :
			t.billboard_cage = self.appendFromTemplate(
				context,("Object","BillboardCage")
				)
		else:
			logging.info("Using current BillboardCage")

		gs_bm_check1 = t.billboard_cage_material is ""
		gs_bm_check2 = t.billboard_cage_material not in bpy.data.materials
		if gs_bm_check1 and gs_bm_check2 :
			t.billboard_cage_material = self.appendFromTemplate(
				context,("Material","Billboard_material")
				)
		else:
			logging.info("Using current Material")
		
		logging.info("Setup helper done")
		return {"FINISHED"}


def initSceneProperties():
	# File path matches the Unity Example
	bpy.types.Scene.gs_billboard_path = bpy.props.StringProperty(
		name = "Export Path", 
		default = "//",
		subtype='DIR_PATH'
		)

	bpy.types.Scene.gs_settings = bpy.props.PointerProperty(
		type=gs_export_options
		)

	bpy.types.Scene.gs_template = bpy.props.PointerProperty(
		type=gs_template_objects
		)

	return


'''
	*** Begin GPL License Block ***

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

	*** End GPL License Block ***
'''
''' (c)2018 GameSolids '''

''' Logic module for Billboard templates and file setup '''

import bpy, os, logging
from . import template_description
from os import path
from operator import itemgetter
from bpy.props import CollectionProperty, FloatVectorProperty, StringProperty
from bpy.props import BoolProperty, EnumProperty, IntProperty
from bpy_extras.io_utils import ImportHelper

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class gs_export_options(bpy.types.PropertyGroup):
	'''Items that will be created at export'''
	
	# diffuse texture atlas
	filename = bpy.props.StringProperty(
		name="Base Name",
		default="billboard_name"
		)
	# diffuse texture atlas
	diffuse = bpy.props.BoolProperty(
		name="Diffuse",
		default=True
		)
	diffuse_sfx = bpy.props.StringProperty(
		name=" ",
		default="_d"
		)
	# normals map texture atlas
	normal = bpy.props.BoolProperty(
		name="Normals",
		default=True
		)
	normal_sfx = bpy.props.StringProperty(
		name=" ",
		default="_n"
		)
	# ambient occlusion texture atlas
	ambio = bpy.props.BoolProperty(
		name="AmbientOcclusion",
		default=False
		)
	ambio_sfx = bpy.props.StringProperty(
		name=" ",
		default="_ao"
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

class ListItem(bpy.types.PropertyGroup):
	''' simple struct to add Index to set of Strings '''
	name = bpy.props.StringProperty(name="Object Name", default="Unknown")
	index = bpy.props.IntProperty(name="Ref", default=22, subtype='UNSIGNED')



class gs_template_objects(bpy.types.PropertyGroup):
	'''Billboard items stored in the scene'''

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

	group_objects = bpy.props.CollectionProperty(
		type=ListItem
		)

	name = bpy.props.CollectionProperty(
		type=ListItem
		)

	index = bpy.props.IntProperty()


def DialogSimple(self, context, message = "", title = "Notice: ", icon = 'INFO'):
	''' Simple message alert box '''

	def draw(self, context):
		self.layout.label(message)
	
	bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

class DialogConfirm(bpy.types.Operator):
    """ This will over write your current settings. """
    bl_idname = "my_category.custom_confirm_dialog"
    bl_label = "Over write current template?"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "CONTINUE")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class RenderAtlasButton(bpy.types.Operator):
	''' Bake the textures, and write the files '''
	bl_idname = "gs_billboard.render_atlas"
	bl_label = "Render Atlas"
	bl_description = ""
	bl_options = {"REGISTER"}

	@classmethod
	def poll(cls, context):
		return True
	
	def setSelection(self, context):
		''' Setup Baking selection, activate cage '''

		# some shorthand for common objects
		scene = bpy.context.scene
		t = scene.gs_template

		# store selected objects
		obj_active = scene.objects.active
		selection = bpy.context.selected_objects

		# check selected objects
		if len(selection) > 0:
			if t.billboard_cage is not "":
				scene.objects[t.billboard_cage].select = True
				scene.objects.active = scene.objects[t.billboard_cage]
				return True
			else: 
				ShowMessageBox(self, context, "You need to set Billboard and BillboardCage")
				logging.warning("Scene not setup correctly")
		else: 
			ShowMessageBox(self, context, "You need to select at least one mesh object.")
			logging.warning("No objects were selected")


		return False

	def hasImage(self, context):
		''' Select or Create image to bake to '''
		image = bpy.data.images["BillboardBaker"]
		
		#if image is None:
		#	image = bpy.data.images.new("BillboardBaker", width=1024, height=1024)


		return True

	def bakeSelectedOptions(self):

		# some shorthand for common objects
		scene = bpy.context.scene
		t = scene.gs_template
		obj_active = scene.objects.active

		# start bakes
		if scene.gs_settings.diffuse:

			fName = obj_active.name +"_d.png"
			fPath = os.path.join(scene.gs_billboard_path, fName)

			bpy.ops.object.bake(
				type='DIFFUSE', 
				pass_filter={'COLOR'}, 
				filepath=fPath, 
				width=1024, height=1024, 
				margin=1, 
				use_selected_to_active=True, 
				save_mode='INTERNAL', 
				use_split_materials=False
				)
			image = bpy.data.images["BillboardBaker"]
			image.filepath_raw = fPath
			image.save()

		# start bakes
		if scene.gs_settings.normal:

			fName = obj_active.name +"_n.png"
			fPath = os.path.join(scene.gs_billboard_path, fName)

			bpy.ops.object.bake(
				type='NORMAL', 
				pass_filter={'COLOR'}, 
				filepath=fPath, 
				width=1024, height=1024, 
				margin=1, 
				use_selected_to_active=True, 
				save_mode='INTERNAL', 
				use_split_materials=False
				)
			image = bpy.data.images["BillboardBaker"]
			image.filepath_raw = fPath
			image.save()

		if scene.gs_settings.unityComponent:
			from . import billboard_unity
			billboard_unity.writeUnityComponent()

	def execute(self, context):

		# some shorthand for common objects
		scene = bpy.context.scene
		t = scene.gs_template
		obj_active = scene.objects.active

		# check objects are selected
		if len(scene.objects) > 0 and scene.objects.active is not None:
				logging.info("Setting up baking for: "+scene.objects.active.name)

				# check material image is available
				if self.setSelection(context) and self.hasImage(context):
					# make sure cage UV is mapped for baking
					for uv_face in scene.objects.active.data.uv_textures["UVMap"].data:
						uv_face.image = bpy.data.images["BillboardBaker"]

					logging.info("Bake starting...")

				else:
					logging.info("Baking Canceled")
		else:
			logging.warning("billboard template not defined")

		# do it
		self.bakeSelectedOptions()

		return {"FINISHED"}

# could not figure out putting this in a class
def group_getter(self, context):
	''' returns list of Group names from template. '''
	filepath = os.path.join(SCRIPT_DIR, "template.blend")
	with bpy.data.libraries.load(filepath) as (data_from, data_to):
		# operate directly on external data
		for group in range(len(data_from.groups)):
			if group is not None:
				print(data_from.groups[group])
				yield (str(group), data_from.groups[group], "")


class SetupTemplateButton(bpy.types.Operator):
	''' Checks current Scene for Billboard Mesh and Cage,
		add them if not found. '''
	bl_idname = "gs_billboard.template_setup"
	bl_label = "Load Template"
	
	instance_groups = True
	directory = ""
	
	@classmethod
	def poll(cls, context):
		return True


	def findActiveView3D(self, context):
		''' returns active 3dView port or current context '''
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						#move cursor to Interest point, update view port
						context_override = bpy.context.copy()
						context_override['area'] = area
						context_override['region'] = region
						# context_override now refferrs to the Active View3D
		
						return context_override
		return context


	def appendFromTemplate(self,context,typePath):
		''' copy object presets from blender file '''

		# some shorthand for common objects
		scene = bpy.context.scene
		t = scene.gs_template

		# open template file in Addon directory
		t.file = os.path.join(SCRIPT_DIR, "template.blend")
		t.section = "\\"+typePath[0]+"\\"

		# append necessary blender objects
		t_filepath  = t.file + t.section + typePath[1]
		t_directory = t.file + t.section
		t_filename  = typePath[1]

		bpy.ops.wm.append(
			filepath=t_filepath, 
			filename=t_filename,
			directory=t_directory
			)

		logging.info(typePath[1]+" loaded from template")

		# return object name
		return typePath[1]


	def invoke(self, context, event):
		# set template 
		self.directory = os.path.join(SCRIPT_DIR, "template.blend\\Group\\")

		# reset dialog list
		scene = bpy.context.scene
		scene.gs_template.name.clear()
		# populate dialog list
		for index, name, _ in group_getter(self, context):
			item = scene.gs_template.name.add()
			item.index = int(index)
			item.name = name
		# open dialog window
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=400, height=240)
	

	def draw(self, context):

		layout = self.layout
		scene = bpy.context.scene
		# show single column list
		col = layout.column()
		col.template_list( 
			"UI_UL_list", "template_list", 
			scene.gs_template, "name", 
			scene.gs_template, "index", 
			rows=1 
			)


	def execute(self, context):
		''' on execute, examin selection and append that template '''

		scene = bpy.context.scene
		t = scene.gs_template

		# store selection in current scene
		# used to restore user state after import is done
		obj_active = scene.objects.active
		selection = bpy.context.selected_objects

		logging.info("Starting setup helper...")

		scene = bpy.context.scene
		index = scene.gs_template.index
		message = '%s (index %d) selected' % (
			scene.gs_template.name[index].name, 
			index
			)
		selected = scene.gs_template.name[index].name
		print(selected)
		if selected in bpy.data.groups:
			print("use existing")
		else:
			print("use template group")
			self.appendFromTemplate(
				context,("Group",selected)
				)


		#print(scene.gs_template.name[index].name)
		# returns after method call, instead of logging
		# which is called inline
		self.report({'INFO'}, message)

		return {"FINISHED"}


	def executes(self, context):

		# some shorthand for common objects
		scene = bpy.context.scene
		t = scene.gs_template

		# store selection
		obj_active = scene.objects.active
		selection = bpy.context.selected_objects

		logging.info("Starting setup helper...")

		''' only link template items if we haven't assigned them already
			check1 is to see if billboard exists
			check2 is to see if user-defined billboard has been assigned 
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

		# ensure material makes it, regardless of global import settings
		gs_bm_check1 = t.billboard_cage_material is ""
		gs_bm_check2 = t.billboard_cage_material not in bpy.data.materials
		if gs_bm_check1 and gs_bm_check2 :
			t.billboard_cage_material = self.appendFromTemplate(
				context,("Material","Billboard_material")
				)
		else:
			logging.info("Using current Material")
		
		# retrieve selection
		scene.objects.active = obj_active
		for obj in selection:
			obj.select = True

		logging.info("Setup helper done")

		return {"FINISHED"}



class ClearTemplateButton(bpy.types.Operator):
	''' Checks current Scene for Billboard Mesh and Cage,
		add them if not found. '''
	bl_idname = "gs_billboard.template_clear"
	bl_label = "Clear Rig"
	bl_description = ""
	bl_options = {"REGISTER"}
	
	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		return {"FINISHED"}


def initSceneProperties():
	# File path matches the Unity Example

	bpy.types.Scene.gs_template = bpy.props.PointerProperty(
		type=gs_template_objects
		)

	bpy.types.Scene.gs_billboard_path = bpy.props.StringProperty(
		name = "Export Path", 
		default = os.path.join(os.path.expanduser('~'), "billboard"+os.path.sep),
		subtype='DIR_PATH'
		)

	bpy.types.Scene.gs_settings = bpy.props.PointerProperty(
		type=gs_export_options
		)

	logging.info("Template Scene Properties have been added")

	return


def clearSceneProperties():
	# File path matches the Unity Example

	del bpy.types.Scene.gs_template
	del bpy.types.Scene.gs_billboard_path
	del bpy.types.Scene.gs_settings

	logging.info("Template Scene Properties have been removed")

	return


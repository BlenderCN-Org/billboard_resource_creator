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

bl_info = {
	"name": "Billboard Resource Creator",
	"description": "Creates texture atlas and like for 3d billboards",
	"author": "GameSolids",
	"version": (0, 0, 1),
	"blender": (2, 79, 0),
	"location": "View3D > UI > Billboard Resources",
	"warning": "This addon is still in development.",
	"wiki_url": "",
	"category": "Import-Export" 
}

if "bpy" in locals():
	import importlib
	importlib.reload(billboard_ops)
	importlib.reload(billboard_ui)
else:
	from .billboard_resources import billboard_ops
	from .billboard_resources import billboard_ui

import bpy


# register
##################################

import traceback

def register():

	try: bpy.utils.register_module(__name__)
	except: traceback.print_exc()

	billboard_ops.initSceneProperties()
	
	print("Registered {} with {} modules".format(bl_info["name"], str(2)))


def unregister():
	try: bpy.utils.unregister_module(__name__)
	except: traceback.print_exc()

	print("Unregistered {}".format(bl_info["name"]))

	#del bpy.types.Object.billboard_mesh

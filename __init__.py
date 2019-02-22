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

''' module imports and reloading '''
if "bpy" in locals():
	import importlib
	importlib.reload(billboard_ops)
	importlib.reload(billboard_ui)
else:
	from .billboard_resources import billboard_ops
	from .billboard_resources import billboard_ui

import bpy, os, logging, traceback


''' Settings and Addon options that 
	help with debugging and development.'''
LOG_TO_FILE = True
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

''' debug logging '''
if LOG_TO_FILE is True:
	logging.basicConfig(
		filename=os.path.join(SCRIPT_DIR,'example.log'),
		level=logging.DEBUG
		)
	logging.getLogger().addHandler(logging.StreamHandler())
else:
	logging.basicConfig(format='%(message)s',level=logging.INFO)


# registration hooks
##################################
def register():
	''' start registering Blender components'''
	try: bpy.utils.register_module(__name__)
	except: logging.error(traceback.message)

	try: billboard_ops.initSceneProperties()
	except: logging.error(traceback.message)

	''' presume normal operation'''
	logging.info(
		"Registered {} with {} modules".
		format(bl_info["name"], str(2))
		)


def unregister():
	''' remove Blender components when disabling addon'''
	try: bpy.utils.unregister_module(__name__)
	except: traceback.print_exc()

	logging.info(
		"Unregistered {}".
		format(bl_info["name"])
		)


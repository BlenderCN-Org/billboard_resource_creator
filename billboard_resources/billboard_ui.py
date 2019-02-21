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

import bpy
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty

class BillboardResourcesPanel(bpy.types.Panel):
	bl_idname = "VIEW_3D_PT_billboard_resources"
	bl_label = "Billboard Resources"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_context = "view3d"

	def draw(self, context):
		scene = context.scene               
		layout = self.layout
		layout.prop(scene, "gs_billboard_path")
		#layout.prop_search(scene, "gs_billboard_mesh", scene, "objects")
		layout.operator("gs_billboard.check_settings")
		layout.label(text="Export Options")
		layout.prop(scene.gs_settings, "diffuse")
		layout.prop(scene.gs_settings, "normal")
		layout.prop(scene.gs_settings, "ambio")
		layout.prop(scene.gs_settings, "unityComponent")
		layout.prop(scene.gs_settings, "unrealComponent")
		layout.operator("gs_billboard.render_atlas", text="Export Package")


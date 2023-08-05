import bpy

class YogasmaraDeleteAll(bpy.types.Operator):
    """Delete all available object on the scene"""
    bl_idname = "object.yogasmara_delete_all"
    bl_label = "Delete All Object"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)
        
        return {'FINISHED'}
        
        
class YogasmaraFileManager(bpy.types.Panel):
    """Yogasmara file manager"""
    bl_idname = "PANEL_PT_yogasmara_file_manager" # Panel Type yogasmara file manager
    bl_category = "Yogasmara Addon" # Name of the addon
    bl_space_type = "VIEW_3D" # where the addon will be placed
    bl_region_type = "UI"
    bl_label = "File Manager"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("wm.open_mainfile", text="Open File", icon="FILEBROWSER")
        
        row = layout.row()
        row.operator("wm.save_mainfile", text="Save File", icon="FILE_TICK")
        
class YogasmaraObjectManager(bpy.types.Panel):
    """Yogasmara object manager"""
    bl_idname = "PANEL_PT_yogasmara_object_manager"
    bl_category = "Yogasmara Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Object Manager"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.delete", text="Delete Selected Object")
        
        row = layout.row()
        row.operator("object.delete_all", text="Delete All Object")
        
        row = layout.row()
        row.operator("object.select_all", text="Select All Object")
        
class YogasmaraMeshManager(bpy.types.Panel):
    """Yogasmara mesh manager"""
    bl_idname = "PANEL_PT_yogasmara_mesh_manager"
    bl_category = "Yogasmara Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Mesh Manager"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("mesh.primitive_plane_add", text="Add New Plane", icon="MESH_PLANE")
        
        row = layout.row()
        row.operator("mesh.primitive_cube_add", text="Add New Cube", icon="MESH_CUBE")
        
        row = layout.row()
        row.operator("mesh.primitive_circle_add", text="Add New Circle", icon="MESH_CIRCLE")
        
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", text="Add New UV Sphere", icon="MESH_UVSPHERE")
        
        row = layout.row()
        row.operator("mesh.primitive_ico_sphere_add", text="Add New ICO Sphere", icon="MESH_ICOSPHERE")
        
        row = layout.row()
        row.operator("mesh.primitive_cylinder_add", text="Add New Cylinder", icon="MESH_CYLINDER")
        
        row = layout.row()
        row.operator("mesh.primitive_cone_add", text="Add New Cone", icon="MESH_CONE")
        
        row = layout.row()
        row.operator("mesh.primitive_torus_add", text="Add New Torus", icon="MESH_TORUS")
        
        
 
def register():
    bpy.utils.register_class(YogasmaraFileManager)
    bpy.utils.register_class(YogasmaraObjectManager)
    bpy.utils.register_class(YogasmaraMeshManager)
    bpy.utils.register_class(YogasmaraDeleteAll)

def unregister():
    bpy.utils.unregister_class(YogasmaraFileManager)
    bpy.utils.unregister_class(YogasmaraObjectManager)
    bpy.utils.unregister_class(YogasmaraMeshManager)
    bpy.utils.unregister_class(YogasmaraDeleteAll)
        
if __name__ == "__main__":
    register()
    

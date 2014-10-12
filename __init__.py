bl_info = {
    "name":         "OGL Lib Pose Library",
    "author":       "Tyler Schicke",
    "blender":      (2, 6, 2),
    "version":      (0, 0, 1),
    "location":     "File > Import-Export",
    "description":  "Export Pose Library for OGL Lib",
    "category":     "Import-Export"
}

if "bpy" in locals():
    import imp;
    if "export_poslib" in locals():
        imp.reload(export_poslib);

import bpy
from bpy_extras.io_utils import ExportHelper

class OGLExporter(bpy.types.Operator, ExportHelper):
    bl_idname       = "export_poslib.poslib"
    bl_label        = "OGL Pose Library Exporter"
    bl_options      = {'PRESET'}
    
    filename_ext    = ".poslib"
    
    def execute(self, context):
        from . import export_poslib
        
        return export_poslib.save(self, context, self.filepath)
        
def menu_func(self, context):
    self.layout.operator(OGLExporter.bl_idname, text="OGL Pose Library Format (.poslib)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
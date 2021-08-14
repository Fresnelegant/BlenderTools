bl_info = {
    "name": "BillboardTools",
    "author": "Fresnelegant",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "description": "Scripts for preparing meshes to be used as billboards",
    "category": "Mesh",
}

import bpy
import bmesh

class MESH_OT_Shrink_Faces(bpy.types.Operator):
    bl_label = "Shrink Faces"
    bl_idname = "mesh.shrink_faces"
    bl_description = "Shrinks all selected faces to their individual origins"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # valid if any selected object is a mesh and we're in edit mode
        return (
            bpy.context.mode == 'EDIT_MESH' and
            bpy.context.selected_objects and
            any(ob.type == 'MESH' for ob in bpy.context.selected_objects)
        )

    def execute(self, context):
        # get selection
        selected_mesh_obs = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH']
        # split up all faces
        bpy.ops.mesh.edge_split(type='EDGE')
        # shrink faces
        for ob in selected_mesh_obs:
            bm = bmesh.from_edit_mesh(ob.data)

            selected_faces = [face for face in bm.faces if face.select]
            for face in selected_faces:
                c = face.calc_center_median()
                for v in face.verts:
                    v.co = c + 0.0025 * (v.co - c).normalized()
            bmesh.update_edit_mesh(ob.data)
        return {"FINISHED"}

class VIEW3D_PT_BillboardTools(bpy.types.Panel):
    bl_label = "Billboard Tools"
    bl_idname = "VIEW3D_PT_billboardtools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Billboard"
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        layout.label(text="UV:")
        layout.operator("uv.reset", text="Normalize UVs")
        layout.label(text="Mesh:")
        #layout = layout.box()
        layout.operator(MESH_OT_Shrink_Faces.bl_idname, text="Shrink Faces")
        #layout.label(text="Vertex Color:")
        #layout.label(text="...")

classes = (
    MESH_OT_Shrink_Faces,
    VIEW3D_PT_BillboardTools
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

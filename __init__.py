import bpy

bl_info = {
    "name": "CC0 Assets Loader",
    "author": "Yuki Koyama",
    "version": (0, 0, 0),
    "blender": (2, 80, 0),
    "location": "Shader Editor > Add",
    "description": "Loading CC0 Assets",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/yuki-koyama/cc0-assets-loader",
    "tracker_url": "https://github.com/yuki-koyama/cc0-assets-loader/issues",
    "category": "Material"
}


class CC0_ASSETS_LOADER_OP_AddMetal07Material(bpy.types.Operator):
    bl_idname = "node.add_metal07_material"
    bl_label = "Add Metal07 Material"
    bl_description = "Add Metal07 material to the data block"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(CC0_ASSETS_LOADER_OP_AddMetal07Material.bl_idname)


def register():
    bpy.utils.register_class(CC0_ASSETS_LOADER_OP_AddMetal07Material)
    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    bpy.types.NODE_MT_add.remove(menu_func)
    bpy.utils.unregister_class(CC0_ASSETS_LOADER_OP_AddMetal07Material)


if __name__ == "__main__":
    register()

import bpy
import os

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

package_dir = os.path.dirname(os.path.abspath(__file__))

materials = {
    "Metal07": {
        "color": package_dir + "/assets/cc0textures.com/[2K]Metal07/Metal07_col.jpg",
        "metallic": package_dir + "/assets/cc0textures.com/[2K]Metal07/Metal07_met.jpg",
        "roughness": package_dir + "/assets/cc0textures.com/[2K]Metal07/Metal07_rgh.jpg",
        "normal": package_dir + "/assets/cc0textures.com/[2K]Metal07/Metal07_nrm.jpg",
        "displacement": package_dir + "/assets/cc0textures.com/[2K]Metal07/Metal07_disp.jpg",
        "ambient_occlusion": "",
    },
}


def create_texture_node(node_tree, path, is_color_data):
    # Instantiate a new texture image node
    texture_node = node_tree.nodes.new(type='ShaderNodeTexImage')

    # Open an image and set it to the node
    texture_node.image = bpy.data.images.load(path)

    # Set other parameters
    texture_node.image.colorspace_settings.is_data = False if is_color_data else True

    # Return the node
    return texture_node


def build_pbr_textured_nodes(node_tree,
                             color_texture_path="",
                             metallic_texture_path="",
                             roughness_texture_path="",
                             normal_texture_path="",
                             displacement_texture_path="",
                             ambient_occlusion_texture_path="",
                             scale=(1.0, 1.0, 1.0)):
    output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    coord_node = node_tree.nodes.new(type='ShaderNodeTexCoord')
    mapping_node = node_tree.nodes.new(type='ShaderNodeMapping')
    mapping_node.vector_type = 'TEXTURE'
    mapping_node.scale = scale
    node_tree.links.new(coord_node.outputs['UV'], mapping_node.inputs['Vector'])

    if color_texture_path != "":
        texture_node = create_texture_node(node_tree, color_texture_path, True)
        node_tree.links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        if ambient_occlusion_texture_path != "":
            ao_texture_node = create_texture_node(node_tree, ambient_occlusion_texture_path, False)
            node_tree.links.new(mapping_node.outputs['Vector'], ao_texture_node.inputs['Vector'])
            mix_node = node_tree.nodes.new(type='ShaderNodeMixRGB')
            mix_node.blend_type = 'MULTIPLY'
            node_tree.links.new(texture_node.outputs['Color'], mix_node.inputs['Color1'])
            node_tree.links.new(ao_texture_node.outputs['Color'], mix_node.inputs['Color2'])
            node_tree.links.new(mix_node.outputs['Color'], principled_node.inputs['Base Color'])
        else:
            node_tree.links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])

    if metallic_texture_path != "":
        texture_node = create_texture_node(node_tree, metallic_texture_path, False)
        node_tree.links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        node_tree.links.new(texture_node.outputs['Color'], principled_node.inputs['Metallic'])

    if roughness_texture_path != "":
        texture_node = create_texture_node(node_tree, roughness_texture_path, False)
        node_tree.links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        node_tree.links.new(texture_node.outputs['Color'], principled_node.inputs['Roughness'])

    if normal_texture_path != "":
        texture_node = create_texture_node(node_tree, normal_texture_path, False)
        node_tree.links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
        node_tree.links.new(texture_node.outputs['Color'], normal_map_node.inputs['Color'])
        node_tree.links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])

    if displacement_texture_path != "":
        texture_node = create_texture_node(node_tree, displacement_texture_path, False)
        node_tree.links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        node_tree.links.new(texture_node.outputs['Color'], output_node.inputs['Displacement'])


def clean_nodes(nodes):
    for node in nodes:
        nodes.remove(node)


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

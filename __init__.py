import bpy
import glob
import os
from typing import Tuple

bl_info = {
    "name": "CC0 Assets Loader",
    "author": "Yuki Koyama",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Shader Editor > Add",
    "description": "Loading CC0 Assets",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/yuki-koyama/cc0assetsloader",
    "tracker_url": "https://github.com/yuki-koyama/cc0assetsloader/issues",
    "category": "Material"
}

################################################################################
# Material definition
################################################################################

materials = {}
package_dir = os.path.dirname(os.path.abspath(__file__))
dir_paths = glob.glob(glob.escape(package_dir) + "/assets/cc0textures.com/*")
for dir_path in dir_paths:
    _, name = dir_path.rsplit("]", 1)

    def get_file_path(type):
        files = glob.glob(glob.escape(dir_path) + "/*_" + type + ".jpg")
        return files[0] if files else ""

    texture_paths = {}
    texture_paths["color"] = get_file_path("col")
    texture_paths["metallic"] = get_file_path("met")
    texture_paths["roughness"] = get_file_path("rgh")
    texture_paths["normal"] = get_file_path("nrm")
    texture_paths["displacement"] = get_file_path("disp")
    texture_paths["ambient_occlusion"] = get_file_path("AO")

    materials[name] = texture_paths

################################################################################
# Utility functions
################################################################################

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import nodelayout


def create_texture_node(node_tree: bpy.types.NodeTree, path: str, is_color_data: bool) -> bpy.types.Node:
    # Instantiate a new texture image node
    texture_node = node_tree.nodes.new(type='ShaderNodeTexImage')

    # Open an image and set it to the node
    texture_node.image = bpy.data.images.load(path)

    # Set other parameters
    if bpy.app.version >= (2, 80, 0):
        texture_node.image.colorspace_settings.is_data = False if is_color_data else True
    else:
        texture_node.color_space = 'COLOR' if is_color_data else 'NONE'

    # Return the node
    return texture_node


def build_pbr_textured_nodes(node_tree: bpy.types.NodeTree,
                             color_texture_path: str = "",
                             metallic_texture_path: str = "",
                             roughness_texture_path: str = "",
                             normal_texture_path: str = "",
                             displacement_texture_path: str = "",
                             ambient_occlusion_texture_path: str = "",
                             scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)) -> None:
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

    nodelayout.arrange_nodes(node_tree, use_current_layout_as_initial_guess=False)


def clean_nodes(nodes: bpy.types.Nodes) -> None:
    for node in nodes:
        nodes.remove(node)


def build_pbr_textured_nodes_from_name(material_name: str, scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)) -> None:
    new_material = bpy.data.materials.new(material_name)
    new_material.use_nodes = True
    clean_nodes(new_material.node_tree.nodes)

    build_pbr_textured_nodes(new_material.node_tree,
                             color_texture_path=materials[material_name]["color"],
                             metallic_texture_path=materials[material_name]["metallic"],
                             roughness_texture_path=materials[material_name]["roughness"],
                             normal_texture_path=materials[material_name]["normal"],
                             displacement_texture_path=materials[material_name]["displacement"],
                             ambient_occlusion_texture_path=materials[material_name]["ambient_occlusion"],
                             scale=scale)


################################################################################
# Operators
################################################################################


class AddMaterialOperator(bpy.types.Operator):
    bl_options = {"REGISTER", "UNDO"}

    material_name = None

    def execute(self, context):
        if bpy.data.materials.find(self.material_name) >= 0:
            self.report({'ERROR'}, self.material_name + " is already defined in the materials data block.")
            return {'CANCELLED'}

        build_pbr_textured_nodes_from_name(self.material_name)

        return {'FINISHED'}


operator_classes = []
for material_name in sorted(materials.keys()):
    operator_class = type(
        "CC0_ASSETS_LOADER_OP_Add" + material_name + "Material", (AddMaterialOperator, ), {
            "material_name": material_name,
            "bl_idname": "node.add_" + material_name.lower() + "_material",
            "bl_label": material_name,
            "bl_description": "Add " + material_name + " material to the data block",
        })

    operator_classes.append(operator_class)


class CC0_ASSETS_LOADER_MT_Menu(bpy.types.Menu):
    bl_idname = "CC0_ASSETS_LOADER_MT_Menu"
    bl_label = "CC0 Textured Materials"
    bl_description = "Add predefined CC0 textured materials to the data block"

    def draw(self, context):
        for operator_class in operator_classes:
            self.layout.operator(operator_class.bl_idname)


def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(CC0_ASSETS_LOADER_MT_Menu.bl_idname)


def register():
    bpy.utils.register_class(CC0_ASSETS_LOADER_MT_Menu)
    for operator_class in operator_classes:
        bpy.utils.register_class(operator_class)

    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    bpy.types.NODE_MT_add.remove(menu_func)

    for operator_class in operator_classes:
        bpy.utils.unregister_class(operator_class)
    bpy.utils.unregister_class(CC0_ASSETS_LOADER_MT_Menu)


if __name__ == "__main__":
    register()

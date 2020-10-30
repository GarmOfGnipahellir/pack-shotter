import os
import bpy
import nodeitems_utils
from .common import PackShotterNode, PackShotterNodeCategory


# ---------------------------------------------------------------------------- #
#                                   Base Type                                  #
# ---------------------------------------------------------------------------- #


class PackShotterVariationsNode(PackShotterNode):
    def __iter__(self):
        self._current = 0
        self._num_variations = self.get_num_variations()
        return self

    def __next__(self):
        if self._current < self._num_variations:
            index = self._current
            self._current += 1
            return index
        else:
            raise StopIteration

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")
        self.outputs.new('NodeSocketVirtual', "Output")

    def apply_variation(self, index):
        raise NotImplementedError

    def revert_variation(self):
        raise NotImplementedError

    def get_variation_name(self, index):
        raise NotImplementedError

    def get_num_variations(self):
        return 0


# ---------------------------------------------------------------------------- #
#                               Image Variations                               #
# ---------------------------------------------------------------------------- #


class PackShotterImageVariationsNode(PackShotterVariationsNode):
    bl_idname = "PackShotterImageVariationsNode"
    bl_label = "Image Variations"
    bl_icon = 'FILE_IMAGE'

    image: bpy.props.PointerProperty(type=bpy.types.Image, name="Image",
                                     description="The image that wil have it's file changed for different variations")
    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The folder which contains the image variations")

    def draw_buttons(self, context, layout):
        layout.prop(self, "image")
        layout.prop(self, "folder")

    def apply_variation(self, index):
        self._tmp_filepath = self.image.filepath
        file = os.listdir(bpy.path.abspath(self.folder))[index]
        self.image.filepath = os.path.join(self.folder, file)

    def revert_variation(self):
        self.image.filepath = self._tmp_filepath

    def get_variation_name(self, index):
        file = os.listdir(bpy.path.abspath(self.folder))[index]
        return bpy.path.display_name(file)

    def get_num_variations(self):
        return len(os.listdir(bpy.path.abspath(self.folder)))


# ---------------------------------------------------------------------------- #
#                             Collection Variations                            #
# ---------------------------------------------------------------------------- #


class PackShotterCollectionVariations(PackShotterVariationsNode):
    bl_idname = "PackShotterCollectionVariations"
    bl_label = "Collection Variations"
    bl_icon = 'GROUP'

    collection: bpy.props.PointerProperty(
        type=bpy.types.Collection, name="Collection")

    def draw_buttons(self, context, layout):
        layout.prop(self, "collection")

    def apply_variation(self, index):
        for i, child in enumerate(self.collection.children):
            child.hide_render = False if i == index else True

    def revert_variation(self):
        for i, child in enumerate(self.collection.children):
            child.hide_render = False

    def get_variation_name(self, index):
        return self.collection.children[index].name

    def get_num_variations(self):
        return len(self.collection.children)


# ---------------------------------------------------------------------------- #
#                                Mesh Variations                               #
# ---------------------------------------------------------------------------- #


class MeshVariationsMesh(bpy.types.PropertyGroup):
    value: bpy.props.PointerProperty(type=bpy.types.Mesh)


class AddMeshVariationsMesh(bpy.types.Operator):
    bl_idname = "packshotter.add_mesh_variations_mesh"
    bl_label = "Add"
    bl_icon = 'PLUS'

    def invoke(self, context, event):
        self.node = context.node
        return self.execute(context)

    def execute(self, context):
        self.node.meshes.add()
        return {'FINISHED'}


class RemoveMeshVariationsMesh(bpy.types.Operator):
    bl_idname = "packshotter.remove_mesh_variations_mesh"
    bl_label = "Clear"
    bl_icon = 'MINUS'

    def invoke(self, context, event):
        self.node = context.node
        return self.execute(context)

    def execute(self, context):
        self.node.meshes.clear()
        return {'FINISHED'}


class MESH_UL_meshes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "value", text="", emboss=True, icon_value=icon)


class PackShotterMeshVariationsNode(PackShotterVariationsNode):
    bl_idname = "PackShotterMeshVariationsNode"
    bl_label = "Mesh Variations (WIP)"
    bl_icon = 'FILE_IMAGE'

    obj: bpy.props.PointerProperty(type=bpy.types.Object, name="Object",
                                   description="The object that will have it's mesh changed for different variations")
    meshes: bpy.props.CollectionProperty(
        type=MeshVariationsMesh, name="Meshes")
    active_mesh: bpy.props.IntProperty(default=0)

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")
        self.outputs.new('NodeSocketVirtual', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, "obj")
        layout.template_list(
            "MESH_UL_meshes", "", self, "meshes", self, "active_mesh")
        layout.operator(AddMeshVariationsMesh.bl_idname)
        layout.operator(RemoveMeshVariationsMesh.bl_idname)

    def apply_variation(self, index):
        self._tmp_mesh = self.obj.data
        self.obj.data = self.meshes[index].value
    
    def revert_variation(self):
        self.obj.data = self._tmp_mesh

    def get_variation_name(self, index):
        return self.meshes[index].value.name

    def get_num_variations(self):
        return len(self.meshes)


# ---------------------------------------------------------------------------- #
#                            Registration Constants                            #
# ---------------------------------------------------------------------------- #


category = PackShotterNodeCategory("VARIATIONS", "Variations", items=[
    nodeitems_utils.NodeItem(PackShotterImageVariationsNode.bl_idname),
    nodeitems_utils.NodeItem(PackShotterCollectionVariations.bl_idname),
    nodeitems_utils.NodeItem(PackShotterMeshVariationsNode.bl_idname),
])


REGISTER_CLASSES = (
    PackShotterImageVariationsNode,
    PackShotterCollectionVariations,
    MeshVariationsMesh,
    AddMeshVariationsMesh,
    RemoveMeshVariationsMesh,
    MESH_UL_meshes,
    PackShotterMeshVariationsNode,
)

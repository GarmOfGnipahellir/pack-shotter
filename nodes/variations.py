import os
import bpy
import nodeitems_utils
from .common import PackShotterNode, PackShotterNodeCategory


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

    def apply_variation(self, index):
        raise NotImplementedError

    def get_variation_name(self, index):
        raise NotImplementedError

    def get_num_variations(self):
        return 0


class PackShotterImageVariationsNode(PackShotterVariationsNode):
    bl_idname = "PackShotterImageVariationsNode"
    bl_label = "Image Variation"
    bl_icon = 'FILE_IMAGE'
    bl_width_default = 200

    image: bpy.props.PointerProperty(type=bpy.types.Image, name="Image",
                                     description="The image that wil have it's file changed for different variations")
    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The folder which contains the image variations")

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")
        self.outputs.new('NodeSocketVirtual', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, "image")
        layout.prop(self, "folder")

    def apply_variation(self, index):
        file = os.listdir(bpy.path.abspath(self.folder))[index]
        self.image.filepath = os.path.join(self.folder, file)

    def get_variation_name(self, index):
        file = os.listdir(bpy.path.abspath(self.folder))[index]
        return bpy.path.display_name(file)

    def get_num_variations(self):
        return len(os.listdir(bpy.path.abspath(self.folder)))


category = PackShotterNodeCategory("VARIATIONS", "Variations", items=[
    nodeitems_utils.NodeItem(PackShotterImageVariationsNode.bl_idname)
])


REGISTER_CLASSES = (PackShotterImageVariationsNode,)

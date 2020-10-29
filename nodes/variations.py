import bpy
import nodeitems_utils
from .common import PackShotterNode, PackShotterNodeCategory


class PackShotterVariationsNode(PackShotterNode):
    pass


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
        # self.inputs.new('NodeSocketVirtual', "Input")
        self.outputs.new('NodeSocketVirtual', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, "image")
        layout.prop(self, "folder")


category = PackShotterNodeCategory("VARIATIONS", "Variations", items=[
    nodeitems_utils.NodeItem(PackShotterImageVariationsNode.bl_idname)
])


REGISTER_CLASSES = (PackShotterImageVariationsNode,)

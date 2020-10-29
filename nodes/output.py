import bpy
import nodeitems_utils
from .common import PackShotterNode, PackShotterNodeCategory
from ..operators import render


class PackShotterRenderNode(PackShotterNode):
    bl_idname = "PackShotterRenderNode"
    bl_label = "Render"
    bl_icon = 'RENDER_STILL'
    bl_width_default = 200

    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The output folder")

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")

    def draw_buttons(self, context, layout):
        layout.prop(self, "folder")
        layout.operator(render.PackShotterRender.bl_idname)


category = PackShotterNodeCategory("OUTPUT", "Output", items=[
    nodeitems_utils.NodeItem(PackShotterRenderNode.bl_idname)
])


REGISTER_CLASSES = (PackShotterRenderNode,)

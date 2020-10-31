import bpy
import nodeitems_utils
from .common import PackShotterNode, PackShotterNodeCategory
from ..operators import render


class PackShotterRenderNode(PackShotterNode):
    bl_idname = "PackShotterRenderNode"
    bl_label = "Render"
    bl_icon = 'RENDER_STILL'

    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The output folder")

    scene: bpy.props.PointerProperty(
        type=bpy.types.Scene, name="Scene", description="The scene to render")

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")

    def draw_buttons(self, context, layout):
        layout.prop(self, "folder")
        layout.prop(self, "scene")
        layout.operator(render.PackShotterRender.bl_idname)


category = PackShotterNodeCategory("OUTPUT", "Output", items=[
    nodeitems_utils.NodeItem(PackShotterRenderNode.bl_idname)
])


REGISTER_CLASSES = (PackShotterRenderNode,)

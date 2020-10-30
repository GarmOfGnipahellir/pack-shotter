import bpy


class PackShotterSocket(bpy.types.NodeSocket):
    pass


class VariationsSocket(PackShotterSocket):
    bl_idname = "ps_VariationsSocket"

    def draw(self, context, layout, node, text):
        layout.label(text = text)

    def draw_color(self, context, node):
        return [1, 1, 1, 1]


REGISTER_CLASSES = (VariationsSocket,)

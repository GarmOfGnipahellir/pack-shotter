import bpy


class PackShotterSocket(bpy.types.NodeSocket):
    def draw(self, context, layout, node, text):
        layout.label(text=text)


class VariationsSocket(PackShotterSocket):
    bl_idname = "ps_VariationsSocket"

    def draw_color(self, context, node):
        return [1, 1, 1, 1]


class FilesSocket(PackShotterSocket):
    bl_idname = "ps_FilesSocket"

    def draw_color(self, context, node):
        return [1, 0, 0, 1]


REGISTER_CLASSES = (
    VariationsSocket,
    FilesSocket,
)

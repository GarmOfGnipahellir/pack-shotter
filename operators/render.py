import os
import bpy


class PackShotterRender(bpy.types.Operator):
    bl_idname = "packshotter.render"
    bl_label = "Render"

    def invoke(self, context, event):
        self.node = context.node
        return self.execute(context)

    def execute(self, context):
        input_node = self.node.inputs[0].links[0].from_node

        self._render_recursive(input_node, [])

        return {'FINISHED'}

    def _render_recursive(self, variation_node, names):
        try:
            input_node = variation_node.inputs[0].links[0].from_node
        except Exception:
            input_node = None

        for i in variation_node:
            variation_node.apply_variation(i)
            name = variation_node.get_variation_name(i)
            new_names = names.copy()
            new_names.append(name)
            if input_node is not None:
                self._render_recursive(input_node, new_names)
            else:
                blend_name = bpy.path.display_name(bpy.data.filepath)
                bpy.context.scene.render.filepath = os.path.join(
                    self.node.folder, f"{blend_name}_{'_'.join(new_names)}.png")
                bpy.ops.render.render(write_still=True)


REGISTER_CLASSES = (PackShotterRender,)

import os
import bpy


class PackShotterRender(bpy.types.Operator):
    bl_idname = "packshotter.render"
    bl_label = "Render"

    #node: nodes.output.PackShotterRenderNode

    def invoke(self, context, event):
        self.node = context.node

        # for each variation in input
        #   change variation setting
        #   for each variation in variation input
        #       change variation setting
        #
        #       ...
        #
        #           render image

        return self.execute(context)

    def execute(self, context):
        input_node = self.node.inputs[0].links[0].from_node

        folder_abspath = bpy.path.abspath(input_node.folder)

        dir_content = os.listdir(folder_abspath)

        for file in dir_content:
            blend_name = bpy.path.display_name(bpy.data.filepath)
            file_name = bpy.path.display_name(file)
            file_relpath = bpy.path.relpath(os.path.join(folder_abspath, file))

            context.scene.render.filepath = os.path.join(
                self.node.folder, f"{blend_name}_{file_name}.png")
            input_node.image.filepath = file_relpath
            bpy.ops.render.render(write_still=True)

            print("done", file_name, file_relpath)

        return {'FINISHED'}


REGISTER_CLASSES = (PackShotterRender,)

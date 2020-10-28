import os
import bpy
import nodeitems_utils

bl_info = {
    "name": "Pack Shotter",
    "description": "A suite of tools for generating similar images with alot of variations.",
    "author": "Henrik Melsom",
    "version": (1, 7, 0),
    "blender": (2, 90, 0),
    "support": "COMMUNITY",
    "category": "Generic"
}


class PackShotterNodeTree(bpy.types.NodeTree):
    bl_idname = "PackShotterNodeTree"
    bl_label = "Pack Shotter"
    bl_icon = 'RENDERLAYERS'


class PackShotterNode(bpy.types.Node):
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == PackShotterNodeTree.bl_idname


class PackShotterImageVariationsNode(PackShotterNode):
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


class PackShotterRenderNode(PackShotterNode):
    bl_idname = "PackShotterRenderNode"
    bl_label = "Render"
    bl_icon = 'RENDER_STILL'
    bl_width_default = 100

    image: bpy.props.PointerProperty(type=bpy.types.Image, name="Image",
                                     description="The image that wil have it's file changed for different variations")
    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The folder which contains the image variations")

    def init(self, context):
        self.inputs.new('NodeSocketVirtual', "Input")

    def draw_buttons(self, context, layout):
        layout.operator(PackShotterRender.bl_idname)


class PackShotterNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == PackShotterNodeTree.bl_idname


node_categories = [
    PackShotterNodeCategory("OUTPUT", "Output", items=[
        nodeitems_utils.NodeItem(PackShotterRenderNode.bl_idname)
    ]),
    PackShotterNodeCategory("VARIATIONS", "Variations", items=[
        nodeitems_utils.NodeItem(PackShotterImageVariationsNode.bl_idname)
    ])
]


class PackShotterVariation(bpy.types.PropertyGroup):
    image: bpy.props.PointerProperty(type=bpy.types.Image, name="Image",
                                     description="The image that wil have it's file changed for different variations")
    folder: bpy.props.StringProperty(
        subtype='DIR_PATH', name="Folder", description="The folder which contains the image variations")


class PackShotterRender(bpy.types.Operator):
    bl_idname = "packshotter.render"
    bl_label = "Render"

    node: PackShotterRenderNode

    def invoke(self, context, event):
        self.node = context.node

        current_node = self.node
        while current_node.inputs[0] != None and len(current_node.inputs[0].links) > 0:
            current_node = current_node.inputs[0].links[0].from_node

            print(current_node)
        
        # for each variation in input
        #   change variation setting
        #   for each variation in variation input
        #       change variation setting
        #
        #       ...
        # 
        #           render image


        return {'FINISHED'}
        return self.execute(context)

    def execute(self, context):
        image = context.scene.packshotter_variation.image

        folder_abspath = bpy.path.abspath(
            context.scene.packshotter_variation.folder)

        dir_content = os.listdir(folder_abspath)

        for file in dir_content:
            blend_name = bpy.path.display_name(bpy.data.filepath)
            file_name = bpy.path.display_name(file)
            file_relpath = bpy.path.relpath(os.path.join(folder_abspath, file))

            context.scene.render.filepath = f"//..\\Render\\{blend_name}_{file_name}.png"
            image.filepath = file_relpath
            bpy.ops.render.render(write_still=True)

            print("done", file_name, file_relpath)

        return {'FINISHED'}


class PackShotterPanel(bpy.types.Panel):
    bl_idname = "PACKSHOTTER_PT_PackShotter"
    bl_label = "Pack Shotter"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Pack Shotter"

    def draw(self, context):
        self.layout.prop(bpy.context.scene.packshotter_variation, 'image')
        self.layout.prop(bpy.context.scene.packshotter_variation, 'folder')
        self.layout.operator(PackShotterRender.bl_idname)


classes = (
    PackShotterNodeTree,
    PackShotterImageVariationsNode,
    PackShotterRenderNode,
    PackShotterVariation,
    PackShotterRender,
    PackShotterPanel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.packshotter_variation = bpy.props.PointerProperty(
        type=PackShotterVariation)

    nodeitems_utils.register_node_categories(
        "PACKSHOTTER_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("PACKSHOTTER_NODES")

    for c in classes:
        bpy.utils.unregister_class(c)

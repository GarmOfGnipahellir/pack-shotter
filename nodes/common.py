import bpy
import nodeitems_utils


class PackShotterNodeTree(bpy.types.NodeTree):
    bl_idname = "PackShotterNodeTree"
    bl_label = "Pack Shotter"
    bl_icon = 'RENDERLAYERS'


class PackShotterNode(bpy.types.Node):
    bl_width_default = 200
    
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == PackShotterNodeTree.bl_idname


class PackShotterNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == PackShotterNodeTree.bl_idname


REGISTER_CLASSES = (PackShotterNodeTree,)
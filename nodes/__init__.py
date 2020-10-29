import bpy
import nodeitems_utils
from ..utils import register_recursive, unregister_recursive
from . import common, variations, output


categories = [
    output.category,
    variations.category,
]


REGISTER_CLASSES = (
    common,
    variations,
    output,
)


def register():
    register_recursive(REGISTER_CLASSES)

    nodeitems_utils.register_node_categories(
        "PACKSHOTTER_NODES", categories)


def unregister():
    nodeitems_utils.unregister_node_categories("PACKSHOTTER_NODES")

    unregister_recursive(REGISTER_CLASSES)

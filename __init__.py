import os
import bpy
from .utils import register_recursive, unregister_recursive
from . import nodes, operators

bl_info = {
    "name": "Pack Shotter",
    "description": "A suite of tools for generating similar images with alot of variations.",
    "author": "Henrik Melsom",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "support": "COMMUNITY",
    "category": "Generic"
}


REGISTER_CLASSES = (
    nodes,
    operators,
)


def register():
    register_recursive(REGISTER_CLASSES)


def unregister():
    unregister_recursive(REGISTER_CLASSES)

## Blender Python Script for Leaves
###### created: 2022-05-28
###### updated: 2022-06-21

from bpy.types import Object
# don't import "bpy" directly

import utils

#######################################################################################################
## Leaf

#######################################################################################################
def _set_crease_leaf_to(object_name: str) -> None:
    utils.set_crease(object_name=object_name, verts=[0,2,5,8], value=0.4)

#######################################################################################################
def set_crease_leafs() -> None:
    for ob in utils.get_objects(type="MESH"):
        ob: Object
        if "levs_Leaf_" in ob.name:
            _set_crease_leaf_to(object_name=ob.name)

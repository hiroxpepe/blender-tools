## Blender Python Script for Morning Glory
###### created: 2022-07-02
###### updated: 2022-07-02

from typing import List
from typing import Tuple

from bpy.types import Object
from bpy.types import PoseBone
# don't import "bpy" directly
import bpy

import utils

# FIXME: クラス化
# base_plant: 
#           hide_from()
#           set_motion()
#           set_crease()

#######################################################################################################
## Leaf

#######################################################################################################
def _set_crease_leaf_to(object_name: str) -> None:
    utils.set_crease(object_name=object_name, verts=[2,3,7,16], value=0.4)

#######################################################################################################
def set_crease_leafs() -> None:
    for ob in utils.get_objects(type="MESH"):
        ob: Object
        if "mngr_Leaf_" in ob.name:
            _set_crease_leaf_to(object_name=ob.name)

#######################################################################################################
def _set_freestyle_petal_to(object_name: str) -> None:
    verts: List[int] = [0,2,4,6,7,8,9,11,14,15,16,17,18,20,21,23,24,26]
    utils.set_freestyle_face(object_name=object_name, verts=verts)

#######################################################################################################
def set_freestyle_petals() -> None:
    for ob in utils.get_objects(type="MESH"):
        ob: Object
        if "mngr_Petal_" in ob.name:
            utils.apply_subsurf(object_name=ob.name)
            _set_freestyle_petal_to(object_name=ob.name)

## Blender Python Script for Emily
###### created: 2022-05-13
###### updated: 2022-06-27

from typing import List
from typing import Tuple

from bpy.types import Object
# don't import "bpy" directly
import bpy

import utils
import armature

#######################################################################################################
## Head

#######################################################################################################
def set_crease_head() -> None:
    """Function to set crease to Head.

    Args:
        None
    Returns:
        None
    """
    utils.set_crease(object_name="emly_Head", verts=[72,75,76], value=1.0)

#######################################################################################################
def set_freestyle_face() -> None:
    verts: List[int] = [64,81,82,83,101,106]
    utils.set_freestyle_face(object_name="emly_Head", verts=verts)

#######################################################################################################
## Body

#### 左肩
# 1段目: 11頂点
body_verts_l1: List[int] = [1955,1957,1960,1961,2375,2377,3669,3670,3876,3877,3889]
# 2段目: 8頂点
body_verts_l2: List[int] = [407,408,409,657,1888,2371,2373,2385]
# 3段目: 7頂点
body_verts_l3: List[int] = [1887,1889,2372,3648,3872,3874,3886]
# 二の腕上部: 5頂点
body_verts_l4: List[int] = [386,387,1834,1837,1840]
# 二の腕中部: 15頂点
body_verts_l5: List[int] = [378,379,1832,1833,1835,1836,1838,1853,1855,3625,3626,3627,3633,3634,3635]

#### 右肩
# 1段目: 11頂点
body_verts_r1: List[int] = [2646,2647,2648,2651,3051,3052,4023,4024,4230,4231,4243]
# 2段目: 8頂点
body_verts_r2: List[int] = [747,748,749,975,2585,3046,3049,3061]
# 3段目: 7頂点
body_verts_r3: List[int] = [2584,2586,3048,4002,4226,4228,4240]
# 二の腕上部: 5頂点
body_verts_r4: List[int] = [726,727,2531,2534,2537]
# 二の腕中部: 11頂点
body_verts_r5: List[int] = [718,719,2529,2530,2532,2533,2536,2550,2552,3979,3980,3981,3987,3988,3989]

#######################################################################################################
def set_weight_body_upper_arm(
    value1: Tuple[float, float], 
    value2: Tuple[float, float], 
    value3: Tuple[float, float],
    value4: Tuple[float, float],
    value5: Tuple[float, float]
    ) -> None:
    """Function to set weight to UpperArm of Body.

    Args:
        value1 (string): the value of setting weight to vertex list of 1.
        value2 (string): the value of setting weight to vertex list of 2.
        value3 (string): the value of setting weight to vertex list of 3.
        value4 (string): the value of setting weight to vertex list of 4.
        value5 (string): the value of setting weight to vertex list of 5.
    Returns:
        None
    """
    object_name: str = "emly_Body"
    utils.apply_subsurf(object_name=object_name)
    #### 左:UpperArm
    # 1段目:0
    # 2段目:0
    # 3段目:0.55
    # 二の腕上部:0.75
    # 二の腕中部:1
    utils.set_weight(object_name=object_name, vertex_group_name="LeftUpperArm", verts=body_verts_l1, value=value1[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftUpperArm", verts=body_verts_l2, value=value2[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftUpperArm", verts=body_verts_l3, value=value3[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftUpperArm", verts=body_verts_l4, value=value4[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftUpperArm", verts=body_verts_l5, value=value5[0])
    #### 右:UpperArm
    # 1段目:0
    # 2段目:0
    # 3段目:0.55
    # 二の腕上部:0.75
    # 二の腕中部:1
    utils.set_weight(object_name=object_name, vertex_group_name="RightUpperArm", verts=body_verts_r1, value=value1[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightUpperArm", verts=body_verts_r2, value=value2[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightUpperArm", verts=body_verts_r3, value=value3[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightUpperArm", verts=body_verts_r4, value=value4[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightUpperArm", verts=body_verts_r5, value=value5[1])

#######################################################################################################
def set_weight_body_shoulder(
    value1: Tuple[float, float],
    value4: Tuple[float, float],
    value5: Tuple[float, float]
    ) -> None:
    """Function to set weight to Shoulder of Body.

    Args:
        value1 (string): the value of setting weight to vertex list of 1.
        value4 (string): the value of setting weight to vertex list of 4.
        value5 (string): the value of setting weight to vertex list of 5.
    Returns:
        None
    """
    object_name: str = "emly_Body"
    utils.apply_subsurf(object_name=object_name)
    #### 左:Shoulder
    # 1段目:0.55～1 ※場合による
    # -- 2段目:※保留:曲面固定での設定を活かす
    # -- 3段目:※保留:曲面固定での設定を活かす
    # 二の腕上部:0.1
    # 二の腕中部:0
    utils.set_weight(object_name=object_name, vertex_group_name="LeftShoulder", verts=body_verts_l1, value=value1[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftShoulder", verts=body_verts_l4, value=value4[0])
    utils.set_weight(object_name=object_name, vertex_group_name="LeftShoulder", verts=body_verts_l5, value=value5[0])
    #### 右:Shoulder
    # 1段目:0.55～1 ※場合による
    # -- 2段目:※保留:曲面固定での設定を活かす
    # -- 3段目:※保留:曲面固定での設定を活かす
    # 二の腕上部:0.1
    # 二の腕中部:0
    utils.set_weight(object_name=object_name, vertex_group_name="RightShoulder", verts=body_verts_r1, value=value1[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightShoulder", verts=body_verts_r4, value=value4[1])
    utils.set_weight(object_name=object_name, vertex_group_name="RightShoulder", verts=body_verts_r5, value=value5[1])

#######################################################################################################
## Skirt

#### 上端前
skirt_verts: List[int] = [48,62,181,183,185,186,219,220,282,283,300,301]

#######################################################################################################
def set_weight_skirt_skirt_base(value: float) -> None:
    object_name: str = "emly_Skirt"
    utils.apply_subsurf(object_name=object_name)
    utils.set_weight(object_name=object_name, vertex_group_name="SkirtBase", verts=skirt_verts, value=0.15)

#######################################################################################################
# for Addon

def set_crease() -> None:
    set_crease_head()

def set_freestyle() -> None:
    set_freestyle_face()

#######################################################################################################
## 引数のフレーム値から非表示にする関数
def hide_from(start_frame: int, value: bool = True) -> None:
    prefix: str = "emly_"
    for ob in bpy.data.objects:
        ob: Object
        if prefix in ob.name:
            ob.hide_viewport = value
            ob.keyframe_insert(data_path="hide_viewport", frame=start_frame)
            ob.hide_render = value
            ob.keyframe_insert(data_path="hide_render", frame=start_frame)

#######################################################################################################
## キーフレームを登録する関数
def keyframe_insert_hips(cut_duration: int) -> None:
    armature.keyframe_insert(armature_name="Emily", bone_name="emly_Hips", cut_duration=cut_duration)

#######################################################################################################
## ポーズモードでボーンを選択する関数
def select_bone_hips() -> None:
    armature.select_bone(armature_name="Emily", bone_name="emly_Hips")

## Blender Python Script for Orange
###### created: 2022-05-13
###### updated: 2022-06-27

from typing import Dict
from typing import List
from typing import Tuple

from bpy.types import Object
# don't import "bpy" directly
import bpy

import utils
import armature

#######################################################################################################
# Whisker

#######################################################################################################
def set_freestyle_whisker() -> None:
    utils.set_freestyle_face(object_name="orng_Whisker")

#######################################################################################################
## Body

#### 左:ねこくん:二の腕:移動する頂点Indexと移動する位置
body_verts_to_move_l: Dict[int, Tuple[float, float,float]] = {
    941: (14.3313, 48.0398, 1.7219),
    942: (14.2644, 49.5498, 2.3474),
    943: (14.3513, 47.4143, 0.2119),
    944: (14.2782, 48.0398, -1.2982),
    945: (14.2083, 49.5498, -1.9237),
    946: (14.1953, 51.0599, -1.2982),
    947: (14.1968, 51.6854, 0.2119),
    948: (14.2076, 51.0599, 1.7219),
    1635: (14.2998, 48.7335, 2.1826),
    1636: (14.3521, 47.5791, 1.0282),
    1637: (14.3221, 47.5791, -0.6044),
    1638: (14.2371, 48.7335, -1.7589),
    1639: (14.1966, 50.3661, -1.7589),
    1640: (14.1961, 51.5206, -0.6044),
    1641: (14.1982, 51.5206, 1.0282),
    1642: (14.2313, 50.3661, 2.1826),
}
#### 右:ねこくん:二の腕:移動する頂点Indexと移動する位置
body_verts_to_move_r: Dict[int, Tuple[float, float,float]] = {
    1401: (-14.2644, 49.5498, 2.3474),
    1402: (-14.3313, 48.0398, 1.7219),
    1403: (-14.3513, 47.4143, 0.2119),
    1404: (-14.2782, 48.0398, -1.2982),
    1405: (-14.2083, 49.5498, -1.9237),
    1406: (-14.1953, 51.0599, -1.2982),
    1407: (-14.1968, 51.6854, 0.2119),
    1408: (-14.2076, 51.0599, 1.7219),
    1869: (-14.2998, 48.7335, 2.1826),
    1870: (-14.3521, 47.5791, 1.0282),
    1871: (-14.3221, 47.5791, -0.6044),
    1872: (-14.2371, 48.7335, -1.7589),
    1873: (-14.1966, 50.3661, -1.7589),
    1874: (-14.1961, 51.5206, -0.6044),
    1875: (-14.1982, 51.5206, 1.0282),
    1876: (-14.2313, 50.3661, 2.1826),
}

#######################################################################################################
def merge_verts_upper_arm() -> None:
    # 曲面適用
    utils.apply_subsurf(object_name="orng_Body")
    ### 二の腕の頂点を外側に向けて移動
    utils.move_vertex(object_name="orng_Body", data=body_verts_to_move_l)
    utils.move_vertex(object_name="orng_Body", data=body_verts_to_move_r)
    ### 頂点のマージ
    utils.remove_double_vertices(object_name="orng_Body")

#### 統合後:左:二の腕
body_verts_union_l: List[int] = [237,238,239,240,241,242,243,921,923,925,927,929,931,933,934,935]

#### 統合後:右:二の腕
body_verts_union_r: List[int] = [461,462,463,1375,1377,1381,1383,1384,1385,1386,1387,1388,1841,1842,1843,1844]

#######################################################################################################
def set_weight_body_shoulder_support(value: Tuple[float, float]) -> None:
    #### 左:ShoulderSupport
    # 0
    utils.set_weight(object_name="orng_Body", vertex_group_name="LeftShoulderSupport", verts=body_verts_union_l, value=value[0])
    #### 右:ShoulderSupport
    # 0
    utils.set_weight(object_name="orng_Body", vertex_group_name="RightShoulderSupport", verts=body_verts_union_r, value=value[1])

#######################################################################################################
def set_weight_body_upper_arm(value: Tuple[float, float]) -> None:
    #### 左:UpperArm
    # 1
    utils.set_weight(object_name="orng_Body", vertex_group_name="LeftUpperArm", verts=body_verts_union_l, value=value[0])
    #### 右:UpperArm
    # 1
    utils.set_weight(object_name="orng_Body", vertex_group_name="RightUpperArm", verts=body_verts_union_r, value=value[1])

#######################################################################################################
def set_weight_body_upper_chest(value: Tuple[float, float]) -> None:
    #### UpperChest
    # 0
    utils.set_weight(object_name="orng_Body", vertex_group_name="UpperChest", verts=body_verts_union_l, value=value[0])
    utils.set_weight(object_name="orng_Body", vertex_group_name="UpperChest", verts=body_verts_union_r, value=value[1])

#######################################################################################################
# for Addon

def set_crease() -> None:
    return # TBA

def set_freestyle() -> None:
    set_freestyle_whisker()

#######################################################################################################
## 引数のフレーム値から非表示にする関数
def hide_from(start_frame: int, value: bool = True) -> None:
    prefix: str = "orng_"
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
    armature.keyframe_insert(armature_name="Orange", bone_name="orng_Hips", cut_duration=cut_duration)

#######################################################################################################
## ポーズモードでボーンを選択する関数
def select_bone_hips() -> None:
    armature.select_bone(armature_name="Orange", bone_name="orng_Hips")

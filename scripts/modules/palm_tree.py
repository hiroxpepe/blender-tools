## Blender Python Script for Palm_Tree
###### created: 2022-06-11
###### updated: 2022-06-25

from typing import List
from typing import Tuple
import random

from bpy.types import Object
from bpy.types import PoseBone
# don't import "bpy" directly
import bpy

import utils
import armature

_palm_tree_fps: int = 24

#######################################################################################################
## ボーンに動きをつける関数
def set_motion(frame_end: int) -> None:
    object_list: List[Object] = utils.get_objects(type="ARMATURE")
    for ob in object_list:
        ob: Object
        if "Palm_Tree" in ob.name:
            armature.rename_bones(object_name=ob.name, prefix="plmt")
            bone_name: str = "plmt_Bone1"
            data_path: str = "rotation_euler"
            ob: Object = bpy.data.objects[ob.name]
            bpy.context.view_layer.objects.active = ob
            pose_bone: PoseBone = bpy.context.active_object.pose.bones[bone_name]
            pose_bone.rotation_mode = "ZXY"
            # set init rotation_euler
            pose_bone.keyframe_insert(data_path=data_path, frame=0, group=bone_name)
            pose_bone.keyframe_insert(data_path=data_path, frame=frame_end + 1, group=bone_name)
            # hold init rotation_euler value
            rotation_euler: List[float] = pose_bone.rotation_euler
            orig_rotation_euler: Tuple[float, ...] = (rotation_euler.x, rotation_euler.y, rotation_euler.z)
            # フレームの長さを分割してキーフレームを設定するタイミングを作成する
            frame_duration: int = _palm_tree_fps * 1 # 1秒ごと
            count: int = int(frame_end / frame_duration)
            for idx in range(count):
                idx: int
                pose_bone.rotation_euler.x = orig_rotation_euler[0] + float(random.randint(-7, 7) / 100)
                pose_bone.rotation_euler.y = orig_rotation_euler[1] + float(random.randint(-7, 7) / 100)
                pose_bone.rotation_euler.z = orig_rotation_euler[2] + float(random.randint(-7, 7) / 100)
                insert_frame: int = 1 + (frame_duration * idx)
                insert_frame += random.randint(-3, 3) # random value of timing
                pose_bone.keyframe_insert(data_path=data_path, frame=insert_frame, group=bone_name)

#######################################################################################################
## 引数のフレーム値から非表示にする関数
def hide_from(start_frame: int, value: bool = True) -> None:
    prefix: str = "plmt_"
    for ob in bpy.data.objects:
        ob: Object
        if prefix in ob.name:
            ob.hide_viewport = value
            ob.keyframe_insert(data_path="hide_viewport", frame=start_frame)
            ob.hide_render = value
            ob.keyframe_insert(data_path="hide_render", frame=start_frame)

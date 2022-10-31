## Blender Python Script for Armature
###### created: 2022-05-25
###### updated: 2022-08-20

from typing import List
from typing import Tuple
import random

from bpy.types import Action
from bpy.types import ActionFCurves
from bpy.types import Area
from bpy.types import Armature
from bpy.types import Bone
from bpy.types import FCurve
from bpy.types import Keyframe
from bpy.types import Object
from bpy.types import Pose
from bpy.types import PoseBone
# don't import "bpy" directly
import bpy # FIXME:

import utils

#######################################################################################################
## ボーン名から回転設定に関するパターン数値を取得する関数
def _get_pattern(bone_name: str) -> int:
    """Function to get the pattern value from Bone name of Blender.

    Args:
        name (string): the name of Bone.
    Returns:
        pattern value (int): the value of pattern.
    """
    if bone_name == "Hips" or bone_name == "Spine" or bone_name == "Chest" or bone_name == "UpperChest" or \
        bone_name == "Neck" or bone_name == "Head" or bone_name == "Head_end" or \
        bone_name == "Hair" or bone_name == "HatBase" or bone_name == "HatMid" or bone_name == "HatTop":
        return 1
    if bone_name == "LeftUpperLeg" or bone_name == "RightUpperLeg":
        return 2
    if bone_name == "LeftLowerLeg" or bone_name == "LeftFoot" or bone_name == "LeftToeBase" or bone_name == "LeftToeEnd" or \
        bone_name == "RightLowerLeg" or bone_name == "RightFoot" or bone_name == "RightToeBase" or bone_name == "RightToeEnd":
        return 3
    if bone_name == "LeftShoulder" or bone_name == "LeftUpperArm" or bone_name == "LeftLowerArm" or bone_name == "LeftHand" or \
        bone_name == "LeftThumbProximal" or bone_name == "LeftThumbIntermediate" or bone_name == "LeftThumbDistal" or \
        bone_name == "LeftIndexProximal" or bone_name == "LeftIndexIntermediate" or bone_name == "LeftIndexDistal" or \
        bone_name == "LeftMiddleProximal" or bone_name == "LeftMiddleIntermediate" or bone_name == "LeftMiddleDistal" or \
        bone_name == "LeftRingProximal" or bone_name == "LeftRingIntermediate" or bone_name == "LeftRingDistal" or \
        bone_name == "LeftLittleProximal" or bone_name == "LeftLittleIntermediate" or bone_name == "LeftLittleDistal":
        return 4
    if bone_name == "RightShoulder" or bone_name == "RightUpperArm" or bone_name == "RightLowerArm" or bone_name == "RightHand" or \
        bone_name == "RightThumbProximal" or bone_name == "RightThumbIntermediate" or bone_name == "RightThumbDistal" or \
        bone_name == "RightIndexProximal" or bone_name == "RightIndexIntermediate" or bone_name == "RightIndexDistal" or \
        bone_name == "RightMiddleProximal" or bone_name == "RightMiddleIntermediate" or bone_name == "RightMiddleDistal" or \
        bone_name == "RightRingProximal" or bone_name == "RightRingIntermediate" or bone_name == "RightRingDistal" or \
        bone_name == "RightLittleProximal" or bone_name == "RightLittleIntermediate" or bone_name == "RightLittleDistal":
        return 5
    if bone_name == "LeftBustBase" or bone_name == "RightBustBase":
        return 6
    if bone_name == "TailBase" or bone_name == "TailCenter" or bone_name == "TailMid" or bone_name == "TailTop":
        return 7

#######################################################################################################
## オイラー角回転モードを設定する文字列を取得する関数
def _get_rotation_mode(bone_name: str) -> str:
    """Function to get the rotation_mode value of Blender from Bone name of Blender.

    Args:
        bone_name (string): the name of Bone.
    Returns:
        rotation_mode value (string): the value of rotation_mode.
    """
    pattern = _get_pattern(bone_name=bone_name)
    if pattern == 1:
        return "ZXY"
    if pattern == 2:
        return "ZXY"
    if pattern == 3:
        return "ZXY"
    if pattern == 4:
        return "ZYX"
    if pattern == 5:
        return "ZYX"
    if pattern == 6:
        return "ZXY"
    if pattern == 7:
        return "ZXY"

#######################################################################################################
## 対象オブジェクトのボーンの回転方式をオイラー角に変更する関数
def set_rotation_mode(object_name: str) -> None:
    # get bones of the object
    bones: List[Bone] = utils.get_active_object_bones(object_name=object_name)
    # get the pose of the object
    pose: Pose = utils.get_active_object_pose(object_name=object_name)
    # set the rotation_mode to the bone
    for bone in bones: # bpy.data.armatures["Orange"].bones["Hips"]
        bone: Bone
        rotation_mode: str = _get_rotation_mode(bone.name)
        if rotation_mode != None:
            pose_bone: PoseBone = pose.bones[bone.name] # bpy.data.objects["Orange"].pose.bones["Hips"]
            pose_bone.rotation_mode = rotation_mode

#######################################################################################################
## 対象オブジェクトのボーンにプリフィックスを付加する関数
def rename_bones(object_name: str, prefix: str) -> None:
    # get bones of the object
    bones: List[Bone] = utils.get_active_object_bones(object_name=object_name)
    # set prefix str to the bone name
    for bone in bones:
        bone: Bone
        bone.name = f"{prefix}_{bone.name}"

#######################################################################################################
## 補間カーブを一定にする関数
def set_curve_constant() -> None:
    action_list: List[str] = ["EmilyAction", "OrangeAction"] # FIXME:
    for action_name in action_list:
        action_name: str
        fcurves: ActionFCurves = bpy.data.actions[action_name].fcurves
        for fcurve in fcurves:
            fcurve: FCurve
            for keyframe in fcurve.keyframe_points:
                keyframe: Keyframe
                keyframe.interpolation = "CONSTANT"

#######################################################################################################
## キーフレームを登録する関数 ※現在: Hipsのみ想定
def keyframe_insert(armature_name: str, bone_name: str, cut_duration: int) -> None:
    fps: float = 24.0 # FIXME:
    ob: Object = bpy.data.objects[armature_name]
    bpy.context.view_layer.objects.active = ob
    pose_bone: PoseBone = bpy.context.active_object.pose.bones[bone_name]
    pose_bone.rotation_mode = "ZXY" # FIXME: Hipsのみ想定
    # カット開始の値を保存
    rotation_euler: List[float] = pose_bone.rotation_euler
    location: List[float] = pose_bone.location
    orig_rotation_euler: Tuple[float, ...] = (rotation_euler.x, rotation_euler.y, rotation_euler.z)
    orig_location: Tuple[float, ...] = (location.x, location.y, location.z)
    # カット開始のキーフレーム挿入
    pose_bone.keyframe_insert(data_path="location")
    pose_bone.keyframe_insert(data_path="rotation_euler")
    # 開始・終了フレーム取得して終了フレームへ移動
    start_frame: int = utils.get_current_frame()
    end_frame: int = start_frame + ((cut_duration * fps) - 1)
    utils.set_current_frame(frame=end_frame)
    # 回転・位置に開始時の値を適用
    pose_bone.rotation_euler = orig_rotation_euler
    pose_bone.location = orig_location
    # カット終了のキーフレーム挿入
    pose_bone.keyframe_insert(data_path="location")
    pose_bone.keyframe_insert(data_path="rotation_euler")
    # 再描画
    for area in bpy.context.window.screen.areas:
        area: Area
        print(area.type)
        if area.type == "DOPESHEET_EDITOR":
            area.tag_redraw()

#######################################################################################################
## ポーズモードでボーンを選択する関数
def select_bone(armature_name: str, bone_name: str) -> None:
    bpy.ops.object.mode_set(mode="OBJECT")
    ob: Object = bpy.data.objects[armature_name]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="POSE")
    armature: Armature = bpy.data.objects[armature_name].data
    bone: Bone = armature.bones[bone_name]
    bone.select = True

#######################################################################################################
## 呼吸アニメを設定する関数

## ボーンごとのキャラの呼吸アニメを設定する関数
def _set_bone_breath_motion(name_tuple: Tuple[str, str], cut_duration: int, cut_start_frame: int, bone_name: str, rotation_mode: str,  rotation_euler_tuple: Tuple[float, ...]) -> None:
    fps: float = 24.0 # FIXME:
    prefix: str = name_tuple[0]
    object_name: str = name_tuple[1]
    # ボーン選択
    bone_name: str = f"{prefix}_{bone_name}"
    data_path: str = "rotation_euler"
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    pose_bone: PoseBone = bpy.context.active_object.pose.bones[bone_name]
    pose_bone.rotation_mode = rotation_mode
    # このカットのフレームを選択する
    utils.set_current_frame(cut_start_frame)
    # hold init rotation_euler value
    rotation_euler: List[float] = pose_bone.rotation_euler
    orig_rotation_euler: Tuple[float, ...] = (rotation_euler.x, rotation_euler.y, rotation_euler.z)
    # フレームの長さを分割してキーフレームを設定するタイミングを作成する
    frame_duration: int = fps * 2 # 2秒ごと
    count: int = int(cut_duration * fps / frame_duration) + 1 # +1 は例えば 2秒カットで 2回処理が必要なため
    timing: motion_timing = motion_timing()
    for idx in range(count):
        idx: int
        pram: Tuple[int, int] = timing.next()
        frame: int = pram[0]
        pattern: int = pram[1]
        shift: int = 1 # カットフレに挿入する調整値
        if pattern == 0:
            pose_bone.rotation_euler.x = orig_rotation_euler[0]
            pose_bone.rotation_euler.y = orig_rotation_euler[1]
            pose_bone.rotation_euler.z = orig_rotation_euler[2]
            if idx != 0: # カット開始以外
                shift += 1
        else:
            pose_bone.rotation_euler.x = orig_rotation_euler[0] + rotation_euler_tuple[0]
            pose_bone.rotation_euler.y = orig_rotation_euler[1] + rotation_euler_tuple[1]
            pose_bone.rotation_euler.z = orig_rotation_euler[2] + rotation_euler_tuple[2]
            shift += 1 # キーポーズは -1 フレに挿入
        pose_bone.keyframe_insert(data_path=data_path, frame=cut_start_frame + frame - shift, group=bone_name)

## カットごとのキャラの呼吸アニメを設定する関数
def _set_cut_breath_motion(name_tuple: Tuple[str, str], cut_duration: int, cut_start_frame: int) -> None:
    # ボーンごとの設定
    bone_name: str = "Spine"
    rotation_euler_tuple: Tuple[float, ...] = (-0.15, 0, 0)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "Head"
    rotation_euler_tuple: Tuple[float, ...] = (0.20, 0, 0)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "LeftShoulder"
    rotation_euler_tuple: Tuple[float, ...] = (0, 0, 0.20)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "LeftUpperArm"
    rotation_euler_tuple: Tuple[float, ...] = (0, 0, -0.20)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "RightShoulder"
    rotation_euler_tuple: Tuple[float, ...] = (0, 0, -0.20)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "RightUpperArm"
    rotation_euler_tuple: Tuple[float, ...] = (0, 0, 0.20)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )
    bone_name: str = "Hair"
    rotation_euler_tuple: Tuple[float, ...] = (0.10, 0.10, 0.10)
    _set_bone_breath_motion(
        name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame, 
        bone_name=bone_name, rotation_mode=_get_rotation_mode(bone_name=bone_name), rotation_euler_tuple=rotation_euler_tuple
    )

## キャラの呼吸アニメを設定する関数
def set_breath_motion(cut_duration_and_start_frame_list: List[Tuple[int, int]]) -> None:
    name_tuple_list: List[Tuple(str, str)] = [("emly", "Emily"), ("orng", "Orange")] # FIXME:
    # キャラごとのループ
    for name_tuple in name_tuple_list:
        name_tuple: Tuple[str, str]
        # カットごとのループ
        for idx, value in enumerate(cut_duration_and_start_frame_list):
            cut_duration: int = value[0]
            cut_start_frame: int = value[1]
            _set_cut_breath_motion(name_tuple=name_tuple, cut_duration=cut_duration, cut_start_frame=cut_start_frame)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Class
class motion_timing():
    """
    + タイミングを表現するクラス
        + next() メソッドを呼ぶたびに
            + 2秒感覚の frame 値を返す
            + 交互にパラメータ値を返す
    """
    ###################################################################################################
    # Constructor

    def __init__(self, fps: float = 24.0):
        self._fps: float = fps
        self._idx: int = 0
        self._pattern: int = 0

    ###################################################################################################
    # public Methods [verb]

    # 呼び出されるたびに開始フレーム値とパターン値を交互に返します
    def next(self) -> Tuple[int, int]:
        frame: int = 1 + int((self._fps * self._idx))
        pattern: int = self._pattern
        self._idx += 2 # idx インクリメント ※2秒ごと
        if self._pattern == 0: # パラメータ反転
            self._pattern = 1
        else:
            self._pattern = 0
        return (frame, pattern)

#######################################################################################################
### 単体テスト

import unittest

class Test_motion_timing(unittest.TestCase):
    # + カットの長さに応じて適切なタイミングを返す
    # * 2秒ごとに交互のパターン値を返す
    def test_motion_timing_next(self):
        obj = motion_timing()
        actual = obj.next()
        self.assertEqual((1, 0), actual) # 1回目 1フレ, 0ポーズ
        actual = obj.next()
        self.assertEqual((49, 1), actual) # 2回目 49フレ, 1ポーズ
        actual = obj.next()
        self.assertEqual((97, 0), actual) # 3回目 97フレ, 0ポーズ

class TestArmature(unittest.TestCase):
    def test_get_pattern_by_LeftShoulder(self):
        value1 = "LeftShoulder"
        expected = 4
        actual = _get_pattern(value1)
        self.assertEqual(expected, actual)

    def test_get_pattern_by_TailBase(self):
        value1 = "TailBase"
        expected = 7
        actual = _get_pattern(value1)
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

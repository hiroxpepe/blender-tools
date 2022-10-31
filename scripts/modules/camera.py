## Blender Python Script for Camera
###### created: 2022-05-30
###### updated: 2022-08-18

from typing import List
from typing import Tuple
from mathutils import Vector
import bpy # FIXME:
# don't import "bpy" directly
from bpy.types import ActionFCurves
from bpy.types import Area
from bpy.types import FCurve
from bpy.types import Keyframe
from bpy.types import Object

import utils

#######################################################################################################
## カメラの位置を返します
def _get_current_position() -> List[float]:
    camera: Object = bpy.data.objects["Camera"]
    location: List[float] = camera.location
    return location

#######################################################################################################
## カメラの回転を返します
def _get_current_rotation_euler() -> List[float]:
    camera: Object = bpy.data.objects["Camera"]
    rotation_euler: List[float] = camera.rotation_euler
    return rotation_euler

#######################################################################################################
## キーフレームを登録する関数
def keyframe_insert() -> None:
    camera: Object = bpy.data.objects["Camera"]
    bpy.context.view_layer.objects.active = camera
    camera.keyframe_insert(data_path="location")
    camera.keyframe_insert(data_path="rotation_euler")
    for area in bpy.context.window.screen.areas:
        area: Area
        print(area.type)
        if area.type == "DOPESHEET_EDITOR":
            area.tag_redraw()

#######################################################################################################
## キーフレームを削除する関数
def keyframe_delete() -> None:
    frame: int = utils.get_current_frame()
    camera: Object = bpy.data.objects["Camera"]
    bpy.context.view_layer.objects.active = camera
    camera.keyframe_delete(data_path="location", frame=frame)
    camera.keyframe_delete(data_path="rotation_euler", frame=frame)
    for area in bpy.context.window.screen.areas:
        area: Area
        print(area.type)
        if area.type == "DOPESHEET_EDITOR":
            area.tag_redraw()

#######################################################################################################
## 補間カーブを一定にする関数
def set_curve_constant() -> None:
    fcurves: ActionFCurves = bpy.data.actions["CameraAction"].fcurves
    for fcurve in fcurves:
        fcurve: FCurve
        for keyframe in fcurve.keyframe_points:
            keyframe: Keyframe
            keyframe.interpolation = "CONSTANT"

#######################################################################################################
## カメラを移動する関数
def come_from(vector: Vector, move_amount: float, frame_shift: int) -> None:
    # get current frame
    frame: int = utils.get_current_frame()
    # get the camera
    camera: Object = utils.get_default_camera()
    bpy.context.view_layer.objects.active = camera
    # 元々の位置・回転保存
    orig_location: Tuple[float, ...] = (camera.location.x, camera.location.y, camera.location.z) # Tuple は不変
    orig_rotation_euler: Tuple[float, ...] = (camera.rotation_euler.x, camera.rotation_euler.y, camera.rotation_euler.z) # Tuple は不変
    #print(f"orig_location: {list(orig_location)}")
    #print(f"orig_rotation_euler: {list(orig_rotation_euler)}")
    # 指定ベクトルに移動
    value: Vector = (vector[0] * move_amount, vector[1] * move_amount, vector[2] * move_amount) # ベクトル作成
    camera.select_set(True)
    bpy.ops.transform.translate(value=value, orient_type="NORMAL") # ノーマル方向に移動するモード
    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame) # 回転を追加してもそれほど効果的ではない模様
    # 元の位置・回転を追加
    camera.location = list(orig_location)
    camera.rotation_euler = list(orig_rotation_euler)
    #print(f"orig_location: {orig_location}")
    #print(f"orig_rotation_euler: {orig_rotation_euler}")
    camera.keyframe_insert(data_path="location", frame=(frame + frame_shift))
    camera.keyframe_insert(data_path="rotation_euler", frame=(frame + frame_shift))
    # TODO:
    # 補間カーブの調整が必要
    # + Python からでは個別のカーブ設定は無理な模様
    #     + 内部でC++実装の関数をコールしている
    #     + フレームが選択出来たら可能？
    #     + 費用対効果を考えて補間カーブは手動設定で運用
    # [bpy.ops.action.interpolation_type(type='BACK')](https://docs.blender.org/api/current/bpy.ops.action.html?highlight=interpolation_type#bpy.ops.action.interpolation_type)

#######################################################################################################
## 徐々に拡大する関数 ※対象オブジェクトにロック出来る？ 対応検討
def zoom_to(vector: Vector, move_amount: float, cut_duration: int) -> None:
    # 切り替え効果処理が完了した後
    # ズームイン・アウト方向にのみ対応
    # カットの長さが分かると良い
    #     + パラメータで指定する
    # 補間カーブを手動でリニアに設定しないといけない
    # get current frame
    frame: int = utils.get_current_frame()
    # get the camera
    camera: Object = utils.get_default_camera()
    bpy.context.view_layer.objects.active = camera
    # 指定ベクトルに移動
    value: Vector = (vector[0] * move_amount, vector[1] * move_amount, vector[2] * move_amount) # ベクトル作成
    camera.select_set(True)
    bpy.ops.transform.translate(value=value, orient_type="NORMAL") # ノーマル方向に移動するモード
    camera.keyframe_insert(data_path="location", frame=(frame + (cut_duration * 24) - 1)) # FIXME: 24FPS に依存
    camera.keyframe_insert(data_path="rotation_euler", frame=(frame + (cut_duration * 24) -1)) # FIXME: 24FPS に依存
